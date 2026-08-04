---
name: huawei-auto-buddy
description: Huawei employee's personal AI work companion. Two-phase pipeline: (1) retro-scope identifies time sinks and recurring time consumption from activity traces (AI sessions, git, browser, WeLink, email, meetings, file edits); (2) skill-forge creates or modifies skills and memories that deal with those problems, so the user can solve them easily next time and avoid wasting time. Invoke when the user says "time log", "how did I spend my time", "evolve", "分析session", "update skills", "review recent work", "时间日志", "工时统计", "自演进", "总结一下最近的工作", etc.
---

# huawei-auto-buddy

Personal AI work companion for Huawei employees. Two jobs, one pipeline:
**diagnose, then act.**

## How it works

```
activity traces → retro-scope (diagnose) → skill-forge (act) → skills/memories
```

1. **retro-scope** reconstructs where the user's time and effort went — which tasks
   consumed the most human time, which problems kept recurring across weeks, what
   the user struggled with. It surfaces time sinks and recurring time consumption
   from the activity traces a person already leaves behind (AI sessions,
   git, browser, WeLink, email, meetings, file edits). No manual logging.

2. **skill-forge** takes those findings and creates or modifies skills and memories
   that address the identified problems — so the next time the user faces the same
   situation, a skill or memory is ready to help them solve it quickly and avoid
   wasting time. It also extracts long-term memory, updates existing skills based on
   new experience, and recommends market skills.

The pipeline is: **find the waste → eliminate the waste going forward.**

## Components

### retro-scope (`retro-scope/`)

Diagnoses where time goes. Multi-horizon reports (90d/30d/7d/1d) with three-way
time accounting (Wall → Active → Human), content-driven root-cause narratives, and
recurring time-consumption analysis (persistent, declining, increasing, automation
candidates). 14 source adapters, all detector-based. Retrospective only — no live
tracking.

See `retro-scope/SKILL.md` for full details.

### skill-forge (`skill-forge/`)

Acts on the diagnosis. 9-step operational workflow: reads retro-scope findings,
collects supplementary data (git, WeLink, CodeHub), extracts long-term memory,
creates/updates skills for recurring problems, recommends market skills, and
checks versions. Includes auto-repair for agentcenter and welink-cli, watermark
for incremental analysis, and detailed methodology rules (forced generalization,
user feedback sedimentation, rule strengthening).

See `skill-forge/SKILL.md` for full details.

## Constraints

- **Retrospective only.** No live tracking, no always-on watchers.
- **Opt-in self-analysis.** No manager-analyzing-team deployment.
- **Open-source only.** No paywalled or closed-source dependencies.
- **No hardcoded user paths or identity.** Portable across colleagues' environments.
