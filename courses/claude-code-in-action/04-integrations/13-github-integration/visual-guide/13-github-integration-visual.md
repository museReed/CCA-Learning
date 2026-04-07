# GitHub Integration — Claude Code GitHub 整合 — 影片逐幀學習指南

| 項目 | 內容 |
|------|------|
| 課程 | claude-code-in-action / 04-integrations / 13-github-integration |
| 影片 | GitHub Integration |
| 字幕數 | 69 段 |
| 格式 | 每段字幕一張截圖 + 雙語字幕（英/中） |

---

### [00:00:00] 第 1 段

![frame 1](./frames/frame_001.jpg)

> **EN:** CloudCode has an official GitHub integration that allows CloudCode to
>
> **ZH:** Claude Code 有一個官方的 GitHub 整合功能，允許 Claude Code

---

### [00:00:03] 第 2 段

![frame 2](./frames/frame_002.jpg)

> **EN:** run inside of a GitHub action.
>
> **ZH:** 在 GitHub Actions 內部運行。

---

### [00:00:05] 第 3 段

![frame 3](./frames/frame_003.jpg)

> **EN:** You can set up this integration by running slash install GitHub app.
>
> **ZH:** 你可以透過執行 `/install-github-app` 指令來設定這個整合。

---

### [00:00:10] 第 4 段

![frame 4](./frames/frame_004.jpg)

> **EN:** This will walk you through a couple of steps.
>
> **ZH:** 這將引導你完成幾個步驟。

---

### [00:00:12] 第 5 段

![frame 5](./frames/frame_005.jpg)

> **EN:** First, you'll need to install the CloudCode app on GitHub.
>
> **ZH:** 首先，你需要在 GitHub 上安裝 Claude Code 應用程式。

---

### [00:00:15] 第 6 段

![frame 6](./frames/frame_006.jpg)

> **EN:** Next, you'll need to add in an API key.
>
> **ZH:** 接下來，你需要新增一個 API key。

---

### [00:00:17] 第 7 段

![frame 7](./frames/frame_007.jpg)

> **EN:** And then after this, a pull request will be automatically generated.
>
> **ZH:** 完成之後，系統會自動產生一個 pull request。

---

### [00:00:21] 第 8 段

![frame 8](./frames/frame_008.jpg)

> **EN:** This pull request adds in two different GitHub actions.
>
> **ZH:** 這個 pull request 會新增兩個不同的 GitHub Actions。

---

### [00:00:25] 第 9 段

![frame 9](./frames/frame_009.jpg)

> **EN:** The first action adds in mentioning support.
>
> **ZH:** 第一個 action 新增了提及支援。

---

### [00:00:27] 第 10 段

![frame 10](./frames/frame_010.jpg)

> **EN:** So from an issue or a pull request, you can mention Cloud with at Cloud and give Cloud
>
> **ZH:** 這樣你就可以在 issue 或 pull request 中，用 `@claude` 提及 Claude Code，

---

### [00:00:32] 第 11 段

![frame 11](./frames/frame_011.jpg)

> **EN:** some kind of task to run.
>
> **ZH:** 並給它分配某種任務來執行。

---

### [00:00:34] 第 12 段

![frame 12](./frames/frame_012.jpg)

> **EN:** The second action adds in support for reviewing pull requests.
>
> **ZH:** 第二個 action 新增了審查 pull request 的支援。

---

### [00:00:37] 第 13 段

![frame 13](./frames/frame_013.jpg)

> **EN:** So whenever you create a pull request, CloudCode will automatically run and review the proposed
>
> **ZH:** 每當你建立一個 pull request 時，Claude Code 就會自動執行並審查

---

### [00:00:41] 第 14 段

![frame 14](./frames/frame_014.jpg)

> **EN:** changes.
>
> **ZH:** 提議的變更。

---

### [00:00:42] 第 15 段

![frame 15](./frames/frame_015.jpg)

> **EN:** Both of these actions can be customized, and you can also add in additional actions to
>
> **ZH:** 這兩個 action 都可以自訂，你也可以新增額外的 action，

---

### [00:00:46] 第 16 段

![frame 16](./frames/frame_016.jpg)

> **EN:** trigger based on other types of events.
>
> **ZH:** 以便根據其他類型的事件來觸發。

