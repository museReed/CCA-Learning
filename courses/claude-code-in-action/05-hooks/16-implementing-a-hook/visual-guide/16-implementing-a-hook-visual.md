# Implementing a Hook — 實作 Hook — 影片逐幀學習指南

| 項目 | 內容 |
|------|------|
| 課程 | claude-code-in-action / 05-hooks / Lesson 16 |
| 影片 | Implementing a Hook |
| 字幕數 | 70 段 |
| 格式 | 每段字幕一張截圖 + 雙語字幕（英/中） |

---

### [00:00:00] 第 1 段

![frame 1](./frames/frame_001.jpg)

> **EN:** Let's put together our custom hook.
>
> **ZH:** 我們來組合自己的自訂 hook。

---

### [00:00:02] 第 2 段

![frame 2](./frames/frame_002.jpg)

> **EN:** Remember, the entire goal here is to prevent Claude from ever reading the contents of the .env file.
>
> **ZH:** 記住，這裡的整個目標是防止 Claude 讀取 .env 檔案的內容。

---

### [00:00:07] 第 3 段

![frame 3](./frames/frame_003.jpg)

> **EN:** In the last video, we discussed many of the different configuration options we'll need to set.
>
> **ZH:** 在上一支影片中，我們討論了許多需要設定的不同配置選項。

---

### [00:00:12] 第 4 段

![frame 4](./frames/frame_004.jpg)

> **EN:** So in this video, we're going to be mostly focused on the implementation.
>
> **ZH:** 所以在這支影片中，我們主要會專注在實作上。

---

### [00:00:14] 第 5 段

![frame 5](./frames/frame_005.jpg)

> **EN:** To get started, inside the .claud directory, I'm going to open up the settings.local.json file.
>
> **ZH:** 首先，在 .claude 目錄裡面，我要打開 settings.local.json 這個檔案。

---

### [00:00:20] 第 6 段

![frame 6](./frames/frame_006.jpg)

> **EN:** Remember, inside of here, we have a list of pre-tool use hooks and post-tool use hooks.
>
> **ZH:** 記住，在這裡面我們有一個 pre-tool use hooks 和 post-tool use hooks 的列表。

---

### [00:00:26] 第 7 段

![frame 7](./frames/frame_007.jpg)

> **EN:** As we discussed a moment ago, we want to make a pre-tool use hook so that we can prevent Claude from ever reading the contents of that particular file.
>
> **ZH:** 如同我們剛才討論的，我們要做一個 pre-tool use hook，這樣就能防止 Claude 讀取那個特定檔案的內容。

---

### [00:00:33] 第 8 段

![frame 8](./frames/frame_008.jpg)

> **EN:** I already added in a little configuration section right here for us, just to save us a little bit of typing.
>
> **ZH:** 我已經在這裡預先加了一小段配置區塊，幫我們省一點打字的時間。

---

### [00:00:39] 第 9 段

![frame 9](./frames/frame_009.jpg)

> **EN:** All we need to do is fill in the matcher and the command.
>
> **ZH:** 我們只需要填入 matcher 和 command 就好。

---

### [00:00:42] 第 10 段

![frame 10](./frames/frame_010.jpg)

> **EN:** First is the matcher.
>
> **ZH:** 首先是 matcher。

---

### [00:00:44] 第 11 段

![frame 11](./frames/frame_011.jpg)

> **EN:** So the matcher is going to be the tools that we want to watch for.
>
> **ZH:** matcher 就是我們想要監控的工具。

---

### [00:00:47] 第 12 段

![frame 12](./frames/frame_012.jpg)

> **EN:** In our case, as we discussed, we want to watch for calls to the read and the grep tools.
>
> **ZH:** 在我們的案例中，如同討論過的，我們要監控對 read 和 grep 工具的呼叫。

---

### [00:00:53] 第 13 段

![frame 13](./frames/frame_013.jpg)

> **EN:** I'm going to separate those two tool names with a pipe symbol.
>
> **ZH:** 我要用一個 pipe 符號來分隔這兩個工具名稱。

---

### [00:00:57] 第 14 段

![frame 14](./frames/frame_014.jpg)

> **EN:** So that's not an L or a capital I.
>
> **ZH:** 那不是字母 L 也不是大寫的 I。

---

### [00:00:59] 第 15 段

![frame 15](./frames/frame_015.jpg)

> **EN:** It is the symbol right above the return key on your keyboard.
>
> **ZH:** 它是你鍵盤上 return 鍵正上方的那個符號。

