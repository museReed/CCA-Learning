# Prompt Caching in Action — Engineering Deep Dive（简体中文）

| 项目 | 详情 |
|------|------|
| 考试领域 | D5 — Enterprise Deployment (20%) 主要；D2 — Tool Design (18%) 次要 |
| Task Statements | 5.1（成本／延迟优化）、5.2（生产性能）、2.1（tool schema 设计） |
| 来源 | building-with-the-claude-api / 06-extended-features / Lesson 58 |

---

## One-Liner

实战上的 prompt caching 就是：把 tools list 和 system prompt 转成可缓存的 longhand block 形式并加上 `cache_control`，然后看 response 里的 `cache_creation_input_tokens` / `cache_read_input_tokens` 去验证命中与写入。

---

## 真实 app 中哪里最能省

课程点出三个高价值目标：

- **大型 system prompt** — 例如约 6K token 的编程助手 system prompt。
- **复杂 tool schema** — 例如约 1.7K tokens 的多个 tool 定义。
- **重复的 message 内容** — 持续重发相同前缀的对话或 workflow。

原则：caching 只在你重复发送一模一样的内容时才有用——而在许多真实 app 中，这种情况**极其频繁**。

---

## Tool Schema Caching 的设置

要缓存 tool schema，把 `cache_control` 加到 **list 的最后一个 tool**。这个 tool 之前（包括本身）的所有东西都会被缓存。

```python
if tools:
    tools_clone = tools.copy()
    last_tool = tools_clone[-1].copy()
    last_tool["cache_control"] = {"type": "ephemeral"}
    tools_clone[-1] = last_tool
    params["tools"] = tools_clone
```

为什么要先 copy 再改：

- `tools.copy()` 创建 tools list 的浅拷贝，不会影响调用方的原始 list。
- `tools_clone[-1].copy()` 创建最后一个 tool dict 的浅拷贝，原来那个保持干净。
- 只有拷贝会被加上 `cache_control`。

你**也可以**直接写 `tools[-1]["cache_control"] = ...`，但 copy 的做法能避免之后重排 tool、跨调用共用 list、或 app 不同部分共享 tool 定义时出现的诡异 bug。

`cache_control` 值设为 `{"type": "ephemeral"}`——标准的 1 小时 cache 类型。

---

## System Prompt Caching 的设置

System prompt 要从纯字符串转成 longhand 结构化 block 形式，才有地方放 `cache_control`：

```python
if system:
    params["system"] = [
        {
            "type": "text",
            "text": system,
            "cache_control": {"type": "ephemeral"},
        }
    ]
```

字符串形式的 system prompt 没有字段能放 `cache_control`；block 形式有。一旦把 system prompt 这样结构化，整个 system prompt 就会成为 cached prefix 的一部分。

---

## 从 Response 读取 Cache 行为

启用 caching 后，API 的 `usage` block 会新增几个 token 计数器，告诉你这一次是写入还是读取 cache：

| 字段 | 含义 |
|------|------|
| `cache_creation_input_tokens` | 这次请求 Claude **写入** cache 的 token 数（第一次或 cache miss 被迫重写）。 |
| `cache_read_input_tokens` | 这次请求 Claude 从 cache **读取** 的 token 数（命中——省钱事件）。 |

常见模式：

- **第一次请求**：`cache_creation_input_tokens=1772`、`cache_read_input_tokens=0`——正在写入 cache。
- **后续请求，内容相同**：`cache_creation_input_tokens=0`、`cache_read_input_tokens=1772`——正在读取 cache。
- **内容改变**：改过的段会产生新的 `cache_creation_input_tokens`，因为那段还不在 cache 里。

Cache **极度敏感**：tools 或 system prompt 改一个字符就会让那个组件的整份 cache 失效。

---

## Cache Ordering 与部分命中

你可以在单个请求里设置多个 cache breakpoint。Claude 的处理顺序是固定的：

1. **Tools**（如果有）
2. **System prompt**（如果有）
3. **Messages**

这个顺序让**部分命中**成为可能。假设你改了 system prompt 但 tools 没动：

- Tools 仍然逐字节一致 → tools 段 **cache read**。
- System prompt 不同 → 新的 system prompt **cache write**。
- Messages 正常处理。

你只为真的改变的部分付费。这种细粒度缓存是本功能最大的优点之一：它是渐进失效，而不是全有全无。

