# Running the Eval — Engineering Deep Dive（简体中文）

| 项目 | 内容 |
|------|------|
| Exam Domain | D3 — Evaluation & Iteration（20%，主要）；D5 — Enterprise Deployment（20%，次要） |
| Task Statements | 3.3（eval 执行）、3.1（eval 设计）、3.2（测试数据集） |
| Source | building-with-the-claude-api / 02-prompt-evaluation / Lesson 20 |

---

## 一句话摘要

核心 eval pipeline 由三个小函数构成 — `run_prompt`、`run_test_case`、`run_eval` — 拿一份数据集，把每一条推进 Claude，吐出一份可以交给 grader 的结构化结果列表。

---

## 三函数架构

课程把 eval runner 组织成三个职责分离清晰的可组合函数：

```
┌─────────────────────┐
│     run_eval        │  ← 加载数据集、遍历每一条
│  (dataset)          │
└──────────┬──────────┘
           │ 对每个 test_case
           ▼
┌─────────────────────┐
│   run_test_case     │  ← 串接 prompt + grader
│  (test_case)        │
└──────────┬──────────┘
           │ 调用
           ▼
┌─────────────────────┐
│    run_prompt       │  ← 把 template 和输入合并、调用 Claude
│  (test_case)        │
└─────────────────────┘
```

每个函数只做一件事。这是刻意的 — 当 eval 变复杂（并行执行、重试、model-based grading），你一次只改一个函数，不用重写整条 pipeline。

---

## 函数 1：`run_prompt`

最底层的函数处理单次 prompt 执行：

```python
def run_prompt(test_case):
    """Merges the prompt and test case input, then returns the result"""
    prompt = f"""
Please solve the following task:

{test_case["task"]}
"""

    messages = []
    add_user_message(messages, prompt)
    output = chat(messages)
    return output
```

注意此时 prompt 的状态 — 刻意极简。没有格式指令、没有输出约束。课程说：*"现在我们让 prompt 极其简单。没有包含任何格式指令，所以 Claude 很可能返回比我们需要的更冗长的输出。我们会在后面迭代 prompt 设计时改善这点。"*

那个冗长输出的 baseline 正是重点 — 它就是你后面加结构时要度量的对照组。

---

## 函数 2：`run_test_case`

中间层负责跑一条测试案例并评分：

```python
def run_test_case(test_case):
    """Calls run_prompt, then grades the result"""
    output = run_prompt(test_case)

    # TODO - Grading
    score = 10

    return {
        "output": output,
        "test_case": test_case,
        "score": score
    }
```

两个重要观察点：

1. **Score 硬编码为 10。** 这是刻意的 placeholder。真正的 grading 逻辑在 Lesson 21（model-based）和 22（code-based）。硬编码 10 让 pipeline 在 grader 还没准备好之前就能端到端跑 — 这是经典的"walking skeleton"技巧。
2. **返回结构是一个紧凑的合约。** 每条结果都带 `output`、`test_case`、`score`。下游消费者（报表生成、regression 检测、dashboards）都依赖这个形状。

---

## 函数 3：`run_eval`

最上层驱动整个循环：

```python
def run_eval(dataset):
    """Loads the dataset and calls run_test_case with each case"""
    results = []

    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)

    return results
```

刻意写得很琐碎。就是循环、调用 `run_test_case`、收集结果。后面章节会把它升级成并行执行，但这个同步版已经足以示范模式。

---

## 驱动整条 Pipeline

加载并跑完整 eval 只需要五行 script：

```python
with open("dataset.json", "r") as f:
    dataset = json.load(f)

results = run_eval(dataset)
```

Lesson 19 保存下来的数据集被 `json.load` 读进来，交给 `run_eval`，返回一串 result dict。

**时间备注：** 课程提醒即使用 Haiku，第一次跑完整数据集大约要 30 秒。生产规模（几百到几千条）下这会成为第一个瓶颈，这就是为什么要引入并行化。

---

## 结果结构

每个 result dict 有三个 key：

| Key | 内容 | 用途 |
|-----|------|------|
| `output` | Claude 的完整文本响应 | 你要评分的对象 |
| `test_case` | 原始测试案例（`task` dict） | Grader 和报表的上下文 |
| `score` | 数值分数（当前硬编码 10） | 质量指标 |

检查结果：

```python
print(json.dumps(results, indent=2))
```