---

### [00:01:03] 第 16 段

![frame 16](./frames/frame_016.jpg)

> **EN:** Then next up, we need to provide a command to run whenever Claude attempts to call those two tools.
>
> **ZH:** 接下來，我們需要提供一個 command，在 Claude 嘗試呼叫這兩個工具時執行。

---

### [00:01:09] 第 17 段

![frame 17](./frames/frame_017.jpg)

> **EN:** We could put in here any command you want.
>
> **ZH:** 你可以在這裡放任何你想要的命令。

---

### [00:01:11] 第 18 段

![frame 18](./frames/frame_018.jpg)

> **EN:** So it can be a CLI.
>
> **ZH:** 可以是一個 CLI。

---

### [00:01:12] 第 19 段

![frame 19](./frames/frame_019.jpg)

> **EN:** It can be a call to a shell script.
>
> **ZH:** 可以是呼叫一個 shell script。

---

### [00:01:14] 第 20 段

![frame 20](./frames/frame_020.jpg)

> **EN:** Absolutely anything.
>
> **ZH:** 什麼都可以。

---

### [00:01:15] 第 21 段

![frame 21](./frames/frame_021.jpg)

> **EN:** To follow the pattern that I've already established inside the rest of this file,
>
> **ZH:** 為了延續我在這個檔案其他地方已經建立的模式，

---

### [00:01:19] 第 22 段

![frame 22](./frames/frame_022.jpg)

> **EN:** I'm going to call a node.js script that I placed ahead of time inside the hooks directory of this project.
>
> **ZH:** 我要呼叫一個 node.js 腳本，我事先放在這個專案的 hooks 目錄裡面。

---

### [00:01:25] 第 23 段

![frame 23](./frames/frame_023.jpg)

> **EN:** So inside the hooks directory, I put together for us a read underscore hook dot js file.
>
> **ZH:** 在 hooks 目錄裡面，我幫我們準備了一個 read_hook.js 檔案。

---

### [00:01:30] 第 24 段

![frame 24](./frames/frame_024.jpg)

> **EN:** This is the file that I want to run whenever Claude attempts to call one of those two tools.
>
> **ZH:** 這就是我想在 Claude 嘗試呼叫那兩個工具時執行的檔案。

---

### [00:01:35] 第 25 段

![frame 25](./frames/frame_025.jpg)

> **EN:** So to call that, I'm going to replace the true right here, which is just a placeholder for right now,
>
> **ZH:** 所以要呼叫它的話，我要把這裡的 true（目前只是一個佔位符）

---

### [00:01:40] 第 26 段

![frame 26](./frames/frame_026.jpg)

> **EN:** with node dot slash hooks, read underscore hook dot js.
>
> **ZH:** 替換成 node ./hooks/read_hook.js。

---

### [00:01:45] 第 27 段

![frame 27](./frames/frame_027.jpg)

> **EN:** I'm then going to save this file and that's all we have to do inside of here.
>
> **ZH:** 然後我要存檔，在這個檔案裡我們要做的就這些。

---

### [00:01:50] 第 28 段

![frame 28](./frames/frame_028.jpg)

> **EN:** Next up, we need to actually implement the command that's going to run anytime Claude tries to call
>
> **ZH:** 接下來，我們需要實際實作那個在 Claude 嘗試呼叫

---

### [00:01:54] 第 29 段

![frame 29](./frames/frame_029.jpg)

> **EN:** the read or the grep tools.
>
> **ZH:** read 或 grep 工具時會執行的 command。

---

### [00:01:56] 第 30 段

![frame 30](./frames/frame_030.jpg)

> **EN:** So that's going to be the read hook dot js file.
>
> **ZH:** 也就是 read_hook.js 這個檔案。

---

### [00:01:58] 第 31 段

![frame 31](./frames/frame_031.jpg)

> **EN:** At the top of this file, I've got some code that's going to read from standard in and parse that data as JSON.
>
> **ZH:** 在這個檔案的最上面，我有一些程式碼會從 standard in 讀取資料並解析成 JSON。

---

### [00:02:04] 第 32 段

![frame 32](./frames/frame_032.jpg)

> **EN:** So this tool args object right here, that's going to be the big JSON object I showed you in this diagram
>
> **ZH:** 這裡的 toolArgs 物件，就是我在這張圖表中展示給你看的那個大 JSON 物件，

---

### [00:02:09] 第 33 段

![frame 33](./frames/frame_033.jpg)

