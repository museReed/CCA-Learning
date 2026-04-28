#!/usr/bin/env python3
"""Scrape lesson content for 3 new courses from Skilljar.
Creates source/ transcripts and proper directory structure.
"""
import json
import re
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path("/Volumes/Muse_AI_Core/CCA-Learning")
SESSION_FILE = BASE / "scripts" / "skilljar_session.json"

COURSES = [
    {
        "name": "claude-101",
        "slug": "claude-101",
        "chapter": "01-full-course",
        "lessons": [
            ("01-what-is-claude", "What is Claude?"),
            ("02-your-first-conversation-with-claude", "Your first conversation with Claude"),
            ("03-getting-better-results", "Getting better results"),
            ("04-claude-desktop-app", "Claude desktop app: Chat, Cowork, Code"),
            ("05-introduction-to-projects", "Introduction to projects"),
            ("06-creating-with-artifacts", "Creating with artifacts"),
            ("07-working-with-skills", "Working with skills"),
            ("08-connecting-your-tools", "Connecting your tools"),
            ("09-enterprise-search", "Enterprise search"),
            ("10-research-mode-for-deep-dives", "Research mode for deep dives"),
            ("11-claude-in-action", "Claude in action: use-cases by role"),
            ("12-other-ways-to-work-with-claude", "Other ways to work with Claude"),
            ("13-whats-next", "What's next?"),
        ],
    },
    {
        "name": "introduction-to-agent-skills",
        "slug": "introduction-to-agent-skills",
        "chapter": "01-full-course",
        "lessons": [
            ("01-what-are-skills", "What are skills?"),
            ("02-creating-your-first-skill", "Creating your first skill"),
            ("03-configuration-and-multi-file-skills", "Configuration and multi-file skills"),
            ("04-skills-vs-other-claude-code-features", "Skills vs. other Claude Code features"),
            ("05-sharing-skills", "Sharing skills"),
            ("06-troubleshooting-skills", "Troubleshooting skills"),
        ],
    },
    {
        "name": "introduction-to-subagents",
        "slug": "introduction-to-subagents",
        "chapter": "01-full-course",
        "lessons": [
            ("01-what-are-subagents", "What are subagents?"),
            ("02-creating-a-subagent", "Creating a subagent"),
            ("03-designing-effective-subagents", "Designing effective subagents"),
            ("04-using-subagents-effectively", "Using subagents effectively"),
        ],
    },
]


def scrape_lesson(page, course_slug, lesson_name):
    """Find and scrape a lesson page by name."""
    # First go to course page to find the lesson link
    page.goto(f"https://anthropic.skilljar.com/{course_slug}",
              wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)

    # Find the lesson link
    lesson_link = page.evaluate("""(lessonName) => {
        const links = document.querySelectorAll('a[href]');
        for (const a of links) {
            const text = a.textContent.trim();
            if (text === lessonName) {
                return a.getAttribute('href');
            }
        }
        // Fuzzy match
        const norm = lessonName.toLowerCase().replace(/[^a-z0-9]/g, '');
        for (const a of links) {
            const text = a.textContent.trim().toLowerCase().replace(/[^a-z0-9]/g, '');
            if (text === norm || text.includes(norm) || norm.includes(text)) {
                const href = a.getAttribute('href');
                if (href.match(/\\/\\d+$/)) return href;
            }
        }
        return null;
    }""", lesson_name)

    if not lesson_link:
        print(f"      ⚠️ Could not find link for '{lesson_name}'")
        return None

    # Navigate to lesson page
    url = f"https://anthropic.skilljar.com{lesson_link}" if lesson_link.startswith("/") else lesson_link
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    time.sleep(5)

    # Extract content
    content = page.evaluate("""() => {
        const data = {
            title: '',
            url: window.location.href,
            hasVideo: false,
            videoType: null,
            youtubeId: null,
            textContent: '',
            htmlContent: '',
            images: [],
            contentType: 'unknown',
        };

        // Title
        const h1 = document.querySelector('h1');
        data.title = h1 ? h1.textContent.trim() : document.title;

        // Check for video
        const video = document.querySelector('video');
        const ytIframe = document.querySelector('iframe[src*="youtube"]');
        if (video) {
            data.hasVideo = true;
            data.videoType = 'jwplayer';
        } else if (ytIframe) {
            data.hasVideo = true;
            data.videoType = 'youtube';
            const m = ytIframe.src.match(/embed\\/([\\w-]+)/);
            if (m) data.youtubeId = m[1];
        }

        // Get main content area (exclude nav, sidebar)
        const selectors = [
            '.lesson-content',
            '.page-content',
            '.content-area',
            'article',
            'main .content',
            'main',
        ];
        let main = null;
        for (const sel of selectors) {
            main = document.querySelector(sel);
            if (main && main.textContent.trim().length > 100) break;
        }
        if (!main) main = document.body;

        // Get clean text content
        const clone = main.cloneNode(true);
        // Remove nav, header, footer, sidebar elements
        clone.querySelectorAll('nav, header, footer, .sidebar, .nav, script, style, .curriculum').forEach(el => el.remove());

        data.textContent = clone.textContent.trim();
        data.htmlContent = clone.innerHTML;

        // Collect images
        main.querySelectorAll('img').forEach(img => {
            const src = img.src || '';
            const alt = img.alt || '';
            if (src && !src.includes('avatar') && !src.includes('logo') && !src.includes('favicon'))
                data.images.push({src, alt});
        });

        // Detect content type
        if (document.querySelector('form, input[type="radio"], .quiz, .assessment'))
            data.contentType = 'quiz';
        else if (data.hasVideo && data.textContent.length < 500)
            data.contentType = 'video-only';
        else if (data.hasVideo)
            data.contentType = 'video+text';
        else
            data.contentType = 'text';

        return data;
    }""")

    return content


