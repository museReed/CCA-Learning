#!/usr/bin/env python3
"""
Generate bilingual SRT files (EN + ZH) from original English SRT files.
Each subtitle entry gets a Chinese translation line added below the English.

Generates two variants per video:
  - EN + zh-TW (Traditional Chinese) → *_bilingual.srt
  - EN + zh-CN (Simplified Chinese)  → *_bilingual_zh-CN.srt
"""

import re
from pathlib import Path

from zh_cn_translations import (
    INTRODUCING_HOOKS_ZH_CN,
    DEFINING_HOOKS_ZH_CN,
    IMPLEMENTING_HOOK_ZH_CN,
    USEFUL_HOOKS_ZH_CN,
)

BASE_DIR = Path("/Volumes/Muse_AI_Core/CCA-Learning/courses/claude-code-in-action/05-hooks")

# Unit directory mapping: (srt_filename, unit_dir)
UNIT_MAP = {
    "Introducing_hooks_3uGhMBFx.srt": "14-introducing-hooks",
    "Defining_hooks_qzgBYFlx.srt": "15-defining-hooks",
    "Implementing_a_hook_WpOJxKsp.srt": "16-implementing-a-hook",
    "Useful_hooks_fXIRG62r.srt": "18-useful-hooks",
}

# ============================================================
# Translations
# ============================================================

INTRODUCING_HOOKS_ZH = {
    1: "在這個影片中，我們來看看 hooks。",
    2: "它們讓你可以在 Claude 嘗試執行工具之前或之後執行命令。",
    3: "Hooks 可以用來實現非常有趣且實用的功能。",
    4: "例如，在 Claude 決定寫入檔案後，你可以自動執行程式碼格式化工具",
    5: "對剛建立的檔案進行格式化。",
    6: "或者你可以在檔案被編輯後執行測試。",
    7: "或者你可以阻止 Claude 讀取特定檔案。",
    8: "可能性真的是無窮的，我準備了幾個好例子",
    9: "來展示如何在你的專案中使用 hooks。",
    10: "不過首先，讓我幫你理解 hooks 到底怎麼運作。",
    11: "提醒一下，當你向 Claude Code 提問時，你的查詢會連同一些工具定義",
    12: "一起送到 Claude 模型。",
    13: "Claude 模型可能會透過提供一個格式化的回應來決定執行某個工具。",
    14: "到這個時候，就由 Claude Code 來執行被請求的工具，比如在這個案例中",
    15: "讀取一個檔案，然後回傳工具呼叫的結果。",
    16: "現在 hooks 讓我們有能力在工具執行之前或之後執行程式碼。",
    17: "在工具之前執行的 hooks 被稱為 PreToolUse hooks，因為它們在",
    18: "工具之前執行。",
    19: "在工具之後執行的 hooks 被稱為 PostToolUse，原因相同。",
    20: "要定義 hooks，我們在 Claude 設定檔中加入設定。",
    21: "記住有幾個不同的設定檔。",
    22: "一個是你機器上所有專案的全域設定。",
    23: "一個是你特定專案的設定，會與其他工程師共用；另一個是只屬於你的",
    24: "特定專案設定。",
    25: "你可以手動在設定檔中寫出 hooks，或是使用內建的",
    26: "Claude Code 的 /hooks 指令。",
    27: "設定本身看起來就像你在螢幕右側看到的樣子。",
    28: "讓我帶你看看這個範例檔案，讓你更了解是怎麼回事。",
    29: "首先注意這個檔案裡有兩個不同的區塊。",
    30: "一個區塊列出了所有在工具使用之前應該執行的命令。",
    31: "記住那些被稱為 PreToolUse hooks。",
    32: "另一個區塊列出了所有在工具使用之後應該執行的",
    33: "不同命令。",
    34: "同樣的，那些是 PostToolUse hooks。",
    35: "在每個區塊中，我們提供一個 matcher。",
    36: "這表示我們要匹配哪些工具使用類型。",
    37: "所以在這個案例中，我想匹配 Read 工具的使用。",
    38: "每當 Claude Code 嘗試讀取檔案時，我想執行你看到列出的那個命令。",
    39: "同樣在 PostToolUse 區塊中，在使用 Write、Edit 或 MultiEdit 工具之後，",
    40: "有一個不同的命令我想要執行。",
    41: "現在重點來了。",
    42: "這就是 hooks 真正的用途。",
    43: "你看到的那些命令會收到 Claude 想要執行的工具呼叫的詳細資訊。",
    44: "在 PreToolUse hook 的情況下，你可以檢查 Claude 想做什麼。",
    45: "如果出於任何原因你不想允許它，你可以阻擋工具使用操作並",
    46: "把錯誤訊息送回給 Claude。",
    47: "在 PostToolUse hook 的情況下，工具呼叫已經發生了，所以阻擋",
    48: "已經太遲了。",
    49: "所以你可以基於工具呼叫做一些後續操作，比如格式化一個",
    50: "剛被編輯的檔案。",
    51: "你也可以向 Claude 回傳一些關於該工具使用的訊息。",
    52: "例如，你可能決定執行一個獨立的程式來檢查編輯的程式碼品質，",
    53: "或者做型別檢查，然後把回饋提供給 Claude。",
    54: "Claude 可能會根據回饋去更新它剛寫入的檔案。",
    55: "如果你仍然對 hooks 或它們的用途感到困惑，那完全",
    56: "沒問題。",
    57: "理解 hooks 確實可能很有挑戰性。",
    58: "所以讓我們等一下回來，用一個範例專案來練習 hooks。",
}

