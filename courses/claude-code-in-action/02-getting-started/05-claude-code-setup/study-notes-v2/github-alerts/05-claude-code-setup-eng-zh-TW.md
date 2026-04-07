# Claude Code Setup — Engineering Deep Dive

| Item | Detail |
|------|--------|
| Exam Domain | D3: Claude Code Configuration & Workflows |
| Task Statements | 3.1 (setup is prerequisite) |
| Source | Anthropic Skilljar — Claude Code in Action |

---

# PART 1: Official Course Content

> [!NOTE] 本節所有內容均直接來自官方課程教材。

## One-Liner / TL;DR

Claude Code 透過單一終端指令即可在 macOS、Linux、WSL 或 Windows 上安裝，首次執行時自動觸發身份驗證。

## Core Concepts

### 安裝方式

提供三種平台專屬安裝指令：

| 平台 | 指令 |
|------|------|
| macOS (Homebrew) | `brew install --cask claude-code` |
| macOS, Linux, WSL | `curl -fsSL https://claude.ai/install.sh \| bash` |
| Windows CMD | `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd` |

> [!NOTE]
> macOS 通用腳本（`curl ... install.sh`）在沒有 Homebrew 的 macOS 上也能使用，因此 Mac 使用者有兩種安裝選項。

### 首次執行與身份驗證

- 安裝完成後，在終端執行 `claude`
- 首次啟動會自動觸發身份驗證流程

### 完整設定參考

- 官方 quickstart 文件：https://code.claude.com/docs/en/quickstart

### Enterprise / 雲端供應商選項

企業部署的替代驗證後端：

| 供應商 | 文件連結 |
|--------|---------|
| AWS Bedrock | https://code.claude.com/docs/en/amazon-bedrock |
| Google Cloud Vertex AI | https://code.claude.com/docs/en/google-vertex-ai |

## Key Takeaways

1. 每個支援平台都只需一行指令即可安裝
2. macOS 有兩條安裝路徑：Homebrew cask 或通用 curl 腳本
3. Windows 使用下載-執行-清除的模式（`curl -o ... && ... && del ...`）
4. 身份驗證在首次執行 `claude` 時自動觸發
5. 企業團隊可透過 AWS Bedrock 或 Google Cloud Vertex AI 取代直接的 Anthropic 驗證

---

# PART 2: Study Aids

> [!TIP] 補充學習資料，非官方課程內容。

## Familiar Analogies

- **Homebrew cask install** — 與 `brew install --cask visual-studio-code` 相同模式。Cask = GUI/CLI 應用程式（非 library）。
- **curl pipe to bash** — 通用的 Node.js/Rust 安裝器模式（`nvm`、`rustup`）。下載腳本並一次執行完畢。
- **Windows 三步驟** — 類似下載 `.exe` 安裝程式、執行後刪除。`&&` 串接確保每個步驟成功後才執行下一步。
- **首次執行驗證** — 類似 `gh auth login`（GitHub CLI）或 `aws configure`——工具在首次使用時引導完成憑證設定。

## CCA Exam Connection

> [!TIP]
> Setup 是所有實作域的先決條件。預期考題會測試：
> - 特定 OS 對應的正確安裝指令
> - 身份驗證是透過執行 `claude` 觸發（不是獨立的 `claude auth` 步驟）
> - Bedrock/Vertex 是企業替代方案（個人使用不需要）

## Anti-Patterns

| Anti-Pattern | 為何錯誤 | 正確做法 |
|-------------|---------|---------|
| 執行 `npm install -g claude-code` | 這是舊的安裝方法，不再是推薦路徑 | 使用 `brew install --cask claude-code` 或官方 curl 腳本 |
| 對 curl 安裝腳本使用 `sudo` | 官方腳本已處理權限；`sudo` 可能導致檔案擁有者問題 | 以一般使用者身份執行 curl 指令 |
| 首次執行時跳過身份驗證 | Claude Code 未驗證無法運作 | 執行 `claude` 並完成驗證提示 |
| 誤認 Bedrock/Vertex 為必要設定 | 它們是可選的企業後端 | 直接 Anthropic 驗證是預設方式 |

## Practice Questions

**Q1.** 團隊中有位開發者使用 macOS 但未安裝 Homebrew。他應該使用哪個指令安裝 Claude Code？

- A) `brew install --cask claude-code`
- B) `npm install -g @anthropic/claude-code`
- C) `curl -fsSL https://claude.ai/install.sh | bash`
- D) `pip install claude-code`

> [!NOTE]
> **答案：C。** 通用 curl 腳本適用於 macOS、Linux 和 WSL，不需要 Homebrew。選項 A 需要 Homebrew。選項 B 和 D 不是官方安裝方式。

**Q2.** 安裝 Claude Code 後，開始使用的下一步是什麼？

- A) 執行 `claude auth login` 設定憑證
- B) 在終端執行 `claude`——首次啟動會觸發身份驗證
- C) 手動設定 `ANTHROPIC_API_KEY` 環境變數
- D) 從 Applications 資料夾開啟 Claude Code GUI 應用程式

> [!NOTE]
> **答案：B。** 在終端執行 `claude` 即可觸發首次身份驗證流程。標準設定不需要獨立的 auth 指令或手動 API key 設定。
