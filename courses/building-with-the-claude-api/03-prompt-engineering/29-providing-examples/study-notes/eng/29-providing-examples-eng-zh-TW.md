# 提供範例 — Engineering Deep Dive

| 項目 | 內容 |
|------|------|
| 考試領域 | D3 — Evaluation & Iteration（20%）主；D2 — Tool Design（18%）次 |
| 任務陳述 | 3.1（提升可靠性的 prompt 設計）、2.2（結構化內容區塊） |
| 來源 | building-with-the-claude-api / 03-prompt-engineering / Lesson 29 |

---

## 一句話總結

Few-shot prompting（one-shot / multi-shot）是把「輸入/輸出」範例丟給 Claude，而不是用文字描述想要的行為——這是處理 corner case、格式和語氣最有效的 prompt engineering 技巧。

---

## 為什麼「示範」比「描述」更有效

指令是「告訴」，範例是「展示」。當任務的細微之處很難用文字精確表達——諷刺、特定 JSON 結構、公司風格——示範預期行為比描述它更可靠。課程原文稱 few-shot 是「你最常用的 prompt engineering 技巧之一」。

課程裡的經典失敗案例是帶有諷刺意味的情感分析。這則推文：

> "Yeah, sure, that was the best movie I've seen since 'Plan 9 from Outer Space'"

表面看起來像正面（best、since、sure），但實際上是諷刺、是負面。不管你寫多短的「請偵測諷刺」指令都難以穩定修好，但加一個諷刺範例就可以。

---

## 結構化的諷刺範例

課程中改進後的 prompt 包含：

- 一個明確的正面範例：`"Great game tonight!"` → `"Positive"`
- 一個諷刺範例：`"Oh yeah, I really needed a flight delay tonight! Excellent!"` → `"Negative"`
- 解釋為什麼諷刺要被小心處理的 context

關鍵是，這些範例都包在 XML 標籤裡：`<sample_input>` 和 `<ideal_output>`。這直接扣回 Lesson 28——XML 標籤分隔範例輸入、範例輸出和真正的任務。沒有結構的 few-shot 會讓 Claude 猜哪段文字才是「答案」。

```
<example>
  <sample_input>Great game tonight!</sample_input>
  <ideal_output>Positive</ideal_output>
</example>

<example>
  <sample_input>Oh yeah, I really needed a flight delay tonight! Excellent!</sample_input>
  <ideal_output>Negative</ideal_output>
</example>

Classify the following tweet. Sarcasm should be treated as negative.

<tweet>
{user_tweet}
</tweet>
```

---

## One-Shot vs Multi-Shot

直接引用課程：

- **One-shot**——單一範例，足以建立模式
- **Multi-shot**——多個範例，涵蓋不同情境和 edge case

當你需要處理多種 corner case、或示範多種有效的回應類型時用 multi-shot。原則：每多加一個範例，都應該「付清自己的成本」——也就是能覆蓋前面範例沒覆蓋到的失敗模式。

---

## 什麼時候範例是對的工具

根據課程，範例對以下情況特別有用：

- 處理 corner case 或邊緣情境（諷刺、模糊輸入）
- 定義複雜的輸出格式（如特定 JSON 結構）
- 展示精確的風格或語氣
- 示範如何處理模糊輸入

注意共通點：任何「給我看」比「精確描述我要什麼」更快的場景。

---

## 從 Evaluations 收割範例

實務上最重要的一點：當你跑 prompt eval 時，看**得分最高的輸出**，然後把它們升級成 prompt 裡的範例。課程原文明確寫：「找出得 10 分（或你最高分）的回應，把這些輸入/輸出對當作 prompt 的範例」。

這形成一個良性迴圈：

1. 用現有 prompt 跑 eval
2. 找出 Claude 已經產出理想輸出的 case
3. 把那些（input, output）對複製到 prompt 裡當 few-shot 範例
4. 重跑 eval——難 case 的分數應該會上升

這就是 Lesson 29 被放在本章「prompt engineering → evaluation」流程裡的原因：範例和 eval 是同一個迭代迴圈。

---

## 不只是展示，還要解釋

課程強調一個理想範例應該附上「為什麼這是好的」的說明。原文：

