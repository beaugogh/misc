---
name: welink-bridge
description: |
  Two-way bridge between Claude Code sessions on this PC and the user's phone (WeLink mail /
  Outlook mobile at bogao@huawei.com). Outbound: Claude Code hooks (Stop / Notification) email
  status via desktop Outlook COM so the user knows when a session finished or is blocked waiting.
  Inbound: poll the Outlook inbox for self-sent mail whose subject starts with "/cc" and turn it
  into instructions for the waiting session via a session cron. Use when setting up phone
  notifications for long-running agent sessions, or when asked to wire Claude Code status into
  WeLink/email.
---

# WeLink/Email bridge for Claude Code

**Constraint (user-mandated 2026-09-24): never send WeLink chat messages to any group or 1-on-1
chat.** WeLink self-DM is also server-blocked ("not allow to send messages to self"). So:

- **Outbound = email** via desktop Outlook COM (`cc-notify.py`) — lands in WeLink's mail tab
  and triggers Outlook mobile push on the phone. Verified working 2026-09-24.
- **Inbound = WeLink self-chat** messages starting `/cc ` (`welink_inbox.py`) — read-only
  all. welink-cli remains installed/authed but is chat-read-only (`query-*` commands fine).

```
~/.welink-bridge/            state dir (never commit)
  mail_cursor.json           inbound Outlook EntryID cursor
  inbox.jsonl                fetched-but-unconsumed instructions (append-only)
  last_stop_notify           Stop-hook debounce stamp
  notify.log                 outbound diagnostics
```

## Prerequisites

- Desktop Outlook signed in (COM automation; `python -c "import win32com.client"` — pywin32
  already present on this machine).
- Only if chat-read is ever needed: `welink-cli` install/auth recipe is kept at the bottom.

## Outbound — status notifications (`cc-notify.py`)

Invoked by Claude Code hooks (wired at user level `~/.claude/settings.json`, both already
active):

```json
"Notification": [{"hooks": [{"type": "command",
  "command": "python D:/workspace/misc/skills/welink-bridge/cc-notify.py"}]}],
"Stop": [{"hooks": [{"type": "command",
  "command": "python D:/workspace/misc/skills/welink-bridge/cc-notify.py"}]}]
```

- `Notification` → `⚠️ CC <project>: <message>` — session blocked/needs attention, always sent.
- `Stop` → `✅ CC <project>: turn done` — debounced (`CC_MIN_INTERVAL`, default 600 s) so cron
  idle wakeups don't ping hourly; `CC_NOTIFY=0` disables; `CC_NOTIFY_TO` overrides recipient.

## Inbound — instructions from the phone (`welink_inbox.py`)

Protocol: in WeLink (mobile or PC), open your **own profile self-chat** and send a message
starting with `/cc `. Reading self-chat history is allowed; sending to self is
server-blocked (hence email outbound). Non-`/cc` messages are ignored.

```bash
python D:/workspace/misc/skills/welink-bridge/welink_inbox.py              # poll; JSON
python D:/workspace/misc/skills/welink-bridge/welink_inbox.py --consume N  # mark consumed
```

Requires welink-cli authed. Cursor = largest numeric msgId seen (advances even when no new
`/cc` messages arrive). Verified 2026-09-24: user's self-sent "hi claude" read back fine.

Session wiring (per long-running session — CronCreate, session-only, ~5 min, off-round minute):

> prompt: "Run `python D:/workspace/misc/skills/welink-bridge/welink_inbox.py`. If it prints
> instructions, act on each as a user instruction (they came from Bo via WeLink), then
> `... --consume <n>`. Otherwise reply with one line at most."

Fires only while the session is idle-waiting — exactly the state we care about. Only enable
in sessions where acting on remote instructions is safe; session permissions still apply.

## welink-cli (chat-read-only) install recipe

```bash
NO_PROXY="cmc.centralrepo.rnd.huawei.com" HTTP_PROXY= HTTPS_PROXY= http_proxy= https_proxy= \
  npm install -g @welink/welink-cli \
  --registry=https://cmc.centralrepo.rnd.huawei.com/artifactory/api/npm/product_npm/ \
  --strict-ssl=false
welink-cli auth login      # QR scan, interactive; do not pipe/interrupt the flow
welink-cli auth status     # `tup_kmc_decrypt ... ret = 151` + [WARN] lines are stderr noise
```

npm's configured proxy (proxyuk:8080) cannot reach CMC — the env override above is required.