> **EN:** back over here.
>
> **ZH:** 就在這邊。

---

### [00:02:10] 第 34 段

![frame 34](./frames/frame_034.jpg)

> **EN:** So it's going to have properties like session ID, the tool name, the tool input, and so on.
>
> **ZH:** 它會有像 session ID、tool name、tool input 等等這些屬性。

---

### [00:02:15] 第 35 段

![frame 35](./frames/frame_035.jpg)

> **EN:** So all we really need to do is take a look at that file path right there and decide whether or not
>
> **ZH:** 所以我們真正需要做的就是看一下那個 file path，然後判斷它

---

### [00:02:20] 第 36 段

![frame 36](./frames/frame_036.jpg)

> **EN:** it is trying to read the dot EMV file.
>
> **ZH:** 是不是在嘗試讀取 .env 檔案。

---

### [00:02:22] 第 37 段

![frame 37](./frames/frame_037.jpg)

> **EN:** If it is, then we want to make sure that we exit from our program or our command here with an exit
>
> **ZH:** 然後在我們的程式或 command 裡面，我們需要透過 standard in 接收這些資訊，解析那個 JSON，然後讀取 tool name、tool input 的參數等等，決定我們要怎麼處理這個工具呼叫。

---

### [00:02:27] 第 38 段

![frame 38](./frames/frame_038.jpg)

> **EN:** code of two, and hopefully also log some information out to Claude that says, sorry, but you can't read
>
> **ZH:** 然後到第四步。

---

### [00:02:32] 第 39 段

![frame 39](./frames/frame_039.jpg)

> **EN:** that file.
>
> **ZH:** 在第四步，當我們的 command 收到那個提議的工具呼叫資料後，我們接著要 exit。

---

### [00:02:33] 第 40 段

![frame 40](./frames/frame_040.jpg)

> **EN:** So you'll notice that back over here, I've already got some code that's going to read that file path.
>
> **ZH:** 你會注意到回到這邊，我已經有一些程式碼會讀取那個 file path。

---

### [00:02:37] 第 41 段

![frame 41](./frames/frame_041.jpg)

> **EN:** You'll also notice that there's a fallback of looking at tool input dot path right here.
>
> **ZH:** 你也會注意到這裡有一個 fallback 去看 toolInput.path。

---

### [00:02:42] 第 42 段

![frame 42](./frames/frame_042.jpg)

> **EN:** I'll tell you why that's added in, in just a moment.
>
> **ZH:** 我等一下會告訴你為什麼要加這個。

---

### [00:02:45] 第 43 段

![frame 43](./frames/frame_043.jpg)

> **EN:** So now let's implement the to do statement.
>
> **ZH:** 現在我們來實作這個 TODO 的部分。

---

### [00:02:48] 第 44 段

![frame 44](./frames/frame_044.jpg)

> **EN:** We'll say if read path includes dot EMV.
>
> **ZH:** 我們寫：如果 readPath 包含 .env。

---

### [00:02:53] 第 45 段

![frame 45](./frames/frame_045.jpg)

> **EN:** That means that Claude must be trying to read the dot EMV file.
>
> **ZH:** 那就代表 Claude 一定是在嘗試讀取 .env 檔案。

---

### [00:02:56] 第 46 段

![frame 46](./frames/frame_046.jpg)

> **EN:** And if that's the case, then I want to make sure that we block that operation and provide some
>
> **ZH:** 如果是這種情況，我要確保我們阻擋這個操作，並提供一些

---

### [00:03:01] 第 47 段

![frame 47](./frames/frame_047.jpg)

> **EN:** logging feedback to Claude.
>
> **ZH:** 日誌回饋給 Claude。

---

### [00:03:02] 第 48 段

![frame 48](./frames/frame_048.jpg)

> **EN:** Claude.
>
> **ZH:** Claude。

---

### [00:03:02] 第 49 段

![frame 49](./frames/frame_049.jpg)

> **EN:** So I'm going to first add in a console dot air specifically a console dot air, because
>
> **ZH:** 所以我要先加一個 console.error，特別是 console.error，因為

---

### [00:03:07] 第 50 段

![frame 50](./frames/frame_050.jpg)

> **EN:** we want to log to standard air.
>
> **ZH:** 我們要輸出到 standard error。

---

### [00:03:09] 第 51 段

![frame 51](./frames/frame_051.jpg)

> **EN:** Remember, that's how we provide some feedback to Claude.
>
> **ZH:** 記住，這就是我們提供回饋給 Claude 的方式。

