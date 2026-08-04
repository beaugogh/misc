---
name: huawei-auto-buddy
description: Huawei employee's personal AI work companion. Two components: (1) retro-scope — reconstructs where your time and effort went from activity traces (AI sessions, git, browser, WeLink, email, meetings, file edits), with multi-horizon reports and recurring time-consumption analysis; (2) skill-forge — auto-evolves your skill ecosystem by analyzing sessions, extracting long-term memory, creating/updating skills, and recommending market skills. Invoke when the user says "time log", "how did I spend my time", "evolve", "分析session", "update skills", "review recent work", "时间日志", "工时统计", "自演进", "总结一下最近的工作", etc.
---

# huawei-auto-buddy

Personal AI work companion for Huawei employees. Two components work together:

## Components

### retro-scope (`retro-scope/`)

Records the user's time/effort across task kinds, aggregatable by day / week /
month / year, to reveal which kinds of work consume the most time/effort. Beyond
time, it reconstructs a **task model** per task: input, output, and success/failure
— not just duration.

- **Multi-horizon reports** (90d/30d/7d/1d) with three-way time accounting (Wall →
  Active → Human) and content-driven root-cause narratives.
- **Recurring time-consumption analysis** — splits the horizon into time windows and
  surfaces patterns that keep coming back (persistent, declining, increasing,
  automation candidates).
- **14 source adapters** — Claude Code, codeagent, git, Chrome/Edge, WeLink CLI,
  Outlook, VSCode Local History, iCalendar, meeting recordings, and more. All
  detector-based: present sources are used, absent ones reported honestly.
- **Retrospective only** — no live tracking, no always-on watchers. Opt-in
  self-analysis.

See `retro-scope/SKILL.md` for full details.

### skill-forge (`skill-forge/`)

Auto-evolves the user's skill ecosystem by analyzing personal data traces
(opencode/codeagent sessions, git commits, WeLink chat, token metrics, 3ms/Wiki
authoring). Extracts long-term memory, creates and updates skills, recommends/installs
market skills, and checks skill versions.

See `skill-forge/SKILL.md` for full details.

## How they relate

retro-scope shows where time goes; skill-forge acts on it. The recurring
time-consumption patterns surfaced by retro-scope (especially automation
candidates) are natural inputs for skill-forge's skill creation. The two
components share the same data-source ecosystem (AI sessions, git, WeLink,
browser history) but serve different purposes: measurement vs. evolution.
