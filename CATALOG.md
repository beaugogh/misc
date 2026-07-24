# Catalog

A machine- and human-readable index of **every agent-facing artifact** in this
repo — skills (own + three external collections) and OpenCLI plugins — so an
external agent can survey what's available in one place.

## How an agent should use this

Read the sections below, pick the artifacts relevant to the user's task, and
**recommend** them (name + path). The user activates picks manually — do not
attempt to install anything yourself. Prefer stable skills; skip any flagged
⚠️ deprecated or 🚧 in-progress unless the user asks for them.

There are **two kinds** of artifact, with different activation models — an
agent must know which is which:

- **Skill** — open its `SKILL.md` (linked from the path) and follow the steps.
  Self-contained instructions, no prerequisites. Portable as a document.
- **OpenCLI plugin** — a CLI command `opencli <plugin> <command>` you call.
  Needs `opencli` + the Browser Bridge set up and (for Huawei-site plugins) a
  logged-in Huawei session in Chrome — all human one-time setup. Portable as a
  *command*, not as pure code. See [`opencli-plugins/README.md`](./opencli-plugins/README.md)
  for prerequisites and install.

Regenerate after adding/removing skills or plugins: `./scripts/generate-catalog.sh`

## Skills

### Own skills (skills/) (13)

| Skill | Description |
|---|---|
| [`adversarial-review`](./skills/adversarial-review) | Production-grade review of any artifact (source code, prompt, SKILL.md, AGENTS.md, CLAUDE.md, workflow definition, configuration, specification, documentation, tool schema, evaluation, or a combination) as if you are the senior engineer, staff architect, and final approver responsible for deploying it. Falsify-first: assume the artifact contains flaws even if it appears correct, actively search for evidence that it is wrong before searching for evidence that it is right, and spend at least as much effort attempting to break the solution as was spent creating it. Use when you are about to ship, merge, or hand off an artifact and want a rigorous final gate — not a surface "looks good" pass. Outputs a structured review (intent alignment, adversarial analysis scratchpad, issues by severity, test/evaluation gaps, alternative designs, confidence, approval decision, and a corrected artifact if any issues are found). Does not defend the implementation or assume design decisions were intentional. |
| [`analyze-paper-corpus`](./skills/analyze-paper-corpus) | Analyzes a corpus of harvested academic papers (markdown files from top AI venues or arXiv) against a reference/context document (e.g., a design brainstorm, project proposal, or system architecture doc). Extracts abstracts from all papers, screens each against the reference context, flags only papers with genuinely novel and relevant ideas, and composes a structured findings document organized by topic. Use when the user has a harvested paper corpus and a design/planning document, and wants to mine the corpus for ideas that expand their thinking — not to summarize every paper, but to ruthlessly filter to what matters. Handles corpora of 500-2000+ papers via parallel abstract screening followed by selective deep-read of the most promising hits. |
| [`caveman-compress`](./skills/caveman-compress) | Compress natural language memory files (CLAUDE.md, todos, preferences) into caveman format to save input tokens. Preserves all technical substance, code, URLs, and structure. Compressed version overwrites the original file. Human-readable backup saved as FILE.original.md. Trigger: /caveman-compress FILEPATH or "compress memory file" |
| [`caveman`](./skills/caveman) | Ultra-compressed communication mode. Cuts output tokens 65% (measured) by speaking like caveman while keeping full technical accuracy. Supports intensity levels: lite, full (default), ultra, wenyan-lite, wenyan-full, wenyan-ultra. Use when user says "caveman mode", "talk like caveman", "use caveman", "less tokens", "be brief", or invokes /caveman. Also auto-triggers when token efficiency is requested. |
| [`chatgpt-web-imagegen`](./skills/chatgpt-web-imagegen) | Generate images via the chatgpt.com web interface (not the API) by driving your logged-in Chrome session through OpenCLI. Use when you want to create images with ChatGPT image generation but the OpenAI/codex /images/generations API endpoint times out or returns a ~190s cap on long/multi-character prompts, when you don't have an API key but ARE logged into chatgpt.com in a browser, or when prompts get blocked by ChatGPT's third-party-content-similarity moderation and you want automatic rephrase-and-retry. Accepts a single prompt or an array of prompts; not bound to any file format. Each prompt is sent as a fresh chat conversation and the rendered image is scraped from the DOM. |
| [`git-corporate-proxy-lfs`](./skills/git-corporate-proxy-lfs) | Diagnoses and fixes `git clone`/`git pull` failures behind a strict corporate proxy on Windows — the "Failed to connect to github.com:443" timeout, the schannel revocation-check hang (CRYPT_E_NO_REVOCATION_CHECK / 0x80092012), and Git LFS pulling at single-digit KB/s. Use when git over HTTPS stalls or times out on a corporate/VPN network, when regular git works but LFS crawls, when a clone dies mid-checkout leaving files as LFS pointers, or when the proxy injects a 407 Proxy Authentication Required partway through a transfer. Also covers partial (`blob:none`/promisor) clones that can't finish a checkout (`could not fetch ... from promisor remote`) and phantom `git status` deletions caused by the LFS smudge filter. |
| [`harvest-ai-papers`](./skills/harvest-ai-papers) | Use when asked to list, inventory, harvest, preserve, or convert top AI venue paper pages, conference paper pages, proceedings pages, or AI research URLs into Markdown for downstream AI-agent reading, including NeurIPS, ICML, ICLR, AAAI, images, metadata, citations, and AI-readable visual equivalents. |
| [`install-claude-code-windows`](./skills/install-claude-code-windows) | Installs Anthropic's Claude Code CLI and the Claude Code Router (CCR, pinned to v1.x) on Windows 11 behind a strict corporate firewall / VPN, and routes Claude Code to internal OpenAI-compatible model endpoints. Use when setting up Claude Code on a Windows machine where the official install.ps1 fails (proxy returns an HTML block page) or where CCR v2's web UI hangs forever on "loading". Also use when CCR reports "No available models" — usually a BOM-corrupted config.json. |
| [`karpathy-guidelines`](./skills/karpathy-guidelines) | Behavioral guidelines to reduce common LLM coding mistakes. Use when writing, reviewing, or refactoring code to avoid overcomplication, make surgical changes, surface assumptions, and define verifiable success criteria. |
| [`meeting-recording-analysis`](./skills/meeting-recording-analysis) | Analyzes meeting recordings (video + audio) — transcribes speech to a timestamped transcript and extracts key frames from screen-share video, then summarizes / pulls action items / answers questions about the meeting. Built for WeLink recordings (a directory with meeting_1.mp4 + meeting_1.m4a + audio.pcm) but works on any video file. Use when the user wants to know what happened in a recorded meeting, get a summary or action items, extract something shown on the shared screen (slides, code, a diagram), or search what was said by timestamp. Requires the Python venv with openai-whisper + imageio-ffmpeg (see Setup). |
| [`pip-corporate-proxy`](./skills/pip-corporate-proxy) | Installs Python pip packages behind a strict corporate proxy / VPN on Windows when pip hangs forever or fails with 407 Proxy Authentication Required. Use when `pip install` stalls on large wheels (numpy, onnxruntime, torch, av, imageio-ffmpeg, etc.) while small packages install fine, when pip's `--timeout` never fires, when `pip config global.proxy` returns 407 but env-var `HTTPS_PROXY` works, or when you need to install heavy ML wheels (faster-whisper, pytorch, transformers) on a locked-down network. |
| [`verify-model-endpoints`](./skills/verify-model-endpoints) | Smoke-tests any OpenAI-compatible chat model endpoint — DashScope/Bailian plans and regions, DeepSeek, Moonshot/Kimi, Zhipu/GLM, SiliconFlow, OpenRouter, OpenAI, local Ollama — by firing a prompt and printing the reply. Use when you want to confirm a new API key / base URL / model name actually works end-to-end, debug "why does my model call 401/404/hang", or quickly compare a prompt across providers before wiring it into an app. The openai SDK pointed at a custom base_url does the work; .env holds per-provider credentials. |
| [`webpage-to-markdown`](./skills/webpage-to-markdown) | Use when asked to parse, extract, archive, preserve, clean up, or transform a given web page URL into a complete, human-readable and agent-friendly Markdown file for models that may or may not be multimodal, including page metadata, headings, links, tables, code blocks, images, visual fallbacks, and provenance. |