---

### [00:00:48] 第 17 段

![frame 17](./frames/frame_017.jpg)

> **EN:** Let me show you how you can customize the mentioning feature.
>
> **ZH:** 讓我示範如何自訂提及功能。

---

### [00:00:51] 第 18 段

![frame 18](./frames/frame_018.jpg)

> **EN:** First, we just merged in those two action config files to our repository on GitHub.
>
> **ZH:** 首先，我們剛剛把這兩個 action 設定檔案合併到了我們在 GitHub 上的儲存庫。

---

### [00:00:56] 第 19 段

![frame 19](./frames/frame_019.jpg)

> **EN:** So I need to pull those changes down to my local machine.
>
> **ZH:** 所以我需要將這些變更拉取到我的本機。

---

### [00:00:59] 第 20 段

![frame 20](./frames/frame_020.jpg)

> **EN:** Then inside of the newly created GitHub workflows directory, I'll see these two action config files.
>
> **ZH:** 然後在新建的 GitHub workflows 目錄裡，我會看到這兩個 action 設定檔案。

---

### [00:01:05] 第 21 段

![frame 21](./frames/frame_021.jpg)

> **EN:** One adds in support for the pull request review, and the other adds in support for handling
>
> **ZH:** 一個新增了對 pull request 審查的支援，另一個新增了對處理

---

### [00:01:09] 第 22 段

![frame 22](./frames/frame_022.jpg)

> **EN:** mentions.
>
> **ZH:** 提及的支援。

---

### [00:01:10] 第 23 段

![frame 23](./frames/frame_023.jpg)

> **EN:** Now, here's how I want to customize the mention functionality.
>
> **ZH:** 現在，這是我想要自訂提及功能的方式。

---

### [00:01:13] 第 24 段

![frame 24](./frames/frame_024.jpg)

> **EN:** Whenever I mention Cloud inside of an issue or a pull request, I want it to be able to run
>
> **ZH:** 每當我在 issue 或 pull request 中提及 Claude Code 時，我希望它能夠執行

---

### [00:01:18] 第 25 段

![frame 25](./frames/frame_025.jpg)

> **EN:** the project and use the Playwright MCP server to access the app inside of a web browser,
>
> **ZH:** 這個專案，並使用 Playwright MCP server 在 web 瀏覽器中存取應用程式，

---

### [00:01:23] 第 26 段

![frame 26](./frames/frame_026.jpg)

> **EN:** all inside of a GitHub action.
>
> **ZH:** 全部都在 GitHub Actions 內部完成。

---

### [00:01:25] 第 27 段

![frame 27](./frames/frame_027.jpg)

> **EN:** To make this work, I'll first add in a step before CloudCode runs in this workflow.
>
> **ZH:** 為了實現這個功能，我會在 Claude Code 執行之前，在這個 workflow 中先新增一個步驟。

---

### [00:01:30] 第 28 段

![frame 28](./frames/frame_028.jpg)

> **EN:** I'll run the setup command and then start the development server up.
>
> **ZH:** 我將執行 setup 指令，然後啟動開發伺服器。

---

### [00:01:34] 第 29 段

![frame 29](./frames/frame_029.jpg)

> **EN:** Then I'm going to update the CloudCode configuration.
>
> **ZH:** 然後我會更新 Claude Code 的設定。

---

### [00:01:37] 第 30 段

![frame 30](./frames/frame_030.jpg)

> **EN:** I'll add in some custom instructions.
>
> **ZH:** 我會新增一些自訂指令。

---

### [00:01:39] 第 31 段

![frame 31](./frames/frame_031.jpg)

> **EN:** These are passed directly to Cloud, and they allow us to provide some additional directions
>
> **ZH:** 這些指令會直接傳遞給 Claude Code，允許我們提供一些額外的說明

---

### [00:01:43] 第 32 段

![frame 32](./frames/frame_032.jpg)

> **EN:** or context.
>
> **ZH:** 或情境資訊。

---

### [00:01:44] 第 33 段

![frame 33](./frames/frame_033.jpg)

> **EN:** In this case, I'll tell Cloud that the development server is already running, and that I can use
>
> **ZH:** 在這個例子中，我會告訴 Claude Code 開發伺服器已經在執行，

---

