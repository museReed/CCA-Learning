# Defining Prompts — PM Perspective（简体中文）

| 项目 | 说明 |
|------|------|
| Exam Domain | D2 — Tool Design & MCP Integration（18%）主；D1 — Agentic Architecture（22%）次 |
| Task Statements | 2.3（MCP primitives：prompts）、1.2（agent loop priming） |
| Source | building-with-the-claude-api / 07-mcp / Lesson 69 |

---

## One-Liner

Prompts 是 MCP 的"精选集"——由 server 作者策划、专家级调优过的指令。让用户不必学 prompt engineering 也能稳定拿到高质量结果，把"自由输入、结果不稳"变成"可预期、品牌一致"的功能。

---

## 心智模型：食谱

- 用户自己写 prompt 像家里厨房即兴发挥，有时好吃，有时难以下咽
- Prompts 是餐厅老板给的食谱，照着做每次都是主厨水准
- 用户还是能通过参数定制（`doc_id` 就像换食材），但方法是锁定的

好的 MCP server 会为最常见的 use case 出食谱。用户从 slash menu 选，server 负责复杂的 prompt 工作。

---

## 为什么 PM 要关心

自由 prompt 相当于 AI 产品里的"打命令行"。专家爱用，其他人看到就跑。Prompts 把专家知识转成：

- **稳定质量** — 每个用户都拿到同样测试过的结果
- **可发现的功能** — prompts 变成 slash-command、快捷动作、按钮
- **品牌语气** — 你的写作风格、格式、语调都内建在模板里
- **新手捷径** — 新用户按"run prompt"立刻看到好结果
- **成本控制** — 调优过的 prompt 通常比用户自己打的更短更聚焦

对 PM 而言，prompts 是 tool 与 resource 之上的产品化层。

---

## 产品场景

### 什么时候 Prompts 划算

| 场景 | 为什么适合 |
|------|-----------|
| 用户重复做的任务（改格式、总结、翻译） | 一次写好最佳版本 |
| 措辞至关重要的任务（语气、结构、合规） | 把措辞锁定 |
| 希望暴露为 slash-command 或快捷动作的功能 | Prompts 天然对应 UI |
| 低信心用户想"就给我好的结果" | 把 prompt 复杂度藏在按钮后 |

### Prompts 过头时

| 场景 | 更适合 |
|------|--------|
| 一次性任务、没有回头客 | 自由输入即可 |
| 任务变化大、约束反而碍事 | 让用户自己写 |
| 任务其实是查数据 | 用 resource |
| 任务其实是执行动作 | 用 tool |

---

## 用户怎么体验一个 Prompt

从用户视角看，prompt 通常是：

1. CLI 或 chat UI 的 slash-command（`/format`、`/summarize`）
2. 图形界面的按钮或快捷动作
3. 首次启动时的模板选择器

他们选、填一两个参数（如哪份文档），系统就跑完整的预工程化指令。用户从不需要看、也从不需要写底层 prompt 文本。

---

## PM 决策框架

做 prompt 前问自己：

| 问题 | 若 Yes | 意义 |
|------|--------|------|
| 输出质量对措辞高度敏感？ | Yes | 出 prompt |
| 许多用户重复做的任务？ | Yes | 出 prompt |
| 只有你的团队有能力做好这件事？ | Yes | 出 prompt（外化专业） |
| 用户希望用很多创意方式做这件事？ | Yes | 不要做 prompt，保留自由输入 |
| Prompt 需要 live data？ | Yes | Prompt 结合 resource 或 tool |

---

## 质量门槛：什么时候 prompt"够好"能上线？

本课建议很严格：只上真的比用户自己写更好的 prompt。大致 checklist：

1. **用 5+ 真实输入测过** — 每次都产出好结果？
2. **清晰的参数 schema** — 每个参数都有 description，让 client 显示
3. **与 server 的 tool / resource 协同** — prompt 引用真实存在的 server 原语
4. **扛得住边界情况** — 空输入、非标准 doc ID、极端长度
5. **一行描述** — 用户靠这行挑

若你的 prompt 赢不了用户临时敲的 30 秒版本，别上——会训练用户对 prompts 失去信任。

---

## PM 常见错误

1. **上太多 prompts** — 多到用户扫不完会 decision paralysis，3–10 个好 prompt 胜过 50 个平庸的
2. **描述模糊** — 用户看不出 prompt 做什么就不会选，要像按钮 label 一样写
3. **把 prompts 当静态配置** — 它们需要版本控制、eval、迭代，跟其他面向模型的 code 一样
4. **把数据混进 prompt** — 如果你发现要把文档内容写进 prompt，其实要的是 resource
5. **不量化 prompt 质量** — 跟踪哪些 prompt 被选、哪些导致 rework，淘汰失败者

> **Key Insight**
>
> Prompts 是让 MCP 从"开发者 SDK"变成"产品表面"的原语。Tool 与 resource 让 server 有能力，prompts 让它好用。理解这点的 PM 会出"小而精的高质量动作清单"——AI 产品版的 Notion 或 Linear slash-menu——用户觉得拿到好用工具，而且从头到尾不必打开文本框。

---

## CCA Exam Relevance

- **D2（Tool Design & MCP Integration）**：Prompts 是 tool / resource 之后的第三种 MCP 原语，知道它带参数、返回一串消息
- **D1（Agentic Architecture）**：Prompts 用高质量对话开场 seed agent loop
- 考题模式："Server 作者要上线一个可复用的'改写成 markdown'指令，哪个原语？" → prompt

---

## Flashcards

| Front | Back |
|-------|------|
| Prompts 的"食谱"比喻是什么？ | 用户自己写 prompt 是即兴厨师；prompts 是餐厅老板给的食谱，用户换食材（参数），每次都拿主厨水准 |
| 为什么 prompts 是产品化层？ | 把专家 prompt engineering 转成用户能用的 slash-command 或快捷动作 |
| 什么时候 PM 不该做 prompt？ | 任务变异大、一次性任务，或其实是查数据（resource）或动作（tool） |
| 一个 prompt 要"可上线"需要什么？ | 真实输入测过、清晰参数 schema、配合 server tool/resource、处理边界情况、一行清晰描述 |
| 描述模糊为什么会杀死 prompt？ | 用户按描述挑 prompt，模糊的没人选，浪费工程资源 |
| 上 50 个平庸 prompt 还是 5 个精品？ | 5 个精品——prompt 太多造成 decision paralysis 并稀释认知质量 |
| Prompts 怎么跟 tools 与 resources 组合？ | Prompt 可引用 tool（例如"用 `edit_document` 存结果"）或 resource，像多步 workflow 的食谱 |
| 若 prompt 把文档内容写死而非参数化会怎样？ | 你其实想要的是 resource——prompt 是模板、resource 是数据 |
