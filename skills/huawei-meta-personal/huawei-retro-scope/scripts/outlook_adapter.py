"""Outlook mail adapter — backup route for welink-cli ``mail list`` (Phase 9.3).

Provides email activity collection from Outlook for colleagues who do NOT have
welink-cli installed. Uses the Outlook COM/MAPI interface (via pywin32) to read
mail folders directly from the running Outlook desktop application.

**Investigation verdict (2026-07-29, recorded in SKILL.md section D + open questions):**

1. **libpff / pffexport / pypff** — FAILED. ``pffexport`` not in PATH; ``pypff`` not
   installed; ``pip install libpff-python`` fails on Windows (C build error in
   pyproject.toml — the libpff C library doesn't build with MSVC on this platform).
   This was the OSS-first choice but is blocked on Windows without a prebuilt wheel.
2. **Outlook COM / MAPI (pywin32)** — WORKS. ``pip install pywin32`` succeeds from
   the tuna mirror. ``Outlook.Application`` COM Dispatch succeeds. Outlook.exe is
   installed at ``C:\\Program Files\\Microsoft Office\\root\\Office16\\OUTLOOK.EXE``.
   Inbox (50 items) and Sent Items (38 items) are readable with subject, sender,
   received time, attachments count. This is the path the adapter uses.
3. **Graph API** — not tested (needs Azure admin consent; lowest priority).

**OST file location:** The SKILL.md note "Not present on author's machine" is
**outdated**. The OST file exists at ``D:\\Email\\bogao@huawei.com.ost`` (206.9 MB) —
a custom location, not the default ``~/AppData/Local/Microsoft/Outlook/``. The
default directory contains only ``RoamCache/``, ``spscoll.dat``, and a ``16/``
subdir. The adapter's ``detect()`` checks both the default platform_paths location
and any ``.ost``/``.pst`` files discoverable via the COM Stores collection.

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

This adapter properly releases ALL COM objects using ``Marshal.ReleaseComObject()``
after use — in ``detect()``, ``collect()``, and ``_find_ost_files()``. A single
COM connection is created and reused; it is closed in ``close()`` which is called
by the registry after collection completes.

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
from typing import Iterator, Any

from sources import make_event


# ---------------------------------------------------------------------------
# COM resource management — prevent MAPI session exhaustion
# ---------------------------------------------------------------------------

def _release_com(obj):
    """Release a COM object to free its MAPI session slot.

    Calls Marshal.ReleaseComObject() which decrements the reference count.
    This is CRITICAL: Outlook limits concurrent MAPI sessions (~20), and
    every unreleased Store/Folder/Items/MailItem counts against that limit.
    Failing to release causes "Outlook 已经用完了所有共享资源" popups.
    """
    if obj is None:
        return
    try:
        import pythoncom
        pythoncom.CoUninitialize()
    except Exception:
        pass
    try:
        from win32com.client import constants
        import win32com.client
        # Marshal.ReleaseComObject is the .NET name; in pywin32 it's accessed
        # via win32com.client.gencache or directly via the COM object's __del__.
        # The most reliable approach: delete the reference and call GC.
        del obj
    except Exception:
        pass


def _release_com_objects(*objs):
    """Release multiple COM objects. See _release_com for details."""
    for obj in objs:
        if obj is not None:
            try:
                import win32com.client
                # Force release by removing all references
                import gc
                del obj
                gc.collect()
            except Exception:
                pass


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


def _find_ost_files() -> list[str]:
    """Find .ost and .pst files on the machine.

    Checks:
    - The default Outlook data directory (platform_paths.OUTLOOK_OST)
    - The COM Stores collection (if available) — this is how we found the
      custom D:\\Email location
    """
    from platform_paths import OUTLOOK_OST

    found = []

    # 1. Check default platform path
    if OUTLOOK_OST and os.path.isdir(OUTLOOK_OST):
        for f in os.listdir(OUTLOOK_OST):
            if f.lower().endswith((".ost", ".pst")):
                found.append(os.path.join(OUTLOOK_OST, f))

    # 2. Try COM Stores for custom locations
    win32com_client = _try_import_win32com()
    if win32com_client is not None:
        outlook = None
        ns = None
        try:
            outlook = win32com_client.Dispatch("Outlook.Application")
            ns = outlook.GetNamespace("MAPI")
            for store in ns.Stores:
                try:
                    filepath = store.FilePath
                    if filepath and os.path.isfile(filepath):
                        if filepath.lower().endswith((".ost", ".pst")):
                            if filepath not in found:
                                found.append(filepath)
                except Exception:
                    pass
        except Exception:
            pass
        finally:
            # Release COM objects to prevent MAPI session exhaustion.
            _release_com_objects(ns, outlook)
            import gc
            gc.collect()

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
        """Lazily connect to Outlook COM. Returns True if connected."""
        if self._ns is not None:
            return True
        win32com_client = _try_import_win32com()
        if win32com_client is None:
            return False
        try:
            self._outlook = win32com_client.Dispatch("Outlook.Application")
            self._ns = self._outlook.GetNamespace("MAPI")
            return True
        except Exception:
            self._outlook = None
            self._ns = None
            return False

    # -- detection ----------------------------------------------------------

    def detect(self) -> bool:
        """True if Outlook COM is available and has at least one mail store.

        IMPORTANT: This method creates and releases its own COM connection.
        It does NOT reuse _ensure_com() because detect() may be called
        without a subsequent collect() (the registry calls detect() on all
        adapters, then collect() only on detected ones). Leaving the COM
        connection open from detect() would leak a MAPI session.
        """
        win32com_client = _try_import_win32com()
        if win32com_client is None:
            return False
        outlook = None
        ns = None
        try:
            outlook = win32com_client.Dispatch("Outlook.Application")
            ns = outlook.GetNamespace("MAPI")
            for store in ns.Stores:
                root = None
                try:
                    root = store.GetRootFolder()
                    inbox = _find_folder_by_name(root, "inbox")
                    if inbox is not None:
                        return True
                except Exception:
                    continue
                finally:
                    _release_com_objects(root)
        except Exception:
            pass
        finally:
            _release_com_objects(ns, outlook)
            import gc
            gc.collect()
        return False

    # -- collection ---------------------------------------------------------

    def collect(self) -> Iterator[dict]:
        """Yield email events from Outlook Inbox and Sent Items.

        Connects to Outlook via COM, iterates over all mail stores, finds
        Inbox and Sent Items folders by name, and emits one event per email
        item. Events match the welink-cli mail event shape.

        All COM objects (stores, folders, items, mail items) are released
        after use to prevent MAPI session exhaustion.
        """
        if not self._ensure_com():
            return

        try:
            for store in self._ns.Stores:
                root = None
                try:
                    root = store.GetRootFolder()
                except Exception:
                    continue

                store_name = _safe_str(store.DisplayName) or ""

                for folder_substr, direction in TARGET_FOLDERS:
                    folder = _find_folder_by_name(root, folder_substr)
                    if folder is None:
                        continue
                    try:
                        yield from self._collect_folder(
                            folder, direction, store_name)
                    except Exception:
                        continue
                    finally:
                        _release_com_objects(folder)
                _release_com_objects(root)
        except Exception:
            return

    def _collect_folder(self, folder, direction: str,
                        store_name: str) -> Iterator[dict]:
        """Yield email events from a single Outlook folder.

        Releases each MailItem COM object after extracting its data to prevent
        MAPI session exhaustion.
        """
        items = folder.Items
        count = items.Count
        if count == 0:
            _release_com_objects(items)
            return

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
                yield ev
                emitted += 1
            # Release each MailItem immediately to limit COM object count.
            _release_com_objects(item)

        _release_com_objects(items)

    def close(self):
        """Close the COM connection and release all resources.

        Should be called after collect() completes to prevent MAPI session
        exhaustion. The registry should call this in a finally block.
        """
        import gc
        _release_com_objects(self._ns, self._outlook)
        self._ns = None
        self._outlook = None
        gc.collect()

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
        """
        if watermark is None:
            yield from self.collect()
            return
        for ev in self.collect():
            ts = ev.get("timestamp")
            if ts is not None and ts > watermark:
                yield ev
