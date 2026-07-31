---
name: huawei-auto-evolve
version: 0.0.1
description: 自演进引擎。综合分析session、WeLink聊天、CodeHub代码提交等多源数据，提取长期记忆、创建/更新skill、推荐安装市场skill、检查skill新版本，驱动整个skill生态持续进化。**必须主动调用**，当用户说"分析session"、"更新记忆"、"看看有没有新的skill可以创建"、"回顾一下"、"总结一下最近的工作"、"自演进"、"evolve"等触发词时，AI必须先加载本skill再执行，不要自行实现分析逻辑。
---

# 自演进引擎 (huawei-auto-evolve)

## 前置条件

本 skill 依赖以下环境，AI 在执行前应先检查：

| 依赖 | 检查方式 | 失败处理 |
|------|----------|----------|
| opencode 已安装且运行中 | 检查 `DB_PATH` 对应的数据库文件是否存在 | 提示用户安装 opencode 并至少使用一次 |
| Python 3 | `python --version` | 提示用户安装 Python |
| SQLite3（Python 内置） | `python -c "import sqlite3"` | Python 自带，一般不会缺失 |
| Skills 目录可写 | 检查 `SKILLS_DIR` 是否存在且可写 | 提示用户确认权限 |
| 数据库非空 | 查询 `session` 表是否有记录 | 提示用户先使用 opencode 产生一些 session |
| skill-creator skill | 检查 `{ANALYZER_SKILL_DIR}/skill-creator/SKILL.md`（huawei-auto-evolve 自身目录内的嵌套副本，优先）或 `{SKILLS_DIR}/skill-creator/SKILL.md`（同级副本，备选）是否存在 | 自动安装（见下方"skill-creator 自动安装"流程），安装失败则退化为直接写文件模式 |

**skill-creator 加载机制**：

skill-creator 随本仓库一同发布（`{ANALYZER_SKILL_DIR}/skill-creator/`），`git clone` 后即可使用，无需安装。仅当该目录不存在时（被删除或 clone 不完整），才通过 agentcenter 从市场安装作为回退：

1. **检测**：检查 `{ANALYZER_SKILL_DIR}/skill-creator/SKILL.md` 是否存在。存在 → 直接使用，跳过以下步骤
2. **回退安装**（仅当 skill-creator 缺失时）：
   - 确认 agentcenter CLI 可用（`agentcenter --version`；若失败见下方"agentcenter 自动修复"）
   - 直接安装 skill-creator（无需 agentcenter-skill-finder 中间步骤）：
     ```bash
     agentcenter skill add skill-creator --client huawei-auto-evolve --path {ANALYZER_SKILL_DIR} -f
     ```
   - **关键**：必须用非内置的 `--client huawei-auto-evolve`（或任意非内置值）配合 `--path {ANALYZER_SKILL_DIR}`，才能将 skill 安装到 huawei-auto-evolve 目录内。若用内置 client（`claudecode`/`opencode`/`cac` 等），`--path` 被忽略，skill 落到全局目录
3. **验证**：再次检查 `{ANALYZER_SKILL_DIR}/skill-creator/SKILL.md` 是否存在
4. **降级**：如果 agentcenter 不可用或安装失败，退化为直接写文件模式（创建目录 + 写 SKILL.md），并在报告中提示用户可手动安装 skill-creator 获得更高质量的 skill 创建

**agentcenter 自动修复**：agentcenter 是必备依赖（Task 8/9 需要）。若 `agentcenter --version` 失败（`command not found` 或 `Cannot find module .../src/bin/index.js`——后者常见于 node_modules 被清理后 shim 存在但包丢失），**自动执行重装，不要提示用户、不要跳过**：
```bash
NO_PROXY=cmc.centralrepo.rnd.huawei.com npm install -g @aimarket/agentcenter --@aimarket:registry=https://cmc.centralrepo.rnd.huawei.com/artifactory/api/npm/product_npm/ --strict-ssl=false
```
重装后再次 `agentcenter --version` 验证。三个关键细节：必须用 `product_npm` registry（不是 `npm-all`，那个会 401）；必须设 `NO_PROXY=cmc.centralrepo.rnd.huawei.com`（内网直连，绕过公司代理）；必须 `--strict-ssl=false`（公司代理做 TLS 拦截）。若 npm 报 `407 Proxy Authentication Required`，安装前清除代理环境变量（`HTTP_PROXY=""`/`HTTPS_PROXY=""`）。`agentcenter` 是 npm 全局 bin，默认安装到 `%APPDATA%\npm`，若 `command not found` 将该目录加入 PATH。自动修复是首选行为，不是"可选优化"

**空环境首次运行引导**：如果用户是在全新环境（没有 `huawei-auto-evolve-created-global-memory`、没有任何 `huawei-auto-evolve-created-` skill）下首次运行，分析器应自动完成以下初始化，确保开箱即用：
1. 创建 `SKILLS_DIR` 目录（如不存在）
2. 创建 `huawei-auto-evolve-created-global-memory` skill（见步骤5"首次创建"流程）
3. 询问用户身份信息（姓名、工号/账号），用于初始化记忆和外部数据源采集
4. 依次检测可选外部数据源（W3、CloudDevOps Wiki、WeLink），可用的自动采集
5. 分析所有历史 session，提取记忆和创建 skill
6. 完成后输出初始化报告，告知用户哪些数据源可用、哪些跳过

**可选依赖**（影响外部数据源采集，不可用时跳过，不影响核心分析功能）：

| 可选依赖 | 用途 | 检测方式 | 缺失影响 |
|----------|------|----------|----------|
| welink-cli | 分析时间段内的聊天记录 | 检查 PATH 中是否有 `welink-cli`，`welink-cli auth status` 是否已登录 | 若未安装，**自动安装** `npm install -g @welink/welink-cli`；若 token 过期，**自动刷新** `welink-cli auth login`；均失败才跳过 |
| W3 搜索 MCP 工具 | 搜索用户公开信息 | 尝试调用 W3 搜索 MCP 工具或 API | 跳过 W3 数据源 |
| CloudDevOps Wiki MCP | 获取用户 Wiki | `wiki-mcp.py`（自包含，读操作无需认证） | 跳过 Wiki 数据源 |
| git (CodeHub/GitHub) | 获取代码提交记录 | `git --version`；可选 CodeHub MCP（`codehub.py --list-tools`）或 GitHub MCP（`github_mcp.py --list-tools`），按仓库 remote 归属选择 | 跳过 MCP 协作层数据（本地 git 仍可用） |
| agentcenter CLI | 推荐安装 skill、检查 skill 新版本 | `agentcenter --version`；若报 module not found（shim 存在但包丢失），**自动重装**（见下方"agentcenter 自动修复"） | **阻塞**：agentcenter 是必备依赖，不可跳过。自动修复失败才提示用户 |

## 核心功能

分析从上次运行到现在的所有新 session，**同时采集外部数据源（WeLink聊天、CodeHub代码提交、W3搜索等）**，综合全量信息执行五个任务：
1. **更新长期记忆**：提取值得长期记住的信息，更新到记忆 skill（见下方配置）
2. **创建新 skill**：发现重复性模式，创建 `huawei-auto-evolve-created-` 前缀的新 skill
3. **更新已有 skill**：检查所有 `huawei-auto-evolve-created-` 开头的 skill，根据新发现的经验更新
4. **推荐并安装 skill**：根据分析结果，在 agentcenter 市场中搜索可能对用户有用的 skill 并安装
5. **检查 skill 新版本**：检查用户已安装的所有 skill 是否有新版本，有则更新

## 配置

以下路径在首次运行时自动检测，后续复用：

| 配置项 | 说明 | 检测方式 |
|--------|------|----------|
| `SKILLS_DIR` | Skills 安装目录 | 见下方"SKILLS_DIR 路径映射" |
| `DB_PATH` | Session 数据库路径 | `~/.local/share/opencode/db/ngagent.db`（Linux/Mac）或 `%USERPROFILE%\.local\share\opencode\db\ngagent.db`（Windows） |
| `MEMORY_SKILL_NAME` | 存储长期记忆的 skill 名称 | 默认 `huawei-auto-evolve-created-global-memory`，如不存在则首次运行时自动创建 |
| `ANALYZER_SKILL_DIR` | 本 skill 所在目录 | 在 `SKILLS_DIR` 下查找 `huawei-auto-evolve` 子目录；如 AI 无法自动定位，可通过 `glob` 搜索 `**/huawei-auto-evolve/SKILL.md` 找到 |

**SKILLS_DIR 路径映射**（不同 AI 客户端的 skills 目录不同，必须根据当前环境自动识别）：

