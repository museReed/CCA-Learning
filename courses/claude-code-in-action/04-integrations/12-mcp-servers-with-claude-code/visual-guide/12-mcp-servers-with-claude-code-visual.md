# MCP Servers with Claude Code — 使用 MCP Server 擴展 Claude Code — 影片逐幀學習指南

| 項目 | 內容 |
|------|------|
| 課程 | claude-code-in-action / 04-integrations / 12-mcp-servers-with-claude-code |
| 影片 | MCP Servers with Claude Code |
| 字幕數 | 39 段 |
| 格式 | 每段字幕一張截圖 + 雙語字幕（英/中） |

---

### [00:00:00] 第 1 段

![frame 1](./frames/frame_001.jpg)

> **EN:** You can add new tools and capabilities to CloudCode through the use of MCP servers.
>
> **ZH:** 你可以透過使用 MCP server 為 Claude Code 新增工具和功能。

---

### [00:00:05] 第 2 段

![frame 2](./frames/frame_002.jpg)

> **EN:** These MCP servers either run remotely or locally on your machine.
>
> **ZH:** 這些 MCP server 可以遠端運行，也可以在你的本機上運行。

---

### [00:00:09] 第 3 段

![frame 3](./frames/frame_003.jpg)

> **EN:** A very popular MCP server named Playwright gives CloudCode the ability to control a browser.
>
> **ZH:** 一個非常受歡迎的 MCP server 叫做 Playwright，它賦予 Claude Code 控制瀏覽器的能力。

---

### [00:00:15] 第 4 段

![frame 4](./frames/frame_004.jpg)

> **EN:** Let me show you how to add it to CloudCode, and then we'll use it to develop our app a little bit more.
>
> **ZH:** 讓我來示範如何將它加入 Claude Code，然後我們再用它進一步開發我們的應用程式。

---

### [00:00:20] 第 5 段

![frame 5](./frames/frame_005.jpg)

> **EN:** To install this server at your terminal, not inside of CloudCode, we'll execute Cloud MCP add,
>
> **ZH:** 要安裝這個 server，請在你的終端機（不是在 Claude Code 內部）執行 claude mcp add，

---

### [00:00:26] 第 6 段

![frame 6](./frames/frame_006.jpg)

> **EN:** and then a name for this MCP server, I'm going to name it Playwright,
>
> **ZH:** 然後指定這個 MCP server 的名稱，我將它命名為 Playwright，

---

### [00:00:29] 第 7 段

![frame 7](./frames/frame_007.jpg)

> **EN:** and then after the name, we'll add in a command that will start up the server locally on your machine.
>
> **ZH:** 在名稱之後，我們還需要加上一個指令，用來在你的本機上啟動這個 server。

---

### [00:00:34] 第 8 段

![frame 8](./frames/frame_008.jpg)

> **EN:** We can then start CloudCode and ask it to open a browser and navigate to our application at localhost 3000.
>
> **ZH:** 然後我們可以啟動 Claude Code，讓它開啟瀏覽器並導航到我們位於 localhost 3000 的應用程式。

---

### [00:00:41] 第 9 段

![frame 9](./frames/frame_009.jpg)

> **EN:** Before the browser opens, you might notice that you are required to give permission for that tool to run.
>
> **ZH:** 在瀏覽器開啟之前，你可能會注意到系統要求你授予該工具執行的權限。

---

### [00:00:45] 第 10 段

![frame 10](./frames/frame_010.jpg)

> **EN:** If you get tired of all those permission pop-ups, you can open up the Cloud directory inside there, settings.local.json,
>
> **ZH:** 如果你厭倦了這些權限彈出視窗，可以打開 `.claude` 目錄，找到 `settings.local.json`，

---

### [00:00:52] 第 11 段

![frame 11](./frames/frame_011.jpg)

> **EN:** and then inside of the allow array, you can add in a string of MCP underscore underscore.
>
> **ZH:** 然後在 `allowed tools` 陣列中，新增一個以 `mcp__` 開頭的字串。

---

### [00:00:58] 第 12 段

![frame 12](./frames/frame_012.jpg)

> **EN:** Notice there are two underscores there, Playwright.
>
> **ZH:** 注意這裡有兩個底線，後面接 Playwright。

---

### [00:01:00] 第 13 段

![frame 13](./frames/frame_013.jpg)

> **EN:** This allows CloudCode to make use of this MCP server and the tools inside of it in any way it wants
>
> **ZH:** 這樣 Claude Code 就可以任意使用這個 MCP server 及其中的所有工具，

---

### [00:01:05] 第 14 段

![frame 14](./frames/frame_014.jpg)

> **EN:** without requiring you to provide permission every time.
>
> **ZH:** 而不需要你每次都手動授予權限。

---

### [00:01:08] 第 15 段

![frame 15](./frames/frame_015.jpg)

> **EN:** If I restart CloudCode and then ask it to open a browser again,
>
> **ZH:** 如果我重新啟動 Claude Code，然後再次讓它開啟瀏覽器，

---

### [00:01:12] 第 16 段

![frame 16](./frames/frame_016.jpg)

> **EN:** it will do so without requiring me to give permission.
>
> **ZH:** 它將直接執行，不再要求我授予權限。

---

### [00:01:14] 第 17 段

![frame 17](./frames/frame_017.jpg)

> **EN:** There are an incredible number of ways that you can use the Playwright MCP server.
>
> **ZH:** Playwright MCP server 有非常多種用途。

---

### [00:01:18] 第 18 段

![frame 18](./frames/frame_018.jpg)

