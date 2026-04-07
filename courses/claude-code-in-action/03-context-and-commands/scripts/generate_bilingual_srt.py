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
    CONTROLLING_CONTEXT_ZH_CN,
    CUSTOM_COMMANDS_ZH_CN,
)

BASE_DIR = Path("/Volumes/Muse_AI_Core/CCA-Learning/courses/claude-code-in-action/03-context-and-commands")

# Unit directory mapping: (srt_filename, unit_dir)
UNIT_MAP = {
    "Controlling_context_pIw5RYqx.srt": "10-controlling-context",
    "Custom_commands_ChNLn8eT.srt": "11-custom-commands",
}

# ============================================================
# Translations (zh-TW)
# ============================================================

CONTROLLING_CONTEXT_ZH = {
    1: "在這支影片中，我想向你展示幾種不同的技術，用來控制和",
    2: "引導對話的流向。",
    3: "先來看一個基本範例。",
    4: "我要請 Claude 為一個認證檔案裡的函式撰寫測試，",
    5: "這些函式就寫在那個檔案裡。",
    6: "Claude 很快就提出了一個計畫，打算撰寫幾個不同的測試。",
    7: "不過，我知道測試這個檔案有點複雜，我希望 Claude 一次只",
    8: "測試一件事。",
    9: "要中斷 Claude，我可以按 escape。",
    10: "這會讓 Claude 立刻停下來，讓我能夠建議一個不同的方向。",
    11: "把 escape 和 memories 搭配使用，是修正 Claude 反覆犯錯的一個",
    12: "非常強大的方式。",
    13: "來看個範例。",
    14: "我要再次請 Claude 為同一個檔案撰寫測試。",
    15: "這次，它會嘗試讀取一個其實並不存在的測試設定檔，",
    16: "但那個檔案根本不存在。",
    17: "這是一個我在這個專案中已經看過 Claude 犯過的錯誤。",
    18: "所以為了避免這個錯誤再次發生，我會非常快速地按下 escape。",
    19: "接著我會用 # 快捷鍵加入一條關於這個測試設定檔正確名稱的 memory，",
    20: "就是關於那個測試設定檔的正確名稱。",
    21: "現在我應該不會再看到這個錯誤了。",
    22: "這些對話控制快捷鍵有些看起來只是為了方便，但",
    23: "用得好的話，真的能大幅提升 Claude 有效工作、保持專注的能力。",
    24: "讓我給你看一個更實際的範例。",
    25: "在 auth.ts 檔案裡有四個不同的函式，我想讓 Claude 逐一",
    26: "為每個函式撰寫測試。",
    27: "從一個叫做 create session 的函式開始。",
    28: "Claude 當然會嘗試撰寫測試，但在執行的過程中，它遇到了",
    29: "一個錯誤，並花了一些時間除錯。",
    30: "原來是我忘記安裝一個套件了。",
    31: "最終測試完成並通過，是時候開始處理下一",
    32: "組測試了。",
    33: "但問題是，",
    34: "在我的對話歷史中，已經累積了大量圍繞那個有問題套件的來回討論。",
    35: "這些都是與撰寫下一組測試完全不相關的 context。",
    36: "完全無關的 context。",
    37: "理想上，我們能夠跳回過去，回到我們之前發送的訊息，",
    38: "直接把它改成「為 get session 撰寫測試」。",
    39: "這樣做的好處是，我們保留了 Claude 已經讀過 auth.ts 檔案內容的 context，",
    40: "它也已經知道我們說的 get session 是什麼。",
    41: "而且因為我們去掉了那些只是關於除錯的多餘訊息，",
    42: "不會有那麼多干擾了。",
    43: "不會有那麼多干擾。",
    44: "這樣 Claude 就能真正保持專注。",
    45: "要回到對話歷史，按兩下 escape。",
    46: "這會顯示你所有發送過的訊息。",
    47: "你可以倒退回過去某個時間點，跳過一些中間的對話。",
    48: "Claude 現在開始處理下一組測試了。",
    49: "這次 Claude 保持非常專注，但不幸的是遇到了一些問題。",
    50: "最終它解決了這些問題，讓測試通過。",
    51: "現在，Claude 已經獨立工作了幾分鐘，對如何為這個檔案撰寫測試",
    52: "有了非常好的掌握。",
    53: "但同時，我們的對話歷史中又累積了大量 context。",
    54: "當需要為下一個函式撰寫測試時，我要使用一個叫做",
    55: "/compact 的指令。",
    56: "/compact 指令會彙整目前對話中的所有訊息並加以摘要。",
    57: "/compact 非常適合用在 Claude 已經充分了解目前任務、而你想要",
    58: "在進入下一個任務時保留這些知識的情況。",
    59: "最後一個需要知道的 context 相關指令是 /clear 指令。",
    60: "/clear 會清除整個對話歷史，讓你從頭開始。",
    61: "/clear 最適合用在你即將開始一個完全不同的、",
    62: "與目前任務無關的任務時。",
    63: "我建議多多使用這些快捷鍵，特別是當你在不同任務之間切換，",
    64: "或是與 Claude 進行長時間對話的時候。",
    65: "在這門課程的後續部分，我們會多次使用它們，確保 Claude 保持",
    66: "專注在任務上。",
}

