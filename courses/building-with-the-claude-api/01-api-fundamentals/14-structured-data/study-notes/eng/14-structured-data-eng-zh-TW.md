# Structured Data — 工程深度解析

| 項目 | 細節 |
|------|------|
| 考試領域 | D5 — Enterprise Deployment (20%) 主要；D2 — Tool Design & MCP Integration (18%) 次要 |
| Task Statements | 5.3（production 模式）、1.3（prompt engineering）、2.1（tools 的結構化輸出） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 14 |

---

## 一句話總結

當你需要 Claude 回傳純 JSON、程式碼或其他結構化資料，而不要它自然包在輸出外面的閒聊時，你用 **assistant message prefilling** 加 **stop sequences** 強制 Claude 進入你要的格式。

---

## 問題：Claude 天生想幫忙

請 Claude 給 JSON，你通常會拿到這種東西：

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

JSON 是對的，但包在 markdown code fences 裡**而且**後面還接一段英文解釋。對於 AWS EventBridge 規則產生器——使用者預期按「複製」就能直接貼到 AWS console——這是糟糕 UX。使用者得手動選 JSON、去掉 fences、記得不要包含解釋。

這不是 Claude 的 bug——這是 Claude 預設 helpful 行為漏進了你需要 raw data 的情境。你單靠 `temperature` 或更好的 system prompt 修不了；Claude 還是會想解釋自己。

---

## 解法：Prefill + Stop Sequences

訣竅是給 Claude 一個**已經起頭的 assistant message**——就像 Claude 已經用你要的開頭起手了。然後用 **stop sequence** 在 Claude 加上任何尾巴文字之前切斷生成。

```python
messages = []

add_user_message(messages, "Generate a very short event bridge rule as json")
add_assistant_message(messages, "```json")

text = chat(messages, stop_sequences=["```"])
```

流程：

1. **User message**——告訴 Claude 要生成什麼
2. **Prefilled assistant message**——`` ```json `` 讓 Claude 以為自己已經開了 markdown code block。接下來生成的 tokens 必須延續那個 block
3. **Claude 生成 JSON 內容**——被 prefill 約束成吐 JSON（不是散文）
4. **Stop sequence**——當 Claude 試圖用 `` ``` `` 關閉 code block，API 立刻停止生成。尾巴解釋永遠不會出現

結果是乾淨 JSON，沒有 markdown fences、沒有解說、沒有東西要 strip：

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

## 為什麼 Prefilling 有效

Claude 是下一個 token 的預測器。當你交給它一個 assistant message，它把那個 message 當成「我已經說過的」，從那繼續。如果 prefill 是 `` ```json ``，那麼統計上下一個 tokens 壓倒性地可能是 valid JSON——因為訓練分布中，markdown fence 開頭後面就是 JSON。

Prefilling 是一種 prompt engineering，繞過「helpful 前言」本能。Claude 無法致歉或介紹它的答案，因為從它的視角它已經開始寫 JSON 了。沒有「code block 之前」可以回去。

---

## 為什麼 Stop Sequences 重要

沒有 stop sequence，Claude 會開心地把 code block 結束然後繼續寫解釋。Prefill 解決輸出的開頭；stop sequence 解決結尾。

`stop_sequences` 是一串 strings，當 Claude 吐出它們時，API 立刻結束生成。吐出的 stop sequence 本身**不**包含在輸出裡。所以你傳 `stop_sequences=["```"]`，Claude 試著關 fence 時，生成就在那些 backticks 出現在回傳文字之前停止。

你可以傳最多（少數幾個）stop sequences，任何一個都會觸發結束。常見用法：

- `"```"` 停在結束的 markdown fence
- `"\n\n"` 停在段落斷行
- 透過 prefill 注入的自訂 delimiters

---

## 把它串進 chat() helper

接著 Lessons 09 和 11 的 chat 函式，加上 `stop_sequences`：

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

和 `system` 一樣的條件模式：只在有提供時才插入 `stop_sequences`。

---

## 解析結果

因為 Claude 在開頭 fence 後立刻生成 JSON 內容，raw 回傳文字通常含前置空白或換行。parse 前先 strip：

