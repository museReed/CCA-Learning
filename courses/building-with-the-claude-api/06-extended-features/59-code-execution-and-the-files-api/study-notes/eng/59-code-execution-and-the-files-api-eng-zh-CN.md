# Code Execution and the Files API — Engineering Deep Dive（简体中文）

| 项目 | 详情 |
|------|------|
| 考试领域 | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.4（server-side tools）、2.1（tool schema 设计）、1.2（multi-turn tool loop） |
| 来源 | building-with-the-claude-api / 06-extended-features / Lesson 59 |

---

## One-Liner

Files API 让你把文件上传一次、之后用 ID 引用；Code Execution 是一个 server-side Python 沙箱（隔离 Docker 容器、没有网络），Claude 可以直接驱动——两者组合起来，你就能把真正的计算工作交给 Claude，而不用自己搭执行环境。

---

## Files API — 上传一次，多次引用

一般你把文件（图片、PDF）以 base64 嵌在 message 里。Files API 是另一条路：单独上传文件，拿到一份 file metadata 对象和一个独特的 **file ID**，之后的 message 就用这个 ID 引用。

流程：

1. 通过专用 API 调用上传文件（图片、PDF、文本、CSV 等）。
2. 拿到一份 file metadata 对象，内含 **file ID**。
3. 之后的 message 用 file ID 引用，不再嵌入原始 bytes。

为什么重要：

- 不用每次请求都重发文件——一次上传，多次引用。
- 大文件变得可以便宜复用——不用在每个请求里塞 base64。
- 它是把数据**送入／取出** Code Execution 沙箱的主要通道，因为沙箱没有网络。

---

## Code Execution Tool — Server-Side Python 沙箱

Code Execution 是一个 **server-side tool**。与一般 client-side tool 不同，你不用自己实现——只要在请求里声明预设的 tool schema，Claude 就可以在隔离环境中执行 Python。

执行环境的特性相当刻意：

| 特性 | 细节 |
|------|------|
| **Runtime** | 隔离 Docker 容器中的 Python |
| **网络访问** | **无**。容器不能调用外部 API |
| **Iteration** | Claude 可在单次对话中多次执行 code，随分析进展迭代 |
| **集成** | 结果被捕获、由 Claude 解读，产出最终响应 |
| **需要实现** | **客户端不需要**——这是 Anthropic 提供的 server-side tool |

隔离是特性，不是限制：它让你能安全地让 Claude 跑 code，不用暴露你的 infra、密钥或网络。

---

## 结合 Files API + Code Execution

因为 Docker 容器**没有网络**，Files API 自然成为桥梁：它是把数据**送进**、把生成的 artifact **取出**的主要通道。

典型 workflow：

1. 用 Files API 上传数据文件（例如 CSV）。
2. 在 message 里放一个 `container_upload` block 带 file ID，让沙箱收到文件。
3. 要 Claude 分析数据。
4. Claude 在容器里写 Python 并执行来处理文件。
5. Claude 可以生成输出（图表、报告）并通过 Files API 提供下载。

这是干净的委派模式：你控制输入输出，Claude 处理 code。

---

## 实战示例：流失分析

课程演示一份流媒体服务数据集（`streaming.csv`），包含用户信息——订阅档位、观看习惯、流失标签。

先用 helper 函数上传：

```python
file_metadata = upload('streaming.csv')
```

然后建一条 message，把文本指令和一个 `container_upload` block 配在一起引用上传的文件，并启用 code execution tool：

```python
messages = []
add_user_message(
    messages,
    [
        {
            "type": "text",
            "text": """Run a detailed analysis to determine major drivers of churn.
            Your final output should include at least one detailed plot summarizing your findings."""
        },
        {"type": "container_upload", "file_id": file_metadata.id},
    ],
)

chat(
    messages,
    tools=[{"type": "code_execution_20250522", "name": "code_execution"}]
)
```

关键：

- `container_upload` block 是把上传文件注入沙箱的方式。
- `tools` list 只有一项，`type: "code_execution_20250522"`——预设 server-side tool schema，你不用实现。
- Claude 收到指令和文件引用后，就能跑 Python 分析。

---

## 响应结构

Claude 使用 code execution 时，response 会含多种 block 类型交错出现：

| Block 类型 | 内容 |
|-----------|------|
| **Text blocks** | Claude 的分析、推理、自然语言说明。 |
| **Server tool use blocks** | Claude 决定要跑的实际 Python code。 |
| **Code execution tool result blocks** | 跑 code 的输出（stdout、错误、文件 handle）。 |

Claude 可以在单次响应中**多次**执行 code，逐步建立分析（读入 → 检视 → 清理 → 绘图 → 总结）。每个执行 cycle 以一个 `server tool use` block 接一个 `code execution tool result` block 呈现。

