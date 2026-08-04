# Research findings: existing OSS retrospective activity analyzers

Searched for open-source tools that fuse multiple historical activity records into a holistic
time/task picture, retrospectively. Four candidates surfaced in round 1 (via external agent,
2026-07-29); two more in round 2. Assessment and actionable takeaways below.

## Candidates assessed

| Tool | License | Approach | Multi-source | Retrospective | Categorizes | Verdict |
|------|---------|----------|--------------|---------------|-------------|---------|
| **Memacs** (novoid/Memacs) | GPL-3.0 | Independent Python modules per source → unified Org-mode timeline | yes (git, browser, email, SMS, RSS, CSV, EXIF, iCalendar) | yes (cron-run parsers) | manual (Org tags) | **architectural reference** |
| **ActivityWatch** (ActivityWatch/activitywatch) | MPL-2.0 | Live watchers → local server → dashboard | yes (window, AFK, browser ext, editor) | no (live-first; retrospective only via custom import scripts you write) | yes (rule engine on titles/URLs) | rejected on live-watcher requirement; categorization-rule engine worth referencing |
| **Hourgit** (Flyrell/hourgit) | GPL-3.0 | Parses git reflog → branch time reports | no (git only) | yes | implicit (branch names) | rejected on single-source; **reflog technique worth borrowing** |
| **Promnesia** (karlicoss/promnesia) | Apache-2.0 | Local indexer fusing personal data dumps → browser extension for context | yes (browser, bookmarks, chat exports, notes) | yes | no (provenance, not time categories) | wrong goal (information retrieval, not time distribution); built on **karlicoss/HPI** which is the more general fusion framework — closer architectural reference than Promnesia itself, not surfaced by the search |
| **Git Timeline MCP** (PramodKumarYadav/git-timeline-mcp-server) | MIT | MCP server reading git reflog + source files → HTML timeline | no (git only) | yes | yes (**domain detection from file paths + package config** — package.json/eslint/docker — not commit messages) | rejected on single-source; **domain-detection technique worth borrowing**; reflog use cross-validates Hourgit. MCP packaging irrelevant to us (we build a skill, not an MCP server). |
| **TimeTracker MCP** (lumile/timetracker-mcp) | MIT | MCP server wrapping a manual time-entry DB; AI queries it | n/a (own DB) | no (manual/live entry: "Log 2h to Project X") | yes (project/client) | rejected on retrospective + no-manual-entry requirements. Only value: query/output vocabulary (`get_daily_summary`, `analyze_work_sessions`) as a minor reference for our reporting commands. |

## Architectural reference: Memacs

Memacs's shape is **exactly our adapter-registry / open-discovery design**: independent Python
modules per source (`memacs_git.py`, `memacs_firefox.py`, …), each parsing historical records
into a normalized intermediate (Org-mode entries). This validates that the adapter-registry
pattern is the proven approach for multi-source retrospective fusion, not a novel gamble.

- **Borrow the pattern, don't fork the code.** Adapting Memacs would mean stripping Org
  output, adding AI-session modules, adding the task-model layer, adding auto-categorization —
  most of the work anyway.
- **GPL-3.0 copyleft** applies to lifted code (fine for internal sharing; a consideration if
  this ever leaves the company). Architecture/patterns aren't copyrightable, only code is.
- **Followup worth doing:** search karlicoss/HPI (Human Programming Interface) — the more
  general "unify all my personal data" framework that Promnesia is built on. Possibly a
  closer/more modern fusion reference than Memacs.

## Concrete techniques to borrow

### 1. Git reflog (from Hourgit) — finer time signal than commits
Hourgit parses `git reflog` (branch-checkout timestamps), not just `git log` (commits). Branch
switches give "when you switched to working on X" at finer granularity than commit timestamps
— a coding-task boundary signal we hadn't considered. Added to SKILL.md section C.

### 2. iCalendar (.ics) export (from Memacs's source list) — Outlook-access unlock
Memacs parses iCalendar files. This sidesteps both Outlook-access blockers we flagged:
- Parsing OST (proprietary format, needs libpff/COM/MAPI) — high friction
- Microsoft Graph API (needs Azure admin consent, may be blocked in corporate env)

Instead: the user exports their Outlook/WeLink calendar to `.ics`, which is an open format
Memacs already parses. Low-friction path to meeting duration. Added to SKILL.md section D as
an Outlook/WeLink-calendar access option.

### 3. Domain detection from file paths + package config (from Git Timeline MCP) — stronger auto-categorization
Git Timeline MCP infers the *business domain* of work from which files/packages were touched
(`package.json`, `eslint`, `docker` configs, file paths like `login.js` → "Authentication"),
rather than parsing commit messages. This is a stronger auto-categorization signal than
commit-subject parsing because:
- Commit messages are optional/varying; file paths and package manifests are always present.
- File paths encode the business domain directly (auth, billing, onboarding) where commit
  messages often describe the *change* ("fix typo") not the *domain*.
Noted in SKILL.md task-taxonomy open question as a categorization signal to combine with
session titles, tool-call patterns, commit messages, etc.

## What these results expose as gaps in our design (and validate)

### The task-model layer is genuinely novel — none of these do it
Memacs builds a raw timeline. ActivityWatch categorizes by window-title rules. Hourgit groups
by branch. None reconstruct first-class task objects with boundaries + input + output +
success. That's the thing we're building that doesn't exist — and it's novel *because these
tools predate AI coding agents*: none of them fuse Claude Code / codeagent session JSONL,
which is where the task model (TaskCreate/TaskUpdate/usage/is_error) already lives.

**Our differentiator is the AI-session task model; the fusion+categorization layer is where
we follow Memacs's pattern.**

### Auto-categorization is unsolved everywhere
ActivityWatch = manual rules. Memacs = manual Org tags. Hourgit = implicit branch names. None
auto-derive a taxonomy. This confirms our open question is a real open problem — and suggests
the hybrid answer (auto-derive a draft, let the user refine) is the right call, since no tool
does the auto-derivation well.

