# Code Execution and the Files API — PM Perspective（简体中文）

| 项目 | 详情 |
|------|------|
| 考试领域 | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.4（server-side tools）、2.1（tool schema 设计） |
| 来源 | building-with-the-claude-api / 06-extended-features / Lesson 59 |

---

## One-Liner

Files API 和 Code Execution 合起来，能让你的产品上线「把文件丢给 Claude」型的功能——用户上传文件、用自然语言提问、拿回带图表的分析结果——而你的团队不用自建数据管道、沙箱或图表渲染器。

---

## PM 为什么要关心

在这个功能之前，上线「上传 CSV 拿到分析」意味着要拥有整条管道：文件存储、沙箱 runtime、绘图库、结果 UI，以及任何一环坏掉时的值班工程师。Code Execution 把这些压缩成：**声明一个 server-side tool、把 Files API 接起来做上传／下载**。分析工作、图表生成、迭代——全由 Claude 在 Anthropic 操作的沙箱里搞定。

这是「把计算委派给 Claude」的模式，能解锁原本需要几个季度才能做出来的产品功能：数据分析、图像处理、文档转换、数学建模。你的 roadmap 只要有任何「上传 X 拿回 Y」类型的功能，这堂课就是最短的上线路径。

---

## Mental Model：可信承包商的封闭工坊

把 Code Execution 想象成雇佣一个在封闭工坊里工作的承包商：

| 承包商比喻 | API 对应 |
|------------|----------|
| 你在工坊门口把原料交给承包商 | 用 Files API 上传文件，通过 `container_upload` 送入沙箱 |
| 工坊没有电话、没有网络——不受外界干扰 | Docker 容器没有网络——安全、隔离 |
| 承包商可以在里面建造、迭代、尝试不同做法 | Claude 可以在单次响应中多次执行 Python |
| 你在门口领取完成的产品 | 你通过 Files API 下载生成文件 |
| 你不用提供工具——承包商自带 | Code Execution 是 server-side tool，无需客户端实现 |

封闭工坊不是限制——它就是**你能放心把真正 runtime 交给 Claude 的理由**。

---

## Product Use Cases

### 课程点出的高价值模式

| 场景 | 用户做什么 | Claude 做什么 |
|------|------------|----------------|
| 数据分析（流失、销售、实验） | 上传 CSV、用自然语言提问 | 清洗、分析、绘图、总结 |
| 图像处理 | 上传图片、描述要做的转换 | 在容器中跑图像库，返回处理后的图 |
| 文档解析与转换 | 上传 PDF、要求格式或脱敏 | 提取、转换、重新输出文档 |
| 数学建模 | 描述问题、上传参数 | 建立并执行模型，返回图和数字 |
| 自定义报表生成 | 上传原始数据、描述版式 | 生成格式化的 HTML／PDF 输出 |

### 不适用的场景

| 场景 | 为什么不行 |
|------|------------|
| 需要实时外部 API 的功能 | 沙箱没有网络 |
| 需要跨 session 持久状态的功能 | 容器是 ephemeral——状态要靠 Files API |
| 电子表格就能算的微小计算 | 额外成本不划算；Claude 原生推理就够便宜 |
| 高安全性数据不能离开你的 infra | 沙箱是 Anthropic hosted——要先跑合规审查 |

---

## PM Decision Framework

为「Claude 做计算」的功能 scope 时：

| 问题 | 为什么重要 |
|------|------------|
| 功能需要处理、绘图、解析或转换数据吗？ | 是就可能适合 code execution |
| 输入是文件（CSV、PDF、图片）吗？ | 是就用 Files API 上传 |
| 输出包含生成的 artifact（图表、报表）吗？ | 是就要通过 `code_execution_output` block 接下载路径 |
| 功能需要外部网络吗？ | 是就不适合——沙箱没网络 |
| 计算工作量有限（秒到分钟）吗？ | 迭代分析会如此；UX 要设计 streaming 或进度指示器 |
| 文件离开 infra 有合规顾虑吗？ | 上线前要审查 |

前三题是、后三题答案可接受，就是好下注。

---

## UX 含义

Code execution 改变了「简单功能」能做到的事。单个 prompt 可以产出：

- 含多个图表输出的分析。
- 多步骤推理（读入 → 检视 → 清洗 → 绘图 → 总结），由 Claude 旁白。
- 不需额外用户操作的迭代精修。

对用户来说，这像随时有一个资深数据分析师在线。对产品来说，你可以承诺以前需要 services 团队或复杂 UI 才能交付的结果——通过一个文本框加一个文件上传就能做到。

---

## Common PM Mistakes

1. **承诺实时数据分析** — 沙箱没网络，「获取最新股价并绘图」开箱即用不可行。要先在自己的 code 抓数据，上传结果，再调用 code execution。
2. **改用自建管道** — 团队常低估 code execution 的能力，建一套自家沙箱——结果更慢、更不稳、更难维护。
3. **忘记把生成 artifact 暴露在 UI 上** — 如果 UI 从不显示 Claude 产出的文件，用户只会看到文字说明，感觉功能没完成。要把 `code_execution_output` 文件渲染出来。
4. **低估迭代** — Claude 可能在单次响应跑 code 三到五次。UX 和 log 要接得住，不能假设只执行一次。
5. **跳过合规审查** — 只要文件离开你的 infra，法务和安全团队就要介入。企业客户上线前这关不能省。
6. **没有同时规划 Files API** — 没 Files API 的 code execution 就像没有出货门的工坊。要一起规划。

---

> **Key Insight**
>
> Code Execution + Files API 是**产品捷径**：把「我们要建一条沙箱运算管道」变成「我们要声明一个 tool、接好文件上下传」。Roadmap 上任何「用户上传 X、我们分析并返回 Y」的项目，这个组合能把几个月的工程压成一个 sprint。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）** — 要知道区别：server-side tool（如 code execution）不需客户端实现，client-side tool 则要。考题常问「什么时候你要自己实现 tool，什么时候是 Claude 在 server 端跑」。
- 记住沙箱特性：隔离 Docker 容器、没有网络、Python。
- 记住 Files API 是数据进（`container_upload`）、出（`download_file(file_id)`）的通道。
- 题目若出现「把某个计算任务委派给 Claude」的情境，正确答案通常是 Code Execution + Files API 模式。

---

## Flashcards

| Front | Back |
|-------|------|
| Code Execution + Files API 解锁哪类产品功能？ | 用户上传文件、用自然语言请求分析／转换／报表，而你的团队不用自建沙箱或管道。 |
| Files API 为产品做什么？ | 提供「上传一次、用 ID 引用」的文件模式，同时作为 Code Execution 沙箱进／出的桥梁。 |
| Code Execution 是 server-side 还是 client-side tool？ | Server-side——无需客户端实现；Claude 替你在隔离容器跑 Python。 |
| 为什么沙箱没有网络？ | 那是隔离／安全特性——容器不能调用外部 API，执行环境因此安全。 |
| 举一个这个模式不适合的功能。 | 需要实时外部 API 的东西（沙箱没网络），或需要跨 session 持久状态的东西。 |
| 哪个 mental model 很好地描述这个模式？ | 可信承包商的封闭、离线工坊——你在门口交原料，他在里面工作，你在门口领产品。 |
| 为什么 PM 不该改用自建沙箱？ | 因为 server-side tool 把几个月的工作压成一次 tool 声明加 Files API 接线，团队也省下维护自家 runtime 的成本。 |
| 哪种 block 把生成文件交还给你？ | 带 file ID 的 `code_execution_output` block，通过 Files API 取回。 |
