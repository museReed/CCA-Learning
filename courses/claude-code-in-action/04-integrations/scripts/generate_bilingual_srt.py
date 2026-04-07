#!/usr/bin/env python3
"""Generate bilingual SRT files (EN + ZH) from original English SRT files.

Produces two output variants per video:
  - *_bilingual_zh_tw.srt  (English + Traditional Chinese)
  - *_bilingual_zh_cn.srt  (English + Simplified Chinese)

Hallucination entries beyond max_valid_entry are silently dropped.
"""

import re
from pathlib import Path

from zh_cn_translations import MCP_SERVERS_ZH_CN, GITHUB_INTEGRATION_ZH_CN

BASE_DIR = Path(
    "/Volumes/Muse_AI_Core/CCA-Learning/courses/claude-code-in-action/04-integrations"
)

UNIT_MAP = {
    "MCP_servers_with_Claude_Code_EkzVe83z.srt": "12-mcp-servers-with-claude-code",
    "Github_integration_ZzNXo5m0.srt": "13-github-integration",
}

# ---------------------------------------------------------------------------
# zh-TW translation dictionaries
# ---------------------------------------------------------------------------

MCP_SERVERS_ZH = {
    1: "你可以透過使用 MCP server 為 Claude Code 新增工具和功能。",
    2: "這些 MCP server 可以遠端運行，也可以在你的本機上運行。",
    3: "一個非常受歡迎的 MCP server 叫做 Playwright，它賦予 Claude Code 控制瀏覽器的能力。",
    4: "讓我來示範如何將它加入 Claude Code，然後我們再用它進一步開發我們的應用程式。",
    5: "要安裝這個 server，請在你的終端機（不是在 Claude Code 內部）執行 claude mcp add，",
    6: "然後指定這個 MCP server 的名稱，我將它命名為 Playwright，",
    7: "在名稱之後，我們還需要加上一個指令，用來在你的本機上啟動這個 server。",
    8: "然後我們可以啟動 Claude Code，讓它開啟瀏覽器並導航到我們位於 localhost 3000 的應用程式。",
    9: "在瀏覽器開啟之前，你可能會注意到系統要求你授予該工具執行的權限。",
    10: "如果你厭倦了這些權限彈出視窗，可以打開 `.claude` 目錄，找到 `settings.local.json`，",
    11: "然後在 `allowed tools` 陣列中，新增一個以 `mcp__` 開頭的字串。",
    12: "注意這裡有兩個底線，後面接 Playwright。",
    13: "這樣 Claude Code 就可以任意使用這個 MCP server 及其中的所有工具，",
    14: "而不需要你每次都手動授予權限。",
    15: "如果我重新啟動 Claude Code，然後再次讓它開啟瀏覽器，",
    16: "它將直接執行，不再要求我授予權限。",
    17: "Playwright MCP server 有非常多種用途。",
    18: "讓我向你展示一個非常適合我們目前專案的應用場景。",
    19: "回到我的編輯器，我要找到 `src/lib/prompts/generation.tsx` 這個檔案。",
    20: "這是實際用於產生元件的提示詞檔案，也就是你在我們的應用程式中所請求的元件。",
    21: "所以我想讓 Claude Code 利用瀏覽器，自行產生一個元件，",
    22: "然後根據產生的元件，自行調整這個提示詞。",
    23: "我們希望最終能產生外觀更好的元件。",
    24: "讓我來示範如何做到這一點。",
    25: "回到 Claude Code，我要讓它導航到 localhost 3000，",
    26: "嘗試產生一個元件，查看產生的原始碼並評估樣式，",
    27: "然後更新我們在 `generation.tsx` 檔案中的提示詞。",
    28: "我們希望最終能得到樣式更好的產生元件。",
    29: "讓我們看看它的表現如何。",
    30: "Claude Code 首先會開啟瀏覽器。",
    31: "它會嘗試產生一個元件。",
    32: "從 Claude Code 的評論來看，它似乎不太滿意。",
    33: "你可能會注意到它抱怨了一種在這類應用程式中很常見的樣式，",
    34: "也就是紫色到藍色的漸層效果。",
    35: "Claude Code 接下來會更新我們的提示詞，然後嘗試產生一個新的元件。",
    36: "說實話，這個結果比我預期的要好得多。",
    37: "這張推薦卡片看起來真的非常出色。",
    38: "僅憑這些結果，你就能立刻感受到 MCP server 確實開啟了許多有趣的應用場景。",
    39: "我強烈建議你去研究一下，哪些 MCP server 可以幫助 Claude Code 開發你個人正在做的專案。",
    40: "說實話。",
}

