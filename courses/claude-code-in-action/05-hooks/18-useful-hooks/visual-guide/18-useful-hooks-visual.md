# Useful Hooks — 實用 Hooks — 影片逐幀學習指南

| 項目 | 內容 |
|------|------|
| 課程 | claude-code-in-action / 05-hooks / Lesson 18 |
| 影片 | Useful Hooks |
| 字幕數 | 163 段 |
| 格式 | 每段字幕一張截圖 + 雙語字幕（英/中） |

---

### [00:00:00] 第 1 段

![frame 1](./frames/frame_001.jpg)

> **EN:** In this video, I'd like to show you some really useful hooks that you might want to use on
>
> **ZH:** 在這支影片中，我想展示一些非常實用的 hooks，你可能會想在自己的專案裡使用

---

### [00:00:04] 第 2 段

![frame 2](./frames/frame_002.jpg)

> **EN:** your own projects.
>
> **ZH:** 這些 hooks。

---

### [00:00:05] 第 3 段

![frame 3](./frames/frame_003.jpg)

> **EN:** These hooks are intended to address some common weak points in CloudCode.
>
> **ZH:** 這些 hooks 的目的是解決 Claude Code 的一些常見弱點。

---

### [00:00:09] 第 4 段

![frame 4](./frames/frame_004.jpg)

> **EN:** To help you understand how the first one works, let me give you a quick demonstration of a
>
> **ZH:** 為了讓你理解第一個 hook 的運作方式，讓我先快速示範一個

---

### [00:00:13] 第 5 段

![frame 5](./frames/frame_005.jpg)

> **EN:** problem that CloudCode sometimes runs into, especially on larger projects.
>
> **ZH:** Claude Code 有時候會遇到的問題，尤其是在比較大的專案裡。

---

### [00:00:18] 第 6 段

![frame 6](./frames/frame_006.jpg)

> **EN:** So inside the SRC directory, I'm going to find schema.ts.
>
> **ZH:** 在 SRC 目錄裡面，我要找到 schema.ts。

---

### [00:00:22] 第 7 段

![frame 7](./frames/frame_007.jpg)

> **EN:** Inside of here, there's just one single function called create schema.
>
> **ZH:** 裡面只有一個函式叫做 create schema。

---

### [00:00:26] 第 8 段

![frame 8](./frames/frame_008.jpg)

> **EN:** This function is called from the main.ts file specifically right here.
>
> **ZH:** 這個函式是從 main.ts 檔案呼叫的，就在這裡。

---

### [00:00:31] 第 9 段

![frame 9](./frames/frame_009.jpg)

> **EN:** Now I'm going to go back to the schema.ts file and I'm going to update the function definition.
>
> **ZH:** 現在我要回到 schema.ts 檔案，然後更新這個函式定義。

---

### [00:00:35] 第 10 段

![frame 10](./frames/frame_010.jpg)

> **EN:** I'm going to say that if you ever want to call this function, you must also pass in a verbose
>
> **ZH:** 我要加一個條件：如果你要呼叫這個函式，你必須同時傳入一個 verbose

---

### [00:00:40] 第 11 段

![frame 11](./frames/frame_011.jpg)

> **EN:** argument that must be of type Boolean.
>
> **ZH:** 參數，型別必須是 Boolean。

---

### [00:00:43] 第 12 段

![frame 12](./frames/frame_012.jpg)

> **EN:** Now as soon as I add in this change, if I go back over to the main.ts file, I'm going to
>
> **ZH:** 一旦我加了這個改動，如果我回到 main.ts 檔案，就會

---

### [00:00:47] 第 13 段

![frame 13](./frames/frame_013.jpg)

> **EN:** get a type error because I just updated the definition of this function, but I have not
>
> **ZH:** 出現一個 type error，因為我更新了這個函式的定義，但我還沒有

---

### [00:00:51] 第 14 段

![frame 14](./frames/frame_014.jpg)

> **EN:** actually added in a value for verbose.
>
> **ZH:** 實際傳入 verbose 的值。

---

### [00:00:54] 第 15 段

![frame 15](./frames/frame_015.jpg)

> **EN:** So the error right here says specifically argument for verbose was not provided.
>
> **ZH:** 這個錯誤明確指出：verbose 的參數沒有被提供。

---

### [00:01:00] 第 16 段

![frame 16](./frames/frame_016.jpg)

> **EN:** Now I'm going to undo that change very quickly.
>
> **ZH:** 現在我快速把這個改動復原。

---

### [00:01:02] 第 17 段

![frame 17](./frames/frame_017.jpg)

> **EN:** I'm going to close the main.ts file.
>
> **ZH:** 我要關掉 main.ts 檔案。

---

### [00:01:04] 第 18 段

![frame 18](./frames/frame_018.jpg)

> **EN:** I'm then going to open up CloudCode and ask it to make the exact same change.
>
> **ZH:** 然後打開 Claude Code，請它做完全一樣的改動。

---

### [00:01:10] 第 19 段

![frame 19](./frames/frame_019.jpg)

> **EN:** Now if I run this, CloudCode is going to have absolutely no issue making this edit whatsoever,
>
> **ZH:** 如果我執行這個，Claude Code 做這個編輯完全沒問題，

---

### [00:01:15] 第 20 段

![frame 20](./frames/frame_020.jpg)