### [00:01:48] 第 34 段

![frame 34](./frames/frame_034.jpg)

> **EN:** the Playwright MCP server to access the app in the browser if needed.
>
> **ZH:** 並且如果需要的話，我可以使用 Playwright MCP server 在瀏覽器中存取應用程式。

---

### [00:01:53] 第 35 段

![frame 35](./frames/frame_035.jpg)

> **EN:** Then I will add in some configuration to set up the Playwright MCP server itself.
>
> **ZH:** 然後我會新增一些設定來設置 Playwright MCP server 本身。

---

### [00:01:57] 第 36 段

![frame 36](./frames/frame_036.jpg)

> **EN:** There is one other thing to be aware of here.
>
> **ZH:** 這裡還有一件事需要注意。

---

### [00:01:59] 第 37 段

![frame 37](./frames/frame_037.jpg)

> **EN:** When you're running CloudCode inside of an action, we have to specifically list out all
>
> **ZH:** 當你在 action 中執行 Claude Code 時，我們必須明確列出所有

---

### [00:02:03] 第 38 段

![frame 38](./frames/frame_038.jpg)

> **EN:** the permissions that we want to grant CloudCode.
>
> **ZH:** 我們想要授予 Claude Code 的權限。

---

### [00:02:06] 第 39 段

![frame 39](./frames/frame_039.jpg)

> **EN:** And there's one tricky aspect to this.
>
> **ZH:** 這裡有一個棘手的地方。

---

### [00:02:08] 第 40 段

![frame 40](./frames/frame_040.jpg)

> **EN:** If you're using an MCP server, you have to individually list out each tool from each MCP
>
> **ZH:** 如果你使用了 MCP server，你必須逐一列出每個 MCP server 中

---

### [00:02:14] 第 41 段

![frame 41](./frames/frame_041.jpg)

> **EN:** server that you want to allow.
>
> **ZH:** 你想要允許的每個工具。

---

### [00:02:16] 第 42 段

![frame 42](./frames/frame_042.jpg)

> **EN:** There is no shortcut for permissions like we saw previously.
>
> **ZH:** 不像之前那樣有權限的快捷方式。

---

### [00:02:19] 第 43 段

![frame 43](./frames/frame_043.jpg)

> **EN:** Unfortunately, the Playwright MCP server has many different tools, so they each need to
>
> **ZH:** 遺憾的是，Playwright MCP server 有很多不同的工具，所以它們都需要

---

### [00:02:24] 第 44 段

![frame 44](./frames/frame_044.jpg)

> **EN:** be listed out.
>
> **ZH:** 逐一列出。

---

### [00:02:25] 第 45 段

![frame 45](./frames/frame_045.jpg)

> **EN:** Once I've finished with this configuration update, I'll be sure to commit these changes
>
> **ZH:** 完成這個設定更新後，我會確保提交這些變更

---

### [00:02:28] 第 46 段

![frame 46](./frames/frame_046.jpg)

> **EN:** and push them.
>
> **ZH:** 並推送它們。

---

### [00:02:30] 第 47 段

![frame 47](./frames/frame_047.jpg)

> **EN:** Now it's time to test out this updated workflow.
>
> **ZH:** 現在是時候測試這個更新後的 workflow 了。

---

### [00:02:33] 第 48 段

![frame 48](./frames/frame_048.jpg)

> **EN:** I'm going to give Cloud a little task.
>
> **ZH:** 我要給 Claude Code 一個小任務。

---

### [00:02:34] 第 49 段

![frame 49](./frames/frame_049.jpg)

> **EN:** In our actual app, see these two buttons up here?
>
> **ZH:** 在我們的實際應用程式中，看到上面這兩個按鈕了嗎？

---

### [00:02:37] 第 50 段

![frame 50](./frames/frame_050.jpg)

> **EN:** Right now they work fine.
>
> **ZH:** 目前它們運作正常。

---

### [00:02:38] 第 51 段

![frame 51](./frames/frame_051.jpg)

> **EN:** I can toggle between the preview and the code panels without issue.
>
> **ZH:** 我可以在預覽面板和程式碼面板之間切換，沒有任何問題。

---

### [00:02:41] 第 52 段

![frame 52](./frames/frame_052.jpg)

