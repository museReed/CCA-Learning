# Temperature — 工程深度解析

| 項目 | 細節 |
|------|------|
| 考試領域 | D5 — Enterprise Deployment (20%) |
| Task Statements | 5.1（模型設定）、5.3（production 模式）、5.4（evaluation 與可靠度） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 11 |

---

## 一句話總結

Temperature 是一個 sampling 參數（0.0–1.0），控制 Claude 下一個 token 機率分布的銳利或平滑程度——低值讓輸出確定、事實取向，高值讓輸出多變、具創意。

---

## Claude 實際上怎麼產生文字

理解 temperature 前，先看三步驟生成迴圈：

1. **Tokenization**——輸入被切成 tokens（subword 單位）
2. **Prediction**——模型對所有可能的下一個 token 計算機率分布
3. **Sampling**——從這個分布抽一個 token 加到輸出。重複，直到模型輸出 stop token 或達到 `max_tokens`

對於以「What do you think?」結尾的 prompt，分布可能長這樣：

| 候選下一個 token | 機率 |
|-----------------|------|
| " about" | 30% |
| " would" | 20% |
| " of" | 10% |
| ... | ... |

模型挑一個、接上去，再跑整個迴圈產生下一個 token。Temperature 就是調整步驟 3 的旋鈕。

---

## Temperature 在數學上做什麼

Temperature 在 softmax 前對 logits（pre-softmax 分數）做 rescale。

- **Temperature = 0** → 分布坍縮成 argmax。永遠挑機率最高的 token。輸出幾乎確定性（實務上——不計 tie-break）
- **Temperature = 1** → 直接用原始分布。Claude 從完整機率質量抽樣，產生多變輸出
- **介於 0 和 1 之間** → 中間銳化程度。高機率 token 仍然被偏好，但低機率的也有合理機會

把它想成「信心旋鈕」。0 的時候你只信最好的那個猜測；1 的時候你讓多樣性進來。

---

## 三個 Temperature 區段

不同的產品行為需要不同區段。課程定義了三個：

### 低（0.0 – 0.3）——確定性任務

當答案範圍窄、事實很重要時使用。

- 事實性 Q&A
- Coding 輔助
- 資料抽取 / 分類
- 內容審核
- 任何要餵給下游 parser 的場景

### 中（0.4 – 0.7）——結構化創意

當你要連貫、有用、帶點自然變化的輸出時使用。

- Summarization
- 教育內容
- 問題解決
- 有約束的創意寫作

### 高（0.8 – 1.0）——發散式生成

當目標是多樣性與新穎時使用。

- Brainstorming
- 行銷文案
- 虛構 / 笑話生成
- 發想 session

把區段和任務對上。內容審核系統開 temperature 1.0 是 bug。Brainstorming 工具開 temperature 0.0 很無趣。

---

## 把 Temperature 加進 chat 函式

接著 Lesson 09 的 `chat()` helper，把 `temperature` 加成第一級參數：

```python
from anthropic import Anthropic

client = Anthropic()

def chat(messages, system=None, temperature=1.0):
    params = {
        "model": "claude-sonnet-4-5",
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
    }
    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message.content[0].text
```

和 Lesson 09 版本的唯一差別是新的 `temperature=1.0` kwarg 和對應的 `params` 條目。注意 `temperature` **永遠**被傳入——和 `system` 不同，它不需要條件處理，因為 API 直接接受 float 值。

---

## 觀察效果

用兩個極端生成電影點子：

```python
messages = [{"role": "user", "content": "Give me a one-sentence movie idea."}]

print(chat(messages, temperature=0.0))
# "A time-traveling archaeologist must prevent ancient artifacts from being stolen."

print(chat(messages, temperature=1.0))
# 每次執行差異很大——不同主題、角色、情節
```

