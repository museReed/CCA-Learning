# The StreamableHTTP Transport — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%) |
| Task Statements | 2.1 (MCP transport 选择), 2.4 (远程 server 配置) |
| Source | model-context-protocol-advanced-topics / 03-transports / Lesson 12 |

---

## One-Liner

StreamableHTTP 让你的 MCP server 上网，但就像从私人办公室搬到公共柜台 — 增加了可及性，却失去了主动找人的能力。

---

## 柜台类比

- **Stdio** = 私人办公室。你和同事面对面坐着，任何人都能随时发起对话。
- **StreamableHTTP** = 服务柜台。访客（client）可以走过来提问，但柜台人员（server）**不能离开柜台**去找访客 — 必须等人来。

这是 HTTP 的根本限制：**server 只能回应，不能主动发起**。

---

## 对产品的意义

### 仍然可用的功能（Client-Initiated）

| 功能 | 用户体验 |
|------|----------|
| Tool call | 用户问 AI，AI 调用 server 工具 — 完美运作 |
| Resource read | AI 从 server 获取数据 — 完美运作 |
| Prompt template | AI 从 server 加载模板 — 完美运作 |

### 有风险的功能（Server-Initiated）

| 功能 | 失去什么 | 产品影响 |
|------|---------|---------|
| Sampling（CreateMessage） | Server 无法请求 AI 生成文字 | 无 server 端 AI 推理 |
| Progress notification | Server 无法报告「完成 50%...」 | 用户在长任务中看不到进度 |
| Logging | Server 无法推送调试消息 | Production 更难排查问题 |
| Root listing | Server 无法问「开了哪些文件？」 | 无 workspace 感知功能 |

> 💡 **Key Insight**
> 如果你的产品路线图包含 **server 需要向 client 提问**的功能（如「批准这个操作？」或「应该用哪个文件？」），启用限制性设置的 StreamableHTTP 会阻挡这些功能。

---

## 两个配置开关

把它们想成基础架构团队可以设置的**限制等级**：

| 设置 | 关闭（默认） | 开启 | 商业影响 |
|------|------------|------|---------|
| `stateless_http` | Server 记住每个 client session | Server 将每个请求视为独立 | 更容易扩展，但失去进度追踪和 server-initiated 功能 |
| `json_response` | Server 可以逐步流式传输结果 | Server 最后才一次返回 | 基础架构更简单，但用户等待更久 |

### 限制光谱

```
最多功能 ◄──────────────────────────────► 最简单架构

两者都关        stateless 开      json 开         两者都开
（默认）        或 json 开       或 stateless     （最大限制）
```

---

## PM 决策矩阵

| 商业需求 | 建议设置 |
|---------|---------|
| 「需要实时进度条」 | 两个标志都关（默认） |
| 「需要扩展到一万用户」 | `stateless_http=true`（接受功能损失） |
| 「简单的 webhook 风格集成」 | 两个标志都开 |
| 「Server 需要调用 AI 模型」 | 两个标志都关 + SSE 设置 |
| 「只需要基本工具访问」 | 任何配置都行 |

---

## 利益相关者沟通的核心取舍

| 维度 | Stdio | StreamableHTTP（默认） | StreamableHTTP（限制） |
|------|-------|----------------------|---------------------|
| 部署 | 仅限本地 | 远程/云端 | 远程/云端 |
| 可扩展性 | 单一用户 | 中等 | 高 |
| 功能覆盖 | 100% | ~80%（有 SSE workaround） | ~50% |
| 基础架构复杂度 | 最低 | 中等 | 低 |

---

## CCA 考试重点

- **情境题**：「Web 应用的远程 MCP server」→ StreamableHTTP。然后检查场景需要哪些功能来决定标志设置。
- **取舍题**：知道每个限制等级确切失去哪些功能。
- **标志默认值**：都是 `false` — 这是常考的。启用是限制而非增强。
- **方向不要搞混**：Client→server 永远可用。只有 server→client 受影响。

---

## Flashcards

| Front | Back |
|-------|------|
| 用商业术语描述 StreamableHTTP 的功能？ | 远程 MCP server 托管 — server 可以在云端，通过网络服务用户 |
| HTTP 对 MCP 的根本限制是什么？ | Server 无法主动发起通信 — 只能回应 client 请求 |
| 哪些产品功能需要 server-initiated request？ | 进度条、人工审批流程、server 端 AI 推理（sampling） |
| 两个标志的默认值是？ | `stateless_http` 和 `json_response` 都默认为 `false`（最少限制） |
| 开启 `stateless_http` 会怎样？ | Server 忘记 session — 更容易扩展但失去进度追踪和 server-initiated 功能 |
| 开启 `json_response` 会怎样？ | 无 streaming — server 一次返回完整结果而非逐步更新 |
| PM 何时应该接受功能取舍？ | 当可扩展性或基础架构简洁性比 server-initiated 功能更重要时 |
| 不管标志怎么设，哪些功能永远可用？ | Client-initiated 功能：tool call、resource read、prompt template 获取 |