> **EN:** but it's going to update this file.
>
> **ZH:** 但它只會更新這個檔案。

---

### [00:01:16] 第 21 段

![frame 21](./frames/frame_021.jpg)

> **EN:** And then unfortunately, after making that change, so there's the new verbose true right there.
>
> **ZH:** 然後很不幸地，做完改動之後——verbose true 就在那裡。

---

### [00:01:21] 第 22 段

![frame 22](./frames/frame_022.jpg)

> **EN:** Unfortunately, Cloud won't go around the project and try to find where that function is actually
>
> **ZH:** 不幸的是，Claude 不會主動去整個專案裡找這個函式實際被呼叫的地方，

---

### [00:01:25] 第 23 段

![frame 23](./frames/frame_023.jpg)

> **EN:** called and try to update any of the different call sites.
>
> **ZH:** 然後更新那些呼叫點。

---

### [00:01:28] 第 24 段

![frame 24](./frames/frame_024.jpg)

> **EN:** So if I now open up main.ts, we'll see that we do in fact have an error over here and Cloud
>
> **ZH:** 所以如果我現在打開 main.ts，會看到這裡確實有個錯誤，而 Claude

---

### [00:01:33] 第 25 段

![frame 25](./frames/frame_025.jpg)

> **EN:** didn't really catch this unfortunately.
>
> **ZH:** 很遺憾地沒有抓到這個問題。

---

### [00:01:35] 第 26 段

![frame 26](./frames/frame_026.jpg)

> **EN:** So the first hook that I want to show you will fix this solution super easily.
>
> **ZH:** 所以我要展示的第一個 hook 可以超輕鬆地解決這個問題。

---

### [00:01:39] 第 27 段

![frame 27](./frames/frame_027.jpg)

> **EN:** In case you're not familiar with TypeScript, if you're not, that's totally fine.
>
> **ZH:** 如果你不熟悉 TypeScript，沒關係，完全沒問題。

---

### [00:01:42] 第 28 段

![frame 28](./frames/frame_028.jpg)

> **EN:** If I close out a CloudCode and run the command tsc-noemit, that's going to run a type check
>
> **ZH:** 如果我關掉 Claude Code 然後執行 tsc --noEmit 這個指令，它會對我整個專案

---

### [00:01:49] 第 29 段

![frame 29](./frames/frame_029.jpg)

> **EN:** on my entire project.
>
> **ZH:** 跑一次 type check。

---

### [00:01:51] 第 30 段

![frame 30](./frames/frame_030.jpg)

> **EN:** And in this type check, we can see that the error is very evident right here.
>
> **ZH:** 在這個 type check 的結果裡，我們可以看到錯誤非常明顯地出現在這裡。

---

### [00:01:55] 第 31 段

![frame 31](./frames/frame_031.jpg)

> **EN:** So it's complaining about our call to create schema from that main.ts file.
>
> **ZH:** 它在抱怨我們從 main.ts 檔案裡呼叫 create schema 的那段程式碼。

---

### [00:01:59] 第 32 段

![frame 32](./frames/frame_032.jpg)

> **EN:** So my idea for a hook is really simple.
>
> **ZH:** 所以我的 hook 想法其實很簡單。

---

### [00:02:02] 第 33 段

![frame 33](./frames/frame_033.jpg)

> **EN:** I think that any time that we edit a TypeScript file, we should run the TypeScript type checker
>
> **ZH:** 我認為每次我們編輯一個 TypeScript 檔案的時候，都應該跑 TypeScript type checker

---

### [00:02:07] 第 34 段

![frame 34](./frames/frame_034.jpg)

> **EN:** and see if there are any distinct errors.
>
> **ZH:** 然後看看有沒有任何新的錯誤。

---

### [00:02:10] 第 35 段

![frame 35](./frames/frame_035.jpg)

> **EN:** If there are, we should attempt to feed these errors back into Cloud immediately inside of
>
> **ZH:** 如果有的話，我們應該在 post tool use hook 裡面

---

### [00:02:14] 第 36 段

![frame 36](./frames/frame_036.jpg)

> **EN:** a post tool use hook.
>
> **ZH:** 立即把這些錯誤回饋給 Claude。

---

### [00:02:16] 第 37 段

![frame 37](./frames/frame_037.jpg)

> **EN:** And hopefully this will give Cloud a signal and tell it that there is a type error that
>
> **ZH:** 希望這能給 Claude 一個訊號，告訴它剛剛引入了一個 type error，

---

### [00:02:20] 第 38 段

![frame 38](./frames/frame_038.jpg)

> **EN:** it just introduced that it probably needs to go and fix somewhere else inside of our project.
>
> **ZH:** 它可能需要去專案的其他地方修復。

---

### [00:02:25] 第 39 段

![frame 39](./frames/frame_039.jpg)

> **EN:** Now I already put this hook together for us, fortunately, just to save us a little bit
>
> **ZH:** 我已經幫我們把這個 hook 寫好了，省點時間，

---

### [00:02:28] 第 40 段

![frame 40](./frames/frame_040.jpg)

> **EN:** of time inside the hooks tsc.js file.
>
> **ZH:** 就在 hooks 的 tsc.js 檔案裡。

---

### [00:02:32] 第 41 段

![frame 41](./frames/frame_041.jpg)

> **EN:** So inside this file, I've got a bunch of logic put together to run the TypeScript type checker,
>
> **ZH:** 在這個檔案裡，我寫了一堆邏輯來執行 TypeScript type checker，

