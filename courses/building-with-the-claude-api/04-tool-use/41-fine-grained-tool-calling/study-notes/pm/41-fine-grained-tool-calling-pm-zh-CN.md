# Fine-Grained Tool Calling — PM Perspective

| 项目 | 内容 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration (18%)、D5 — Enterprise Deployment (20%) |
| Task Statements | 2.1（tool schema 与选择）、5.2（streaming 与响应速度） |
| Source | building-with-the-claude-api / 04-tool-use / Lesson 41 |

---

## One-Liner

Fine-grained tool calling 让产品可以让用户实时看到 AI "一个字一个字敲出" tool 参数的过程——代价是工程端必须更仔细处理可能暂时不合法的 JSON。

---

## Mental Model：现场即时字幕 vs. 完整字幕

| 模式 | 类比 | 用户体验 |
|------|------|---------|
| 默认 streaming | 每次一整句才出现的电视字幕 | 停顿后整句浮出 |
| Fine-grained | 一个字一个字即时敲出的现场听打 | 平滑实时,但偶尔会闪过错字 |

同样的 trade-off 套用在 tool 参数 streaming:默认感觉像爆发、fine-grained 感觉像 live feed——但 live feed 可能瞬间出现稍后会被修正的乱码。

---

## 为什么对产品重要

Tool 参数生成可能很长。如果 tool 接收一篇 2,000 字的文章或一张详细的 JSON 表单,Claude 要花好几秒组装。这段时间内用户什么都看不到——除非你 stream。

Fine-grained tool calling 是下列三者的差别：

- **"点击 Generate、等 8 秒、内容出现"**（不 stream）
- **"点击 Generate、内容随主要字段完成而分批出现"**（默认 streaming）
- **"点击 Generate、看到光标在即时敲出结果"**（fine-grained）

对内容生成型 UX（写作、起草、表单填写）,第三种通常明显更好。

---

## Product Use Cases

### 适合 Fine-Grained 的场景

| 场景 | 为什么有价值 |
|------|-------------|
| 有预览面板的 AI 写作工具 | 用户想看到草稿慢慢浮现 |
| 长文 email 生成器 | 显著降低感知延迟 |
| 多字段的实时表单 autofill | 每个字段完成就立即渲染 |
| 带可视编辑器的 code generation | 像人类协作者的实时打字感 |
| 长结构化报告（多段） | 用户可以边读前段边等后段生成 |

### 默认模式更合适

| 场景 | 为什么保留默认 |
|------|---------------|
| 短小的原子 tool call（< 1 秒） | Buffering 看不出来,fine-grained 的复杂度白花 |
| 没人看的后台自动化 | 没人看 stream,不用付延迟代价 |
| 合规关键流程 | 你想保留服务器端验证的安全网 |
| 单一错值就让下游坏掉的 tool | 部分/无效 JSON 风险太高 |

---

## PM Decision Framework

| 问题 | 如果 Yes | 行动 |
|------|---------|------|
| 有用户正在看响应渲染吗？ | Yes | 考虑 streaming |
| Tool 参数生成超过 3 秒吗？ | Yes | Streaming 有价值 |
| 默认 streaming 明显卡卡的吗？ | Yes | 考虑 fine-grained |
| 工程端能加完整的 JSON 错误处理吗？ | Yes | Fine-grained 可以安全使用 |
| 这个 tool 对畸形输入零容忍吗？ | Yes | 保留默认 |

---

## 隐藏成本：工程复杂度

Fine-grained tool calling 不是一个免费的"加速"开关,它把责任从 Anthropic 服务器搬到你的代码：

- JSON 验证 → 搬到 client
- 错误恢复 → 搬到 client
- Schema 一致性检查 → 搬到 client
- 边缘情况（null、undefined、断开的字符串）处理 → 搬到 client

PM 提议启用 fine-grained 时必须把这些工程工作算进预算。草率上线会带来比默认模式更糟的 UX（用户在 live feed 上看到 crash）。

---

## 应该追踪的指标

上线后需要埋点以下项目：

1. **首个可见 token 的时间** — 使用 fine-grained 的主要理由,应该显著下降
2. **Tool 执行成功率** — 应该维持;如果下降,代表 JSON 处理有 bug
3. **Client 端 parse 错误率** — fine-grained 下会是非零,应随处理成熟而下降
4. **端到端完成时间** — 可能不会变快;fine-grained 主要改善"感知延迟"
5. **生成期间的用户参与度** — 是否更愿意停留在页面？真正的 UX 胜面

---

## Common PM Mistakes

1. **以为 fine-grained 就是全部变快** — 端到端时间通常一样,改善的是感知延迟而不是吞吐量。
2. **没写 JSON 错误处理就上 fine-grained** — 用户会看到 live feed 没错,也会看到 malformed chunk 造成的 crash。
3. **在短 tool call 上用 fine-grained** — 复杂度多了、UX 几乎没差。
4. **没埋点 parse 错误率** — 没有这个指标,你根本不知道自己的处理有没有效。
5. **把 fine-grained 跟 "Claude 变快" 混为一谈** — 它只影响 streaming 中 tool 参数的投递,不影响模型生成速度。

> **Key Insight**
>
> Fine-grained tool calling 是感知延迟的杠杆,不是吞吐量的杠杆。在用户正在看长时间 tool 生成、且工程端能投入完整 JSON 处理时才启用。CCA 考试要记得:trade-off 是"client 端 JSON 验证责任"换"chunk 立即投递"。

---

## CCA Exam Relevance

- **D2 (Tool Design)**：理解 fine-grained 会关闭 streaming 期间服务器的 JSON 验证,client 必须处理错误。
- **D5 (Enterprise Deployment)**：Streaming 是核心 UX 杠杆,fine-grained 是其中最激进的设定。
- 题目可能描述一个 UX 问题（"tool streaming 感觉一阵一阵"）并问是哪个设定控制的。

---

## Flashcards

| Front | Back |
|-------|------|
| Fine-grained tool calling 的用户可见效果是什么？ | Tool 参数以逐 token 实时串流出现,而不是一阵一阵地 burst |
| 默认 tool-use streaming 感觉像什么？ | 停顿后爆发——每个 burst 对应一个验证过的最外层 key |
| Fine-grained 的主要工程成本是什么？ | Client 必须在 streaming 中 graceful 处理无效 / 部分 JSON |
| PM 什么时候应该选 fine-grained？ | 长时间 tool 生成、用户正在看响应浮现、且工程端能投入 JSON 错误处理 |
| 哪一个指标在 fine-grained 之后最会改善？ | 首个可见 token 的时间——感知延迟 |
| 启用 fine-grained 之后哪个指标不应该变差？ | Tool 执行成功率——parse bug 会在这里浮现 |
| Fine-grained streaming 最好的类比？ | 一个字一个字的现场听打,相对于整句才出现的电视字幕 |
| 什么时候 fine-grained 是白花复杂度？ | 短 tool call、后台自动化,或不能容忍畸形输入的关键 tool |
