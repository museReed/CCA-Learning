#!/usr/bin/env python3
"""
CCA Learning HTML builder.
- Walks courses/*/**/study-notes/{eng,pm}/*.md
- Converts each to HTML with standard CSS
- Copies visuals/ alongside
- Regenerates html/index.html
"""
import os, re, shutil, html as htmllib
from pathlib import Path
import markdown

# Resolve repo root from this script's location: scripts/build_html.py → repo root
ROOT = Path(__file__).resolve().parent.parent
COURSES = ROOT / "courses"
HTML = ROOT / "html"

COURSE_META = {
    "claude-code-in-action": {"tag": "CCA", "title": "Claude Code in Action"},
    "introduction-to-model-context-protocol": {"tag": "CCA", "title": "Introduction to MCP"},
    "model-context-protocol-advanced-topics": {"tag": "CCA", "title": "MCP Advanced Topics"},
    "building-with-the-claude-api": {"tag": "CCA", "title": "Building with the Claude API"},
    "claude-101": {"tag": "Intro", "title": "Claude 101"},
    "introduction-to-agent-skills": {"tag": "CCA", "title": "Introduction to Agent Skills"},
    "introduction-to-subagents": {"tag": "CCA", "title": "Introduction to Subagents"},
}

COURSE_ORDER = [
    "claude-101",                                # 1. 入門概覽 — Claude 是什麼、能做什麼
    "claude-code-in-action",                     # 2. 主課程 — D1+D3+D4，佔考試 62%
    "introduction-to-model-context-protocol",    # 3. MCP 入門 — D2 核心
    "model-context-protocol-advanced-topics",    # 4. MCP 進階 — D2 深入 + 部署
    "building-with-the-claude-api",              # 5. API 大課 — D1+D2+D4+D5 綜合
    "introduction-to-agent-skills",              # 6. Skills — D3 補充
    "introduction-to-subagents",                 # 7. Subagents — D3 補充
]

