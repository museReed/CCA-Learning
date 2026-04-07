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
    ADDING_CONTEXT_ZH_CN,
    MAKING_CHANGES_ZH_CN,
)

BASE_DIR = Path("/Volumes/Muse_AI_Core/CCA-Learning/courses/claude-code-in-action/02-getting-started")

# Unit directory mapping: (srt_filename, unit_dir)
UNIT_MAP = {
    "Adding_context_wWHe1PIF.srt": "07-adding-context",
    "Making_changes_v2XzmjpP.srt": "08-making-changes",
}

# ============================================================
# Translations (zh-TW)
# ============================================================

ADDING_CONTEXT_ZH = {
    1: "我在那個小專案裡打開了程式碼編輯器。",
    2: "我要用 npm run dev 啟動開發伺服器。",
    3: "執行之後，我就可以在瀏覽器裡導航到 localhost 3000，",
    4: "看到應用程式正在運行。",
    5: "就是這裡。",
    6: "我們要用 Claude Code 在這個專案上做一些工作。",
    7: "但首先，有一件非常重要的事我希望你能了解，關於使用 Claude Code 的部分。",
    8: "具體來說，我希望你學完這門課程後，能對 context 管理有深刻的理解。",
    9: "你看，在一個典型的專案裡，可能有幾十甚至幾百個檔案。",
    10: "每個檔案都有大量的資訊。",
    11: "每當我們問 Claude Code 一個問題或交給它一個任務，Claude 需要某個理想數量的資訊。",
    12: "剛好夠它理解如何回答你的問題或完成你的任務。",
    13: "一旦我們開始加入不相關的額外資訊，Claude Code 的效率就會開始下降。",
    14: "所以引導 Claude 找到專案裡相關的檔案或文件，對我們來說非常重要。",
    15: "Claude Code 確實可以在沒有任何引導的情況下工作，但如果你給它一點點方向，",
    16: "你會得到最好的結果。",
    17: "所以在這支影片的剩餘時間裡，我會給你一堆不同的技巧，教你如何給 Claude 最好的 context。",
    18: "首先，在我的編輯器裡，我開啟了終端機，然後執行 claude 指令來啟動 Claude Code。",
    19: "每次你在一個專案裡第一次執行 Claude Code，我強烈建議執行 /init 指令。",
    20: "這讓 Claude 對你的整個程式碼庫進行深入分析。",
    21: "它會找出專案的目的、整體架構、相關指令、重要檔案等等。",
    22: "搜尋完成後，它會把發現的內容整理後放進一個叫做 CLAUDE.md 的檔案。",
    23: "當 Claude 嘗試建立這個檔案時，它會請求許可。",
    24: "你可以按 Enter 接受，或者如果你不想對每個檔案寫入請求都要授權，",
    25: "你也可以按 Shift-Tab，這樣 Claude Code 就可以自由地在你的專案裡寫入檔案。",
    26: "我建議你開啟生成的 CLAUDE.md 檔案，看看它的內容。",
    27: "如我所說，這個檔案的內容會被包含在我們每次傳給 Claude 的請求裡。",
    28: "這個檔案有兩個不同的目的。",
    29: "第一，它幫助 Claude 更好地了解你的程式碼庫，讓它能更快找到相關程式碼。",
    30: "第二，它是一個你可以給 Claude 一些通用指導的地方。",
    31: "讓你知道，Claude Code 會使用多個 CLAUDE.md 檔案。",
    32: "有專案層級、本地層級，以及機器層級。",
    33: "專案層級就是我們剛才執行 /init 指令生成的那個。",
    34: "我們通常會把這個檔案提交到版本控制，像是 Git。",
    35: "我們會把這個檔案分享給其他工程師，它會包含一些我們想傳達給 Claude 的專案特定指示。",
    36: "選擇性地，我們也可以建立一個 CLAUDE.local.md 檔案。",
    37: "這個檔案不會被提交，你通常也不會與其他工程師分享。",
    38: "在這個檔案裡，你可能會放一些只希望 Claude 為你個人遵守的指示。",
    39: "最後，你可以在你的電腦上有一個全域的 CLAUDE.md 檔案。",
    40: "這個檔案會包含要應用於你在本地執行的所有專案的指示。",
    41: "現在，我一直提到給 Claude 特殊或自訂指示，讓我給你看一個例子。",
    42: "假設 Claude 在它寫的程式碼裡用了太多注解。",
    43: "我們可以透過更新 CLAUDE.md 檔案來解決這個問題。",
    44: "我們可以手動修改檔案，或者有個小捷徑是在 Claude Code 裡輸入井字號 #。",
    45: "這讓我們進入 memory 模式。",
    46: "這讓我們可以智慧地編輯我們的某個 CLAUDE.md 檔案。",
    47: "所以我們可以輸入一個請求，像是「不要太常寫注解」。",
    48: "然後我會指定要把這個指示加入到專案的 CLAUDE.md 檔案，",
    49: "Claude 就會智慧地把這個指示合併進那個檔案。",
    50: "如果我打開那個檔案並搜尋，我就會看到它確實加入了那個新指示。",
    51: "現在我們已經建立了 CLAUDE.md 檔案，我想讓你更了解如何在對話中引入特定的 context。",
    52: "假設我們想更了解這個專案中認證系統是如何運作的。",
    53: "我們可以直接問 Claude 來告訴我們，這樣它就會搜尋我們的程式碼庫，找到與認證系統相關的檔案。",
    54: "那樣做確實有效，但就是需要一些時間。",
    55: "或者，如果我們已經知道一些與認證系統相關的檔案，我們可以用 @ 符號來提及它們。",
    56: "當我們提及一個檔案，它就會自動被包含在我們傳給 Claude 的請求裡。",
    57: "這是一個把 Claude 指向特定方向的絕佳技巧。",
    58: "你可以在 CLAUDE.md 裡用相同的語法來提及檔案。",
    59: "讓我給你展示一個例子，說明為什麼這非常有用。",
    60: "在這個專案的 Prisma 資料夾裡，有一個叫做 schema.prisma 的檔案。",
    61: "這個檔案包含了這個專案中使用的 SQLite 資料庫裡所有不同資料表和記錄類型的完整定義，用來儲存資訊。",
    62: "因為這個資訊對這個專案的許多方面來說非常重要且相關，我可能會決定在 CLAUDE.md 檔案裡提及這個檔案。",
    63: "讓我示範我會怎麼做。",
    64: "首先，我輸入 # 進入 memory 模式。",
    65: "然後我會提及那個 schema 檔案，並且特別告訴 Claude 在任何需要更了解資料庫內部資料結構時，都要參考那個檔案。",
    66: "更新完成後，我要看一下 CLAUDE.md 檔案，確認那個備注已經被加進去了。",
    67: "當你像這樣提及一個檔案，它的內容就會自動被包含在你的請求裡。",
    68: "所以如果我問使用者有哪些屬性，Claude 就能立即回答，不需要再讀取 schema 檔案。",
}