课程说输出"相当冗长"，因为 prompt 没有格式指令 — 这就是整章后半要改进的 baseline 条件。

---

## 你搭了什么 vs. 还缺什么

课程讲得很明白：*"你刚刚搭好的几乎就是 eval pipeline 实际会做的大部分事情。"* 骨架可以跑 — 数据集进、结果出。剩下的是三层深化：

| 维度 | 当前状态 | 后续课程 |
|------|----------|----------|
| Grading | 硬编码 10 | Lesson 21（model-based）与 22（code-based） |
| Prompt 质量 | 冗长 baseline | 依 eval 分数迭代 |
| 性能 | 串行、~30 秒 | 并行 batching |

关键 insight 是：*pipeline* 本身很简单 — 复杂度在每一阶段的细节里，不在阶段间的连接方式。

---

## 为什么这个最小 pipeline 是正确起点

"Walking skeleton"有三个完整版 runner 没有的特性：

1. **端到端证明** — 你可以在任何 grader 实现前就演示整个循环能跑，早期抓到集成 bug。
2. **隔离升级** — 你可以把硬编码 grader 换成真的，而不碰到 `run_prompt` 或 `run_eval`。
3. **稳定合约** — 下游工具（dashboards、regression CI、报表）从第一天起就能依赖结果结构。

这正是生产 AI 系统想要的模式：先上最简 pipeline，随着产品成熟再一个一个函数替换成精细版。

---

## 常见错误

1. **跳过 walking skeleton** — 想一次搭完 grader、并行、dashboard，会陷入 debugging 地狱。
2. **把 grading 混进 `run_prompt`** — 职责分离才让你能独立升级 grader。
3. **没把 `results` 存盘** — 生产里你会想把结果存盘，方便跨跑比对 diff。
4. **生产规模下还用同步循环** — 3 条没问题，3,000 条致命；早点规划 `asyncio` 或线程池。
5. **忘了修掉 grader placeholder** — 把 `score = 10` 上 CI 会让 eval 失去意义；这只是教学用。

---

> **Key Insight**
>
> 三函数架构的力量不在于复杂，而在于职责分离。`run_prompt` 管 Claude 调用、`run_test_case` 管评分、`run_eval` 管迭代。每个函数都能独立替换，这正是从 notebook demo 迈向生产 eval pipeline 所需要的特性。CCA 考试会考结构化结果形状（`output` / `test_case` / `score`）这个 D3 task 3.3 的细节。

---

## CCA 考试相关性

- **D3（Evaluation & Iteration）**：知道三函数分解和固定的结果形状；理解硬编码 grader 是跳板不是终点。
- **D5（Enterprise Deployment）**：这个 pipeline 就是每一个生产 prompt eval 的运作基底；要认识到 walking-skeleton 模式可以通过逐一替换函数扩展到真实系统。
- 考题触发词：任何问"你实际怎么对数据集跑 eval"都指向 `run_eval → run_test_case → run_prompt` 的分层。

---

## Flashcards

| Front | Back |
|-------|------|
| Eval runner 的三个函数从外到内是什么？ | `run_eval`（遍历数据集）→ `run_test_case`（串 prompt 和 grader）→ `run_prompt`（调用 Claude）。 |
| `run_prompt` 做什么？ | 把 prompt 模板跟测试案例的 `task` 输入合并，用 `chat()` 送进 Claude，返回输出文本。 |
| `run_test_case` 返回什么？ | 一个三键 dict：`output`（Claude 响应）、`test_case`（原始输入）、`score`（数值分数，当前硬编码 10）。 |
| 为什么这课的 grading score 硬编码 10？ | 为了在真正的 grader（lesson 21-22）实现前让 walking-skeleton pipeline 能跑。 |
| 执行时如何加载数据集？ | `with open("dataset.json", "r") as f: dataset = json.load(f)` — 就是 Lesson 19 生成的文件。 |
| 用 Haiku 第一次跑 eval 大概多久？ | 课程说完整（小）数据集大约 30 秒。 |
| 为什么 baseline prompt 产出冗长响应？ | 因为没有格式指令 — 这是刻意的，让后续 prompt 迭代能展示可度量的改进。 |
| 本课示范的"walking skeleton"模式是什么？ | 先用 placeholder 把整条 pipeline 搭起来，再把每个函数换成生产版，但合约不变。 |
