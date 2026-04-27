# CCA-Learning Session Handoff

**Date**: 2026-04-28
**Last commit**: `09cfed3` — fix(pipeline): improve bilingual subtitle overlay layout

---

## Project Overview

Skilljar 線上課程學習筆記庫，涵蓋 Anthropic 官方 7 門課程。包含學習筆記 (Markdown)、視覺指南 (SVG)、逐幀截圖、翻譯字幕 (JSON)、雙語 SRT 和建構腳本。

---

## Current Status — All Major Work Complete

### Content Inventory

| 項目 | 數量 |
|------|------|
| 課程 | 7 門（4 門完整，3 門大綱） |
| 已完成課堂 | 106 堂 |
| 學習筆記 | 636 份（106 課 × 6 版本） |
| SVG 圖表 | 187 個 |
| 翻譯 JSON | 108 個（4 課程全覆蓋） |
| 雙語 SRT | 216 個（108 × zh-TW/zh-CN） |
| 逐幀學習指南 | 7,658 幀 + 108 Markdown |
| HTML 頁面 | 637 頁 |
| 教學影片 | 108 支 |

### Translation Coverage

| Course | Files | Entries | Status |
|--------|------:|--------:|--------|
| Introduction to MCP | 11 | 679 | 100% |
| MCP Advanced Topics | 8 | 774 | 100% |
| Building with Claude API | 74 | 5,257 | 100% |
| Claude Code in Action | 15 | 949 | 100% |
| **Total** | **108** | **7,659** | **100%** |

---

## Completed Work (This Session)

1. **Bilingual SRT generation** — 216 雙語字幕檔（from translation JSONs via `bilingual_pipeline.py`）
2. **Visual guide generation** — 6,710 逐幀截圖（3 courses with chapter-level visual-guides）
3. **Subtitle overlay fix** — 修正中文字幕佈局（overlay 120→140px，中/英雙行正確顯示）
4. **Claude-code-in-action translation JSONs** — 從已有雙語 SRT 反向生成 15 個 JSON
5. **Cleanup (88 items):**
   - 7 個 study-notes-v2 重複目錄
   - 3 個重複 lesson 目錄（05-hooks 新舊版衝突）
   - 2 個重複 SRT 檔
   - 6 個 chapter-level scripts 目錄
   - 15 個 raw frame 目錄（948 原始幀）
   - 10 個空 source/images 目錄
   - 45 個空目錄
6. **README.md update** — 反映最新統計和資源
7. **INDEX.md** — 4 門主力課程各自的課堂導覽目錄

---

## Remaining Work (Low Priority)

1. **3 門輕量課程** — claude-101, introduction-to-agent-skills, introduction-to-subagents 只有大綱和 placeholder，無官方內容可供充實
2. **HTML rebuild** — `python3 scripts/build_html.py` 可能需要重跑以反映最新筆記
3. **Visual guides for claude-code-in-action** — 此課程的 visual-guide 已在之前 session 完成（lesson-level），格式與其他 3 門課不同（chapter-level visual-guides）

---

## Key Technical Details

### File Structure Patterns

| 課程 | 原始文字稿 | SRT 位置 | 雙語 SRT | 逐幀截圖 |
|------|-----------|---------|---------|---------|
| building-with-the-claude-api | `<chapter>/NN-slug.md` | `<chapter>/` (loose) | `<chapter>/srt/bilingual/` | `<chapter>/visual-guides/` |
| claude-code-in-action | `<chapter>/<lesson>/source/` | `<chapter>/<lesson>/srt/` | `<chapter>/<lesson>/srt/bilingual/` | `<chapter>/<lesson>/visual-guide/` |
| intro-mcp / mcp-advanced | `<chapter>/NN-slug/` | `<chapter>/` (loose) | `<chapter>/srt/bilingual/` | `<chapter>/visual-guides/` |

### Key Scripts

| Script | Purpose |
|--------|---------|
| `bilingual_pipeline.py` | scan/templates/bilingual/visual 管線 |
| `fill_translations.py` | 翻譯核心：`fill_template_from_dict()` + `tw_to_cn()` |
| `build_html.py` | Markdown → HTML 建置 |
| `translate_*.py` | 各課程翻譯腳本（13 支） |

---

## Environment

- Working directory: `/Volumes/Muse_AI_Core/CCA-Learning`
- Git branch: `main`
- Python 3 + Pillow + ffmpeg required for visual pipeline
