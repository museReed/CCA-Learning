# Controlling Context — 工程师视角


![Context Control Tools Decision Tree](../../visuals/context-control-tools-decision-tree-zh-TW.svg)
*圖：選擇上下文控制工具的決策樹。*

| 项目 | 内容 |
|------|------|
| 考试对应 | D5 — Reliability & Performance（15%）、D3 — Claude Code Configuration & Workflows（20%） |
| Task Statements | 5.1 ★★★（context preservation）、5.4 ★★（large codebase context）、3.5 ★★（iterative refinement） |
| 课程来源 | claude-code-in-action / 03-context-and-commands / Lesson 10 |

---

## 一句话理解

Context 是有限资源 — Escape 中断输出、双击 Escape 倒带对话历史、`/compact` 摘要保留已学知识、`/clear` 完全重来。选对工具就能让 Claude 保持专注、节省 tokens。

---

## 为什么 Context 管理很重要

Claude Code 在一个固定大小的 **context window** 里运行。你发的每一条消息、Claude 读的每一个文件、每一次 debug 的来回，全部都消耗 tokens。当 window 满了，Claude 会丢失早期的信息，导致：

- **重复犯错** — Claude 忘了你之前给的修正
- **注意力漂移** — 不相关的 debug 历史干扰当前任务
- **Token 浪费** — 在噪音上花钱，不是在信号上

管理 context 不只是方便 — 它直接影响输出质量。

---

## 四种 Context 控制工具

### 1. Escape（按一次）— 中断

停止 Claude 正在输出的内容。适用于：
- Claude 正往错误方向走
- 你想在它浪费 tokens 之前重新导向
- 你需要在 Claude 完成前提供额外指引

> 💡 **Escape + Memory = 永久修正**
>
> 当 Claude 重复犯同一个错（例如试图读取一个不存在的 config 文件），立刻按 Escape，然后用 `#` 快捷键保存一条 memory，记录正确行为。这可以防止未来 session 再犯同样的错 — 不只是当前对话。

### 2. 双击 Escape — 倒带对话

按两次 Escape 可以看到你所有的消息历史，跳回任何一个之前的时间点。这会**丢弃选定点之后的所有消息**，等于倒带对话。

最适合用在：
- Debug 的来回污染了 context
- 你想从一个已知正确的状态重新尝试
- Claude 顺利完成了 Task A，但在 Task B 撞到问题，你想回到 Task A 完成后的状态

> 🎬 **视频补充**
>
> 讲师示范在 `auth.ts` 里写四个函数的测试。在为 `createSession` debug 一个缺少 package 的问题后，他倒带到 debug 之前，把 prompt 改成「写 getSession 的测试」。这保留了有用的 context（Claude 已经读过 `auth.ts`），同时丢掉了噪音（package debug 历史）。

### 3. `/compact` — 摘要后继续

把整个对话压缩成摘要，然后从摘要继续。核心区别：Claude **保留已学的知识**，但以压缩的形式。

最适合用在：
- Claude 在这个 session 中已经积累了对 codebase 的深入理解
- 你在相关子任务之间切换（例如完成函数 2 的测试后开始函数 3）
- Context window 快满了但积累的知识很宝贵

### 4. `/clear` — 全新开始

清除整个对话历史。Claude 从零开始（除了 CLAUDE.md 和 memories）。

最适合用在：
- 你要切换到完全不相关的任务
- 当前对话已经太混乱，抢救 context 反而有害
- 开始一个新的 coding session 做不同的 feature

---

## 决策框架：什么时候用什么工具？

| 情境 | 工具 | 原因 |
|------|------|------|
| Claude 正在输出烂东西 | **Escape** | 立刻止血 |
| Claude 又犯了同样的错 | **Escape + Memory** | 永久修正 |
| Debug 的来回污染了 context | **双击 Escape** | 倒带到干净状态，保留之前有用的 context |
| Context 满了但知识很宝贵 | **`/compact`** | 压缩，不丢弃 |
| 切换到完全不同的任务 | **`/clear`** | 全新开始，不带包袱 |
| 长 session，渐渐失去连贯性 | **`/compact`** | 摘要以回收 window 空间 |

> 🎯 **考试重点**
>
> 考试会测你是否理解 context preservation 和 context pollution 之间的取舍。核心洞察：**更多 context 不一定更好**。不相关的 context（debug 噪音、失败的尝试）会主动降低输出质量。

---

## 工程师类比

| 概念 | 类比 |
|------|------|
| Context window | RAM — 有限，所有运行中的 process 共享 |
| Escape（中断） | 终端里的 `Ctrl+C` — 杀掉当前 process |
| 双击 Escape（倒带） | `git reset --soft HEAD~3` — 撤销最近的 commits，保留 working tree |
| `/compact` | `git squash` — 把多个 commits 压成一个，保留净结果 |
| `/clear` | 在新目录 `git init` — 从零开始 |
| Context pollution | Memory leaks — 每次 debug 都留下残留物，降低性能 |