DEFINING_HOOKS_ZH = {
    1: "為了更好地了解 hooks 的運作方式，我們來看一個新的範例專案。",
    2: "這堂課附帶了一個叫做 queries.zip 的檔案。",
    3: "我建議你下載這個專案，然後用你的程式碼編輯器打開它。",
    4: "編輯器打開後，在終端機裡執行 npm run setup。",
    5: "這會安裝一些依賴套件，並準備好幾個 hooks 讓你使用。",
    6: "為了更深入理解 hooks，我們要在這個專案裡自己做一個。",
    7: "我希望我們的 hook 做到以下這件事。",
    8: "在專案的根目錄裡有一個叫做 .env 的檔案。",
    9: "這個檔案包含一些敏感資訊。",
    10: "為了謹慎起見，我想要完全防止 Claude 直接讀取這個檔案。",
    11: "讓我用幾張圖來幫助你理解我們要怎麼組合這個 hook。",
    12: "第一步是決定我們需要 pre-tool use 還是 post-tool use hook。",
    13: "在這個情境下，我們想要阻止 Claude 讀取特定檔案。",
    14: "如果我們用 post-tool use 區塊，那我們的 hook 會在 Claude 已經讀完檔案之後才執行。",
    15: "所以在這個情況下，我們絕對需要一個 pre-tool use hook，確保我們能在讀取操作發生之前就把它擋下來。",
    16: "接下來我們要決定的是，到底要監控哪些類型的 tool call。",
    17: "在這張圖的右邊，我列出了目前所有不同的 tool 名稱。",
    18: "要背下 Claude Code 裡所有不同的 tool 名稱其實蠻有挑戰性的，",
    19: "尤其是你還可以透過 MCP server 加入你自己的自訂工具。",
    20: "所以讓我教你一個小技巧。",
    21: "如果我切回去打開 Claude Code，我可以直接問 Claude 列出它目前可以使用的所有 tool 名稱。",
    22: "在這些工具裡面，有兩個可以很輕鬆地讀取檔案內容。",
    23: "第一個是 read tool，然後還有一個很容易被忽略的，其實也能讀取檔案內容。",
    24: "就是 grep tool。",
    25: "grep 可以搜尋檔案的內容。",
    26: "所以我們真正需要監控的是 read tool 和 grep tool 的 tool call。",
    27: "接下來，我們需要寫一個 command，它會接收 Claude 想要執行的 tool call 的相關資訊。",
    28: "這部分的運作方式是這樣的。",
    29: "我們會寫一個 command。",
    30: "Claude 會自動執行它。",
    31: "然後透過 standard in，Claude 會把一些 tool call 的資料以 JSON 格式餵進去。",
    32: "在右上角我放了一個 tool call 資料的範例。",
    33: "它會是一個大的 JSON 物件，包含 tool 名稱和該 tool 的輸入參數。",
    34: "在這個例子裡，tool 名稱是 read。",
    35: "也就是說 Claude 正在嘗試呼叫 read tool，而且它可能正試圖讀取一個指向那個 .env 檔案的路徑。",
    36: "而這就是我們想要阻止讀取操作的那個檔案。",
    37: "所以在我們的程式或 command 裡面，我們需要透過 standard in 接收這些資訊、解析那個 JSON，然後讀取 tool 名稱、tool 的輸入參數等等，接著決定要怎麼處理這個 tool call。",
    38: "然後進入第四步。",
    39: "在第四步，當我們的 command 接收到提議的 tool call 資料後，我們就會 exit。",
    40: "而我們的 exit code 會向 Claude Code 回傳一個訊號。",
    41: "exit code 為零代表一切正常，我們允許這個 tool call 執行。",
    42: "但 exit code 為二，則是告訴 Claude Code 我們要封鎖這個 tool call。",
    43: "這專門只適用於 pre-tool use hooks，因為記住，只有在 pre-tool use hook 裡我們才能真正封鎖一個 tool call。",
    44: "如果我們以 exit code 二結束，那麼在 command 執行期間我們產生的任何 standard error 日誌也會作為回饋發送給 Claude。",
    45: "所以我們可以同時拒絕 tool call 並告訴 Claude 原因。",
    46: "以上就是整個流程。",
    47: "我知道，這裡又有很多東西要消化。",
    48: "所以讓我們在專案裡從頭到尾走一遍這個 hook 的完整接線過程，來理解所有步驟是怎麼串在一起的。",
}