在 `0.0` 你常常每次拿到一樣的答案。在 `1.0` 每次呼叫都會拿到明顯不同的答案。這就是為什麼非確定性流程的整合測試必須把 `temperature=0` 釘住，或用 LLM-as-judge evals，不能用 exact-match assertion。

---

## Temperature 不是保證

兩個關鍵警告：

1. **Temperature 0 在不同 API 版本或 infra 上不嚴格確定性**。Tie-break、KV-cache 效應、backend routing 都可能產生罕見變異。如果你需要精確確定性，把低 temperature 搭配確定性 evaluation（對多次抽樣做 exact-match，不是單次呼叫）
2. **高 temperature 不保證新穎**。就算 1.0，Claude 可能還是會重複常見措辭，因為那些 token 在分布裡還是主導。Temperature 改變機率；它不會發明新 token

---

## Temperature 和其他 Sampling 參數

Temperature 是幾個 sampling 控制之一。Anthropic API 也支援 `top_p`（nucleus sampling），把分布在累積機率門檻處截斷。課程聚焦 temperature 因為它最直覺；實務上，production 系統通常把 `top_p` 留在預設，只調 temperature。

**經驗法則**：一次只調一個 sampling 參數。`temperature` 和 `top_p` 一起調，會讓輸出很難推理。

---

## 常見錯誤

1. **在抽取 pipeline 用高 temperature**——如果下游 code 預期結構化 JSON，temperature 1.0 是 parse error 溫床
2. **在創意任務用 temperature 0**——輸出變得重複無趣，使用者立刻察覺
3. **假設 temperature 0 是 bit-exact 可重現**——不是的；infra 層級的 nondeterminism 可能導致罕見變異
4. **在調 prompt 之前先調 temperature**——品質最大的槓桿是 prompt + system prompt；temperature 是微調旋鈕，不是第一層修復
5. **完全忘了設 temperature**——全部預設 1.0 會讓結構化任務的測試不穩定、production 行為不一致

> **Key Insight**
>
> Temperature 是政策決策，不是效能決策。它編碼的是你產品能接受多少變異。依使用者期望選區段：使用者要*那個*答案（低）、*一個好*答案（中）、還是*很多不同*答案（高）？然後每個 endpoint 或 feature 鎖死——不要讓它飄動。

---

## CCA 考試重點

- **D5 (Enterprise Deployment)**：temperature 是核心 production 設定參數。預期會考給定情境該用哪個 temperature 區段（抽取 vs brainstorming）
- **D5.3（evaluation 與可靠度）**：確定性 evaluation pipelines 需要釘住 temperature——考試可能問可重現性
- 注意「如何讓 Claude 輸出在資料抽取任務上保持一致？」這種情境——答案是低 temperature（加上結構化 prompting），不是重試

---

## Flashcards

| 題目 | 答案 |
|------|------|
| Claude `temperature` 參數的有效範圍？ | 0.0 到 1.0，含端點 |
| Temperature 0 在機制上是什麼意思？ | Claude 每一步都挑機率最高的下一個 token——實際是 argmax，產生近確定性輸出 |
| Temperature 1 在機制上是什麼意思？ | 直接從完整機率分布 sampling，產生多變且具創意的輸出 |
| 資料抽取該用哪個 temperature 區段？ | 低（0.0–0.3）——確定性和事實忠實度很重要 |
| Brainstorming 該用哪個 temperature 區段？ | 高（0.8–1.0）——目標是多樣性與新穎 |
| Summarization 該用哪個 temperature 區段？ | 中（0.4–0.7）——結構化但帶自然變化 |
| Temperature 0 是 bit-exact 可重現嗎？ | 不是——infra 層級 nondeterminism 會造成罕見變異；是近確定性，不是保證 |
| 文字生成的三個步驟是？ | Tokenization → Prediction（機率分布）→ Sampling（挑下一個 token）|
| 為什麼不該在調 prompt 前先調 temperature？ | Prompt 是第一層品質槓桿；temperature 是微調旋鈕，修不了壞 prompt |