CSS_PAGE = """
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 900px; margin: 0 auto; padding: 2rem; line-height: 1.7; color: #1a1a1a; background: #fafafa; }
h1 { color: #1e293b; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; }
h2 { color: #334155; margin-top: 2rem; }
h3 { color: #475569; }
table { border-collapse: collapse; width: 100%; margin: 1rem 0; }
th, td { border: 1px solid #e2e8f0; padding: 0.5rem 0.75rem; text-align: left; }
th { background: #f1f5f9; font-weight: 600; }
code { background: #f1f5f9; padding: 0.1rem 0.3rem; border-radius: 3px; font-size: 0.9em; }
pre { background: #1e293b; color: #e2e8f0; padding: 1rem; border-radius: 8px; overflow-x: auto; }
pre code { background: none; color: inherit; padding: 0; }
blockquote { border-left: 4px solid #3b82f6; margin: 1rem 0; padding: 0.5rem 1rem; background: #eff6ff; }
img { max-width: 100%; height: auto; display: block; margin: 1.5rem auto; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
em { color: #64748b; }
a { color: #3b82f6; }
hr { border: none; border-top: 1px solid #e2e8f0; margin: 2rem 0; }
.back-link { display: inline-block; margin-bottom: 1rem; color: #6366f1; text-decoration: none; font-size: 0.9em; }
.back-link:hover { text-decoration: underline; }
"""

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
<a href="/Volumes/Muse_AI_Core/CCA-Learning/html/index.html?aud={audience}&lang={lang_code}&from={from_path}&lesson={lesson_slug}" class="back-link">\u2190 Back to Index</a>
{body}
</body>
</html>
"""


def parse_filename(md_path: Path):
    """Extract (lesson_name, audience, lang) from filename like 32-introducing-tool-use-eng-en.md"""
    stem = md_path.stem
    m = re.match(r"^(.*)-(eng|pm)-(en|zh-TW|zh-CN)$", stem)
    if not m:
        return None
    return m.group(1), m.group(2), m.group(3)


def titleize(slug: str) -> str:
    parts = re.sub(r"^\d+-", "", slug).split("-")
    return " ".join(p.capitalize() for p in parts)


def md_to_html_body(md_text: str) -> str:
    return markdown.markdown(md_text, extensions=["tables", "fenced_code", "nl2br"])


def build_page(md_path: Path, course: str) -> Path:
    """Convert one md file to html in the html/ tree. Returns html path."""
    rel = md_path.relative_to(COURSES)
    # rel example: building-with-the-claude-api/04-tool-use/32-introducing-tool-use/study-notes/eng/32-introducing-tool-use-eng-en.md
    parts = list(rel.parts)
    # Remove study-notes/{eng,pm}/ from middle
    try:
        idx = parts.index("study-notes")
        parts = parts[:idx] + parts[idx + 2 :]
    except ValueError:
        pass
    html_rel = Path(*parts).with_suffix(".html")
    html_path = HTML / html_rel
    html_path.parent.mkdir(parents=True, exist_ok=True)

    parsed = parse_filename(md_path)
    lang_attr = "en"
    audience = "eng"
    lang_code = "zh-TW"
    if parsed:
        _, audience, lang_code = parsed
        lang_attr = {"en": "en", "zh-TW": "zh-TW", "zh-CN": "zh-CN"}[lang_code]

    # Build from_path = "course/chapter" and lesson_slug for back-link highlighting
    lesson_dir = md_path.parent.parent.parent
    chapter_slug = lesson_dir.parent.name
    lesson_slug = lesson_dir.name
    from_path = f"{course}/{chapter_slug}"

    md_text = md_path.read_text(encoding="utf-8")
    # Fix image refs: ../../visuals/foo.svg or visuals/foo.svg → visuals/foo.svg (alongside html)
    md_text = re.sub(
        r"!\[([^\]]*)\]\((?:\.\./)*(visuals/[^)]+)\)",
        r"![\1](\2)",
        md_text,
    )
    body = md_to_html_body(md_text)
    title = titleize(md_path.stem)

    html_content = PAGE_TEMPLATE.format(
        lang_attr=lang_attr,
        title=htmllib.escape(title),
        css=CSS_PAGE,
        body=body,
        audience=audience,
        lang_code=lang_code,
        from_path=from_path,
        lesson_slug=lesson_slug,
    )
    html_path.write_text(html_content, encoding="utf-8")
    return html_path


def copy_visuals(lesson_dir: Path):
    """Copy lesson's visuals/ folder to matching html/ lesson dir."""
    visuals_src = lesson_dir / "visuals"
    if not visuals_src.is_dir():
        return
    rel = lesson_dir.relative_to(COURSES)
    visuals_dst = HTML / rel / "visuals"
    visuals_dst.mkdir(parents=True, exist_ok=True)
    for f in visuals_src.iterdir():
        if f.is_file() and f.suffix.lower() in {".svg", ".png", ".jpg", ".jpeg", ".gif"}:
            shutil.copy2(f, visuals_dst / f.name)


def scan_course(course: str):
    """Yield md_paths for a course from study-notes/eng/ and study-notes/pm/."""
    course_root = COURSES / course
    if not course_root.is_dir():
        return
    for subdir in ("eng", "pm"):
        for md_path in sorted(course_root.rglob(f"study-notes/{subdir}/*.md")):
            yield md_path


def scan_lessons_by_chapter(course: str):
    """Return {chapter_dir: {lesson_dir: set_of_variants}}"""
    chapters = {}
    for md_path in scan_course(course):
        lesson_dir = md_path.parent.parent.parent  # strip study-notes/{eng,pm}/file
        chapter_dir = lesson_dir.parent
        variants = chapters.setdefault(str(chapter_dir), {}).setdefault(str(lesson_dir), set())
        parsed = parse_filename(md_path)
        if parsed:
            _, aud, lang = parsed
            variants.add((aud, lang))
    return chapters


def build_all_pages():
    """Build HTML for ALL courses (keeps things consistent)."""
    count = 0
    lesson_dirs_seen = set()
    for course in COURSE_ORDER:
        for md_path in scan_course(course):
            build_page(md_path, course)
            count += 1
            lesson_dir = md_path.parent.parent.parent
            if str(lesson_dir) not in lesson_dirs_seen:
                copy_visuals(lesson_dir)
                lesson_dirs_seen.add(str(lesson_dir))
    return count


# ============ INDEX BUILDING ============

