# Rules of Prompt Caching — Engineering Deep Dive（简体中文）

| 项目 | 详情 |
|------|------|
| 考试领域 | D5 — Enterprise Deployment (20%) 主要；D2 — Tool Design (18%) 次要 |
| Task Statements | 5.1（成本／延迟优化）、5.2（生产性能）、2.1（tool schema 设计） |
| 来源 | building-with-the-claude-api / 06-extended-features / Lesson 57 |

---

## One-Liner

Prompt caching 只有在你遵守规则时才有用：必须手动加 cache breakpoint、cached 内容必须逐字节相同、breakpoint 之前至少要有 1024 tokens、每次请求最多 4 个 breakpoint。

---

## Cache 不是自动的——要加 Breakpoint

Caching 默认**不**启用。你必须在请求里的某个 block 上明确加上 **cache breakpoint** 才会触发。

运行原则：

- Message 上的处理工作**不会被自动缓存**。
- 你要手动在某个 block 上加 `cache_control` 字段。
- 该 breakpoint **之前与包含本身** 的所有内容会被缓存。
- 后续请求只有在到 breakpoint 为止的内容**完全一致**时才能读取 cache。

换句话说，breakpoint 就是一条「切线」：上面的是可缓存的前缀，下面的每次都是新的、要重新 preprocess。

---

## 必须使用 Longhand Block 形式

Message 的简短形式（纯字符串）没有地方放 `cache_control`。你必须用 **longhand block 形式**：

```python
# Shorthand — 无法缓存
messages = [{"role": "user", "content": "这是一份长文档..."}]

# Longhand — 可以缓存
messages = [{
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": "这是一份长文档...",
            "cache_control": {"type": "ephemeral"},
        }
    ],
}]
```

`cache_control` 字段值设为 `{"type": "ephemeral"}`。`ephemeral` 是目前支持的缓存类型，对应 lesson 56 的 1 小时 TTL。

---

## 逐字节精确匹配

Cache 非常敏感。到 breakpoint 为止的内容必须在后续请求中**完全一致**才能复用。

即使很小的改动都会使 cache 失效：

- 多加一个「please」→ cache miss。
- 改一个空白字符 → cache miss。
- 把两句话顺序调换 → cache miss。

只要前缀一变，Claude 就得从分歧点开始重新 preprocess，你还要再付一次 cache write 的费用。

**设计启示：** 稳定内容放前面，可变内容放后面。用户当下的问题应该放在 breakpoint **之后**，绝对不要放进缓存前缀里。

---

## 跨消息 Caching

Cache breakpoint 可以横跨多条 message，也可以跨不同 message 类型。如果你把 breakpoint 放在较靠后的 message 上，**所有前面的 message**（user、assistant 等）都会被纳入 cached 内容。

这对对话型 agent 特别有用：你可以把到某个稳定点为止的整个对话历史都缓存下来，然后后面继续 append 新回合。

---

## 可缓存的 Block 类型

不限于 text block。Cache breakpoint 可以加在：

- System prompts
- Tool definitions
- Image blocks
- Tool use blocks
- Tool result blocks

System prompt 和 tool definition 是**最佳**候选，因为它们在不同请求之间几乎不变，通常也是缓存收益最大的地方。

---

## Cache Ordering：Tools → System → Messages

Claude 在幕后按固定顺序处理请求的各个组件：

1. **Tools**（如果有）
2. **System prompt**（如果有）
3. **Messages**

这个顺序决定了什么会被缓存到哪。如果你第一个 breakpoint 放在 messages 区，Claude 仍会把 tools 和 system prompt 视为 cached 前缀的一部分，因为它们在处理顺序上排在前面。

每个请求最多可以放 **4 个 cache breakpoint**。常见的生产 layout：

- Breakpoint 1 → tools 末尾（缓存所有 tool schemas）
- Breakpoint 2 → system prompt 末尾（缓存 system prompt）
- Breakpoint 3 → message history 某处（缓存稳定的对话前缀）
- Breakpoint 4 → 保留给更细粒度的缓存