GITHUB_INTEGRATION_ZH = {
    1: "Claude Code 有一個官方的 GitHub 整合功能，允許 Claude Code",
    2: "在 GitHub Actions 內部運行。",
    3: "你可以透過執行 `/install-github-app` 指令來設定這個整合。",
    4: "這將引導你完成幾個步驟。",
    5: "首先，你需要在 GitHub 上安裝 Claude Code 應用程式。",
    6: "接下來，你需要新增一個 API key。",
    7: "完成之後，系統會自動產生一個 pull request。",
    8: "這個 pull request 會新增兩個不同的 GitHub Actions。",
    9: "第一個 action 新增了提及支援。",
    10: "這樣你就可以在 issue 或 pull request 中，用 `@claude` 提及 Claude Code，",
    11: "並給它分配某種任務來執行。",
    12: "第二個 action 新增了審查 pull request 的支援。",
    13: "每當你建立一個 pull request 時，Claude Code 就會自動執行並審查",
    14: "提議的變更。",
    15: "這兩個 action 都可以自訂，你也可以新增額外的 action，",
    16: "以便根據其他類型的事件來觸發。",
    17: "讓我示範如何自訂提及功能。",
    18: "首先，我們剛剛把這兩個 action 設定檔案合併到了我們在 GitHub 上的儲存庫。",
    19: "所以我需要將這些變更拉取到我的本機。",
    20: "然後在新建的 GitHub workflows 目錄裡，我會看到這兩個 action 設定檔案。",
    21: "一個新增了對 pull request 審查的支援，另一個新增了對處理",
    22: "提及的支援。",
    23: "現在，這是我想要自訂提及功能的方式。",
    24: "每當我在 issue 或 pull request 中提及 Claude Code 時，我希望它能夠執行",
    25: "這個專案，並使用 Playwright MCP server 在 web 瀏覽器中存取應用程式，",
    26: "全部都在 GitHub Actions 內部完成。",
    27: "為了實現這個功能，我會在 Claude Code 執行之前，在這個 workflow 中先新增一個步驟。",
    28: "我將執行 setup 指令，然後啟動開發伺服器。",
    29: "然後我會更新 Claude Code 的設定。",
    30: "我會新增一些自訂指令。",
    31: "這些指令會直接傳遞給 Claude Code，允許我們提供一些額外的說明",
    32: "或情境資訊。",
    33: "在這個例子中，我會告訴 Claude Code 開發伺服器已經在執行，",
    34: "並且如果需要的話，我可以使用 Playwright MCP server 在瀏覽器中存取應用程式。",
    35: "然後我會新增一些設定來設置 Playwright MCP server 本身。",
    36: "這裡還有一件事需要注意。",
    37: "當你在 action 中執行 Claude Code 時，我們必須明確列出所有",
    38: "我們想要授予 Claude Code 的權限。",
    39: "這裡有一個棘手的地方。",
    40: "如果你使用了 MCP server，你必須逐一列出每個 MCP server 中",
    41: "你想要允許的每個工具。",
    42: "不像之前那樣有權限的快捷方式。",
    43: "遺憾的是，Playwright MCP server 有很多不同的工具，所以它們都需要",
    44: "逐一列出。",
    45: "完成這個設定更新後，我會確保提交這些變更",
    46: "並推送它們。",
    47: "現在是時候測試這個更新後的 workflow 了。",
    48: "我要給 Claude Code 一個小任務。",
    49: "在我們的實際應用程式中，看到上面這兩個按鈕了嗎？",
    50: "目前它們運作正常。",
    51: "我可以在預覽面板和程式碼面板之間切換，沒有任何問題。",
    52: "但我要假裝它們沒有按預期運作。",
    53: "我要用那裡的按鈕截一張圖。",
    54: "然後我要建立一個 issue。",
    55: "我要貼上截圖，然後用 `@claude` 提及 Claude Code，並讓",
    56: "它驗證這兩個按鈕是否按預期運作。",
    57: "然後我會建立這個 issue 並等待。",
    58: "action 實際啟動可能需要一兩分鐘，然後 Claude Code",
    59: "才會回應。",
    60: "記住，正如我們剛才在 action 中看到的，我們現在需要先設定整個應用程式並啟動",
    61: "它執行，然後 Claude Code 才會開始執行。",
    62: "但最終，Claude Code 會回應。",
    63: "它通常會建立一個步驟清單來完成給定的任務。",
    64: "在這個例子中，它將嘗試造訪應用程式、手動測試按鈕，並",
    65: "修復發現的任何問題。",
    66: "Claude Code 會發現這兩個按鈕實際上運作得很好，所以它會",
    67: "提早結束並給出一條記錄其發現結果的訊息。",
    68: "這只是一個小例子，展示了你如何使用 Claude Code 的 GitHub 整合功能。",
    69: "我建議你花些時間思考，如何為你自己的特定專案量身打造它。",
}

