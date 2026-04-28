# Controlling Context — PM 视角


![Context Window As Resource Analogy](../../visuals/context-window-as-resource-analogy-zh-TW.svg)
*圖：Context Window 是有限資源 — 類比。*


![Context Control Tools Decision Tree](../../visuals/context-control-tools-decision-tree-zh-TW.svg)
*圖：選擇上下文控制工具的決策樹。*

| 项目 | 内容 |
|------|------|
| 考试对应 | D5 — Reliability & Performance（15%）、D3 — Claude Code Configuration & Workflows（20%） |
| Task Statements | 5.1 ★★★（context preservation）、5.4 ★★（large codebase context）、3.5 ★★（iterative refinement） |
| 课程来源 | claude-code-in-action / 03-context-and-commands / Lesson 10 |

---

## TL;DR

Claude Code 有一个有限的「工作记忆」（context window）。就像开太久的会议一样，对话积累噪音，Claude 会失去专注。四种工具管理这件事：**Escape**（中断）、**双击 Escape**（倒带）、**`/compact`**（摘要后继续）、**`/clear`**（全新开始）。PM 需要了解这些，因为 context 管理直接影响开发者生产力和 AI 输出质量 — 这影响冲刺速度和产品时间线。

---

## 为什么 PM 需要知道这些

你不需要自己管理 context，但你需要理解：

1. **「再问一次 Claude」不是免费的** — 每次交互都消耗 tokens 和 context 空间
2. **为什么长 coding session 会产出更差的结果** — context pollution 是真实的工程限制
3. **如何设定合理的期望** — 2 小时的 Claude session 不是线性生产力

这些知识帮你规划冲刺、估算工作量，以及和工程团队沟通 AI 辅助开发的事。

---

## 心智模型：会议室白板

| 工具 | 白板类比 | 什么时候用 |
|------|---------|-----------|
| **Escape** | 「等等，停下来 — 让我澄清一下」 | 有人往错误方向走 |
| **双击 Escape** | 擦掉最后 3 个项目，从一个好的点重新开始 | 跑题带偏了会议 |
| **`/compact`** | 拍一张白板照片，擦掉白板，把照片贴成小参考 | 白板满了但洞察很宝贵 |
| **`/clear`** | 把白板完全擦干净换新主题 | 切换到完全不同的会议议程 |

> 💡 **PM 决策框架**
>
> 问自己：「AI 还需要它之前学到的东西吗，还是要开始一个不相关的事？」
> - 需要先前知识 → **`/compact`**
> - 干净的开始更好 → **`/clear`**

---

## 产品情境演练

### 情境：AI 辅助开发的冲刺规划

你的工程团队每天用 Claude Code。一位资深工程师反馈：「Claude 前 20 分钟很好用，然后开始犯奇怪的错。」以下是发生了什么以及你可以建议什么：

| 症状 | 根本原因 | 建议 |
|------|---------|------|
| Claude 重复已修好的 bug | debug 噪音填满了 context window | 子任务之间用 `/compact` |
| Claude 忘记项目惯例 | 早期的命令掉出了 context | 把惯例存为 memories 或放在 CLAUDE.md |
| Claude 修改错误的文件 | 前一个任务的不相关 context | 切换 feature 时用 `/clear` |
| Claude 的输出质量随时间下降 | Context window 被低信号内容塞满 | 训练团队主动使用 Escape + 倒带 |

> 🎯 **PM 重点**
>
> Context 管理是一项**开发者技能**，应该纳入团队的 AI 工具入职培训。主动管理 context 的团队，从 AI coding assistant 得到的结果明显更好。

---

## 四种工具 — PM 需要知道的

### Escape — 「停下来重新导向」

当 Claude 往错误方向走时，开发者按 Escape 中途停止它。这节省 tokens 也防止坏的输出污染 context。

**PM 相关性**：这就是为什么「Claude 跑偏了 10 分钟」是培训问题，不是 Claude 的问题。开发者应该及早中断。

### 双击 Escape — 「回到前几步」

按两次 Escape 让开发者把对话倒带到任何之前的消息。那个点之后的一切都被丢弃。

**PM 相关性**：这等同于「让我们回到可行的地方，试另一个方法」。保留有用的 context 同时移除失败的尝试。

### `/compact` — 「摘要后继续」

把整个对话压缩成摘要。Claude 保留它学到的东西，但以压缩的形式。

**PM 相关性**：这是让长 session 能保持生产力的工具。没有它，session 在 20-30 分钟后就会退化。有了它，开发者可以维持数小时的高效 AI session。

### `/clear` — 「全新开始」

清除所有东西。Claude 从零 context 开始。

**PM 相关性**：切换不相关任务时必备。使用一个 feature 的残留 context 去做另一个 feature，会造成交叉污染。

---

## 视频洞察

视频示范中 PM 应注意的要点：

1. **Context 管理是主动的，不是被动的** — 讲师在 Claude 出问题_之前_就用这些工具，不是之后。这是团队应该采用的最佳实践。
2. **Escape + Memory 组合** — 当 Claude 重复犯错时，讲师按 Escape 然后保存 memory。这是永久修正，不是单次 session 的变通方案。鼓励你的团队随时间积累 memories。
3. **「对话控制快捷键看起来只是方便，但它们真的能改善 Claude 有效工作的能力」** — 讲师的原话。这些不是可有可无的；它们是必要的工作流程工具。

---

## 模拟考题

### 第一题：Developer Productivity 情境

你的团队已经用 Claude Code 两个月了。回顾会上，工程师们反映 Claude 做小任务很好，但在较长的 feature 实现 session（1 小时以上）中表现挣扎。几位工程师提到 Claude 会「忘记」之前的决定并开始自相矛盾。什么团队层级的建议能改善这个情况？

- A. 切换到 context window 更大的模型
- B. 训练团队在子任务间用 `/compact`，切换 feature 时用 `/clear`
- C. 限制 Claude Code session 最多 15 分钟
- D. 把所有项目文档加到 CLAUDE.md 让 Claude 永远不会忘

<details><summary>答案与解析</summary>

**B** — 根本原因是长 session 中的 context pollution。教会团队正确的 context 管理工具才是解决实际问题的方法。这是 Task 5.1（context preservation）的考试重点概念。

- A 可能有帮助但没有解决 context pollution 的根本问题 — 更大的 window 还是会被噪音填满
- C 太限制了，降低生产力
- D 会让 CLAUDE.md 太大，本身就消耗 context window 空间

**PM 重点**：Context 管理是可学习的技能。把它纳入你团队的 AI 工具入职培训。
</details>

### 第二题：Code Generation 情境

一位开发者已经和 Claude 花了 25 分钟构建一个复杂的数据 pipeline。Claude 现在理解了 schema、转换规则和错误处理 patterns。开发者需要新增一个转换步骤，但 context window 快满了。他该怎么做？

- A. 用 `/clear` 重新解释整个 pipeline
- B. 用 `/compact` 压缩 session，然后新增转换步骤
- C. 开新的 Claude Code session 然后粘贴 pipeline 代码
- D. 不做 context 管理继续下去

<details><summary>答案与解析</summary>

**B** — `/compact` 保留 Claude 对 pipeline 架构的理解，同时释放 context 空间。积累的知识（schema、转换 patterns、错误处理）正是值得保留的那种 context。

- A 浪费了 25 分钟的积累理解
- C 失去 context 而且需要手动重新解释
- D 有 context 溢出的风险，Claude 会丢失关键的早期信息

**PM 重点**：当开发者说「我必须重新跟 Claude 解释所有事」，问他有没有先试过 `/compact`。
</details>