| 客户端 | SKILLS_DIR 路径 | 识别特征 |
|--------|----------------|----------|
| opencode | `~/.config/opencode/skills`（Linux/Mac）或 `%USERPROFILE%\.config\opencode\skills`（Windows） | 路径含 `.config/opencode` |
| cac | `~/.cac/skills`（Linux/Mac）或 `%USERPROFILE%\.cac\skills`（Windows） | 路径含 `.cac` |
| codeAgent | `~/.config/codeagent/skills`（Linux/Mac）或 `%USERPROFILE%\.config\codeagent\skills`（Windows） | 路径含 `.config/codeagent` |
| claudecode | `~/.claude/skills`（Linux/Mac）或 `%USERPROFILE%\.claude\skills`（Windows） | 路径含 `.claude` |

识别方式：优先检查本 SKILL.md 文件的实际路径（即 `huawei-auto-evolve/SKILL.md` 所在目录的父目录），这是最准确的判断依据。如果无法获取自身路径，按上表依次检查哪个目录存在。

**路径检测示例**（Python）：
```python
import os, platform

home = os.path.expanduser("~")
is_windows = platform.system() == "Windows"

# 优先通过本文件路径推断 SKILLS_DIR
this_dir = os.path.dirname(os.path.abspath(__file__))
SKILLS_DIR = os.path.dirname(this_dir)  # huawei-auto-evolve 的父目录

# 如果无法获取自身路径，按优先级检查
if not os.path.isdir(SKILLS_DIR):
    candidates = [
        os.path.join(home, ".config", "opencode", "skills"),
        os.path.join(home, ".cac", "skills"),
        os.path.join(home, ".config", "codeagent", "skills"),
        os.path.join(home, ".claude", "skills"),
    ]
    for d in candidates:
        if os.path.isdir(d):
            SKILLS_DIR = d
            break

DB_PATH = os.path.join(home, ".local", "share", "opencode", "db", "ngagent.db")
MEMORY_SKILL_NAME = "huawei-auto-evolve-created-global-memory"
```

## 外部数据源（每次分析时采集）

**重要变更**：外部数据源不再仅限于首次创建记忆时采集，而是**每次分析时都尝试采集增量数据**，与 session 数据综合分析。这使分析器能发现 session 中未体现的工作内容（如会议讨论、代码提交、文档撰写等）。

每个数据源都是可选的，检测到可用则使用，不可用则跳过。

### 数据源 1：WeLink 聊天记录

**用途**：获取分析时间段内的工作沟通记录，发现会议决策、项目进展、待办跟进等 session 中可能未体现的信息

**检测方式**：检查 `welink-cli` 是否在 PATH 中可执行，`welink-cli auth status` 是否已登录。若 welink-cli 不在 PATH 中，**自动安装**：`npm install -g @welink/welink-cli`。若 token 已过期（状态显示 EXPIRED），**自动执行 `welink-cli auth login` 刷新 token**（该命令连接 WeLink PC 客户端非交互刷新，无需用户操作），刷新后重新检测。自动安装或自动刷新均失败才跳过 WeLink 数据源并在报告中说明

**采集方式**：
```bash
# 获取会话列表
welink-cli im query-recent-conversation --count 50

# 读取各会话消息（按分析时间段筛选）
welink-cli im query-history-message --group-id <ID> --query-count 50
welink-cli im query-history-message --user-account <ACCOUNT> --query-count 50
```
- 优先读取：与领导的私聊、核心管理群、项目群、ST群
- 按优先级分批串行读取，每次最多3个会话，读取后立即摘要关键信息
- **禁止并行超过3个 welink-cli 消息查询**，否则消息总量会超出上下文处理能力
- 分析维度：
  - 核心事项：决策、争议、重要进展
  - 会议和讨论：会议主题 + 结论
  - 待办和跟进：待办项 + 责任人 + 截止时间
  - 风险与阻碍：影响 + 需要的支持
- 注意：welink-cli 可能需配置 NO_PROXY（`open.inner.welink.huawei.com` 和 `cmc.centralrepo.rnd.huawei.com`）

### 数据源 2：CodeHub 代码提交

**用途**：获取分析时间段内的代码提交记录，了解实际开发工作

**检测方式**：`git --version`（本地提交）；可选 CodeHub MCP 工具（远程 MR/检视/Issue）

**采集方式**：

**A. 本地 git 提交记录**（基础，始终可用）：
```bash
# 查看分析时间段内的代码提交
git log --author="<工号或姓名>" --since="<开始日期>" --until="<结束日期>" --all --format="%h %ai %s" --no-merges

# 查看关键提交详情
git show <hash> --stat
```
- 提取：提交次数、MR 数量、代码行数变更、关键提交概要
- 与 session 中的开发记录交叉验证，补充 session 未记录的代码工作

**B. CodeHub MCP 工具**（可选，补充本地 git 看不到的协作层数据）：

> CodeHub MCP 服务器是 MR/Issue 中心，**不是**提交中心——它不能按作者枚举原始提交历史，但能获取本地 git 看不到的 MR 生命周期、检视意见、Issue 数据。与本地 git 互补。

**检测方式**：优先使用本仓库自包含的 CodeHub 工具（`{ANALYZER_SKILL_DIR}/../../mcp-tools/huawei-codehub/codehub.py`）；或检查 opencode 的 MCP 配置（`~/.config/opencode/opencode.json` 的 `mcp.Codehub-Mcp-Server`）是否 `enabled: true`；或直接尝试调用 CodeHub MCP 工具

**前置条件**（本地 stdio 服务器，非免安装）：需 `uvx`（uv）在 PATH 上、能访问华为内网制品库、且设置 `PRIVATE_TOKEN` 环境变量（从 CodeHub → Settings → Access Tokens 获取）。无 token 时脚本会友好报错退出。

**uvx 自动发现**：Git Bash 的 `which`/`command -v` 可能找不到 uvx（常见于 uv 安装在非标准路径如 `D:/CodingAgentCLI/uv/uvx.exe`）。检测逻辑：`command -v uvx || ls /d/CodingAgentCLI/uv/uvx.exe || ls "$LOCALAPPDATA/uv/uvx.exe"`。若找到 uvx 但不在 PATH 上，通过 `CODEHUB_UVX_ARGS` 环境变量传入完整 uvx 路径（JSON 数组，替换默认的 `"uvx"` 命令），参见 `mcp-tools/huawei-codehub/README.md` 的 Troubleshooting

**凭据管理**：token 存于 `{ANALYZER_SKILL_DIR}/.env`（已 gitignore，参见 `.env.example` 模板）。调用 codehub 工具前先加载：
```bash
set -a; source "{ANALYZER_SKILL_DIR}/.env"; set +a
```
该 `.env` 含 `PRIVATE_TOKEN` 和 `WEB_HOST`（默认 `https://codehub-g.huawei.com/`，直接可达；`codehub-y.huawei.com` 在部分网络段不可达）。加载后 `codehub.py` 会从环境读取。Windows 上 uvx 受 TLS 拦截影响需 `--allow-insecure-host`（已在默认参数中，参见 `mcp-tools/huawei-codehub/README.md` 的 Troubleshooting）

- **首选：调用自包含脚本**（任何有 Bash + Python 3 的环境都能用，无需 MCP 支持）：
  ```bash
  export PRIVATE_TOKEN=<your-token>
  # 1. git_url → project_id（其他工具的入参）
  python3 mcp-tools/huawei-codehub/codehub.py get-project-info --git-url <仓库git地址>
  # 2. 列举该项目的合并请求（按状态）
  python3 mcp-tools/huawei-codehub/codehub.py list-merge-requests --project-id <ID> --state all
  # 3. 获取某 MR 的检视意见 —— 反复出现的检视意见=反复犯的错误，强信号
  python3 mcp-tools/huawei-codehub/codehub.py get-merge-request-reviews --project-id <ID> --mr-iid <IID> --json
  # 4. 获取某 MR 的变更内容（filters=commits 可返回该 MR 内的提交）
  python3 mcp-tools/huawei-codehub/codehub.py get-merge-request-changes --project-id <ID> --mr-iid <IID> --filters commits
  ```
  工具名用 kebab-case（如 `list-merge-requests`），脚本自动映射为服务器的 snake_case 名。参数以 `--key value` 传入，脚本自动转换 int/bool，服务器校验完整 schema。`--list-tools` 可列出全部 17 个工具
- **备选：调用 MCP 工具**（服务器 `Codehub-Mcp-Server`，需将 `mcp-tools/huawei-codehub/opencode.mcp.json` 或 `claude-code.mcp.json` 载入 harness，并填入真实 `PRIVATE_TOKEN`）。此时须在启动 agent 的 shell 设置 `NO_PROXY=cmc.centralrepo.rnd.huawei.com,mirrors.tools.huawei.com,codehub-y.huawei.com`
- **提取**：MR 标题/状态/分支、**检视意见（review comments）**、Issue 标题/状态/讨论
- **重点**：反复出现的检视意见揭示反复犯的错误；MR 的门禁状态（`get-merge-request-mergeable-state`）反映代码质量阻塞点；这些是 session 中通常不会记录的协作信号

