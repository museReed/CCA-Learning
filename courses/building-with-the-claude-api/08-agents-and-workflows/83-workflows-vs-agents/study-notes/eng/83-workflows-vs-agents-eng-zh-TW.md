# Workflows vs Agents — Engineering 深度解析

| 項目 | 內容 |
|------|------|
| 考試領域 | D1 — Agentic Coding & Architecture (22%);D5 — Enterprise Deployment (20%) |
| Task Statements | 1.1 (agent vs workflow 架構)、1.2 (agentic loop)、5.1 (production pattern 選型) |
| 來源 | building-with-the-claude-api / 08-agents-and-workflows / Lesson 83 |

---

## 一句話總結

**預設選 workflow,真的不得已才升級到 agent** —— Workflow 對已知問題給你可靠度和可預測性,agent 對開放問題給你彈性,工程師的工作就是挑能解決使用者問題的最便宜 pattern。

---

## 定義

### Workflow

**一連串預先定義的 Claude 呼叫**,解決已知問題。開發者把控制流寫死:「先用 model A 分類,再用 model B 草稿,再用 model C review。」每個呼叫的工作都很窄。

```python
def summarize_ticket(ticket):
    category = classify(ticket)               # Step 1
    summary = summarize(ticket, category)     # Step 2
    priority = score_priority(summary)        # Step 3
    return {"category": category, "summary": summary, "priority": priority}
```

### Agent

**目標 + 工具集** 交給 Claude,runtime 由它決定呼叫什麼、什麼順序。沒有寫死的序列。

```python
messages = [{"role": "user", "content": user_goal}]
while True:
    response = client.messages.create(model="claude-sonnet-4-5", tools=tools, messages=messages)
    if response.stop_reason == "end_turn": break
    # 處理 tool_use,loop 繼續
```

差異在於 **控制流由誰擁有**:開發者(workflow)還是 Claude(agent)。

---

## 完整比較表

| 維度 | Workflow | Agent |
|------|----------|-------|
| **彈性** | 低 — 只處理你寫死的形狀 | 高 — 組合 tools 處理新情境 |
| **可靠度** | 高 — 每步都窄、都經測試 | 較低 — 開放式規劃可能出錯 |
| **每任務成本** | 低 — token 數可預測、可 cache | 高 — 多次 loop 迭代、更多 token |
| **Latency** | 低 — 固定次數的循序呼叫 | 變動 — 看 Claude 跑幾次 loop |
| **Debuggability** | 高 — 你知道哪一步失敗 | 低 — 軌跡不確定、難以重現 |
| **可預測性** | 高 — 相同輸入永遠相同序列 | 低 — Claude 對相似輸入可能選不同 tool 鏈 |
| **Eval 成本** | 中等 — 逐步單元測試 | 高 — 必須 eval emergent 行為,需更多測試案例 |
| **Upfront design 成本** | 高 — 必須列出全部流程 | 較低 — 設計工具箱而非流程 |
| **最佳使用情境** | 摘要、分類、抽取、翻譯、合規流程 | 寫程式助手、創意內容、混亂資料上的開放問答 |
| **最差使用情境** | 開放或多變的使用者請求 | 有已知序列的窄重複任務 |

---

## 來源原文的優缺點

### Workflow 優點

- Claude 一次只關注一個子任務,通常準確度更高
- 更容易 eval 和測試——你知道每一步
- 執行更可預測、更可靠
- 適合解決定義良好的問題

### Workflow 缺點

- 彈性低很多——只能解特定任務類型
- UX 較受限——你必須知道精確輸入
- 需要更多前期規劃和設計工作

### Agent 優點

- 更彈性的 UX
- 可以用沒預期的方式組合 tool
- 能處理設計時沒想到的新情境
- 需要時可以問使用者補充資訊

### Agent 缺點

- 任務完成率比 workflow 低
- 較難 instrument、測試、eval
- 行為較不可預測

---

## 決策框架

Anthropic 的建議很直白:**預設 workflow。只有 workflow 真的解不了的問題才用 agent。**

每個 AI 功能都走這個 checklist:

```
1. 我能事先列出所有使用者流程嗎?
   YES -> workflow
   NO  -> 繼續

2. 這個任務是純轉換(input -> output)沒有分支嗎?
   YES -> workflow
   NO  -> 繼續

3. 使用者的請求會用多元、不可預測的方式表達嗎?
   YES -> 繼續評估 agent
   NO  -> workflow

4. 正確動作取決於目前環境 state 嗎?
   YES -> agent(搭配 environment inspection)
   NO  -> workflow

5. 我負擔得起 agent 的 cost、latency、eval 複雜度嗎?
   YES -> agent
   NO  -> 拆成更小的 workflow
```