# ---------------------------------------------------------------------------
# SRT configuration: (filename, zh_tw_dict, zh_cn_dict, max_valid_entry)
# Entries beyond max_valid_entry are Whisper hallucinations and are dropped.
# ---------------------------------------------------------------------------
SRT_CONFIG = [
    (
        "MCP_servers_with_Claude_Code_EkzVe83z.srt",
        MCP_SERVERS_ZH,
        MCP_SERVERS_ZH_CN,
        40,  # entries 41-61 are zero-duration or repeated hallucinations
    ),
    (
        "Github_integration_ZzNXo5m0.srt",
        GITHUB_INTEGRATION_ZH,
        GITHUB_INTEGRATION_ZH_CN,
        69,  # entries 70-87 are repeated hallucinations
    ),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_srt(path: Path, max_valid_entry: int) -> list[dict]:
    """Parse an SRT file and return a list of entry dicts.

    Each dict has keys: index (int), timecode (str), text (str).
    Entries with index > max_valid_entry are dropped.
    Entries whose text is empty after stripping are also dropped.
    """
    content = path.read_text(encoding="utf-8")
    # Split on blank lines between entries
    raw_blocks = re.split(r"\n\s*\n", content.strip())
    entries = []
    for block in raw_blocks:
        lines = block.strip().splitlines()
        if len(lines) < 2:
            continue
        try:
            index = int(lines[0].strip())
        except ValueError:
            continue
        if index > max_valid_entry:
            continue
        timecode = lines[1].strip()
        text = " ".join(line.strip() for line in lines[2:]).strip()
        if not text:
            continue
        entries.append({"index": index, "timecode": timecode, "text": text})
    return entries


def generate_bilingual_srt(
    entries: list[dict],
    zh_dict: dict[int, str],
    output_path: Path,
) -> None:
    """Write a bilingual SRT file.

    Each subtitle block contains:
      Line 1: English original
      Line 2: Chinese translation (zh-TW or zh-CN depending on zh_dict)

    If a translation is missing for a given index, the Chinese line is omitted.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for entry in entries:
        idx = entry["index"]
        en_text = entry["text"]
        zh_text = zh_dict.get(idx, "")
        lines.append(str(idx))
        lines.append(entry["timecode"])
        lines.append(en_text)
        if zh_text:
            lines.append(zh_text)
        lines.append("")  # blank line separator
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Written: {output_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("Generating bilingual SRT files for chapter 04-integrations...\n")

    for srt_filename, zh_tw_dict, zh_cn_dict, max_valid in SRT_CONFIG:
        unit_dir = UNIT_MAP[srt_filename]
        srt_path = BASE_DIR / unit_dir / "srt" / srt_filename
        bilingual_dir = BASE_DIR / unit_dir / "srt"

        print(f"Processing: {srt_filename}  (max_valid_entry={max_valid})")

        if not srt_path.exists():
            print(f"  ERROR: Source file not found: {srt_path}")
            continue

        entries = parse_srt(srt_path, max_valid)
        print(f"  Parsed {len(entries)} valid entries")

        # Derive output stem from the original filename (strip .srt)
        stem = srt_path.stem

        # zh-TW bilingual
        tw_output = bilingual_dir / f"{stem}_bilingual_zh_tw.srt"
        generate_bilingual_srt(entries, zh_tw_dict, tw_output)

        # zh-CN bilingual
        cn_output = bilingual_dir / f"{stem}_bilingual_zh_cn.srt"
        generate_bilingual_srt(entries, zh_cn_dict, cn_output)

        print()

    print("Done.")


if __name__ == "__main__":
    main()
