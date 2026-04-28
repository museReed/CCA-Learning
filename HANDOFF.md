# CCA-Learning Session Handoff

**Date**: 2026-04-28
**Last commit**: `3b362b9` — refactor: restructure 3 courses to lesson-self-contained layout

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

## File Structure — Unified Lesson-Self-Contained

All 4 courses now use the same **lesson-self-contained** layout:

```
courses/<course>/<chapter>/<lesson>/
├── source/                    ← 課程文字稿 + 截圖 + images/
├── study-notes/universal/     ← 6 個學習筆記（eng/pm × en/zh-TW/zh-CN）
├── visuals/                   ← SVG 圖表（EN + zh-TW）
├── srt/                       ← 英文 SRT
│   └── bilingual/             ← 雙語 SRT（EN+繁中 / EN+簡中）
├── videos/                    ← MP4 教學影片
└── visual-guide/              ← 逐幀雙語截圖指南
```

### Restructure Details (commit 3b362b9)

- Converted 3 courses from chapter-shared → lesson-self-contained:
  - building-with-the-claude-api (68 lessons, 9 chapters)
  - introduction-to-model-context-protocol (11 lessons, 4 chapters)
  - model-context-protocol-advanced-topics (8 lessons, 4 chapters)
- All 93 video lessons matched SRT/video/visual-guide successfully
- claude-code-in-action was already lesson-self-contained (no change needed)

---

## Completed Work (This Session)

1. **Bilingual SRT generation** — 216 雙語字幕檔
2. **Visual guide generation** — 6,710 逐幀截圖
3. **Subtitle overlay fix** — 中文字幕佈局修正
4. **Claude-code-in-action translation JSONs** — 15 個 JSON（從雙語 SRT 反向生成）
5. **Cleanup (88 items)** — 重複目錄/檔案/空目錄清理
6. **README.md + INDEX.md** — 更新反映統一結構
7. **Restructure** — 3 門課程統一為 lesson-self-contained 結構（593 files）

---

## Remaining Work (Low Priority)

1. **3 門輕量課程** — claude-101, introduction-to-agent-skills, introduction-to-subagents 只有大綱和 placeholder
2. **HTML rebuild** — `python3 scripts/build_html.py` 需重跑以反映新目錄結構
3. **Git push** — 本地 commits 尚未推送至 remote

---

## Key Scripts

| Script | Purpose |
|--------|---------|
| `bilingual_pipeline.py` | scan/templates/bilingual/visual 管線 |
| `fill_translations.py` | 翻譯核心：`fill_template_from_dict()` + `tw_to_cn()` |
| `build_html.py` | Markdown → HTML 建置 |
| `translate_*.py` | 各課程翻譯腳本（13 支） |

## Environment

- Working directory: `/Volumes/Muse_AI_Core/CCA-Learning`
- Git branch: `main`
- Python 3 + Pillow + ffmpeg required for visual pipeline
