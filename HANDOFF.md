# CCA-Learning Session Handoff

**Date**: 2026-04-27
**Last commit**: `0f80c22` — chore: add sync/delete to build_html.py, remove 49 stale files

---

## Project Overview

Skilljar 線上課程學習筆記庫，涵蓋 Anthropic 官方 7 門課程。包含學習筆記 (Markdown)、視覺指南 (SVG)、翻譯字幕 (JSON) 和建構腳本。

## Repository Structure

```
courses/
├── building-with-the-claude-api/       86 SVGs, 74 translations, 575 notes
├── claude-code-in-action/              91 SVGs,  0 translations, 338 notes
├── introduction-to-model-context-protocol/  10 SVGs, 11 translations,  87 notes
├── model-context-protocol-advanced-topics/  12 SVGs,  8 translations,  73 notes
├── claude-101/                         (outline only)
├── introduction-to-agent-skills/       (outline only)
├── introduction-to-subagents/          (outline only)
scripts/                                Translation & build utilities
```

---

## Completed Work (This Session + Prior Sessions)

### 1. Translation: zh_tw + zh_cn for 93 Files — DONE

All subtitle translation templates filled with Traditional Chinese (zh_tw), Simplified Chinese (zh_cn) auto-converted via `tw_to_cn()`.

| Course | Files | Entries | Status |
|--------|------:|--------:|--------|
| Introduction to MCP | 11 | 679 | 100% |
| MCP Advanced Topics | 8 | 774 | 100% |
| Building with Claude API | 74 | 5,257 | 100% |
| **Total** | **93** | **6,710** | **100%** |

Note: 6 entries in `The_web_search_tool` (96-101) have empty English source — nothing to translate.

**Translation scripts** (all in `scripts/`):
- `fill_translations.py` — Core utility: `fill_template_from_dict()` + `tw_to_cn()`
- `translate_intro_mcp.py` — 11 files, 679 entries
- `translate_mcp_advanced.py` — 8 files, 764 entries
- `translate_api_ch01.py` through `translate_api_ch09.py` — 74 files, 5,257 entries

### 2. Study Notes — Previously Complete

- **building-with-the-claude-api**: 575 .md files across 9 chapters (ch01-ch09)
- **claude-code-in-action**: 338 .md files across 6 chapters
- **introduction-to-model-context-protocol**: 87 .md files across 4 chapters
- **model-context-protocol-advanced-topics**: 73 .md files across 4 chapters

### 3. Visual Guides (SVG) — Previously Complete

- 199 total SVGs across 4 courses
- Includes zh-TW bilingual variants for some diagrams

---

## Uncommitted Changes

Large batch of uncommitted work (all untracked):

### Must commit:
- `courses/*/translations/` — All 93 translation JSON files (the work from recent sessions)
- `scripts/translate_*.py` — 11 translation scripts
- `scripts/fill_translations.py` — Core translation utility
- `scripts/bilingual_pipeline.py` — Bilingual subtitle/visual pipeline (not yet executed)

### Visual guides (untracked `visual-guides/` dirs):
- 17 `visual-guides/` directories across 4 courses — appear to be empty placeholder dirs

### Other untracked:
- `courses/*/00-outline.json` — Modified outlines (4 files)
- `scripts/check_upstream.py`, `scripts/probe_skilljar.py`, `scripts/save_session.py`, `scripts/verify_session.py` — Utility scripts
- `logs/`, `reports/` — Generated output directories
- `.obsidian/workspace.json` — Obsidian editor state

---

## Pending / Next Steps

### High Priority
1. **Commit translations** — Stage and commit all 93 translation JSONs + scripts
2. **Run bilingual pipeline** — `scripts/bilingual_pipeline.py` exists but has NOT been executed yet; it should generate bilingual subtitle files and/or visual guides from the translations

### Medium Priority
3. **claude-code-in-action translations** — 0/? translation files exist; this course has no translation templates yet
4. **Clean up empty visual-guides dirs** — 17 empty placeholder directories

### Low Priority
5. **Remaining 3 courses** (claude-101, introduction-to-agent-skills, introduction-to-subagents) — Only outlines exist, no content yet

---

## Key Technical Details

### Translation JSON Format
```json
{
  "srt_file": "...",
  "video_file": "...",
  "max_valid_entry": 56,
  "entries": {
    "1": { "en": "English text...", "zh_tw": "繁體中文...", "zh_cn": "简体中文..." }
  }
}
```

### tw_to_cn() Conversion
`fill_translations.py` contains character-level mapping + word-level tech term replacements:
- 程式碼→代码, 伺服器→服务器, 資料庫→数据库, 模組→模块, etc.

### Translation Script Pattern
Each `translate_api_chXX.py`:
1. Imports `fill_template_from_dict` from `fill_translations.py`
2. Defines dict `T` mapping `"chapter/filename"` → `{entry_num: "zh_tw_text"}`
3. Iterates and fills templates; zh_cn auto-generated

---

## Environment Notes
- Working directory: `/Volumes/Muse_AI_Core/CCA-Learning`
- Git branch: `main`
- Python 3 required for scripts
- Obsidian vault for viewing .md notes
