# Getting an API Key — PM Perspective（繁體中文）

| 項目 | 內容 |
|------|------|
| Exam Domain | D3 — Claude Code Configuration (20%) 主要；D5 — Enterprise Deployment (20%) 次要 |
| Task Statements | 3.1（API key lifecycle）、3.2（workspace 策略）、5.3（生產環境 secret 衛生） |
| Source | building-with-the-claude-api / 01-api-fundamentals / Lesson 05 |

---

## One-Liner

Anthropic API key 就是你 Claude feature 的信用卡——把建立、workspace 選擇、rotation 當成產品問題（不只是 devops 的事），才不會在凌晨三點收到爆表的帳單或安全事故通知。

---

## Mental Model：銀行保險箱的鑰匙

Anthropic API key 就像銀行保險箱的鑰匙：

| 特性 | 保險箱鑰匙 | Anthropic API Key |
|------|----------|-------------------|
| 只給一次 | 從銀行拿回家 | 建立時只顯示一次 |
| 不能恢復 | 掉了就鑽開箱子換新的 | 掉了就刪了重建 |
| 銀行能驗證但不能複製 | 銀行只存 hash，不存鑰匙 | Anthropic 只存 hash，不存明文 |
| 誰有誰就能用 | 進箱子不驗身分 | 誰有 key 誰就能花你的預算 |

PM 的啟示：**把 key 當現金處理**。你不會把實體現金放 repo 裡——API key 也一樣。

---

## 為什麼 PM 該關心 key

| 顧慮 | PM 影響 |
|------|--------|
| 成本歸屬 | 沒有 workspace 紀律，你無法回答「Feature X 花了多少錢」 |
| 安全事故 | Key 洩漏是真金白銀的曝險，會出現在下個月的帳單 |
| Launch 卡關 | 合規團隊在企業 launch 前會問「key 存哪裡」 |
| 團隊 onboarding | 新工程師需要 key，流程必須文件化且可稽核 |
| 供應商審查 | 企業客戶在採購階段會問你的 key 管理 |

**沒有 key 管理計畫就推 Claude feature，等於推了一個偽裝成 feature 的成本與安全負債。**

---

## Product Use Cases：Workspace 策略就是產品決策

### 一產品一 workspace

多個產品共用一個 Anthropic 帳號、需要乾淨的產品級計費時用。

| 好處 | 代價 |
|------|------|
| 「Product A 花了多少 Claude 錢」一目瞭然 | 工程師要在 console 切 workspace |
| 每產品配額可以防止互相搶資源 | 管理負擔略增 |

### 一環境一 workspace

營運安全很重要時用（生產幾乎都要）。

| 好處 | 代價 |
|------|------|
| Dev 失控的 loop 抽不到生產配額 | 要 rotate 的 key 變多 |
| 事故時 blast radius 很清楚 | 要監控的稽核面更多 |

### 共用 Default workspace

只有 prototype 和教學才用。

| 好處 | 代價 |
|------|------|
| 零設定 | 沒有成本歸屬；任何事故影響一切 |

---

## Key 生命週期：PM 檢查清單

```
     建立
      │
      ▼
     複製一次 → 存 secret manager
      │
      ▼
     文件化：名字、擁有者、用途
      │
      ▼
     用在 service → 監控用量/成本
      │
      ▼
     定期 rotate（季度）
      │
      ▼
     Service 退役時刪掉
```

每一步都是產品問題：

| 步驟 | PM 責任 |
|------|--------|
| 建立 | 確保命名慣例存在並被遵守 |
| 儲存 | PRD 裡規定用 secret manager |
| 文件化 | 維護 key 庫存（誰擁有什麼） |
| 監控 | 不尋常開銷的 dashboard |
| Rotate | 把每季 rotate 排成工程 ticket |
| 刪除 | Feature 退役時有 decommission checklist |

---

## PM Decision Framework

新的 Claude feature 提案時跑這份問卷：

| 問題 | 預設答案 |
|------|---------|
| 這把 key 要放哪個 workspace？ | 專屬的 per-feature 或 per-env workspace |
| 誰是這把 key 的人類擁有者？ | Feature team 裡指名的工程師，不是「整個 team」 |
| 生產環境這把 key 存哪？ | Secret manager（不要放裸機器的環境變數） |
| 怎麼 rotate？ | 每季，排定 ticket |
| 洩漏怎麼知道？ | 帳單異常告警 + GitHub secret scanning |
| 事故 playbook 是什麼？ | Console 刪掉 → 建新 → redeploy → post-mortem |

---

## Common PM Mistakes

1. **把 key 管理當成純 devops 的事** —— 它是產品問題，因為它驅動成本歸屬、安全姿態、launch 就緒度。
2. **跳過命名慣例** —— 第一個事故打來時，「My Key 3」會讓你花好幾小時在當偵探。
3. **沒編 rotation 的工時** —— Rotation 沒排進 roadmap 就不會發生，排成每季。
4. **Dev 跟 prod 共用一個 workspace** —— 今天省十分鐘，之後被失控帳單打回來。
5. **沒有事故 playbook** —— Key 洩漏時，team 在壓力下臨時想 rotate 步驟，浪費時間。

> **Key Insight**
>
> Key 管理不是小事——它是偽裝成水電的產品設計決策。為 Claude feature 失眠的 PM，通常都是那些把 API key 當成「工程師的事」的人，然後被一個 4 萬美金的 dev 失控帳單或 public repo 洩漏事件狠狠教訓。**把「workspace + key 計畫」加進 feature launch checklist，就放在「隱私審查」旁邊。**

---

## CCA Exam Relevance

- **D3（Claude Code Configuration）**：建立流程、儲存模式、恢復路徑（不能恢復，只能 rotate）。
- **D5（Enterprise Deployment）**：Workspace 作為計費/配額邊界；key 衛生作為生產需求。
- 情境觸發：「Key 洩漏到 public repo」→ Console 刪掉、建新、redeploy、檢討怎麼洩漏的。

---

## Flashcards

| Front | Back |
|-------|------|
| 為什麼 PM 該關心 API key 管理？ | 它驅動成本歸屬、安全事故、企業 launch 就緒度 |
| Anthropic API key 的心智模型是什麼？ | 保險箱鑰匙——只給一次、不能恢復、銀行只存 hash |
| 「workspace 要選哪個」PM 預設答案是什麼？ | 專屬的 per-feature 或 per-env workspace，不是共用 Default |
| Key 庫存要記什麼？ | 名字、擁有者（指名的人）、用途、workspace、rotation 日期 |
| Key 洩漏的正確事故處理是什麼？ | Console 刪掉 → 建新 → redeploy → post-mortem |
| 為什麼季度 rotate 需要 PM 背書？ | 因為 rotation 沒排進 roadmap 就不會發生 |
| Dev 跟 prod 共用一個 workspace 有什麼問題？ | Dev 失控 loop 會抽乾生產配額，造成客戶事故 |
| PM 該在 feature launch checklist 加什麼？ | Workspace + key 計畫，和隱私與安全審查放一起 |
