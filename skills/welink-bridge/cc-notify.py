#!/usr/bin/env python3
"""Outbound side of the Claude Code <-> phone bridge: hook event -> email via Outlook COM.

Replaces welink-notify.py's DM path (WeLink blocks self-DMs; email to bogao@huawei.com
lands in WeLink's mail tab / Outlook mobile notifications on the phone).

Reads the hook event JSON from stdin. Env:
  CC_NOTIFY_TO    recipient (default bogao@huawei.com)
  CC_NOTIFY=0     kill switch
  CC_MIN_INTERVAL debounce seconds for Stop events (default 600)

Wiring (user-level ~/.claude/settings.json):
  "Notification" and "Stop" hooks -> `python <this file>`
"""
import json
import os
import pathlib
import sys
import time

STATE_DIR = pathlib.Path.home() / ".welink-bridge"
MIN_INTERVAL = int(os.environ.get("CC_MIN_INTERVAL", "600"))
TO = os.environ.get("CC_NOTIFY_TO", "bogao@huawei.com")


def send_mail(subject: str, body: str) -> bool:
    if os.environ.get("CC_NOTIFY", "1") == "0":
        return False
    try:
        import win32com.client
        outlook = win32com.client.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)
        mail.To = TO
        mail.Subject = subject
        mail.Body = body
        mail.Send()
        return True
    except Exception as e:  # noqa: BLE001 — hook must never raise
        log(f"send error: {e}")
        return False


def log(msg: str) -> None:
    STATE_DIR.mkdir(exist_ok=True)
    with open(STATE_DIR / "notify.log", "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")


def main() -> None:
    try:
        event = json.load(sys.stdin)
    except Exception:
        event = {}
    hook = event.get("hook_event_name", "")
    cwd_name = pathlib.Path(event.get("cwd") or os.getcwd()).name

    if hook == "Notification":
        # Session is blocked / needs attention — always send (no debounce).
        msg = str(event.get("message") or "needs attention").strip()
        ok = send_mail(f"⚠️ CC {cwd_name}: {msg}", f"Project: {event.get('cwd')}\n\n{msg}")
        log(f"notification sent={ok} msg={msg[:120]}")
        return

    if hook == "Stop":
        # Turn finished. Debounce: cron idle wakeups fire Stop every tick —
        # only notify if the last Stop notice is older than MIN_INTERVAL.
        STATE_DIR.mkdir(exist_ok=True)
        stamp_file = STATE_DIR / "last_stop_notify"
        now = time.time()
        last = float(stamp_file.read_text() or 0) if stamp_file.exists() else 0.0
        if now - last < MIN_INTERVAL:
            log(f"stop debounced ({now - last:.0f}s < {MIN_INTERVAL}s)")
            return
        stamp_file.write_text(str(now))
        ok = send_mail(f"✅ CC {cwd_name}: turn done",
                       f"Project: {event.get('cwd')}\nTurn finished, awaiting instructions.")
        log(f"stop sent={ok}")
        return

    log(f"ignored event {hook}")


if __name__ == "__main__":
    main()
