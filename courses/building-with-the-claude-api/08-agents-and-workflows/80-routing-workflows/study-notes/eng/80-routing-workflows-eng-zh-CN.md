# Routing Workflows — 工程深度解析

| 项目 | 内容 |
|------|------|
| 考试领域 | D1 — Agentic Coding & Architecture(22%)— 主要 |
| 任务陈述 | 1.2(agentic 模式 — routing)、5.2(production workflow 部署)|
| 来源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 80 |

---

## 一句话总结

Routing workflow 用一个分类器 LLM 调用(通常配合 `tool_choice="tool"` 强制工具调用)把进来的请求分类, 再分派到专用下游 pipeline — 它是 LLM workflow 版的 "switch statement"。

---

## Routing 解决的问题

通用 prompt 处理多样化输入时表现不佳。课程示例: 一个社交媒体脚本生成器, 要同时处理 "Python functions"(教育类)和 "surfing"(娱乐类)。单一 script prompt 对两者都产出普通结果。解法是先分类, 再分派到特定类别的 prompt。

Anthropic 在 "Building Effective Agents" 中描述 routing 的适用时机: 当复杂任务有明显类别, 每类都能因为专用处理而受益, *并且*分类可以被 LLM 或确定性算法准确完成。

---

## 标准两步结构

```
用户输入 ──→ [分类器 LLM 调用] ──→ 类别 ──→ [专用 pipeline] ──→ 输出
```

1. **分类** — 把用户请求送给 Claude, 附带预定义类别清单, 要求返回一个类别标签
2. **专用处理** — 用返回的类别查出对应的 prompt template / tool set / 子 workflow, 再产出最终输出

核心观念: 用户输入只会进*一个*专用 pipeline, 不是全部。每个 pipeline 可以独立优化。

---

## 示例类别(课程)

| 类别 | 风格 |
|------|------|
| Entertainment | 高能量、有文化梗、用流行语 |
| Educational | 清楚吸引人的解释配易懂示例 |
| Comedy | 犀利意外的内容, 聪明观察与节奏 |
| Personal vlog | 真诚亲密的对话式叙事 |
| Reviews | 果断、基于体验, 强调优缺点 |
| Storytelling | 沉浸式, 用鲜活细节与情感连接 |

每个类别有自己的专用 prompt, routing 挑对的那个。

---

## 课程的分类 Prompt

```
Categorize the topic of a video into one of the listed categories:
<topic>Python functions</topic>

<categories>
- Educational
- Entertainment
- Comedy
- Personal vlog
- Reviews
- Storytelling
</categories>
```

Claude 回 "Educational", 你的代码就去挑教育类 prompt template。

---

## 用 `tool_choice="tool"` 强制分类

Production 场景中, 分类器应该返回*结构化*类别, 而不是自由文字再自己 parse。CCA 会考的关键技巧是用 tool use 并设 `tool_choice` 强制调用特定 tool:

```python
from anthropic import Anthropic

client = Anthropic()

ROUTE_TOOL = {
    "name": "route_request",
    "description": "把用户请求 route 到专用内容 pipeline。",
    "input_schema": {
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "enum": ["Educational", "Entertainment", "Comedy",
                         "Personal vlog", "Reviews", "Storytelling"],
                "description": "这个主题的内容类别。"
            },
            "confidence": {
                "type": "number",
                "description": "分类器置信度, 0.0 到 1.0。"
            }
        },
        "required": ["category", "confidence"]
    }
}

def classify(topic: str) -> dict:
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        tools=[ROUTE_TOOL],
        tool_choice={"type": "tool", "name": "route_request"},  # 强制
        messages=[{"role": "user",
                   "content": f"Categorize the topic: {topic}"}],
    )
    for block in resp.content:
        if block.type == "tool_use" and block.name == "route_request":
            return block.input  # {"category": "...", "confidence": ...}
    raise RuntimeError("分类器没调用 route_request tool")
```

为什么 `tool_choice={"type": "tool", "name": "..."}` 很重要:

- **强制** Claude 发出 route_request tool call(不允许自由文字)
- 通过 `input_schema` 保证响应 shape
- `enum` 限制防止幻觉类别
- 分类器不能 "闲聊" 或解释 — 只能分类

`tool_choice` 的选项:

| 选项 | 行为 |
|------|------|
| `{"type": "auto"}` | 默认 — Claude 自己决定要不要用 tool |
| `{"type": "any"}` | Claude 必须调用*某个* tool, 但选哪个 |
| `{"type": "tool", "name": "X"}` | Claude 必须调用指定的 tool X |

Routing 要用 `"tool"` — 你要每次都调用*特定*分类器 tool。

---

## 完整 Routing Pipeline

```python
PROMPTS = {
    "Educational": "写一份清楚的教育脚本……",
    "Entertainment": "写一份高能量的娱乐脚本……",
    "Comedy": "写一份喜剧脚本……",
    "Personal vlog": "...",
    "Reviews": "...",
    "Storytelling": "...",
}

def generate_script(topic: str) -> str:
    classification = classify(topic)
    category = classification["category"]
    prompt_template = PROMPTS[category]

    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2048,
        messages=[{"role": "user",
                   "content": f"{prompt_template}\n\nTopic: {topic}"}],
    )
    return resp.content[0].text
```

每个分支可以独立优化, 新增类别只要在 `PROMPTS` 和 `ROUTE_TOOL` 的 enum 加一条。

---

## 什么时候 Routing 是对的模式

Anthropic 建议, routing 适用于:

1. **可以清楚定义类别** — 分支之间没有模糊重叠
2. **信任分类器** — Claude(或更便宜的分类器)能可靠分类
3. **专用处理真的有好处** — 每分支优化优于通用 prompt
4. **分类开销值得分摊** — 多一次 LLM 调用是值得的

如果第一次 LLM 调用无法可靠分类, routing 反而是错误 — 你会把请求送到错的 pipeline, 结果比单一通用 prompt 还糟。

---

## 常见错误

1. **分类器用自由文字。** 没有 `tool_choice="tool"` + `enum`, Claude 可能回 "应该是教育类?" — 你就要 parse。强制 tool call。
2. **类别太多。** Routing 适合类别明显时。20+ 类别又有重叠会让分类器不可靠。控制在 10 以下。
3. **没有误分类的 fallback。** 置信度低时怎么办? 要有默认/通用 pipeline。
4. **忽略分类成本。** 每个请求都多付一次 LLM 调用。对低延迟 app, 分类用更小/便宜的模型(例如 Haiku)。
5. **把 routing 和 agent 混淆。** Routing 是 *workflow* — 代码分派到特定 pipeline。Agent 则是让 Claude 在推理时自由挑工具。不一样。

---

> **关键洞察**
>
> Routing 是 LLM workflow 版的 "switch statement" — 先分类, 再分派。Production 级别的版本用 `tool_choice={"type": "tool", "name": "..."}` 配合 `enum` input schema, 强制出结构化类别标签。这是 CCA 关键重点: **强制 tool use 保证分类器返回有效类别, 且无法闲聊。**

---

## CCA 考试关联

- **D1(22%)主要**: Routing 是四大 workflow 模式之一, 预期有场景题。
- **D2(18%)次要**: `tool_choice` 选项被明确测试 — 记三个值(`auto`、`any`、`tool`)。
- **D5(20%)次要**: Production 模式 — 便宜分类器模型、fallback 分支、enum 约束。
- Routing 信号词: "categorize"、"classifier"、"dispatch"、"specialized handling per category"。
- 考试陷阱: routing ≠ agent。Routing 是分类调用后由代码驱动分派。

---

## Flashcards

| 题目 | 答案 |
|------|------|
| 什么是 routing workflow? | 分类器 LLM 调用分类请求, 再由代码分派到专用 pipeline |
| 为什么分类器要用 `tool_choice={"type": "tool", "name": "X"}`? | 强制 Claude 通过 tool 返回结构化类别, 不允许自由文字 |
| 列出 `tool_choice` 的三个选项。 | `auto`(默认)、`any`(任一 tool)、`tool`(强制特定 tool)|
| 如何防止分类器幻觉出新类别? | Tool input schema 用 `"enum": [...]` 列出有效类别 |
| 什么时候*不*该用 routing? | 类别重叠、分类器不可靠、或单一 prompt 已经可靠时 |
| 分类器步骤的关键 production 优化? | 用更小/便宜的模型(例如 Haiku), 因为分类比生成简单 |
| Routing 是 workflow 还是 agent? | Workflow — 代码掌握分类调用后的分派 |
| 置信度低时分类器该返回什么? | Route 到默认/通用 pipeline 或请求人工审核(fallback 路径)|