---

## 实用考量

Prompt caching 在以下情况最有效：

- **Tool schema 跨请求一致** — 带稳定工具箱的生产 agent。
- **System prompt 稳定** — 锁定的 persona 与指令。
- **App 会发出多个带相似 context 的请求** — 聊天、迭代工作流、批量 eval。

记住：cache 只活一小时。这个设计是给**相对高频的 API 使用**，不是长期存储。如果你的产品每几小时才调用一次，cache 会在调用间过期，你会不断付 cache write 却没拿到 read 的好处。

---

## Common Mistakes

1. **原地修改调用方的 tool list** — 直接写 `tools[-1]["cache_control"] = ...` 可能悄悄影响 app 其他地方共用的同一份 list。用 copy-then-assign 模式。
2. **System prompt 继续用纯字符串** — 字符串没地方放 `cache_control`。必须包进 `{"type": "text", "text": ..., "cache_control": ...}` block。
3. **以为整个请求是一个 cache 单元** — 它不是。Tools、system prompt、messages 按处理顺序各自独立缓存，你可以拿到部分命中。
4. **生产没检查 `usage` 字段** — 不监控 `cache_creation_input_tokens` 对 `cache_read_input_tokens`，你根本不知道 cache 有没有真的在用。
5. **对 cached 段做琐碎编辑** — tool description 或 system prompt 一个空白、一个标点，就强制 cache 重写。把 cached 段当成有版本、不可变的 asset。
6. **对低频 workload 启用 caching** — Entry 在被复用前就过期，你只付写入、拿不到读取。

---

> **Key Insight**
>
> 实战的 caching 只有三件事：(1) 把最后一个 tool 包上 `cache_control` 以缓存整份 tool schema、(2) 把 system prompt 转成 longhand block 形式以放 `cache_control`、(3) 检查 response 的 `cache_creation_input_tokens` / `cache_read_input_tokens` 验证命中确实发生。处理顺序（tools → system → messages）自然送你部分命中。

---

## CCA Exam Relevance

- **D5（Enterprise Deployment）** — 考题会测哪个 API 字段证明 cache 命中（`cache_read_input_tokens`）、哪个证明 cache 写入（`cache_creation_input_tokens`）。
- **D2（Tool Design）** — 记住 `cache_control` 放在 list 的**最后一个** tool，由于处理顺序，它会把前面所有 tools 都纳入 cache。
- 记住部分命中行为：只改 system prompt 时 tools 的 cache 会保留，usage 会呈现 split 模式（tools 读、system 写）。
- 「extremely sensitive」的逐字节比对是常考警语——任何编辑都会失效。

---

## Flashcards

| Front | Back |
|-------|------|
| 哪个 API response 字段告诉你这次请求写入了 cache？ | `cache_creation_input_tokens`——Claude 刚刚写入 cache 的 token 数。 |
| 哪个 API response 字段告诉你这次请求读取了 cache？ | `cache_read_input_tokens`——Claude 从 cache 复用的 token 数。 |
| `cache_control` 要加在 tools list 的哪里才能缓存整份 tools？ | 放在 list 的**最后一个** tool 上。由于 tools 最先被处理，它前面（含本身）的所有东西都会成为 cached prefix。 |
| 为什么要 copy tools list 和最后一个 tool 再加 `cache_control`？ | 避免修改调用方原本的 list 或原本的 tool dict，防止重排 tool 或其他地方共享时出现 bug。 |
| System prompt 怎么变成可缓存的？ | 把字符串换成 longhand block 形式 `[{"type": "text", "text": ..., "cache_control": {"type": "ephemeral"}}]`。 |
| 1 小时缓存用的 `cache_control` 值是什么？ | `{"type": "ephemeral"}` |
| Tools、system prompt、messages 的 caching 处理顺序是什么？ | 先 tools、再 system prompt、再 messages。 |
| 只改 system prompt 时 cache 会发生什么？ | 部分命中：tools 拿到 cache read（没变），新的 system prompt 拿到 cache write。 |
| Caching context 下「extremely sensitive」是什么意思？ | 任何 cached 段的改动——哪怕一个字符——都会让 cache 失效，强制重写。 |
| 为什么 caching 不适合长期、低频 workload？ | 因为 cache 只存活一小时，调用之间就过期，你只付 cache write 却永远拿不到 read。 |
