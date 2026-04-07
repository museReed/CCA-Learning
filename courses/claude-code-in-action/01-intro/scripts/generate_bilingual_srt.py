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
    INTRODUCTION_ZH_CN,
    WHAT_IS_CODING_ASSISTANT_ZH_CN,
    CLAUDE_CODE_IN_ACTION_ZH_CN,
)

BASE_DIR = Path("/Volumes/Muse_AI_Core/CCA-Learning/courses/claude-code-in-action/01-intro")

# Unit directory mapping: (srt_filename, unit_dir)
UNIT_MAP = {
    "Introduction_rLVnV1aS.srt": "02-introduction",
    "What_is_a_coding_assistant_WQnSCLF3.srt": "03-what-is-a-coding-assistant",
    "Claude_Code_in_action_3IQrknws.srt": "04-claude-code-in-action",
}

# ============================================================
# Translations (zh-TW)
# ============================================================

INTRODUCTION_ZH = {
    1: "哈囉，歡迎。我的名字是 Steven Greider，我是 Anthropic 的技術人員。",
    2: "在這門課程中，我們要帶你快速上手 Claude Code。在我們深入",
    3: "任何太技術的東西之前，我想先給你一個快速的課程大綱。",
    4: "這門課程分成四個部分。我們首先會花一些時間了解",
    5: "coding assistant 到底是什麼。接著我們會看看 Claude Code 本身，了解",
    6: "是什麼讓它在市面上眾多不同的 coding assistant 中脫穎而出。一旦我們",
    7: "建立了這些基礎，我們會在一個典型的專案中實際使用 Claude Code，並獲得一些",
    8: "實際操作的經驗。最後，我們會總結一下，看看如何在你自己的專案中",
    9: "把 Claude Code 發揮到最大效用。",
}

