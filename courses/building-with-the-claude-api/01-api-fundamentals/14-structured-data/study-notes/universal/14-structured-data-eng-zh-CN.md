# Structured Data — 工程深度解析

| 项目 | 细节 |
|------|------|
| 考试领域 | D5 — Enterprise Deployment (20%) 主要；D2 — Tool Design & MCP Integration (18%) 次要 |
| Task Statements | 5.3（production 模式）、1.3（prompt engineering）、2.1（tools 的结构化输出） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 14 |

---

## 一句话总结

当你需要 Claude 返回纯 JSON、代码或其他结构化数据，而不要它自然包在输出外面的闲聊时，你用 **assistant message prefilling** 加 **stop sequences** 强制 Claude 进入你要的格式。

---

## 问题：Claude 天生想帮忙

请 Claude 给 JSON，你通常会拿到这种东西：

````
```json
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["running"]
  }
}
```

This rule captures EC2 instance state changes when instances start running.
````

JSON 是对的，但包在 markdown code fences 里**而且**后面还接一段英文解释。对于 AWS EventBridge 规则生成器——用户预期按「复制」就能直接粘到 AWS console——这是糟糕 UX。用户得手动选 JSON、去掉 fences、记得不要包含解释。

这不是 Claude 的 bug——这是 Claude 默认 helpful 行为漏进了你需要 raw data 的场景。你单靠 `temperature` 或更好的 system prompt 修不了；Claude 还是会想解释自己。

---

## 解法：Prefill + Stop Sequences

诀窍是给 Claude 一个**已经起头的 assistant message**——就像 Claude 已经用你要的开头起手了。然后用 **stop sequence** 在 Claude 加上任何尾巴文字之前切断生成。

```python
messages = []

add_user_message(messages, "Generate a very short event bridge rule as json")
add_assistant_message(messages, "```json")

text = chat(messages, stop_sequences=["```"])
```

流程：

1. **User message**——告诉 Claude 要生成什么
2. **Prefilled assistant message**——`` ```json `` 让 Claude 以为自己已经开了 markdown code block。接下来生成的 tokens 必须延续那个 block
3. **Claude 生成 JSON 内容**——被 prefill 约束成吐 JSON（不是散文）
4. **Stop sequence**——当 Claude 试图用 `` ``` `` 关闭 code block，API 立刻停止生成。尾巴解释永远不会出现

结果是干净 JSON，没有 markdown fences、没有解说、没有东西要 strip：

```json
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["running"]
  }
}
```

---

## 为什么 Prefilling 有效

Claude 是下一个 token 的预测器。当你交给它一个 assistant message，它把那个 message 当成「我已经说过的」，从那继续。如果 prefill 是 `` ```json ``，那么统计上下一个 tokens 压倒性地可能是 valid JSON——因为训练分布中，markdown fence 开头后面就是 JSON。

Prefilling 是一种 prompt engineering，绕过「helpful 前言」本能。Claude 无法致歉或介绍它的答案，因为从它的视角它已经开始写 JSON 了。没有「code block 之前」可以回去。

---

## 为什么 Stop Sequences 重要

没有 stop sequence，Claude 会开心地把 code block 结束然后继续写解释。Prefill 解决输出的开头；stop sequence 解决结尾。

`stop_sequences` 是一串 strings，当 Claude 吐出它们时，API 立刻结束生成。吐出的 stop sequence 本身**不**包含在输出里。所以你传 `stop_sequences=["```"]`，Claude 试着关 fence 时，生成就在那些 backticks 出现在返回文字之前停止。

你可以传最多（少数几个）stop sequences，任何一个都会触发结束。常见用法：

- `"```"` 停在结束的 markdown fence
- `"\n\n"` 停在段落断行
- 通过 prefill 注入的自定义 delimiters

---

## 把它串进 chat() helper

接着 Lessons 09 和 11 的 chat 函数，加上 `stop_sequences`：

```python
from anthropic import Anthropic

client = Anthropic()

def chat(messages, system=None, temperature=1.0, stop_sequences=None):
    params = {
        "model": "claude-sonnet-4-5",
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
    }
    if system:
        params["system"] = system
    if stop_sequences:
        params["stop_sequences"] = stop_sequences

    message = client.messages.create(**params)
    return message.content[0].text

def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})

def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})
```

和 `system` 一样的条件模式：只在有提供时才插入 `stop_sequences`。

---

## 解析结果

因为 Claude 在开头 fence 后立刻生成 JSON 内容，raw 返回文字通常含前置空白或换行。parse 前先 strip：

