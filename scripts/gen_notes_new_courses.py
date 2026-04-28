#!/usr/bin/env python3
"""Generate 6-version study notes for 3 new courses.
Reads source transcripts and generates eng/pm × en/zh-TW/zh-CN notes.

Since we can't call external APIs, this generates structured notes
from the transcript content directly.
"""
import re
from pathlib import Path

BASE = Path("/Volumes/Muse_AI_Core/CCA-Learning/courses")

# CCA domain mapping
DOMAIN_MAP = {
    "claude-101": {
        "domain": "General — Claude Fundamentals",
        "task_statements": "General product knowledge (not directly CCA-tested, but foundational)",
    },
    "introduction-to-agent-skills": {
        "domain": "D3 — Claude Code Configuration & Workflows (20%)",
        "task_statements": "3.1 (CLAUDE.md), 3.3 (custom commands/skills), 3.5 (permission model)",
    },
    "introduction-to-subagents": {
        "domain": "D3 — Claude Code Configuration & Workflows (20%), D1 — Agentic Architecture (27%)",
        "task_statements": "3.4 (context management), 1.1 (agentic loops), 1.3 (multi-agent orchestration)",
    },
}


def read_transcript(lesson_dir):
    """Read the source transcript."""
    source_dir = lesson_dir / "source"
    if not source_dir.exists():
        return ""
    mds = list(source_dir.glob("*.md"))
    if not mds:
        return ""
    return mds[0].read_text(encoding="utf-8")


def extract_sections(text):
    """Extract key sections from transcript text."""
    # Remove metadata lines
    lines = text.split('\n')
    content_lines = []
    for line in lines:
        if line.startswith('>'):
            continue
        content_lines.append(line)
    text = '\n'.join(content_lines)

    # Extract learning objectives (bullet points after "By the end...")
    obj_match = re.search(r"(?:By the end.*?:|you'll be able to:)\s*\n(.*?)(?:\n\n|\n\(\d)", text, re.DOTALL)
    learning_objectives = ""
    if obj_match:
        raw = obj_match.group(1).strip()
        # Format as proper bullet list
        obj_lines = [l.strip() for l in raw.split('\n') if l.strip()]
        learning_objectives = '\n'.join(f"- {l}" if not l.startswith('-') else l for l in obj_lines)

    # Extract video description (paragraph after "(X minutes)" time marker)
    desc_match = re.search(r'\(\d+ minutes?\)\s*\n+(.*?)(?:\nKey takeaway|\n\n\n)', text, re.DOTALL)
    video_description = desc_match.group(1).strip() if desc_match else ""

    # Extract key takeaways
    takeaway_match = re.search(r'Key takeaways?\s*\n(.*?)(?:\n\n\n|\n[A-Z][a-z]+ [a-z])', text, re.DOTALL)
    takeaways = ""
    if takeaway_match:
        raw = takeaway_match.group(1).strip()
        # Each takeaway is a paragraph — split on blank lines or sentence boundaries
        takeaway_lines = [l.strip() for l in raw.split('\n') if l.strip()]
        takeaways = '\n'.join(takeaway_lines)

    return {
        "objectives": learning_objectives,
        "description": video_description,
        "takeaways": takeaways,
        "full_text": text,
    }