WHAT_IS_CODING_ASSISTANT_ZH = {
    1: "在這支影片中，我們要更深入了解 coding assistant 到底是什麼。",
    2: "沒錯，coding assistant 是一個會寫程式的工具，但我想讓你更了解",
    3: "它背後實際上發生了什麼事。",
    4: "你看，只要理解 coding assistant 真正在做什麼、它怎麼運作，你就會",
    5: "更能體會什麼樣的 assistant 才能真正成為你團隊的強力夥伴。",
    6: "有一種方式可以幫助你想像 coding assistant 在做什麼。",
    7: "assistant 首先會收到一個任務。",
    8: "比如說，assistant 可能需要根據某個錯誤訊息來修一個 bug。",
    9: "這個任務會在內部傳給一個 language model，它需要想辦法",
    10: "解決這個問題。",
    11: "不同的 language model 會用非常不同的方式解題，取決於",
    12: "任務的複雜程度，但在很多情況下，它的運作方式其實跟人類",
    13: "很像。",
    14: "它首先可能需要收集背景資訊，了解這個錯誤指的是什麼、是哪個部分的",
    15: "程式碼丟出這個錯誤，以及哪些檔案看起來是相關的。",
    16: "收集完這些資訊之後，它就需要擬定一個計畫，決定要怎麼",
    17: "完成這個任務。",
    18: "這個案例中，它可能會決定修改一些程式碼，然後執行或撰寫測試來確認",
    19: "問題是否真的修好了。",
    20: "最後，它會採取行動。",
    21: "在這個案例中，可能就是更新檔案並執行測試。",
    22: "現在，我想給你更多關於這整個過程的說明。",
    23: "特別是，我希望你注意到這裡的第一步和最後一步都需要 coding",
    24: "assistant 實際去做一些事情。",
    25: "換句話說，就是要從外部世界獲取資訊，或者以某種方式",
    26: "影響外部世界。",
    27: "比如說，要收集背景資訊，assistant 可能需要讀取一個檔案，或是抓取一些線上的",
    28: "文件。",
    29: "而執行行動時，assistant 可能需要實際執行一個指令或編輯一個檔案。",
    30: "要讓 language model 真正做到這些事，其實比聽起來",
    31: "要複雜一些。",
    32: "讓我來幫你理解為什麼會這樣。",
    33: "假設我們直接跟一個 language model 互動。",
    34: "也就是說，它沒有在任何 coding assistant 或類似工具裡面跑。",
    35: "然後假設我們直接問這個 language model，main.go 這個檔案",
    36: "裡面寫了什麼程式碼——在沒有 coding assistant 或類似工具的情況下跑的 language model",
    37: "本身並不具備讀取檔案、執行指令",
    38: "這類能力。",
    39: "Language model 接收的是文字這樣的內容，它回傳的也是文字。",
    40: "就這樣。",
    41: "這就是它們能力的全部範圍。",
    42: "而且所有的 language model 都是這樣。",
    43: "所以如果你傳一段文字給一個純粹的 language model，叫它讀取一個檔案，它",
    44: "很可能會回答說它沒有能力讀取任何檔案。",
    45: "所以讓我來展示一下 coding assistant 和市面上很多很多其他工具，是怎麼做到",
    46: "讓 language model 能夠「讀取」一個檔案的。",
    47: "是這樣運作的。",
    48: "每當你傳送一個請求給你的 coding assistant，coding assistant 在",
    49: "背後會自動在你的請求裡附加很多文字。",
    50: "在這個特別的案例中，我們可以想像 coding assistant 會加上",
    51: "一段文字，大概是說：language model，如果你想讀取一個檔案，請用",
    52: "這個格式非常仔細地回覆。",
    53: "比如說，可能是像 readfile 加上冒號，再加上要讀取的檔案名稱。",
    54: "這樣一來，language model 就會意識到，為了回答我們的問題，",
    55: "它需要用讀取那個檔案的方式來回應。",
    56: "所以它可能會回覆 readfile: main.go。",
    57: "接下來 coding assistant 就負責接收這個格式非常仔細的訊息，",
    58: "並且理解到 language model 想要採取某種行動——讀取一個檔案。",
    59: "所以 coding assistant 就負責實際讀取那個檔案，並把",
    60: "那個檔案的內容傳回給 language model。",
    61: "現在 language model 已經拿到那個檔案的實際內容，它就能寫出一個",
    62: "最終回應傳回給我們，裡面可能會說：我讀了這個檔案，",
    63: "它包含了一些程式碼，或者檔案裡有什麼其他東西。",
    64: "這整個系統——給 language model 這些額外的小指令，要求它用",
    65: "非常規範的格式回應——就叫做 tool use。",
    66: "所以 tools 是用來給 model 額外的能力的。",
    67: "model 負責以非常特定的方式回應。",
    68: "然後像 coding assistant 這樣的東西，就負責實際去執行",
    69: "所承諾的事情。",
    70: "也就是實際讀取一個檔案、寫入一個檔案，或者其他任何操作。",
    71: "再強調一次，所有的 language model 都是這樣運作的。",
    72: "它們都使用 tool use 這個概念。",
    73: "現在有一個關鍵點，是關於 Claude 這個系列的 model。",
    74: "Opus、Sonnet 和 Haiku 在理解 tools 被呼叫時的作用這方面特別強，",
    75: "而且能有效地用這些 tools 來完成任務，並以非常有趣的組合方式",
    76: "來完成更進階或更複雜的任務。",
    77: "Claude 強大的 tool use 能力，是 Claude Code 作為 coding assistant 的絕對核心優勢。",
    78: "原因是這樣的。",
    79: "首先，就像我剛才提到的，有了更好的 tool use，Claude 能處理更複雜的任務。",
    80: "其次，Claude Code 本身是可以擴充的。",
    81: "所以要在 Claude Code 裡加入新的 tools 非常容易，Claude 也很樂意使用這些 tools。",
    82: "這在持續保持相關性方面特別重要，因為我們看到開發領域的變化非常快速。",
    83: "換句話說，Claude Code 是一個會在未來幾年跟著你一起進化的 assistant。",
    84: "最後，有了更好的 tool use，你通常會獲得更好的安全性，因為 Claude 能有效地搜尋",
    85: "你的程式碼庫來找到相關的程式碼，而不需要依賴索引——索引通常需要把你",
    86: "整個程式碼庫傳送到外部伺服器。",
    87: "Claude Code 是一個值得深入了解的好工具。",
    88: "讓我們快速複習一下在這支影片裡學到的內容——關於 coding assistant 到底是什麼。",
    89: "記住，coding assistant 在內部使用 language model 來完成不同的任務。",
    90: "這些 language model 需要知道如何使用 tools，才能處理被交付的絕大多數任務。",
    91: "Tools 被用來讀取檔案、寫入檔案、執行指令，以及基本上所有不只是",
    92: "生成文字的操作。",
    93: "並不是所有的 language model 都在同一個水準上使用 tools，這對 coding assistant 整體的效率有很大的影響。",
}