IMPLEMENTING_HOOK_ZH = {
    1: "我們來組合自己的自訂 hook。",
    2: "記住，這裡的整個目標是防止 Claude 讀取 .env 檔案的內容。",
    3: "在上一支影片中，我們討論了許多需要設定的不同配置選項。",
    4: "所以在這支影片中，我們主要會專注在實作上。",
    5: "首先，在 .claude 目錄裡面，我要打開 settings.local.json 這個檔案。",
    6: "記住，在這裡面我們有一個 pre-tool use hooks 和 post-tool use hooks 的列表。",
    7: "如同我們剛才討論的，我們要做一個 pre-tool use hook，這樣就能防止 Claude 讀取那個特定檔案的內容。",
    8: "我已經在這裡預先加了一小段配置區塊，幫我們省一點打字的時間。",
    9: "我們只需要填入 matcher 和 command 就好。",
    10: "首先是 matcher。",
    11: "matcher 就是我們想要監控的工具。",
    12: "在我們的案例中，如同討論過的，我們要監控對 read 和 grep 工具的呼叫。",
    13: "我要用一個 pipe 符號來分隔這兩個工具名稱。",
    14: "那不是字母 L 也不是大寫的 I。",
    15: "它是你鍵盤上 return 鍵正上方的那個符號。",
    16: "接下來，我們需要提供一個 command，在 Claude 嘗試呼叫這兩個工具時執行。",
    17: "你可以在這裡放任何你想要的命令。",
    18: "可以是一個 CLI。",
    19: "可以是呼叫一個 shell script。",
    20: "什麼都可以。",
    21: "為了延續我在這個檔案其他地方已經建立的模式，",
    22: "我要呼叫一個 node.js 腳本，我事先放在這個專案的 hooks 目錄裡面。",
    23: "在 hooks 目錄裡面，我幫我們準備了一個 read_hook.js 檔案。",
    24: "這就是我想在 Claude 嘗試呼叫那兩個工具時執行的檔案。",
    25: "所以要呼叫它的話，我要把這裡的 true（目前只是一個佔位符）",
    26: "替換成 node ./hooks/read_hook.js。",
    27: "然後我要存檔，在這個檔案裡我們要做的就這些。",
    28: "接下來，我們需要實際實作那個在 Claude 嘗試呼叫",
    29: "read 或 grep 工具時會執行的 command。",
    30: "也就是 read_hook.js 這個檔案。",
    31: "在這個檔案的最上面，我有一些程式碼會從 standard in 讀取資料並解析成 JSON。",
    32: "這裡的 toolArgs 物件，就是我在這張圖表中展示給你看的那個大 JSON 物件，",
    33: "就在這邊。",
    34: "它會有像 session ID、tool name、tool input 等等這些屬性。",
    35: "所以我們真正需要做的就是看一下那個 file path，然後判斷它",
    36: "是不是在嘗試讀取 .env 檔案。",
    37: "然後在我們的程式或 command 裡面，我們需要透過 standard in 接收這些資訊，解析那個 JSON，然後讀取 tool name、tool input 的參數等等，決定我們要怎麼處理這個工具呼叫。",
    38: "然後到第四步。",
    39: "在第四步，當我們的 command 收到那個提議的工具呼叫資料後，我們接著要 exit。",
    40: "你會注意到回到這邊，我已經有一些程式碼會讀取那個 file path。",
    41: "你也會注意到這裡有一個 fallback 去看 toolInput.path。",
    42: "我等一下會告訴你為什麼要加這個。",
    43: "現在我們來實作這個 TODO 的部分。",
    44: "我們寫：如果 readPath 包含 .env。",
    45: "那就代表 Claude 一定是在嘗試讀取 .env 檔案。",
    46: "如果是這種情況，我要確保我們阻擋這個操作，並提供一些",
    47: "日誌回饋給 Claude。",
    48: "Claude。",
    49: "所以我要先加一個 console.error，特別是 console.error，因為",
    50: "我們要輸出到 standard error。",
    51: "記住，這就是我們提供回饋給 Claude 的方式。",
    52: "我會寫類似「你不能讀取 .env 檔案」這樣的訊息。",
    53: "然後我會做 process.exit(2)。",
    54: "現在來測試一下，我要存檔。",
    55: "我要打開 Claude Code。",
    56: "如果你已經打開了，請確保你重新啟動 Claude Code。",
    57: "你必須重新啟動它，hooks 的任何變更才會生效。",
    58: "我要請 Claude 讀取 .env 檔案。",
    59: "它大概會嘗試去讀，但當它嘗試讀取時，我們會回傳",
    60: "一個錯誤說「你不能讀取 .env 檔案」。",
    61: "然後 Claude 應該就會意識到，抱歉，你其實不能讀這個檔案。",
    62: "事實上，它甚至能辨識出是被一個 read hook 擋下來的。",
    63: "現在，我們的 hook 應該對 grep 操作也同樣有效。",
    64: "所以如果我請 Claude 試試 grep 工具，這應該也會被禁止。",
    65: "我們來看看效果如何。",
    66: "沒錯，一樣的結果。",
    67: "現在也被禁止了。",
    68: "這就是我們組合出來的一個可運作的 hook。",
    69: "這個 hook 不是特別實用，我等一下會展示一個",
    70: "更實用的 hook 給你看。",
}

