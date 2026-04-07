# Controlling Context — 控制對話流向 — 影片逐幀學習指南

| 項目 | 內容 |
|------|------|
| 課程 | claude-code-in-action / 03-context-and-commands / 10-controlling-context |
| 影片 | Controlling Context |
| 字幕數 | 66 段 |
| 格式 | 每段字幕一張截圖 + 雙語字幕（英/中） |

---

### [00:00:00] 第 1 段

![frame 1](./frames/frame_001.jpg)

> **EN:** In this video, I'd like to show you a couple of different techniques for controlling and
>
> **ZH:** 在這支影片中，我想向你展示幾種不同的技術，用來控制和

---

### [00:00:04] 第 2 段

![frame 2](./frames/frame_002.jpg)

> **EN:** directing the flow of conversation.
>
> **ZH:** 引導對話的流向。

---

### [00:00:06] 第 3 段

![frame 3](./frames/frame_003.jpg)

> **EN:** Here's a basic example right away.
>
> **ZH:** 先來看一個基本範例。

---

### [00:00:08] 第 4 段

![frame 4](./frames/frame_004.jpg)

> **EN:** I'm going to ask Claude to write tests for some functions written into an authentication
>
> **ZH:** 我要請 Claude 為一個認證檔案裡的函式撰寫測試，

---

### [00:00:12] 第 5 段

![frame 5](./frames/frame_005.jpg)

> **EN:** file.
>
> **ZH:** 這些函式就寫在那個檔案裡。

---

### [00:00:13] 第 6 段

![frame 6](./frames/frame_006.jpg)

> **EN:** Claude quickly comes up with a plan for authoring several different tests.
>
> **ZH:** Claude 很快就提出了一個計畫，打算撰寫幾個不同的測試。

---

### [00:00:16] 第 7 段

![frame 7](./frames/frame_007.jpg)

> **EN:** However, I know that testing this file is a little tough, and I'd like Claude to only
>
> **ZH:** 不過，我知道測試這個檔案有點複雜，我希望 Claude 一次只

---

### [00:00:21] 第 8 段

![frame 8](./frames/frame_008.jpg)

> **EN:** test one thing at a time.
>
> **ZH:** 測試一件事。

---

### [00:00:23] 第 9 段

![frame 9](./frames/frame_009.jpg)

> **EN:** To interrupt Claude, I can press escape.
>
> **ZH:** 要中斷 Claude，我可以按 escape。

---

### [00:00:25] 第 10 段

![frame 10](./frames/frame_010.jpg)

> **EN:** This will stop Claude in its tracks, allowing me to suggest a different path.
>
> **ZH:** 這會讓 Claude 立刻停下來，讓我能夠建議一個不同的方向。

---

### [00:00:30] 第 11 段

![frame 11](./frames/frame_011.jpg)

> **EN:** Combining escape along with memories is a really powerful way to fix errors that Claude
>
> **ZH:** 把 escape 和 memories 搭配使用，是修正 Claude 反覆犯錯的一個

---

### [00:00:34] 第 12 段

![frame 12](./frames/frame_012.jpg)

> **EN:** makes repeatedly.
>
> **ZH:** 非常強大的方式。

---

### [00:00:35] 第 13 段

![frame 13](./frames/frame_013.jpg)

> **EN:** Here's an example.
>
> **ZH:** 來看個範例。

---

### [00:00:36] 第 14 段

![frame 14](./frames/frame_014.jpg)

> **EN:** I'm going to ask Claude to write tests for the same file again.
>
> **ZH:** 我要再次請 Claude 為同一個檔案撰寫測試。

---

### [00:00:39] 第 15 段

![frame 15](./frames/frame_015.jpg)

> **EN:** This time around, it will attempt to read a test configuration file that doesn't actually
>
> **ZH:** 這次，它會嘗試讀取一個其實並不存在的測試設定檔，

---

### [00:00:43] 第 16 段

![frame 16](./frames/frame_016.jpg)