---

## 下载生成的文件

最强大的特性之一是 Claude 可以生成文件（图表、报告、转换后的 CSV）并让你下载。当 Claude 在容器里建出一张可视化图，它会存储在容器中，你可以通过 Files API 取回。

找 response 里 `type: "code_execution_output"` 的 block——里面有生成内容的 file ID。用 Files API 下载：

```python
download_file("file_id_from_response")
```

这完成了整个来回：CSV 进（通过 Files API），图表出（通过 Files API），中间 Claude 做完所有 pandas／matplotlib 的工作。

---

## 不只数据分析

虽然流失分析是标准例子，这个组合还能做很多其他委派模式：

- **图像处理与操作** — 缩放、格式转换、特征提取。
- **文档解析与转换** — PDF 提取、格式转换、脱敏处理。
- **数学计算与建模** — 模拟、优化、统计检验。
- **报表生成** — 从原始数据生成 HTML 或 PDF 输出。

底层模式相同：Files API 控制*数据边界*，Code Execution 处理*计算*，Claude 用自然语言协调两者。

---

## Common Mistakes

1. **忘记沙箱没有网络** — 写出 `requests.get(...)` 的 code 一定失败；数据必须通过 Files API 进去。
2. **可以用 file ID 却把大文件 inline** — 每个请求都 base64 嵌入大 CSV，浪费 token 和成本；上传一次、用 ID 引用。
3. **以为必须自己实现 code execution tool** — 它是 server-side。你只声明 schema，Anthropic 跑 Python。
4. **漏掉生成的输出** — 没扫 response 找 `code_execution_output` block，就看不到 Claude 产出的图表和报告。
5. **以为沙箱会跨 session 保留** — 容器是 ephemeral；Files API 的 file ID 才是持久的 handle，不是容器状态。
6. **没准备迭代** — Claude 可以在单次响应中多次跑 code；handler 只期待一个 execution block 会漏掉后面的数据。

---

> **Key Insight**
>
> Code Execution 是**完全不用客户端实现的 server-side tool**——你声明 schema、Claude 在隔离容器跑 Python、你读结果 block。Files API 是补上容器没网络这个缺口的数据边界。两者一起让你把整条计算 workflow 委派给 Claude：数据上传进去，拿回分析和 artifact，完全不用自己搭执行 infra。

---

## CCA Exam Relevance

- **D2（Tool Design）** — Code Execution 是 **server-side tool** 的典型示例。要知道你不用实现；只要在 `tools` list 里声明 `{"type": "code_execution_20250522", "name": "code_execution"}`，Claude 就会替你跑 Python。
- **D1（Agentic Architecture）** — 多次执行 code（Claude 在单次响应多次执行）是一个完全跑在 server side 的 agentic loop。
- 记住沙箱特性：隔离 Docker 容器、没有网络、Python runtime、ephemeral。
- 记住 Files API 是进／出桥梁：文件靠 `container_upload` 进去，artifact 靠 `code_execution_output` → `download_file(file_id)` 出来。

---

## Flashcards

| Front | Back |
|-------|------|
| Files API 让你做什么？ | 上传文件（图片、PDF、CSV 等）一次、拿到 file ID，之后的 message 用该 ID 引用，不用再嵌入原始数据。 |
| Code Execution 是 client-side 还 server-side tool？ | Server-side——你不用实现；你声明预设 schema，Claude 就在隔离容器中跑 Python。 |
| Code Execution 使用什么 runtime 和环境？ | 隔离 Docker 容器中的 Python，**没有网络**。 |
| 为什么用 Code Execution 时 Files API 不可或缺？ | 沙箱没网络，唯一把数据送进去、把 artifact 取出来的方式就是通过 Files API 上传／下载。 |
| 哪个 block 类型把上传的文件注入沙箱？ | `container_upload`，带着 Files API 上传回来的 `file_id`。 |
| 要启用 code execution，tool schema 要填什么？ | 在 `tools` list 里放 `{"type": "code_execution_20250522", "name": "code_execution"}`。 |
| Claude 可以在单次响应中多次执行 code 吗？ | 可以——迭代进行，把 text、server tool use block、code execution result block 交错。 |
| Code execution 响应里会出现哪三种 block？ | Text block（Claude 的解释）、server tool use block（Python code）、code execution tool result block（输出）。 |
| 怎么取回 Claude 在容器中生成的文件？ | 找 `code_execution_output` block 里的 file ID，然后用 Files API 调用 `download_file(file_id)`。 |
| 说出三个 Code Execution + Files API 的非数据分析用途。 | 图像处理、文档解析与转换、数学计算与建模、报表生成。 |
