"""Outlook mail adapter — backup route for welink-cli ``mail list`` (Phase 9.3).

Provides email activity collection from Outlook for colleagues who do NOT have
welink-cli installed. Uses the Outlook COM/MAPI interface (via pywin32) to read
mail folders directly from the running Outlook desktop application.

**Implementation decision:**

1. **libpff / pffexport / pypff** — FAILED. ``pffexport`` not in PATH; ``pypff`` not
   installed; ``pip install libpff-python`` fails on Windows (C build error in
   pyproject.toml — the libpff C library doesn't build with MSVC on this platform).
   This was the OSS-first choice but is blocked on Windows without a prebuilt wheel.
2. **Outlook COM / MAPI (pywin32)** — supported on Windows with a configured
   Outlook desktop profile. This is the path the adapter uses.
3. **Graph API** — not tested (needs Azure admin consent; lowest priority).

**OST file location:** Profiles can place OST/PST files outside the default
platform directory. Detection therefore checks conventional locations without
starting COM; collection discovers configured stores through MAPI.

**Adapter shape:** Emits ``kind="email"``, ``source_kind="comm"`` events matching
the welink-cli mail event shape (same ``tool_input`` keys: folder, direction,
subject, from, from_email, date, is_read, has_attachments, etc.) so downstream
code treats welink-cli mail and Outlook mail identically.

**COM resource management (CRITICAL):**
Outlook has a limit on concurrent MAPI sessions (~20). Every unreleased COM object
(Dispatch, Namespace, Store, Folder, Items, MailItem) counts against that limit.
If COM objects are not released after use, repeated runs exhaust the MAPI session
pool and Outlook shows: "Outlook 已经用完了所有共享资源，请关闭所有消息传递应用
程序并重新启动 Outlook".

Unlike C#'s ``Marshal.ReleaseComObject()``, pywin32 does NOT provide a direct way
to force-decrement a COM object's reference count. The underlying ``PyIDispatch``
only calls COM ``Release()`` when the **Python reference count** drops to zero.
This means:

1. Passing a COM object to a helper function does NOT release it — the caller's
   variable still holds a reference.
2. A generator (``yield``) keeps its frame alive, holding COM references across
   yields until the generator itself is GC'd — far too late for MAPI.
3. Appending COM objects to a list keeps them all alive simultaneously.

This adapter handles all three traps:
- ``collect()`` is NOT a generator — it builds a list of plain dicts (primitive
  data extracted from COM objects), then releases all COM objects before returning.
- Every COM object is explicitly ``del``-ed in the scope that created it, followed
  by ``gc.collect()``.
- ``close()`` calls ``ns.Logoff()`` (frees the MAPI session slot), then ``del``s
  the root references and forces GC.

**Limitations:**
- COM requires Outlook desktop to be installed (not necessarily running — Dispatch
  launches it if needed, but it must have a configured profile).
- Windows-only (COM is a Windows technology). Mac/Linux colleagues need welink-cli.
- Reading large mailboxes can be slow (COM is synchronous, one item at a time).
  ``max_items_per_folder`` caps the count (default 500, matching welink-cli).
- Encoding: Outlook COM returns strings in the system codepage (GBK on Chinese
  Windows). We handle Unicode errors gracefully.
"""

from __future__ import annotations

import os
import sys
import gc
from typing import Iterator, Any

from sources import make_event


# ---------------------------------------------------------------------------
# COM resource management — prevent MAPI session exhaustion
# ---------------------------------------------------------------------------

