# Generating Test Datasets — Engineering Deep Dive（简体中文）

| 项目 | 内容 |
|------|------|
| Exam Domain | D3 — Evaluation & Iteration（20%，主要）；D5 — Enterprise Deployment（20%，次要） |
| Task Statements | 3.2（测试数据集）、3.1（eval 设计）、3.3（eval 执行） |
| Source | building-with-the-claude-api / 02-prompt-evaluation / Lesson 19 |

---

## 一句话摘要

你可以在几分钟内用 Claude 帮你生成 eval 数据集 — 用 Haiku 这种更快的模型、JSON prefilling 技巧、配合 stop sequences，一次就能拿到可 parse 的干净输出。

---

## 场景：AWS Code Assistant

课程构建的 eval 系统是给一个帮用户写 **AWS 专属代码**的 prompt，输出格式有三种：

- Python 代码
- JSON 配置文件
- 正则表达式

核心需求：输出必须**干净** — 不能有多余的解释、前言、后记。这个"干净输出"需求正是 eval 数据集要压力测试的属性。

起始（v1）prompt：

```python
prompt = f"""
Please provide a solution to the following task:
{task}
"""
```

---

## 数据集结构：Task 数组

数据集是一个 JSON 对象数组，每个对象有一个 `task` 字段描述要 Claude 完成什么：

```json
[
  { "task": "Description of task" },
  ...additional
]
```

这种最小结构是刻意的。执行 eval 时你会遍历整个数组，把每个 `task` 内插到 prompt 模板后送进 Claude。之后加字段（expected output、分类、难度）很容易；从简单开始更快。

---

## 为什么用 Haiku 生成数据集

课程明确建议用 **Haiku** 而不是完整版 Claude 来生成数据集。理由是经济考量：

- 数据集生成是批量、创意性任务，不需要 frontier-model 的推理能力。
- Haiku 每次调用更快、更便宜。
- 一百条数据集用 Sonnet 很贵，用 Haiku 几乎免费。

这是 CCA 课纲的通用模式：**批量工作用快模型，被评估的任务本身才用 frontier 模型。**

---

## 与 Claude 交互的辅助函数

课程介绍三个会在整章重复使用的辅助函数：

```python
def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages, system=None, temperature=1.0, stop_sequences=[]):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature
    }
    if system:
        params["system"] = system
    if stop_sequences:
        params["stop_sequences"] = stop_sequences

    response = client.messages.create(**params)
    return response.content[0].text
```

三个观察点：

1. **`temperature=1.0` 默认** — 数据集生成需要高熵产出多样的测试案例，而不是重复的清单。
2. **`stop_sequences` 已接好** — 这就是让 prefilling 技巧能干净运作的关键（下面说明）。
3. **`chat()` 返回 `.content[0].text`** — 为调用端抽象掉 content-block 结构，直接拿纯文本。

---

## 数据集生成函数

课程主函数：

```python
def generate_dataset():
    prompt = """
Generate an evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects, each representing task that requires Python, JSON, or a Regex to complete.

Example output:
```json
[
  {
    "task": "Description of task",
  },
  ...additional
]
```

* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a single regex
* Focus on tasks that do not require writing much code

Please generate 3 objects.
"""
```

三个值得注意的 prompt engineering 决策：

- **Example output 放在围栏代码块里** — Claude 得到具体的形状模板，而不是抽象描述。
- **两个明确约束** — "单一 function / object / regex" 和 "不用写太多代码"。这两条把生成空间收窄，让数据集保持聚焦。
- **明确数量** — "Please generate 3 objects" 给出确定的输出大小。

---

## JSON Prefilling + Stop Sequence 技巧

本课最重要的技术：

```python
messages = []
add_user_message(messages, prompt)
add_assistant_message(messages, "```json")
text = chat(messages, stop_sequences=["```"])
return json.loads(text)
```

这是从 Claude 拿到可 parse JSON 的经典模式。运作方式：

1. **加一条 assistant message 内容为 ` ```json `** — 等于告诉 Claude"你已经开始写一个 JSON 代码块了，继续写下去"。
2. **设置 `stop_sequences=["```"]`** — Claude 一旦要关闭 code fence 就立刻停下。
3. **用 `json.loads` 解析原始文本** — 拿回来的就是纯 JSON，没有前言后语，没有收尾围栏。

