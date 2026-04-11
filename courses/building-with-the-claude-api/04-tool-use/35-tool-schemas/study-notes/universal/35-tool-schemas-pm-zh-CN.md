# Tool Schemas — PM Perspective

| 项目 | 内容 |
|------|------|
| 考试 Domain | D2 — Tool Design & MCP Integration (18%) 主要；D1 — Agentic Architecture (22%) 次要 |
| Task Statements | 2.1（tool schema 设计）、2.2（tool function 定义）、1.2（agentic loop 基础） |
| 来源 | building-with-the-claude-api / 04-tool-use / Lesson 35 |

---

## 一句话总结

Tool schema 是你的 AI 在决定如何帮用户之前会读的产品文案 — 把它的文字当成 app store 描述来对待，因为 Claude 就是这样看它。

---

## 心智模型：菜单项目描述

想象一份餐厅菜单：

- 菜名 **name**（「辣味金枪鱼卷」）— 告诉客人这东西存在。
- 菜单描述 **description**（「新鲜黄鳍金枪鱼、辣椒蒜泥蛋黄酱、葱、6 贯」）— 告诉客人何时该点、能期待什么。
- **过敏原/辣度/价格** 注记 — 限制谁该点。

Tool schema 对 Claude 来说正是这样：

| 菜单概念 | Schema 字段 |
|----------|-------------|
| 菜名 | `name` |
| 菜单描述 | `description` |
| 食材/过敏原/辣度 | `input_schema.properties`（含 type、description、enum） |
| 必选选项（如「请选配菜」） | `input_schema.required` |

描述含糊的菜单（「鱼料理 $12」）点单少、客人疑惑多。描述丰富的菜单能把对的菜送到对的人。Tool schema 也一样。

---

## 为什么 PM 应该拥有描述文案

多数工程师会很乐意写「Gets current time」这种一句话描述然后走人。那句话是*Claude 每次调用时会读的产品文案*。写一份好描述只花几分钟，可靠度红利却庞大。

PM 应该：

1. **每个 tool 的 `description` 都要 review**，像审 app store 列表或 onboarding 文案一样。
2. **提供「何时使用」那一句** — 这是描述里最有价值的一句，工程师最常跳过。
3. **列出相关 tool** 帮 Claude 区分。
4. **在属性描述里放具体示例**。

---

## 产品场景：Schema 质量真正改变结果的地方

| 场景 | Schema 质量如何帮忙 |
|------|--------------------|
| 多个类似的 tool（如多个日历动作） | 描述让 Claude 挑对而非用猜的 |
| 用户讲话含糊 | 「何时使用」那句把 Claude 引导到对的 tool |
| 严格的参数格式（ID、日期、SKU） | 属性描述与 enum 避免调用格式错误 |
| 不同语言的用户 | 丰富的描述让 Claude 把翻译对应到对的 tool |
| 高风险动作（支付、删除） | 明确的必填字段避免意外遗漏 |

---

## 三个字段的白话解释

| 字段 | 对 PM 而言的意思 |
|------|-------------------|
| `name` | 内部 ID。当作 slug。短、无歧义、snake_case。 |
| `description` | 销售话术。告诉 Claude *做什么*、*何时用*、*返回什么*。3-4 句。 |
| `input_schema` | 订单表格。哪些字段必填、哪些值合法、什么单位、什么格式。 |

把这三个当成 PRD 的三个字段：身份、价值主张、设置。

---

## 「何时使用」那一句

Schema 文案最常被省略的，就是告诉 Claude**何时**该挑这个 tool 而不是别个。例：

- 差：「返回今天的日期。」
- 好：「返回今天的日期。**当用户问今天、明天、或任何相对日期时使用此 tool。**」

PRD 里，每个 tool 都明确写一行：

> Claude 应在此时使用此 tool：*(一句话)*

这会迫使 PM 与工程师在写代码前先对齐 tool 的用途，这句话接着就直接写进描述。

---

## PM 对 Schema 设计的决策框架

对功能中每个 tool 问：

| 问题 | 产出 |
|------|------|
| 什么名字能无歧义地标识这个 tool？ | `name` |
| 「何时使用」的一句话是什么？ | `description` 第一句 |
| 这个 tool 返回什么、什么格式？ | `description` 最后一句 |
| 哪些参数是严格必填？ | `input_schema.required` |
| 每个参数，合法值是什么？（enum？范围？格式？） | 属性 `type`、`enum`、`description` 内示例 |
| 有没有 Claude 可能混淆的相关 tool？ | `description` 内交叉引用 |
| Claude 传错参数会发生什么？ | 定义恢复 UX（链接到 tool function 的错误处理） |

---

## PM 常犯的错

1. **让工程把一句话描述出货** — 跳过文案 review，Claude 就会把用户请求导错路。
2. **写实现细节而非意图** — 「调用 /v1/time endpoint」对 Claude 毫无帮助。
3. **忘了列举合法值** — 「温度单位」应该是 `enum: ["celsius", "fahrenheit"]`，不是自由字符串。
4. **没交叉引用相似 tool** — 在多 tool 系统里，Claude 需要协助区分。「此 tool 返回现在时间；要排期未来事件请用 `create_reminder`。」
5. **改代码没改 schema** — 参数改名与新增 optional 字段都必须同步到 schema，否则 Claude 的先验会过期。

> **Key Insight**
>
> Tool schema 描述是你的 AI 会读并据以行动的产品文案。把它当成工程的事后补充，等于 app 上架却留空 app store 描述：下载变少、体验变差。PM 要像拥有 UI 文案那样严格拥有 schema 文案，才能做出感觉明显更能干的功能。CCA 考试 D2 的 tool design 与选择类题目会直接考这点。

---

## CCA 考试重点

- **D2（Tool Design & MCP Integration）**：Tool 定义三个必填字段、描述 best practice、`required` 语意、`enum` 用于限制值。
- **D1（Agentic Architecture）**：描述质量驱动 Claude 在 agent loop 中选 tool。
- 预期会出产品框架的题目：「团队有两个类似 tool，Claude 常选错，最可能的修正是？」— 答：改善描述、加入「何时使用」句、在 tool 间交叉引用。

---

## Flashcards

| Front | Back |
|-------|------|
| Tool 定义的三个必填字段是什么？ | `name`、`description`、`input_schema`。 |
| Tool schema 的菜单项目比喻是什么？ | Name 是菜名、description 是菜单描述、properties 是食材/限制、required 是「必选配菜」。 |
| Schema 描述最常被跳过的一句是？ | 「何时使用」那一句 — 告诉 Claude 当多个 tool 可选时该挑哪个。 |
| 为什么 PM 应该 review tool 描述？ | 它是 Claude 每次调用时都会读的产品文案；直接影响功能可靠度与用户体验。 |
| 要怎么避免 Claude 混淆两个相似的 tool？ | 在每个描述内交叉引用（「若要做 X 请改用 `other_tool`」）。 |
| 什么时候该在参数描述用 `enum`？ | 当合法值是固定集合（如单位、状态、类别）时 — 消除模糊性。 |
| Tool schema 的 `required` 是什么意思？ | 它列出 Claude 必须提供的参数名；没列的就是 optional。 |
| PRD 里哪一行能捕捉 tool 对 Claude 的用途？ | 「Claude 应在此时使用此 tool：*(一句话)*」— 直接写进描述。 |
