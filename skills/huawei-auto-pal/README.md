# huawei-auto-pal Setup / 配置指南

This guide helps a new user set up huawei-auto-pal. The core skill works with
**zero configuration** — optional tools enhance the analysis but are not required.
本指南帮助新用户配置 huawei-auto-pal。核心功能**零配置**即可使用，可选工具增强分析能力。

---

## What works out of the box / 开箱即用

Retro-scope (the diagnosis phase) runs on Python 3.9+ with no credentials, no
CLI tools, and no `.env` file. It automatically detects:

retro-scope（诊断阶段）仅需 Python 3.9+，无需凭据、CLI 工具或 `.env` 文件，自动检测：

| Source / 数据源 | What it captures / 捕获内容 | Requirement / 要求 |
|---|---|---|
| Claude Code | AI session prompts, tool calls, errors | Claude Code installed |
| Codeagent (new) | AI session JSONL records | Codeagent installed |
| Codeagent (legacy) | AI session SQLite records | nga.db exists |
| Git | Commits, checkouts | git on PATH |
| Chrome | Browser history, searches, downloads | Chrome installed |
| Edge | Browser history, searches, downloads | Edge installed |
| VS Code History | Per-file edit timestamps | VS Code used |
| Windows Recent | .lnk file shortcuts | Windows |
| Jump Lists | App+doc pairs | Windows |
| WeLink recordings | Meeting recording metadata | `WELINK_RECORDINGS_DIR` set |

To check which sources are available on your machine:
检查你的机器上有哪些数据源可用：

```bash
python retro-scope/scripts/run.py --check
```

---

## Optional tools / 可选工具

These tools enhance the analysis but are **not required**. Install them only if
you want the additional data. The skill detects each tool and skips it with a
coverage note if missing — it never blocks the pipeline.

这些工具增强分析能力但**非必需**。仅在需要额外数据时安装。技能会自动检测每个工具，缺失时跳过并说明影响——不会阻塞流程。

### welink-cli — WeLink messages/meetings/calendar/mail

**Adds / 增加数据**: WeLink chat history, meeting records, calendar events, email.
**Prerequisite / 前置条件**: Node.js ≥ v18 (`node -v`), WeLink PC client installed.

```bash
NO_PROXY=cmc.centralrepo.rnd.huawei.com \
  npm install -g @welink/welink-cli \
  --strict-ssl=false \
  --@welink:registry=https://cmc.centralrepo.rnd.huawei.com/artifactory/api/npm/product_npm/
```

- Verify / 验证: `welink-cli --version`
- Login / 登录: `welink-cli auth login` (connects to WeLink PC client, non-interactive refresh, token valid ~30 min)

**Proxy note / 代理说明**: The intranet npm registry must bypass the corporate
proxy (`NO_PROXY=cmc.centralrepo.rnd.huawei.com`). Prefer the trusted corporate
CA; if TLS interception still blocks the approved Huawei intranet registry,
`--strict-ssl=false` is permitted for this single command only. Do not write it
to global config or use it for public registries.

内网 npm registry 必须绕过公司代理。优先配置可信 CA；若 TLS 拦截仍阻断华为内网
registry，可对单次安装使用 `--strict-ssl=false`，不要写入全局配置，也不要用于公网。

### agentcenter — Skill market management

**Adds / 增加数据**: Skill market search, version checking, skill installation.
**Prerequisite / 前置条件**: Node.js ≥ v18.

```bash
NO_PROXY=cmc.centralrepo.rnd.huawei.com \
  npm install -g @aimarket/agentcenter \
  --strict-ssl=false \
  --@aimarket:registry=https://cmc.centralrepo.rnd.huawei.com/artifactory/api/npm/product_npm/
```

- Verify / 验证: `agentcenter --version`
- If `agentcenter --version` reports `Cannot find module .../src/bin/index.js`
  (shim exists but package missing, common after node_modules cleanup), rerun
  the install command above.

### uvx (uv) — CodeHub MCP server runtime

**Adds / 增加数据**: CodeHub MR reviews, issues (via local MCP server).
**Prerequisite / 前置条件**: uv/uvx (not a Huawei internal tool).