为什么重要：没有 prefilling，Claude 经常会包一句前言（"Here is your dataset:"）或忘记关围栏。Prefilling + stop sequences 把"从 Claude 取 JSON"从 regex parsing 问题变成一行 `json.loads`。

这同时是 **D5 生产模式**，也是 D3 技巧 — 任何你要从 Claude 取结构化输出但又不想动用 tool use 的场景都可以用。

---

## 执行

```python
dataset = generate_dataset()
print(dataset)
```

这会返回三个覆盖 Python、JSON config、regex 的 AWS 测试案例。

---

## 持久化数据集

```python
with open('dataset.json', 'w') as f:
    json.dump(dataset, f, indent=2)
```

把数据集存盘很重要，原因有三：

- **可复现性** — 同一份数据集必须在 prompt 迭代间重用（否则比较无效，见 Lesson 18）。
- **版本控制** — 你可以把 `dataset.json` commit 进 repo，每个工程师都对同一份正典输入集打分。
- **解耦** — 生成和执行变成两个独立步骤；生成一次、eval 跑很多次。

文件就放在 notebook 旁边，让 Lesson 20 的 eval runner 用 `open("dataset.json", "r")` 直接读。

---

## 常见错误

1. **用 Sonnet 来生成数据集** — 浪费钱；Haiku 才是批量创意工作的正确选择。
2. **跳过 JSON prefilling 技巧** — parser 会被 Claude 的前言后语搞坏。
3. **忘了 `stop_sequences`** — 没设置时，Claude 会关围栏然后继续写，毁掉 parse。
4. **生成后在每次迭代重新生成** — 这会摧毁可比性；生成一次、存盘、重用。
5. **没在 prompt 里指定确切数量** — "生成一些测试案例"会给你不可预测的大小，搞坏批处理假设。

---

> **Key Insight**
>
> Prefilling + stop-sequence 技巧是本课最值得重用的技术。它把"让 Claude 输出 JSON"从脆弱的 parse 问题变成一行代码。背下来 — 它会出现在 D3（数据集生成）、D5（生产结构化输出），以及任何需要机器可读输出但又不想启动完整 tool use 协议的地方。

---

## CCA 考试相关性

- **D3（Evaluation & Iteration）**：Dataset generation 是 eval 工作流的命名子步骤；要知道"用 Claude 生成"和"手工构造"两种选项。
- **D5（Enterprise Deployment）**：Prefilling + stop-sequence 模式是生产系统取结构化输出的首选做法。
- 准备好回答类似"如何为新 prompt bootstrap 一份 eval 数据集？"→ 用 Haiku 生成、prefill JSON 围栏、用 stop sequence、`json.loads`、存盘。

---

## Flashcards

| Front | Back |
|-------|------|
| 课程建议用哪个模型生成数据集？为什么？ | Haiku — 对批量创意工作（如生成测试案例），它比完整版 Claude 更快、更便宜。 |
| AWS code assistant prompt 的三种输出格式是？ | Python 代码、JSON 配置文件、正则表达式。 |
| 数据集的最小结构是什么？ | 一个 JSON 对象数组，每个对象有一个 `task` 字段描述 Claude 要完成什么。 |
| 如何从 Claude 取得干净 JSON 而不用 tool use？ | Prefill 一条 assistant message 为 ` ```json `、设 `stop_sequences=["```"]`、对结果调用 `json.loads(text)`。 |
| `stop_sequences=["```"]` 在这个模式中的作用是什么？ | Claude 一写下收尾的 code fence 就停止生成，所以返回文本是纯 JSON。 |
| 为什么数据集要存盘？ | 这样同一份数据集可以在 prompt 迭代间重用，这是分数可比较的前提。 |
| 生成 prompt 里的两个明确约束是什么？ | "单一 Python function / JSON object / regex" 和 "不用写太多代码"。 |
| `chat()` helper 的默认 temperature 是多少？原因？ | `temperature=1.0` — 高熵产生更多样的测试案例，这正是 eval 数据集所需要的。 |