---

### [00:02:36] 第 42 段

![frame 42](./frames/frame_042.jpg)

> **EN:** take any errors that it found and pass them back into Cloud.
>
> **ZH:** 把它找到的任何錯誤回傳給 Claude。

---

### [00:02:40] 第 43 段

![frame 43](./frames/frame_043.jpg)

> **EN:** At present, I disabled this hook just so I can give you that demonstration you just saw.
>
> **ZH:** 目前我先停用了這個 hook，這樣才能做剛才那個示範給你看。

---

### [00:02:45] 第 44 段

![frame 44](./frames/frame_044.jpg)

> **EN:** So I disabled it by adding the process exit zero right there.
>
> **ZH:** 我是透過加上 process.exit(0) 來停用的，就在那裡。

---

### [00:02:47] 第 45 段

![frame 45](./frames/frame_045.jpg)

> **EN:** I'm going to delete that.
>
> **ZH:** 我現在要把它刪掉。

---

### [00:02:49] 第 46 段

![frame 46](./frames/frame_046.jpg)

> **EN:** And now this hook should be working a-okay.
>
> **ZH:** 這樣這個 hook 就能正常運作了。

---

### [00:02:51] 第 47 段

![frame 47](./frames/frame_047.jpg)

> **EN:** So if I now go back to the schema.ts file, remove that verbose flag, restart Cloud code,
>
> **ZH:** 所以如果我現在回到 schema.ts 檔案，移除 verbose 旗標，重啟 Claude Code，

---

### [00:03:00] 第 48 段

![frame 48](./frames/frame_048.jpg)

> **EN:** and ask it to make the same change once again, it will make the change.
>
> **ZH:** 然後再請它做一次同樣的改動，它會完成改動。

---

### [00:03:05] 第 49 段

![frame 49](./frames/frame_049.jpg)

> **EN:** And then hopefully this time it will immediately get that feedback from the TypeScript type checker
>
> **ZH:** 然後希望這次它會立刻從 TypeScript type checker 得到回饋，

---

### [00:03:09] 第 50 段

![frame 50](./frames/frame_050.jpg)

> **EN:** saying, Hey, you've got an error somewhere else in the project that you've just introduced.
>
> **ZH:** 說：「嘿，你剛在專案其他地方引入了一個錯誤。」

---

### [00:03:13] 第 51 段

![frame 51](./frames/frame_051.jpg)

> **EN:** And hopefully Cloud will go and fix it.
>
> **ZH:** 希望 Claude 就會去修復它。

---

### [00:03:15] 第 52 段

![frame 52](./frames/frame_052.jpg)

> **EN:** So we can see right here, there's the edit that was made.
>
> **ZH:** 我們可以看到這裡，編輯已經完成了。

---

### [00:03:18] 第 53 段

![frame 53](./frames/frame_053.jpg)

> **EN:** We got some edit operation feedback from the hook that we put together.
>
> **ZH:** 我們從我們建的 hook 得到了一些 edit operation 的回饋。

---

### [00:03:21] 第 54 段

![frame 54](./frames/frame_054.jpg)

> **EN:** So it found an issue inside of one of our different files.
>
> **ZH:** 它在我們其中一個檔案裡發現了問題。

---

### [00:03:24] 第 55 段

![frame 55](./frames/frame_055.jpg)

> **EN:** And Cloud is now saying, okay, I understand I introduced an error.
>
> **ZH:** 然後 Claude 現在說：好，我知道我引入了一個錯誤。

---

### [00:03:28] 第 56 段

![frame 56](./frames/frame_056.jpg)

> **EN:** I need to fix the call to create schema inside of main.ts.
>
> **ZH:** 我需要修復 main.ts 裡面呼叫 create schema 的地方。

---

### [00:03:32] 第 57 段

![frame 57](./frames/frame_057.jpg)

> **EN:** And then the next update it makes is going to attempt to go into that file and update that
>
> **ZH:** 接下來它做的更新就是去那個檔案裡面

---

### [00:03:37] 第 58 段

![frame 58](./frames/frame_058.jpg)

> **EN:** function call to add in that missing argument.
>
> **ZH:** 把函式呼叫更新，加上缺少的參數。

---

### [00:03:39] 第 59 段

![frame 59](./frames/frame_059.jpg)

> **EN:** So this is a hook that you might want to try implementing on your own personal projects.
>
> **ZH:** 所以這是一個你可能會想在自己的專案裡實作的 hook。

---

### [00:03:44] 第 60 段

![frame 60](./frames/frame_060.jpg)

> **EN:** Now, even though this hook was implemented specifically for TypeScript, it still works for any other kind of
>
> **ZH:** 雖然這個 hook 是專門為 TypeScript 寫的，但它其實適用於任何

---

### [00:03:49] 第 61 段

![frame 61](./frames/frame_061.jpg)

> **EN:** type language where you can run a type checker very easily.
>
> **ZH:** 可以輕鬆跑 type checker 的型別語言。

---

### [00:03:52] 第 62 段

![frame 62](./frames/frame_062.jpg)

> **EN:** Even if you're using an untyped language, you might even implement the same idea of functionality using
>
> **ZH:** 即使你用的是無型別的語言，你也可以用測試來實現同樣的功能，

---