def summarize_text(text):
    """Extract the video description paragraph as the one-liner summary."""
    # Look for description after time marker "(X minutes)"
    desc_match = re.search(r'\(\d+ minutes?\)\s*\n+(.*?)(?:\nKey takeaway|\n\n\n)', text, re.DOTALL)
    if desc_match:
        desc = desc_match.group(1).strip()
        # Take first 1-2 sentences
        sentences = re.split(r'(?<=[.!?])\s+', desc)
        meaningful = [s for s in sentences if len(s) > 20]
        if meaningful:
            return ' '.join(meaningful[:2])

    # Fallback: find first real paragraph (skip metadata, headers, bullets)
    lines = text.split('\n')
    in_metadata = True
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('#') or stripped.startswith('>'):
            continue
        if in_metadata and re.match(r'(What you|Estimated|By the end|Define |Explain |Describe |Identify |Compare |Choose |Create |Use |Configure |Diagnose |Resolve |Debug |\(\d)', stripped):
            continue
        if stripped.startswith('Key takeaway'):
            continue
        in_metadata = False
        if len(stripped) > 50:
            sentences = re.split(r'(?<=[.!?])\s+', stripped)
            meaningful = [s for s in sentences if len(s) > 20]
            if meaningful:
                return ' '.join(meaningful[:2])
    return ""


def extract_key_concepts(text):
    """Extract bullet-point key concepts."""
    concepts = []
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        # Capture bullet points and bold text
        if line.startswith('- ') or line.startswith('* '):
            concepts.append(line[2:].strip())
        elif '**' in line:
            bold = re.findall(r'\*\*(.+?)\*\*', line)
            for b in bold:
                if len(b) > 10 and len(b) < 100:
                    concepts.append(b)
    return concepts[:10]


def generate_flashcards(title, takeaways):
    """Generate Q&A flashcards from key takeaways."""
    cards = []
    if takeaways:
        lines = [l.strip() for l in takeaways.split('\n') if l.strip()]
        for i, t in enumerate(lines[:6]):
            # Create a question from the first clause
            first_clause = t.split('.')[0] if '.' in t else t[:60]
            # Truncate question if too long
            if len(first_clause) > 80:
                first_clause = first_clause[:77] + "..."
            cards.append(f"**Q{i+1}:** {first_clause}?\n**A{i+1}:** {t}")
    return cards[:6]


def gen_eng_en(lesson_slug, title, transcript, course_name):
    """Generate engineer version in English."""
    sections = extract_sections(transcript)
    domain = DOMAIN_MAP.get(course_name, {})
    summary = summarize_text(transcript)
    concepts = extract_key_concepts(transcript)
    flashcards = generate_flashcards(title, sections["takeaways"])

    lines = [
        f"# {title} — Engineering Deep Dive",
        "",
        "| Item | Detail |",
        "|------|--------|",
        f"| Exam Domain | {domain.get('domain', 'General')} |",
        f"| Task Statements | {domain.get('task_statements', 'N/A')} |",
        f"| Source | {course_name} / Lesson {lesson_slug.split('-')[0]} |",
        "",
        "---",
        "",
        "## One-Liner",
        "",
        summary if summary else f"This lesson covers {title.lower()}.",
        "",
        "---",
        "",
        "## Core Concepts",
        "",
    ]

    if sections["objectives"]:
        lines.append("### Learning Objectives")
        lines.append("")
        lines.append(sections["objectives"])
        lines.append("")

    if sections["takeaways"]:
        lines.append("### Key Takeaways")
        lines.append("")
        lines.append(sections["takeaways"])
        lines.append("")

    if concepts:
        lines.append("### Key Points")
        lines.append("")
        for c in concepts[:8]:
            lines.append(f"- {c}")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## Flashcards",
        "",
    ])
    for card in flashcards:
        lines.append(card)
        lines.append("")

    lines.extend(["---", "", f"*Source: {course_name} — {title}*", ""])
    return '\n'.join(lines)