MAKING_CHANGES_ZH = {
    1: "讓我們試著對這個專案做幾個改動。",
    2: "過程中，我會向你展示一些 Claude Code 的實用功能。",
    3: "我首先想做的是把這個左手邊的佔位文字",
    4: "往下移到這個面板的中央，為了讓 Claude 準確理解我想移動什麼內容，",
    5: "我要截圖那個區域，",
    6: "然後用 Ctrl+V 貼到 Claude Code 裡——注意是 Ctrl+V，",
    7: "而不是你在 macOS 上可能習慣用的 Command+V，",
    8: "Ctrl+V 是專門用來貼上截圖的。",
    9: "Ctrl+V 是專門用來貼上截圖的。",
    10: "然後我可以請 Claude 把那個佔位元素置中。",
    11: "稍微搜尋了一下，Claude 就能做出樣式更新，回到瀏覽器裡，",
    12: "看起來很棒。",
    13: "看起來很棒。",
    14: "讓我向你展示我想在這個 app 裡改動的下一件事。",
    15: "我要請它做一個顯示標題和描述的卡片元件。",
    16: "卡片生成沒有問題，但聊天介面左側有一個奇怪的地方。",
    17: "左側聊天介面有個奇怪的東西。",
    18: "就是「string replace editor」。",
    19: "那個小面板是為了向用戶表示正在建立一個檔案，但",
    20: "現在它用了一個非常技術性的術語「string replace editor」來描述背後使用的工具。",
    21: "在幕後使用的工具。",
    22: "我想在這裡顯示對用戶更友善的文字，只告訴用戶一個檔案",
    23: "正在被建立，以及那個檔案的名稱。",
    24: "當然我們也應該處理聊天機器人可能在編輯或刪除",
    25: "檔案以及其他情況的案例。",
    26: "為了引導 Claude 的注意力，",
    27: "我再次截圖，",
    28: "這樣它就能準確理解我在說什麼。",
    29: "然後回到這裡，我把那張截圖貼進來，請 Claude 把那段特定的",
    30: "文字替換成更友善的訊息。",
    31: "這是一個稍微棘手的任務，需要 Claude 在這個專案裡做相當多",
    32: "的研究才能完成。",
    33: "每當你給 Claude 一個較難的任務時，有兩種方式可以輕鬆提升 Claude 的",
    34: "智能。",
    35: "第一種方式是啟用 planning mode。按兩下 Shift+Tab 或",
    36: "如果你已經是自動接受檔案編輯的話，按一下就好。",
    37: "在 planning mode 下，Claude 會對你專案的內容做更多研究，",
    38: "讀取更多檔案，並想出一個詳細的計畫",
    39: "來完成你的任務。",
    40: "完成計畫後，Claude 會告訴你它想做什麼來完成你的",
    41: "任務。",
    42: "到那時，你可以接受這個計畫，Claude 就會實作它，或者你可以",
    43: "以某種方式調整 Claude 的方向。",
    44: "也許它漏了某個檔案或沒有考慮到某個情境。",
    45: "第二種提升 Claude 智能的方式是啟用 thinking。",
    46: "這會開啟 Claude 的 extended thinking 功能，讓它能對特定",
    47: "任務做更深入的推理。",
    48: "要啟用 thinking，有幾個不同的觸發詞。",
    49: "每個觸發詞給 Claude 越來越大的 token 預算來思考。",
    50: "考慮到這是個比較棘手的任務，我可能會請 Claude ultrathink 一下，找出最好的",
    51: "實作方式。",
    52: "最後要了解的是，planning 和 thinking 可以同時使用。",
    53: "所以除了這個 ultrathink 之外，我也要同時開啟 planning mode。",
    54: "現在我要執行這個，看看 Claude 能多好地實作這個功能。",
    55: "你可能想知道什麼時候應該用 planning，什麼時候應該用 thinking。",
    56: "把這兩個分別看成處理廣度和深度。",
    57: "Planning mode 在任務需要對你的程式碼庫有廣泛理解，",
    58: "需要查看不同區域時很有用。",
    59: "它在處理需要幾個步驟才能完成的任務時也很有用。",
    60: "另一方面，thinking 在你聚焦於某個特別棘手的邏輯，",
    61: "或是在排查一個困難的 bug 時很有用。",
    62: "你可能有的第二個問題是，你是否應該一直開啟 thinking 和 planning。",
    63: "好吧，你當然可以。",
    64: "只需記住，planning 和 thinking 會消耗額外的 tokens。",
    65: "所以使用它們是有成本的。",
    66: "所以使用它們是有成本的。",
    67: "工作幾分鐘後，看起來這個功能已經完成了。",
    68: "所以我要回到我的編輯器測試一下。",
    69: "我們可以立刻看到，我們獲得了比之前更好的狀態資訊。",
    70: "之前的狀態。",
    71: "現在用戶被告知正在建立一個檔案。",
    72: "如果我送出一個後續請求，也許是要改標題，希望這次後續請求中，",
    73: "我們會看到關於編輯那個檔案的資訊。",
    74: "就是這樣。",
    75: "我們正在編輯 app.jsx 檔案。",
    76: "我想說 Claude 確實成功地實作了這個功能。",
    77: "現在我們已經對這個專案做了一些改動，我們應該提交我們的變更。",
    78: "Claude Code 是一個很棒的 Git 助手。",
    79: "我們可以請它 stage 並提交我們的變更，它會為我們撰寫一個具描述性的 commit 訊息。",
    80: "為我們撰寫。",
}

# ============================================================
# SRT file config: (filename, zh-TW translations, zh-CN translations, max_valid_entry)
# ============================================================

SRT_CONFIG = [
    ("Adding_context_wWHe1PIF.srt", ADDING_CONTEXT_ZH, ADDING_CONTEXT_ZH_CN, 68),
    ("Making_changes_v2XzmjpP.srt", MAKING_CHANGES_ZH, MAKING_CHANGES_ZH_CN, 80),
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
