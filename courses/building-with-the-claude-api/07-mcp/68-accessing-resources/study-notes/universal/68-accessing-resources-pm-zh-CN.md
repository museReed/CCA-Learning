# Accessing Resources — PM Perspective（简体中文）

| 项目 | 说明 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration（18%）主；D1 — Agentic Architecture（22%）次 |
| Task Statements | 2.3（client 端 MCP resource 使用）、1.2（context 注入） |
| Source | building-with-the-claude-api / 07-mcp / Lesson 68 |

---

## One-Liner

Accessing resources 是让"@mention"变成产品功能的那块 MCP：应用向 server 请求被引用的数据，直接塞进 prompt 交给 Claude——零 tool call、零猜测、可预测的延迟与成本。

---

## 心智模型：给 Claude 一个打开的文件夹

- **Tool call** 是给 Claude 一张地图，希望它走到正确的大楼。知道路就快，不知道就慢又容易错
- **Resource access** 是直接把文件夹打开摆在 Claude 面前，Claude 立刻就能读，不绕路、不用决定

当用户明确指出要用什么（"用这份文档"、"看这条记录"），resource access 几乎总是对的 pattern。

---

## 为什么 PM 要关心

"@mention"做成 tool 和做成 resource，实际表现差异非常大：

| 指标 | Tool call 路径 | Resource access 路径 |
|------|---------------|---------------------|
| 每条用户消息的 API round trip | 2+ | 1 |
| 延迟开销 | 每多一轮 ~1.5–3 秒 | 几乎 0（在 Claude 调用前完成） |
| Token 成本 | tool schema + tool_use + tool_result + 最终答案 | 只有注入的内容 |
| 可靠性 | 依赖 Claude 正确决策 | 确定性 |
| UX | "thinking..."转圈更久 | 响应更利落 |

用 resource access 上线的功能，立即就比较快且便宜——不用再调 prompt。

---

## 产品场景

### 什么时候用 Resource Access

| 用户体验 | 为什么适合 |
|---------|-----------|
| @mention 文档 / 记录 / ticket | 用户明确指定要包含什么 |
| Always-on context（公司政策、术语表） | 每次都要带 |
| "总结这一页"带页 ID 选择器 | 确定性查询、无需 Claude 决策 |
| File picker → 注入 | 应用知道是哪个文件，无歧义 |

### Resource Access 不够时

| 用户需求 | 更适合的 pattern |
|---------|-----------------|
| 对话中途让 Claude 决定是否查更多 | Tool call |
| 跨多个项目搜索 | Tool call 带 query |
| 按推理决定是否 fetch | Tool call |
| 有副作用的动作 | Tool call（绝不是 resource） |

---

## PM 决策框架

对任何"抓取并显示"的功能问自己：

| 问题 | 若 Yes | 意义 |
|------|--------|------|
| 用户指定要抓哪个项目？ | Yes | Resource access |
| 候选集合在 UI 构建时就已知？ | Yes | Resource access（可用 dropdown / autocomplete） |
| 希望这个意图永远触发 fetch？ | Yes | Resource access |
| 希望 Claude 可以跳过 fetch？ | Yes | Tool call |
| fetch 需要搜索或排序？ | Yes | Tool call（Claude 带 query） |

---

## 需要设计的 UX 层面

因为 resource access 在 **Claude 调用之前** 发生，UX 负担落在你的应用本身：

- **Discovery** — 用户怎么知道有 resource 可用？（@ autocomplete、slash menu、file picker）
- **Selection affordance** — dropdown vs 模糊搜索 vs 命令输入
- **进度提示** — resource fetch 仍有延迟，要放低调 loader
- **错误状态** — URI 失败时显示"该文档不可用"
- **Preview** — 让用户在提交前看到将注入什么（可选但体验好）

这完全是产品设计，不是 prompt engineering，设计师负责。

---

## 成本与 Context Window

Resource access 单次 API 调用便宜，但 token 不是免费——注入内容会占 prompt 空间。PM 要预算：

- **大文档** — 能否放进 context window？要定 truncation 或 chunking 规则
- **多 resource 同时** — 用户若能 @mention 多项，总量可能爆炸，要设上限
- **数据陈旧** — 内容是某时点快照，要决定每轮是否重抓
- **log 中的敏感数据** — 注入内容会流经 telemetry，要决定 redaction

---

## PM 常见错误

1. **把 @mention 做成 tool call** — 能用但慢一倍、贵一倍，用户没有任何好处
2. **让 resource 无上限增长** — 把 50 页 PDF 每轮都注入会烧爆 context 与延迟，要设上限
3. **没设计 resource discovery UX** — 用户找不到的 resource 等同于不存在
4. **忘记错误状态** — resource 可能失败（不存在、无权限、太大），UI 必须处理
5. **跳过 preview affordance** — 让用户看到将注入什么能提升信任，减少"Claude 为什么这样说？"的客诉

> **Key Insight**
>
> Resource access 是让"用户驱动的 context"变得无感的 pattern。用户视角："我 mention 了一个文件，Claude 读了"。架构视角：一次 API 调用而不是两次、确定性的内容、清晰切分"应用抓什么"与"Claude 推理什么"。对 PM 而言，这是设计 context 丰富的 Claude 功能时最高杠杆的 pattern。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：要知道 resource access 在 MCP client 内（如 `read_resource`），在 Claude 调用之前执行，不是 tool loop 的一部分
- **D1（Agentic Architecture）**：Resources 把 context 预先注入，缩短 agent loop
- 考题模式："用户 @mention 一份文档，文档内容怎么到 Claude？" → client 抓 resource 后 inline 进 prompt，不是 tool call

---

## Flashcards

| Front | Back |
|-------|------|
| "文件夹 vs 地图"的比喻？ | Tool call 给 Claude 一张地图希望它找到数据；resource access 直接把文件夹打开摆在 Claude 面前 |
| 为什么 resource access 比 tool call 做 @mention 便宜？ | 一次 API round trip 而非两次、总 token 更少、不用等 Claude 决定是否抓 |
| 谁负责 resource discovery 的 UX？ | 你的产品 / 设计团队——用户看到的 @ autocomplete、file picker、slash menu |
| Resource access 仍有什么成本？ | 注入内容占 prompt token，可能逼近 context window |
| 什么时候 tool call 比 resource 好？ | 需要 Claude 判断是否抓、需要 search、或操作有副作用时 |
| @mention 功能的 PRD 要包含什么？ | mention 数量与大小上限、resource 失败的 fallback UX、preview 机制、延迟预算、注入内容的隐私规则 |
| 为什么 resource access 比 tool call 更确定？ | 应用保证 fetch 一定发生，Claude 不会决定、不会跳过 |
| Resource-based 流程中，Claude 被调用前发生了什么？ | 应用通过 MCP client 抓 resource 并 inline 进正在组装的 prompt |