USEFUL_HOOKS_ZH = {
    1: "在這支影片中，我想展示一些非常實用的 hooks，你可能會想在自己的專案裡使用",
    2: "這些 hooks。",
    3: "這些 hooks 的目的是解決 Claude Code 的一些常見弱點。",
    4: "為了讓你理解第一個 hook 的運作方式，讓我先快速示範一個",
    5: "Claude Code 有時候會遇到的問題，尤其是在比較大的專案裡。",
    6: "在 SRC 目錄裡面，我要找到 schema.ts。",
    7: "裡面只有一個函式叫做 create schema。",
    8: "這個函式是從 main.ts 檔案呼叫的，就在這裡。",
    9: "現在我要回到 schema.ts 檔案，然後更新這個函式定義。",
    10: "我要加一個條件：如果你要呼叫這個函式，你必須同時傳入一個 verbose",
    11: "參數，型別必須是 Boolean。",
    12: "一旦我加了這個改動，如果我回到 main.ts 檔案，就會",
    13: "出現一個 type error，因為我更新了這個函式的定義，但我還沒有",
    14: "實際傳入 verbose 的值。",
    15: "這個錯誤明確指出：verbose 的參數沒有被提供。",
    16: "現在我快速把這個改動復原。",
    17: "我要關掉 main.ts 檔案。",
    18: "然後打開 Claude Code，請它做完全一樣的改動。",
    19: "如果我執行這個，Claude Code 做這個編輯完全沒問題，",
    20: "但它只會更新這個檔案。",
    21: "然後很不幸地，做完改動之後——verbose true 就在那裡。",
    22: "不幸的是，Claude 不會主動去整個專案裡找這個函式實際被呼叫的地方，",
    23: "然後更新那些呼叫點。",
    24: "所以如果我現在打開 main.ts，會看到這裡確實有個錯誤，而 Claude",
    25: "很遺憾地沒有抓到這個問題。",
    26: "所以我要展示的第一個 hook 可以超輕鬆地解決這個問題。",
    27: "如果你不熟悉 TypeScript，沒關係，完全沒問題。",
    28: "如果我關掉 Claude Code 然後執行 tsc --noEmit 這個指令，它會對我整個專案",
    29: "跑一次 type check。",
    30: "在這個 type check 的結果裡，我們可以看到錯誤非常明顯地出現在這裡。",
    31: "它在抱怨我們從 main.ts 檔案裡呼叫 create schema 的那段程式碼。",
    32: "所以我的 hook 想法其實很簡單。",
    33: "我認為每次我們編輯一個 TypeScript 檔案的時候，都應該跑 TypeScript type checker",
    34: "然後看看有沒有任何新的錯誤。",
    35: "如果有的話，我們應該在 post tool use hook 裡面",
    36: "立即把這些錯誤回饋給 Claude。",
    37: "希望這能給 Claude 一個訊號，告訴它剛剛引入了一個 type error，",
    38: "它可能需要去專案的其他地方修復。",
    39: "我已經幫我們把這個 hook 寫好了，省點時間，",
    40: "就在 hooks 的 tsc.js 檔案裡。",
    41: "在這個檔案裡，我寫了一堆邏輯來執行 TypeScript type checker，",
    42: "把它找到的任何錯誤回傳給 Claude。",
    43: "目前我先停用了這個 hook，這樣才能做剛才那個示範給你看。",
    44: "我是透過加上 process.exit(0) 來停用的，就在那裡。",
    45: "我現在要把它刪掉。",
    46: "這樣這個 hook 就能正常運作了。",
    47: "所以如果我現在回到 schema.ts 檔案，移除 verbose 旗標，重啟 Claude Code，",
    48: "然後再請它做一次同樣的改動，它會完成改動。",
    49: "然後希望這次它會立刻從 TypeScript type checker 得到回饋，",
    50: "說：「嘿，你剛在專案其他地方引入了一個錯誤。」",
    51: "希望 Claude 就會去修復它。",
    52: "我們可以看到這裡，編輯已經完成了。",
    53: "我們從我們建的 hook 得到了一些 edit operation 的回饋。",
    54: "它在我們其中一個檔案裡發現了問題。",
    55: "然後 Claude 現在說：好，我知道我引入了一個錯誤。",
    56: "我需要修復 main.ts 裡面呼叫 create schema 的地方。",
    57: "接下來它做的更新就是去那個檔案裡面",
    58: "把函式呼叫更新，加上缺少的參數。",
    59: "所以這是一個你可能會想在自己的專案裡實作的 hook。",
    60: "雖然這個 hook 是專門為 TypeScript 寫的，但它其實適用於任何",
    61: "可以輕鬆跑 type checker 的型別語言。",
    62: "即使你用的是無型別的語言，你也可以用測試來實現同樣的功能，",
    63: "而不是跑 type checker。",
    64: "所以每次做完編輯，你都可以跑測試來確保改動沒問題。",
    65: "接下來我要展示的 hook 稍微難解釋一點，",
    66: "但一旦你理解了背後的概念，我覺得你一定會覺得這個 hook 非常有用，",
    67: "尤其是在比較大的專案裡。",
    68: "為了幫你理解這個 hook，我想先介紹一下這個專案的背景。",
    69: "在 SRC queries 目錄裡面，有很多不同的檔案。",
    70: "每個檔案裡都包含了很多用函式寫的 SQL queries。",
    71: "特別是在 orderqueries.ts 檔案裡面，我想指出有一個函式叫做",
    72: "get pending orders。",
    73: "這個 query 會查詢一個包含電商資料的資料庫。",
    74: "理論上，它會找出所有已建立且處於 pending 狀態的訂單。",
    75: "先記住這個函式，等一下會用到。",
    76: "好，我要快速展示幾張圖，幫你理解在大型專案中",
    77: "常會出現的一個問題。",
    78: "在這張圖裡，左邊是我的不同 query 檔案列表。",
    79: "正如我們看到的，每個 query 檔案裡都包含很多不同的 queries。",
    80: "特別是在那個 orderqueries.ts 檔案裡面就有 get pending orders 函式。",
    81: "所以我們已經有一個現成的 query 可以用來找 pending 的訂單了。",
    82: "現在如果我去問 Claude，請它更新 main.ts 檔案來印出所有",
    83: "pending 超過三天的訂單，",
    84: "在理想情況下，Claude 會找到 orderqueries.ts 檔案。",
    85: "它會找到那個現有的 query 然後直接用它，",
    86: "而不是寫一個全新的 query。",
    87: "這才是我們想要的結果。",
    88: "而且如果我們現在就讓 Claude 去做這件事，",
    89: "我們會得到我們想要的結果。",
    90: "所以我要請 Claude：在 main.ts 檔案裡，印出 pending 狀態的訂單。",
    91: "說句公道話，Claude 確實會去看現有的 query 檔案。",
    92: "它會找到 orderqueries 檔案。",
    93: "然後在裡面，它會發現已經有一個叫做 get pending orders 的 query。",
    94: "然後它會嘗試使用那個函式，而不是建立一個新的 query。",
    95: "我們不想要新的 query。",
    96: "我們希望 Claude 使用現有的函式。",
    97: "所以當我們給 Claude 一個很聚焦、很明確的任務時，",
    98: "它能理解，對，它可能不應該寫新的 query。",
    99: "它至少應該先看看已經存在的那些。",
    100: "這確實很好。",
    101: "現在我要給 Claude 出個難題。",
    102: "我要故意把這個任務變得更困難一點。",
    103: "首先，我要執行 /clear 來清除我們累積的所有 context。",
    104: "然後我希望你看一下 task.md 檔案。",
    105: "在這個檔案裡，我寫了一個 prompt，還是會請 Claude 找 pending 一段時間的訂單。",
    106: "但我把它包在一個更大的專案裡面。",
    107: "我請 Claude 寫一個 Slack 整合，每天對特定頻道發一次訊息，",
    108: "列出所有 pending 太久的訂單。",
    109: "所以在這個情境裡，我們還是要找 pending 太久的訂單。",
    110: "但現在我把它包在一個更大的任務裡面了。",
    111: "如果我把這個任務丟給 Claude，在做完 /clear 之後，",
    112: "我們會看到這一次它不會那麼聚焦了。",
    113: "它最終會試著寫一個全新的 get pending orders query，",
    114: "這又不是我們想要的，因為這會在專案裡產生重複的程式碼。",
    115: "如果我讓它跑一陣子，最終會看到它確實建了一個新的 query 叫 get orders pending too long。",
    116: "所以這就是一個 Claude 失焦的例子，它決定寫一個全新的 query 而不是重用現有的。",
    117: "又出現重複程式碼了，這可能不是我們想要的。",
    118: "不僅如此，它不只建了新的 query。",
    119: "它還建了一個全新的檔案，這大概也不是我們想要的。",
    120: "我們可能會希望把這個訂單相關的 query 加到 order queries 檔案裡。",
    121: "現在我們理解了這個問題，讓我展示如何用 hook 來修復它。",
    122: "好。",
    123: "每當 Claude 嘗試用 write、edit 或 multi-edit 工具去修改 queries 目錄裡的東西時，",
    124: "我就會執行以下這個 hook。",
    125: "首先，在這個 hook 裡，我會啟動一個全新的、獨立的 Claude Code 副本。",
    126: "我會請這個新的副本去看剛才做的改動，同時看看 queries 目錄裡的現有程式碼，檢查是否已經有類似的 query 存在。",
    127: "然後如果有現成的 query，我就會把這個回饋傳回給原本的 Claude 副本。",
    128: "然後請 Claude 決定要不要修正這個情況。",
    129: "也就是移除新加的 query，改用已經存在的那個。",
    130: "這樣就能確保 queries 資料夾保持乾淨，不會有一堆重複的程式碼。",
    131: "讓我展示一下實際運作的效果。",
    132: "首先，我切回這邊。",
    133: "我要刪掉剛建的 order alerts queries.ts 檔案和 slack.ts 檔案。",
    134: "然後我要在 hooks 目錄裡找到 query hook 檔案。",
    135: "我已經幫我們把這個 hook 寫好了。",
    136: "現在它目前是停用的，因為我在最上面放了 process.exit。",
    137: "讓我們快速走過這個 hook。",
    138: "首先，我告訴它只要檢查對 SRC queries 目錄的改動。",
    139: "再往下一點，我會檢查剛才的改動是不是在 queries 目錄裡做的。",
    140: "接著這裡有一段長長的 prompt，請 Claude 對剛才的改動做 review。",
    141: "然後在那之後就是我用程式化方式啟動 Claude Code 的地方。",
    142: "具體來說就是這幾行。",
    143: "這裡用的是 Claude Code 的 TypeScript SDK。",
    144: "等一下我可以給你更多相關資訊。",
    145: "現在你只要理解這裡基本上等同於我們在終端機使用 Claude Code。",
    146: "Claude Code 跑完之後我拿到回應，我會檢查 Claude 是判斷改動沒問題，",
    147: "還是有重複的 query。",
    148: "如果有的話，我們就會用 exit code 2 提前結束，這會把回饋傳回 Claude，希望能告訴它需要做修改。",
    149: "現在這個額外的 hook 已經啟用了——我移除了頂部的 process.exit(0)——我要再次重啟 Claude Code。",
    150: "然後再跑一次同樣的指令。",
    151: "希望這次它可能一開始還是會放入重複的 query，但我們的 hook 會執行並告訴它：嘿，我們不要重複的程式碼。",
    152: "你應該用已經存在的 query 來實現這個功能。",
    153: "Claude Code 又會試著建立一個全新的、完全獨立的 query 檔案，沒有使用已經存在的 query。",
    154: "但當它試著建立那個檔案時，我們的 hook 就會執行。",
    155: "它會啟動那個獨立的 Claude Code 副本，去做一些研究，然後發現確實有一個現成的 query 可以重用。",
    156: "它會提供建議說：嘿，你可以去修改這個現有的 query 來完美符合你的需求。",
    157: "然後我們會看到我們正在互動的主要 Claude 實例的回饋說：啊對，有這個現成的 query。",
    158: "我們就修改這個現有的 query，而不是寫一個全新的。",
    159: "這個 hook 的缺點是，每次我要編輯 queries 目錄裡的東西時，都會額外花一些時間和費用。",
    160: "但好處是，我的 queries 目錄裡會少很多重複的程式碼。",
    161: "所以這真的取決於你自己的取捨，決定要不要在自己的專案裡實作這樣的東西。",
    162: "如果你要做的話，我至少建議像 query hook 裡展示的那樣做。",
    163: "就是這個，只監控少數幾個目錄，像是專案裡真正重要的資料夾，盡量減少額外的工作量。",
}

