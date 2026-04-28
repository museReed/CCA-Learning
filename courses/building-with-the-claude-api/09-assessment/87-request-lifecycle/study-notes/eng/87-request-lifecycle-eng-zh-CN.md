# 请求生命周期 Request Lifecycle — 工程深入

| 项目 | 说明 |
|------|------|
| 考试领域 | D1 — Agentic Coding & Architecture（22%）主要；D5 — Enterprise Deployment（20%）次要 |
| 任务声明 | 1.1（API request flow）、5.1（secure architecture）、5.3（stop reasons 与 token 限制） |
| 来源 | building-with-the-claude-api / 09-assessment / Lesson 87 |

---

## 一句话重点

每次 Claude 交互都是一个五步骤来回：client → 你的 server → Anthropic API → Claude 内部 pipeline（tokenize、embed、contextualize、generate）→ 回到 client —— 看懂每一步，你才能设计安全架构、快速 debug 生产问题。

---

## 五步骤请求流程

每一次与 Claude 的交互都遵循可预测的五个阶段：

1. **Request to server** —— client app 把用户输入送到你的 backend
2. **Request to Anthropic API** —— 你的 server 带着 API key 转发请求
3. **Model processing** —— Claude 执行 tokenize、embed、contextualize、generate
4. **Response to server** —— Anthropic 返回结构化的 response，包含 message、usage、stop_reason
5. **Response to client** —— 你的 server 把生成的文字转回 UI

不论你在打造 chatbot、IDE 集成、或 agentic workflow，这个形状都一样。CCA 课纲的每一个进阶模式都是建在这个 loop 上。

---

## 为什么一定要有 Server（不可直连）

来源立场明确：**绝对不要从 client-side 代码直接调用 Anthropic API**。理由：

- API request 需要 secret API key 做认证
- 把 key 放在 client code 中是严重的信息安全漏洞
- 任何人都可以把 key 挖出来做未授权的请求

正确做法：你的 web 或 mobile app 把请求送到**你自己的 server**，server 把 API key 保存在安全存储中，再对上游发送经过清理的请求。这不是便利性建议 —— 这是唯一安全的架构。

这个分层也给你地方可以加 observability、rate limiting、per-user 额度、prompt template、audit logging。每一个生产环境的 Claude app 都有一层 server 介于用户和 Anthropic 之间。

---

## 发出 API Request

Server 对 Anthropic API 发请求时，可以用官方 SDK（Python、TypeScript、JavaScript、Go、Ruby）或原生 HTTP。每个 request 都必须带四个核心字段：

| 字段 | 用途 |
|------|------|
| **API Key** | 让 Anthropic 识别你的请求 |
| **Model** | 要用的 model 名称（例如 `"claude-3-sonnet"`） |
| **Messages** | 含用户输入的 list |
| **Max Tokens** | Claude 可生成的 token 数上限 |

最小 Python 示例：

```python
from anthropic import Anthropic

client = Anthropic()  # 从环境变量读 ANTHROPIC_API_KEY

response = client.messages.create(
    model="claude-3-sonnet",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
)
print(response.content[0].text)
```

API key 放在 server 的环境变量或 secret manager —— 永远不要出现在 client 打包的代码中。

---

## Claude 内部处理

Anthropic 收到请求后，Claude 走四个内部阶段：

### 1. Tokenization

Claude 先把输入文字切成 token。token 可以是整个字、字的一部分、空格或符号。来源建议"一个字约等于一个 token"作为直觉。

### 2. Embedding

每个 token 被转成 embedding —— 代表该字所有可能意义的长串数字。把 embedding 想成"数值化定义"，捕捉语义关系。重点是：一个 token 起初承载了**所有**可能意义，消歧义在下一步。

字常常有多重意义。来源以 "quantum" 为例：

- 物理学中的离散量
- 量子力学或量子物理概念
- 极小的、次原子层级的
- 量子计算应用

### 3. Contextualization

Claude 根据周围字词来调整每个 embedding，决定在当前情境下最可能的意义。这个过程调整数值表示以凸显对的定义。这就是 model 如何为手上这句话挑出**这个**意义的 "quantum"。

### 4. Generation

Contextualized embeddings 通过 output layer，计算每个可能的下一个字的概率。Claude 不会永远挑最高概率的字 —— 它混用概率和受控的随机性，产生自然、多变的响应。选出一个字后，加进序列，对下一个字重复整个流程。