### [00:03:57] 第 63 段

![frame 63](./frames/frame_063.jpg)

> **EN:** tests instead of running a type checker.
>
> **ZH:** 而不是跑 type checker。

---

### [00:04:00] 第 64 段

![frame 64](./frames/frame_064.jpg)

> **EN:** So every time an edit is made, you could run your tests to make sure that the edit is okay.
>
> **ZH:** 所以每次做完編輯，你都可以跑測試來確保改動沒問題。

---

### [00:04:04] 第 65 段

![frame 65](./frames/frame_065.jpg)

> **EN:** Now, the next hook that I would like to show you is a little bit more challenging to explain,
>
> **ZH:** 接下來我要展示的 hook 稍微難解釋一點，

---

### [00:04:09] 第 66 段

![frame 66](./frames/frame_066.jpg)

> **EN:** but once you get the idea behind it, I think that you will definitely find this next one really helpful,
>
> **ZH:** 但一旦你理解了背後的概念，我覺得你一定會覺得這個 hook 非常有用，

---

### [00:04:14] 第 67 段

![frame 67](./frames/frame_067.jpg)

> **EN:** particularly in larger projects.
>
> **ZH:** 尤其是在比較大的專案裡。

---

### [00:04:15] 第 68 段

![frame 68](./frames/frame_068.jpg)

> **EN:** To help you understand this other hook, I want to give you a little bit of background on this project.
>
> **ZH:** 為了幫你理解這個 hook，我想先介紹一下這個專案的背景。

---

### [00:04:20] 第 69 段

![frame 69](./frames/frame_069.jpg)

> **EN:** Inside of the SRC queries directory, there are many different files.
>
> **ZH:** 在 SRC queries 目錄裡面，有很多不同的檔案。

---

### [00:04:24] 第 70 段

![frame 70](./frames/frame_070.jpg)

> **EN:** Each of these different files contains many different SQL queries written inside of different functions.
>
> **ZH:** 每個檔案裡都包含了很多用函式寫的 SQL queries。

---

### [00:04:29] 第 71 段

![frame 71](./frames/frame_071.jpg)

> **EN:** Inside of the orderqueries.ts file in particular, I want to point out that there is a function inside
>
> **ZH:** 特別是在 orderqueries.ts 檔案裡面，我想指出有一個函式叫做

---

### [00:04:34] 第 72 段

![frame 72](./frames/frame_072.jpg)

> **EN:** of here called get pending orders.
>
> **ZH:** get pending orders。

---

### [00:04:36] 第 73 段

![frame 73](./frames/frame_073.jpg)

> **EN:** This query goes through a database that contains some e-commerce related data.
>
> **ZH:** 這個 query 會查詢一個包含電商資料的資料庫。

---

### [00:04:41] 第 74 段

![frame 74](./frames/frame_074.jpg)

> **EN:** And in theory, it's going to find all the different orders that have been created that are in a pending state.
>
> **ZH:** 理論上，它會找出所有已建立且處於 pending 狀態的訂單。

---

### [00:04:46] 第 75 段

![frame 75](./frames/frame_075.jpg)

> **EN:** So just keep that function in mind for a moment.
>
> **ZH:** 先記住這個函式，等一下會用到。

---

### [00:04:49] 第 76 段

![frame 76](./frames/frame_076.jpg)

> **EN:** Okay, so I'm going to show you a couple of diagrams really quickly to help you understand a common problem
>
> **ZH:** 好，我要快速展示幾張圖，幫你理解在大型專案中

---

### [00:04:53] 第 77 段

![frame 77](./frames/frame_077.jpg)

> **EN:** that starts to arise inside of larger projects.
>
> **ZH:** 常會出現的一個問題。

---

### [00:04:56] 第 78 段

![frame 78](./frames/frame_078.jpg)

> **EN:** So in this diagram, I've got my list of different query files on the left-hand side.
>
> **ZH:** 在這張圖裡，左邊是我的不同 query 檔案列表。

---

### [00:05:00] 第 79 段

![frame 79](./frames/frame_079.jpg)

> **EN:** And as we saw, each of those different query files contains many different queries.
>
> **ZH:** 正如我們看到的，每個 query 檔案裡都包含很多不同的 queries。

---

### [00:05:04] 第 80 段

![frame 80](./frames/frame_080.jpg)

> **EN:** Inside of that orderqueries.ts file in particular is the get pending orders function.
>
> **ZH:** 特別是在那個 orderqueries.ts 檔案裡面就有 get pending orders 函式。

---

### [00:05:08] 第 81 段

![frame 81](./frames/frame_081.jpg)

> **EN:** So we've already got a query put together that will attempt to find some different pending orders.
>
> **ZH:** 所以我們已經有一個現成的 query 可以用來找 pending 的訂單了。

---

### [00:05:14] 第 82 段

![frame 82](./frames/frame_082.jpg)

> **EN:** Now, if I go to Claude and ask it to update the main.ts file to print out all the different orders
>
> **ZH:** 現在如果我去問 Claude，請它更新 main.ts 檔案來印出所有

---

### [00:05:20] 第 83 段

![frame 83](./frames/frame_083.jpg)

> **EN:** that have been in a pending state for longer than three days,
>
> **ZH:** pending 超過三天的訂單，

---

### [00:05:23] 第 84 段

![frame 84](./frames/frame_084.jpg)