```python
import json

text = chat(messages, stop_sequences=["```"])
clean_json = json.loads(text.strip())
```

或者你可以更积极，用 regex 抽第一个 `{...}` 或 `[...]` block，但 `text.strip() + json.loads()` 涵盖常见场景。

---

## 不只 JSON

这个技巧和格式无关。任何需要干净结构化输出的地方都能用：

| 目标格式 | Prefill | Stop sequence |
|---------|---------|---------------|
| JSON | `` ```json `` | `` ``` `` |
| Python code | `` ```python `` | `` ``` `` |
| YAML | `` ```yaml `` | `` ``` `` |
| CSV | `` ```csv `` | `` ``` `` |
| 条列清单 | `- ` | `\n\n` |
| 自定义 XML | `<output>` | `</output>` |

模式是：找出 Claude 自然会包在内容外面的东西，用开头当 prefill，用结尾当 stop sequence。

---

## Prefill + Stop Sequences vs Tool Use

对 JSON 来说，还有第二个（通常更好的）方法：用 **tool use** 强制 Claude 把结构化数据当作 tool input 返回。这给你 schema 验证过的 JSON object，不用 prefill 把戏——Claude 把 JSON 当成 tool call，SDK 帮你 parse 好。

什么时候用哪个？

| 方法 | 最适合 |
|------|--------|
| Prefill + stop sequence | 快速、无 schema 的结构化输出；简单脚本；非 JSON 格式如 Python 或 CSV |
| Tool use (input schema) | Production JSON 生成，要 schema 验证、type 保证、agent 式集成 |

Lesson 14 讲 prefill 技巧因为它是基础——任何格式都能用，不需学 tool use protocol。Tool use 在课程后面介绍。

---

## 常见错误

1. **忘了 stop sequence**——prefill 解决开头，但没 `stop_sequences` Claude 会关 fence 并加解释
2. **Prefill 和 stop sequence 的 fence 不匹配**——如果你 prefill `` ```json `` 但 stop 在 `"\n\n"`，你会把结束 fence 抓进输出
3. **parse 前不 strip whitespace**——`json.loads(text)` 遇到前置换行会 fail；永远先 `text.strip()`
4. **期待 100% valid JSON 而没有 retry loop**——Claude 偶尔还是会吐 malformed JSON；production code 要 catch `json.JSONDecodeError` 并用较低 temperature retry
5. **有 tool use 可用时还用 prefill**——production JSON 用 tool use + `input_schema` 免费拿到验证

> **Key Insight**
>
> Prefilling 是约束 Claude 输出格式最老、最简单的方法。有效是因为 Claude 是序列预测器——你把话塞进它嘴里，它就会从那些话继续，而不会重启它惯常的前言。搭配 `stop_sequences` 切掉尾巴解释，你不需要 tool use 或 JSON mode 就能精确控制输出结构。每位 CCA 考生都该对这个模式滚瓜烂熟。

---

## CCA 考试重点

- **D5.3（production 模式）**：prefill + stop sequences 是从 Claude 抽干净结构化输出的标准模式
- **D2 (Tool Design)**：这堂课暗示 tool use 是 JSON 生成的下一级方法；考试可能对比两者
- **D1.3（结构化输出的 prompt engineering）**：预期考如何强制特定输出格式而不加解释文字

---

## Flashcards

| 题目 | 答案 |
|------|------|
| 哪两个技巧结合起来强制 Claude 进入特定输出格式？ | Assistant message prefilling 和 stop sequences |
| Assistant message prefilling 做什么？ | 加一个 assistant message 含部分响应（如 `` ```json ``），让 Claude 从那里继续而不是从 preamble 重新开始 |
| `stop_sequences` 做什么？ | 列出 strings，Claude 吐出时立刻结束生成——stop sequence 本身不包含在输出里 |
| 抽纯 JSON 典型的 prefill + stop sequence 是什么？ | Prefill 用 `` ```json ``，stop 在 `` ``` `` |
| Prefilling 在机制上为什么有效？ | Claude 是下一个 token 预测器；给定部分 assistant message，它从那继续而不是重新自我介绍 |
| 调用 `json.loads()` 前要对结果做什么？ | Strip 前后空白——`text.strip()`——移除 Claude 在开头 fence 后吐的换行 |
| 什么时候 tool use 比 prefill + stop sequences 更好？ | Production JSON 生成，当 schema 验证和 type 保证重要时 |
| 这个技巧对非 JSON 格式有用吗？ | 有用——Python、YAML、CSV、条列清单、自定义 XML。模式是 prefill 开头，stop 结尾 |
| 只靠 prefill 不加 stop sequence 的主要风险是什么？ | Claude 会关 code block 然后加英文解释，打败 prefill 的意义 |