细分 breakpoint 让请求不同段可以各自独立缓存——某段变了只失效那一段，不会整份 cache 打翻。

---

## 最小内容长度：1024 Tokens

有一条底线：**breakpoint 之前与含本身的内容总和至少要 1024 tokens** 才会被缓存。

- 一句短短「Hi there!」跨不过这个门槛。
- 你需要真的大的内容——长 system prompt、完整文档、或详尽的 tool schema——才能触发 caching。
- 1024 token 是所有要 cache 的 block **总和**，不是单个 block。

不到门槛时 `cache_control` 等于 no-op：不会建 cache，也不会省钱。

---

## Common Mistakes

1. **用 shorthand 字符串形式** — 没地方放 `cache_control`，什么都不会被缓存。先改成 longhand block 形式。
2. **把可变内容放在 breakpoint 之前** — 用户的新问题绝对不能放进 cached 前缀里，否则每次都 miss。
3. **低于门槛就想缓存** — 想缓存小于 1024 tokens 的 prompt 还期待省钱。它会静默什么都不做。
4. **超过 4 个 breakpoint** — 请求会被拒绝。设计时要抓住 4 个名额的预算。
5. **不懂处理顺序** — 把 breakpoint 放在 messages 上却心理假设 tools 区「没被缓存」。它被缓存了——tools 和 system prompt 在处理顺序上排前面，永远是 message 层级前缀的一部分。
6. **依赖 fuzzy matching** — Caching 是逐字节精确。先规范化空白、标点、顺序，再说前缀是稳定的。

---

> **Key Insight**
>
> 定义缓存成败的四条规则：(1) 用 breakpoint 明确 opt in、(2) 逐字节比对、(3) 达到 1024 token 底线、(4) 遵守 tools → system → messages 的顺序与 4 breakpoint 上限。任一条没达成，cache 就静默没用——更糟的是你还为永远不会被复用的内容付了 cache write。

---

## CCA Exam Relevance

- **D5（Enterprise Deployment）** — 考题会测你是否知道 caching 是手动、逐字节、1024 token 底线。
- **D2（Tool Design）** — tool definition 是 caching 的头号目标，因为它跨请求稳定；考题可能问「tool 量大的 workflow 要把 breakpoint 放哪？」
- 记住处理顺序：tools、system prompt、messages。这顺序直接对应「我该先缓存什么？」
- 4 个 breakpoint、`{"type": "ephemeral"}`、1024 token 底线——这些是常考数字。

---

## Flashcards

| Front | Back |
|-------|------|
| Prompt caching 是自动的吗？ | 不是——必须手动在请求的某个 block 上加 `cache_control` 字段（cache breakpoint）。 |
| `cache_control` 填什么值？ | `{"type": "ephemeral"}`——目前支持的缓存类型，对应 1 小时 TTL。 |
| 哪种 message 形式支持 cache breakpoint？ | Longhand block 形式（`content` 是 block 的 list）。Shorthand 字符串形式无法携带 `cache_control`。 |
| 放了 breakpoint 后 Claude 会缓存多少内容？ | Breakpoint 之前与包含本身的所有内容。 |
| Follow-up 调用时 cached 内容要完全一样吗？ | 要——逐字节相同。加一个「please」都会失效。 |
| 可缓存前缀的最小 token 数是多少？ | 1024 tokens（breakpoint 之前与含本身的所有 block 总和）。 |
| 一个请求最多放几个 breakpoint？ | 最多 4 个。 |
| Claude 处理请求组件的顺序是什么？ | 先 tools、再 system prompt、再 messages。 |
| 哪些是最佳缓存候选？为什么？ | System prompt 与 tool definition——它们跨请求很少变动，通常是最大的稳定输入块。 |
| 后面的 message 上放 breakpoint 可以缓存前面的 message 吗？ | 可以——跨消息缓存会把 breakpoint 之前所有 message（user、assistant 等）都纳入。 |