**C. GitHub MCP 工具**（可选，补充 GitHub 托管仓库的协作层数据）：

> 与 CodeHub MCP 对称——CodeHub MCP 覆盖华为内部 Git 仓库，GitHub MCP 覆盖 GitHub 托管仓库。如果用户的仓库在 GitHub（如本 misc 仓库），用 GitHub MCP 获取 PR、review、issue 数据。

**检测方式**：优先使用本仓库自包含的 GitHub 工具（`{ANALYZER_SKILL_DIR}/../../mcp-tools/github/github_mcp.py`）；或检查 opencode 的 MCP 配置（`~/.config/opencode/opencode.json` 的 `mcp.github_mcp`）是否 `enabled: true`

**前置条件**：需设置 `GITHUB_MCP_PAT` 环境变量（GitHub Personal Access Token，从 github.com/settings/tokens 获取，repo scope）。该工具是**外部主机**——与内网工具不同，它必须**通过**公司代理（`proxyuk.huawei.com:8080`），wrapper 自动处理（`ProxyHandler` + `ssl.CERT_NONE` 应对 TLS 拦截）

**凭据管理**：PAT 存于 `{ANALYZER_SKILL_DIR}/.env`（与 `PRIVATE_TOKEN` 同文件），加载方式相同：
```bash
set -a; source "{ANALYZER_SKILL_DIR}/.env"; set +a
```

- **首选：调用自包含脚本**（任何有 Bash + Python 3 的环境都能用）：
  ```bash
  export GITHUB_MCP_PAT=<your-github-pat>
  # 1. 列举仓库提交
  python3 mcp-tools/github/github_mcp.py list-commits --owner <owner> --repo <repo> --json
  # 2. 列举 PR（按状态）
  python3 mcp-tools/github/github_mcp.py list-pull-requests --owner <owner> --repo <repo> --state all
  # 3. 获取某 PR 的检视意见 —— 与 CodeHub MR 检视意见同等价值
  python3 mcp-tools/github/github_mcp.py get-pull-request-reviews --owner <owner> --repo <repo> --pull-request-number <N> --json
  # 4. 获取 PR 变更文件
  python3 mcp-tools/github/github_mcp.py get-pull-request-files --owner <owner> --repo <repo> --pull-request-number <N>
  ```
  工具名用 kebab-case，脚本自动映射为服务器的 snake_case 名。`--list-tools` 可列出全部工具
- **备选：调用 MCP 工具**（需将 `mcp-tools/github/claude-code.mcp.json` 或 `opencode.mcp.json` 载入 harness，并填入真实 `Authorization: Bearer <PAT>` 头）。此时须在启动 agent 的 shell 设置 `HTTPS_PROXY=http://proxyuk.huawei.com:8080`（外部主机走代理）
- **提取**：PR 标题/状态/分支、**检视意见（reviews）**、Issue、CI/CD workflow runs
- **判断仓库归属**：从 session 的 `directory` 字段或 git remote 判断仓库在 CodeHub 还是 GitHub——`git remote -v` 含 `codehub-*` → 用 CodeHub MCP；含 `github.com` → 用 GitHub MCP

### 数据源 3：W3 搜索

**用途**：搜索用户在华为内网上的公开信息（技术文章、项目经历、荣誉等）

**检测方式**：优先使用本仓库自包含的 W3 搜索工具（`{ANALYZER_SKILL_DIR}/../../mcp-tools/huawei-w3-search/w3_search.py`），该脚本纯标准库实现、无需安装；或检查 opencode 的 MCP 配置（`~/.config/opencode/opencode.json` 的 `mcp.w3_search_tool`）是否 `enabled: true`，或直接尝试调用 `w3_web_search_tool` MCP 工具

**采集方式**：
- **首选：调用自包含脚本**（任何有 Bash + Python 3 的环境都能用，无需 MCP 支持）：
  ```bash
  python3 mcp-tools/huawei-w3-search/w3_search.py "<用户姓名 + 工号>" --size 10 --json
  ```
  脚本自动绕过公司代理（内置 no-proxy opener），无需手动设置 `NO_PROXY`
- **备选：调用远程 MCP 工具** `w3_web_search_tool`（服务器 `server-w3_search_tool`，无需认证，仅需 `User-Agent: OpenCode-MCP-Client/1.0` 和 `Accept: application/json` 头）。此时必须设置 `NO_PROXY=remote-mcp.rnd.huawei.com` 绕过公司代理
- 工具参数（全部必填）：`query`（搜索词）、`page_index`（页码，从 `"1"` 开始）、`page_size`（每页条数，如 `"10"`）、`engine`（查询引擎，默认 `"huawei"`）
- 用用户姓名 + 工号作为关键词搜索
- 提取：技术领域、项目经历、获奖信息、公开文章
- 过滤：只保留与工作相关的信息，排除个人隐私
- 返回结果为 JSON，含 `title`/`source`/`url`/`texts`/`publish_time`，来源多为 `hw3ms_doclib`（3MS 文档库）

### 数据源 4：CloudDevOps Wiki

**用途**：获取用户撰写的 Wiki 文档，了解其专业领域和工作重点

**检测方式**：使用本仓库自包含的 Wiki MCP 工具（`{ANALYZER_SKILL_DIR}/../../mcp-tools/huawei-wiki/wiki_mcp.py`，纯标准库、无需安装、读操作无需认证）

**采集方式**：
- **首选：调用 wiki-mcp 自包含脚本**（任何有 Bash + Python 3 的环境都能用）：
  ```bash
  # 搜索某知识库内的 Wiki（读操作无需 token）
  python3 mcp-tools/huawei-wiki/wiki_mcp.py search-wiki-documents --url <wiki-url> --search-range knowledge --search-key "<用户姓名>" --json
  # 获取文档内容
  python3 mcp-tools/huawei-wiki/wiki_mcp.py fetch-wiki-content --url <wiki-url> --json
  # 列出某类目下的文档
  python3 mcp-tools/huawei-wiki/wiki_mcp.py list-wiki-documents --url <wiki-url> --query-range category --query-type all
  ```
  用户级查询（如 list-my-initiated-wiki-countersigns）和写操作需 `WIKI_X_AUTH_TOKEN` 环境变量
- 按作者搜索用户撰写的所有 Wiki
- 统计各域的文档数量，识别核心关注领域
- 抽样阅读高星/高引用文档，提取专业观点和方法论
- 注意：API 中用户账号可能与工号格式不同（如工号带字母前缀，账号需去掉前缀），具体规则需根据实际系统确认

### 数据源 5：AI 辅助研发 Token 消耗（可选）

**用途**：了解分析时间段内的 AI 辅助研发使用情况

**检测方式**：`nga.cmd` 是否可用。注意：Git Bash 的 `which`/`command -v` 不识别 `.cmd` 扩展名，需用 `command -v nga.cmd || ls /d/CodingAgentCLI/nga.cmd` 检测；常见位置 `D:/CodingAgentCLI/nga.cmd`（已加入 bash PATH）

**采集方式**：
```bash
nga.cmd session list --disable-update
nga.cmd metrics <session_id> --disable-update
```
- `--disable-update` 抑制版本检查噪声
- 汇总 input/output token、运行时长
- 若 `session list` 返回空（nga TUI 与 opencode session DB 是独立存储），回退到直接查询 `DB_PATH` 数据库（数据源 1）中的 metrics 表

### 采集策略

- **每次分析时**：依次检测所有数据源，可用的全部采集增量数据，与 session 数据综合分析
- **首次创建记忆 skill 时**：全量采集所有历史数据
- **后续运行时**：仅采集上次分析时间之后的增量数据
- **采集失败时**：跳过该数据源，不影响其他数据源和主流程，在报告中说明哪些数据源跳过及原因

## 数据源

数据库结构（ngagent.db）：
- `session` 表：id(TEXT PK), title(TEXT), time_created(INTEGER), time_updated(INTEGER), directory(TEXT), ...
- `message` 表：id(TEXT PK), session_id(TEXT FK), time_created(INTEGER), time_updated(INTEGER), data(TEXT, 含 role 字段)
- `part` 表：id(TEXT PK), message_id(TEXT FK), session_id(TEXT FK), time_created(INTEGER), time_updated(INTEGER), data(TEXT, 含 type 和具体内容)

