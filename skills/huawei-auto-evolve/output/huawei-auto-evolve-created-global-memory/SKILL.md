---
name: huawei-auto-evolve-created-global-memory
version: 0.0.1
description: 长期记忆 skill。存储用户身份、工作习惯、开发环境、项目与团队等信息，供 huawei-auto-evolve 自演进引擎在每次分析时读取和增量更新。
---

# 全局记忆 (huawei-auto-evolve-created-global-memory)

本文件由 huawei-auto-evolve 自演进引擎自动生成和维护，存储用户的长期记忆。
每次运行自演进分析时，引擎会从 session 和外部数据源中提取新信息，增量更新到此文件。

## 用户身份

- **姓名**：高博
- **工号**：b00563677
- **部门**：云计算BU云服务产品部数字化平台部（据 W3 任命通知 2025-003号）
- **WeLink UID**：b00563677

## 工作习惯与偏好

- 重视自包含、开箱即用的工具设计——git clone 后无需额外安装即可运行（仅凭据需用户配置）
- 要求依赖安装在项目文件夹内，**禁止安装到全局目录**（如 `~/.claude/skills`、`~/.config/opencode/skills`）
- 重视一致命名——所有华为特定工具用 `huawei-` 前缀
- 重视诚实文档——工具的前置条件（如需 uvx、需 token）必须在 README 中明确说明，不能假装"免安装"
- 偏好 `.env` 文件管理凭据（gitignored），而非 config.yaml
- 要求 AI 能自动修复的问题就自动修复，不要把已知修复方案的问题抛给用户
- 要求 session 聚焦——明确声明本 session 的目标（如"只关注 auto-evolve"），不偏离

## 开发环境

- **OS**：Windows 11 Pro (10.0.22631)，Git Bash
- **Python**：3.12.10 (pyenv-win, `C:/Users/b00563677/.pyenv/pyenv-win/versions/3.12.10`)
- **Node.js**：v22.23.1 (winget)
- **Git**：2.55.0.windows.2
- **uv/uvx**：`D:/CodingAgentCLI/uv/uvx.exe`（不在 bash PATH 上，需 CODEHUB_UVX_ARGS 或完整路径）
- **nga.cmd**：`D:/CodingAgentCLI/nga.cmd`（不在 bash PATH 上，.bashrc 已添加 /d/CodingAgentCLI）
- **agentcenter**：v1.1.34，npm 全局安装，需 `product_npm` registry + NO_PROXY + --strict-ssl=false
- **welink-cli**：v1.0.14，npm 全局安装，token 每 30 分钟过期，`welink-cli auth login` 非交互刷新
- **公司代理**：`proxyuk.huawei.com:8080`，做 TLS 拦截（MITM）
  - 内网主机需 NO_PROXY 绕过
  - uv/uvx 在 Windows 上读注册表代理，NO_PROXY 不可靠，需 `--allow-insecure-host`
  - urllib 用 `ProxyHandler({})` 强制绕过
- **opencode session DB**：`~/.local/share/opencode/db/ngagent.db`（97 messages, 1 session）

## 关键同事与人际关系

- **刘泽宇**（l00921965）：分享 Agent 评测构建经验，Wiki 文档撰写者
- **刘羽洋**：讨论组成员
- **杨迪宇、杨立博**：讨论组成员
- **刘嘉悦**：讨论组成员
- **姜旭阳**（j00679256）：IT智能体小分队，分享会议材料
- **IT智能体小分队**：工作群，讨论 Agent 评测、会议 AI 纪要

## 项目与团队

- **misc 仓库**（`D:\workspace\misc`）：技能/插件/MCP工具集合，供任何 agent/harness 使用
  - 三类 artifact：skills、opencli-plugins、mcp-tools
  - 四个 MCP 工具：huawei-w3-search、huawei-codehub、huawei-wiki、huawei-clouddevops
  - 三个子模块：anthropic-skills、superpowers、mattpocock-skills（位于 skills/ 下）
  - Git 子模块 relocated from root to skills/
- **auto-evolve / huawei-auto-evolve**：自演进引擎 skill，本次 session 的核心工作对象
- **huawei-retro-scope**：回顾分析 skill（其他 agent 的工作）
- **huawei-chaspark**：茶思屋 OpenCLI 插件
- **webpage-to-markdown**：网页转 Markdown skill

## 已知踩坑与经验

- **agentcenter 安装**：必须用 `product_npm` registry（`npm-all` 会 401），必须 `NO_PROXY=cmc.centralrepo.rnd.huawei.com`，必须 `--strict-ssl=false`
- **uvx TLS 问题**：公司代理拦截 TLS，uv 拒绝重签名证书，报 `client error (Connect)`；修复：`--allow-insecure-host cmc.centralrepo.rnd.huawei.com`（灵感来自 git-corporate-proxy-lfs skill 的 `http.schannelCheckRevoke=false`）
- **mcp-server-codehub 打包缺陷**：pyproject.toml 漏声明 `python-dotenv` 依赖；`mcp` 2.0 移除了 `FastMCP`，需 `--with "mcp<2"` pin
- **Windows bash 不识别 .cmd**：`which nga.cmd` 失败，需 `command -v nga.cmd || ls /d/CodingAgentCLI/nga.cmd`
- **MCP stdio 多 content item**：CodeHub 服务器返回 list 时，每个元素是独立的 content item（不是单个 JSON 数组），wrapper 需解析所有 items 并组装 list
- **Claude Code 安装**：公司防火墙阻止 npm postinstall 下载二进制；用 `--registry=https://registry.npmmirror.com` 绕过
- **argparse.REMAINDER 陷阱**：`--json` 放在 tool name 之后会被 REMAINDER 吞掉，需 pre-extract 全局 flags
- **外部主机 vs 内网主机代理方向相反**：华为内网工具（w3-search/codehub/wiki/clouddevops）需 **绕过** 代理（`ProxyHandler({})`）；GitHub 等外部主机需 **通过** 代理（`ProxyHandler({"https": "proxyuk...})` + `ssl.CERT_NONE`）。这是首次在 repo 中出现"通过代理"的工具
- **env var 命名规范**：用户面用 `<PLATFORM>_TOKEN` / `<PLATFORM>_HOST`（如 `CODEHUB_TOKEN`、`GITHUB_TOKEN`、`CODEHUB_HOST`）；若服务器期望不同名称（如 CodeHub 服务器读 `PRIVATE_TOKEN`/`WEB_HOST`），wrapper 内部翻译，不暴露给用户
- **Claude Code vs opencode session DB**：auto-evolve 读 opencode 的 `ngagent.db`，不读 Claude Code 的 session 存储。在 Claude Code 中的工作不会出现在 auto-evolve 的分析范围内——这是已知 gap

## 工具与路径

- **misc 仓库根**：`D:\workspace\misc`
- **huawei-auto-evolve 目录**：`skills/huawei-auto-evolve/`
- **MCP 工具目录**：`mcp-tools/{github,huawei-w3-search,huawei-codehub,huawei-wiki,huawei-clouddevops}/`
- **.env（凭据）**：`skills/huawei-auto-evolve/.env`（CODEHUB_TOKEN + CODEHUB_HOST + GITHUB_TOKEN，gitignored，参见 README.md 获取指南）
- **catalog 生成**：`./scripts/generate-catalog.sh`（从 manifests 自动生成 CATALOG.md）
- **adversarial-review skill**：`skills/adversarial-review/`（用于代码审查）
- **evolved skills 输出目录**：`skills/huawei-auto-evolve/output/`（huawei-auto-evolve-created-* skills 存放处）