---

## 反面模式

| 反面模式 | 问题 | 更好的做法 |
|---------|------|-----------|
| 长 session 从不用 `/compact` | Context window 满了，Claude 忘记早期命令 | 每完成一个逻辑子任务就 compact |
| 用 `/clear` 但其实 `/compact` 就够了 | 丢掉了宝贵的已学 context | 只在切换到不相关工作时才 `/clear` |
| 让 Claude 无止境 debug 不中断 | 浪费 tokens，用失败的尝试污染 context | 早按 Escape，提供指引，必要时倒带 |
| 不为重复犯的错存 memory | 同样的错在每个新 session 出现 | Escape + `#` memory 快捷键永久修正 |
| 开始新任务不做任何 context 管理 | 前一个任务的噪音干扰新任务 | `/compact`（相关任务）或 `/clear`（不相关任务） |

---

## 考试聚焦：Context Window 是一种资源


![Context Window As Resource Analogy](../../visuals/context-window-as-resource-analogy-zh-TW.svg)
*圖：Context Window 是有限資源 — 類比。*

这直接对应 Task Statement 5.1（context preservation）和 5.4（large codebase context）：

| 考试情境 | 测什么 |
|---------|--------|
| S2（Code Gen） | 生成新模块的代码前，应该 compact 还是 clear？ |
| S4（Developer Productivity） | 如何在多步骤 coding session 中维持专注？ |

核心考试哲学：
- **Context 是有限资源** — 把它当内存分配来管理，不是无限日志
- **Signal > Noise** — 主动管理 window 里留什么
- **Iterative refinement**（Task 3.5）— Escape + 重新导向比让 Claude 完成一个坏方向更快

---

## 模拟考题

### 第一题：Code Generation 情境

你已经和 Claude Code pair-programming 30 分钟了。Claude 读了你的数据库 schema、理解了你的 ORM patterns，也成功实现了三个 API endpoints。你现在需要实现第四个 endpoint，pattern 一样。但是 context window 因为第二个 endpoint 的 debug 输出快满了。你该怎么做？

- A. 用 `/clear` 重新开始做第四个 endpoint
- B. 用 `/compact` 摘要这个 session，然后要求做第四个 endpoint
- C. 不做任何 context 管理，希望 Claude 还记得那些 patterns
- D. 完全关掉 Claude Code，开一个新 session

<details><summary>答案与解析</summary>

**B** — `/compact` 保留 Claude 对你的 schema、ORM patterns 和 endpoint 惯例的理解，同时压缩 debug 噪音。这正是 `/compact` 设计的使用场景。

- A 不必要地丢掉了 30 分钟的已学 context
- C 有 context window 溢出的风险，Claude 会丢失早期命令
- D 等同于 A 但多了额外步骤

核心洞察：Claude 有**宝贵的积累知识**（schema、patterns）— 不要丢弃它，压缩它。
</details>

### 第二题：Developer Productivity 情境

你叫 Claude 重构一个 utility 文件，但它开始改错文件了。Claude 在对话早期已经读过正确的文件。最快回到正轨的方式是什么？

- A. 用 `/clear` 从头开始
- B. 按一次 Escape 中断，然后重新指定正确的文件
- C. 让 Claude 完成，然后叫它 undo 它的改动
- D. 按两次 Escape 倒带到错误重构开始前

<details><summary>答案与解析</summary>

**D** — 双击 Escape 倒带到错误之前，保留了 Claude 之前读正确文件的 context。你可以更新 prompt 更具体地指示。

- A 丢失所有 context，包括 Claude 对正确文件的了解
- B 停止了输出但错误的输出留在 context 里，可能在后续尝试中造成混淆
- C 浪费 tokens 并加更多噪音到 context

考试哲学：**Context preservation** — 倒带到干净状态，而不是在错误上叠加修正。
</details>

### 第三题：Iterative Refinement 情境

Claude 一直尝试从 `utils/test-helpers.ts` import test helper，但你的项目里这个文件其实在 `test/helpers.ts`。这是跨不同 session 第三次犯这个错了。最有效的长期修正是什么？

- A. 每次都按 Escape 然后告诉 Claude 正确路径
- B. 按 Escape，然后用 `#` 快捷键保存一条 memory 记录正确路径
- C. 把正确路径加到 CLAUDE.md
- D. B 和 C 都是有效的方法，但 B 在立即生效上更快

<details><summary>答案与解析</summary>

**D** — Memory（B）和 CLAUDE.md（C）都能解决问题，但视频特别示范了 Escape + `#` memory 模式作为重复犯错的快速修正。CLAUDE.md 是更重量级的方案，需要修改文件，而且会影响整个团队。

- A 是暂时修正，不会跨 session 持久化
- B 提供即时、永久的个人层级修正
- C 可行但对单一文件路径的修正来说太重了，而且影响整个团队

考试哲学：**Iterative refinement** — 在正确的持久化层级修正重复的错误。
</details>