> **EN:** in a perfect world, Claude would find the orderqueries.ts file.
>
> **ZH:** 在理想情況下，Claude 會找到 orderqueries.ts 檔案。

---

### [00:05:27] 第 85 段

![frame 85](./frames/frame_085.jpg)

> **EN:** It would find that existing query and it would make use of it,
>
> **ZH:** 它會找到那個現有的 query 然後直接用它，

---

### [00:05:30] 第 86 段

![frame 86](./frames/frame_086.jpg)

> **EN:** as opposed to writing out a brand new query.
>
> **ZH:** 而不是寫一個全新的 query。

---

### [00:05:33] 第 87 段

![frame 87](./frames/frame_087.jpg)

> **EN:** So that's what we want.
>
> **ZH:** 這才是我們想要的結果。

---

### [00:05:34] 第 88 段

![frame 88](./frames/frame_088.jpg)

> **EN:** And we'll see that if we make use of Claude right now and ask it to do exactly that,
>
> **ZH:** 而且如果我們現在就讓 Claude 去做這件事，

---

### [00:05:39] 第 89 段

![frame 89](./frames/frame_089.jpg)

> **EN:** we're going to get exactly the result we want.
>
> **ZH:** 我們會得到我們想要的結果。

---

### [00:05:42] 第 90 段

![frame 90](./frames/frame_090.jpg)

> **EN:** So I'm going to ask Claude in the main.ts file, print out orders that have been pending.
>
> **ZH:** 所以我要請 Claude：在 main.ts 檔案裡，印出 pending 狀態的訂單。

---

### [00:05:46] 第 91 段

![frame 91](./frames/frame_091.jpg)

> **EN:** Now, to Claude's credit, it is going to take a look at the different query files that exist.
>
> **ZH:** 說句公道話，Claude 確實會去看現有的 query 檔案。

---

### [00:05:50] 第 92 段

![frame 92](./frames/frame_092.jpg)

> **EN:** It's going to find the orderqueries file.
>
> **ZH:** 它會找到 orderqueries 檔案。

---

### [00:05:52] 第 93 段

![frame 93](./frames/frame_093.jpg)

> **EN:** And then inside there, it's going to recognize that there is already a query called get pending orders.
>
> **ZH:** 然後在裡面，它會發現已經有一個叫做 get pending orders 的 query。

---

### [00:05:57] 第 94 段

![frame 94](./frames/frame_094.jpg)

> **EN:** And it's going to attempt to use that function as opposed to creating a new query.
>
> **ZH:** 然後它會嘗試使用那個函式，而不是建立一個新的 query。

---

### [00:06:01] 第 95 段

![frame 95](./frames/frame_095.jpg)

> **EN:** We didn't want a new query.
>
> **ZH:** 我們不想要新的 query。

---

### [00:06:03] 第 96 段

![frame 96](./frames/frame_096.jpg)

> **EN:** We wanted Claude to use the existing function.
>
> **ZH:** 我們希望 Claude 使用現有的函式。

---

### [00:06:06] 第 97 段

![frame 97](./frames/frame_097.jpg)

> **EN:** So when we gave Claude a very focused and directed task,
>
> **ZH:** 所以當我們給 Claude 一個很聚焦、很明確的任務時，

---

### [00:06:08] 第 98 段

![frame 98](./frames/frame_098.jpg)

> **EN:** it was able to understand that, yeah, it probably shouldn't write a new query.
>
> **ZH:** 它能理解，對，它可能不應該寫新的 query。

---

### [00:06:12] 第 99 段

![frame 99](./frames/frame_099.jpg)

> **EN:** It should at least take a look at some of the ones that already exist.
>
> **ZH:** 它至少應該先看看已經存在的那些。

---

### [00:06:15] 第 100 段

![frame 100](./frames/frame_100.jpg)

> **EN:** And that was definitely good.
>
> **ZH:** 這確實很好。

---

### [00:06:16] 第 101 段

![frame 101](./frames/frame_101.jpg)

> **EN:** Now I'm going to give Claude a little bit of a curveball.
>
> **ZH:** 現在我要給 Claude 出個難題。

---

### [00:06:19] 第 102 段

![frame 102](./frames/frame_102.jpg)

> **EN:** I'm going to purposefully make this task a little bit more difficult.
>
> **ZH:** 我要故意把這個任務變得更困難一點。

---

### [00:06:22] 第 103 段

![frame 103](./frames/frame_103.jpg)

> **EN:** First, I'm going to run slash clear to clear out all the context that we've gained.
>
> **ZH:** 首先，我要執行 /clear 來清除我們累積的所有 context。

---

### [00:06:26] 第 104 段

![frame 104](./frames/frame_104.jpg)

> **EN:** Then I'd like you to take a look at the task.md file.
>
> **ZH:** 然後我希望你看一下 task.md 檔案。

---

### [00:06:30] 第 105 段

![frame 105](./frames/frame_105.jpg)

> **EN:** Inside this file, I put together a prompt that is still going to ask Claude to find orders that have been pending for a while.
>
> **ZH:** 在這個檔案裡，我寫了一個 prompt，還是會請 Claude 找 pending 一段時間的訂單。

---

### [00:06:36] 第 106 段

![frame 106](./frames/frame_106.jpg)

> **EN:** But I've also wrapped it up in some larger project.
>
> **ZH:** 但我把它包在一個更大的專案裡面。