> **EN:** Let me show you one that would be really applicable to the project we are working on right now.
>
> **ZH:** 讓我向你展示一個非常適合我們目前專案的應用場景。

---

### [00:01:21] 第 19 段

![frame 19](./frames/frame_019.jpg)

> **EN:** Back inside my editor, I'm going to find the src lib prompts generation.tsx file.
>
> **ZH:** 回到我的編輯器，我要找到 `src/lib/prompts/generation.tsx` 這個檔案。

---

### [00:01:28] 第 20 段

![frame 20](./frames/frame_020.jpg)

> **EN:** This is the prompt that is used to actually generate the components that you ask for inside of our app.
>
> **ZH:** 這是實際用於產生元件的提示詞檔案，也就是你在我們的應用程式中所請求的元件。

---

### [00:01:33] 第 21 段

![frame 21](./frames/frame_021.jpg)

> **EN:** So I want to allow CloudCode to make use of the browser, generate a component on its own,
>
> **ZH:** 所以我想讓 Claude Code 利用瀏覽器，自行產生一個元件，

---

### [00:01:38] 第 22 段

![frame 22](./frames/frame_022.jpg)

> **EN:** and then tweak this prompt on its own based upon the generated component.
>
> **ZH:** 然後根據產生的元件，自行調整這個提示詞。

---

### [00:01:42] 第 23 段

![frame 23](./frames/frame_023.jpg)

> **EN:** And hopefully we'll end up with some better looking components being generated out of our app.
>
> **ZH:** 我們希望最終能產生外觀更好的元件。

---

### [00:01:46] 第 24 段

![frame 24](./frames/frame_024.jpg)

> **EN:** So let me show you how we would do that.
>
> **ZH:** 讓我來示範如何做到這一點。

---

### [00:01:48] 第 25 段

![frame 25](./frames/frame_025.jpg)

> **EN:** Back inside of CloudCode, I'm going to ask it to navigate to localhost 3000,
>
> **ZH:** 回到 Claude Code，我要讓它導航到 localhost 3000，

---

### [00:01:53] 第 26 段

![frame 26](./frames/frame_026.jpg)

> **EN:** attempt to generate a component, take a look at the generated source code and evaluate the styling,
>
> **ZH:** 嘗試產生一個元件，查看產生的原始碼並評估樣式，

---

### [00:01:58] 第 27 段

![frame 27](./frames/frame_027.jpg)

> **EN:** and then update our prompt inside that generation.tsx file.
>
> **ZH:** 然後更新我們在 `generation.tsx` 檔案中的提示詞。

---

### [00:02:01] 第 28 段

![frame 28](./frames/frame_028.jpg)

> **EN:** And hopefully we'll end up with some, at the end of the day, better styling on our generated components.
>
> **ZH:** 我們希望最終能得到樣式更好的產生元件。

---

### [00:02:08] 第 29 段

![frame 29](./frames/frame_029.jpg)

> **EN:** So let's see how it does.
>
> **ZH:** 讓我們看看它的表現如何。

---

### [00:02:09] 第 30 段

![frame 30](./frames/frame_030.jpg)

> **EN:** Cloud is going to first open up the browser.
>
> **ZH:** Claude Code 首先會開啟瀏覽器。

---

### [00:02:11] 第 31 段

![frame 31](./frames/frame_031.jpg)

> **EN:** It's going to attempt to generate a component.
>
> **ZH:** 它會嘗試產生一個元件。

---

### [00:02:13] 第 32 段

![frame 32](./frames/frame_032.jpg)

> **EN:** And looking at some of the commentary from Cloud here, it looks like it's not quite so happy.
>
> **ZH:** 從 Claude Code 的評論來看，它似乎不太滿意。

---

### [00:02:18] 第 33 段

![frame 33](./frames/frame_033.jpg)

> **EN:** You might actually notice that it complains about a very common style that's used in applications like this,
>
> **ZH:** 你可能會注意到它抱怨了一種在這類應用程式中很常見的樣式，

---

### [00:02:23] 第 34 段

![frame 34](./frames/frame_034.jpg)

> **EN:** a purple to blue kind of gradient.
>
> **ZH:** 也就是紫色到藍色的漸層效果。

---

### [00:02:26] 第 35 段

![frame 35](./frames/frame_035.jpg)

> **EN:** Cloud is then going to update our prompt and then try to generate a new component.
>
> **ZH:** Claude Code 接下來會更新我們的提示詞，然後嘗試產生一個新的元件。

---

### [00:02:30] 第 36 段

![frame 36](./frames/frame_036.jpg)

> **EN:** And I'll be honest with you, this actually gave a much better result than I ever expected.
>
> **ZH:** 說實話，這個結果比我預期的要好得多。

---

### [00:02:35] 第 37 段

![frame 37](./frames/frame_037.jpg)

> **EN:** This testimonial card actually looks really, really great.
>
> **ZH:** 這張推薦卡片看起來真的非常出色。

---

### [00:02:38] 第 38 段

![frame 38](./frames/frame_038.jpg)

> **EN:** Based on these results alone, you can immediately get a sense that MCP servers really open the door to a lot of interesting use cases.
>
> **ZH:** 僅憑這些結果，你就能立刻感受到 MCP server 確實開啟了許多有趣的應用場景。

---

### [00:02:46] 第 39 段

![frame 39](./frames/frame_039.jpg)

> **EN:** And I highly recommend you look into some MCP servers that might aid Cloud in developing whatever kind of project you personally are working on.
>
> **ZH:** 我強烈建議你去研究一下，哪些 MCP server 可以幫助 Claude Code 開發你個人正在做的專案。

---