```python
import json

text = chat(messages, stop_sequences=["```"])
clean_json = json.loads(text.strip())
```

或者你可以更積極，用 regex 抽第一個 `{...}` 或 `[...]` block，但 `text.strip() + json.loads()` 涵蓋常見情況。

---

## 不只 JSON

這個技巧和格式無關。任何需要乾淨結構化輸出的地方都能用：

| 目標格式 | Prefill | Stop sequence |
|---------|---------|---------------|
| JSON | `` ```json `` | `` ``` `` |
| Python code | `` ```python `` | `` ``` `` |
| YAML | `` ```yaml `` | `` ``` `` |
| CSV | `` ```csv `` | `` ``` `` |
| 條列清單 | `- ` | `\n\n` |
| 自訂 XML | `<output>` | `</output>` |

模式是：找出 Claude 自然會包在內容外面的東西，用開頭當 prefill，用結尾當 stop sequence。

---

## Prefill + Stop Sequences vs Tool Use

對 JSON 來說，還有第二個（通常更好的）方法：用 **tool use** 強制 Claude 把結構化資料當作 tool input 回傳。這給你 schema 驗證過的 JSON object，不用 prefill 把戲——Claude 把 JSON 當成 tool call，SDK 幫你 parse 好。

什麼時候用哪個？

| 方法 | 最適合 |
|------|--------|
| Prefill + stop sequence | 快速、無 schema 的結構化輸出；簡單腳本；非 JSON 格式如 Python 或 CSV |
| Tool use (input schema) | Production JSON 生成，要 schema 驗證、type 保證、agent 式整合 |

Lesson 14 講 prefill 技巧因為它是基礎——任何格式都能用，不需學 tool use protocol。Tool use 在課程後面介紹。

---

## 常見錯誤

1. **忘了 stop sequence**——prefill 解決開頭，但沒 `stop_sequences` Claude 會關 fence 並加解釋
2. **Prefill 和 stop sequence 的 fence 不匹配**——如果你 prefill `` ```json `` 但 stop 在 `"\n\n"`，你會把結束 fence 抓進輸出
3. **parse 前不 strip whitespace**——`json.loads(text)` 遇到前置換行會 fail；永遠先 `text.strip()`
4. **期待 100% valid JSON 而沒有 retry loop**——Claude 偶爾還是會吐 malformed JSON；production code 要 catch `json.JSONDecodeError` 並用較低 temperature retry
5. **有 tool use 可用時還用 prefill**——production JSON 用 tool use + `input_schema` 免費拿到驗證

> **Key Insight**
>
> Prefilling 是約束 Claude 輸出格式最老、最簡單的方法。有效是因為 Claude 是序列預測器——你把話塞進它嘴裡，它就會從那些話繼續，而不會重啟它慣常的前言。搭配 `stop_sequences` 切掉尾巴解釋，你不需要 tool use 或 JSON mode 就能精確控制輸出結構。每位 CCA 考生都該對這個模式滾瓜爛熟。

---

## CCA 考試重點

- **D5.3（production 模式）**：prefill + stop sequences 是從 Claude 抽乾淨結構化輸出的標準模式
- **D2 (Tool Design)**：這堂課暗示 tool use 是 JSON 生成的下一級方法；考試可能對比兩者
- **D1.3（結構化輸出的 prompt engineering）**：預期考如何強制特定輸出格式而不加解釋文字

---

## Flashcards

| 題目 | 答案 |
|------|------|
| 哪兩個技巧結合起來強制 Claude 進入特定輸出格式？ | Assistant message prefilling 和 stop sequences |
| Assistant message prefilling 做什麼？ | 加一個 assistant message 含部分回應（如 `` ```json ``），讓 Claude 從那裡繼續而不是從 preamble 重新開始 |
| `stop_sequences` 做什麼？ | 列出 strings，Claude 吐出時立刻結束生成——stop sequence 本身不包含在輸出裡 |
| 抽純 JSON 典型的 prefill + stop sequence 是什麼？ | Prefill 用 `` ```json ``，stop 在 `` ``` `` |
| Prefilling 在機制上為什麼有效？ | Claude 是下一個 token 預測器；給定部分 assistant message，它從那繼續而不是重新自我介紹 |
| 呼叫 `json.loads()` 前要對結果做什麼？ | Strip 前後空白——`text.strip()`——移除 Claude 在開頭 fence 後吐的換行 |
| 什麼時候 tool use 比 prefill + stop sequences 更好？ | Production JSON 生成，當 schema 驗證和 type 保證重要時 |
| 這個技巧對非 JSON 格式有用嗎？ | 有用——Python、YAML、CSV、條列清單、自訂 XML。模式是 prefill 開頭，stop 結尾 |
| 只靠 prefill 不加 stop sequence 的主要風險是什麼？ | Claude 會關 code block 然後加英文解釋，打敗 prefill 的意義 |
