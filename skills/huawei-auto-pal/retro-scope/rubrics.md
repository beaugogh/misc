# Rubrics — retro-scope

Design principles and quality bars that govern the skill's output. Each rubric
is a durable rule, not a one-off bug report. Bug reports that have been fixed
are folded into the rule they inspired, not kept as separate entries.

## Driving Principles

1. **Human time is the metric, not machine time.** The skill tracks where the
   *user's* time goes, not where the agent's time goes. A 10h autonomous agent
   run with 2 prompts is not a time sink. A forgotten browser tab is not a time
   sink. A meeting nobody spoke in is not a time sink. The skill must detect
   genuine human interaction — typing, clicking, instructing, editing — and
   rank time sinks by human engaged time, not raw active or wall time.

2. **Surface what happened, let the user judge.** High or recurring time
   investment does not imply suffering. A 3h deep coding session might be flow
   state; a weekly code review might be valuable routine. The skill reports
   observable time-consumption patterns; the user decides what to do about
   them. Use neutral language ("时间消耗"), not loaded language ("痛点").

3. **Three-way time accounting.** Every task and every summary must report all
   three time types: **Wall** (total clock span) → **Active** (work detected)
   → **Human** (user engaged). The invariant is: wall ≥ active ≥ human.
   Percentages are per-type: h/H, a/A, w/W.

4. **Content-driven root causes.** The skill must read the actual content of
   tasks — user prompts, error texts, page titles, chat messages, commit
   subjects, file names — and explain *why* a task took the time it did. Generic
   labels like "blocker: command timeout (21 of 46 errors)" are not acceptable;
   the narrative must say what was attempted, what failed, and what the user
   struggled with.

5. **Retrospective, opt-in, portable core.** No live tracking. No always-on
   watchers. No manager-analyzing-team. The core must not require a closed-source
   dependency; optional platform or Huawei integrations must be labeled, detected,
   user-approved, and skipped with an honest coverage note when unavailable.

6. **Working hours derived from real data.** Do not assume a flat 8h/day. Derive
   the working-hour denominator from actual human activity in the period.

## Report Structure

7. **Logical flow.** Summary header → recurring time consumption → top 10 time
   sinks → per-kind work content → per-period breakdown table + chart →
   insights → data availability. Each section has a clear boundary and purpose.

8. **All activity categories shown.** The report must cover AI agent use (Claude
   Code, codeagent, openclaw, codex, hermes), WeLink chats, WeLink meetings,
   web browser use, local file editing — even if some don't reach the top 10.
   Use specific program names (say "git" not "vcs", "WeLink" not "IM").

9. **Top 10 time sinks.** Ranked by human engaged time. Filtered to genuine
   time sinks only (≥5 human actions, ≥5 min engaged). Low-engagement tasks
   listed separately as "低参与度任务" (likely forgotten tabs / abandoned sessions).

10. **Structured root-cause cells.** Each 根因 cell must contain 目标 (goal) and
    困难 (struggle) at minimum. The goal must match the content that follows —
    if the goal says "浏览 AgentCenter", the detail section must be about
    AgentCenter, not unrelated pages. Break narratives into labeled parts
    (🎯目标, ⚠️困难, 📝详情, 🌐页面, 🔍证据, 📥下载, ⏱️时间) instead of a single
    lump of text.

11. **Per-period table includes all three time columns.** Wall, Active, Human —
    not just Wall and Active.

12. **Session records exported as minimized evidence.** Redacted JSON records per
    genuine time sink task may include a capped event timeline, prompts, messages,
    page titles, commit subjects, and file names when needed to support the finding.
    Store them in `output/session_records/` with restrictive permissions. Never
    export credentials, unnecessary identity, or full correspondence.

## Language and Readability

13. **Chinese for analysis, English where clear.** Long descriptive and
    analytical texts in Chinese. Program names, technical terms, and short
    labels in English where it's clearer.

14. **Descriptions must be meaningful, not mechanical.** Avoid descriptions that
    list counts without explaining what the user was actually doing. "593 次访问
    中 378 次为重复访问" is useless without saying what the user was looking for
    and why. Avoid awkward phrasing like "命令超时（网络慢或进程挂起）；用户拒绝
    工具调用——agent 反复提出不需要的操作". Rewrite as plain, specific statements.

15. **Goal text must read like a goal.** "install skill-creator Let me wait for
    it" is not a goal. Strip conversational filler and system-reminder wrappers
    from goal text.

16. **No duplicative categories.** ⚠️ Struggle and 🔥 Difficulty were merged.
    Each labeled part in the root-cause cell must serve a distinct purpose.

## Genuine Interaction Detection

17. **Forgotten sessions are not time sinks.** For each activity type, detect
    whether the user genuinely interacted:
    - **Coding sessions:** user typed instructions/prompts frequently.
    - **Browser pages:** user clicked, scrolled, or navigated actively.
    - **Chat sessions:** user typed messages to others.
    - **File editing:** user made repeated edits across multiple versions.
    - **Meetings:** user participated (spoke, reacted, followed up).

18. **Distinguish human edits from agent edits.** Files edited by an autonomous
    agent (e.g. VSCode Local History records agent edits) must not appear as
    "frequently edited by the user." Tag agent-edited files and exclude them
    from human file-editing time sinks.

19. **Investigate content for each activity type.** When an activity is a
    genuine time sink, investigate its content and explain *why* it took time:
    - **Web browsing:** what pages, what topic, what was the user looking for.
      When `--enrich-pages` is enabled, fetch actual page content for top-visited
      external pages and analyze: what each page was about (from content, not
      just title), how pages relate (shared US tickets, MR numbers, project
      names), and why the user spent time cross-referencing them. Huawei internal
      pages (CloudDevOps, CodeHub, W3) require SSO and are skipped gracefully.
    - **Chat:** what was discussed, how many participants, message volume.
    - **Coding:** what was the goal, what errors occurred, what was retried.
    - **File editing:** what file, what type, what was added/removed/modified.
    - **Meetings:** subject, organizer, whether decisions were followed up.

## Recurring Time Consumption

20. **Cross-window comparison.** Split the horizon into time windows (90d→monthly,
    30d→weekly, 7d→daily, 1d→no comparison) and surface patterns across windows:
    - ⏰ Persistent: same task in top-5 across ≥2 windows.
    - ✅ Declining: was a top sink, now gone from the latest window.
    - 📈 Increasing: human hours on a kind rose ≥50% earliest→latest.
    - 🔧 Automation candidate: recurrent + high error count — a suggestion
      to examine, not a conclusion that the work was painful.

21. **Recurring patterns must be based on human time.** Only tasks with genuine
    human engagement (≥10 min) qualify as recurring time-consumption candidates.
    Autonomous agent runs that cost no human time are excluded from all four
    insight types.

## Computation Rules

22. **Wall ≥ Active ≥ Human.** This invariant must hold for every task and every
    aggregate. If it doesn't, the computation has a bug.

23. **Percentages are per-type.** For a 7-day report with totals H/A/W and a
    task with h/a/w: human% = h/H, active% = a/A, wall% = w/W. Not h/W or a/W.

24. **Working-day basis from real human activity.** Use
    `compute_actual_working_hours()` to derive the denominator, not a flat 8h/day.