**关键字段说明**：
- `time_created`：记录创建时间（毫秒时间戳），用于增量分析
- `time_updated`：记录更新时间，可用于判断 session 是否有变更
- `session.time_updated`：session 最后更新时间，快速筛选可能有增量消息的 session
- `message.data`：JSON 格式，含 `role` 字段（`user` / `assistant`）
- `part.data`：JSON 格式，含 `type` 字段

part.data 的 type 类型：
- `text`：文本内容，字段 `text`
- `tool`：工具调用，字段 `tool`（工具名）、`state.input`（参数）
- `tool-result`：工具结果
- `reasoning`：推理过程，字段 `text`
- `step-start`：步骤开始

## 流程

### 1. 确定分析范围

读取上次分析时间戳，确定本次分析的时间范围。

时间戳存储位置：`{ANALYZER_SKILL_DIR}/last_analysis.txt`

- 如果文件不存在，说明是**首次运行**，分析所有 session
- 如果文件存在，确定分析范围时**必须同时检查两个维度**：
  1. **新 session**：`session.time_created > 上次时间戳` 的 session
  2. **旧 session 的增量消息**：`session.time_created <= 上次时间戳` 但 `message.time_created > 上次时间戳` 的 session（即 session 创建早于上次分析，但后续有新消息）

**关键**：不能只看 `session.time_created`，否则会遗漏旧 session 在上次分析后新增的消息。必须同时查询 `message` 表和 `part` 表中 `time_created > 上次时间戳` 的记录，通过 `session_id` 关联找到有增量更新的旧 session。

排除当前 session 的增量统计（不计入"分析了N个新session"），但**必须从当前 session 中提取用户反馈**（见步骤4的"当前session反馈提取"规则）。当前 session 包含最鲜活的用户反馈，完全排除会丢失最重要的skill改进信号。

**首次运行特殊处理**：
- 首次运行时数据量可能很大，需分批处理：每次最多分析 20 个 session，处理完后如果还有剩余，记录时间戳并告知用户"还有 N 个 session 未分析，请再次运行"
- 首次运行需要收集用户身份信息（见步骤3的"用户身份获取"）

### 2. 导出 session 内容

用 Python 脚本从数据库导出 session 内容到临时目录：

```python
import sqlite3, json, os

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# 1. 找到所有新 session
c.execute("SELECT id, title, time_created FROM session WHERE time_created > ? ORDER BY time_created", (last_timestamp,))
new_sessions = c.fetchall()

# 2. 找到有增量消息的旧 session（session 创建早于上次分析，但有新消息）
c.execute("""
    SELECT DISTINCT s.id, s.title, s.time_created
    FROM session s
    JOIN message m ON s.id = m.session_id
    WHERE s.time_created <= ? AND m.time_created > ?
    ORDER BY s.time_created
""", (last_timestamp, last_timestamp))
updated_sessions = c.fetchall()

all_sessions = list(new_sessions) + list(updated_sessions)
# 去重
seen = set()
unique_sessions = []
for s in all_sessions:
    if s[0] not in seen:
        seen.add(s[0])
        unique_sessions.append(s)

for sid, title, tc in unique_sessions:
    # 对于旧 session 的增量消息，只导出 time_created > last_timestamp 的消息
    c.execute("SELECT id, data, time_created FROM message WHERE session_id = ? ORDER BY time_created", (sid,))
    messages = c.fetchall()
    for mid, data_str, msg_tc in messages:
        # 如果是旧 session，只处理增量消息
        if msg_tc <= last_timestamp:
            continue
        data = json.loads(data_str)
        role = data.get('role', '?')
        c2 = conn.cursor()
        c2.execute("SELECT data FROM part WHERE message_id = ? ORDER BY time_created", (mid,))
        parts = c2.fetchall()
        # 提取 text 类型的 part 内容
        # 提取 tool 类型的 part（工具名+参数）
```

导出时重点关注：
- **用户消息**：完整保留（这是用户原话，用于判断偏好和习惯）
- **助手文本**：保留关键操作总结（用于判断工作流）
- **工具调用**：保留工具名和关键参数（用于判断重复操作模式）

### 2.5 采集外部数据源

在 session 内容导出后，**依次检测并采集所有可用的外部数据源**，获取分析时间段内的增量信息。采集结果与 session 数据合并，共同作为后续分析的输入。

**采集顺序**（按信息密度和可靠性排序）：

1. **WeLink 聊天记录**：
   - 检测 `welink-cli` 可用性；未安装则**自动安装** `npm install -g @welink/welink-cli`
   - 如果 token 过期，**自动执行 `welink-cli auth login`** 刷新（非交互，连接 WeLink PC 客户端）；刷新失败才提示用户
   - 获取会话列表，按优先级分批读取消息（每次最多3个会话，串行读取）
   - 读取后立即摘要关键信息（决策、进展、待办、风险），不保留原始消息全文
   - 将摘要与 session 数据合并分析

2. **CodeHub 代码提交**：
   - 检测 `git` 可用性
   - **项目目录发现**：在用户常用项目目录中执行 `git log`。如果不知道用户的项目目录，按以下优先级发现：
     1. 从 session 的 `directory` 字段提取用户工作过的目录
     2. 从记忆 skill 中读取用户的项目路径
     3. 搜索用户主目录下包含 `.git` 的子目录（限制搜索深度为2层，避免耗时过长）
     4. 如果以上均无法发现，跳过此数据源并在报告中说明
   - 获取分析时间段内的提交记录
   - 提取：提交次数、关键 MR 概要、代码行数变更
   - **可选补充：CodeHub MCP 工具**（见"数据源 2"详述）。若 `PRIVATE_TOKEN` 可用且 `uvx` 可启动服务器，对发现的项目调用 `list-merge-requests` + `get-merge-request-reviews`，补充本地 git 看不到的 MR 检视意见和 Issue 数据。不可用则跳过，不影响本地 git 采集

3. **W3 搜索**（可选）：
   - 检测 W3 搜索 MCP 工具可用性
   - 搜索用户近期公开信息

4. **CloudDevOps Wiki**（可选）：
   - 检测 huawei-wiki MCP 工具可用性
   - 搜索用户近期撰写的 Wiki 文档

5. **AI 辅助研发 Token 消耗**（可选）：
   - 检测 `nga.cmd` 可用性
   - 汇总分析时间段内的 token 消耗

**合并分析规则**：
- 外部数据源的信息与 session 数据**交叉验证**：如果 WeLink 中讨论了某项工作但 session 中没有，说明该工作未使用 AI 辅助，仍应纳入记忆更新
- 外部数据源可能揭示 session 中未体现的**工作模式**：如频繁参与某个项目的会议讨论，说明该项目是当前重点
- 代码提交记录可以验证 session 中声称完成的工作是否确实已提交

### 3. 分析并提取长期记忆

**用户身份获取**（仅首次创建记忆 skill 时需要）：
- 优先从 session 内容推断：用户消息中可能包含姓名、工号、部门等信息
- 如果推断不出，直接询问用户："请告诉我你的姓名和工号，用于初始化个人记忆"
- 从外部数据源补充：W3 搜索、CloudDevOps Wiki、WeLink 等可用数据源会进一步丰富身份信息

从新 session 中提取以下类别的信息：

**用户偏好与习惯**
- 反复强调的工作方式
- 对 AI 行为的明确要求
- 沟通风格偏好

**开发环境与工具**
- 新发现的环境特性
- 工具配置变更
- 新的踩坑经验

**项目与团队**
- 新的项目信息
- 团队人员变动
- 新的协作模式

**重要决策和结论**
- 用户做出的技术选型决策
- 对方案的明确取舍
- 对流程的改进决定

**排除规则**：
- 不提取一次性的操作细节（如某个具体的 git 命令）
- 不提取已存在于记忆 skill 中的信息
- 不提取敏感信息（密码、Token、密钥）

### 4. 发现重复模式并创建/更新 skill

**前置步骤：历史 bug 回溯验证**

在分析新 session 之前，**必须先回溯验证历史 session 中用户报过的 bug 是否已真正修复**。这是最容易遗漏的环节——用户在更早的 session 中报了 bug，AI 可能在当时修了代码逻辑，但没有修 SKILL.md 的约束规则、没有修已经出问题的现状、或者根本没修。

**执行方式**：
1. 搜索**所有历史 session**（不限增量范围）中用户提到的 bug、问题、错误、修复请求。关键词：`bug`、`问题`、`修复`、`出错`、`不对`、`遗漏`、`又出现`、`老问题`、`没修`、`没更新`、`没确认`
2. 对每个历史 bug，验证三件事：
   - **代码/脚本是否已修复**：如果 bug 涉及 skill 中的脚本文件（如 `all_in_one.py`），读取当前脚本检查修复是否存在
   - **SKILL.md 是否已加约束**：如果 bug 的根因是 AI 行为问题（如"没确认就提交"、"重复加 US号"），检查 SKILL.md 中是否已加入明确的禁止规则
   - **已出问题的现状是否已修复**：如果 bug 已经造成了错误结果（如 commit message 中 US号重复了），检查是否已修正该结果，而非只修了生成逻辑