# ============================================================
# SRT file config: (filename, translations, max_valid_entry)
# ============================================================

# (filename, zh-TW translations, zh-CN translations, max_valid_entry)
SRT_CONFIG = [
    ("Introducing_hooks_3uGhMBFx.srt", INTRODUCING_HOOKS_ZH, INTRODUCING_HOOKS_ZH_CN, 58),
    ("Defining_hooks_qzgBYFlx.srt", DEFINING_HOOKS_ZH, DEFINING_HOOKS_ZH_CN, 48),
    ("Implementing_a_hook_WpOJxKsp.srt", IMPLEMENTING_HOOK_ZH, IMPLEMENTING_HOOK_ZH_CN, 70),
    ("Useful_hooks_fXIRG62r.srt", USEFUL_HOOKS_ZH, USEFUL_HOOKS_ZH_CN, 163),
]


def parse_srt(srt_path: Path, max_entry: int) -> list[dict]:
    """Parse SRT file into list of {index, timestamp, text}."""
    content = srt_path.read_text(encoding="utf-8")
    entries = []
    blocks = re.split(r"\n\n+", content.strip())

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        try:
            index = int(lines[0])
        except ValueError:
            continue
        if index > max_entry:
            break

        text = " ".join(lines[2:]).strip()
        if not text:
            continue

        entries.append({
            "index": index,
            "timestamp": lines[1],
            "text_en": text,
        })

    return entries


