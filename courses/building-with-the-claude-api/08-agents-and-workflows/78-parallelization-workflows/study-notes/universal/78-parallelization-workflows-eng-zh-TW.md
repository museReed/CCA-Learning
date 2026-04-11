# Parallelization Workflows — 工程深度解析

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Coding & Architecture(22%)— 主要 |
| 任務陳述 | 1.2(agentic 模式 — parallelization)、5.2(production workflow 部署)|
| 來源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 78 |

---

## 一句話總結

Parallelization workflow 把一個複雜任務拆成多個獨立子任務並行執行(通常用 `asyncio.gather`),再用最後一次 LLM 呼叫匯總結果 — 這是 LLM 推理版的「fan-out / fan-in」模式。

---

## 這個模式解決什麼問題

單一 prompt 處理複雜決策時,會逼 Claude 同時兼顧很多準則。課程的標準範例:材料推薦系統,要從 metal、polymer、ceramic、composite、elastomer、wood 六種材料中挑一個適合某零件圖片的。

天真做法(一個 prompt):
```
「看這個零件,從以下材料挑最好的:metal、polymer、ceramic、composite、elastomer、wood。
考慮強度、重量、成本、可製造性、抗腐蝕……」
```

問題:
1. Claude 要把注意力分散到 6 種材料 × 5+ 個準則 = 30+ 個考量
2. 沒有任何單一材料被深入分析
3. 難以最佳化 — 你沒辦法單獨 A/B 測「metal prompt」
4. 想加第 7 種材料得重寫整個 prompt

---

## Parallelization 模式

出自 Anthropic「Building Effective Agents」部落格,parallelization 有兩種變體:

| 變體 | 用途 | 範例 |
|------|------|------|
| **Sectioning** | 把任務拆成獨立子任務,每個聚焦一個面向 | 材料推薦(每種材料一個 LLM)|
| **Voting** | 跑*同一個*任務多次,取多數決 | Moderation(「這內容安全嗎?」)N 個投票者 |

兩者都是平行跑 N 個 LLM 呼叫再匯總。差別在於每個子任務的輸入/prompt 是*不同*(sectioning)還是*相同*(voting)。

---

## 標準結構

```
       ┌─→ 子任務 1 ──┐
input ─┼─→ 子任務 2 ──┼─→ aggregator ─→ 最終輸出
       └─→ 子任務 N ──┘
```

1. **Split** — 把一個輸入轉成 N 個聚焦子任務
2. **Fan-out** — 並行跑 N 個子任務(`asyncio.gather`)
3. **Fan-in / Aggregate** — 把所有子任務結果餵給最後一次 LLM 呼叫做單一決策
4. **Return** — 把匯總結果回給使用者

---

## Python 實作(asyncio.gather)

```python
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

MATERIALS = ["metal", "polymer", "ceramic", "composite", "elastomer", "wood"]

async def evaluate_material(image_b64: str, material: str) -> dict:
    """每種材料一個專門的 LLM 呼叫。"""
    prompt = f"""
你是材料工程師,評估 {material} 是否適合圖中零件。
只聚焦在 {material} 的準則:

<criteria>
{MATERIAL_CRITERIA[material]}
</criteria>

回傳 JSON: {{"material": "{material}", "score": 0-10, "rationale": "..."}}
"""
    resp = await client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64",
                                             "media_type": "image/jpeg",
                                             "data": image_b64}},
                {"type": "text", "text": prompt},
            ],
        }],
    )
    return parse_json(resp.content[0].text)

async def aggregate(evaluations: list[dict]) -> str:
    """Fan-in:把所有專門評估合併成最終選擇。"""
    prompt = f"""
以下是同一個零件的 6 份獨立材料評估:

{json.dumps(evaluations, indent=2, ensure_ascii=False)}

挑出最佳材料並說明理由。
"""
    resp = await client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text

async def material_recommender(image_b64: str) -> str:
    # fan-out
    tasks = [evaluate_material(image_b64, m) for m in MATERIALS]
    evaluations = await asyncio.gather(*tasks)
    # fan-in
    return await aggregate(evaluations)
```