def gen_pm_en(lesson_slug, title, transcript, course_name):
    """Generate PM version in English."""
    sections = extract_sections(transcript)
    domain = DOMAIN_MAP.get(course_name, {})
    summary = summarize_text(transcript)
    concepts = extract_key_concepts(transcript)

    lines = [
        f"# {title} — PM Perspective",
        "",
        "| Item | Details |",
        "|------|---------|",
        f"| Exam Coverage | {domain.get('domain', 'General')} |",
        f"| Task Statements | {domain.get('task_statements', 'N/A')} |",
        f"| Course Source | {course_name} / Lesson {lesson_slug.split('-')[0]} |",
        "",
        "---",
        "",
        "## TL;DR",
        "",
        summary if summary else f"This lesson covers {title.lower()} from a product perspective.",
        "",
        "---",
        "",
        "## Why This Matters for PMs",
        "",
    ]

    if sections["objectives"]:
        lines.append("### What You'll Understand After This Lesson")
        lines.append("")
        lines.append(sections["objectives"])
        lines.append("")

    if sections["takeaways"]:
        lines.append("### Key Takeaways (Business Impact)")
        lines.append("")
        lines.append(sections["takeaways"])
        lines.append("")

    if concepts:
        lines.append("### Key Concepts to Know")
        lines.append("")
        for c in concepts[:6]:
            lines.append(f"- {c}")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## PRD Checklist",
        "",
        f"- [ ] Does the team understand {title.lower()}?",
        f"- [ ] Are the relevant features documented?",
        f"- [ ] Have edge cases been considered?",
        "",
        "---",
        "",
        f"*Source: {course_name} — {title}*",
        "",
    ])
    return '\n'.join(lines)


def tw_to_cn(text):
    """Convert Traditional Chinese to Simplified Chinese (basic character mapping)."""
    # Minimal mapping for common chars — same approach as fill_translations.py
    TW_CN = str.maketrans(
        "態說這裡個來們對過還將會從與進點開關於機學習題問題實現員類認為應該結構資訊環境變數設計測試運執際錯誤處計畫項標準備輸範圍際連線端點節組件參數據編碼解開發際驗證書檔案類別範例項鏈標記狀態輸響應數據區塊範圍選擇戶頭認證維護擴展語義規則環節對話記錄標籤處運算轉換執緒線進階觀察監視追蹤維護應響視窗區間層級繫結構發佈動態實體範疇運營維護觀測識別語義標記設備驅動裝置優化處置顯示讀寫運算緩衝區間設計檔腳無線顯著與體積預覽採購結餘順價據證書學歷齡資訊優質適確認計實區議體檢單標題覽繫統計劃國際發圖標實餘數據類別語義環節維護實體識別優化視窗進階驗證記錄處運輸資訊對話學習連結設備裝置資料庫結構擴展應響變數設計實現運算標記狀態範圍選擇認證權維護觀測監視追蹤顯示讀寫處置觸發佈動態執緒線計畫處運營維護",
        "态说这里个来们对过还将会从与进点开关于机学习题问题实现员类认为应该结构资讯环境变数设计测试运执际错误处计划项标准备输范围际连线端点节组件参数据编码解开发际验证书档案类别范例项链标记状态输响应数据区块范围选择户头认证维护扩展语义规则环节对话记录标签处运算转换执绑线进阶观察监视追踪维护应响视窗区间层级绑结构发布动态实体范畴运营维护观测识别语义标记设备驱动装置优化处置显示读写运算缓冲区间设计档脚无线显著与体积预览采购结余顺价据证书学历龄资讯优质适确认计实区议体检单标题览系统计划国际发图标实余数据类别语义环节维护实体识别优化视窗进阶验证记录处运输资讯对话学习连结设备装置资料库结构扩展应响变数设计实现运算标记状态范围选择认证权维护观测监视追踪显示读写处置触发布动态执绑线计划处运营维护"
    )
    return text.translate(TW_CN)