INDEX_HEAD = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CCA Learning — Study Notes</title>
  <style>
    :root {
      --bg: #f8f9fa; --card-bg: #fff; --text: #1a1a2e; --text-secondary: #6b7280;
      --border: #e5e7eb; --accent-active: #4f46e5; --hover: #f3f4f6; --radius: 10px;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; background: var(--bg); color: var(--text); }
    .header { background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%); color: white; padding: 40px 32px 24px; }
    .header h1 { font-size: 1.6em; font-weight: 700; margin-bottom: 4px; }
    .header .subtitle { font-size: 0.95em; opacity: 0.75; }
    .stats { display: flex; gap: 24px; margin-top: 16px; }
    .stat-num { font-size: 1.4em; font-weight: 700; }
    .stat-label { font-size: 0.75em; opacity: 0.7; text-transform: uppercase; letter-spacing: 0.5px; }
    .tabs-container { background: white; border-bottom: 1px solid var(--border); padding: 0 32px; position: sticky; top: 0; z-index: 10; }
    .tab-row { display: flex; align-items: center; gap: 4px; padding: 10px 0 0; flex-wrap: wrap; }
    .tab-row-label { font-size: 0.72em; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px; margin-right: 8px; min-width: 60px; }
    .tab-btn { background: none; border: none; padding: 8px 14px; font-size: 0.85em; font-weight: 500; color: var(--text-secondary); cursor: pointer; border-radius: 6px 6px 0 0; position: relative; transition: all 0.15s; white-space: nowrap; }
    .tab-btn:hover { background: var(--hover); color: var(--text); }
    .tab-btn.active { color: var(--accent-active); background: #eef2ff; }
    .tab-btn.active::after { content: ""; position: absolute; bottom: -1px; left: 6px; right: 6px; height: 3px; background: var(--accent-active); border-radius: 3px 3px 0 0; }
    .tab-count { font-size: 0.75em; opacity: 0.7; margin-left: 3px; }
    .content { padding: 24px 32px 48px; max-width: 900px; margin: 0 auto; }
    .panel { display: none; }
    .panel.active { display: block; }

    /* Course sections — shown/hidden by JS based on course tab */
    .course-section { display: none; border: 1px solid var(--border); border-radius: var(--radius); background: var(--card-bg); overflow: hidden; }
    .course-section.active { display: block; }

    /* Chapter inside course */
    .chapter-card { border-bottom: 1px solid var(--border); transition: background 0.3s; }
    .chapter-card:last-child { border-bottom: none; }
    .chapter-card.highlight { background: #eef2ff; }
    .chapter-toggle { display: flex; align-items: center; gap: 10px; width: 100%; padding: 12px 20px; background: none; border: none; cursor: pointer; text-align: left; transition: background 0.12s; }
    .chapter-toggle:hover { background: var(--hover); }
    .chapter-arrow { font-size: 0.6em; color: var(--text-secondary); transition: transform 0.2s; width: 14px; text-align: center; }
    .chapter-card.open > .chapter-toggle .chapter-arrow { transform: rotate(90deg); }
    .chapter-badge { background: #eef2ff; color: var(--accent-active); font-size: 0.7em; font-weight: 700; padding: 2px 7px; border-radius: 4px; }
    .chapter-title { font-weight: 600; font-size: 0.9em; flex: 1; color: var(--text); }
    .chapter-count { font-size: 0.75em; color: var(--text-secondary); }

    /* Lesson list inside chapter */
    .units { display: none; padding: 0; }
    .chapter-card.open > .units { display: block; }
    .unit-link { display: flex; align-items: center; gap: 8px; padding: 8px 20px 8px 44px; font-size: 0.85em; color: var(--text); text-decoration: none; transition: background 0.1s, box-shadow 0.3s; border-left: 3px solid transparent; }
    .unit-link:hover { background: var(--hover); color: var(--accent-active); border-left-color: var(--accent-active); }
    .unit-link.highlight { background: #eef2ff; border-left-color: #6366f1; color: var(--accent-active); font-weight: 600; }
    .unit-num { font-size: 0.75em; color: var(--text-secondary); font-weight: 600; min-width: 20px; }
  </style>
</head>
<body>
"""

INDEX_SCRIPT = """
<script>
  const audTabs = document.querySelectorAll('.aud-tab');
  const langTabs = document.querySelectorAll('.lang-tab');
  const courseTabs = document.querySelectorAll('.course-tab');
  const panels = document.querySelectorAll('.panel');

  // Read query params from back-link
  const params = new URLSearchParams(window.location.search);
  let currentAud = params.get('aud') || 'eng';
  let currentLang = params.get('lang') || 'zh-TW';
  const fromChapter = params.get('from') || '';
  const fromLesson = params.get('lesson') || '';

  // Determine initial course: from back-link or first available
  let currentCourse = '';
  if (fromChapter) {
    currentCourse = fromChapter.split('/')[0];
  }
  if (!currentCourse && courseTabs.length > 0) {
    currentCourse = courseTabs[0].dataset.course;
  }

  function update() {
    // Audience + language tabs
    audTabs.forEach(t => t.classList.toggle('active', t.dataset.audience === currentAud));
    langTabs.forEach(t => t.classList.toggle('active', t.dataset.lang === currentLang));
    panels.forEach(p => p.classList.toggle('active', p.dataset.audience === currentAud && p.dataset.lang === currentLang));

    // Course tabs — show/hide course sections within the active panel
    courseTabs.forEach(t => t.classList.toggle('active', t.dataset.course === currentCourse));
    const activePanel = document.querySelector('.panel.active');
    if (activePanel) {
      activePanel.querySelectorAll('.course-section').forEach(s => {
        s.classList.toggle('active', s.dataset.course === currentCourse);
      });
    }
  }

  audTabs.forEach(t => t.addEventListener('click', () => { currentAud = t.dataset.audience; update(); }));
  langTabs.forEach(t => t.addEventListener('click', () => { currentLang = t.dataset.lang; update(); }));
  courseTabs.forEach(t => t.addEventListener('click', () => { currentCourse = t.dataset.course; update(); }));
  update();

  // Chapter accordion toggle
  document.querySelectorAll('.chapter-toggle').forEach(btn => {
    btn.addEventListener('click', () => btn.parentElement.classList.toggle('open'));
  });

  // Auto-expand and highlight when returning from a lesson
  if (fromChapter) {
    const activePanel = document.querySelector('.panel.active');
    if (activePanel) {
      const card = activePanel.querySelector('.chapter-card[data-chapter="' + fromChapter + '"]');
      if (card) {
        // Expand the chapter
        card.classList.add('open');

        // Highlight the specific lesson
        const link = fromLesson ? card.querySelector('.unit-link[data-lesson="' + fromLesson + '"]') : null;
        if (link) {
          link.classList.add('highlight');
          setTimeout(() => link.scrollIntoView({ behavior: 'smooth', block: 'center' }), 150);
          setTimeout(() => link.classList.remove('highlight'), 4000);
        } else {
          card.classList.add('highlight');
          setTimeout(() => card.scrollIntoView({ behavior: 'smooth', block: 'center' }), 150);
          setTimeout(() => card.classList.remove('highlight'), 4000);
        }
      }
    }
  }
</script>
</body>
</html>
"""


CHAPTER_LABEL = {
    # claude-code-in-action
    "01-intro": ("Ch 01", "Intro"),
    "02-getting-started": ("Ch 02", "Getting Started"),
    "03-context-and-commands": ("Ch 03", "Context And Commands"),
    "04-integrations": ("Ch 04", "Integrations"),
    "05-hooks": ("Ch 05", "Hooks"),
    "06-sdk-and-wrap-up": ("Ch 06", "SDK And Wrap Up"),
    # mcp intro
    "01-mcp-basics": ("Ch 01", "MCP Basics"),
    "02-tools-and-inspector": ("Ch 02", "Tools And Inspector"),
    "03-resources-and-prompts": ("Ch 03", "Resources And Prompts"),
    "04-assessment": ("Ch 04", "Assessment"),
    # mcp advanced
    "01-sampling-and-notifications": ("Ch 01", "Sampling And Notifications"),
    "02-roots-and-messages": ("Ch 02", "Roots And Messages"),
    "03-transports": ("Ch 03", "Transports"),
    # building with api
    "01-api-fundamentals": ("Ch 01", "API Fundamentals"),
    "02-prompt-evaluation": ("Ch 02", "Prompt Evaluation"),
    "03-prompt-engineering": ("Ch 03", "Prompt Engineering"),
    "04-tool-use": ("Ch 04", "Tool Use"),
    "05-retrieval-augmented-generation": ("Ch 05", "RAG"),
    "06-extended-features": ("Ch 06", "Extended Features"),
    "07-mcp": ("Ch 07", "MCP"),
    "08-agents-and-workflows": ("Ch 08", "Agents And Workflows"),
    "09-assessment": ("Ch 09", "Assessment"),
}


def build_index():
    # Collect all variants available per (course, chapter, lesson)
    data = {}  # data[course][chapter_slug] = [(lesson_slug, variants_set)]
    for course in COURSE_ORDER:
        cdata = data.setdefault(course, {})
        course_root = COURSES / course
        if not course_root.is_dir():
            continue
        # Walk lessons
        seen_lessons = {}
        for md_path in scan_course(course):
            lesson_dir = md_path.parent.parent.parent
            chapter_slug = lesson_dir.parent.name
            lesson_slug = lesson_dir.name
            key = (chapter_slug, lesson_slug)
            variants = seen_lessons.setdefault(key, set())
            parsed = parse_filename(md_path)
            if parsed:
                _, aud, lang = parsed
                variants.add((aud, lang))
        # Group by chapter
        for (chapter_slug, lesson_slug), variants in seen_lessons.items():
            cdata.setdefault(chapter_slug, []).append((lesson_slug, variants))
        # Sort lessons within each chapter
        for chapter_slug in cdata:
            cdata[chapter_slug].sort(key=lambda x: x[0])

    # Count totals
    total_notes = 0
    total_lessons = 0
    total_chapters = 0
    for course in COURSE_ORDER:
        for chapter_slug, lessons in data.get(course, {}).items():
            total_chapters += 1
            for _, variants in lessons:
                total_lessons += 1
                total_notes += len(variants)

    # Header
    parts = [INDEX_HEAD]
    parts.append(f"""
  <div class="header">
    <h1>CCA Learning</h1>
    <div class="subtitle">Claude Certified Associate — 學習筆記</div>
    <div class="stats">
      <div class="stat"><div class="stat-num">{len(COURSE_ORDER)}</div><div class="stat-label">Courses</div></div>
      <div class="stat"><div class="stat-num">{total_chapters}</div><div class="stat-label">Chapters</div></div>
      <div class="stat"><div class="stat-num">{total_lessons}</div><div class="stat-label">Lessons</div></div>
      <div class="stat"><div class="stat-num">{total_notes}</div><div class="stat-label">Notes</div></div>
    </div>
  </div>
""")

    # Count per audience and per language for tab badges
    aud_counts = {"eng": 0, "pm": 0}
    lang_counts = {"en": 0, "zh-TW": 0, "zh-CN": 0}
    for course in COURSE_ORDER:
        for chapter_slug, lessons in data.get(course, {}).items():
            for _, variants in lessons:
                for aud, lang in variants:
                    aud_counts[aud] += 1
                    lang_counts[lang] += 1
    # Divide aud by 3 (3 langs) and lang by 2 (2 auds) to get lesson-level count
    aud_counts = {k: v // 3 for k, v in aud_counts.items()}
    lang_counts = {k: v // 2 for k, v in lang_counts.items()}

    # Build course tab buttons
    course_tab_html = ""
    for course in COURSE_ORDER:
        meta = COURSE_META[course]
        course_tab_html += f'<button class="tab-btn course-tab" data-course="{course}">{htmllib.escape(meta["title"])}</button>'

    parts.append(f"""
  <div class="tabs-container">
    <div class="tab-row"><span class="tab-row-label">Audience</span>
      <button class="tab-btn aud-tab" data-audience="eng">Engineer <span class="tab-count">{aud_counts['eng']}</span></button><button class="tab-btn aud-tab" data-audience="pm">PM <span class="tab-count">{aud_counts['pm']}</span></button>
    </div>
    <div class="tab-row"><span class="tab-row-label">Language</span>
      <button class="tab-btn lang-tab" data-lang="zh-TW">繁體中文 <span class="tab-count">{lang_counts['zh-TW']}</span></button><button class="tab-btn lang-tab" data-lang="en">English <span class="tab-count">{lang_counts['en']}</span></button><button class="tab-btn lang-tab" data-lang="zh-CN">简体中文 <span class="tab-count">{lang_counts['zh-CN']}</span></button>
    </div>
    <div class="tab-row"><span class="tab-row-label">Course</span>
      {course_tab_html}
    </div>
  </div>
  <div class="content">
""")

    # Panels — 6 combinations
    for aud in ["eng", "pm"]:
        for lang in ["zh-TW", "en", "zh-CN"]:
            parts.append(f'    <div class="panel" data-audience="{aud}" data-lang="{lang}">\n')
            for course in COURSE_ORDER:
                course_data = data.get(course, {})
                if not course_data:
                    continue
                meta = COURSE_META[course]
                # Count total lessons in this course for this variant
                course_lesson_count = sum(len([l for l in lessons if (aud, lang) in l[1]]) for lessons in course_data.values())
                parts.append(f'      <div class="course-section" data-course="{course}">\n')
                for chapter_slug in sorted(course_data.keys()):
                    lessons = course_data[chapter_slug]
                    # Filter lessons that have this variant
                    filtered = [l for l in lessons if (aud, lang) in l[1]]
                    if not filtered:
                        continue
                    ch_badge, ch_title = CHAPTER_LABEL.get(chapter_slug, ("", titleize(chapter_slug)))
                    parts.append(f'        <div class="chapter-card" data-chapter="{course}/{chapter_slug}">\n')
                    parts.append(f'          <button class="chapter-toggle"><span class="chapter-arrow">\u25B6</span><span class="chapter-badge">{ch_badge}</span><span class="chapter-title">{htmllib.escape(ch_title)}</span><span class="chapter-count">{len(filtered)} lessons</span></button>\n')
                    parts.append('          <div class="units">\n')
                    for lesson_slug, _variants in filtered:
                        unit_num_m = re.match(r"^(\d+)", lesson_slug)
                        unit_num = unit_num_m.group(1) if unit_num_m else ""
                        unit_title = titleize(lesson_slug)
                        href = f"{course}/{chapter_slug}/{lesson_slug}/{lesson_slug}-{aud}-{lang}.html"
                        parts.append(f'            <a href="{href}" class="unit-link" data-lesson="{lesson_slug}"><span class="unit-num">{unit_num}</span>{htmllib.escape(unit_title)}</a>\n')
                    parts.append('          </div>\n')
                    parts.append('        </div>\n')
                parts.append('      </div>\n')
            parts.append('    </div>\n')

    parts.append('  </div>\n')
    parts.append(INDEX_SCRIPT)

    (HTML / "index.html").write_text("".join(parts), encoding="utf-8")
    return total_notes, total_lessons, total_chapters


def sync_delete():
    """Remove stale HTML files whose source .md no longer exists."""
    # Build set of expected html paths (relative to HTML dir)
    expected = set()
    for course in COURSE_ORDER:
        for md_path in scan_course(course):
            rel = md_path.relative_to(COURSES)
            parts = list(rel.parts)
            try:
                idx = parts.index("study-notes")
                parts = parts[:idx] + parts[idx + 2:]
            except ValueError:
                pass
            expected.add(Path(*parts).with_suffix(".html"))

    # Walk html/ and find .html files (skip index.html)
    removed = 0
    for html_path in sorted(HTML.rglob("*.html")):
        if html_path.name == "index.html":
            continue
        rel = html_path.relative_to(HTML)
        if rel not in expected:
            html_path.unlink()
            removed += 1

    # Remove empty visuals dirs that have no matching lesson source
    for vis_dir in sorted(HTML.rglob("visuals"), reverse=True):
        if vis_dir.is_dir():
            # Check if the corresponding source visuals dir still exists
            rel = vis_dir.relative_to(HTML)
            src_vis = COURSES / rel
            if not src_vis.is_dir():
                shutil.rmtree(vis_dir)
                removed += 1
            else:
                # Remove individual stale visual files
                for f in vis_dir.iterdir():
                    if f.is_file() and not (src_vis / f.name).exists():
                        f.unlink()
                        removed += 1

    # Remove empty directories left behind
    for dirpath in sorted(HTML.rglob("*"), reverse=True):
        if dirpath.is_dir() and not any(dirpath.iterdir()):
            dirpath.rmdir()

    return removed


if __name__ == "__main__":
    n = build_all_pages()
    print(f"Built {n} HTML pages")
    removed = sync_delete()
    if removed:
        print(f"Removed {removed} stale files/dirs")
    notes, lessons, chapters = build_index()
    print(f"Index: {chapters} chapters, {lessons} lessons, {notes} notes")