實作重點:
- 用 `AsyncAnthropic`(不是 `Anthropic`),呼叫才能 await
- `asyncio.gather(*tasks)` 讓 fan-out 階段真正並行
- 每個子任務小、聚焦、可獨立測試
- Aggregator 一次看到所有結構化結果

---

## 好處

1. **聚焦注意力** — 每次 Claude 呼叫專注一個面向,精確度提升
2. **獨立最佳化** — 改 metal prompt 不會影響其他;per-material A/B 測試
3. **可擴充** — 加第 7 種材料只要多加一個 prompt 檔,其他六個零風險
4. **可靠度** — 每次呼叫認知負擔低,輸出更一致
5. **延遲** — N 次平行呼叫 ≈ 最慢那一次的時間,而不是 N × 平均

---

## 不該用 Parallelization 的時機

- 後續步驟*依賴*前面輸出的任務(改用 chaining — Lesson 79)
- 子任務無法有意義地分開(「摘要這篇文章」無法平行化)
- 成本比延遲更重要:parallelization 是*增加*呼叫次數,不是減少,token 花費會乘以 N

---

## Voting 變體

同樣的基礎設施也能跑 voting:讓*同一個* prompt 跑 N 次,用多數決匯總。適合安全關鍵決策:

```python
async def moderation_vote(text: str, n: int = 5) -> bool:
    tasks = [is_safe(text) for _ in range(n)]
    votes = await asyncio.gather(*tasks)
    return sum(votes) > n / 2  # 多數決
```

Voting 用成本換可靠度 — 經典的 ensemble 技術套到 LLM 上。

---

## 常見錯誤

1. **忘了 aggregation 步驟。** 平行子任務本身不會產生決策,你還需要一個最後的 LLM(或規則)aggregator。
2. **讓子任務互相依賴。** 如果子任務 2 需要子任務 1 的輸出,那是 chain 不是 parallel,`asyncio.gather` 會 race 或 deadlock。
3. **用 `Anthropic` 而不是 `AsyncAnthropic`。** Sync client 會 block,結果變成序列化而非平行化。
4. **忽略每個任務的 timeout。** 一個慢呼叫會拖住整個 gather。用 `asyncio.wait_for` 或 `gather(return_exceptions=True)`。
5. **Token 成本爆炸。** 每個平行呼叫都是獨立 API 帳單。控制 N,可以 cache 就 cache。

---

> **關鍵洞察**
>
> Parallelization 是「聚焦注意力」的 workflow — 每次 Claude 呼叫只負責一個窄責任,單次分析更好,總延遲也更低。代價是 N 倍 API 花費,所以適用於品質比成本重要、或延遲是瓶頸時。考試記得兩種變體:**sectioning**(不同子任務)與 **voting**(同一任務跑 N 次)。

---

## CCA 考試關聯

- **D1(22%)主要**: 預期有情境題要你辨認 parallelization(關鍵字:「split」、「run simultaneously」、「fan out」、「aggregate」)。
- **D5(20%)次要**: Production 模式 — `asyncio.gather`、延遲/成本權衡。
- 訊號字:「split into multiple independent evaluations」、「run simultaneously」、「aggregate results」、「fan-out / fan-in」。
- 兩種變體都要懂(sectioning vs voting)。

---

## Flashcards

| 題目 | 答案 |
|------|------|
| 什麼是 parallelization workflow? | 把一個任務拆成獨立子任務並行執行,再匯總結果 |
| Parallelization 的兩種變體? | Sectioning(不同子任務用同一輸入)與 voting(同一任務跑 N 次)|
| 執行 fan-out 階段的 Python 原語? | `asyncio.gather(*tasks)` 配 `AsyncAnthropic` client |
| 為什麼 parallelization 比一個 mega-prompt 好? | 聚焦注意力、可獨立最佳化、可擴充、更可靠 |
| Parallelization 的成本取捨? | N 倍 API 花費換取品質與延遲 |
| 什麼時候*不*該用 parallelization? | 子任務互相依賴時(改用 chaining)、或成本比品質更重要時 |
| Voting 模式用來做什麼? | 安全/共識決策 — 同一 prompt 跑 N 次取多數決(例如 moderation)|
| 能讓 Anthropic 呼叫並行的 client class? | `AsyncAnthropic` — Anthropic SDK 的 async 版 client |