### External collections (git submodules)

Tracked upstream and updated via `git submodule update --remote`. Their skills
are read-only references — don't edit in place.

### Anthropic skills (anthropic-skills/skills/) (17)

| Skill | Description |
|---|---|
| [`algorithmic-art`](./anthropic-skills/skills/algorithmic-art) | Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using code, generative art, algorithmic art, flow fields, or particle systems. Create original algorithmic art rather than copying existing artists' work to avoid copyright violations. |
| [`brand-guidelines`](./anthropic-skills/skills/brand-guidelines) | Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply. |
| [`canvas-design`](./anthropic-skills/skills/canvas-design) | Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to create a poster, piece of art, design, or other static piece. Create original visual designs, never copying existing artists' work to avoid copyright violations. |
| [`claude-api`](./anthropic-skills/skills/claude-api) | Reference for the Claude API / Anthropic SDK — model ids, pricing, params, streaming, tool use, MCP, agents, caching, token counting, model migration. TRIGGER — read BEFORE opening the target file; don't skip because it "looks like a one-liner" — whenever: the prompt names Claude/Anthropic in any form (Claude, Anthropic, Fable, Opus, Sonnet, Haiku, `anthropic`, `@anthropic-ai`, `claude-*`, `us.anthropic.*`, `[1m]`); the user asks about an LLM (pricing/model choice/limits/caching) — never answer from memory; OR the task is LLM-shaped with provider unstated (agent/MCP/tool-definition/multi-agent/RAG/LLM-judge/computer-use; generate/summarize/extract/classify/rewrite/converse over NL; debugging refusals/cutoffs/streaming/tool-calls/tokens). SKIP only when another provider is being worked on (overrides all triggers): OpenAI/GPT/Gemini/Llama/Mistral/Cohere/Ollama named in the query; OR `grep -rE 'openai|langchain_openai|google.generativeai|genai|mistralai|cohere|ollama'` over the project hits (run this grep FIRST if no provider named — don't Read the file). |
| [`doc-coauthoring`](./anthropic-skills/skills/doc-coauthoring) | Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This workflow helps users efficiently transfer context, refine content through iteration, and verify the doc works for readers. Trigger when user mentions writing docs, creating proposals, drafting specs, or similar documentation tasks. |
| [`docx`](./anthropic-skills/skills/docx) | Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files) or Word templates (.dotx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', '.dotx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx or .dotx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation. |
| [`frontend-design`](./anthropic-skills/skills/frontend-design) | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direction, typography, and making choices that don't read as templated defaults. |
| [`internal-comms`](./anthropic-skills/skills/internal-comms) | A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude should use this skill whenever asked to write some sort of internal communications (status reports, leadership updates, 3P updates, company newsletters, FAQs, incident reports, project updates, etc.). |
| [`mcp-builder`](./anthropic-skills/skills/mcp-builder) | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK). |
| [`pdf`](./anthropic-skills/skills/pdf) | Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill. |
| [`pptx`](./anthropic-skills/skills/pptx) | Use this skill any time a .pptx or .potx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx or .potx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates (.potx), layouts, speaker notes, or comments. Trigger whenever the user mentions \"deck,\" \"slides,\" \"presentation,\" or references a .pptx or .potx filename, regardless of what they plan to do with the content afterward. If a .pptx or .potx file needs to be opened, created, or touched, use this skill. |
| [`skill-creator`](./anthropic-skills/skills/skill-creator) | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy. |
| [`slack-gif-creator`](./anthropic-skills/skills/slack-gif-creator) | Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation concepts. Use when users request animated GIFs for Slack like "make me a GIF of X doing Y for Slack. |
| [`theme-factory`](./anthropic-skills/skills/theme-factory) | Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10 pre-set themes with colors/fonts that you can apply to any artifact that has been creating, or can generate a new theme on-the-fly. |
| [`web-artifacts-builder`](./anthropic-skills/skills/web-artifacts-builder) | Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui). Use for complex artifacts requiring state management, routing, or shadcn/ui components - not for simple single-file HTML/JSX artifacts. |
| [`webapp-testing`](./anthropic-skills/skills/webapp-testing) | Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs. |
| [`xlsx`](./anthropic-skills/skills/xlsx) | Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .xltx, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved. |

