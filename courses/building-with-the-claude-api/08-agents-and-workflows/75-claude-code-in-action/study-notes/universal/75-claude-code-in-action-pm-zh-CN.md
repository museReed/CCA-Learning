# Claude Code in Action — PM Perspective（简体中文）

| 项目 | 内容 |
|------|------|
| 考试 Domain | D3 — Claude Code Configuration (20%) |
| Task Statements | 3.1（Claude Code 命令）、3.3（CLAUDE.md memory）、1.2（agentic workflow patterns） |
| 来源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 75 |

---

## 一句话总结

Claude Code 的真实价值只有在团队采用"context → plan → implement" workflow 并共享 `CLAUDE.md` 后才能解锁 —— 这是 PM 必须主导的产品/流程决策，不是留给开发者各自为政的工程选项。

---

## 心智模型：新伙伴的第一天

把 Claude Code 进项目当成新工程师入职：

| 入职步骤 | 人类工程师 | Claude Code |
|---------|-----------|-------------|
| 代码库导览 | 读 README + 问问题 | `/init` 扫描并写 `CLAUDE.md` |
| 团队惯例小抄 | 写在 wiki | `CLAUDE.md`（project scope） |
| 个人笔记偏好 | 写在自己的笔记本 | `CLAUDE.md`（local scope） |
| 通用工作风格 | 靠职业养成 | `CLAUDE.md`（user scope） |
| 我们怎么干活 | "先规划再写代码" | context → plan → implement workflow |

新工程师没 context 会写几周 mediocre 代码，Claude Code 没 `CLAUDE.md` 也一样。Memory 文件不是可选功能，它就是入职文档。

---

## 为什么这 lesson 对 PM 重要

大多数团队装了 Claude Code 却用错 —— 把它当 autocomplete 而不是 agent。本 lesson 是这个产品的 workflow 契约：照做得到 10x 价值，略过则只是漂亮点的 search-and-replace。

PM 的任务：

1. **把 `/init` + `CLAUDE.md` 定为团队规范** —— 不是建议。
2. **把三步 workflow 写进团队文档** —— context → plan → implement。
3. **定义哪些东西放进 project-scope CLAUDE.md** —— 不是所有偏好，只放共享的。
4. **把 CLAUDE.md 当成产品产物** —— 像 spec 一样 review、像 spec 一样更新。

---

## 产品使用场景

### 配合正确 workflow 时 Claude Code 最闪光

| 场景 | 为什么合适 |
|------|-----------|
| 在既有代码库上加新功能 | Context-first 流程避免 agent 重新发明你的 pattern |
| 在已有完整 test 的情况下重构 | TDD 变体大显身手 —— test 就是成功标准 |
| 新工程师 ramp up 旧项目 | `CLAUDE.md` 把 tribal knowledge 装好 |
| 跨团队协作 | Project `CLAUDE.md` 把惯例带给每一个贡献者 |

### 单靠 Claude Code 不够的场景

| 场景 | 要搭配什么 |
|------|-----------|
| 需要生产环境实时数据 | 加 MCP server（lesson 76） |
| 需要 UI 设计决策 | 还是要 product spec |
| 需要合规批准 | 人类 review in the loop |
| 需要跨 repo 知识 | `CLAUDE.md` user scope + 纪律 |

---

## CLAUDE.md 的三种 Scope（PM 视角）

这是 lesson 中最与产品相关的概念：

| Scope | 拥有者 | 该放什么 | 不该放什么 |
|-------|-------|---------|-----------|
| **Project** | Team lead / PM | Build 命令、团队惯例、架构规则 | 个人快捷键、机器特定设置 |
| **Local** | 个别工程师 | 个人快捷键、工作笔记、实验 flag | 团队共享惯例、别人要遵守的规则 |
| **User** | 个别工程师 | 通用工作风格（"先说明再改"） | 项目特定 pattern |

PM 应该把 project-scope `CLAUDE.md` 当一等公民 deliverable —— 在 code review 时 review、在重大架构变更时更新、在 PR 描述里引用。