3. 如果任一项未完成，**必须立即修复**，并在报告中列出
4. **回溯验证也适用于 huawei-auto-evolve 自身**：如果历史 session 中用户对自演进引擎的行为提出纠正（如"你没分析出来"、"你漏了某个 bug"、"你应该举一反三"、"你应该能更新自己"），必须检查本 SKILL.md 中是否已加入对应的规则或流程改进。如果没有，立即补充

**为什么需要这一步**：
- 增量分析只看新 session，但用户报的 bug 可能在更早的 session 中，AI 当时可能只修了部分（如只修了代码没修 SKILL.md，或只修了根因没修现状）
- 用户不会反复提醒同一个 bug，如果分析器不主动回溯验证，这些半修的 bug 就永远悬着
- 典型案例：用户在 session A 中报了某函数的 try/except/pass 问题，AI 修了一处但没修同文件中其他同类问题；后续增量分析只看 session B/C/D，永远不会再发现 session A 中未修完的 bug

**识别标准**（满足任一即可）：
- **跨 session 重复**：同类任务在 **2个及以上 session** 中出现
- **单 session 复杂技能**：AI 在 **单个 session** 中执行某类任务时，**工具调用超过5轮**（即 AI 自主进行了5轮以上的工具调用链），说明该任务有足够的复杂度和固定流程，值得固化为 skill
- 任务有 **3步以上** 的固定流程
- AI 在执行时 **犯过错误** 且错误可被规则预防
- 流程中 **无需人类决策** 或只需少量决策

**举一反三：泛化识别规则**：

这是本 skill 最关键的能力之一。当识别到一个模式时，**必须主动思考**：这个模式还能推广到哪些类似场景？

**泛化维度**（每个识别到的模式都必须逐条检查）：

1. **同构不同域**：如果某个域的任务模式成立，检查其他域是否存在相同的结构
   - 例：发现"统计 token 消耗"需要多轮工具调用后，应想到"统计代码行数"、"统计 MR 数量"、"统计 Wiki 数量"等同构任务也可能需要 skill
   - 例：发现"MR 代码检视"需要分析变更→生成报告→发送通知，应想到"文档检视"、"配置检视"等同构流程
   - 例：发现用户在 UT 编写中纠正了断言风格，应想到集成测试、E2E 测试中是否也需要同样的风格规范

2. **同域不同层**：如果某个抽象层的模式成立，检查上下层是否也需要
   - 例：发现"生成日报"需要 skill，应想到"生成周报"、"生成月报"是否也需要
   - 例：发现"单个 MR 检视"需要 skill，应想到"批量 MR 检视"是否也需要
   - 例：发现"单个文件分析"需要 skill，应想到"项目级分析"、"模块级分析"是否也需要

3. **同工具不同场景**：如果某个工具在场景 A 中需要固定流程，检查场景 B/C 是否也需要
   - 例：发现 CloudDevOps Wiki 在"发布设计文档"场景需要 skill，应想到"搜索文档"、"统计文档"是否也需要
   - 例：发现 welink-cli 在"生成日报"场景需要 skill，应想到"查找同事信息"、"发送通知"是否也需要

4. **反面模式泛化**：如果 AI 在某个场景犯了错，检查所有类似场景是否都有同样的风险
   - 例：AI 在 UT 中忘了提取常量，应想到在所有代码生成场景中是否都需要"先定义常量"的规则
   - 例：AI 在某个 API 调用中忘了错误处理，应想到所有 API 调用场景是否都需要强制错误处理

**泛化执行规则**：

- **创建 skill 时**：不要只针对当前观察到的具体任务创建窄 skill，而是思考该 skill 的**自然边界**在哪里。如果多个同构任务可以共用一个 skill，就创建一个更通用的 skill，在 description 中列出所有触发场景
  - 好：`huawei-auto-evolve-created-stats-collector`（触发词：统计token、统计代码行数、统计MR数量、统计Wiki数量）
  - 差：`huawei-auto-evolve-created-token-stats`（只能统计 token）
- **更新 skill 时**：当发现新的类似场景时，检查是否应该**扩展已有 skill 的范围**而非创建新 skill。如果已有 skill 的流程可以复用到新场景，则更新已有 skill 的 description 和流程说明，增加新场景的触发词和处理分支
- **记忆 skill 更新时**：当从 session 中提取到一条经验时，思考这条经验的**适用范围**，写入记忆时标注其适用场景，而非只记一个具体实例
  - 好："用户偏好所有代码中常量提取到文件顶部，适用于 UT、集成测试、工具脚本等所有代码生成场景"
  - 差："用户偏好 UT 中常量提取到文件顶部"

**泛化检查清单**（每次分析时必须逐项过一遍）：

| 检查项 | 问题 | 行动 |
|--------|------|------|
| 同构不同域 | 这个模式在其他域是否存在？ | 如存在，扩展 skill 范围或创建通用 skill |
| 同域不同层 | 这个模式在更粗/更细的粒度是否也需要？ | 如需要，补充到 skill 或创建配套 skill |
| 同工具不同场景 | 涉及的工具在其他场景是否也需要固定流程？ | 如需要，扩展 skill 或创建新 skill |
| 反面模式泛化 | 这个错误在所有类似场景是否都有风险？ | 如有风险，将预防规则写入所有相关 skill |
| 经验适用范围 | 这条经验是只适用于当前场景，还是通用规则？ | 如通用，写入记忆时标注适用范围 |

**强制规则：禁止主观跳过**：
- 当上述标准被满足时，**必须创建 skill**，AI 不得以"本质上是简单调用"、"已被其他 skill 覆盖"等主观理由跳过
- 即使某个功能看起来简单（如 `nga.cmd metrics`），只要 AI 在执行时需要多轮摸索（找工具→试命令→逐个调用→汇总），就说明该流程值得固化，避免下次重复摸索
- 唯一可跳过的例外：该任务已有**同名或功能完全等价**的 huawei-auto-evolve-created skill 存在
- **泛化时也禁止跳过**：如果泛化检查发现新的适用场景，即使该场景在 session 中尚未出现，也必须更新 skill 的 description 和流程说明，确保下次遇到时能正确触发

**"5轮工具调用"判定规则**：
- 统计方式：在单个 session 中，连续执行的、服务于同一目标的工具调用序列算作一轮。例如"搜索→读取→编辑→验证"是一个完整的工具调用轮次
- 阈值：如果 AI 为完成某类任务自主执行了 **5轮及以上** 的工具调用，说明该任务足够复杂，应考虑固化为 skill
- 典型场景举例：
  - 统计 token 消耗：需要列出 session → 逐个获取 metrics → 汇总计算（多轮工具调用，≥5轮）
  - MR 代码检视：需要获取 MR 变更 → 逐文件分析 → 生成报告 → 发送通知（≥5轮）
  - 日报生成：需要查询聊天 → 读取消息 → 检查代码 → 搜索文件 → 汇总输出（≥5轮）
- 排除：简单的一次性操作（如单次 grep 查找、单次文件编辑）不算

**创建新 skill 规则**：
- 名称以 `huawei-auto-evolve-created-` 为前缀
- 安装到 `{ANALYZER_SKILL_DIR}/output/huawei-auto-evolve-created-<name>/SKILL.md`（嵌套于 huawei-auto-evolve 目录内，与其他 huawei-auto-evolve 依赖 skill 同级）
- **必须通过调用 skill-creator skill 来创建新 skill**，而非直接写文件。具体流程：
  1. 加载 `skill-creator` skill（使用 skill 工具加载）
  2. 按照skill-creator的流程执行：
     - **Step 1（理解skill）**：基于从session中分析出的模式，明确skill的功能、触发场景、使用示例
     - **Step 2（规划资源）**：确定是否需要scripts/、references/、assets/目录，以及具体内容
     - **Step 3（初始化）**：运行 `{ANALYZER_SKILL_DIR}/skill-creator/scripts/init_skill.py huawei-auto-evolve-created-<name> --path {ANALYZER_SKILL_DIR}/output` 创建模板目录（若 skill-creator 位于同级 `{SKILLS_DIR}/skill-creator/`，则路径相应改为 `{SKILLS_DIR}/skill-creator/scripts/init_skill.py`，init 的 `--path` 也相应指向 `{SKILLS_DIR}`）
     - **Step 4（编辑skill）**：填充SKILL.md和资源文件，遵循skill-creator的设计原则：
       - frontmatter中description必须写清功能+触发词+使用场景（这是AI决定何时调用的唯一依据）
       - body使用祈使句/不定式
       - 遵循progressive disclosure原则：核心流程在SKILL.md（<500行），详细参考放references/
       - 只包含AI不知道的非显而易见的信息，不写AI已知的一般性解释
       - 设置适当的自由度：脆弱操作用具体脚本（低自由度），多种方案都可行时用文本指令（高自由度）
     - **Step 5（打包）**：跳过打包步骤（huawei-auto-evolve-created skill不需要打包分发）
     - **Step 6（迭代）**：后续分析session时根据实际使用反馈迭代更新
  3. 创建完成后，验证SKILL.md的frontmatter格式正确、description包含完整触发词