> **EN:** exist.
>
> **ZH:** 但那個檔案根本不存在。

---

### [00:00:44] 第 17 段

![frame 17](./frames/frame_017.jpg)

> **EN:** Now, this is an error that I've seen Claude make before on this project.
>
> **ZH:** 這是一個我在這個專案中已經看過 Claude 犯過的錯誤。

---

### [00:00:48] 第 18 段

![frame 18](./frames/frame_018.jpg)

> **EN:** So to stop this mistake from being repeated, I'll very quickly hit escape.
>
> **ZH:** 所以為了避免這個錯誤再次發生，我會非常快速地按下 escape。

---

### [00:00:52] 第 19 段

![frame 19](./frames/frame_019.jpg)

> **EN:** I'll then use the pound shortcut to add in a memory about the correct name of this test
>
> **ZH:** 接著我會用 # 快捷鍵加入一條關於這個測試設定檔正確名稱的 memory，

---

### [00:00:56] 第 20 段

![frame 20](./frames/frame_020.jpg)

> **EN:** config file.
>
> **ZH:** 就是關於那個測試設定檔的正確名稱。

---

### [00:00:57] 第 21 段

![frame 21](./frames/frame_021.jpg)

> **EN:** And now I probably won't have to see this error again.
>
> **ZH:** 現在我應該不會再看到這個錯誤了。

---

### [00:01:01] 第 22 段

![frame 22](./frames/frame_022.jpg)

> **EN:** Some of these conversation control shortcuts seem like they're just for convenience, but
>
> **ZH:** 這些對話控制快捷鍵有些看起來只是為了方便，但

---

### [00:01:05] 第 23 段

![frame 23](./frames/frame_023.jpg)

> **EN:** used correctly, they can really improve Claude's ability to work effectively and stay on task.
>
> **ZH:** 用得好的話，真的能大幅提升 Claude 有效工作、保持專注的能力。

---

### [00:01:10] 第 24 段

![frame 24](./frames/frame_024.jpg)

> **EN:** So let me show you a more practical example.
>
> **ZH:** 讓我給你看一個更實際的範例。

---

### [00:01:13] 第 25 段

![frame 25](./frames/frame_025.jpg)

> **EN:** Inside the auth.ts file, there are four different functions, and I would like to get Claude to
>
> **ZH:** 在 auth.ts 檔案裡有四個不同的函式，我想讓 Claude 逐一

---

### [00:01:17] 第 26 段

![frame 26](./frames/frame_026.jpg)

> **EN:** write tests for each of them one at a time.
>
> **ZH:** 為每個函式撰寫測試。

---

### [00:01:19] 第 27 段

![frame 27](./frames/frame_027.jpg)

> **EN:** Starting on a function called create session.
>
> **ZH:** 從一個叫做 create session 的函式開始。

---

### [00:01:22] 第 28 段

![frame 28](./frames/frame_028.jpg)

> **EN:** Claude will definitely attempt to write the tests, but as it is running them, it runs into
>
> **ZH:** Claude 當然會嘗試撰寫測試，但在執行的過程中，它遇到了

---

### [00:01:26] 第 29 段

![frame 29](./frames/frame_029.jpg)

> **EN:** an error and spends a little bit of time debugging it.
>
> **ZH:** 一個錯誤，並花了一些時間除錯。

---

### [00:01:29] 第 30 段

![frame 30](./frames/frame_030.jpg)

> **EN:** It turns out there was a package that I forgot to install.
>
> **ZH:** 原來是我忘記安裝一個套件了。

---

### [00:01:32] 第 31 段

![frame 31](./frames/frame_031.jpg)

> **EN:** Eventually the tests are completed and working, and it's time to start working on the next
>
> **ZH:** 最終測試完成並通過，是時候開始處理下一

---

### [00:01:36] 第 32 段

![frame 32](./frames/frame_032.jpg)

> **EN:** set of tests.
>
> **ZH:** 組測試了。

---

### [00:01:38] 第 33 段

![frame 33](./frames/frame_033.jpg)

