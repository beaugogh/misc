# skill-forge 配置指南

本文件说明如何安装 skill-forge 所依赖的 CLI 工具，以及如何获取 `.env` 中各凭据变量。

## 快速开始

```bash
# 1. 安装 CLI 工具（见下方"CLI 工具安装"）
# 2. 在 huawei-auto-pal 目录中复制凭据模板
cp .env.example .env
# 3. 按下方说明填入真实凭据
# 4. 使用前加载凭据
set -a; source .env; set +a
```

---

## CLI 工具安装

skill-forge 可选使用以下 CLI 工具。以下命令供用户手动执行；agent 必须先说明
目标、影响和版本，并获得明确批准，不能自行安装、登录或修复。

### 前置条件

- **Node.js ≥ v18**：`node -v` 验证。未安装参考 https://3ms.huawei.com/km/blogs/details/22148443
- **公司代理**：安装内网 npm 包需绕过代理（`NO_PROXY=cmc.centralrepo.rnd.huawei.com`）。优先按内部 IT 文档配置可信 CA（例如 npm 的 `cafile`）。若公司 TLS 检查仍阻断这个已批准的华为内网 registry，可对单次安装使用 `--strict-ssl=false`；不要把该设置写入全局配置，也不要用于公网 registry。

### welink-cli — WeLink 消息/会议/日历/邮件

```bash
NO_PROXY=cmc.centralrepo.rnd.huawei.com \
  npm install -g @welink/welink-cli \
  --strict-ssl=false \
  --@welink:registry=https://cmc.centralrepo.rnd.huawei.com/artifactory/api/npm/product_npm/
```

验证：`welink-cli --version`
登录：`welink-cli auth login`（连接 WeLink PC 客户端，非交互刷新，token 有效期约 30 分钟）

### agentcenter — Skill 市场管理

```bash
NO_PROXY=cmc.centralrepo.rnd.huawei.com \
  npm install -g @aimarket/agentcenter \
  --strict-ssl=false \
  --@aimarket:registry=https://cmc.centralrepo.rnd.huawei.com/artifactory/api/npm/product_npm/
```

验证：`agentcenter --version`

> 如果 `agentcenter --version` 报 `Cannot find module .../src/bin/index.js`（shim 存在但包丢失，常见于 node_modules 被清理后），重新执行上述安装命令即可修复。

### uvx (uv) — CodeHub MCP 服务器运行环境

CodeHub MCP 工具通过 `uvx` 启动一个本地 Python MCP 服务器。uv/uvx 不是华为内部工具，从官方安装：