- **降级策略**：如果skill-creator不可用（未安装且自动安装失败），退化为直接创建目录+写SKILL.md，但必须在报告中提示用户手动安装skill-creator以获得更高质量的skill
- SKILL.md 中应包含完整的执行流程、工具使用方法、输出格式，确保下次 AI 加载该 skill 后无需重新摸索即可执行

**更新已有 skill 规则**：
- **修改范围限制**：自演进引擎只能修改以下两类 skill，**禁止修改其他任何 skill**（如 skill-creator、mr-reviewer、ppt-master-huawei 等非 huawei-auto-evolve-created 的 skill 属于第三方或手动安装的，不得擅自修改）：
  1. `{ANALYZER_SKILL_DIR}/output/huawei-auto-evolve-created-*` 目录下的所有 skill（嵌套于 huawei-auto-evolve 目录内）
  2. `huawei-auto-evolve` 自身（`{ANALYZER_SKILL_DIR}/`）
- 遍历 `{ANALYZER_SKILL_DIR}/output/huawei-auto-evolve-created-*` 目录 + `huawei-auto-evolve` 自身目录（`{ANALYZER_SKILL_DIR}/`）。注意：huawei-auto-evolve-created skill 现在嵌套在 huawei-auto-evolve 目录内，而非 `{SKILLS_DIR}` 下
- **如果不存在任何 `huawei-auto-evolve-created-*` 目录**（首次运行场景），跳过"更新已有 skill"步骤，仅执行"创建新 skill"步骤。不要报错或警告，这是正常的首次运行行为
- **不跳过任何 skill**，包括 `huawei-auto-evolve` 自身。自演进引擎必须能根据 session 中的经验更新自身的流程、规则和注意事项，而不是等用户提醒才更新。`huawei-auto-evolve-created-global-memory` 在步骤3中单独更新，此处也纳入检查但以步骤3的更新为准
- **更新 huawei-auto-evolve 自身时的特殊规则**：自演进引擎是通用工具，设计目标是可分享给其他用户。因此更新自身时必须区分两类经验：
  - **通用方法论 → 更新到 huawei-auto-evolve**：任何用户都会受益的分析能力改进，如"历史 bug 回溯验证"、"举一反三泛化"、"修 bug 要修三件事"等。这些是引擎本身的能力缺陷，不依赖特定用户
  - **个人偏好 → 只更新到 global-memory**：特定用户的工作习惯，如特定的构建命令、项目特有的依赖配置等。这些是用户个人项目的知识，不应写入通用引擎
  - **判断标准**：如果去掉用户身份和项目上下文，这条经验对其他用户是否仍然有价值？如果是 → 通用方法论；如果否 → 个人偏好
- 检查新 session 中是否有与该 skill 相关的新经验
- 新经验包括：新的踩坑点、流程改进、规则补充、异常处理补充、**代码风格反馈**（用户对命名、断言、常量等风格的纠正）
- **主动触发规则**：如果在单个 session 中用户对同一 skill 的行为纠正了 **3次及以上**，说明该 skill 存在系统性缺陷，**必须更新**该 skill 的 SKILL.md 加入预防规则，不得以"用户只在单次 session 中纠正"为由跳过。典型案例：用户在一个 session 中反复纠正 UT 编码规范（常量提取、断言风格、硬编码字符串等），说明 ut-writer skill 缺少这些规则，必须补充
- **用户纠偏必沉淀规则**：只要用户在调用任何 skill 的过程中对 AI 的行为进行了纠正（包括但不限于：指出遗漏、纠正做法、补充步骤、要求举一反三、指出没确认就执行、指出只修根因没修现状等），**必须**将该纠偏沉淀到对应 skill 的 SKILL.md 中，作为预防规则。纠偏出现1次就更新，不需要等重复。这是 skill 自我完善的核心机制——用户每纠正一次，skill 就应该进化一次，确保同类问题不再发生。典型案例：用户纠正"commit message 没确认就提交了"→ 更新 mr-sender skill 加入"commit message 必须确认"规则；用户纠正"你只修了代码没修 SKILL.md"→ 更新 huawei-auto-evolve skill 加入"修 bug 要修三件事"规则
- **用户反馈必沉淀规则（比纠偏更广）**：不仅"纠正"要沉淀，所有用户对 skill 行为的**反馈**都必须沉淀。用户不一定要说"你做错了"才算反馈——以下表达都算反馈，必须更新到对应 skill：
  - "又忘了xxx" → 说明规则存在但无效，需加强
  - "不对吧" / "你没有xxx" → 说明 AI 行为与用户预期不符
  - "下次记得xxx" / "以后要xxx" → 明确的新规则请求
  - "这个skill应该xxx" → 对 skill 流程的直接建议
  - "你怎么没xxx" / "你这次没xxx" → 指出遗漏
  - "是不是应该xxx" → 暗示当前行为不对
  - 用户对自演进引擎说"你没有更新xxx" → 自演进引擎自身遗漏了某项更新
  - **关键原则**：用户不会无缘无故提到某个 skill 的行为。只要用户提到了，就说明当前行为有问题，必须更新。宁可误更新（后续用户可以纠正），不可漏更新（用户不会再重复说）
- **所有session反馈提取**：从所有被分析的session（包括历史session和当前session）中提取用户反馈并更新对应 skill。提取方式：回溯每个 session 中所有用户消息，识别上述"用户反馈必沉淀"中列出的表达模式，立即更新对应 skill。当前 session 虽然不计入增量统计，但同样必须提取反馈——用户反馈往往发生在当前 session，如果等到下次分析才处理，用户在中间这段时间可能已经再次遇到同样的问题
- **规则有效性检查（关键能力）**：仅检查"规则是否存在"是不够的，必须检查"规则是否有效"。一条规则写在了 SKILL.md 里但 AI 反复违反，说明规则需要**加强**而非仅仅存在。这是分析器最容易遗漏的环节——看到规则已存在就跳过，但没意识到规则虽然写了却没起作用。
  - **检测信号**（满足任一即触发）：
    1. 用户说"又忘了"、"又出现了"、"你这次没xxx"、"不是说过要xxx吗"——这表示规则存在但AI没遵守
    2. AI违反了SKILL.md中已有的规则1次——说明规则的措辞或位置不够强，不需要等重复
    3. 用户纠正的内容在SKILL.md中已有类似规则——说明现有规则不够有效，需要加强
  - **加强策略**（按严重程度递进）：
    1. **提升规则位置**：从列表中间移到核心约束顶部或流程步骤0（门控步骤）
    2. **增加门控机制**：将"应该做"改为"不做不准继续"，要求AI确认后才能进入下一步
    3. **增加反面案例**：把AI的具体违规行为作为❌禁止项写入
    4. **拆分规则**：如果一条规则覆盖面太广，拆成多条更具体的规则
  - **典型案例**：ut-writer SKILL.md 中"必须先读 for_ai_to_read/ut_coding_convention.md"写在核心约束第21行、流程步骤3，AI反复跳过。分析器看到规则已存在就跳过了，但实际需要将其提升为流程步骤0门控步骤，并增加"不读完禁止继续"的硬性约束
- **五个维度都要检查**：
  1. **重复模式**：同类经验在 2+ session 中出现（原有标准）
  2. **用户纠正**：即使用户只在单次 session 中纠正了 AI 的行为，也必须更新到对应 skill（例如：用户在 UT 编写中多次纠正常量提取、断言风格、防御性测试等，这些经验即使只在一个 session 中出现，也应更新到 ut-writer skill）
  3. **复杂技能固化**：AI 在单个 session 中执行某类任务超过5轮工具调用，且该任务尚无对应 skill，应创建新 skill；若已有对应 skill 但缺少该流程/工具/细节，应补充更新
  4. **举一反三泛化**：当发现某个 skill 的经验/规则/流程可以推广到其他类似场景时，必须扩展该 skill 的适用范围或更新相关 skill。具体做法：
     - 如果某条规则在场景 A 中被验证有效，检查 skill 中是否还有其他场景 B/C/D 也应该应用该规则，如果是则补充
     - 如果发现某个 skill 的流程模式可以被同构任务复用，更新 description 增加新触发词，并在流程说明中增加对应分支
     - 如果某个踩坑经验具有通用性（不只是当前 skill 的特定问题），检查是否需要同步到其他相关 skill
  5. **历史 bug 回溯**：检查历史 session 中用户报过的 bug，验证是否已同时修复了代码、SKILL.md 约束规则、已出问题的现状这三项。如果只修了其中部分，必须补全。特别关注：用户报了 bug 后 AI 只修了根因代码但没在 SKILL.md 中加约束（导致下次还会犯同类错误）、只修了生成逻辑但没修已经出问题的结果、修了 A 处但同类的 B/C/D 处没修
  6. **规则有效性检查**：检查 SKILL.md 中已有规则是否被 AI 实际遵守。规则存在≠规则有效，如果AI反复违反某条规则，说明规则需要加强（提升位置、增加门控、增加反面案例）。这是最容易遗漏的维度——分析器看到"规则已存在"就跳过，但没意识到规则虽然写了却没起作用
