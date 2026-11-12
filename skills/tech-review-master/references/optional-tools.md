# 可选工具

两项工具及其行为测试均已包含在本技能中，许可与署名见 [LICENSE](../LICENSE)。只在相关任务中使用；普通段落审阅无需运行它们。需要 Python 3.10 或更新版本，均只使用标准库，无需安装第三方包或联网。

命令中的脚本路径相对于技能目录。待审文档路径应显式指定，避免默认扫描整个工作目录。

## 中文文案检查

```powershell
python scripts/lint_copy_rules.py "D:/project/docs/guide.md"
```

脚本只读，区分高置信度错误、依赖上下文的警告和风格提示。默认仅错误导致失败；不要默认启用 `--strict`，否则项目允许的引号、称呼或缩写也可能使检查失败。

词表和排版建议主要针对中文。它不是通用英文语法检查器或 AI 文本检测器；命中一个词不证明表达有问题。代码、URL 和 Markdown 结构有保护逻辑，但仍应核对结果。项目术语和官方名称优先，不按提示自动替换。

## 中文 Markdown 段落换行

先检查或预览，不写回原文：

```powershell
python scripts/unwrap_md_paragraphs.py --check "D:/project/docs/guide.md"
python scripts/unwrap_md_paragraphs.py --stdout "D:/project/docs/guide.md"
```

`--check` 发现可合并的硬换行时返回 2；这表示有格式建议，不等于文档有事实错误。`--stdout` 输出预览。

只有用户已批准相应格式修改时，才运行不带 `--check` 或 `--stdout` 的写回命令。工具面向中文 Markdown，不对英文文档强制一段一行，也不重新格式化代码、表格或需要保留的引用。写回后检查差异与拼接处的中英文留白。

## 维护工具时验证

在技能目录运行：

```powershell
python -m unittest discover -s tests
```

这些测试验证工具的文本处理、Markdown 保护和命令行行为，不证明审阅意见或生成文字质量。