---

### [00:06:39] 第 107 段

![frame 107](./frames/frame_107.jpg)

> **EN:** I'm asking Claude to write out a Slack integration that's going to message a specific channel once a day
>
> **ZH:** 我請 Claude 寫一個 Slack 整合，每天對特定頻道發一次訊息，

---

### [00:06:45] 第 108 段

![frame 108](./frames/frame_108.jpg)

> **EN:** with all the different orders that have been pending for too long.
>
> **ZH:** 列出所有 pending 太久的訂單。

---

### [00:06:48] 第 109 段

![frame 109](./frames/frame_109.jpg)

> **EN:** So in this scenario, we still want to find orders that have been pending for too long.
>
> **ZH:** 所以在這個情境裡，我們還是要找 pending 太久的訂單。

---

### [00:06:52] 第 110 段

![frame 110](./frames/frame_110.jpg)

> **EN:** But now I've wrapped it inside this larger task.
>
> **ZH:** 但現在我把它包在一個更大的任務裡面了。

---

### [00:06:54] 第 111 段

![frame 111](./frames/frame_111.jpg)

> **EN:** And if I take this task and then feed it into Claude, again, after doing that slash clear operation,
>
> **ZH:** 如果我把這個任務丟給 Claude，在做完 /clear 之後，

---

### [00:07:01] 第 112 段

![frame 112](./frames/frame_112.jpg)

> **EN:** we're going to see that this time around, unfortunately, it's not going to stay quite as focused.
>
> **ZH:** 我們會看到這一次它不會那麼聚焦了。

---

### [00:07:06] 第 113 段

![frame 113](./frames/frame_113.jpg)

> **EN:** And it's going to end up trying to write out a brand new get pending orders query,
>
> **ZH:** 它最終會試著寫一個全新的 get pending orders query，

---

### [00:07:10] 第 114 段

![frame 114](./frames/frame_114.jpg)

> **EN:** which is, again, not what we want, because that would be duplicating code throughout our project.
>
> **ZH:** 這又不是我們想要的，因為這會在專案裡產生重複的程式碼。

---

### [00:07:15] 第 115 段

![frame 115](./frames/frame_115.jpg)

> **EN:** If I let this run for a bit, I will eventually see that, yes, it does in fact make a brand new query called get orders pending too long.
>
> **ZH:** 如果我讓它跑一陣子，最終會看到它確實建了一個新的 query 叫 get orders pending too long。

---

### [00:07:23] 第 116 段

![frame 116](./frames/frame_116.jpg)

> **EN:** So this is an example of where Claude kind of lost focus and decided to write a brand new query as opposed to reusing an existing one.
>
> **ZH:** 所以這就是一個 Claude 失焦的例子，它決定寫一個全新的 query 而不是重用現有的。

---

### [00:07:30] 第 117 段

![frame 117](./frames/frame_117.jpg)

> **EN:** Again, we've got some duplicate code here, which is probably not what we want.
>
> **ZH:** 又出現重複程式碼了，這可能不是我們想要的。

---

### [00:07:34] 第 118 段

![frame 118](./frames/frame_118.jpg)

> **EN:** In addition, it didn't only create the new query.
>
> **ZH:** 不僅如此，它不只建了新的 query。

---

### [00:07:37] 第 119 段

![frame 119](./frames/frame_119.jpg)

> **EN:** It also created a brand new file, which is also probably something we don't want.
>
> **ZH:** 它還建了一個全新的檔案，這大概也不是我們想要的。

---

### [00:07:40] 第 120 段

![frame 120](./frames/frame_120.jpg)

> **EN:** We'd probably want this order related query to be added to the order queries file.
>
> **ZH:** 我們可能會希望把這個訂單相關的 query 加到 order queries 檔案裡。

---

### [00:07:45] 第 121 段

![frame 121](./frames/frame_121.jpg)

> **EN:** So now that we understand the issue here, let me show you how we could fix this potentially by making use of a hook.
>
> **ZH:** 現在我們理解了這個問題，讓我展示如何用 hook 來修復它。

---

### [00:07:51] 第 122 段

![frame 122](./frames/frame_122.jpg)

> **EN:** All right.
>
> **ZH:** 好。

---

### [00:07:51] 第 123 段

![frame 123](./frames/frame_123.jpg)

> **EN:** So whenever Claude attempts to write, edit, or use the multi-edit tool to modify something inside the queries directory specifically,
>
> **ZH:** 每當 Claude 嘗試用 write、edit 或 multi-edit 工具去修改 queries 目錄裡的東西時，

---

### [00:07:59] 第 124 段

![frame 124](./frames/frame_124.jpg)

> **EN:** I'm going to run the following hook.
>
> **ZH:** 我就會執行以下這個 hook。

---

### [00:08:01] 第 125 段

![frame 125](./frames/frame_125.jpg)

> **EN:** First, inside this hook, I'm going to launch a brand new separate copy of Claude code.
>
> **ZH:** 首先，在這個 hook 裡，我會啟動一個全新的、獨立的 Claude Code 副本。

---

### [00:08:06] 第 126 段

![frame 126](./frames/frame_126.jpg)

> **EN:** I'm going to ask this new copy to take a look at the change that was just made and take a look at some of the existing code inside the queries directory and see if a similar query is already inside there.
>
> **ZH:** 我會請這個新的副本去看剛才做的改動，同時看看 queries 目錄裡的現有程式碼，檢查是否已經有類似的 query 存在。