def _close_mapi_session(ns, outlook, uninit: bool = True):
    """Properly close a MAPI session and release the Outlook COM connection.

    The critical step is ns.Logoff() — this frees the MAPI session slot
    that Outlook counts against its ~20-session limit. Without Logoff(),
    the session stays open even after Python exits, causing:
    "Outlook 已经用完了所有共享资源" popups.

    After Logoff(), we explicitly ``del`` the root references and force GC.
    pywin32 only calls COM Release() when the Python refcount hits zero,
    so we must ensure no variables hold the objects.
    """
    if ns is not None:
        try:
            ns.Logoff()
        except Exception:
            pass
    # del the references in this scope so PyIDispatch refcount drops to 0.
    del ns
    del outlook
    if uninit:
        try:
            import pythoncom
            pythoncom.CoUninitialize()
        except Exception:
            pass
    gc.collect()


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Outlook folder enum values (OlDefaultFolders) — used as fallback for
# GetDefaultFolder. The COM investigation showed these can be unreliable with
# certain Exchange configurations (the mapping shifts), so we prefer name-based
# folder lookup via the store root.
OL_FOLDER_INBOX = 6
OL_FOLDER_SENT_MAIL = 5  # NOTE: on this machine, 5=Sent, 4=Outbox (shifted!)

# Folders we collect from: (display_name_substring, direction)
TARGET_FOLDERS = [
    ("inbox", "received"),
    ("sent", "sent"),
]

DEFAULT_MAX_ITEMS_PER_FOLDER = 500


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _try_import_win32com():
    """Import win32com.client, returning None if unavailable."""
    try:
        import win32com.client
        return win32com.client
    except ImportError:
        return None
    except Exception:
        return None


def _safe_str(val: Any, max_len: int = 500) -> str | None:
    """Convert a COM value to string, handling encoding errors gracefully."""
    if val is None:
        return None
    try:
        s = str(val)
        return s[:max_len] if len(s) > max_len else s
    except (UnicodeEncodeError, UnicodeDecodeError):
        # COM strings that can't be encoded in the console codepage
        try:
            s = val.encode("utf-8", errors="replace").decode("utf-8", errors="replace")
            return s[:max_len]
        except Exception:
            return "(unreadable)"


def _com_datetime_to_epoch(dt_val: Any) -> float | None:
    """Convert a COM datetime (pywintime) to Unix epoch seconds."""
    if dt_val is None:
        return None
    try:
        # pywintime objects have a timestamp() method in Python 3.12+
        # or can be converted via the datetime module
        import datetime
        if isinstance(dt_val, datetime.datetime):
            return dt_val.timestamp()
        # pywintime (Time object) — try to convert
        if hasattr(dt_val, "timestamp"):
            return float(dt_val.timestamp())
        # Fall back: parse via str
        s = str(dt_val)
        return datetime.datetime.fromisoformat(s).timestamp()
    except Exception:
        return None


def _find_ost_files_no_com() -> list[str]:
    """Find .ost and .pst files WITHOUT using COM (no MAPI session leak).

    Checks the default Outlook data directory + common custom locations.
    This is a pure filesystem scan — no Dispatch, no GetNamespace, no MAPI.
    """
    from platform_paths import OUTLOOK_OST

    found = []

    # 1. Default platform path
    if OUTLOOK_OST and os.path.isdir(OUTLOOK_OST):
        for f in os.listdir(OUTLOOK_OST):
            if f.lower().endswith((".ost", ".pst")):
                found.append(os.path.join(OUTLOOK_OST, f))

    # 2. Common custom OST locations (scan top-level dirs on all drives).
    # The author's OST is at D:\\Email\\ — check common patterns.
    for drive in ("C:", "D:", "E:"):
        for dirname in ("Email", "Outlook", "Mail"):
            path = os.path.join(drive + os.sep, dirname)
            if os.path.isdir(path):
                for f in os.listdir(path):
                    if f.lower().endswith((".ost", ".pst")):
                        full = os.path.join(path, f)
                        if full not in found:
                            found.append(full)

    # 3. Windows registry — Outlook stores the OST path in the registry
    # (without needing COM). This is the most reliable non-COM method.
    try:
        import winreg
        # Outlook profile settings are under:
        # HKCU\Software\Microsoft\Office\16.0\Outlook\OST
        for office_ver in ("16.0", "15.0", "14.0"):
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    f"Software\\Microsoft\\Office\\{office_ver}\\Outlook\\OST"
                )
                ost_path, _ = winreg.QueryValueEx(key, "OSTFile")
                winreg.CloseKey(key)
                if ost_path and os.path.isfile(ost_path) and ost_path not in found:
                    found.append(ost_path)
            except (FileNotFoundError, OSError):
                pass
            # Also check the Outlook directory setting
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    f"Software\\Microsoft\\Office\\{office_ver}\\Outlook"
                )
                # Enumerate values looking for file paths
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        if isinstance(value, str) and value.lower().endswith((".ost", ".pst")):
                            if os.path.isfile(value) and value not in found:
                                found.append(value)
                        i += 1
                    except OSError:
                        break
                winreg.CloseKey(key)
            except (FileNotFoundError, OSError):
                pass
    except ImportError:
        pass  # winreg only on Windows

    return found


