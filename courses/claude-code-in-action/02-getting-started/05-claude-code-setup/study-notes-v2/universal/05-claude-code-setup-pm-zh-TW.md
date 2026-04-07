# Claude Code Setup — PM Perspective

| Item | Detail |
|------|--------|
| Exam Domain | D3: Claude Code Configuration & Workflows |
| Task Statements | 3.1 (setup is prerequisite) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> 📝 本節所有內容均直接來自官方課程教材。

## One-Liner / TL;DR

Claude Code 在每個主要平台上只需一行終端指令即可安裝——團隊成員可以自助完成，不需要 IT 工單。

## Core Concepts

### 安裝方式

三種平台專屬安裝選項——全部都是一行指令，不需要管理員介入：

| 平台 | 指令 | PM 重點 |
|------|------|---------|
| macOS (Homebrew) | `brew install --cask claude-code` | 一行指令，團隊可自助安裝，無需 IT 工單 |
| macOS, Linux, WSL | `curl -fsSL https://claude.ai/install.sh \| bash` | 通用備案——即使沒有 Homebrew 也能安裝 |
| Windows CMD | `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd` | Windows 團隊成員也支援——下載、安裝、自動清除 |

> 📝
> macOS 使用者有兩條路徑（Homebrew 或 curl 腳本）。這表示無論機器設定如何，onboarding 都不會被阻擋。

### 首次執行與身份驗證

- 安裝完成後，在終端執行 `claude` 會觸發首次身份驗證
- 不需要額外設定步驟——工具會在首次啟動時引導使用者完成驗證

### 完整設定參考

- 官方 quickstart 文件：https://code.claude.com/docs/en/quickstart

### Enterprise / 雲端供應商選項

適用於有合規或資料駐留需求的組織：

| 供應商 | 文件連結 | 何時考慮使用 |
|--------|---------|-------------|
| AWS Bedrock | https://code.claude.com/docs/en/amazon-bedrock | 團隊已在 AWS 上，需要資料留在 AWS 區域 |
| Google Cloud Vertex AI | https://code.claude.com/docs/en/google-vertex-ai | 團隊已在 GCP 上，需要資料留在 GCP 區域 |

## Key Takeaways

1. 零摩擦安裝：macOS、Linux、WSL 和 Windows 各一行指令
2. macOS 提供兩條安裝路徑——onboarding 不會有單點故障
3. Windows 使用下載-執行-清除模式（`curl -o ... && ... && del ...`）——完全自動化
4. 身份驗證內建於首次啟動——不需要額外的憑證佈建步驟
5. 有合規需求的企業團隊可透過 AWS Bedrock 或 Google Cloud Vertex AI 路由

---

# PART 2: Study Aids

> 💡 補充學習資料，非官方課程內容。

## Familiar Analogies

- **一行指令安裝** — 類似從 IT 自助入口安裝 Slack 或 Zoom，但只是一行終端指令。不需要下載頁面，不用拖到 Applications。
- **首次執行驗證** — 類似第一次開啟新 SaaS 工具時要求登入。不需要預先設定。
- **Bedrock/Vertex 選項** — 類似選擇團隊的 Slack 資料存放在美國或歐洲區域。同樣的產品，不同的託管方式以滿足合規。
- **三平台指令** — 類似供應商同時提供 Windows、Mac 和 Linux 安裝包——全平台覆蓋代表沒有團隊成員會被阻擋。

## CCA Exam Connection

> 💡
> 作為 PM，你需要知道：
> - 安裝是自助式的（每個平台一行指令）——影響推廣規劃
> - 驗證在首次執行時自動發生——不需要 IT 佈建步驟
> - Bedrock/Vertex 作為企業選項存在——與採購討論相關
> - 哪個指令對應哪個 OS——預期至少有一題考平台與指令的配對

## Anti-Patterns

| Anti-Pattern | 為何錯誤 | 正確做法 |
|-------------|---------|---------|
| 規劃多步驟 IT 協助的推廣流程 | 安裝只是一行指令——過度工程化推廣流程 | 在 Slack 訊息中分享每個平台的對應指令 |
| 假設 Windows 團隊成員無法使用 Claude Code | Windows 透過 CMD 完全支援 | 分享 Windows curl 指令 |
| 在 onboarding 文件中要求手動設定 API key | 驗證由工具在首次執行時處理 | 只需告知團隊安裝後執行 `claude` |
| 在供應商評估時忽略 Bedrock/Vertex | 企業團隊可能因合規需要這些選項 | 在採購檢查清單中納入雲端供應商選項 |

## Practice Questions

**Q1.** 你正在將 Claude Code 推廣到一個跨平台工程團隊（macOS 和 Windows）。一位 Windows 開發者回報他們沒有 Homebrew。你應該如何建議？

- A) 請 IT 在他們的 Windows 機器上安裝 Homebrew
- B) 告知他們 Claude Code 僅支援 macOS
- C) 分享 Windows CMD 指令：`curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd`
- D) 請他們換用 Mac

> 📝
> **答案：C。** Claude Code 提供專用的 Windows CMD 安裝指令。Homebrew 是 macOS 套件管理器，在 Windows 上不可用。Claude Code 支援 macOS、Linux、WSL 和 Windows。

**Q2.** 你的組織要求所有 AI 工具必須通過現有的 AWS 基礎設施路由以滿足合規。你應該推薦哪條設定路徑？

- A) 使用直接 Anthropic 驗證的標準安裝
- B) 按照 https://code.claude.com/docs/en/amazon-bedrock 文件設定 AWS Bedrock 整合
- C) 透過 `pip install claude-code` 安裝以取得 AWS 相容性
- D) Claude Code 無法與 AWS 基礎設施搭配使用

> 📝
> **答案：B。** AWS Bedrock 是兩個企業雲端供應商選項之一（另一個是 Google Cloud Vertex AI），允許透過現有雲端基礎設施路由 Claude Code 以滿足合規需求。
