# CloudDevOps Wiki API 参考

## API 端点

基础 URL：`https://clouddevops.huawei.com`

| 操作 | 方法 | URL | 必要参数 |
|------|------|-----|---------|
| 读取文档 | GET | `/devops-knowledge-management/api/wiki?sn={WIKI_SN}&request_tag={timestamp}&type=UI&filterClassify=FEATURE_API_DESIGN` | `sn` |
| 更新文档 | PUT | `/devops-knowledge-management/api/wiki/structured?requestTag={timestamp}` | payload body |
| 上传图片 | POST | `/vision-file-storage/api/file/upload?file_type=image&username={username}&domain_id=&requestTag={timestamp}` | multipart form data |

## 认证

三种方式（按优先级）：

1. **内置 W3 登录**：`--w3-username` + `--w3-password` + `--w3-cid`（或对应环境变量），脚本自动登录获取 JWT token
2. **手动 token**：`--auth TOKEN`
3. **环境变量**：`CLOUDDEVOPS_AUTH`

内置认证流程：
1. POST `https://login.huawei.com/login1/rest/hwidcenter/login` 获取 Cookie
2. POST `https://clouddevops.huawei.com/auth/api/v1/token` 用 Cookie 换取 JWT token
3. Token 缓存 5 分钟，过期自动刷新

## 文档数据结构

Wiki 文档由一个或多个 `paragraph` 组成：

### 读取响应中的 paragraph 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `content_id` | string | 段落 ID，更新时必须携带 |
| `content` | string | HTML 格式的正文内容 |
| `content_category` | string | 段落分类（如"技术方案设计"） |
| `content_sort` | number | 排序值 |
| `ui_source` | string | 来源标识，固定为 "1" |

### 更新请求中的 paragraph 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `documentClassify` | string | 固定 "DEFAULT_VALUE" |
| `category` | string | 对应读取的 `content_category` |
| `content` | string | HTML 正文 |
| `uiSource` | string | 对应读取的 `ui_source` |
| `order` | number | 对应读取的 `content_sort` |
| `contentId` | string | 对应读取的 `content_id` |

### 更新请求顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `wikiSn` | string | Wiki 文档 SN |
| `wikiTitle` | string | 文档标题 |
| `sourceSystem` | string | 固定 "cloudDevops" |
| `addActivity` | boolean | 固定 true |
| `paragraphs` | array | 段落数组 |
| `wordCount` | number | 固定 0 |
| `characterCount` | number | 固定 0 |

## 图片上传

上传图片到 CloudDevOps 文件存储，用于 Mermaid 图表渲染和文档内图片。

### 请求格式

- Content-Type: `multipart/form-data`
- 表单字段名: `avatar`
- 支持的图片类型: PNG, JPG, SVG 等

### 响应格式

```json
{
  "code": 200,
  "data": {
    "image_url": "/vision-file-storage/api/file/download/upload-v2/2026/5/2/username/uuid/image.png"
  }
}
```

完整图片 URL = `https://clouddevops.huawei.com` + `image_url`

## Mermaid 渲染模式

| 模式 | 参数 | 渲染方式 | 适用场景 |
|------|------|---------|---------|
| upload | `--mermaid upload` | PNG → 上传文件存储 → `<img src="URL">` | **推荐**，CloudDevOps Wiki 不支持内联 SVG |
| img | `--mermaid img` | PNG → base64 → `<img src="data:...">` | 文件存储不可用时的备选 |
| svg | `--mermaid svg` | 内联 `<svg>` 标签 | CloudDevOps Wiki 会显示为原始文本，**不推荐** |
| pre | `--mermaid pre` | `<pre>` 文本块 | 不需要图形化展示，或 mmdc 不可用 |

### 为什么推荐 upload 模式

CloudDevOps Wiki 使用 TinyMCE 编辑器，该编辑器不支持内联 `<svg>` 标签，会将其显示为原始文本。`upload` 模式通过以下流程解决这个问题：

1. 用 mmdc 将 Mermaid 代码渲染为 PNG 图片
2. 将 PNG 上传到 CloudDevOps 文件存储
3. 在 HTML 中使用 `<img src="URL">` 引用上传的图片

### mmdc 依赖

Mermaid 渲染需要 `mmdc`（mermaid-cli）。如果未安装：
- `upload` 和 `img` 模式会降级为 `<pre>` 文本块
- 安装方式：`npm install -g @mermaid-js/mermaid-cli`
- Windows 上命令为 `mmdc.cmd`，脚本已自动处理

## URL 解析

用户通常提供完整 URL 而非 SN，解析规则：

```
https://clouddevops.huawei.com/domains/34152/wiki/3/WIKI2026060200471
                                        ^^^^^        ^^^^^^^^^^^^^^^^
                                        domain_id    wiki_sn
```

脚本内置 `parse_wiki_url()` 函数可自动提取。