---

### [00:08:16] 第 127 段

![frame 127](./frames/frame_127.jpg)

> **EN:** Then if there is an existing query, then I'm going to take that feedback and send it back to the original copy of Claude.
>
> **ZH:** 然後如果有現成的 query，我就會把這個回饋傳回給原本的 Claude 副本。

---

### [00:08:22] 第 128 段

![frame 128](./frames/frame_128.jpg)

> **EN:** And I'm going to ask Claude to maybe decide to fix the situation.
>
> **ZH:** 然後請 Claude 決定要不要修正這個情況。

---

### [00:08:26] 第 129 段

![frame 129](./frames/frame_129.jpg)

> **EN:** So remove the added query and make use of the one that already exists.
>
> **ZH:** 也就是移除新加的 query，改用已經存在的那個。

---

### [00:08:29] 第 130 段

![frame 130](./frames/frame_130.jpg)

> **EN:** So this is going to allow us to make sure that the queries folder generally stays clean and doesn't have a bunch of duplicate code inside of it.
>
> **ZH:** 這樣就能確保 queries 資料夾保持乾淨，不會有一堆重複的程式碼。

---

### [00:08:37] 第 131 段

![frame 131](./frames/frame_131.jpg)

> **EN:** So let me show you how this would work in action.
>
> **ZH:** 讓我展示一下實際運作的效果。

---

### [00:08:39] 第 132 段

![frame 132](./frames/frame_132.jpg)

> **EN:** First, I'm going to flip back over here.
>
> **ZH:** 首先，我切回這邊。

---

### [00:08:41] 第 133 段

![frame 133](./frames/frame_133.jpg)

> **EN:** I'm going to delete the brand new order alerts queries.ts file that was made and the slack.ts file that was made as well.
>
> **ZH:** 我要刪掉剛建的 order alerts queries.ts 檔案和 slack.ts 檔案。

---

### [00:08:51] 第 134 段

![frame 134](./frames/frame_134.jpg)

> **EN:** Then I'm going to find inside the hooks directory, the query hook file.
>
> **ZH:** 然後我要在 hooks 目錄裡找到 query hook 檔案。

---

### [00:08:55] 第 135 段

![frame 135](./frames/frame_135.jpg)

> **EN:** So I already put this hook together for us.
>
> **ZH:** 我已經幫我們把這個 hook 寫好了。

---

### [00:08:57] 第 136 段

![frame 136](./frames/frame_136.jpg)

> **EN:** Right now it is currently disabled because I got a process.exit at the very top.
>
> **ZH:** 現在它目前是停用的，因為我在最上面放了 process.exit。

---

### [00:09:02] 第 137 段

![frame 137](./frames/frame_137.jpg)

> **EN:** So let's walk through this hook really quickly.
>
> **ZH:** 讓我們快速走過這個 hook。

---

### [00:09:04] 第 138 段

![frame 138](./frames/frame_138.jpg)

> **EN:** First, I'm going to tell this thing that it's only going to review changes to the SRC queries directory.
>
> **ZH:** 首先，我告訴它只要檢查對 SRC queries 目錄的改動。

---

### [00:09:09] 第 139 段

![frame 139](./frames/frame_139.jpg)

> **EN:** Then a little bit lower, I'm going to check and see if the change that was just made was made to the queries directory.
>
> **ZH:** 再往下一點，我會檢查剛才的改動是不是在 queries 目錄裡做的。

---

### [00:09:14] 第 140 段

![frame 140](./frames/frame_140.jpg)

> **EN:** After that, I've then got a long prompt here that is asking Claude to do a review on the change that was just made.
>
> **ZH:** 接著這裡有一段長長的 prompt，請 Claude 對剛才的改動做 review。

---

### [00:09:20] 第 141 段

![frame 141](./frames/frame_141.jpg)

> **EN:** And then after that is where I'm launching Claude code programmatically.
>
> **ZH:** 然後在那之後就是我用程式化方式啟動 Claude Code 的地方。

---

### [00:09:24] 第 142 段

![frame 142](./frames/frame_142.jpg)

> **EN:** Specifically these lines right here.
>
> **ZH:** 具體來說就是這幾行。

---

### [00:09:26] 第 143 段

![frame 143](./frames/frame_143.jpg)

> **EN:** This is making use of the Claude code TypeScript SDK.
>
> **ZH:** 這裡用的是 Claude Code 的 TypeScript SDK。

---

### [00:09:30] 第 144 段

![frame 144](./frames/frame_144.jpg)

> **EN:** I can give you a lot more information on it in just a little bit.
>
> **ZH:** 等一下我可以給你更多相關資訊。

---

### [00:09:33] 第 145 段

![frame 145](./frames/frame_145.jpg)

> **EN:** For right now, just understand that this right here is essentially the same as us making use of Claude code at the terminal.
>
> **ZH:** 現在你只要理解這裡基本上等同於我們在終端機使用 Claude Code。

---

### [00:09:39] 第 146 段

![frame 146](./frames/frame_146.jpg)

> **EN:** Once Claude code runs and I get a response back out of it, I check and see if Claude decides that, yeah, the changes look okay.
>
> **ZH:** Claude Code 跑完之後我拿到回應，我會檢查 Claude 是判斷改動沒問題，