def generate_bilingual_srt(entries: list[dict], translations: dict, output_path: Path):
    """Generate bilingual SRT with ZH line below EN line."""
    blocks = []
    for entry in entries:
        idx = entry["index"]
        zh = translations.get(idx, "")
        lines = [
            str(idx),
            entry["timestamp"],
            entry["text_en"],
        ]
        if zh:
            lines.append(zh)
        blocks.append("\n".join(lines))

    output_path.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")
    print(f"  Written: {output_path.name} ({len(entries)} entries)")


def main():
    for filename, zh_tw, zh_cn, max_entry in SRT_CONFIG:
        unit_dir = UNIT_MAP.get(filename)
        if not unit_dir:
            print(f"  SKIP: {filename} has no unit mapping")
            continue

        srt_dir = BASE_DIR / unit_dir / "srt"
        srt_path = srt_dir / filename
        if not srt_path.exists():
            print(f"  SKIP: {srt_path} not found")
            continue

        out_dir = srt_dir / "bilingual"
        out_dir.mkdir(exist_ok=True)

        entries = parse_srt(srt_path, max_entry)

        # EN + zh-TW
        out_tw = srt_path.stem + "_bilingual.srt"
        generate_bilingual_srt(entries, zh_tw, out_dir / out_tw)

        # EN + zh-CN
        out_cn = srt_path.stem + "_bilingual_zh-CN.srt"
        generate_bilingual_srt(entries, zh_cn, out_dir / out_cn)

    print("\nDone! Bilingual SRTs (zh-TW + zh-CN) generated per unit.")


if __name__ == "__main__":
    main()
