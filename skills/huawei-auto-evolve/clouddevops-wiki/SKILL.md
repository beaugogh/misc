---
name: clouddevops-wiki
description: 通过 CloudDevOps REST API 读取和更新 Wiki 文档，支持 Markdown 编写（含 Mermaid 图表）并自动转换为 HTML 发布。当用户提到 CloudDevOps Wiki、查看/编辑/更新 Wiki 文档、发布方案设计文档、把 Markdown 文档上传到 Wiki、查看设计桌面文档时使用此技能。即使用户只说"看看这个文档"并提供了 CloudDevOps URL，也应触发此技能。
---

# CloudDevOps Wiki 文档操作

通过 REST API 操作 CloudDevOps Wiki 文档，核心能力：读取文档、Markdown 编写+发布（支持段落级更新）、图片上传。

## 目录结构

```
clouddevops-wiki/
├── SKILL.md                    ← 本文件
├── scripts/wiki_api.py         ← CLI 工具（所有 API 操作）
└── references/
    ├── api_reference.md        ← API 端点、数据结构、Mermaid 模式详细文档
    └── markdown_guide.md       ← Markdown 语法和 Mermaid 图表示例
```

需要 API 细节时读 `references/api_reference.md`，需要 Mermaid 写法示例时读 `references/markdown_guide.md`。

## 前置条件

- 认证方式二选一：内置 W3 登录（推荐）或手动提供 JWT token
- 网络可访问 `clouddevops.huawei.com`（华为内网，`*.huawei.com` 不走代理）
- Mermaid 渲染需要 `mmdc`（mermaid-cli），未安装则 Mermaid 代码块保留为文本

## 认证

三种方式，按优先级：

1. **内置 W3 登录（推荐）**：传 `--w3-username` + `--w3-password`（或设 `W3_USERNAME`/`W3_PASSWORD` 环境变量），脚本自动登录获取 JWT token，自动缓存 5 分钟、过期自动刷新
2. **手动 token**：传 `--auth TOKEN`
3. **环境变量**：设 `CLOUDDEVOPS_AUTH` 环境变量

```bash
# 推荐：内置认证，一行搞定
python scripts/wiki_api.py --w3-username w00511258 --w3-password 'xxx' publish --sn WIKIxxx --input doc.md

# 或用环境变量
export W3_USERNAME=w00511258
export W3_PASSWORD='xxx'
python scripts/wiki_api.py publish --sn WIKIxxx --input doc.md
```

## URL 解析

用户通常给完整 URL 而非 SN。从 URL 提取信息：

```
https://clouddevops.huawei.com/domains/34152/wiki/3/WIKI2026060200471
                                        ^^^^^        ^^^^^^^^^^^^^^^^
                                        domain_id    wiki_sn
```

脚本内置 `parse_wiki_url()` 函数可自动提取。如果用户给了 URL，先提取 `wiki_sn` 再操作。

## 工作流选择

根据用户意图选择对应工作流：

| 用户意图 | 工作流 | 命令 |
|---------|--------|------|
| "看看这个文档" / "这个wiki写了什么" | 读取文档 | `get` |
| "把这个md发到wiki" / "发布到wiki" | Markdown 发布 | `publish` |
| "把内容写到第X章" / "更新方案设计章节" | **段落级发布** | `publish --section` |
| "先看看转换效果" / "只转HTML" | Markdown 转换 | `convert` |
| "看看文档目录" / "文档结构" / "有哪些章节" | 查看结构 | `structure` |
| "直接改HTML内容" | HTML 更新 | `update`（需手动构造 payload） |

## 工作流详解

### 1. 读取文档

```bash
python scripts/wiki_api.py --w3-username USER --w3-password PASS get --sn WIKIxxxxxxxx [--output doc.json] [--format html|text]
```

- `--format html`：输出原始 HTML（默认）
- `--format text`：输出纯文本，适合快速了解文档内容
- `--output`：保存到文件，不指定则输出到终端

### 2. 段落级发布（最常用）

只更新文档中某个章节，其他章节原样保留。这是最常见的场景——用户通常只想往某个章节填内容。

```bash
python scripts/wiki_api.py --w3-username USER --w3-password PASS \
    publish --sn WIKIxxxxxxxx --input design.md --section "3 方案设计"
```

- `--section`：匹配文档中的段落分类（category），如 `"3 方案设计"`、`"1 需求分析"`
- 先用 `structure` 命令查看有哪些可用段落
- 脚本自动完成：读取文档 → 匹配段落 → 替换内容 → 写回全部段落
- 不匹配时自动列出可用段落供选择

**如何确定 section 名称**：先运行 `structure` 命令查看段落列表，`[]` 中的分类名就是 `--section` 的值。

### 3. 全量发布

替换文档第一个段落的内容（原始行为）。

```bash
python scripts/wiki_api.py --w3-username USER --w3-password PASS \
    publish --sn WIKIxxxxxxxx --input design.md [--title "文档标题"]
```

- `--mermaid upload`（默认）：Mermaid 渲染为 PNG → 上传文件存储 → `<img>` 引用
- `--dry-run payload.json`：只生成 payload 不发送，用于预览检查

### 4. 查看文档结构

```bash
python scripts/wiki_api.py --w3-username USER --w3-password PASS structure --sn WIKIxxxxxxxx
```

输出干净的段落清单：分类名、content_id、内容预览。不再需要 `--domain-id` 参数。

### 5. Markdown 转换（不发布）

```bash
python scripts/wiki_api.py --w3-username USER --w3-password PASS \
    convert --input design.md --output design.html [--mermaid upload|svg|img|pre]
```

`--mermaid upload` 需要同时提供认证信息。

### 6. HTML 更新（高级）

直接用 JSON payload 更新文档。需要先读取文档获取 `content_id`，再构造完整 payload。

```bash
python scripts/wiki_api.py --auth "TOKEN" update --sn WIKIxxxxxxxx --payload update.json
```

## 关键注意事项

- **先读后写**：段落级发布（`--section`）自动处理"先读后写"，无需手动操作
- **完整提交**：更新时必须提交完整 `paragraphs` 数组，`--section` 模式自动保留未修改段落
- **upload 模式是默认**：CloudDevOps Wiki 的 TinyMCE 编辑器不支持内联 SVG，`publish` 默认用 `upload` 模式
- **Token 自动缓存**：内置认证的 token 缓存 5 分钟，过期自动刷新，无需手动管理
- **参数顺序**：全局参数（`--w3-username`、`--auth` 等）必须放在子命令前面
- **Obsidian 图片语法**：脚本自动将 `![[image.png]]` 转为标准 Markdown 格式
- **本地图片自动上传**：Markdown 中引用的本地图片会自动上传到 CloudDevOps 文件存储
- **图片路径含空格**：脚本会自动处理路径中的空格

## API 发布失败的降级方案

当 API 方式发布失败（如 `WIKI_ALREADY_DELETED` 错误）时，可使用 Playwright 浏览器自动化作为降级方案：

1. 用 Playwright 打开 Wiki 文档编辑页面
2. 通过 `tinymce.activeEditor.setContent(html)` 注入 HTML 内容
3. 点击保存按钮

这种情况通常发生在新创建的空文档（`content_id` 为 null）上，浏览器保存会自动初始化段落记录。