### No agent-ecosystem artifact exists for this
The search covered Claude skills, sub-agents, and MCP servers and found nothing — all four
results are standalone OSS projects. huawei-retro-scope fills a genuine gap in the skill ecosystem,
not just internally.

## Why "compose single-source MCP servers" is the wrong architecture for us

Round 2's closing suggestion was: connect a Git MCP + Browser-history MCP + Filesystem MCP to
the AI assistant and let it fuse them in-prompt ("reconstruct my day from these three
sources"). Technically how MCP works, but wrong for our case, for two reasons:

1. **Fusion at query time doesn't scale.** Every analysis re-reads browser history, git
   reflog, editor logs into the model context. That doesn't scale to weeks/months of data and
   isn't reproducible — two runs give different categorizations. Our design fuses into a
   structured store once, then aggregates deterministically.
2. **It loses the task model.** Composing single-source MCPs yields parallel per-source
   timelines (git events, browser events, file events). Reconstructing a *task* — boundaries
   + input + output + success — requires cross-source reasoning that a per-source MCP can't
   express. The task model is our differentiator; an MCP-composition approach can't represent
   it.

The agent's "you don't need one server to do everything" advice is right *for MCP* but wrong
*for us*. We're building a skill that owns the fusion + task-model + categorization layers;
MCP servers would be inputs at best, not the architecture.

## Net after two rounds

Six tools surveyed (Memacs, ActivityWatch, Hourgit, Promnesia, Git Timeline MCP, TimeTracker
MCP). None do multi-source retrospective fusion with a task model. The gap is real and stable
across searches. Our differentiator (AI-session task model from Claude Code/codeagent JSONL:
TaskCreate/TaskUpdate/usage/is_error) is confirmed novel — these tools predate AI coding
agents and don't fuse that source. Borrowed techniques: reflog (Hourgit + Git Timeline,
cross-validated), .ics export (Memacs), domain detection from file paths + package config
(Git Timeline). Architectural reference: Memacs's adapter-registry pattern (and karlicoss/HPI
as a followup).

## Next: deep research on methods (query for external agent)

The two rounds above established the OSS *tool* landscape is thin. The next step is a
methods-level deep research — asking for techniques, algorithms, and research from adjacent
fields that have solved pieces of the hard sub-problems. Query below, framed for delegation
to a deep-research agent.

```
Deep research: techniques and methods for retrospective, multi-source personal
task and time reconstruction from historical activity records.

CONTEXT
I'm designing a system that takes a holistic, retrospective view of a person's
work — coding, web browsing, chat, meetings, document authoring — and
reconstructs how their time/effort is distributed across task kinds,
aggregatable by day/week/month/year. It is opt-in self-analysis on the user's
own data. It reads only historical records that already exist (local files,
AI-agent session logs, editor history, browser history, filesystem recent-
files, git history, calendar/email exports) — no always-on watcher, no
real-time instrumentation. Open-source only.

I already know the OSS tool landscape is thin here (Memacs, ActivityWatch,
Hourgit, Promnesia, Git Timeline MCP, TimeTracker MCP — none do multi-source
retrospective fusion with a task model). So I'm NOT looking for more product
surveys. I'm looking for METHODS, ALGORITHMS, and RESEARCH that solve the
hard sub-problems below, from adjacent fields that may have already worked on
them.

THE HARD SUB-PROBLEMS (find techniques for each)

1. TASK BOUNDARY DETECTION from a stream of heterogeneous events. How do you
   segment an activity timeline into discrete "tasks" (goal-directed work
   sessions) when there's no explicit task marker? Signals available: user-
   message turns in AI sessions, git branch checkouts (reflog) and commits,
   editor file-edit timestamps, browser visit clusters, calendar events.

2. MULTI-SOURCE EVENT FUSION into a unified timeline. Events come from
   sources with different schemas, granularities, and timestamp formats (ISO
   8601 strings, epoch millis, Chrome's micros-since-1601, .ics DTSTART).
   How do you normalize, de-duplicate, and correlate events across sources
   into one coherent timeline?

3. CROSS-SOURCE TASK IDENTITY (entity resolution across sources). When the
   same underlying task produces traces in several sources (e.g. an AI coding
   session + a git commit + a browser search all belong to one task), how do
   you determine that these traces belong together? This is the hardest part
   of fusion — an entity-resolution / record-linkage problem across
   heterogeneous event sources. What temporal, semantic, and contextual cues
   work for linking traces to a single task?

4. AUTOMATIC TASK CATEGORIZATION. How do you classify tasks into kinds
   (coding, meetings, research, communication, documentation) without manual
   rules? Signals: file paths + package manifests (domain detection), commit
   messages, browser URL domains, session titles, tool-call patterns, email
   subjects. What works — rule induction, clustering, embedding-based
   classification, LLM-based labeling?

5. EFFORT vs. TIME. Time is wall-clock span; effort is harder. Available
   effort signals: per-message token usage in AI session logs, edit density
   from editor history, commit size. How do others distinguish "active work"
   from "session open but idle"? How do you estimate human effort when you
   only see AI-effort or artifact-density?

6. TASK I/O + SUCCESS ATTRIBUTION. How do you attribute artifacts and
   outcomes to a task? Specifically: (a) INPUT — linking the prompts, files,
   and context that fed a task; (b) OUTPUT — linking the artifacts a task
   produced (edited files, commits, command results, documents) back to the
   task; (c) SUCCESS/FAILURE — classifying whether a task achieved its goal
   from indirect signals (task-status fields, tool errors, user corrections
   following the task, follow-up messages that reopen the question). What
   methods exist for artifact-to-task linking and outcome classification?

7. EVALUATION / GROUND TRUTH. How do you validate reconstructed tasks when
   there's no ground truth? If we build heuristics for boundary detection,
   categorization, and success attribution, how do we measure correctness?
   Are there annotated personal-activity datasets, inter-rater agreement
   methods for task segmentation, or proxy-validation techniques for
   retrospective reconstruction?

ADJACENT FIELDS TO CHECK (not exhaustive — follow where the methods lead)
- Process mining (discovering process/task structure from event logs)
- Ubiquitous computing / human activity recognition (from digital sensors)
- Personal informatics / quantified-self (self-tracking frameworks)
- Digital forensics timeline correlation (fusing multiple log sources)
- Sequence segmentation / temporal clustering
- Event-log fusion in SIEM/security contexts
- Record linkage / entity resolution (for cross-source task identity)
- Information retrieval provenance & attribution (for task I/O linking)
- Workplace / personal analytics research literature

WHAT TO REPORT
For each relevant method, technique, or paper: what problem it solves, which
sub-problem above it addresses, how it works at a high level, what data it
assumes, known failure modes / where it breaks, whether it's been implemented
in open source, and how adoptable it is for a Python-based retrospective
analyzer reading local + remote records. Prioritize actionable techniques
over survey breadth.
```