- 官网：https://github.com/astral-sh/uv
- Windows：`winget install astral-sh.uv` 或从 [releases 页面](https://github.com/astral-sh/uv/releases) 下载
- 验证：`uvx --version`
- **PATH 注意**：如 `uvx` 不在 PATH，参考 [`../../mcp-tools/huawei-codehub/README.md`](../../mcp-tools/huawei-codehub/README.md) 配置 `CODEHUB_UVX_ARGS`。

### nga.cmd — AI 辅助研发 Token 统计（可选）

nga.cmd 是 CodeAgent CLI 套件的一部分。使用 `nga.cmd --help` 验证；如果不在
PATH，按本机 CodeAgent 安装文档定位，不要在 skill 中固化某个盘符。

---

## 凭据配置

`.env` 已被 gitignore，但 ignore 规则不会自动取消已跟踪文件。创建后用
`git check-ignore .env` 和 `git ls-files .env` 验证它未被跟踪。

### CODEHUB_TOKEN — CodeHub 个人访问令牌

**用途**：CodeHub MCP 工具（`huawei-codehub`）访问华为内部 Git 仓库的 MR、检视意见、Issue 数据。

**获取方式**：

1. 登录 CodeHub（`https://codehub-g.huawei.com/`）
2. 点击右上角头像 → **设置**

   ![CodeHub 设置入口](img/codehub-settings.PNG)

3. 进入 **访问令牌**（Access Tokens）页面

   ![访问令牌管理](img/codehub-settings-token-manage.PNG)

4. 创建新令牌，勾选所需权限（`api` 或 `read_api` 最小权限）

   ![创建令牌](img/codehub-settings-token-create.PNG)

5. 复制生成的令牌（格式如 `xxxxxxxxxxxxxxxx...`）

**填入 `.env`**：
```
CODEHUB_TOKEN=你的CodeHub令牌
CODEHUB_HOST=https://codehub-g.huawei.com/
```

**CODEHUB_HOST 说明**：
- `codehub-g.huawei.com`：大多数华为网络可直接访问（推荐）
- `codehub-y.huawei.com`：部分网络段不可达，如遇到超时请切换为 `-g`
- 验证可达性：`NO_PROXY=*.huawei.com curl -sS -o /dev/null -w "%{http_code}\n" https://codehub-g.huawei.com/`

**网络注意**：CodeHub 是华为内网主机，按内部网络策略配置。仓库包装器位于
[`../../mcp-tools/huawei-codehub/codehub.py`](../../mcp-tools/huawei-codehub/codehub.py)。

### GITHUB_TOKEN — GitHub 个人访问令牌

**用途**：GitHub MCP 工具（`github`）访问 GitHub 托管仓库的 PR、review、issue、commit 数据。

**获取方式**：

1. 登录 GitHub（`https://github.com`）
2. 点击右上角头像 → **Settings** → **Developer settings** → **Personal access tokens**

   ![GitHub 凭据页面](img/github-settings-credentials.PNG)

3. 选择令牌类型：
   - **Fine-grained（推荐）**：权限更细，可限定仓库
     - Repository access → 选择 `Public Repositories` 或指定仓库
     - Permissions → Repository permissions：
       - Contents: Read（读取文件、提交）
       - Pull requests: Read（读取 PR、review）
       - Issues: Read（读取 issue）
       - Metadata: Read（必选）
     - 生成后令牌格式如 `github_pat_11AA...`
   - **Classic（更简单）**：勾选 `repo` scope 即可覆盖所有操作
     - 生成后令牌格式如 `ghp_xxxxx...`
4. 复制生成的令牌

**填入 `.env`**：
```
GITHUB_TOKEN=你的GitHub令牌
```

**网络注意**：GitHub 是外部主机，按公司代理和可信 CA 策略配置，并保持 TLS
证书校验开启。不要使用禁用证书校验的客户端；如仓库中的
[`../../mcp-tools/github/github_mcp.py`](../../mcp-tools/github/github_mcp.py) 仍使用
`ssl.CERT_NONE`，本 skill 必须跳过该补充数据源，直到包装器被独立修复和验证。

### WIKI_X_AUTH_TOKEN — CloudDevOps Wiki 用户令牌（可选）

**用途**：Wiki MCP 工具（`huawei-wiki`）的用户级查询（如 `list-my-pending-wiki-countersigns`）和写操作。读操作（搜索、获取文档内容）**无需此令牌**。

**获取方式**：从 CloudDevOps 平台获取 X-Auth-Token（通常通过浏览器登录后的 Cookie 或平台设置页面）。

**填入 `.env`（可选）**：
```
WIKI_X_AUTH_TOKEN=你的Wiki令牌
```

> skill-forge 只读取 Wiki 文档（搜索、获取内容），无需此令牌。仅当需要用户级查询或写操作时才配置。

---

## 安全须知

- `.env` 已被 `.gitignore` 忽略；仍需用 `git ls-files .env` 确认它没有被跟踪
- 不要在任何 skill、记忆 skill 或报告中写入真实 token 值
- 如果 token 泄露（如意外粘贴到聊天中），立即在对应平台撤销并重新生成
- 定期轮换 token（建议 90 天）