```
<ideal_output>
[Your example output here]
</ideal_output>

This example is well-structured, provides detailed information
on food choices and quantities, and aligns with the athlete's
goals and restrictions.
```

範例後面的短註解告訴 Claude 這個輸出「好在哪裡」，而不只是「長什麼樣子」。這有助於 generalization——Claude 學到的是判斷標準，不只是表面形式。

---

## Python 模式

```python
from anthropic import Anthropic

client = Anthropic()

few_shot = """<example>
  <sample_input>Great game tonight!</sample_input>
  <ideal_output>Positive</ideal_output>
</example>

<example>
  <sample_input>Oh yeah, I really needed a flight delay tonight! Excellent!</sample_input>
  <ideal_output>Negative</ideal_output>
</example>

Sarcasm should be treated as negative."""

tweet = "Yeah, sure, that was the best movie I've seen since 'Plan 9 from Outer Space'"

prompt = f"""{few_shot}

Classify the following tweet as Positive or Negative.

<tweet>
{tweet}
</tweet>"""

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=64,
    messages=[{"role": "user", "content": prompt}],
)
```

兩個重點：範例放在真實任務上方，而且範例和真實輸入都用 XML 標籤包起來。

---

## 課程的最佳實踐

- 永遠用 XML 標籤結構化範例
- 明確說明你在展示什麼（「Here is an example input with an ideal response」）
- 範例要針對最常見的失敗 case
- 解釋為什麼範例輸出是理想的
- 範例要跟你的實際任務相關

---

## 常見錯誤

1. **範例沒用 XML 結構**——Claude 得猜哪段是輸入、哪段是輸出、哪段是真正的問題。
2. **挑選太容易的範例**——示範的全是 Claude 已經做得很好的 case，卻忽略真正的失敗模式。
3. **範例和任務飄移**——用的範例接近但不完全等同真實輸入的形狀。
4. **只展示不解釋**——理想輸出沒有註解會讓 Claude 只會「複製」而不是「推理」。
5. **Eval 後沒重新收割範例**——eval set 變了但範例沒更新，prompt 就不再對準難 case。

> **Key Insight**
>
> Few-shot prompting 是 Lesson 28（XML 結構）和 Chapter 04（tool use）之間的橋樑。CCA 考試預期會出現這類情境題：「prompt 能處理正常 case 但在諷刺／JSON 格式／特定語氣上失敗」。答案幾乎都是：加 XML 標籤的範例來覆蓋那些失敗模式，最好來自 eval 分數最高的輸出。

---

## CCA 考試相關性

- **D3（Evaluation & Iteration）**：當 eval 暴露出系統性失敗模式時，few-shot 是主要的迭代手段。「把高分 eval 輸出升級成範例」的迴圈是考點。
- **D2（Tool Design）**：設計嚴格輸出格式（包含 tool-like 行為的 JSON）時，範例比文字描述 schema 更可靠。
- 題目關鍵字：「sarcasm」「specific format」「corner case」「style or tone」——都指向 few-shot 範例。

---

## Flashcards

| 正面 | 反面 |
|------|------|
| 什麼是 few-shot prompting？ | 在 prompt 裡提供輸入/輸出範例對來引導 Claude 回應（one-shot = 1 個範例，multi-shot = 多個）。 |
| 為什麼範例比指令更適合處理諷刺偵測？ | 諷刺很難用文字描述；示範一個諷刺範例比叫 Claude「注意諷刺」更可靠。 |
| 課程為範例使用哪些 XML 標籤？ | `<sample_input>` 和 `<ideal_output>`（實務上外層再包一個 `<example>`）。 |
| 什麼時候該用 multi-shot 而非 one-shot？ | 需要覆蓋多個 edge case 或示範不同有效回應類型時。 |
| 怎麼從 eval 取得好範例？ | 找出得分最高（例如 10/10）的回應，把那些輸入/輸出對升級成 prompt 範例。 |
| 為什麼要解釋範例為什麼是理想的？ | 幫助 Claude 學到背後的判斷標準，而不只是複製表面形式。 |
| 列出四個範例特別有用的情境 | Corner case、複雜輸出格式、特定風格/語氣、模糊輸入。 |
| Lesson 28 和 Lesson 29 的關係是什麼？ | XML 標籤（28）提供結構；範例（29）在結構裡填入示範——設計上就是配套使用。 |