- Install / 安装: `winget install astral-sh.uv` (Windows) or see
  [astral-sh/uv](https://github.com/astral-sh/uv/releases)
- Verify / 验证: `uvx --version`
- If `uvx` is not on PATH, see
  [`../../mcp-tools/huawei-codehub/README.md`](../../mcp-tools/huawei-codehub/README.md)
  to configure `CODEHUB_UVX_ARGS`.

### nga.cmd — AI dev token statistics (optional)

**Adds / 增加数据**: AI-assisted development token consumption stats.
**Prerequisite / 前置条件**: CodeAgent CLI suite installed.

Verify with `nga.cmd --help`. If not on PATH, follow your CodeAgent CLI install
docs — do not hardcode a drive path.

---

## Credential setup / 凭据配置

Some supplementary data sources (used by skill-forge) require credentials.
Copy the template and fill in your values:

skill-forge 的部分补充数据源需要凭据。复制模板并填入真实值：

```bash
# 1. Copy the template / 复制模板
cp .env.example .env

# 2. Edit .env and fill in your real tokens / 编辑 .env 填入真实 token

# 3. Load credentials before running / 运行前加载凭据
set -a; source .env; set +a

# 4. Verify .env is gitignored and not tracked / 验证 .env 未被跟踪
git check-ignore .env    # should print: .env
git ls-files .env        # should print nothing
```

> **Important / 重要**: `.gitignore` prevents new files from being tracked, but
> it does **not** untrack a file that is already committed. Always verify with
> `git ls-files`. If a credentials file was accidentally committed, remove it
> with `git rm --cached .env` and commit the removal.
>
> `.gitignore` 只能阻止新文件被跟踪，**不能**取消已跟踪的文件。务必用
> `git ls-files` 验证。如果凭据文件已被意外提交，用 `git rm --cached .env` 移除。

### CODEHUB_TOKEN — CodeHub personal access token

**Used for / 用于**: Reading MR reviews and issues from Huawei internal Git repos.

**How to get it / 获取方式**:

1. Login to CodeHub (`https://codehub-g.huawei.com/`)
2. Click your avatar → **Settings / 设置**

   ![CodeHub 设置入口](img/codehub-settings.PNG)

3. Go to **Access Tokens / 访问令牌**

   ![访问令牌管理](img/codehub-settings-token-manage.PNG)

4. Create a new token with `api` or `read_api` scope (minimum)

   ![创建令牌](img/codehub-settings-token-create.PNG)

5. Copy the generated token

**Add to `.env` / 填入 `.env`**:
```
CODEHUB_TOKEN=your_codehub_token_here
CODEHUB_HOST=https://codehub-g.huawei.com/
```

**CODEHUB_HOST**:
- `codehub-g.huawei.com`: reachable from most Huawei networks (recommended / 推荐)
- `codehub-y.huawei.com`: may be unreachable on some segments — switch to `-g` if timeouts occur
- Test reachability: `NO_PROXY=*.huawei.com curl -sS -o /dev/null -w "%{http_code}\n" https://codehub-g.huawei.com/`

**Network / 网络**: CodeHub is an intranet host — bypass the corporate proxy
(`NO_PROXY=*.huawei.com`). The wrapper is at
[`../../mcp-tools/huawei-codehub/codehub.py`](../../mcp-tools/huawei-codehub/codehub.py).

### GITHUB_TOKEN — GitHub personal access token

**Used for / 用于**: Reading PR reviews and issues from GitHub repos.

**How to get it / 获取方式**:

1. Login to GitHub (`https://github.com`)
2. Avatar → **Settings** → **Developer settings** → **Personal access tokens**

   ![GitHub 凭据页面](img/github-settings-credentials.PNG)

3. Choose token type:
   - **Fine-grained (recommended / 推荐)**: Contents Read, Pull requests Read,
     Issues Read, Metadata Read
   - **Classic (simpler / 更简单)**: check `repo` scope

4. Copy the generated token

**Add to `.env` / 填入 `.env`**:
```
GITHUB_TOKEN=your_github_token_here
```

**Network / 网络**: GitHub is an external host — route **through** the corporate
proxy (`proxyuk.huawei.com:8080`), not `NO_PROXY`. Keep TLS verification enabled.
The current GitHub wrapper (`mcp-tools/github/github_mcp.py`) uses
`ssl.CERT_NONE` and is skipped by this skill until it is independently fixed.

### WIKI_X_AUTH_TOKEN — CloudDevOps Wiki token (optional)

**Used for / 用于**: User-level Wiki queries and write operations. Read operations
(search, fetch content) need **no token**.

**How to get it / 获取方式**: Obtain X-Auth-Token from CloudDevOps platform (browser
cookie or settings page).

**Add to `.env` (optional / 可选)**:
```
WIKI_X_AUTH_TOKEN=your_wiki_token_here
```

> skill-forge only reads Wiki documents (search, fetch content) — no token needed
> unless you want user-level queries or write operations.
>
> skill-forge 只读取 Wiki 文档（搜索、获取内容），无需此 token。仅在需要用户级查询或写操作时配置。

---

## Security / 安全须知

- `.env` is gitignored — always verify with `git ls-files .env` that it's not tracked
- Never write real token values into skills, memories, prompts, or reports
- If a token is leaked (e.g. accidentally pasted in chat), revoke it immediately
  on the platform and generate a new one
- Rotate tokens regularly (recommended: 90 days)
- This skill never installs, authenticates, or modifies configuration without
  explicit user approval for each action

- `.env` 已被 gitignore — 务必用 `git ls-files .env` 确认未被跟踪
- 不要在任何 skill、记忆或报告中写入真实 token 值
- 如果 token 泄露，立即在平台撤销并重新生成
- 定期轮换 token（建议 90 天）
- 本技能不会在未经用户明确批准的情况下安装、登录或修改配置