### Superpowers (superpowers/skills/) (14)

| Skill | Description |
|---|---|
| [`brainstorming`](./superpowers/skills/brainstorming) | You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation. |
| [`dispatching-parallel-agents`](./superpowers/skills/dispatching-parallel-agents) | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies |
| [`executing-plans`](./superpowers/skills/executing-plans) | Use when you have a written implementation plan to execute in a separate session with review checkpoints |
| [`finishing-a-development-branch`](./superpowers/skills/finishing-a-development-branch) | Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup |
| [`receiving-code-review`](./superpowers/skills/receiving-code-review) | Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation |
| [`requesting-code-review`](./superpowers/skills/requesting-code-review) | Use when completing tasks, implementing major features, or before merging to verify work meets requirements |
| [`subagent-driven-development`](./superpowers/skills/subagent-driven-development) | Use when executing implementation plans with independent tasks in the current session |
| [`systematic-debugging`](./superpowers/skills/systematic-debugging) | Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes |
| [`test-driven-development`](./superpowers/skills/test-driven-development) | Use when implementing any feature or bugfix, before writing implementation code |
| [`using-git-worktrees`](./superpowers/skills/using-git-worktrees) | Use when starting feature work that needs isolation from current workspace or before executing implementation plans - ensures an isolated workspace exists via native tools or git worktree fallback |
| [`using-superpowers`](./superpowers/skills/using-superpowers) | Use when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response including clarifying questions |
| [`verification-before-completion`](./superpowers/skills/verification-before-completion) | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always |
| [`writing-plans`](./superpowers/skills/writing-plans) | Use when you have a spec or requirements for a multi-step task, before touching code |
| [`writing-skills`](./superpowers/skills/writing-skills) | Use when creating new skills, editing existing skills, or verifying skills work before deployment |