---

### [00:03:12] 第 52 段

![frame 52](./frames/frame_052.jpg)

> **EN:** And I'll say something like you cannot read the dot EMV file.
>
> **ZH:** 我會寫類似「你不能讀取 .env 檔案」這樣的訊息。

---

### [00:03:18] 第 53 段

![frame 53](./frames/frame_053.jpg)

> **EN:** And then I'll do a process dot exit two.
>
> **ZH:** 然後我會做 process.exit(2)。

---

### [00:03:21] 第 54 段

![frame 54](./frames/frame_054.jpg)

> **EN:** So now to test this out, I'm going to save the file.
>
> **ZH:** 現在來測試一下，我要存檔。

---

### [00:03:23] 第 55 段

![frame 55](./frames/frame_055.jpg)

> **EN:** I'm going to open up Claude code.
>
> **ZH:** 我要打開 Claude Code。

---

### [00:03:25] 第 56 段

![frame 56](./frames/frame_056.jpg)

> **EN:** If you already have it open, make sure you restart Claude code.
>
> **ZH:** 如果你已經打開了，請確保你重新啟動 Claude Code。

---

### [00:03:28] 第 57 段

![frame 57](./frames/frame_057.jpg)

> **EN:** You have to restart it to have any changes to your hooks take effect.
>
> **ZH:** 你必須重新啟動它，hooks 的任何變更才會生效。

---

### [00:03:32] 第 58 段

![frame 58](./frames/frame_058.jpg)

> **EN:** I'm going to ask Claude to read the dot EMV file.
>
> **ZH:** 我要請 Claude 讀取 .env 檔案。

---

### [00:03:38] 第 59 段

![frame 59](./frames/frame_059.jpg)

> **EN:** And it's probably going to attempt to, but as it attempts to read it, we're going to send
>
> **ZH:** 它大概會嘗試去讀，但當它嘗試讀取時，我們會回傳

---

### [00:03:41] 第 60 段

![frame 60](./frames/frame_060.jpg)

> **EN:** back an error that says you cannot read the dot EMV file.
>
> **ZH:** 一個錯誤說「你不能讀取 .env 檔案」。

---

### [00:03:44] 第 61 段

![frame 61](./frames/frame_061.jpg)

> **EN:** And then Claude is hopefully going to realize that, sorry, you can't actually read this.
>
> **ZH:** 然後 Claude 應該就會意識到，抱歉，你其實不能讀這個檔案。

---

### [00:03:48] 第 62 段

![frame 62](./frames/frame_062.jpg)

> **EN:** As a matter of fact, it's even able to recognize that it was prevented by a read hook.
>
> **ZH:** 事實上，它甚至能辨識出是被一個 read hook 擋下來的。

---

### [00:03:52] 第 63 段

![frame 63](./frames/frame_063.jpg)

> **EN:** Now, our hook should also be working on grep operations as well.
>
> **ZH:** 現在，我們的 hook 應該對 grep 操作也同樣有效。

---

### [00:03:56] 第 64 段

![frame 64](./frames/frame_064.jpg)

> **EN:** So if I ask Claude to try the grep tool, this should also hopefully be forbidden as well.
>
> **ZH:** 所以如果我請 Claude 試試 grep 工具，這應該也會被禁止。

---

### [00:04:03] 第 65 段

![frame 65](./frames/frame_065.jpg)

> **EN:** So let's see how it does.
>
> **ZH:** 我們來看看效果如何。

---

### [00:04:05] 第 66 段

![frame 66](./frames/frame_066.jpg)

> **EN:** And yep, same thing.
>
> **ZH:** 沒錯，一樣的結果。

---

### [00:04:06] 第 67 段

![frame 67](./frames/frame_067.jpg)

> **EN:** It is now forbidden.
>
> **ZH:** 現在也被禁止了。

---

### [00:04:07] 第 68 段

![frame 68](./frames/frame_068.jpg)

> **EN:** So that is a working hook that we have put together.
>
> **ZH:** 這就是我們組合出來的一個可運作的 hook。

---

### [00:04:10] 第 69 段

![frame 69](./frames/frame_069.jpg)

> **EN:** Now, this hook is not terribly useful, and I'm going to show you a much more useful hook
>
> **ZH:** 這個 hook 不是特別實用，我等一下會展示一個

---

### [00:04:14] 第 70 段

![frame 70](./frames/frame_070.jpg)

> **EN:** in just a moment.
>
> **ZH:** 更實用的 hook 給你看。

---