> **EN:** But I'm going to pretend as though they weren't working as intended.
>
> **ZH:** 但我要假裝它們沒有按預期運作。

---

### [00:02:44] 第 53 段

![frame 53](./frames/frame_053.jpg)

> **EN:** I'm going to take a screenshot with that button right there.
>
> **ZH:** 我要用那裡的按鈕截一張圖。

---

### [00:02:47] 第 54 段

![frame 54](./frames/frame_054.jpg)

> **EN:** I'm then going to make an issue.
>
> **ZH:** 然後我要建立一個 issue。

---

### [00:02:49] 第 55 段

![frame 55](./frames/frame_055.jpg)

> **EN:** I'm going to paste in the screenshot and I'm going to mention Cloud with at Cloud and ask
>
> **ZH:** 我要貼上截圖，然後用 `@claude` 提及 Claude Code，並讓

---

### [00:02:53] 第 56 段

![frame 56](./frames/frame_056.jpg)

> **EN:** it to verify that the two buttons are working as intended.
>
> **ZH:** 它驗證這兩個按鈕是否按預期運作。

---

### [00:02:56] 第 57 段

![frame 57](./frames/frame_057.jpg)

> **EN:** I'll then create the issue and wait.
>
> **ZH:** 然後我會建立這個 issue 並等待。

---

### [00:02:58] 第 58 段

![frame 58](./frames/frame_058.jpg)

> **EN:** Now it is going to take a minute or two for the action to actually start up and for Cloud
>
> **ZH:** action 實際啟動可能需要一兩分鐘，然後 Claude Code

---

### [00:03:02] 第 59 段

![frame 59](./frames/frame_059.jpg)

> **EN:** to respond.
>
> **ZH:** 才會回應。

---

### [00:03:03] 第 60 段

![frame 60](./frames/frame_060.jpg)

> **EN:** Remember, as we just saw in the action, we are now setting up the entire app and starting
>
> **ZH:** 記住，正如我們剛才在 action 中看到的，我們現在需要先設定整個應用程式並啟動

---

### [00:03:07] 第 61 段

![frame 61](./frames/frame_061.jpg)

> **EN:** it running before Cloud code even starts to run at all.
>
> **ZH:** 它執行，然後 Claude Code 才會開始執行。

---

### [00:03:11] 第 62 段

![frame 62](./frames/frame_062.jpg)

> **EN:** But eventually, Cloud will respond.
>
> **ZH:** 但最終，Claude Code 會回應。

---

### [00:03:13] 第 63 段

![frame 63](./frames/frame_063.jpg)

> **EN:** It will very often create a checklist of steps to accomplish the given task.
>
> **ZH:** 它通常會建立一個步驟清單來完成給定的任務。

---

### [00:03:17] 第 64 段

![frame 64](./frames/frame_064.jpg)

> **EN:** In this case, it is going to attempt to visit the app, manually test out the button, and
>
> **ZH:** 在這個例子中，它將嘗試造訪應用程式、手動測試按鈕，並

---

### [00:03:21] 第 65 段

![frame 65](./frames/frame_065.jpg)

> **EN:** fix any issues that it finds.
>
> **ZH:** 修復發現的任何問題。

---

### [00:03:23] 第 66 段

![frame 66](./frames/frame_066.jpg)

> **EN:** Cloud will notice that the buttons actually are working just fine, and so it's going to
>
> **ZH:** Claude Code 會發現這兩個按鈕實際上運作得很好，所以它會

---

### [00:03:27] 第 67 段

![frame 67](./frames/frame_067.jpg)

> **EN:** terminate early with a message documenting its findings.
>
> **ZH:** 提早結束並給出一條記錄其發現結果的訊息。

---

### [00:03:29] 第 68 段

![frame 68](./frames/frame_068.jpg)

> **EN:** Now, this is just a small example of how you can use Cloud Codes GitHub integration.
>
> **ZH:** 這只是一個小例子，展示了你如何使用 Claude Code 的 GitHub 整合功能。

---

### [00:03:34] 第 69 段

![frame 69](./frames/frame_069.jpg)

> **EN:** I recommend you spend some time to think about how you can custom tailor it for your own particular project.
>
> **ZH:** 我建議你花些時間思考，如何為你自己的特定專案量身打造它。

---