- 判断是否需要更新的关键：**重复模式**或**用户明确纠正**或**复杂技能固化**或**举一反三泛化**，满足任一即应更新
- 直接修改 SKILL.md 文件

### 5. 执行更新

**更新记忆 skill**：
- 读取 `{ANALYZER_SKILL_DIR}/output/{MEMORY_SKILL_NAME}/SKILL.md`（记忆 skill 作为 huawei-auto-evolve-created skill，位于 output/ 目录内）
- 如果不存在，**首次创建**：
  1. 创建目录 `{ANALYZER_SKILL_DIR}/output/{MEMORY_SKILL_NAME}/` 和基础 SKILL.md（含 frontmatter 和标题）
  2. 依次检测外部数据源（W3、CloudDevOps Wiki、WeLink），可用的全部采集
  3. 综合分析所有采集数据，生成初始记忆内容，写入以下分类：
     - 用户身份
     - 工作习惯与偏好
     - 关键同事与人际关系
     - 开发环境
     - 已知踩坑与经验
     - 项目与团队
     - 工具与路径
  4. 在报告中说明哪些数据源成功采集、哪些跳过
- 如果已存在，仅从 session 增量分析中追加新信息（不删除已有内容）
- 如果新信息与已有信息矛盾，用新信息替换

**创建新 skill**：
- **必须调用 skill-creator skill 来创建**，具体流程见步骤4"创建新 skill 规则"
- 简要流程：加载skill-creator → init_skill.py初始化 → 编辑SKILL.md和资源文件 → 验证
- 如果skill-creator不可用（未安装且自动安装失败），降级为：创建目录 `{ANALYZER_SKILL_DIR}/output/huawei-auto-evolve-created-<name>` → 直接写入SKILL.md

**更新已有 skill**：
- 直接编辑对应的 SKILL.md

### 6. 记录分析时间

将本次分析的时间戳写入 `{ANALYZER_SKILL_DIR}/last_analysis.txt`：

```python
import time
with open(os.path.join(ANALYZER_SKILL_DIR, "last_analysis.txt"), 'w') as f:
    f.write(str(int(time.time() * 1000)))
```

### 7. 报告结果

向用户汇报：
- 分析了多少个新 session
- 采集了哪些外部数据源（WeLink/CodeHub/W3/Wiki等），哪些跳过及原因
- 更新了记忆 skill 中的哪些内容
- 创建了哪些新 skill（名称+用途）
- 更新了哪些已有 skill（更新了什么）

### 8. 推荐并安装 skill

根据本次分析的综合结果（session + 外部数据源），在 agentcenter 市场中搜索可能对用户有用的 skill，推荐并安装。

**前置条件**：`agentcenter` CLI 已安装且已认证。若 `agentcenter --version` 失败（command not found 或 module not found），**自动执行重装**（见前置条件中的"agentcenter 自动修复"），不要跳过、不要提示用户。重装后验证通过才继续。如果认证过期，执行 `agentcenter auth` 重新认证。

**推荐逻辑**：

基于以下信号识别用户可能需要的 skill：
1. **工作场景匹配**：从 WeLink 聊天和 session 中识别用户的工作场景（如日报、MR检视、Wiki撰写、代码分析等），搜索对应 skill
2. **工具使用频率**：如果用户频繁使用某个工具（如 welink-cli、git、nga.cmd），搜索该工具相关的 skill
3. **痛点识别**：如果用户在 session 中反复遇到某类问题（如 UT 编写、token 统计、文档发布），搜索对应的解决方案 skill
4. **已有 skill 的生态补充**：如果用户已安装某个 skill，搜索与之配套的 skill（如已安装 mr-reviewer，可推荐 doraemon-mr-sender）

**执行流程**：

1. **生成搜索关键词**：基于上述信号，提取 3-5 个搜索关键词
2. **搜索 agentcenter 市场**：
   ```bash
   agentcenter search skill --keyword <关键词> --json
   ```
   - 如果 `--json` 参数不支持，改用 `agentcenter skill list --keyword <关键词>` 或直接通过 `agentcenter skill add <skill-name> --dry-run` 预览信息
   - **注意**：`agentcenter search skill` 可能进入交互式选择模式（需要箭头键），在非交互环境中会报错。遇到此情况，改用 `agentcenter skill add <skill-name> --client <client> -g -f` 直接安装，或先通过 API/Web 端搜索获取 skill 名称
3. **筛选推荐列表**：
   - 排除用户已安装的 skill
   - 排除功能与已有 huawei-auto-evolve-created skill 完全重叠的 skill
   - 优先推荐：下载量高、版本号高（说明维护积极）、description 与用户场景高度匹配的 skill
   - 每次最多推荐 5 个 skill
4. **展示推荐**：向用户展示推荐列表（名称、版本、描述、推荐理由），**询问用户是否安装**
5. **用户确认后安装**：
   ```bash
   agentcenter skill add <skill-name> --client huawei-auto-evolve --path {ANALYZER_SKILL_DIR} -f
   ```
   - **关键**：必须用非内置的 `--client huawei-auto-evolve`（或任意非内置值）配合 `--path {ANALYZER_SKILL_DIR}`，才能将 skill 安装到 huawei-auto-evolve 目录内。若用内置 client（`claudecode`/`opencode`/`cac` 等）加 `-g`，`--path` 会被忽略，skill 会落到该 client 的全局 skills 目录，违反"依赖 skill 安装在 huawei-auto-evolve 文件夹内"的约束
   - 安装后验证 `{ANALYZER_SKILL_DIR}/<skill-name>/SKILL.md` 是否存在
6. agentcenter 是必备依赖——若不可用，先自动重装（见"agentcenter 自动修复"），修复后继续执行；只有修复也失败才阻塞并在报告中说明

**禁止行为**：
- 不得未经用户确认就安装 skill
- 不得安装功能与已有 skill 完全重复的 skill
- 不得推荐与用户工作场景无关的 skill

### 9. 检查并更新 skill 新版本

检查用户已安装的所有 skill（包括 huawei-auto-evolve-created 和从 agentcenter 安装的）是否有新版本，有则更新。

**前置条件**：`agentcenter` CLI 已安装且已认证。

**执行流程**：

1. **遍历已安装 skill**：扫描 `{ANALYZER_SKILL_DIR}/` 下所有包含 `SKILL.md` 的子目录（即 huawei-auto-evolve 目录内的所有依赖 skill，含 skill-creator 等）
2. **对每个非 huawei-auto-evolve-created 的 skill**，在 agentcenter 市场中搜索其最新版本：
   ```bash
   agentcenter search skill --keyword <skill-name> --json
   ```
   - 交互式环境问题同步骤8，优先使用 `--json` 或非交互式替代命令
3. **版本比较**：
   - 读取已安装 skill 的 SKILL.md frontmatter 中的版本信息（如有）
   - 与市场中的最新版本比较
   - 如果市场版本 > 已安装版本，标记为可更新
4. **对于 huawei-auto-evolve-created 开头的 skill**：这些是本地生成的，不在市场中发布，跳过版本检查
5. **展示更新列表**：向用户展示可更新的 skill（名称、当前版本→最新版本、更新内容摘要），**询问用户是否更新**
6. **用户确认后更新**：
   ```bash
   agentcenter skill add <skill-name> --client huawei-auto-evolve --path {ANALYZER_SKILL_DIR} -f
   ```
   - 同步骤8，必须用非内置 `--client huawei-auto-evolve` + `--path {ANALYZER_SKILL_DIR}` 安装到 huawei-auto-evolve 目录内
   注意：更新会覆盖已有文件，如果用户对 skill 有本地修改，需先备份
7. agentcenter 是必备依赖——若不可用，先自动重装（见"agentcenter 自动修复"），修复后继续；只有修复也失败才阻塞并在报告中说明