CLAUDE_CODE_IN_ACTION_ZH = {
    1: "就在剛才，我做了一些相當大膽的聲明，說 Claude 是使用工具的專家，",
    2: "而且 Claude Code 非常容易擴展。",
    3: "當然，你可能會有一點懷疑。",
    4: "所以我想給你幾個快速的示範，這張表上列出的是",
    5: "Claude Code 裡預設可用的工具。",
    6: "它具備你所期待的所有功能，像是讀取檔案、寫入檔案、",
    7: "執行指令，等等這些。",
    8: "我要展示幾個用 Claude Code 完成的任務。",
    9: "在每個案例中，它都會以相當聰明的方式使用這套工具。",
    10: "而且在至少一個任務裡，我還會給 Claude 一套額外的新工具來使用。",
    11: "這個過程不只能讓你了解 Claude Code 開箱即用能做什麼，",
    12: "希望你也能看到要擴展 Claude Code 的功能有多容易。",
    13: "這是我給 Claude Code 的第一個任務。",
    14: "我要請它找出並優化 chalk 這個函式庫裡的效能問題。",
    15: "如果你不熟悉的話，chalk 是一個 JavaScript 套件。",
    16: "這是它的文件說明。",
    17: "這是一個非常小的函式庫，只有一個非常簡單的用途。",
    18: "它做的事就是用漂亮的顏色格式印出文字。",
    19: "就像你在這張範例截圖裡看到的這樣。",
    20: "你可以給文字加上顏色、背景和各種格式，諸如此類的東西。",
    21: "這聽起來可能是個很簡單又無聊的套件，但重點來了。",
    22: "原來這實際上是整個 JavaScript 生態系中下載量第五名的套件。",
    23: "光是上週，它就有 4 億 2900 萬次下載。",
    24: "簡單來說，這個套件被廣泛使用。",
    25: "如果我能找到任何方式來優化這個套件裡的東西，那應該是值得的。",
    26: "所以我要請 Claude 跑 benchmark、找出效能最差的案例，",
    27: "用一些 profiling 工具找出那些案例跑得這麼慢的原因，然後修復它們。",
    28: "接著我們會看到 Claude 將使用各種不同的工具，聰明地解決這個問題。",
    29: "它會建立一個待辦清單來追蹤進度、執行指令來跑 benchmark、",
    30: "寫入一個檔案來更仔細地聚焦在某個特定案例上，",
    31: "用 CPU profiler 來了解那個案例跑得這麼慢的原因，",
    32: "然後實作一些改善。",
    33: "最後，我們會在這個函式庫的某個特定操作上，得到 3.9 倍的吞吐量提升。",
    34: "這是另一個展示 Claude 如何串連不同 tool call 來完成複雜任務的好例子。",
    35: "我要給它一個 CSV 檔案裡的資料集。",
    36: "這裡面的所有資料包含一個影片串流平台上不同用戶的資訊，",
    37: "我要請它做一個通用的分析，",
    38: "也許找出平台上用戶流失的一些原因。",
    39: "而且我希望所有分析都在 Jupyter notebook 裡完成。",
    40: "這是我的資料集。",
    41: "然後我要請 Claude 跑這個分析，看看它表現如何。",
    42: "這是一個很好的例子，說明為什麼有效的工具使用非常重要。",
    43: "你看，Claude 只是把程式碼寫進 notebook 裡是不夠的。",
    44: "Claude 還可以在不同的 cell 裡執行程式碼，並查看執行結果。",
    45: "這意味著 Claude 可以在 notebook 裡先初步查看資料，",
    46: "然後針對某些特定細節，自訂每一個後續的 cell。",
    47: "接下來，我想展示一個例子，我透過給 Claude Code 一套新工具來擴展它的能力。",
    48: "我建了一個小 app，它會根據在畫面左側輸入的描述來生成 UI 元件。",
    49: "生成的元件會顯示在右側。",
    50: "這個 app 可以很輕鬆地生成好看的元件，但左側的聊天介面和頂部的 header 看起來不太好看。",
    51: "所以我要用 Claude Code 來改善樣式。",
    52: "如果我只是請它修復聊天介面和 header 的樣式，它可能會做得不錯。",
    53: "但記住，我這裡的目標是要展示給 Claude Code 增加額外功能有多容易。",
    54: "所以除了這個樣式任務之外，我還要給 Claude Code 存取一套新工具，這套工具由一個叫做 Playwright MCP server 的東西提供，我稍後會詳細介紹。",
    55: "這些工具讓 Claude 可以直接開啟並控制瀏覽器。",
    56: "所以這個過程實際上看起來是這樣的。",
    57: "我要請 Claude 改善我的 app 樣式，並使用瀏覽器來完成。",
    58: "它會在畫面右側開啟一個瀏覽器，然後導航到我的 app。",
    59: "它會截圖來查看目前的樣式，然後更新樣式。",
    60: "我們會看到 Claude 使用各種不同的工具來聰明地處理這個問題。我們甚至可以請 Claude 在完成時再截一張截圖，然後多次疊代設計，真正做出一個很吸睛的設計。",
    61: "沒多久，我們就得到了一個看起來相當不錯的結果。",
    62: "我還有最後一組示範想給你看。",
    63: "記得我剛才提到的。",
    64: "Claude 如此善用工具的能力，將讓 Claude Code 能夠在未來跟著你和你的團隊一起成長。",
    65: "讓我馬上給你看一個例子。",
    66: "Claude Code 與 GitHub 有非常緊密的整合。",
    67: "你可以設定 Claude Code 在 GitHub Action 裡運行，它會根據特定事件自動執行，比如建立 pull request，或是在 issue 裡被直接 @ 到。",
    68: "Claude Code 在 GitHub 上運行時，不只能查看和執行你的程式碼，還能存取一套與 GitHub 互動的新工具，像是建立留言、建立 commit 或 pull request 等等。",
    69: "你可以利用這個整合來自動審查 pull request。",
    70: "讓我給你看一個例子。",
    71: "先讓我為你設定一個小情境。",
    72: "假設我們正在 AWS 上建置一些基礎設施，所有的基礎設施都定義在一組 Terraform 檔案裡，這些檔案被 commit 並儲存在 GitHub 上。",
    73: "因為我們所有的基礎設施都定義在 Terraform 檔案裡，Claude Code 對資訊如何在我們的基礎設施中流動有很好的了解。",
    74: "現在，假設在這個架構裡，我有一個 DynamoDB 資料表。",
    75: "如果你不熟悉的話，它有點像是一般的資料庫表格。",
    76: "裡面我儲存了一些關於用戶的不同資訊，包括也許看過的方案和註冊日期。",
    77: "也許因為某些原因，我們想要把只有看過的方案和註冊日期這些資訊，分享給一個內部行銷團隊，但也要分享給一個外部行銷團隊。",
    78: "所以另一家公司可以存取我們寫入這個 bucket 的資料。",
    79: "所以對我們來說，隨時掌握哪些資訊隨時間被寫入那個 bucket 是非常重要的。",
    80: "每晚，我們可能有一個 Lambda function，把所有加入那張資料表的不同用戶拉出來，",
    81: "然後只提取看過的方案和註冊日期，並儲存到 S3 bucket 裡。",
    82: "這樣這兩個行銷團隊就可以存取那些資訊。",
    83: "現在，假設幾個月後，內部行銷團隊要求我們也把 email 儲存到這個 S3 bucket 裡。",
    84: "所以我們可能會去到 Lambda function，加入一行程式碼，取得用戶的 email 並儲存到 bucket 裡。",
    85: "因為這是幾個月後的事，我們可能已經完全忘記這個 S3 bucket 是和一個外部行銷合作夥伴共享的。",
    86: "所以現在到了這個時間點，我們正在把個人識別資訊放進這個 bucket，而這個 bucket 是另一家公司可以存取的。",
    87: "這是大忌，絕對是我們不想做的事。",
    88: "但同時，這種錯誤確實會發生。",
    89: "而且如果我們對這個 S3 bucket 的情況沒有很清楚的了解，是很難察覺的。",
    90: "結果發現 Claude Code 可以很輕鬆地在 pull request 裡抓到這種情境，",
    91: "特別是因為我們所有的基礎設施都定義在那些 Terraform 檔案裡。",
    92: "所以這裡有個快速的例子。",
    93: "我建了那個我剛剛在圖表裡展示給你看的專案。",
    94: "我建立了一個 pull request，在 Lambda function 裡加入用戶的 email。",
    95: "所以我改動的唯一一行程式碼就是那行。",
    96: "我說對於每一個用戶，我想要取得他們的 email，並把它加入 bucket 裡。",
    97: "現在，Claude Code 對我的基礎設施有很好的了解。",
    98: "所以它能夠在一個自動化審查裡，就像我們現在看到的，查看我在這個 pull request 裡做的所有改動。",
    99: "它能夠準確地搞清楚我的基礎設施是怎麼運作的。",
    100: "而且它能夠識別出我正在把一些個人識別資訊暴露給一個合作夥伴。",
    101: "所以它在這裡列出了資料流，也就是發生的確切步驟，",
    102: "並詳細說明這個 bucket 是如何與外部合作夥伴共享的。",
    103: "在開發過程中而不是部署變更後才抓到這類問題，是使用 Claude Code 在 GitHub 上整合的一個驚人優勢。",
    104: "我稍後會詳細說明，向你展示如何設定一個完全像這樣的流程。",
    105: "我想我們現在已經對 Claude Code 能做什麼有了很好的了解，這要感謝它出色的工具使用能力。",
    106: "記住，你真的應該把 Claude Code 想成一個靈活的助手，它可以被客製化、成長，並隨著時間改變，以滿足你的團隊需求。",
}

# ============================================================
# SRT file config: (filename, zh-TW translations, zh-CN translations, max_valid_entry)
# ============================================================

SRT_CONFIG = [
    ("Introduction_rLVnV1aS.srt", INTRODUCTION_ZH, INTRODUCTION_ZH_CN, 9),
    ("What_is_a_coding_assistant_WQnSCLF3.srt", WHAT_IS_CODING_ASSISTANT_ZH, WHAT_IS_CODING_ASSISTANT_ZH_CN, 93),
    ("Claude_Code_in_action_3IQrknws.srt", CLAUDE_CODE_IN_ACTION_ZH, CLAUDE_CODE_IN_ACTION_ZH_CN, 106),
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