> **EN:** But here's the thing.
>
> **ZH:** 但問題是，

---

### [00:01:39] 第 34 段

![frame 34](./frames/frame_034.jpg)

> **EN:** In my conversation history, there is now a lot of back and forth around that broken package.
>
> **ZH:** 在我的對話歷史中，已經累積了大量圍繞那個有問題套件的來回討論。

---

### [00:01:44] 第 35 段

![frame 35](./frames/frame_035.jpg)

> **EN:** Now this is a bunch of context that is not at all relevant to running the next set of
>
> **ZH:** 這些都是與撰寫下一組測試完全不相關的 context。

---

### [00:01:49] 第 36 段

![frame 36](./frames/frame_036.jpg)

> **EN:** tests.
>
> **ZH:** 完全無關的 context。

---

### [00:01:50] 第 37 段

![frame 37](./frames/frame_037.jpg)

> **EN:** Ideally, we would be able to jump back in time and go back to the previous message we sent
>
> **ZH:** 理想上，我們能夠跳回過去，回到我們之前發送的訊息，

---

### [00:01:55] 第 38 段

![frame 38](./frames/frame_038.jpg)

> **EN:** and just update it to say, write tests for a get session.
>
> **ZH:** 直接把它改成「為 get session 撰寫測試」。

---

### [00:01:58] 第 39 段

![frame 39](./frames/frame_039.jpg)

> **EN:** Now the benefit here is that we maintain the context where Claude already took a look at
>
> **ZH:** 這樣做的好處是，我們保留了 Claude 已經讀過 auth.ts 檔案內容的 context，

---

### [00:02:02] 第 40 段

![frame 40](./frames/frame_040.jpg)

> **EN:** the contents of the auth.ts file, and it already knows what we're talking about when we refer
>
> **ZH:** 它也已經知道我們說的 get session 是什麼。

---

### [00:02:06] 第 41 段

![frame 41](./frames/frame_041.jpg)

> **EN:** to get session.
>
> **ZH:** 而且因為我們去掉了那些只是關於除錯的多餘訊息，

---

### [00:02:08] 第 42 段

![frame 42](./frames/frame_042.jpg)

> **EN:** And because we dumped all those extra messages that were just about debugging, we're not going
>
> **ZH:** 不會有那麼多干擾了。

---

### [00:02:12] 第 43 段

![frame 43](./frames/frame_043.jpg)

> **EN:** to have as much distraction going on here.
>
> **ZH:** 不會有那麼多干擾。

---

### [00:02:14] 第 44 段

![frame 44](./frames/frame_044.jpg)

> **EN:** So again, Claude can really just stay focused and on task.
>
> **ZH:** 這樣 Claude 就能真正保持專注。

---

### [00:02:18] 第 45 段

![frame 45](./frames/frame_045.jpg)

> **EN:** To go back in the conversation history, hit escape twice.
>
> **ZH:** 要回到對話歷史，按兩下 escape。

---

### [00:02:21] 第 46 段

![frame 46](./frames/frame_046.jpg)

> **EN:** This will show you all the different messages that you have sent.
>
> **ZH:** 這會顯示你所有發送過的訊息。

---

### [00:02:23] 第 47 段

![frame 47](./frames/frame_047.jpg)

> **EN:** So you can rewind back to a previous point in time and skip over some intermediate conversation.
>
> **ZH:** 你可以倒退回過去某個時間點，跳過一些中間的對話。

---

### [00:02:29] 第 48 段

![frame 48](./frames/frame_048.jpg)

> **EN:** Claude is now going to start working on the next set of tests.
>
> **ZH:** Claude 現在開始處理下一組測試了。

---

### [00:02:32] 第 49 段

![frame 49](./frames/frame_049.jpg)

> **EN:** This time around Claude stays super focused, but unfortunately it runs into a number of issues.
>
> **ZH:** 這次 Claude 保持非常專注，但不幸的是遇到了一些問題。

---

### [00:02:36] 第 50 段

![frame 50](./frames/frame_050.jpg)

