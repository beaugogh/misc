# 中英文清晰表达指南

审阅的目标是让意思准确、直接、自然。下面列的是需要判断的信号，不是禁词表，也不用于判断文本是否由 AI 生成。原文有明确用途的术语、对比、限定和引用应保留。

## 看整段在说什么

先用一句普通话概括本段的意思，再检查原文是否确实支持它：谁做了什么，什么发生了变化，读者需要知道什么。如果无法概括，先定位缺失的对象、逻辑或证据。

按照「主要信息 → 必要解释或证据」组织。需要条件才能成立的结论，把条件放在读者能及时看到的位置。删掉重复的开头和结尾，不必给每段添加总结句。

不要把一个冗长段落仅拆成更多同样空泛的句子，也不要把全文机械改成列表。用段落解释关系，用列表呈现并列项或步骤，用表格比较同一维度。

## 常见信号与修订方法

| 表达问题 | 中文信号 | English signals | 修订方法 |
|---|---|---|---|
| 套话开场 | 随着技术的飞速发展；在当今时代 | In today's rapidly evolving landscape; As we navigate | 删除背景套话，直接进入文档的问题或结论 |
| 无信息的强调 | 值得注意的是；不难发现；显而易见 | It is important to note; Needless to say; Clearly | 直接说事实；需要强调时说明它改变了什么判断 |
| 宣传式修饰 | 全面赋能；极致体验；强大而灵活 | seamless; groundbreaking; robust and powerful | 用有证据的功能或结果代替；缺少依据的主张提出删除建议 |
| 抽象名词堆叠 | 实现能力的有效提升；形成协同闭环 | facilitate the optimization of; enable the realization of | 写出对象、动作和结果；确认对象不明时提出澄清 |
| 机械过渡 | 此外；与此同时；综上所述，反复出现 | Furthermore; Moreover; Ultimately, in every paragraph | 只保留表达实际逻辑关系所需的连接词 |
| 人造对立 | 这不仅是 X，更是 Y；不是 X，而是 Y | This isn't just X—it's Y; More than a tool | 对比不影响理解时直接陈述；真实的区别则具体解释 |
| 空泛结尾 | 为未来奠定坚实基础；仍需综合考虑 | pave the way; unlock new possibilities; only time will tell | 写明已知结论或实际下一步，没有新信息则删除 |
| 模板化结构 | 每段都先定义、再三点优势、最后升华 | repeated three-part lists, rhetorical questions, recap paragraphs | 依内容组织，避免为了形式增加句子 |

这些词在特定上下文可以准确，例如控制理论中的 robustness 或真实需要区分的两种技术方案。问题在于表达是否具体、有用、自然，不在于命中了某个词。

## 中文：动作明确，关系顺畅

**原文：**

> 值得注意的是，该模块通过对失败请求进行最多 3 次的重试处理，并在每次重试前进行 5 秒等待，来实现请求重试能力。

**建议：**

> 该模块对失败的请求最多重试 3 次，每次重试前等待 5 秒。

删除无信息的强调、名词化动作和重复结尾；保留次数与等待条件。

**原文：**

> 系统通过对已接受版本所包含的配置修改进行跨轮次继承，实现后续任务执行过程中对前序优化结果的持续利用。

**建议：**

> 系统保留已接受的配置修改，并在后续各轮任务中继续使用。

只有原文确实指「配置修改」时才能这样写。不要把含义不明的「状态」自行解释成代码、权重或记忆。

**原文：**

> 在权限校验未通过的情况下，系统可能不会执行该请求。

**建议：**

> 权限校验失败时，系统可能不执行该请求。

保留「可能」。若这不符合接口设计，应作为事实问题核查，不能在语言修订中偷偷改成「拒绝请求」。

中文检查：减少「进行……的处理」「基于……实现……的能力」等绕行表达；把连续的「的」拆成清楚的关系；用明确对象替代指代不清的「其」「该能力」。保留自然的句子节奏，不强制每句同样长。

## English: direct verbs and idiomatic sentences

**Before:**

> It is important to note that the service may perform up to three retry attempts for failed requests, with a waiting period of five seconds prior to each attempt.

**Proposed:**

> The service may retry failed requests up to three times, waiting five seconds before each attempt.

Keep “may,” the retry limit, and the timing. Remove the preamble and turn noun phrases into verbs.

**Before:**

> The system facilitates the persistence of accepted configuration modifications across successive execution cycles, thereby enabling the continued utilization of prior optimization outcomes.

**Proposed:**

> The system keeps accepted configuration changes for use in subsequent runs.

Name the saved object and explain what happens to it. Do not replace precise objects with vague words such as “things” merely to sound conversational.

**Before:**

> This is not merely a caching mechanism; it is a paradigm shift that unlocks seamless access to previously computed results.

**Proposed:**

> The cache stores computed results for reuse.

The rewrite removes the unsupported claim of a paradigm shift. In the review, flag that removal explicitly as an unsupported claim, rather than presenting it as a meaning-neutral copyedit. Do not invent latency or cost benefits.

English checks: prefer “evaluate” to “perform an evaluation of” and “use” to “make use of” when the meaning is the same. Break up dense noun strings. Use active voice when the actor matters; passive voice is useful when the result or object is the focus. Preserve the document's spelling convention and level of formality.

## 简洁不能以含义为代价

- 保留必要的 may、only、up to、unless，以及「可能」「仅」「最多」「除非」。这些词往往改变技术含义。
- 专业术语准确且读者熟悉时，保留它；新读者需要时给一次简短定义，后文不反复解释。
- 不用固定字数、句长或禁词计数代替阅读判断。很短的抽象句子也可能难懂。
- 不添加没有依据的例子、指标、机制或个人口吻来让文字显得自然。
- 已经清楚的句子保持原样。例如 “The API returns a job ID.” 和「接口返回任务 ID。」都无需为了变化而改写。
- 审阅意见同样避免套话：指出具体问题，给出替换文本；必要时解释一句为何更清楚。

## 先修复解释缺口，再润色

**原文 / Before:**

> 该设计通过异步化实现性能优化，构建高效处理闭环。
>
> The design leverages asynchronous processing to unlock seamless performance optimization.

这两句都没有说清异步处理什么、请求何时返回或如何衡量收益。先检查设计或代码。如果材料只说明请求入队后返回任务 ID，可建议：

> 接口将任务放入队列后返回任务 ID。工作进程从队列中取出任务并执行。
>
> The API queues the task and returns a job ID. A worker takes the task from the queue and runs it.

只有材料确实说明队列和工作进程时才使用这段。没有性能数据就不补写延迟下降、吞吐提高或成本降低。若只能看到原来的空泛句子，提出需要补充的信息，不能自行发明架构。

**状态与条件 / Status and conditions:**

> 计划在下个版本中允许管理员关闭重试；目前每个失败请求最多重试 3 次。
>
> The next release is planned to let administrators disable retries. Currently, each failed request is retried up to three times.

修订后仍须区分未来计划与当前行为，保留下一版本的计划时间、管理员权限、失败请求和次数上限。简化成「管理员可以关闭重试 / Administrators can disable retries」会改变事实。