### Mattpocock skills (mattpocock-skills/skills/) (41)

| Skill | Category | Description |
|---|---|---|
| [`design-an-interface`](./mattpocock-skills/skills/deprecated/design-an-interface) | ⚠️ deprecated | Generate multiple radically different interface designs for a module using parallel sub-agents. Use when user wants to design an API, explore interface options, compare module shapes, or mentions "design it twice". |
| [`qa`](./mattpocock-skills/skills/deprecated/qa) | ⚠️ deprecated | Interactive QA session where user reports bugs or issues conversationally, and the agent files GitHub issues. Explores the codebase in the background for context and domain language. Use when user wants to report bugs, do QA, file issues conversationally, or mentions "QA session". |
| [`request-refactor-plan`](./mattpocock-skills/skills/deprecated/request-refactor-plan) | ⚠️ deprecated | Create a detailed refactor plan with tiny commits via user interview, then file it as a GitHub issue. Use when user wants to plan a refactor, create a refactoring RFC, or break a refactor into safe incremental steps. |
| [`ubiquitous-language`](./mattpocock-skills/skills/deprecated/ubiquitous-language) | ⚠️ deprecated | Extract a DDD-style ubiquitous language glossary from the current conversation, flagging ambiguities and proposing canonical terms. Saves to UBIQUITOUS_LANGUAGE.md. Use when user wants to define domain terms, build a glossary, harden terminology, create a ubiquitous language, or mentions "domain model" or "DDD". |
| [`ask-matt`](./mattpocock-skills/skills/engineering/ask-matt) | engineering | Ask which skill or flow fits your situation. A router over the skills in this repo. |
| [`code-review`](./mattpocock-skills/skills/engineering/code-review) | engineering | Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes — Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/PRD asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X". |
| [`codebase-design`](./mattpocock-skills/skills/engineering/codebase-design) | engineering | Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary. |
| [`diagnosing-bugs`](./mattpocock-skills/skills/engineering/diagnosing-bugs) | engineering | Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow. |
| [`domain-modeling`](./mattpocock-skills/skills/engineering/domain-modeling) | engineering | Build and sharpen a project's domain model. Use when the user wants to pin down domain terminology or a ubiquitous language, record an architectural decision, or when another skill needs to maintain the domain model. |
| [`grill-with-docs`](./mattpocock-skills/skills/engineering/grill-with-docs) | engineering | A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go. |
| [`implement`](./mattpocock-skills/skills/engineering/implement) | engineering | Implement a piece of work based on a spec or set of tickets. |
| [`improve-codebase-architecture`](./mattpocock-skills/skills/engineering/improve-codebase-architecture) | engineering | Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick. |
| [`prototype`](./mattpocock-skills/skills/engineering/prototype) | engineering | Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like. |
| [`research`](./mattpocock-skills/skills/engineering/research) | engineering | Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent. |
| [`resolving-merge-conflicts`](./mattpocock-skills/skills/engineering/resolving-merge-conflicts) | engineering | Use when you need to resolve an in-progress git merge/rebase conflict. |
| [`setup-matt-pocock-skills`](./mattpocock-skills/skills/engineering/setup-matt-pocock-skills) | engineering | Configure this repo for the engineering skills — set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before first use of the other engineering skills. |
| [`tdd`](./mattpocock-skills/skills/engineering/tdd) | engineering | Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests. |
| [`to-spec`](./mattpocock-skills/skills/engineering/to-spec) | engineering | Turn the current conversation into a spec and publish it to the project issue tracker — no interview, just synthesis of what you've already discussed. |
| [`to-tickets`](./mattpocock-skills/skills/engineering/to-tickets) | engineering | Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker — edges as text in one file per ticket locally, or native blocking links on a real tracker. |
| [`triage`](./mattpocock-skills/skills/engineering/triage) | engineering | Move issues and external PRs through a state machine of triage roles — categorise, verify, grill if needed, and write agent-ready briefs. |
| [`wayfinder`](./mattpocock-skills/skills/engineering/wayfinder) | engineering | Plan a huge chunk of work — more than one agent session can hold — as a shared map of decision tickets on your issue tracker, and resolve them one at a time until the way to the destination is clear. |
| [`batch-grill-me`](./mattpocock-skills/skills/in-progress/batch-grill-me) | 🚧 in-progress | A relentless interview that asks every frontier question at once, round by round. |
| [`claude-handoff`](./mattpocock-skills/skills/in-progress/claude-handoff) | 🚧 in-progress | Hand the current conversation off to a fresh background agent that picks up the work immediately. |
| [`loop-me`](./mattpocock-skills/skills/in-progress/loop-me) | 🚧 in-progress | Grill me about specs for the workflows I want to build, within this workspace. |
| [`setup-ts-deep-modules`](./mattpocock-skills/skills/in-progress/setup-ts-deep-modules) | 🚧 in-progress | Wire dependency-cruiser into a TypeScript repo so each package is a deep module — implementation hidden in subfolders, reachable only through its entry-point files. User-invoked. |
| [`to-questionnaire`](./mattpocock-skills/skills/in-progress/to-questionnaire) | 🚧 in-progress | Turn a decision you can't fully answer into a questionnaire for someone else to fill in. |
| [`wizard`](./mattpocock-skills/skills/in-progress/wizard) | 🚧 in-progress | Generate an interactive bash wizard that walks a human through a manual procedure — third-party setup, a one-off migration, an A→B state transition — opening URLs, capturing values, confirming each step, and writing .env files and GitHub Actions secrets. |
| [`writing-beats`](./mattpocock-skills/skills/in-progress/writing-beats) | 🚧 in-progress | Writing, exploit — assemble raw material into a journey of beats, grounding each term before a beat leans on it. |
| [`writing-fragments`](./mattpocock-skills/skills/in-progress/writing-fragments) | 🚧 in-progress | Writing, explore — mine raw fragments, no structure yet. |
| [`writing-shape`](./mattpocock-skills/skills/in-progress/writing-shape) | 🚧 in-progress | Writing, exploit — shape raw material into an article, paragraph by paragraph. |
| [`git-guardrails-claude-code`](./mattpocock-skills/skills/misc/git-guardrails-claude-code) | misc | Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destructive git operations, add git safety hooks, or block git push/reset in Claude Code. |
| [`migrate-to-shoehorn`](./mattpocock-skills/skills/misc/migrate-to-shoehorn) | misc | Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn, wants to replace `as` in tests, or needs partial test data. |
| [`scaffold-exercises`](./mattpocock-skills/skills/misc/scaffold-exercises) | misc | Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use when user wants to scaffold exercises, create exercise stubs, or set up a new course section. |
| [`setup-pre-commit`](./mattpocock-skills/skills/misc/setup-pre-commit) | misc | Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when user wants to add pre-commit hooks, set up Husky, configure lint-staged, or add commit-time formatting/typechecking/testing. |
| [`edit-article`](./mattpocock-skills/skills/personal/edit-article) | personal | Edit and improve articles by restructuring sections, improving clarity, and tightening prose. Use when user wants to edit, revise, or improve an article draft. |
| [`obsidian-vault`](./mattpocock-skills/skills/personal/obsidian-vault) | personal | Search, create, and manage notes in the Obsidian vault with wikilinks and index notes. Use when user wants to find, create, or organize notes in Obsidian. |
| [`grill-me`](./mattpocock-skills/skills/productivity/grill-me) | productivity | A relentless interview to sharpen a plan or design. |
| [`grilling`](./mattpocock-skills/skills/productivity/grilling) | productivity | Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases. |
| [`handoff`](./mattpocock-skills/skills/productivity/handoff) | productivity | Compact the current conversation into a handoff document for another agent to pick up. |
| [`teach`](./mattpocock-skills/skills/productivity/teach) | productivity | Teach the user a new skill or concept, within this workspace. |
| [`writing-great-skills`](./mattpocock-skills/skills/productivity/writing-great-skills) | productivity | Reference for writing and editing skills well — the vocabulary and principles that make a skill predictable. |


