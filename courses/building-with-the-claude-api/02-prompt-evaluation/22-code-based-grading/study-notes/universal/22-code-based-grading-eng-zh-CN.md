# 代码评分 Code-Based Grading — 工程深入

| 项目 | 说明 |
|------|------|
| 考试领域 | D3 — Evaluation（20%）主要；D5 — Enterprise Deployment（20%）次要 |
| 任务声明 | 3.4（deterministic 评分）、3.3（test runner 集成）、5.4（综合 eval 指标） |
| 来源 | building-with-the-claude-api / 02-prompt-evaluation / Lesson 22 |

---

## 一句话重点

Code-based grading 把 model 输出丢进 deterministic parser —— JSON、Python AST、regex —— 每个 test case 返回 10 或 0，给你一个便宜可靠的 eval 质量底线，与较模糊的 model grader 互补。

---

## 为什么需要 Code Grader

评估会产生代码的 AI model 时，"答案看起来对吗？"还不够。你需要验证产出的代码**有合法 syntax 且符合正确格式**。用 model grader 做这件事又慢又贵 —— 而且这问题根本不需要判断，需要的是 parser。

Code grading 验证 AI 响应的两个面向：

| 面向 | 检查 |
|------|------|
| **Format** | 响应只能返回指定的 code 类型（Python、JSON 或 Regex），不能有解释 |
| **Valid Syntax** | 产出的代码必须能被正确 parse |
| **Task Following** | （由 model grader 处理 —— 不是 code grader） |

这个分工是故意的：便宜/deterministic 的东西交给 code grader，主观的东西交给 model grader。两者合起来提供完整评估。

---

## 三个 Validator

来源的三个 syntax validator 都走同一模式 —— 尝试 parse、成功返回 10、失败返回 0：

```python
def validate_json(text):
    try:
        json.loads(text.strip())
        return 10
    except json.JSONDecodeError:
        return 0

def validate_python(text):
    try:
        ast.parse(text.strip())
        return 10
    except SyntaxError:
        return 0

def validate_regex(text):
    try:
        re.compile(text.strip())
        return 10
    except re.error:
        return 0
```

三个工程要点：

1. **先 `.strip()`** —— 不然前后空白会让合法 payload 被误判为 false negative。
2. **binary 10 或 0 的输出** —— 让分数尺度与 model grader 一致，后面才能平均。
3. **catch 特定 exception** —— `json.JSONDecodeError`、`SyntaxError`、`re.error`。裸 `except:` 会掩盖 grader 本身的 bug。

三个 validator 都用标准库 —— 没有外部依赖、没有 API 成本、延迟以微秒计。

---

## Dataset 格式要求

为了让 code grader 知道**该跑哪个** validator，每个 test case 必须声明它期待的格式：

```python
{
    "task": "Create a Python function to validate an AWS IAM username",
    "format": "python"
}
```

来源建议更新你的 dataset 生成 prompt，让它自动把这个 `format` 字段加进示例输出结构，这样新 test case 永远带有 routing 所需的提示。

---

## 改善 Prompt 清晰度

Code grader 也反过来逼你把底层 prompt engineering 写得更严谨。为了提升通过率，来源建议在 prompt 层面做两件事：

```
* Respond only with Python, JSON, or a plain Regex
* Do not add any comments or commentary or explanation
```

还有一个聪明的 pre-fill 技巧 —— 用不指定语言的通用 code fence 作为 assistant 消息开头：

```python
add_assistant_message(messages, "```code")
```

这告诉 Claude 直接开始吐 code content，runner 不必事先知道输出是 Python、JSON 还是 Regex。后面要调用哪个 validator 靠 test case 的 `format` 字段决定，不是靠这个 fence。

---

## 合并 Model + Code 分数

最后一步是把 model grader 分数和 code grader 分数合起来。来源的简单预设是非加权平均：

```python
model_grade = grade_by_model(test_case, output)
model_score = model_grade["score"]
syntax_score = grade_syntax(output, test_case)

score = (model_score + syntax_score) / 2
```

这给内容质量（model grader）和技术正确性（code grader）同等权重。来源也直说：依产品需求不同可调整权重 —— 例如 code-generation 产品，syntax 正确性可能占 70% 权重。

---

## Code Grader 的真正价值

来源收尾给出最关键的定位：分数本身无所谓好坏 —— **重要的是你能不能靠调整 prompt 让它提升**。Code grader 给你量化的方式衡量 prompt engineering 进展，不再靠主观感觉。它们是 prompt 迭代的量化骨干。

两个实务属性要内化：

- **Deterministic** —— 同一输入永远得到同一分数。没有 model grader 那种随机性。
- **便宜** —— 微秒延迟、无 API 成本。每次改 prompt 都能跑全 dataset。

合起来就代表 code grader 是任何 eval pipeline 的第一道防线。code grader 没过？连调用 model grader 都不用浪费。

---

## 常见错误

1. **只用 model grader 验 syntax** —— 浪费 token，还给一个本该 deterministic 的问题引入 variance。
2. **没调用 `.strip()`** —— 前后有空白的合法 payload 会 fail，false negative 污染指标。
3. **test case 缺 `format` 字段** —— runner 无法 route 到正确的 validator。
4. **catch 裸 `Exception`** —— 掩盖 grader 代码本身的 bug；一律 catch 特定 parser exception。
5. **没跟 model grader 平均** —— 代码正确性必要但不充分，还需要内容质量。
6. **一组权重用到底** —— 不同产品看重 syntax vs 质量的比例不同；权重要调。

> **关键洞察**
>
> Code graders 是 prompt evaluation 的便宜、deterministic 骨干。它们不能评"味道"，但能用微秒的时间免费抓出每一个坏 payload。搭 model grader（评味道）取平均 —— 你就拥有一个可以在每次 prompt 改动上跑、而不会烧钱的综合指标。

---

## CCA 考试相关性

- **D3（Evaluation）**：Code graders 是混合 eval pipeline 的 deterministic 那一半。会考何时用 code vs model grader、以及如何合并分数。
- **D5（Enterprise Deployment）**：Deterministic 评分适合塞进 prompt 的 CI/CD —— 便宜、快、够可靠，每个 PR 都能跑。
- 注意："你要验证 AI 产生的 JSON / Python / Regex"→ 永远是 code grader，绝对不是 model grader。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Code grading 验证哪两个面向？ | Format（只能返回指定 code 类型）和 Valid Syntax（能实际 parse）。 |
| 成功的 `validate_json` 返回什么分数？ | 10 |
| 失败的 `validate_python` 返回什么分数？ | 0 |
| 哪个 Python 模块用来 parse Python code？ | `ast` —— 具体是 `ast.parse(text.strip())`。 |
| `validate_regex` 捕捉哪个 exception？ | `re.error` |
| Dataset 必须带哪个字段让 runner 知道用哪个 validator？ | `format` —— 值像 `"python"`、`"json"`、`"regex"`。 |
| 哪个 assistant prefill 技巧能鼓励输出纯 code 又不指定语言？ | `` add_assistant_message(messages, "```code") `` |
| 来源如何合并 model grader 和 code grader 分数？ | 非加权平均：`(model_score + syntax_score) / 2`。 |
| 为什么绝对 code-grader 分数无所谓好坏？ | 因为重要的是能不能靠 prompt 调整让它提升 —— 看方向不看绝对值。 |
| Code grader 相对 model grader 的两大优势？ | Deterministic（同输入同分数）和极便宜（微秒、无 API 成本）。 |