這不是純粹主義測試——混合系統存在。常見 pattern:外層是 workflow,路由到內層 agent 處理彈性步驟,其餘用 workflow 作護欄。

---

## Cost 和 Latency 數學

一個 workflow 有 3 個固定 model 呼叫,每個 ~1000 tokens:

- **Tokens**:每任務 ~3000(deterministic)
- **Latency**:3 次循序呼叫,總共 ~3-6 秒
- **Cost**:可預測、可用 prompt caching cache

同樣任務用 agent 解,3-10 次 loop 迭代:

- **Tokens**:每任務 ~3000 到 ~30000(變動)
- **Latency**:3-10 次 round trip,總共 ~5-30 秒
- **Cost**:同樣輸出品質下是 workflow 的 1x 到 10x

如果 eval 顯示 workflow 95% 準確、agent 96% 準確,agent 的彈性大概不值那 5-10x 的 cost 倍數。挑能達成品質門檻的最便宜 pattern。

---

## Production 裡的混合 Pattern

真實 production 系統很少只選一種。常見混合:

| Pattern | 運作方式 | 範例 |
|---------|---------|------|
| **Workflow 路由到 agent** | 便宜的分類 workflow 決定請求是否需要 agent 等級彈性 | Support ticket router:FAQ -> workflow,新 bug -> agent |
| **Agent 帶 workflow sub-step** | Agent 把 workflow 當成一個 tool 呼叫 | 寫程式 agent 呼叫 deterministic「run_tests」workflow |
| **Agent 帶 workflow 安全閘門** | Agent 提出動作,workflow 執行前驗證 | AI 交易員提案,workflow 檢查合規規則 |
| **失敗升級** | 先 workflow 失敗再 agent | 結構化資料抽取,schema 變動時回退到 agent |

這些 pattern 讓你對 80% 流量保持 workflow 的可靠度,同時保留 agent 彈性給難搞的 20%。

---

## 常見錯誤

1. **Agent-washing** — 因為 agent 聽起來潮就把所有東西做成 agent,然後接下來整個專案週期都在跟 cost 和 eval 打架。
2. **Workflow 僵化** — 把每個變異都塞成 if-tree 的一條分支,最後變成無法維護的義大利麵。這就是該升級到 agent 的時候。
3. **Agent 跳過 eval** — 因為 agent 軌跡變動,你需要 **更大更多元** 的 eval set,不是更小。
4. **忽略 latency 稅** — 每次 agent loop 都是一次 round trip。話多的 agent 即使每個呼叫都很快,整體感覺就是慢。
5. **沒量每成功任務的 cost** — 「每次呼叫的 token 數」是錯的 metric;「每次驗證成功的 cost」才是重點。

> **Key Insight**
>
> Anthropic 的建議很俐落:預設 workflow,只有無法事先決定步驟時才選 agent。使用者不在乎你做了個聰明的 agent,他們只在乎產品穩定好用。把 pattern 對齊到問題(而且誠實面對你實際有的是哪種)是 agentic 產品裡最高槓桿的架構決策。

---

## CCA 考試關聯

- **D1 (Agentic Coding & Architecture)**:會考「什麼時候用 agent vs workflow」。背熟 trade-off 表。
- **D5 (Enterprise Deployment)**:Cost、latency、eval 複雜度、debuggability 是面對 production 的 trade-off。每個軸該知道哪個 pattern 勝出。
- 考題提示字:「varied requests」「unpredictable」「combine tools creatively」 -> agent;「well-defined steps」「known flow」「compliance」「cheapest predictable」 -> workflow。

---

## Flashcards

| 正面 | 背面 |
|------|------|
| Anthropic 的預設建議是什麼? | 預設用 workflow;只有 workflow 解不了的問題才用 agent。 |
| Workflow 跟 agent 的控制流由誰擁有? | Workflow:開發者寫死序列。Agent:Claude 在 runtime 決定序列。 |
| 列出三個 workflow 勝 agent 的維度。 | 可靠度、cost、latency、debuggability、可預測性(任三)。 |
| 列出三個 agent 勝 workflow 的維度。 | 彈性、新情境覆蓋、使用者驅動對話 UX、較低 upfront design cost(任三)。 |
| 為什麼 agent 比 workflow 難 eval? | Agent 軌跡不確定——你不能單步測試;必須對大量案例測 emergent 行為。 |
| 舉一個混合 pattern 把兩者結合。 | Workflow router 把簡單案例送到 workflow 分支,難案例送到 agent。 |
| 比「每次呼叫 token 數」更重要的 cost metric 是什麼? | 每次驗證成功的 cost——agent 用更多 token 但若能解 workflow 解不了的案例,每成功 cost 反而可能更低。 |
| 決策框架的第一個問題是什麼? | 我能事先列出所有使用者流程嗎?能 -> workflow。 |