## OpenCLI plugins

Each plugin's `opencli-plugin.json` `commands` array declares the command
surface (args + output columns) — that manifest is the catalog source of
truth. Full recon notes and setup live in each plugin's `README.md`.

### Plugins (2)

| Plugin | Commands |
|---|---|
| [`huawei-jiaxian`](./opencli-plugins/huawei-jiaxian/README.md) | **`search`** <query> · --limit <int> · --language<br>columns: `rank, title, type, author, date, views, replies, summary, post_id, resource_type, url`<br><br>**`read`** <post_id> · --type<br>columns: `title, author, author_id, dept, date, views, likes, replies, body, url` |
| [`huawei-terminology`](./opencli-plugins/huawei-terminology/README.md) | **`search`** <query> · --limit <int> · --language · --filter-language<br>columns: `rank, term_en, term_cn, domain, confidence, definition, url` |


## Using a picked skill

Activate manually. For Claude Code, symlink (or copy) the skill folder into
your personal skills dir:

```bash
# Windows (Git Bash)
ln -s "$(pwd)/<path-from-catalog>/<skill-name>" "$HOME/.claude/skills/<skill-name>"
```

For the submodules, use the full path from the table, e.g.
`./anthropic-skills/skills/pdf` or `./mattpocock-skills/skills/engineering/tdd`.

For other agents, follow their skill-discovery convention, or just open the
skill's `SKILL.md` and follow the steps directly — every skill is self-contained.

## Using a picked plugin

Install once (see `opencli-plugins/README.md`), then call as a CLI command:

```bash
opencli <plugin> <command> [args]        # e.g. opencli huawei-jiaxian search "盘古" --limit 3
```