> **EN:** It eventually resolves them and gets the test to pass.
>
> **ZH:** 最終它解決了這些問題，讓測試通過。

---

### [00:02:40] 第 51 段

![frame 51](./frames/frame_051.jpg)

> **EN:** Now at this point, Claude has been working by itself for several minutes and has a really
>
> **ZH:** 現在，Claude 已經獨立工作了幾分鐘，對如何為這個檔案撰寫測試

---

### [00:02:43] 第 52 段

![frame 52](./frames/frame_052.jpg)

> **EN:** good idea of how to write tests for this file.
>
> **ZH:** 有了非常好的掌握。

---

### [00:02:46] 第 53 段

![frame 53](./frames/frame_053.jpg)

> **EN:** At the same time, once again, we have a bunch of context in this conversation history.
>
> **ZH:** 但同時，我們的對話歷史中又累積了大量 context。

---

### [00:02:51] 第 54 段

![frame 54](./frames/frame_054.jpg)

> **EN:** When it is time to write tests for the next function, I'm going to use a command called
>
> **ZH:** 當需要為下一個函式撰寫測試時，我要使用一個叫做

---

### [00:02:55] 第 55 段

![frame 55](./frames/frame_055.jpg)

> **EN:** compact.
>
> **ZH:** /compact 的指令。

---

### [00:02:57] 第 56 段

![frame 56](./frames/frame_056.jpg)

> **EN:** The compact command will take all the messages in the current conversation and summarize them.
>
> **ZH:** /compact 指令會彙整目前對話中的所有訊息並加以摘要。

---

### [00:03:02] 第 57 段

![frame 57](./frames/frame_057.jpg)

> **EN:** Compact is really useful when Claude has learned a lot about the current task and you want
>
> **ZH:** /compact 非常適合用在 Claude 已經充分了解目前任務、而你想要

---

### [00:03:06] 第 58 段

![frame 58](./frames/frame_058.jpg)

> **EN:** to maintain that knowledge as it goes into the next task.
>
> **ZH:** 在進入下一個任務時保留這些知識的情況。

---

### [00:03:10] 第 59 段

![frame 59](./frames/frame_059.jpg)

> **EN:** The last context related command to be aware of is the clear command.
>
> **ZH:** 最後一個需要知道的 context 相關指令是 /clear 指令。

---

### [00:03:13] 第 60 段

![frame 60](./frames/frame_060.jpg)

> **EN:** Clear will dump the entire conversation history, allowing you to start off from scratch.
>
> **ZH:** /clear 會清除整個對話歷史，讓你從頭開始。

---

### [00:03:18] 第 61 段

![frame 61](./frames/frame_061.jpg)

> **EN:** Clear is most useful anytime you are about to start on a completely different
>
> **ZH:** /clear 最適合用在你即將開始一個完全不同的、

---

### [00:03:21] 第 62 段

![frame 62](./frames/frame_062.jpg)

> **EN:** task unrelated to the current one.
>
> **ZH:** 與目前任務無關的任務時。

---

### [00:03:24] 第 63 段

![frame 63](./frames/frame_063.jpg)

> **EN:** I recommend using these shortcuts quite a bit, particularly when you are changing between
>
> **ZH:** 我建議多多使用這些快捷鍵，特別是當你在不同任務之間切換，

---

### [00:03:27] 第 64 段

![frame 64](./frames/frame_064.jpg)

> **EN:** tasks or anytime you are having a long running conversation with Claude.
>
> **ZH:** 或是與 Claude 進行長時間對話的時候。

---

### [00:03:31] 第 65 段

![frame 65](./frames/frame_065.jpg)

> **EN:** In the remainder of this course, we'll use them several times to make sure that Claude stays
>
> **ZH:** 在這門課程的後續部分，我們會多次使用它們，確保 Claude 保持

---

### [00:03:35] 第 66 段

![frame 66](./frames/frame_066.jpg)

> **EN:** on task and focused.
>
> **ZH:** 專注在任務上。

---