---

### [00:09:45] 第 147 段

![frame 147](./frames/frame_147.jpg)

> **EN:** Or maybe we've got a duplicate query.
>
> **ZH:** 還是有重複的 query。

---

### [00:09:47] 第 148 段

![frame 148](./frames/frame_148.jpg)

> **EN:** And if we do, then we're going to exit early with an exit code of two, which is going to give this feedback back to Claude and hopefully tell it that it needs to make a change.
>
> **ZH:** 如果有的話，我們就會用 exit code 2 提前結束，這會把回饋傳回 Claude，希望能告訴它需要做修改。

---

### [00:09:55] 第 149 段

![frame 149](./frames/frame_149.jpg)

> **EN:** So now that I've got this additional hook put together and enabled by removing that process exit zero at the top, I'm going to again restart Claude code.
>
> **ZH:** 現在這個額外的 hook 已經啟用了——我移除了頂部的 process.exit(0)——我要再次重啟 Claude Code。

---

### [00:10:06] 第 150 段

![frame 150](./frames/frame_150.jpg)

> **EN:** And then run the same query again.
>
> **ZH:** 然後再跑一次同樣的指令。

---

### [00:10:09] 第 151 段

![frame 151](./frames/frame_151.jpg)

> **EN:** And hopefully this time it might initially put in that duplicate query, but then our hook right here is going to run and hopefully tell it, hey, we don't want that duplicate code.
>
> **ZH:** 希望這次它可能一開始還是會放入重複的 query，但我們的 hook 會執行並告訴它：嘿，我們不要重複的程式碼。

---

### [00:10:18] 第 152 段

![frame 152](./frames/frame_152.jpg)

> **EN:** You should make use of some already existing query to implement this functionality.
>
> **ZH:** 你應該用已經存在的 query 來實現這個功能。

---

### [00:10:21] 第 153 段

![frame 153](./frames/frame_153.jpg)

> **EN:** Now Claude code is once again going to attempt to create a brand new, completely separate query file, not making use of the old query that already existed.
>
> **ZH:** Claude Code 又會試著建立一個全新的、完全獨立的 query 檔案，沒有使用已經存在的 query。

---

### [00:10:30] 第 154 段

![frame 154](./frames/frame_154.jpg)

> **EN:** When it tries to create that file, however, our hook is going to run.
>
> **ZH:** 但當它試著建立那個檔案時，我們的 hook 就會執行。

---

### [00:10:34] 第 155 段

![frame 155](./frames/frame_155.jpg)

> **EN:** This is going to launch that separate copy of Claude code, which is going to do some research and find that there is in fact an existing query that can be reused.
>
> **ZH:** 它會啟動那個獨立的 Claude Code 副本，去做一些研究，然後發現確實有一個現成的 query 可以重用。

---

### [00:10:41] 第 156 段

![frame 156](./frames/frame_156.jpg)

> **EN:** It's going to provide some advice and say, hey, you could probably go and update this other existing query to suit your purposes perfectly.
>
> **ZH:** 它會提供建議說：嘿，你可以去修改這個現有的 query 來完美符合你的需求。

---

### [00:10:48] 第 157 段

![frame 157](./frames/frame_157.jpg)

> **EN:** And we'll see some feedback from Claude, our primary instance that we are interacting with saying, ah, yes, there is this existing query.
>
> **ZH:** 然後我們會看到我們正在互動的主要 Claude 實例的回饋說：啊對，有這個現成的 query。

---

### [00:10:55] 第 158 段

![frame 158](./frames/frame_158.jpg)

> **EN:** Let's just modify that existing query rather than attempting to write out a brand new one.
>
> **ZH:** 我們就修改這個現有的 query，而不是寫一個全新的。

---

### [00:11:00] 第 159 段

![frame 159](./frames/frame_159.jpg)

> **EN:** Now, the downside to this hook is that it's going to take some additional time and expense to run every single time that I want to edit something inside the queries directory.
>
> **ZH:** 這個 hook 的缺點是，每次我要編輯 queries 目錄裡的東西時，都會額外花一些時間和費用。

---

### [00:11:07] 第 160 段

![frame 160](./frames/frame_160.jpg)

> **EN:** But the upside is that I'm going to end up with a lot less duplicate code inside my queries directory.
>
> **ZH:** 但好處是，我的 queries 目錄裡會少很多重複的程式碼。

---

### [00:11:13] 第 161 段

![frame 161](./frames/frame_161.jpg)

> **EN:** So it really comes down to a set of trade-offs for you deciding whether or not you want to implement something like this in your own project.
>
> **ZH:** 所以這真的取決於你自己的取捨，決定要不要在自己的專案裡實作這樣的東西。

---

### [00:11:19] 第 162 段

![frame 162](./frames/frame_162.jpg)

> **EN:** If you do, I would at least recommend doing what I showed you inside of the query hook.
>
> **ZH:** 如果你要做的話，我至少建議像 query hook 裡展示的那樣做。

---

### [00:11:24] 第 163 段

![frame 163](./frames/frame_163.jpg)

> **EN:** So this one right here and only watching maybe a handful of directories, like really important folders inside of your project, just to minimize the amount of extra work that is being done.
>
> **ZH:** 就是這個，只監控少數幾個目錄，像是專案裡真正重要的資料夾，盡量減少額外的工作量。

---