CUSTOM_COMMANDS_ZH = {
    1: "當你執行 Claude Code 時，你可以輸入斜線，然後看到一堆 Claude Code 預設內建的指令。",
    2: "除了這些預設指令之外，你也可以輕鬆地加入自己的 custom commands。",
    3: "Custom commands 適合用來自動化你經常重複執行的任務。",
    4: "讓我示範如何建立一個。",
    5: "在我的專案目錄裡，我要找到 .claude 資料夾。",
    6: "在那個資料夾裡，我會建立一個叫做 commands 的新目錄。",
    7: "然後在裡面，我會建立一個叫做 audit.md 的新檔案。",
    8: "我們建立的這個檔案的名稱——在這個例子中是 audit——就會是我們最終執行的指令名稱。",
    9: "這個指令的目標是稽核這個專案中所有已安裝的相依套件，",
    10: "如果有任何安全漏洞就更新它們，然後執行測試確保沒有東西壞掉。",
    11: "建立好指令檔案之後，你要重新啟動 Claude Code。",
    12: "別忘了重新啟動它。",
    13: "重新開啟 Claude Code 時，輸入 /audit。",
    14: "這樣就會顯示你剛剛建立的指令。",
    15: "你可以執行它，在這個例子中，它會完全按照我們要求 Claude 做的事情來執行。",
    16: "它會執行指令、檢查是否有容易受攻擊的套件、必要時修復它們，然後執行測試。",
    17: "Custom commands 也可以接收參數。",
    18: "讓我給你看一個範例。",
    19: "我要再建立一個叫做 write tests 的指令。",
    20: "每次我執行這個指令時，我想為專案中某個特定檔案建立測試。",
    21: "在指令文字中，我會加入一個 $ARGUMENTS 的佔位符。",
    22: "每次我執行這個指令時，如果我傳入一個檔案路徑，那個路徑就會被插入到 $ARGUMENTS 的位置。",
    23: "所以現在我可以再次重新啟動 Claude Code，然後執行 write test 指令。",
    24: "現在要說清楚，我們傳入的參數不一定要是檔案路徑。",
    25: "它可以是任何我們想要傳入的字串。",
    26: "所以我可能隨意地要求為某個特定資料夾中的一個檔案撰寫測試，給 Claude 一點關於在哪裡找的方向提示。",
}

# ============================================================
# SRT file config: (filename, zh-TW translations, zh-CN translations, max_valid_entry)
# ============================================================

SRT_CONFIG = [
    ("Controlling_context_pIw5RYqx.srt", CONTROLLING_CONTEXT_ZH, CONTROLLING_CONTEXT_ZH_CN, 66),
    ("Custom_commands_ChNLn8eT.srt", CUSTOM_COMMANDS_ZH, CUSTOM_COMMANDS_ZH_CN, 26),
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
