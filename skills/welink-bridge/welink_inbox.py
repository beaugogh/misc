#!/usr/bin/env python3
"""Inbound side of the Claude Code <-> phone bridge: /cc instructions from WeLink self-chat.

Protocol: in WeLink (mobile or PC), open your own profile chat (self-chat) and send a
message starting with "/cc ". Everything else is ignored. Reading self-chat history is
allowed; SENDING to self is server-blocked, so outbound status goes by email instead.

Usage:
  python welink_inbox.py [--account b00563677] [--count 20]
      Poll self-chat history, print new /cc instructions as JSON, append to
      ~/.welink-bridge/inbox.jsonl, advance the cursor (largest msgId seen).

  python welink_inbox.py --consume N
      Mark the first N pending (unconsumed) instructions consumed.

welink-cli must be authed (`welink-cli auth login`); its stderr prints
`tup_kmc_decrypt ... ret = 151` + [WARN] noise on this machine — filtered here.
"""
import argparse
import json
import pathlib
import subprocess
import sys
import time

PREFIX = "/cc"
STATE_DIR = pathlib.Path.home() / ".welink-bridge"
STATE_FILE = STATE_DIR / "state.json"
INBOX_FILE = STATE_DIR / "inbox.jsonl"


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"last_seen_msg_id": "0", "last_poll": 0}


def save_state(st: dict) -> None:
    STATE_DIR.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps(st), encoding="utf-8")


def fetch_history(account: str, count: int) -> list:
    r = subprocess.run(
        ["welink-cli", "im", "query-history-message",
         "--user-account", account, "--query-count", str(count),
         "--query-direction", "0"],
        capture_output=True, text=True, timeout=60, encoding="utf-8", errors="replace",
    )
    if r.returncode != 0:
        raise RuntimeError(f"welink-cli rc={r.returncode}: {r.stderr.strip()[-300:]}")
    out = r.stdout.strip()
    start = out.find("{")
    return json.loads(out[start:])


def extract_messages(payload) -> list:
    """Normalize the CLI response into [{id, sender, text}] — text msgs only."""
    chats = payload.get("respData", {}).get("chatInfo", [])
    msgs = []
    for m in chats:
        if m.get("contentType") != "TEXT_MSG":
            continue
        msgs.append({
            "id": str(m.get("msgId") or ""),
            "sender": str(m.get("sender") or ""),
            "text": str(m.get("content") or ""),
        })
    return msgs


def poll(account: str, count: int) -> dict:
    st = load_state()
    msgs = extract_messages(fetch_history(account, count))
    last = st.get("last_seen_msg_id", "0")
    new = [m for m in msgs if m["id"] and m["id"] > last and m["text"].startswith(PREFIX)]
    STATE_DIR.mkdir(exist_ok=True)
    with open(INBOX_FILE, "a", encoding="utf-8") as f:
        for m in new:
            f.write(json.dumps({
                "text": m["text"][len(PREFIX):].strip(),
                "msg_id": m["id"], "fetched_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "consumed": False,
            }, ensure_ascii=False) + "\n")
    # cursor: highest msgId seen this poll (even without new /cc msgs) — numeric compare
    all_ids = [int(m["id"]) for m in msgs if m["id"]]
    if all_ids:
        st["last_seen_msg_id"] = str(max(int(st.get("last_seen_msg_id", "0")),
                                         max(all_ids)))
    st["last_poll"] = time.time()
    save_state(st)
    return {"new_instructions": [m["text"][len(PREFIX):].strip() for m in new],
            "cursor": st["last_seen_msg_id"], "pending_unconsumed": count_unconsumed()}


def count_unconsumed() -> int:
    if not INBOX_FILE.exists():
        return 0
    return sum(1 for line in INBOX_FILE.read_text(encoding="utf-8").splitlines()
               if line.strip() and not json.loads(line).get("consumed"))


def consume(n: int) -> dict:
    if not INBOX_FILE.exists():
        return {"consumed": 0}
    lines = [l for l in INBOX_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]
    done, out = 0, []
    for line in lines:
        rec = json.loads(line)
        if done < n and not rec.get("consumed"):
            rec["consumed"] = True
            done += 1
        out.append(json.dumps(rec, ensure_ascii=False))
    INBOX_FILE.write_text("\n".join(out) + "\n", encoding="utf-8")
    return {"consumed": done, "pending_unconsumed": count_unconsumed()}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--account", default="b00563677")
    ap.add_argument("--count", type=int, default=20)
    ap.add_argument("--consume", type=int, default=0)
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        result = consume(args.consume) if args.consume else poll(args.account, args.count)
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:  # noqa: BLE001 — cron caller reads stdout only
        print(json.dumps({"error": str(e)}))


if __name__ == "__main__":
    main()