def clean_text(text):
    """Clean scraped text content."""
    # Remove excessive whitespace
    lines = text.split('\n')
    cleaned = []
    prev_empty = False
    for line in lines:
        line = line.strip()
        if not line:
            if not prev_empty:
                cleaned.append('')
            prev_empty = True
        else:
            prev_empty = False
            cleaned.append(line)
    return '\n'.join(cleaned).strip()


def create_transcript(lesson_dir, slug, title, content):
    """Create a source transcript markdown file."""
    source_dir = lesson_dir / "source"
    source_dir.mkdir(parents=True, exist_ok=True)

    md_path = source_dir / f"{slug}.md"

    lines = [f"# {title}", ""]

    if content.get("url"):
        lines.append(f"> Source: {content['url']}")
        lines.append("")

    if content.get("hasVideo"):
        vtype = content.get("videoType", "unknown")
        if content.get("youtubeId"):
            lines.append(f"> Video: YouTube ({content['youtubeId']})")
        else:
            lines.append(f"> Video: {vtype}")
        lines.append("")

    # Clean and add text content
    text = clean_text(content.get("textContent", ""))
    if text:
        lines.append(text)
    else:
        lines.append("*(Video-only lesson — see video and SRT for content)*")

    lines.append("")
    md_path.write_text('\n'.join(lines), encoding='utf-8')
    return md_path


def main():
    session_data = json.loads(SESSION_FILE.read_text())
    storage_state = session_data.get("storage_state")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=storage_state)
        page = context.new_page()

        for course in COURSES:
            print(f"\n{'='*70}")
            print(f"📖 {course['name']} ({len(course['lessons'])} lessons)")
            print(f"{'='*70}")

            for slug, title in course["lessons"]:
                lesson_dir = BASE / "courses" / course["name"] / course["chapter"] / slug
                lesson_dir.mkdir(parents=True, exist_ok=True)

                # Check if transcript already exists
                source_dir = lesson_dir / "source"
                if source_dir.exists() and list(source_dir.glob("*.md")):
                    existing = list(source_dir.glob("*.md"))[0]
                    size = existing.stat().st_size
                    if size > 200:  # more than just a placeholder
                        print(f"   ⏭️  {slug} (transcript exists, {size}B)")
                        continue

                print(f"   ⬇️  {slug} — {title}")
                content = scrape_lesson(page, course["slug"], title)

                if content:
                    md_path = create_transcript(lesson_dir, slug, title, content)
                    text_len = len(content.get("textContent", ""))
                    ctype = content.get("contentType", "?")
                    print(f"      ✅ {ctype} | {text_len} chars → {md_path.name}")
                else:
                    # Create minimal placeholder
                    source_dir.mkdir(parents=True, exist_ok=True)
                    (source_dir / f"{slug}.md").write_text(
                        f"# {title}\n\n> Source: https://anthropic.skilljar.com/{course['slug']}\n\n*(Content not available)*\n",
                        encoding='utf-8')
                    print(f"      ⚠️ Created placeholder")

        time.sleep(2)
        browser.close()

    # Update outline JSONs
    print(f"\n{'='*70}")
    print("Updating outline JSONs...")
    print(f"{'='*70}")
    for course in COURSES:
        outline = {
            "title": course["name"].replace("-", " ").title(),
            "lessons": [{"slug": s, "title": t} for s, t in course["lessons"]],
            "method": "sequential",
        }
        outline_path = BASE / "courses" / course["name"] / "00-outline.json"
        outline_path.write_text(json.dumps(outline, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f"   ✅ {course['name']}/00-outline.json ({len(course['lessons'])} lessons)")

    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    for course in COURSES:
        course_dir = BASE / "courses" / course["name"] / course["chapter"]
        transcripts = list(course_dir.rglob("source/*.md"))
        videos = list(course_dir.rglob("videos/*.mp4"))
        srts = list(course_dir.rglob("srt/*.srt"))
        print(f"   {course['name']:45s} {len(transcripts)} transcripts | {len(videos)} videos | {len(srts)} SRTs")


if __name__ == "__main__":
    main()