---

## PM 决策框架

要把 Claude Code rollout 给团队时，回答：

1. **谁拥有 project `CLAUDE.md`？** 必须有人 curate。通常是 tech lead 或 PM。
2. **里面放什么？** 从 build 命令、代码风格、测试要求、架构概览开始。
3. **`CLAUDE.md` 的改动怎么 review？** 跟引发改动的代码放同一个 PR。
4. **如何强制"先计划"workflow？** 团队共识、PR template 或内部工具。
5. **量什么指标？** 新工程师 time-to-first-working-PR；PR 中包含"Plan:"段落的比例。

---

## Workflow 作为产品标准

"context → plan → implement" pattern 不是 Claude Code 的特殊怪癖 —— 而是现代 agent UX pattern。其他 agent 工具（Cursor、Windsurf、自研产品）都收敛到同一形状。PM 层级：

| Workflow 步骤 | 可要求的产品产物 |
|--------------|----------------|
| Context | 文件清单、相关文档、过去的 PR |
| Plan | PR 里在 code 之前贴出的书面计划 |
| Implement | 实际的 PR |

标准化后，code review 更快、onboarding 更便宜、质量下限提升 —— 同时消耗的 senior engineering 时数变少。

---

## 常见 PM 错误

1. **把 `CLAUDE.md` 当选配** —— 没它，每场新 session 都得重学项目。复利优势全没。
2. **让工程师把所有东西塞 user-scope** —— 共享惯例必须放 project scope，否则团队受益不到。
3. **为了"省时间"跳过 plan 步骤** —— 省了分钟却浪费小时修方向错的实现。
4. **没把 `CLAUDE.md` 列入 code review checklist** —— 它是活文档，过时条目会产出坏结果。
5. **混淆 `/clear` 与 `/init`** —— 教学入门经典错误。文档里要清楚告诉团队何时用哪个。

> **关键洞察**
>
> Claude Code 是 **团队协议**，不只是开发者工具。PM 真正的 deliverable 不是"我们装好了"，而是"我们有共用的 `CLAUDE.md`、我们遵守 context → plan → implement、我们 review agent memory 的改动像 review code 一样"。做到的团队拿到 agent 优势；没做到的没有。

---

## CCA 考试重点

- **D3（Claude Code Configuration）**：直接考 `/init`、`/clear`、`#`、`CLAUDE.md` scope 的题目概率很高。
- **D1（Agentic Coding & Architecture）**：context → plan → implement workflow 就是 agent 的标准 pattern。
- 预期会出场景题："某团队装了 Claude Code 但产能没提升 —— 缺了什么？"答案通常是 `CLAUDE.md` + workflow。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| PM 应该强制的三步 Claude Code workflow 是什么？ | 1) 读相关文件喂 context、2) 要求书面计划不写代码、3) 请 Claude 实现计划 |
| `CLAUDE.md` 的三种 scope 与各自拥有者是什么？ | Project（团队/PM 拥有、进 git）、Local（个别工程师、不进 git）、User（个别工程师、跨所有项目） |
| 为什么 PM 该把 project-scope `CLAUDE.md` 当一等 deliverable？ | 它是所有未来 Claude Code session 继承的入职文档、风格指南、架构摘要 —— 过时内容会产出坏结果 |
| `/init` 做什么？何时该跑？ | 扫描代码库并把总结写入 `CLAUDE.md`；项目启动时跑一次，重大架构改动后重跑 |
| `#` 快捷键做什么？ | 追加笔记到 `CLAUDE.md` 并询问 project、local 或 user scope |
| Claude Code 的 TDD 变体 workflow 是什么？ | 喂 context → 请 Claude 头脑风暴 test cases → 实现 test → 写代码直到全绿 |
| PM rollout Claude Code 的头号错误？ | 把 `CLAUDE.md` 当选配 —— 这会消除持久项目记忆的复利优势 |
| 怎么量化团队是否遵守"plan first"规则？ | PR 中在 code diff 前包含书面计划的比例 |