Framing notes:
- **Sub-problems named, not solutions prescribed** — no "use HMMs" / "use DBSCAN". Right level
  for deep research; too open yields a shallow survey, naming the sub-problems focuses it.
- **Cross-source task identity (#3) split out from fusion** — the hardest part of fusion is
  entity resolution across sources; foregrounding it ensures it's treated as first-class.
- **Task I/O + success attribution (#6)** is our differentiator — without it the researcher
  returns segmentation/categorization but nothing on artifact-to-task linking or outcomes.
- **Evaluation / ground truth (#7)** — needed to validate the heuristics we build.
- **"Known failure modes" in report fields** — our sources vary wildly in density (Claude
  Code: 39k lines vs. legacy codeagent: 1 session), so where a method breaks matters as much
  as what it solves.
- **Process mining is the highest-value adjacent-field lead** — discovering process structure
  from event logs may reframe the task-model design.

Results: merged below — the full deep-research report, with our assessment as the
synthesis wrapper.

---

## Deep research results (received 2026-07-29)

The deep-research agent returned a full report on algorithmic foundations for the seven
sub-problems. The full content is merged below (sections 1–7), followed by our synthesis
(three high-leverage finds, compact catalog, library-verification notes).

**Assessment of the report:** substantively real — core libraries cited (Plaso, pm4py,
ruptures, Splink, igraph/Leiden, wittgenstein, prov, segeval) all exist and are the right
tools; the math (PELT cost function, Fellegi-Sunter m/u, Allen's 13 relations, exponential
temporal decay) is stated correctly; failure modes are the honest ones.

**Citation caveat:** the Works Cited list (appended at the end) is truncated at #27 but
in-text citations run to ~#52. The other agent explained this as "numbering from a broader
index" — the gaps are understood but the missing refs are not resolvable from the document.
Actionable content (algorithms, library names, failure modes) is self-contained enough that
this doesn't block adoption; it only blocks tracing a specific claim to its source.

**Math rendering note:** the original report embedded equations as image placeholders that
did not render. They have been converted to prose here; where a formula is load-bearing it is
written inline.

### Three high-leverage finds (our synthesis — these reshape the design)

1. **OCEL 2.0 / Object-Centric Process Mining (§1.2) — reframes the storage shape.** A flat
   timeline (Memacs/Plaso shape) *cannot* represent many-to-many event↔object relations
   without duplication — but "a task touches multiple files, and a file is touched by multiple
   tasks" is exactly that. OCEL 2.0's E2O/O2O relational model handles it natively; pm4py
   supports it. Likely replaces "flat timeline" as the fusion-target schema. Resolves (or at
   least informs) the open storage-shape question.

2. **Plaso as fusion co-reference (§1.1) — stronger than Memacs for normalization.**
   Industrial-strength version of the adapter-registry pattern: decoupled parsers →
   normalized microsecond-epoch → deduped storage. Battle-tested in forensics. Elevate to
   co-reference alongside Memacs: Plaso for normalization/dedup machinery, Memacs for the
   personal-data module shape. Known failure mode: clock skew across devices causes
   chronological inversions; flat event structure struggles with semantic relations (which
   OCEL 2.0 solves).

3. **AI-effort discounting mechanism (§5.2) — solves the differentiator's hardest sub-problem.**
   We flagged "per-message usage measures AI-effort, not human-effort" as unsolved. The report
   gives the precise mechanism: cross-reference git diffs against preceding AI responses; if a
   large diff matches an AI output's code blocks, discount the human-effort score heavily.
   Concrete and implementable — the bridge between our two effort signals (AI `usage` tokens
   vs. artifact density).

---

### Full report: Retrospective Multi-Source Task and Time Reconstruction — Algorithmic Foundations

The retrospective reconstruction of personal tasks and time allocation from disparate digital
traces presents a formidable challenge in computational analytics and personal informatics.
As digital workspaces fracture across local file systems, IDEs, web browsers, and autonomous
AI agents, tracking human cognitive effort requires systems capable of ingesting highly
heterogeneous, asynchronous event logs. The objective is to define the mathematical,
algorithmic, and architectural methodologies required to synthesize a unified, privacy-
preserving, retrospective activity timeline without relying on persistent, real-time
surveillance instrumentation.

By surveying adjacent domains — digital forensics, streaming process mining, graph theory,
probabilistic record linkage, and temporal logic — this report delineates robust, Python-
compatible solutions for seven fundamental sub-problems: temporal normalization, unsupervised
task boundary detection, cross-source entity resolution, automated categorization, effort
estimation, artifact provenance, and heuristic evaluation. Each methodology is evaluated on
its theoretical mechanism, assumed data structures, open-source Python adaptability, and
inherent failure modes.

#### 1. Multi-Source Event Fusion and Temporal Normalization

The fundamental prerequisite for retrospective analysis is harmonizing disparate event logs.
A knowledge worker generates artifacts with fundamentally distinct schemas, granularities, and
temporal encodings: an IDE logs Unix epoch milliseconds, a web browser uses Chrome's
microseconds-since-1601, calendar exports use ISO 8601 or `.ics` DTSTART. Fusing these into a
single chronological timeline requires robust parsing, normalization, and deduplication.

##### 1.1 Digital Forensic Timelining Architectures

The digital forensics domain provides battle-tested methodologies. The `log2timeline`
architecture, part of the **Plaso** framework, is the standard computational model. Plaso is
an open-source, Python-based engine designed to parse varied forensic artifacts — from file
system metadata to application-specific databases — and normalize them into a unified
super-timeline.

The Plaso pipeline operates through discrete stages: extraction, normalization, serialization.
Event parsers are decoupled from the core engine, allowing rapid induction of custom Python
parsers for local JSON lines, git reflogs, or agent session logs. Plaso addresses timestamp
heterogeneity by mapping all extracted temporal data into a standardized microsecond-precision
epoch format, storing results in a compressed SQLite-based `.plaso` dump file. The
architecture deduplicates overlapping records by hashing the event payload and tracking file
offsets. Subsequent processing uses the `psort` tool to filter, slice, and export the timeline
into CSV or Elasticsearch indices.

**Failure modes when applied to personal analytics:** clock skew across local devices or
remote servers can introduce chronological inversions (a response appears to precede a
request). Plaso assumes a flat event structure, which struggles to natively represent complex
semantic relationships between events and objects without massive data duplication.

##### 1.2 Object-Centric Event Logs (OCEL 2.0)

A flat tabular structure is insufficient for representing modern digital work. In a flat
timeline, representing that a single task involves multiple distinct entities (an IDE file, a
browser tab, a terminal command) requires duplicating event rows or losing relational context.

The process mining discipline has pivoted toward **Object-Centric Process Mining (OCPM)** to
solve this convergence/divergence problem. The **OCEL 2.0** standard provides a rigorous
metamodel for many-to-many relationships between events and objects. In OCEL 2.0, events are
discrete, time-stamped occurrences that do not contain payload data themselves; rather, they
are linked via **Event-to-Object (E2O)** and **Object-to-Object (O2O)** relational mappings.
OCEL 2.0 supports dynamic object attributes, enabling the system to track the evolving state
of an artifact (e.g., a source file's size or complexity) over time.

For a Python-based analyzer, the **pm4py** library allows native ingestion, manipulation, and
analysis of OCEL 2.0 relational databases. Mapping the fused timeline into an OCEL 2.0 SQLite
structure preserves the distinct lifecycle of a "Git Repository" object independently of a
"Browser Session" object, while observing the intersection of these objects during a specific
task event.

| Fusion Paradigm | Core Architecture | Primary Python Library | Assumed Data Structure | Known Failure Modes |
| :---- | :---- | :---- | :---- | :---- |
| **Forensic Super-Timeline** | Worker-based parsing, microsecond epoch normalization | `plaso` (log2timeline) | Flat tabular events, isolated timestamps | Clock skew across devices; duplication of relational data; difficult to query entity lifecycles. |
| **Object-Centric Process Mining** | Relational E2O and O2O mapping | `pm4py` (OCEL 2.0) | Relational SQLite / XML / JSON with dynamic attributes | High memory overhead for dense event streams; requires upfront schema mapping. |

#### 2. Unsupervised Task Boundary Detection

Segmenting a continuous, unannotated stream of digital exhaust into discrete, goal-directed
work sessions is a major algorithmic challenge. Because the system operates retrospectively on
local files and logs, it must detect implicit context shifts without explicit start/stop
markers. Available signals: temporal gaps, application switching, domain transitions.

##### 2.1 Penalized Change Point Detection (CPD)

Detecting a task boundary can be modeled as a **Change Point Detection** problem. CPD
algorithms partition a time series into segments by identifying points where the statistical
properties of the data shift significantly. In user activity, a change point represents a
shift in the distribution of accessed file paths, active window titles, or network domains.

The **Pruned Exact Linear Time (PELT)** algorithm provides an optimal approach for sequence
segmentation by minimizing a penalized cost function. The goal is to find the number of change
points and their positions that minimize: the sum of segment costs plus a linear penalty (β)
on the number of change points. Formally, minimize `Σ C(y[i..j]) + β·K`, where `C` is a cost
function (e.g., negative log-likelihood of the segment under a chosen distribution), `β` is a
penalty to prevent overfitting, and `K` is the number of change points. The open-source
Python library **ruptures** provides optimized PELT implementations. Applying PELT to a
multivariate time series of one-hot encoded activity domains reliably detects context
switches.

**Failure mode:** over-segmentation when the penalty β is set too low, interpreting brief
multitasking interruptions (e.g., replying to a single chat message) as entirely new task
boundaries.

##### 2.2 Distributional Modeling of Inter-Arrival Times

Another signal is the temporal gap between consecutive events. Cognitive tasks produce
clustered bursts of interaction separated by periods of inactivity (reading, thinking, task
switching). The inter-arrival time — elapsed time between consecutive events — often exhibits
a heavy-tailed distribution in human-computer interaction.

Research in network traffic analysis and behavioral modeling shows that representing inter-
arrival times using **Gaussian Mixture Models (GMMs)** or log-normal mixtures effectively
separates intra-task event gaps from inter-task boundaries. By fitting a two-component GMM to
the log-transformed inter-arrival times of a user's historical data, the system dynamically
learns a personalized threshold: the component with the lower mean represents continuous
execution of a single task; the component with the higher mean represents task-switching or
natural breaks. When an inter-arrival gap exceeds the probabilistic threshold connecting the
two distributions, a task boundary is inferred.

**Failure mode:** this approach assumes tasks are fundamentally sequential; it breaks down in
highly concurrent environments where a user rapidly interleaves actions across multiple
distinct tasks without significant temporal gaps.

##### 2.3 Streaming Process Mining and Concept Drift

In streaming process mining, the phenomenon where a process changes its fundamental behavior
over time is **concept drift**. Detection techniques employ adaptive windowing: comparing the
probability distributions of events in a reference window (historical) against a detection
window (recent) using statistical hypothesis testing. If the p-value falls below a
significance threshold, a concept drift — interpreted here as a task switch — is flagged.

These heuristics are robust against noise and identify both sudden task switches and gradual
transitions (e.g., slowly pivoting from IDE coding to exploratory web research). The AVOCADO
framework, for standardizing streaming process mining challenges, highlights that such
algorithms must process data incrementally and evaluate processing latency alongside
accuracy. For retrospective analysis, incremental processing lets the analyzer parse massive
historical logs sequentially without loading the entire timeline into memory.

#### 3. Cross-Source Task Identity and Entity Resolution

The most complex phase of retrospective fusion is determining that a sequence of browser
events, a cluster of IDE edits, and a terminal execution all belong to one semantic task.
This requires **Entity Resolution (ER)** — also known as record linkage or deduplication —
across domains with completely disparate schemas. Traditional deterministic matching fails
here: browser logs and git commits share no explicit foreign keys.

##### 3.1 Probabilistic Record Linkage: The Fellegi-Sunter Model

The foundational mathematical framework is the **Fellegi-Sunter model**, which computes the
probability that two records refer to the same underlying entity based on agreement or
disagreement of their attributes. The model estimates two parameters per attribute compared:

- **m-probability:** the probability that an attribute agrees *given that* the records belong
  to the same true task.
- **u-probability:** the probability that an attribute agrees by random chance *given that*
  the records belong to entirely different tasks.

For Python, the open-source library **Splink** offers a highly scalable engine using DuckDB
for local execution. Splink calculates match weights using an unsupervised **Expectation-
Maximization (EM)** algorithm — no pre-labeled training dataset is needed to learn the m and
u probabilities. By defining custom comparison functions (e.g., Jaccard similarity between
words in a browser page title and a git commit message; verifying timestamps fall within a
configurable temporal collar), Splink probabilistically links multi-source traces into unified
task clusters.

**Failure mode:** the Fellegi-Sunter model (and Splink) assumes **conditional independence
among attributes**. If the input contains highly correlated columns (e.g., a browser URL and
a page title often contain the same repository name), the model double-counts the evidence,
producing artificially inflated match probabilities and false positives.

##### 3.2 Temporal Graph Clustering and Community Detection

An alternative methodology maps the problem into a temporal graph space. Every discrete event
sequence (the sub-tasks from §2) becomes a node. Edges between nodes are weighted by a fusion
of temporal proximity and semantic similarity. To account for chronological decay of
relevance, the edge weight between node i and node j is subjected to an exponential decay
function based on their time difference Δt: `w_ij = sim(i,j) · e^(-λ·Δt)`, where `sim(i,j)`
is the cosine similarity of tf-idf vectors or LLM embeddings of the event payloads.

Once the temporal graph is constructed, **community detection** algorithms isolate the
discrete tasks. The **Leiden algorithm** — an improvement over Louvain — optimizes graph
modularity, partitioning nodes into densely connected clusters with mathematically guaranteed
connectivity. Each resulting cluster represents a canonical task, linking the AI prompt, the
subsequent IDE edits, and the final git commit into a unified identity graph. Python libraries
such as **GoldenMatch** leverage this combination of LLM-based semantic matching and graph
resolution for zero-configuration entity resolution with persistent identity graphs.

| Entity Resolution Technique | Mathematical Foundation | Primary Python Libraries | Strengths for Task Fusion | Known Failure Modes |
| :---- | :---- | :---- | :---- | :---- |
| **Probabilistic Linkage** | Fellegi-Sunter Model, Expectation-Maximization | `Splink` | Unsupervised parameter estimation; scalable to millions of records via DuckDB. | Fragile with highly correlated attributes (violates conditional independence). |
| **Temporal Graph Clustering** | Modularity optimization, exponential time decay | `GoldenMatch`, `igraph` (Leiden) | Naturally models time-decaying relevance; resilient to missing schema attributes. | Computationally expensive embedding generation; requires careful tuning of the decay parameter λ. |

#### 4. Automatic Task Categorization

After segmentation and grouping, the system must autonomously classify tasks into higher-level
domains (coding, research, communication, documentation) without fragile manually curated
rules. Signals: file paths, package manifests, commit messages, browser URL domains, session
titles, email subjects.

##### 4.1 Count-Based and Distributional Embeddings

Inferring a task's category from low-level events requires understanding semantic context. In
process mining, distributional similarity posits that events in similar chronological contexts
share a semantic relationship. While neural embeddings (Word2Vec adapted for event logs) can
capture this, recent research highlights the efficacy of **count-based embeddings** for event
data: because the vocabulary of a personal activity log (unique application names, base URLs,
file extensions) is substantially smaller than natural language, direct encoding of
co-occurrences using **Positive Pointwise Mutual Information (PPMI)** matrices provides highly
effective, computationally inexpensive representations. Generating an embedding for a task
cluster based on tf-idf weighting of its constituent URLs, file extensions, and executable
names lets unsupervised algorithms (K-means, DBSCAN) automatically group tasks into
homogeneous, unnamed categories.

##### 4.2 LLM-Based Context Segmentation and Labeling

Localized LLMs offer zero-shot/few-shot task categorization, assigning human-readable labels
to the clusters above. Open-source Python frameworks such as **llm-context-ts** demonstrate
that models like Mistral or DeepSeek-R1 can accurately classify and summarize textual
representations of event sequences. In a local setup, the system parses the dominant signals
from a resolved task — git diff text, LLM prompt history, browser page titles — into a
structured prompt. The LLM acts as an extraction agent, inferring the underlying objective and
assigning a semantic category. To prevent semantic drift over time, **Retrieval-Augmented
Generation (RAG)** supplies the LLM with historical categorizations (exemplars) to maintain a
consistent taxonomy across months of data.

**Failure mode:** context window overflow — supplying raw git diffs or massive terminal
outputs exhausts local LLM capabilities, requiring aggressive pre-summarization or keyword
extraction pipelines.

##### 4.3 Rule Induction as an Interpretable Fallback

Rule induction algorithms offer transparency and execution speed. **RIPPER** (Repeated
Incremental Pruning to Produce Error Reduction) inductively learns if-then-else rules from
data. Using the open-source Python package **wittgenstein**, a system can train a RIPPER model
on a small subset of user-labeled or LLM-labeled tasks. The resulting rules (e.g., `IF
domain="github.com" AND extension=".py" THEN category="Coding"`) execute with near-zero
computational overhead and allow users to manually audit, correct, and adjust the
categorization logic — ensuring the user retains ultimate agency over how their personal data
is classified, addressing the "black box" criticism of pure neural approaches.

#### 5. Estimating Effort Versus Wall-Clock Time

A critical distinction: total elapsed time (wall-clock span) vs. actual cognitive effort. A
task might span four hours from first log entry to final commit, yet the user spent three of
those hours in an unrelated meeting or away from the keyboard. Reconstructing true effort
requires transitioning from point-in-time timestamps to interval-based reasoning.

##### 5.1 Temporal Reasoning via Allen's Interval Algebra

The system uses **Allen's Interval Algebra** — the standard calculus for reasoning about
temporal durations in AI, defining 13 mutually exclusive and exhaustive relations between time
intervals (BEFORE, MEETS, OVERLAPS, STARTS, DURING, FINISHES, and their inverses). By
expanding discrete point-in-time events into intervals using a configured temporal "collar"
(assigning an event a duration of N seconds), the system evaluates the intersection of
intervals across all sources linked to a task.

| Allen's Relation | Application in Retrospective Activity Tracking |
| :---- | :---- |
| **PRECEDES / BEFORE** (A ends before B begins) | If the gap exceeds the GMM inter-arrival threshold, the intervening time is classified as idle and excised from effort calculations. |
| **MEETS** (A ends exactly when B begins) | Immediate transition (e.g., closing an IDE and immediately opening a browser). Continuous effort is accumulated. |
| **OVERLAPS** (A and B overlap in time) | Concurrent execution; the user is actively referencing two applications. The union of the intervals represents total effort, avoiding double-counting. |
| **DURING** (A occurs entirely within B) | A short, discrete action conducted while a long-running process is active. |

The union of overlapping and meeting intervals yields total active effort time. If intervals
exhibit BEFORE/AFTER with a gap exceeding the inter-arrival threshold from §2, the intervening
duration is excised. This distinguishes active engagement from idle suspension (e.g., leaving
a browser tab open while walking away).

##### 5.2 Artifact-Density and Proxy Signals

When explicit duration data is absent (an IDE failing to log focus events, offline reading),
the system relies on artifact density. In AI-assisted workflows, **token usage per message
turn** is a reliable proxy for cognitive load and prompt-engineering time. In code editors,
keystroke density or volume of lines changed (via git diffs) serves as an estimator. Mapping
these discrete volume metrics against the continuous temporal intervals from Allen's Algebra
yields an "intensity score" for the task.

**Failure mode:** conflation of automated generation with human effort. A massive file change
generated by an AI agent or formatting script exhibits high density but low human cognitive
effort. **Countermeasure:** cross-reference git diffs with AI agent session logs; if a large
diff immediately follows an AI response containing identical code blocks, the human-effort
score is heavily discounted. *(This is the mechanism highlighted in our high-leverage find #3
— it bridges AI-effort and artifact-density signals.)*

#### 6. Task I/O Provenance and Success Attribution

To transform a time-tracker into a work-reconstruction system, the tool must attribute inputs
(consumed information) and outputs (produced artifacts) to inferred tasks, and evaluate
whether the task was successfully completed.

##### 6.1 Information Provenance Tracking via PROV-O

Tracking task inputs/outputs maps to information provenance. The W3C **PROV-O** ontology
provides a standardized data model. In Python, the **prov** library generates semantic
provenance graphs. Modeling a reconstructed task as an **Activity** node, the system links
input references — **Entity** objects (a viewed StackOverflow page, a read PDF, an AI prompt)
— via the `used` relationship. Outputs (a modified `.py` file, a generated image, a compiled
binary) are linked via `wasGeneratedBy`. This directed acyclic graph enables root-cause
analysis: "Which specific web searches and AI conversations directly led to the implementation
of this feature branch?"

##### 6.2 Semantic Role Labeling for Outcome Classification

Determining task success from indirect, un-instrumented signals requires extracting semantic
meaning from unstructured logs (commit messages, terminal outputs, subsequent AI prompts).
**Semantic Role Labeling (SRL)** processes these texts to identify actions, actors, and
business objects. Heuristic state machines infer outcomes from the sequencing of these roles:
if a task concludes with an error code in the terminal log, followed immediately by an AI
prompt containing stack-trace data, the engine infers "Failure / Retry"; if a coding sequence
is followed by a git commit labeled "Fix issue #402" and `npm run test` returns exit code 0,
the task is classified "Success". Modern LLM-based metadata extraction can process the
terminal/editor exhaust at the end of a task interval to generate confidence-scored success
metrics.

**Failure mode:** this struggles when goals are implicit or open-ended. Exploratory research
tasks rarely end in a definitive success/failure event, often fading into a different
activity. In such cases, outcome classification defaults to "Completed / Abandoned" based
purely on temporal expiration.

#### 7. Heuristic Evaluation and Ground Truth Proxies

A critical barrier in unsupervised retrospective log analysis is the lack of labeled ground
truth. When the system segments a timeline and categorizes tasks automatically, traditional
precision/recall/F1 are incalculable without manual annotation. To validate the heuristic
engines, the system employs specialized segmentation metrics, continuous intrinsic
evaluation, and framework-level proxy testing.

##### 7.1 Text and Sequence Segmentation Metrics

To evaluate boundary detection (§2), the system uses metrics developed in NLP for topic
segmentation. Standard precision/recall fail in sequence segmentation because they severely
penalize "near-miss" boundaries — if the algorithm places a boundary at 10:04 instead of the
true 10:05, exact-match metrics score it as total failure. The Python packages **segeval** and
**chunkseg** implement robust alternatives:

| Metric | Mechanism | Utility in Retrospective Reconstruction |
| :---- | :---- | :---- |
| **Pk Metric** | Probability that a sliding window of size k ends in different segments in predicted vs. reference data. | Highly robust to near-miss boundary predictions; provides a probabilistic error rate. |
| **WindowDiff** | Counts the absolute difference in boundaries within a sliding window; penalizes false positives and false negatives equally. | More stable than Pk for varying task lengths; standard for sequence boundary validation. |
| **Boundary Edit Distance (BED)** | Minimum edit operations (insertions, deletions, substitutions) to transform predicted boundaries into reference boundaries. | Gracefully handles temporal data where an event is offset by a few seconds. |
| **Collar-Based F1** | A predicted boundary is a true positive if it falls within N collar seconds of a reference boundary. | Ideal for evaluating temporal boundaries independent of the underlying log format. |

By manually annotating a small benchmark subset of their own personal data (e.g., reviewing one
day of logs), users can tune PELT penalties and GMM thresholds using WindowDiff and Collar-
Based F1 to optimize segmentation before deploying fully unsupervised.

##### 7.2 Unsupervised Assessment and Challenge Frameworks

In the process mining community, frameworks like AVOCADO evaluate streaming algorithms on
processing latency, robustness to concept drift, and mean absolute error in the absence of
perfect static logs. For this system, continuous intrinsic evaluation of the Entity Resolution
phase is necessary: mathematically measure cluster cohesion and separation (Silhouette
scores, Modularity metrics) for the temporal graphs. If Leiden generates clusters with high
internal density and sparse inter-cluster edges, the ER engine is functioning optimally even
without human verification. **Leave-One-Out Cross-Validation (LOOCV)** can be adapted for
rule-induction training, ensuring categorization rules generalize across days/weeks rather
than overfitting to a specific project.

#### Conclusion (report's)

The retrospective, multi-source reconstruction of personal tasks from passive digital records
requires synthesizing techniques from disparate computational fields. Normalizing
heterogeneous timestamps via forensic architectures (Plaso) and structuring them relationally
through Object-Centric Process Mining (OCEL 2.0 via pm4py) establishes the foundation.
Algorithmic change point detection (PELT) and probabilistic record linkage (Fellegi-Sunter
via Splink, or Leiden temporal graph clustering) autonomously segment the timeline and bind
cross-platform events into singular task entities. Estimating cognitive effort rather than
raw elapsed time requires Allen's Interval Algebra to model overlaps and interruptions.
Paired with localized LLM-based categorization, count-based embeddings, and W3C PROV-O
provenance tracking, the architecture delivers privacy-preserving insights into productivity,
context switching, and task outcomes entirely from historical, un-instrumented system exhaust.
Segmentation metrics (WindowDiff, Collar-Based F1) rigorously tune and validate the heuristics
despite the lack of explicit ground truth.

---

### Algorithm catalog (compact, per sub-problem — our synthesis)

| Sub-problem | Candidate method | Library | Failure mode |
|---|---|---|---|
| 1. Fusion + normalization | Forensic super-timeline (decoupled parsers → µs-epoch → dedup) | `plaso` (log2timeline) | clock skew; relational duplication (OCEL fixes this) |
| 1. Fusion storage shape | Object-Centric Event Log 2.0 (E2O/O2O relations) | `pm4py` | high memory on dense streams; upfront schema mapping |
| 2. Boundary detection | PELT change-point detection (penalized cost) | `ruptures` | over-segmentation if penalty β too low (flags a chat reply as a new task) |
| 2. Boundary detection (gaps) | 2-component GMM on log inter-arrival times | `sklearn` | breaks under heavy task interleaving (no clean gaps) |
| 2. Boundary detection (drift) | Adaptive windowing + hypothesis test (concept drift) | custom | — |
| 3. Cross-source identity | Fellegi-Sunter probabilistic record linkage (unsupervised EM) | `Splink` (DuckDB) | conditional-independence violation — correlated URL+title double-counts evidence |
| 3. Cross-source identity (alt) | Temporal-decay graph + Leiden community detection | `igraph`, GoldenMatch | embedding cost; decay-param tuning |
| 4. Categorization | PPMI embeddings + K-means/DBSCAN; LLM + RAG for taxonomy consistency; RIPPER rules as interpretable fallback | `wittgenstein`, local LLM | LLM context overflow on raw diffs; needs pre-summarization |
| 5. Effort vs time | Allen's Interval Algebra (13 relations) + artifact density | custom | conflation of AI-generated diffs with human effort (solved by find #3) |
| 6. Task I/O | PROV-O provenance graph (`used` / `wasGeneratedBy`) | `prov` | — |
| 6. Success/failure | Semantic Role Labeling + heuristic state machine | LLM-based | open-ended/research tasks default to "abandoned" on temporal expiry |
| 7. Evaluation | WindowDiff, Pk, Boundary Edit Distance, Collar-Based F1 | `segeval`, `chunkseg` | needs a small manually-annotated benchmark subset |

### Libraries to verify before committing

Core libs I'm confident exist: `plaso`, `pm4py`, `ruptures`, `Splink`, `igraph`, `wittgenstein`,
`prov`, `segeval`. Two were flagged for doubt; the other agent confirmed both:

- **GoldenMatch** — polyglot (Python via PyPI + TypeScript via npm) Fellegi-Sunter + LLM entity
  resolution. Confirmed real by the other agent. Not independently verified here; if it fails
  to install, fall back to `Splink` + `igraph`/Leiden — the methods are available independently.
- **llm-context-ts** — Python research repo (HumanMachineLab); `-ts` = "text segmentation",
  not TypeScript. Confirmed real by the other agent. Evaluate-topic-segmentation approach;
  library is replaceable, the method (local LLM for topic boundary detection) is not.

A `pip index versions` check on the eight core libs before committing to them in the design
would be the natural next verification step.

### Works cited (as provided — truncated at #27; in-text citations run to ~#52)

1. Using log2timeline.py — the Plaso documentation — Read the Docs, https://plaso.readthedocs.io/en/latest/sources/user/Using-log2timeline.html
2. Plaso — LimaCharlie Documentation, https://docs.limacharlie.io/5-integrations/extensions/third-party/plaso/
3. Super Timeline Using ELK Stack — Network Intelligence, https://www.networkintelligence.ai/blogs/super-timeline-using-elk-stack/
4. building-incident-timeline-with-timesketch • Anthropic-Cybersecurity-Skills — Tessl, https://tessl.io/registry/skills/github/mukul975/Anthropic-Cybersecurity-Skills/building-incident-timeline-with-timesketch
5. Create a Super Timeline with TACTICAL/IREC Triage Image — Vikas Singh — Medium, https://vikas891.medium.com/create-a-super-timeline-with-tactical-irec-triage-image-ca5114b83b6f
6. plaso.parsers.text_plugins package — Plaso (log2timeline) 20260512 documentation, https://plaso.readthedocs.io/en/stable/sources/api/plaso.parsers.text_plugins.html
7. Intelligent Forensics in Next-Generation Mobile Networks — arXiv, https://arxiv.org/html/2603.29364v1
8. Time and Relations into Focus: Ontological Foundations of Object-Centric Event Data — arXiv, https://arxiv.org/pdf/2512.14425
9. OCEL (Object-Centric Event Log) 2.0 Specification — arXiv, https://arxiv.org/html/2403.01975v1
10. OCEL (Object-Centric Event Log) 2.0 Specification — arXiv, https://arxiv.org/pdf/2403.01975
11. arXiv:2309.14092v1 [cs.DB] 25 Sep 2023, https://arxiv.org/pdf/2309.14092
12. Visual OCEL 2.0 Editor — PADS@RWTH Aachen, https://www.pads.rwth-aachen.de/global/show_document.asp?id=aaaaaaaacwerskq&download=1
13. pm4py — OCEL 2.0, https://www.ocel-standard.org/tool-support/libraries/pm4py/
14. PM4Py Feature Overview — Process Intelligence Solutions GmbH (P.I.S.), https://processintelligence.solutions/pm4py/features
15. Towards a Simple and Extensible Standard for Object-Centric Event Data (OCED) — Core Model, Design Space, and Lessons, https://www.tf-pm.org/upload/1728651303832.pdf
16. (PDF) ruptures: change point detection in Python — ResearchGate, https://www.researchgate.net/publication/322243109_ruptures_change_point_detection_in_Python
17. Productive, Anxious, Lonely — 24 Hours Without Push Notifications — arXiv, https://arxiv.org/pdf/1612.02314
18. Intelligent Notification Systems: A Survey of the State of the Art and Research Challenges — arXiv, https://arxiv.org/pdf/1711.10171
19. Evaluating Diverse Feature Extraction Techniques of Multifaceted IoT Malware Analysis: A Survey — arXiv, https://arxiv.org/html/2509.03442v1
20. Probabilistic Delay Forecasting in 5G Using Recurrent and Attention-Based Architectures — arXiv, https://arxiv.org/pdf/2503.15297
21. Towards Zero Touch Networks: Cross-Layer Automated Security Solutions for 6G Wireless Networks — arXiv, https://arxiv.org/html/2502.20627v1
22. Task-based preemptive scheduling on FPGAs leveraging partial reconfiguration — arXiv, https://arxiv.org/pdf/2301.07615
23. Change Point Detection and Dealing with Gradual and Multi-order Dynamics in Process Mining — ResearchGate, https://www.researchgate.net/publication/300569169_Change_Point_Detection_and_Dealing_with_Gradual_and_Multi-order_Dynamics_in_Process_Mining
24. Change Point Detection and Dealing with Gradual and Multi-Order Dynamics in Process Mining — Wil van der Aalst, https://www.vdaalst.com/publications/p822.pdf
25. AVOCADO: The Streaming Process Mining Challenge — arXiv, https://arxiv.org/html/2510.17089v1
26. AVOCADO: The Streaming Process Mining Challenge — OceanRep, https://oceanrep.geomar.de/63821/1/Avocado_paper_07.pdf
27. Streaming Process Mining over Realistic Event Streams, https://dl.gi.de/bitstreams/b0ba2223-53b8-4fd3-9969-bbfe0cf517f4/download

*(Citations 28–52 are referenced in-text but were not included in the report's Works Cited
list; see the citation caveat above.)*

### Status

Recorded as assessment only — no design committed. The three high-leverage finds (especially
OCEL 2.0 as storage schema) are real architectural choices that deserve a deliberate decision
before being folded into SKILL.md. The `PLAN.md` phases 4 and 5 are where these methods enter
implementation. Next step: verify the core libraries, then commit to a chosen stack per sub-
problem as each phase is reached.