**安全规则**：
- 更新前检查 skill 的 SKILL.md 是否有本地修改（与市场版本 diff），如果有本地修改，在更新列表中标注"有本地修改，更新可能覆盖"
- 不得未经用户确认就更新 skill
- 更新后验证 SKILL.md 的 frontmatter 格式正确

## 注意事项

- **依赖 skill 必须安装在 huawei-auto-evolve 文件夹内**：所有 huawei-auto-evolve 依赖、创建或更新的 skill（skill-creator、huawei-auto-evolve-created-*、{MEMORY_SKILL_NAME} 等）必须安装在 `{ANALYZER_SKILL_DIR}/` 下，**禁止安装到全局/客户端 skills 目录**（如 `~/.claude/skills`、`~/.cac/skills`、`~/.config/opencode/skills`）。通过 agentcenter 安装时，必须使用 `--client huawei-auto-evolve --path {ANALYZER_SKILL_DIR}`（非内置 client 值才能让 `--path` 生效），**禁止**使用内置 client（`claudecode`/`opencode`/`cac` 等）加 `-g`，否则 `--path` 被忽略、skill 落到全局目录
- **AI 必须先加载本 skill 再执行分析**，不要自行实现分析逻辑。当用户触发分析时，第一步就是调用本 skill
- 分析时不要把当前 session 自身算作"新 session"（当前 session 还在进行中）
- 创建 skill 时确保 description 写清触发词，否则 AI 不知道何时调用
- 更新 skill 时保持原有结构，只追加/修改必要内容
- 更新已有 skill 时，不要仅依赖"重复模式"判断，用户单次 session 中的纠正和复杂技能（≥5轮工具调用）也是重要更新来源
- **举一反三是核心能力，不是可选步骤**：每次分析时必须执行泛化检查清单，不能因为"session 中没出现"就跳过泛化思考
- **宁可泛化过度，不可泛化不足**：如果拿不准某条经验是否应该泛化，默认泛化。后续可以通过用户纠正来收窄范围，但漏掉的泛化不会自动补上
- **历史 bug 回溯是必做步骤，不是可选步骤**：每次分析时必须搜索所有历史 session 中的 bug/问题/修复请求，验证是否真正修完。增量分析只能发现新问题，回溯验证才能发现半修的旧问题
- **修 bug 要修三件事**：代码/脚本 + SKILL.md 约束规则 + 已出问题的现状，缺一不可。如果只修了代码但没在 SKILL.md 中加约束，下次 AI 还会犯同样的错。**同样重要的第四件事**：如果项目有规范文件（如 `for_ai_to_read/`、`docs/` 等 AI 可读的约定文档），修 bug 时也必须同步更新规范文件，否则 AI 下次写代码时不会读取到新规则，同类问题会反复出现
- **反复出现的 bug 需深挖根因**：如果用户说某个 bug"又出现了"或"之前就出现过"，说明之前的修复只治标不治本。分析器必须追问：为什么修了还会复发？是 SKILL.md 约束不够明确？是约束有了但 AI 没遵守？是修了 A 场景但 B/C/D 场景没修？必须找到根因并彻底修复，不能只做表面修补
- **规则存在≠规则有效**：这是分析器最容易犯的错误——检查到 SKILL.md 中已有某条规则就认为"已处理"，跳过更新。但规则写了AI不遵守，说明规则需要**加强**（提升位置、增加门控、增加反面案例），而非仅仅存在。AI违反已有规则1次就必须加强，不需要等重复。典型案例：ut-writer SKILL.md 中"必须先读 for_ai_to_read"规则存在，但AI反复跳过，直到将其提升为流程步骤0门控步骤才有效。检测信号：用户说"又忘了"、"你这次没xxx"、AI违反了已有规则
- **修改 skill 代码后必须同步安装目录**：skill 通常有两份副本——项目仓库（用于版本控制）和安装目录（AI 实际加载的）。修改任一份后，必须同步到另一份，否则 AI 加载的还是旧版。分析器在更新 skill 的脚本文件时，必须检查两份是否一致
- **迭代式分析，不要一次跑太远**：分析 session 时，先完成增量分析并报告结果，等用户确认后再做更深度的回溯分析。不要在一次分析中同时做增量分析+全量回溯+创建5个skill+更新10个文件，容易出错且用户无法及时纠偏
- **用户原话必须一字不改地保留**：在提取记忆、更新 skill、生成报告时，用户说的话必须原样引用，不能总结、改写或概括。只有 AI 的行为才需要总结。这是确保信息不丢失的关键原则
- **执行前先检查项目规范文件**：如果被分析的项目有 AI 可读的规范文件（如 `for_ai_to_read/`、`.cursorrules`、`CLAUDE.md` 等），分析器在判断"AI 是否违反规则"时应先读取这些规范文件，而非仅凭自身判断。很多用户纠偏的本质是"AI 没遵守项目已有的规范"
- **自演进引擎必须能更新自身**：当 session 中出现对引擎行为的纠正、改进建议、或用户指出引擎遗漏的问题时，必须更新本 SKILL.md，而不是等用户提醒。自演进引擎不能成为唯一一个不会被自动更新的 skill
- **看到必须行动，不能只记录不修复**：自演进引擎发现了历史 bug 未修完、skill 缺少规则、自身能力不足等问题后，必须立即修复并更新，不能只在报告中列出"发现了问题"然后等用户说"帮我修"。自演进引擎的价值在于自动闭环，不是只做诊断
- **创建 skill 时必须调用 skill-creator**：不要直接写文件创建skill，skill-creator提供了规范的结构、frontmatter格式、progressive disclosure设计等最佳实践，能显著提升skill质量。如果skill-creator未安装，自演进引擎会自动安装（见前置条件中的"skill-creator 自动安装流程"）；自动安装失败才退化为直接写文件
- **外部数据源是每次分析的标配，不是可选附加**：WeLink 聊天、CodeHub 代码提交等数据源能发现 session 中未体现的工作内容，每次分析时都必须尝试采集。不可用的跳过即可，但不能因为"上次采过了"就不再采集
- **外部数据源要增量采集**：每次只采集上次分析时间之后的增量数据，不要重复采集历史数据。WeLink 消息按时间筛选，git log 用 --since/--until 限定范围
- **WeLink 消息读取要分批串行**：禁止并行超过3个 welink-cli 消息查询，否则消息总量会超出上下文处理能力导致卡死。每批读取后立即摘要，下一批只带摘要
- **推荐和更新 skill 必须用户确认**：不得未经用户确认就安装或更新 skill，这是对用户环境的侵入性操作
- **agentcenter 是必备依赖，不可跳过**：若 `agentcenter --version` 失败，自动重装（见前置条件"agentcenter 自动修复"），不要降级跳过。只有自动重装也失败时才在报告中说明并阻塞 Task 8
- 临时导出文件分析完成后必须清理
- 不要将密码、Token 等敏感信息写入任何 skill 或记忆 skill
- 所有路径通过配置项动态获取，不硬编码用户目录

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| 数据库文件不存在 | 提示用户安装 opencode 并至少使用一次，然后重试 |
| 数据库为空（无 session） | 告知用户暂无 session 可分析，建议使用 opencode 一段时间后再运行 |
| Skills 目录不存在 | 自动创建 `SKILLS_DIR` 目录 |
| Skills 目录无写权限 | 提示用户检查权限，或手动指定其他目录 |
| 外部数据源不可用 | 先尝试自动修复（welink-cli 自动安装/刷新、CodeHub uvx 自动发现、agentcenter 自动重装）；修复失败才跳过该数据源，在报告中说明原因，不影响核心分析功能 |
| 首次运行数据量过大 | 分批处理（每次最多 20 个 session），记录时间戳，提示用户再次运行继续分析 |
| 记忆 skill 创建失败 | 检查目录权限，重试一次；仍失败则告知用户手动创建 |
| welink-cli 未安装 | **自动安装**：`npm install -g @welink/welink-cli`；安装后重新检测；失败才跳过并提示用户 |
| welink-cli token 过期 | **自动执行 `welink-cli auth login` 刷新**；刷新失败才跳过并提示用户 |
| agentcenter 未安装或损坏（`agentcenter --version` 报 command not found 或 module not found） | **自动重装**：`NO_PROXY=cmc.centralrepo.rnd.huawei.com npm install -g @aimarket/agentcenter --@aimarket:registry=https://cmc.centralrepo.rnd.huawei.com/artifactory/api/npm/product_npm/ --strict-ssl=false`。重装后验证；仍失败才阻塞 Task 8 并提示用户 |
| agentcenter 认证过期 | 尝试 `agentcenter auth` 重新认证；失败则跳过 skill 推荐和版本检查 |
| skill 安装/更新失败 | 在报告中说明失败原因，不影响其他分析结果 |
