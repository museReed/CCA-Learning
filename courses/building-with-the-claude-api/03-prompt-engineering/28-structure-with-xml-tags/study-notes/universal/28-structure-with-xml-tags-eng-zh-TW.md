# 使用 XML 標籤建立結構 — Engineering Deep Dive

| 項目 | 內容 |
|------|------|
| 考試領域 | D3 — Evaluation & Iteration（20%）主；D2 — Tool Design（18%）次 |
| 任務陳述 | 3.1（提升可靠性的 prompt 設計）、2.2（結構化內容區塊） |
| 來源 | building-with-the-claude-api / 03-prompt-engineering / Lesson 28 |

---

## 一句話總結

XML 標籤是 prompt 字串裡的明確分隔符，讓 Claude 能清楚區分哪些 token 是指令、哪些是資料、哪些是範例——是 prompt engineering 裡最簡單也最可靠的結構化技巧。

---

## 問題：一鍋 Token 粥

當你把指令、20 頁銷售紀錄、以及使用者問題全部串接成一個 prompt 字串時，Claude 看到的是一長串沒有區隔的 token 序列。沒有邊界，它只能從文字本身推敲結構，而這種推敲非常脆弱：

- 指令會滲進資料
- 資料會滲進範例
- Claude 可能會「執行」原本只是要分析的內容

課程原文的描述是：Claude「有時會難以判斷哪些文字屬於同一組、各段落又分別代表什麼」。

XML 標籤透過在 token 流裡插入明確的標記解決這個問題。`<sales_records>...</sales_records>` 告訴 Claude：這裡面的東西是同一個邏輯單位，而且是某種特定類型。

---

## 經典範例

課程中的運動員飲食計畫 prompt：

```
<athlete_information>
- Height: 6'2"
- Weight: 180 lbs
- Goal: Build muscle
- Dietary restrictions: Vegetarian
</athlete_information>

Generate a meal plan based on the athlete information above.
```

這裡有三件事同時發生：

1. **語意群組**——身高、體重、目標、飲食限制被綁在同一個容器內。
2. **角色分離**——指令（"Generate a meal plan..."）放在標籤外，完全不會有「這是資料還是指令」的模糊地帶。
3. **可指涉性**——指令可以直接說「the athlete information above」，剛好對應標籤名稱。

---

## 程式碼 vs 文件：最戲劇化的例子

課程裡第二個例子：請 Claude 用提供的文件 debug 程式碼。如果把兩者混成一坨（"Not Great" 版本），幾乎無法讓 Claude 分辨哪些是程式碼、哪些是散文。"Better" 版本用標籤把兩段內容包起來：

```
<my_code>
def calculate_total(items):
    return sum(item.price for item in items)
</my_code>

<docs>
Item class 有三個欄位：name (str)、price (float)、quantity (int)。
價格以整數分（cents）儲存。
</docs>

請使用上述文件，找出 my_code 中的 bug。
```

現在 Claude 知道：把 `my_code` 當 Python 解析，把 `docs` 當作 ground truth，找出不一致的地方（文件說 price 是整數分，但程式碼直接把總和當成最終價格）。

---

## 標籤名稱很重要

課程明確表示你不需要用「官方」XML。標籤名稱是語意提示，所以越具體越好：

| 弱 | 強 | 理由 |
|----|----|------|
| `<data>` | `<sales_records>` | 告訴 Claude 是什麼類型的資料 |
| `<info>` | `<athlete_information>` | 避免與其他 info 混淆 |
| `<text>` | `<customer_review>` | 隱含領域（情感、語氣） |
| `<input>` | `<my_code>` / `<docs>` | 區分並列的內容 |

原則：如果你能在程式裡幫這個變數取名，就用同一個名字當標籤。

---

## 何時 XML 標籤最有價值

直接引用課程內容，XML 最有用的場景是：

- 包含大量 context 或資料
- 混合不同類型的內容（程式碼、文件、資料）
- 你想特別清楚地標示內容邊界
- 複雜 prompt 中內插多個變數

對於單行 prompt（「翻譯成法文：hello」），加標籤是殺雞用牛刀。收益會隨 prompt 複雜度放大。

---

## Python 模式：安全的字串內插

```python
from anthropic import Anthropic

client = Anthropic()

athlete_info = """- Height: 6'2"
- Weight: 180 lbs
- Goal: Build muscle
- Dietary restrictions: Vegetarian"""

prompt = f"""<athlete_information>
{athlete_info}
</athlete_information>

Generate a meal plan based on the athlete information above."""

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}],
)
```

注意內插點完全在標籤內。使用者提供的資料沒辦法滲到指令區——這也能降低 prompt injection 的攻擊面：攻擊者塞進來的文字最多污染 `athlete_information`，標籤外的指令仍然固定。

---

## 常見錯誤

1. **模糊的標籤名稱**——用 `<data>` 或 `<text>` 而不是 `<sales_records>`。Claude 無法利用沒被給出的提示。
2. **忘記關閉標籤**——沒有關閉的 `<my_code>` 可能讓 Claude 把後面全部都當成程式碼。
3. **多段內容不加標籤**——把程式碼和文件並排放但沒有分隔符，正是課程警告的失敗場景。
4. **對簡單 prompt 過度加標籤**——為一句話的請求加 XML 只會增加雜訊。
5. **以為 XML 會改變輸出格式**——標籤只管輸入結構；要 Claude 回 XML 還需要另外的指令。

> **Key Insight**
>
> XML 標籤是 prompt engineering 裡最便宜的可靠性升級。它不會改變 Claude 能做什麼，但會改變它「多有把握地」區分你的指令和你的資料。在 CCA 考試中，任何牽涉「大量 context」「多種資料類型」或「Claude 把指令和內容搞混」的情境，都指向 XML 結構化這個答案。

---

## CCA 考試相關性

- **D3（Evaluation & Iteration）**：當 eval 顯示 Claude 誤判輸入時，XML 加標籤是第一道改善手段。預期會有情境題描述某個 prompt 失敗，原因是邊界模糊。
- **D2（Tool Design）**：同樣的分隔原則也適用於 `tool_use` / `tool_result` 的 content blocks——結構化通道優於自由字串。
- 留意題目中出現「interpolating」或「mixing」——標準答案是「用 XML 標籤分隔每一段」。

---

## Flashcards

| 正面 | 反面 |
|------|------|
| XML 標籤在 prompt 裡解決什麼問題？ | 用明確邊界讓 Claude 能區分指令、資料、範例。 |
| XML 標籤名稱必須符合某個標準嗎？ | 不需要——偏好用 `<sales_records>`、`<athlete_information>` 這類描述性自訂名稱。 |
| XML 標籤何時最有價值？ | 大量 context、多種內容類型、內插多個變數的複雜 prompt。 |
| 舉一組弱/強標籤名稱對比 | 弱：`<data>`；強：`<sales_records>`。 |
| 程式碼 vs 文件的經典範例長什麼樣？ | 用 `<my_code>` 包程式碼、`<docs>` 包文件，再請 Claude 依文件找 bug。 |
| XML 標籤會改變回應的輸出格式嗎？ | 不會——它只管輸入結構；輸出格式需要另外指令。 |
| XML 標籤對 prompt injection 有什麼好處？ | 使用者資料被關在標籤內，標籤外的指令較難被覆寫。 |
| 簡單 prompt 也要用 XML 嗎？ | 不一定——收益隨複雜度放大；一行 prompt 加標籤反而是雜訊。 |