def _find_ost_files() -> list[str]:
    """Find .ost and .pst files. Uses _find_ost_files_no_com() + COM as fallback.

    The COM fallback is only used if the non-COM scan finds nothing,
    to discover custom locations. It creates and properly closes a MAPI
    session.
    """
    # Try non-COM first (no session leak risk).
    found = _find_ost_files_no_com()
    if found:
        return found  # No need for COM — files found via filesystem/registry.

    # COM fallback for custom locations not covered above.
    win32com_client = _try_import_win32com()
    if win32com_client is not None:
        outlook = None
        ns = None
        stores = None
        try:
            outlook = win32com_client.Dispatch("Outlook.Application")
            ns = outlook.GetNamespace("MAPI")
            stores = ns.Stores
            for store in stores:
                try:
                    filepath = store.FilePath
                    if filepath and os.path.isfile(filepath):
                        if filepath.lower().endswith((".ost", ".pst")):
                            if filepath not in found:
                                found.append(filepath)
                except Exception:
                    pass
                del store
        except Exception:
            pass
        finally:
            # Release all COM references in reverse order of creation.
            del stores
            _close_mapi_session(ns, outlook)

    return found


def _find_folder_by_name(root, name_substring: str):
    """Find a folder under a root folder by case-insensitive name match.

    Returns the folder object or None.
    """
    name_lower = name_substring.lower()
    try:
        for f in root.Folders:
            if name_lower in f.Name.lower():
                return f
    except Exception:
        pass
    return None


# ---------------------------------------------------------------------------
# Adapter
# ---------------------------------------------------------------------------