def translate_to_zh_tw(text):
    """Basic English → Traditional Chinese translation for headers and structure.
    Full content stays in English with Chinese headers/labels."""
    # Replace common headers
    replacements = {
        "# Engineering Deep Dive": "# 工程師深度解析",
        "# PM Perspective": "# PM 觀點",
        "## One-Liner": "## 一句話摘要",
        "## TL;DR": "## 一句話摘要",
        "## Core Concepts": "## 核心概念",
        "### Learning Objectives": "### 學習目標",
        "### Key Takeaways": "### 重點摘要",
        "### Key Points": "### 關鍵要點",
        "### Key Takeaways (Business Impact)": "### 重點摘要（商業影響）",
        "### What You'll Understand After This Lesson": "### 課後你會理解",
        "### Key Concepts to Know": "### 需要了解的概念",
        "## Why This Matters for PMs": "## 為什麼 PM 需要知道",
        "## Flashcards": "## 記憶卡",
        "## PRD Checklist": "## PRD 檢查清單",
        "| Item | Detail |": "| 項目 | 細節 |",
        "| Item | Details |": "| 項目 | 細節 |",
        "| Exam Domain |": "| 考試領域 |",
        "| Exam Coverage |": "| 考試覆蓋 |",
        "| Task Statements |": "| 任務陳述 |",
        "| Source |": "| 來源 |",
        "| Course Source |": "| 課程來源 |",
    }
    for en, zh in replacements.items():
        text = text.replace(en, zh)
    return text


def process_course(course_name, chapter_name):
    """Process all lessons in a course."""
    course_dir = BASE / course_name / chapter_name
    lessons = sorted([d for d in course_dir.iterdir()
                      if d.is_dir() and d.name[0].isdigit()])

    print(f"\n{'='*70}")
    print(f"📖 {course_name} ({len(lessons)} lessons × 6 versions = {len(lessons)*6} notes)")
    print(f"{'='*70}")

    count = 0
    for lesson_dir in lessons:
        slug = lesson_dir.name
        transcript = read_transcript(lesson_dir)
        if not transcript:
            print(f"   ⚠️ {slug} — no transcript, skipping")
            continue

        # Extract title from transcript
        title_match = re.match(r'^# (.+)', transcript)
        title = title_match.group(1) if title_match else slug.split('-', 1)[1].replace('-', ' ').title()

        eng_dir = lesson_dir / "study-notes" / "eng"
        pm_dir = lesson_dir / "study-notes" / "pm"
        eng_dir.mkdir(parents=True, exist_ok=True)
        pm_dir.mkdir(parents=True, exist_ok=True)

        # Generate 6 versions
        # 1. eng-en
        eng_en = gen_eng_en(slug, title, transcript, course_name)
        (eng_dir / f"{slug}-eng-en.md").write_text(eng_en, encoding='utf-8')

        # 2. eng-zh-TW (Chinese headers, English content)
        eng_zhtw = translate_to_zh_tw(eng_en)
        (eng_dir / f"{slug}-eng-zh-TW.md").write_text(eng_zhtw, encoding='utf-8')

        # 3. eng-zh-CN
        eng_zhcn = tw_to_cn(eng_zhtw)
        (eng_dir / f"{slug}-eng-zh-CN.md").write_text(eng_zhcn, encoding='utf-8')

        # 4. pm-en
        pm_en = gen_pm_en(slug, title, transcript, course_name)
        (pm_dir / f"{slug}-pm-en.md").write_text(pm_en, encoding='utf-8')

        # 5. pm-zh-TW
        pm_zhtw = translate_to_zh_tw(pm_en)
        (pm_dir / f"{slug}-pm-zh-TW.md").write_text(pm_zhtw, encoding='utf-8')

        # 6. pm-zh-CN
        pm_zhcn = tw_to_cn(pm_zhtw)
        (pm_dir / f"{slug}-pm-zh-CN.md").write_text(pm_zhcn, encoding='utf-8')

        count += 6
        print(f"   ✅ {slug} — 6 notes ({len(eng_en)} + {len(pm_en)} bytes)")

    return count


def main():
    total = 0
    total += process_course("claude-101", "01-full-course")
    total += process_course("introduction-to-agent-skills", "01-full-course")
    total += process_course("introduction-to-subagents", "01-full-course")

    print(f"\n{'='*70}")
    print(f"TOTAL: {total} study notes generated")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
