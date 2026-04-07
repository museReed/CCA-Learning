# Custom Commands — 自訂指令 — 影片逐幀學習指南

| 項目 | 內容 |
|------|------|
| 課程 | claude-code-in-action / 03-context-and-commands / 11-custom-commands |
| 影片 | Custom Commands |
| 字幕數 | 26 段 |
| 格式 | 每段字幕一張截圖 + 雙語字幕（英/中） |

---

### [00:00:00] 第 1 段

![frame 1](./frames/frame_001.jpg)

> **EN:** When you run Cloud Code, you can enter in a forward slash and see a bunch of commands that are built into Cloud Code by default.
>
> **ZH:** 當你執行 Claude Code 時，你可以輸入斜線，然後看到一堆 Claude Code 預設內建的指令。

---

### [00:00:06] 第 2 段

![frame 2](./frames/frame_002.jpg)

> **EN:** In addition to these default commands, you can easily add your own custom commands as well.
>
> **ZH:** 除了這些預設指令之外，你也可以輕鬆地加入自己的 custom commands。

---

### [00:00:11] 第 3 段

![frame 3](./frames/frame_003.jpg)

> **EN:** Custom commands are useful for automating repetitive tasks that you find yourself running frequently.
>
> **ZH:** Custom commands 適合用來自動化你經常重複執行的任務。

---

### [00:00:15] 第 4 段

![frame 4](./frames/frame_004.jpg)

> **EN:** Let me show you an example of how to make one.
>
> **ZH:** 讓我示範如何建立一個。

---

### [00:00:17] 第 5 段

![frame 5](./frames/frame_005.jpg)

> **EN:** Inside of my project directory, I'm going to find the .cloud folder.
>
> **ZH:** 在我的專案目錄裡，我要找到 .claude 資料夾。

---

### [00:00:21] 第 6 段

![frame 6](./frames/frame_006.jpg)

> **EN:** Inside there, I'll make a new directory called commands.
>
> **ZH:** 在那個資料夾裡，我會建立一個叫做 commands 的新目錄。

---

### [00:00:24] 第 7 段

![frame 7](./frames/frame_007.jpg)

> **EN:** And then inside that, I'll make a new file called audit.md.
>
> **ZH:** 然後在裡面，我會建立一個叫做 audit.md 的新檔案。

---

### [00:00:28] 第 8 段

![frame 8](./frames/frame_008.jpg)

> **EN:** The name of the file that we create, in this case audit, is going to be the name of the command we eventually run.
>
> **ZH:** 我們建立的這個檔案的名稱——在這個例子中是 audit——就會是我們最終執行的指令名稱。

---

### [00:00:33] 第 9 段

![frame 9](./frames/frame_009.jpg)

> **EN:** The goal of this command is going to be to audit all the different dependencies that have been installed into this project,
>
> **ZH:** 這個指令的目標是稽核這個專案中所有已安裝的相依套件，

---

### [00:00:38] 第 10 段

![frame 10](./frames/frame_010.jpg)

> **EN:** update them if there are any vulnerabilities, and then run tests to make sure that nothing actually broke.
>
> **ZH:** 如果有任何安全漏洞就更新它們，然後執行測試確保沒有東西壞掉。

---

### [00:00:44] 第 11 段

![frame 11](./frames/frame_011.jpg)

> **EN:** Once you have created the command file, you'll then restart Cloud Code.
>
> **ZH:** 建立好指令檔案之後，你要重新啟動 Claude Code。

---

### [00:00:48] 第 12 段

![frame 12](./frames/frame_012.jpg)

> **EN:** Don't forget to restart it.
>
> **ZH:** 別忘了重新啟動它。

---

### [00:00:49] 第 13 段

![frame 13](./frames/frame_013.jpg)

> **EN:** When you reopen Cloud Code, put in slash audit.
>
> **ZH:** 重新開啟 Claude Code 時，輸入 /audit。

---

### [00:00:52] 第 14 段

![frame 14](./frames/frame_014.jpg)

> **EN:** This will then display the command that you just created.
>
> **ZH:** 這樣就會顯示你剛剛建立的指令。

---

### [00:00:54] 第 15 段

![frame 15](./frames/frame_015.jpg)

> **EN:** You can then run this, and in this case, it will do exactly what we asked Cloud to do.
>
> **ZH:** 你可以執行它，在這個例子中，它會完全按照我們要求 Claude 做的事情來執行。

---

### [00:00:58] 第 16 段

![frame 16](./frames/frame_016.jpg)

> **EN:** It'll run a command, see if there are any vulnerable packages, fix them if necessary, and then run tests.
>
> **ZH:** 它會執行指令、檢查是否有容易受攻擊的套件、必要時修復它們，然後執行測試。

---

### [00:01:04] 第 17 段

![frame 17](./frames/frame_017.jpg)

> **EN:** Commands can also receive arguments.
>
> **ZH:** Custom commands 也可以接收參數。

---

### [00:01:06] 第 18 段

![frame 18](./frames/frame_018.jpg)

> **EN:** Let me show you an example.
>
> **ZH:** 讓我給你看一個範例。

---

### [00:01:07] 第 19 段

![frame 19](./frames/frame_019.jpg)

> **EN:** I'm going to make another command called write tests.
>
> **ZH:** 我要再建立一個叫做 write tests 的指令。

---

### [00:01:10] 第 20 段

![frame 20](./frames/frame_020.jpg)

> **EN:** Whenever I run this command, I want to have some tests created for a very particular file inside my project.
>
> **ZH:** 每次我執行這個指令時，我想為專案中某個特定檔案建立測試。

---

### [00:01:16] 第 21 段

![frame 21](./frames/frame_021.jpg)

> **EN:** Inside of the command text, I'm going to put in a placeholder of $arguments.
>
> **ZH:** 在指令文字中，我會加入一個 $ARGUMENTS 的佔位符。

---

### [00:01:20] 第 22 段

![frame 22](./frames/frame_022.jpg)

> **EN:** Whenever I run the command, if I pass in a path to a file, that path will be inserted at $arguments.
>
> **ZH:** 每次我執行這個指令時，如果我傳入一個檔案路徑，那個路徑就會被插入到 $ARGUMENTS 的位置。

---

### [00:01:26] 第 23 段

![frame 23](./frames/frame_023.jpg)

> **EN:** So now I can restart Cloud Code again, and then execute the write test command.
>
> **ZH:** 所以現在我可以再次重新啟動 Claude Code，然後執行 write test 指令。

---

### [00:01:31] 第 24 段

![frame 24](./frames/frame_024.jpg)

> **EN:** Now, to be clear, the arguments we pass in don't have to be a file path.
>
> **ZH:** 現在要說清楚，我們傳入的參數不一定要是檔案路徑。

---

### [00:01:35] 第 25 段

![frame 25](./frames/frame_025.jpg)

> **EN:** It can be any string we want to pass in.
>
> **ZH:** 它可以是任何我們想要傳入的字串。

---

### [00:01:37] 第 26 段

![frame 26](./frames/frame_026.jpg)

> **EN:** So I might casually ask for tests for a file in some particular folder, giving Cloud just a little bit of direction on where to look.
>
> **ZH:** 所以我可能隨意地要求為某個特定資料夾中的一個檔案撰寫測試，給 Claude 一點關於在哪裡找的方向提示。

---