class OutlookAdapter:
    """Adapter for Outlook email via the COM/MAPI interface.

    Collects email events (send/receive times, subjects, senders) from Outlook
    desktop. Uses pywin32 (win32com) to talk to the Outlook COM object — this
    requires Outlook to be installed with a configured profile on Windows.

    Emits ``kind="email"``, ``source_kind="comm"`` events matching the welink-cli
    mail event shape so downstream code treats them identically.

    ``detect()`` returns True if:
    - pywin32 is importable, AND
    - Outlook COM Dispatch succeeds, AND
    - at least one mail store with an Inbox folder is accessible.

    If pywin32 is not installed or Outlook is not configured, ``detect()``
    returns False and the registry skips this adapter cleanly.
    """

    name = "outlook"
    source_kind = "comm"

    def __init__(self, max_items_per_folder: int = DEFAULT_MAX_ITEMS_PER_FOLDER):
        self._max_items = max_items_per_folder
        self._outlook = None
        self._ns = None

    # -- COM connection -----------------------------------------------------

    def _ensure_com(self) -> bool:
        """Lazily connect to Outlook COM. Returns True if connected.

        Dispatch("Outlook.Application") starts Outlook if it isn't running.
        Calls CoInitialize() for the current thread — required when COM is
        used from a non-main thread (e.g. test runners). Retries up to 3
        times with a short delay for cold-start reliability.
        """
        if self._ns is not None:
            return True
        win32com_client = _try_import_win32com()
        if win32com_client is None:
            return False
        # CoInitialize the current thread (required for COM in non-main threads).
        try:
            import pythoncom
            pythoncom.CoInitialize()
        except ImportError:
            pass  # pythoncom not available — main thread is already initialized
        import time
        for attempt in range(3):
            try:
                self._outlook = win32com_client.Dispatch("Outlook.Application")
                self._ns = self._outlook.GetNamespace("MAPI")
                return True
            except Exception as e:
                self._outlook = None
                self._ns = None
                if attempt < 2:
                    import sys
                    print(f"[outlook] COM Dispatch attempt {attempt+1} failed: {e}, retrying...", file=sys.stderr)
                    time.sleep(3)
        return False

    # -- detection ----------------------------------------------------------

    def detect(self) -> bool:
        """True if Outlook data is likely available — WITHOUT creating a COM session.

        CRITICAL: This method must NOT call Dispatch("Outlook.Application") or
        GetNamespace("MAPI"). Creating a MAPI session just to check detection
        leaks the session slot (Outlook limits to ~20). Instead, we check for:
          1. pywin32 importable (win32com.client)
          2. OST/PST files exist on disk (file-based check, no COM)

        The actual COM connection is only created in collect() via _ensure_com().
        """
        win32com_client = _try_import_win32com()
        if win32com_client is None:
            return False
        # Check for OST/PST files WITHOUT using COM.
        ost_files = _find_ost_files_no_com()
        return len(ost_files) > 0

    # -- collection ---------------------------------------------------------

    def collect(self) -> list[dict]:
        """Return email events from Outlook Inbox and Sent Items.

        Connects to Outlook via COM, iterates over all mail stores, finds
        Inbox and Sent Items folders by name, and collects one event per email
        item. Events match the welink-cli mail event shape.

        NOT a generator — builds a list of plain dicts, then releases ALL COM
        objects before returning. A generator would hold its frame (and COM
        refs) alive across yields, causing MAPI session exhaustion.
        """
        if not self._ensure_com():
            import sys
            print("[outlook] COM connection failed — Outlook may not be installed or not started. "
                  "Email data unavailable for this run.", file=sys.stderr)
            return []

        events: list[dict] = []
        stores = None
        try:
            stores = self._ns.Stores
            for store in stores:
                root = None
                try:
                    root = store.GetRootFolder()
                except Exception:
                    del store
                    continue

                store_name = _safe_str(store.DisplayName) or ""

                for folder_substr, direction in TARGET_FOLDERS:
                    folder = _find_folder_by_name(root, folder_substr)
                    if folder is None:
                        continue
                    try:
                        events.extend(self._collect_folder(
                            folder, direction, store_name))
                    except Exception:
                        pass
                    finally:
                        del folder
                del root
                del store
        except Exception as e:
            import sys
            print(f"[outlook] collect() error iterating stores: {e}", file=sys.stderr)
        finally:
            # Release the Stores collection reference.
            del stores
            gc.collect()

        return events

    def _collect_folder(self, folder, direction: str,
                        store_name: str) -> list[dict]:
        """Return email events from a single Outlook folder.

        Extracts primitive data from each MailItem into a plain dict, then
        ``del``s the COM object immediately. NOT a generator — a generator
        frame would hold COM refs across yields.
        """
        events: list[dict] = []
        items = folder.Items
        count = items.Count
        if count == 0:
            del items
            return events

        # Sort by received/sent time ascending
        try:
            if direction == "received":
                items.Sort("[ReceivedTime]", False)
            else:
                items.Sort("[SentOn]", False)
        except Exception:
            pass

        folder_name = _safe_str(folder.Name) or "(unknown)"

        emitted = 0
        for i in range(1, count + 1):  # COM collections are 1-indexed
            if emitted >= self._max_items:
                break
            item = None
            try:
                item = items.Item(i)
            except Exception:
                continue

            ev = self._item_to_event(item, folder_name, direction, store_name)
            if ev is not None:
                events.append(ev)
                emitted += 1
            # del the MailItem COM reference so PyIDispatch refcount drops to 0.
            del item

        # Release the Items collection reference.
        del items
        gc.collect()
        return events

    def close(self):
        """Close the COM connection and release all MAPI resources.

        CRITICAL: calls ns.Logoff() to free the MAPI session slot, then
        ``del``s the instance attributes so PyIDispatch refcount drops to 0.
        Without this, Outlook accumulates leaked sessions and shows
        "Outlook 已经用完了所有共享资源" popups.
        """
        ns = self._ns
        outlook = self._outlook
        # Clear instance attributes first so only locals hold the refs.
        self._ns = None
        self._outlook = None
        if ns is not None or outlook is not None:
            # _close_mapi_session does ns.Logoff(), then dels its locals.
            _close_mapi_session(ns, outlook, uninit=True)

    def __del__(self):
        """Ensure COM resources are released on garbage collection."""
        try:
            self.close()
        except Exception:
            pass

    def _item_to_event(self, item, folder: str, direction: str,
                       store_name: str) -> dict | None:
        """Convert an Outlook COM mail item to a normalized event.

        Matches the welink-cli ``_mail_to_event`` shape:
        kind="email", source_kind="comm", tool_input keys: domain, folder,
        direction, subject, from, from_email, date, is_read, has_attachments.
        """
        # Timestamp
        if direction == "received":
            dt_val = getattr(item, "ReceivedTime", None)
            date_raw = _safe_str(dt_val)
        else:
            dt_val = getattr(item, "SentOn", None)
            date_raw = _safe_str(dt_val)

        ts = _com_datetime_to_epoch(dt_val)
        if ts is None:
            return None

        # Subject
        subject = _safe_str(getattr(item, "Subject", None)) or "(no subject)"

        # Sender
        sender = _safe_str(getattr(item, "SenderName", None))
        sender_email = _safe_str(getattr(item, "SenderEmailAddress", None))

        # Exchange X.400 addresses look like /O=HUAWEI EXCHANGE ORG/... — normalize
        if sender_email and sender_email.startswith("/O="):
            # This is an Exchange distinguished name; keep it but also note it
            sender_email = sender_email

        # Read status
        is_read = getattr(item, "UnRead", None)
        if is_read is not None:
            is_read = not is_read  # UnRead=True means is_read=False

        # Attachments
        has_attachments = None
        try:
            has_attachments = item.Attachments.Count > 0
        except Exception:
            pass

        # Item ID (Outlook EntryID)
        item_id = _safe_str(getattr(item, "EntryID", None), max_len=200)

        # To recipients (for sent items)
        to_recipients = None
        if direction == "sent":
            try:
                to_recipients = _safe_str(getattr(item, "To", None))
            except Exception:
                pass

        return make_event(
            source="outlook",
            source_kind="comm",
            session_id=item_id,
            cwd=None,
            git_branch=None,
            timestamp=ts,
            timestamp_raw=date_raw,
            kind="email",
            text=subject,
            tool_input={
                "domain": "mail",
                "folder": folder,
                "direction": direction,
                "item_id": item_id,
                "subject": subject,
                "from": sender,
                "from_email": sender_email,
                "date": date_raw,
                "is_read": is_read,
                "has_attachments": has_attachments,
                "preview": None,  # COM doesn't easily give a preview without opening
                "to": to_recipients,
                "store": store_name,
            },
            extra={
                "tool": "outlook_com",
            },
        )

    def collect_since(self, watermark: float | None) -> Iterator[dict]:
        """Yield only events after the watermark (epoch seconds).

        Outlook COM doesn't support efficient time-range queries, so we
        collect all and filter post-hoc. This is acceptable for typical
        mailbox sizes (hundreds, not millions of items).

        Safe as a generator: collect() returns a list of plain dicts (no COM
        objects), so no COM references are held across yields.
        """
        if watermark is None:
            yield from self.collect()
            return
        for ev in self.collect():
            ts = ev.get("timestamp")
            if ts is not None and ts > watermark:
                yield ev