---

## Claude 何时停止生成

每产出一个 token，Claude 检查几个条件决定要不要继续：

- **Max tokens reached** —— 达到你指定的上限了吗？
- **Natural ending** —— 生成了 end-of-sequence token？
- **Stop sequence** —— 碰到预设的停止短语？

这三种情况在 response 里会产生不同的 `stop_reason`。在应用代码中区分处理，是"健壮集成"和"悄悄截断答案"的差别。

---

## API Response

生成结束后，API 返回结构化 response，内容包含：

| 字段 | 意义 |
|------|------|
| **Message** | 生成的文字 |
| **Usage** | input/output token 数（用于计费和预算追踪） |
| **Stop Reason** | 为什么停止生成（`end_turn`、`max_tokens`、`stop_sequence`、`tool_use`） |

Server 收到后把生成的文字转回 client 应用，最终出现在 UI 上。

---

## 实务上为什么重要

来源列出看懂这个流程的四个好处：

- 设计保护 API key 的安全架构
- 为你的使用场景设适当的 token 上限
- 在代码中处理不同 stop reason
- 通过了解 pipeline 中问题可能发生的位置来 debug

换句话说，生命周期是"出事时你需要的那张地图"。延迟飙高？你可以推断是网络（1-2、4-5 步）还是 model（3 步）。输出被截断？看 stop_reason。账单爆炸？看 usage。没这张地图，每一次故障都只能瞎猜。

---

## 常见错误

1. **从 client code 直接调 Anthropic API** —— 泄漏 API key；来源明确说这绝对不行。
2. **不处理不同 stop reason** —— 把所有 response 当自然结束，会悄悄掩盖 `max_tokens` 截断。
3. **忽略 usage 字段** —— 账单爆炸是必然的，per-user 预算也坏掉。
4. **写死 model 名称** —— model 升级会很痛苦；应通过环境变量配置。
5. **忘了 max_tokens** —— 不设上限的请求会带来未预期的成本和延迟。
6. **误把 tokenization 当 word split** —— token 可能是子字、空白或符号；"一字 ≈ 一 token"是直觉，不是规则。

> **关键洞察**
>
> Request lifecycle 是让 CCA 课纲中所有其他主题变得可理解的心智模型。Tool use、streaming、caching、agents —— 它们全都是这五步流程的变体。记熟一次，每个进阶模式都变成"这一步，稍作修改"。跳过这步，每一种失败模式都像魔法。

---

## CCA 考试相关性

- **D1（Agentic Architecture）**：生命周期是所有 agentic 模式的基础。会考"X 发生在 request flow 的哪一步？"
- **D5（Enterprise Deployment）**：安全架构（server 介于 client 和 API）、token 预算、stop-reason 处理是生产部署必备。
- 注意："为什么 client 和 Anthropic 之间要有 server？"→ API key 安全性。"Claude 内部做什么？"→ tokenize、embed、contextualize、generate。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Claude request lifecycle 的五个步骤是什么？ | Request to server → request to Anthropic API → model processing → response to server → response to client。 |
| 为什么 request 一定要走你自己的 server，不能从 client 直接发？ | Client-side 的 API key 可以被挖出来，造成严重信息安全漏洞，让任何人发未授权请求。 |
| 每个 API request 必须包含哪四个核心字段？ | API Key、Model、Messages、Max Tokens。 |
| Claude 内部处理的四个阶段是什么？ | Tokenization、embedding、contextualization、generation。 |
| 什么是 tokenization？ | 把输入文字切成更小的 chunk（整字、字的一部分、空格或符号），叫 token。 |
| 什么是 embedding？ | 代表一个 token 所有可能意义的长串数字 —— 数值化的定义。 |
| Contextualization 做什么？ | 根据周围字词调整每个 embedding，决定当前情境下最可能的意义。 |
| 为什么 Claude 不永远挑最高概率的下一个字？ | 它混用概率和受控的随机性，产生自然、多变的响应。 |
| 哪三个条件让 Claude 停止生成？ | 达到 max tokens、自然结束（end-of-sequence token）、或碰到预设的 stop sequence。 |
| API response 含哪三个字段？ | Message（生成的文字）、Usage（input/output token 数）、Stop Reason（停止原因）。 |
| 为什么懂生命周期有助于 debug？ | 让你能定位故障发生在哪一环 —— 网络、认证、model 处理、或 response 处理。 |
