# Fine-Grained Tool Calling — Engineering Deep Dive

| 项目 | 内容 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%)、D5 — Enterprise Deployment (20%) |
| Task Statements | 2.1（tool schema 与选择）、2.4（多轮 tool loop）、5.2（streaming 与响应速度） |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 41 |

---

## One-Liner

Fine-grained tool calling 是一个可选的 streaming 模式,会关闭服务器端对 tool 参数的 JSON 验证,让你能实时收到 tool_use 的部分 JSON chunk,代价是你必须自己处理非法 JSON。

---

## 背景：Tool Use + Streaming

对带有 tool 的 messages 请求启用 streaming 后,Claude 会在生成过程中发出事件：

- `ContentBlockStart` / `ContentBlockStop`
- `ContentBlockDelta` — 普通文本生成
- `InputJsonEvent` — 专属于 tool_use block,传递部分 JSON

每个 `InputJsonEvent` 都带两个关键属性：

| 属性 | 含义 |
|------|------|
| `partial_json` | 代表 tool 参数某一段的 JSON chunk |
| `snapshot` | 到目前为止所有 chunk 累积后的 JSON |

```python
for chunk in stream:
    if chunk.type == "input_json":
        print(chunk.partial_json)     # 增量片段
        current_args = chunk.snapshot # 当前累积结果
```

---

## 默认行为：Buffered Validation

默认情况下,Anthropic API **不会**把 Claude 生成的每个 token 立刻往 client 推,而是在服务器端把 chunk 先 buffer 起来、对照你的 tool schema 做验证之后才 flush 出去。验证单位是**最外层的 key-value pair**。

假设 tool schema 期望的结构是：

```json
{
  "abstract": "This paper presents a novel...",
  "meta": {
    "word_count": 847,
    "review": "This paper introduces QuanNet..."
  }
}
```

API 的行为：

1. 等整段 `abstract` 的值生成完毕
2. 对该 key-value pair 做 schema 验证
3. 一次发出 `abstract` 所有 buffer 住的 chunk
4. 接着处理 `meta` 对象

这就是为什么 tool-use streaming 感觉起来是**延迟后的爆发**,而不是平滑的逐 token 串流。验证是在保护你,避免把无效或无法使用的部分参数往下游代码送。

---

## 启用 Fine-Grained Tool Calling

Fine-grained tool calling 会**关闭**上述的服务器端验证：

```python
run_conversation(
    messages,
    tools=[save_article_schema],
    fine_grained=True,
)
```

对比效果：

| 方面 | 默认 | Fine-Grained |
|------|-----|--------------|
| JSON 验证 | 有（每个最外层 key-value） | 无 |
| Chunk 发送方式 | 每个有效 key 后的 buffered burst | 立即,逐 token |
| UX 响应速度 | 有延迟感 | 实时感 |
| 可能收到无效 JSON？ | 不会（服务器端处理） | **会 — client 必须处理** |

启用 fine-grained 后,你可能在整个 `meta` 对象还没完成之前就先拿到 `word_count`,可以更早更新 UI 或预处理。

---

## 处理无效 JSON

验证关闭后,Claude 可能发出还不合法的 JSON,比如 `"word_count": undefined` 而不是一个数字。你的 snapshot parser 必须能容忍这种情况：

```python
import json

for chunk in stream:
    if chunk.type != "input_json":
        continue
    try:
        parsed_args = json.loads(chunk.snapshot)
    except json.JSONDecodeError:
        # 部分 / 无效 JSON — 继续累积,不要 crash
        continue
    # 能 parse 成功后,才能安全地使用 parsed_args
```

常见的防御模式：

1. **累积 + 重试** — 尝试 parse snapshot,失败就等下一批 chunk
2. **逐字段抽取** — 用宽松的 regex 或增量 JSON parser 抽出已完成的 key
3. **最终验证** — 当该 tool_use block 的 `ContentBlockStop` 到来时,做一次严格 parse 与 schema check

---

## 什么时候用 Fine-Grained

以下任一情况可以考虑启用：

- 需要**实时显示 tool 参数生成进度**（比如把一篇草稿串流到预览面板）
- 想**提早开始处理部分 tool 结果**以压低端到端延迟
- 默认的 buffering 延迟明显伤害 UX
- 团队有能力投入**完整的 JSON 错误处理**

多数应用用默认（验证）模式就够好。只有当 buffering 造成用户可感知的卡顿时才值得上 fine-grained。

---

## 与 Non-Streaming 的对比

| 模式 | 延迟特征 | 验证 | 复杂度 |
|------|---------|-----|--------|
| Non-streaming | 最后一次响应 | 完整 schema 验证 | 最简单 |
| Streaming（默认） | 最外层 key 之间的 burst | 逐 key 验证 | 中等 |
| Streaming（fine-grained） | 平滑逐 token | 无（交给 client） | 最高 |

用最简单、能满足 UX 的模式。只有 buffering 延迟真的让用户感觉卡,才值得付 fine-grained 的复杂度代价。

---

## Common Mistakes

1. **启用 fine-grained 却没写 JSON 错误处理** — 串流 consumer 会在第一个无法 parse 的 snapshot 就 crash。
2. **把 `partial_json` 当成独立 JSON 文档直接 parse** — `partial_json` 是片段,应该 parse `snapshot`。
3. **把第一个能 parse 的 snapshot 当成最终结果** — snapshot 还会继续增长,要等 tool_use block 的 `ContentBlockStop` 才算结束。
4. **对不能容忍畸形参数的 tool 启用 fine-grained** — 如果下游无法处理 malformed 输入,就保留默认模式。
5. **结束后没做最终 schema 验证** — fine-grained 完全跳过服务器验证,你必须在执行 tool 前自己验一次。

> **Key Insight**
>
> Fine-grained tool calling 是延迟与正确性的 trade-off：用"服务器端 JSON 验证"换"更快、更平滑的 streaming"。默认模式更安全;fine-grained 是在"看得见的串流进度值得在 client 端实现完整 JSON 错误处理"时才用。

---

## CCA Exam Relevance

- **D2 (Tool Design)**：理解 tool 参数 streaming 默认是 buffered、逐 key 验证,并知道如何 opt out。
- **D5 (Enterprise Deployment)**：生产环境 UX 的延迟优化——streaming tool_use 是一个具体杠杆。
- 题目如果描述"tool 参数 streaming 有延迟后爆发的感觉",答案就是 per-key 验证造成的 buffering。

---

## Flashcards

| Front | Back |
|-------|------|
| 哪种事件传递 streaming 中的部分 tool 参数？ | `InputJsonEvent`,带 `partial_json`（增量）与 `snapshot`（累积） |
| 默认 streaming 模式验证什么？ | Tool 参数每一个最外层 key-value pair 对照 schema 验证 |
| `fine_grained=True` 会关掉什么？ | Streaming 过程中服务器端对 tool 参数的 JSON 验证 |
| 为什么默认的 tool-use streaming 会有"爆发感"？ | API buffer chunk 直到一个完整、有效的最外层 key-value pair 完成 |
| Fine-grained tool calling 的主要风险？ | Claude 可能发出无效 JSON,client 必须 graceful 地处理 `json.JSONDecodeError` |
| 什么时候该启用 fine-grained tool calling？ | 当实时 streaming 进度对用户重要,且团队能投入完整 JSON 错误处理 |
| 哪个属性提供当前累积的 JSON？ | `InputJsonEvent` 的 `snapshot` |
| Fine-grained streaming 结束后还必须做什么？ | 做最后一次严格 parse 与 schema check,再执行 tool |
