# Claude Code Setup — PM 觀點

| 項目 | 細節 |
|------|---------|
| 考試涵蓋 | D3 — Effective Claude Code Usage（佔考試 30%） |
| Task Statements | 3.1 (CLAUDE.md hierarchy — awareness level) |
| 課程來源 | claude-code-in-action / 02-getting-started / Lesson 05（純文字課程） |

---


![Installation Methods Platform Grid](../../visuals/installation-methods-platform-grid-zh-TW.svg)
*圖：各平台安裝方式。*

## TL;DR

Claude Code 是一個命令列工具，開發者用一行指令即可安裝。PM 需要知道它是 CLI-only（沒有 GUI）、支援所有主流平台，且可設定透過企業雲端供應商（AWS Bedrock、Google Cloud Vertex）路由以符合合規要求。

---

## 為什麼 PM 該關注

1. **部署規劃** — 了解安裝需求有助於評估工程團隊的上手時間
2. **企業合規** — Cloud provider 選項（Bedrock、Vertex）決定 Claude Code 是否符合組織的資料駐留與安全政策
3. **無 GUI = 開發者原生** — 這不是你在瀏覽器中 demo 的產品；它活在終端機裡

---

## 商業類比

| 概念 | 商業類比 |
|---------|-----------------|
| CLI-only 工具 | 像 Slack 只有聊天沒有 email 備案 — 它強制採用原生工作流 |
| Cloud provider 路由 | 像選擇付款走 Stripe 直連還是透過銀行的支付閘道 |
| 首次啟動驗證 | 像存取任何企業 SaaS 前的 SSO 登入 |

---

## 決策框架：Cloud Provider 選擇

| 因素 | 直接 Anthropic API | AWS Bedrock | Google Cloud Vertex |
|--------|---------------------|-------------|-------------------|
| 設定複雜度 | 最低 | 中等 | 中等 |
| 企業帳單 | 獨立 Anthropic 帳單 | 合併至 AWS 帳單 | 合併至 GCP 帳單 |
| 資料駐留 | Anthropic 基礎設施 | 你的 AWS 區域 | 你的 GCP 區域 |
| 最適合 | 個人開發者、小團隊 | AWS 優先組織 | GCP 優先組織 |

---

## 練習題

### 情境：企業推廣規劃

你的工程主管問將 Claude Code 推廣到 50 人團隊需要多長時間。根據本課內容，哪個答案最準確？

- A. 數週 — 每個開發者需要客製化設定
- B. 每個開發者幾分鐘 — 就是一行 CLI 安裝指令加驗證
- C. 完全取決於 cloud provider 設定
- D. Claude Code 需要 IT 中央集中安裝到所有機器上

<details><summary>答案</summary>

**B** — Claude Code 用一行指令安裝，只需首次啟動驗證。安裝本身微不足道。

然而，如果組織需要 Bedrock/Vertex 路由，IT 或 DevOps 需要一次性完成額外的雲端設定（不是每個開發者都需要）。這不會改變每個開發者的安裝時間。

**PM 重點**：不要高估推廣複雜度。瓶頸在於 cloud provider 設定（如果需要的話），而不是工具安裝本身。
</details>
