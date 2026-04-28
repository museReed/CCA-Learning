#!/usr/bin/env python3
"""Audit all Skilljar courses: enroll if needed, scrape every lesson for video URLs,
compare against local inventory.

Requires: scripts/skilljar_session.json (from scrape_skilljar.py --login)
"""
import json
import re
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path("/Volumes/Muse_AI_Core/CCA-Learning")
SESSION_FILE = BASE / "scripts" / "skilljar_session.json"
REPORT_FILE = BASE / "scripts" / "video_audit_report.json"

COURSES = [
    # (local dir name, skilljar slug, enroll checkout path or None)
    ("claude-101", "claude-101", "/checkout/2241o57l5z4jp"),
    ("introduction-to-agent-skills", "introduction-to-agent-skills", "/checkout/3qmto78bpdsi1"),
    ("introduction-to-subagents", "introduction-to-subagents", "/checkout/2ekik7yjcypt1"),
    ("building-with-the-claude-api", "claude-with-the-anthropic-api", None),
    ("claude-code-in-action", "claude-code-in-action", None),
    ("introduction-to-model-context-protocol", "introduction-to-model-context-protocol", None),
    ("model-context-protocol-advanced-topics", "model-context-protocol-advanced-topics", None),
]


def load_session():
    data = json.loads(SESSION_FILE.read_text())
    return data.get("storage_state") if isinstance(data, dict) else None


def get_local_videos(course_dir_name):
    """Get set of local video stems."""
    course_dir = BASE / "courses" / course_dir_name
    mp4s = set()
    for f in course_dir.rglob("*.mp4"):
        mp4s.add(f.stem)
    srts = set()
    for f in course_dir.rglob("*.srt"):
        if "bilingual" not in f.name:
            srts.add(f.stem)
    return mp4s, srts


def try_enroll(page, checkout_path):
    """Try to enroll in a free course."""
    url = f"https://anthropic.skilljar.com{checkout_path}"
    print(f"   Enrolling via {url}")
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)

    # Look for "Enroll" or "Complete" button
    for selector in [
        'button:has-text("Enroll")',
        'button:has-text("Complete")',
        'button:has-text("Register")',
        'input[type="submit"]',
        '.checkout-button',
        'button.btn-primary',
    ]:
        btn = page.query_selector(selector)
        if btn and btn.is_visible():
            print(f"   Clicking: {selector}")
            btn.click()
            time.sleep(5)
            print(f"   → Now at: {page.url}")
            return True

    # Maybe already enrolled
    if "resume" in page.url or "page/" in page.url:
        print("   Already enrolled (redirected to course)")
        return True

    print(f"   Could not find enroll button. URL: {page.url}")
    # Print page text for debugging
    text = page.evaluate("() => document.body.innerText.substring(0, 500)")
    print(f"   Page text: {text[:200]}")
    return False


def scrape_course_lessons(page, skilljar_slug):
    """Get all lesson links from a course page."""
    url = f"https://anthropic.skilljar.com/{skilljar_slug}"
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    time.sleep(5)

    lessons = page.evaluate("""(slug) => {
        const lessons = [];
        const seen = new Set();
        document.querySelectorAll('a[href]').forEach(a => {
            const href = a.getAttribute('href');
            const text = a.textContent.trim();
            // Match lesson links like /course-slug/123456
            const match = href.match(new RegExp('/' + slug + '/(\\\\d+)$'));
            if (match && !seen.has(href)) {
                seen.add(href);
                lessons.push({
                    name: text.substring(0, 100),
                    href: href,
                    id: match[1],
                });
            }
        });
        return lessons;
    }""", skilljar_slug)

    return lessons


def scrape_lesson_video(page, lesson_url, lesson_name):
    """Visit a single lesson page and extract video info."""
    full_url = f"https://anthropic.skilljar.com{lesson_url}"
    try:
        page.goto(full_url, wait_until="domcontentloaded", timeout=30000)
    except Exception as e:
        print(f"      ⚠️ Failed to load: {e}")
        return None
    time.sleep(3)

    info = page.evaluate("""() => {
        const data = {
            title: document.title,
            url: window.location.href,
            hasVideo: false,
            videoSources: [],
            iframes: [],
            contentType: 'unknown',
            textLength: 0,
        };

        // Direct <video> elements
        document.querySelectorAll('video').forEach(v => {
            data.hasVideo = true;
            if (v.src) data.videoSources.push({type: 'video-src', url: v.src});
            v.querySelectorAll('source').forEach(s => {
                if (s.src) data.videoSources.push({type: 'video-source', url: s.src});
            });
        });

        // Wistia embeds (common on Skilljar)
        document.querySelectorAll('[class*="wistia"], [id*="wistia"]').forEach(el => {
            const match = el.className.match(/wistia_async_([a-z0-9]+)/);
            if (match) {
                data.hasVideo = true;
                data.videoSources.push({
                    type: 'wistia',
                    id: match[1],
                    url: 'https://fast.wistia.net/embed/medias/' + match[1],
                });
            }
        });

        // Iframes (YouTube, Wistia, etc.)
        document.querySelectorAll('iframe').forEach(f => {
            const src = f.src || '';
            data.iframes.push({src: src, title: f.title || ''});
            if (src.includes('youtube.com') || src.includes('youtu.be')) {
                data.hasVideo = true;
                data.videoSources.push({type: 'youtube', url: src});
            }
            if (src.includes('wistia')) {
                data.hasVideo = true;
                data.videoSources.push({type: 'wistia-iframe', url: src});
            }
            if (src.includes('video')) {
                data.hasVideo = true;
                data.videoSources.push({type: 'video-iframe', url: src});
            }
        });

        // Check for Wistia JSON in page
        const scripts = document.querySelectorAll('script');
        scripts.forEach(s => {
            const txt = s.textContent || '';
            const wMatch = txt.match(/wistia_async_([a-z0-9]+)/);
            if (wMatch) {
                data.hasVideo = true;
                data.videoSources.push({type: 'wistia-script', id: wMatch[1]});
            }
        });

        // Content type detection
        const main = document.querySelector('main, .content, .lesson-content, article');
        const text = (main || document.body).textContent || '';
        data.textLength = text.length;

        if (document.querySelector('form, [class*="quiz"], [class*="assessment"], input[type="radio"]'))
            data.contentType = 'quiz';
        else if (document.querySelector('[class*="survey"]'))
            data.contentType = 'survey';
        else if (data.hasVideo)
            data.contentType = 'video';
        else if (text.length > 500)
            data.contentType = 'text';
        else
            data.contentType = 'minimal';

        return data;
    }""")

    status = "🎬" if info["hasVideo"] else "📝" if info["contentType"] == "text" else "📋" if info["contentType"] == "quiz" else "📊" if info["contentType"] == "survey" else "❓"
    video_detail = ""
    if info["videoSources"]:
        v = info["videoSources"][0]
        video_detail = f" [{v['type']}]"
        if "url" in v:
            video_detail += f" {v['url'][:60]}"
    print(f"      {status} {lesson_name[:50]:50s}{video_detail}")

    return info


def main():
    storage_state = load_session()
    if not storage_state:
        print("❌ No valid session. Run: python3 scripts/scrape_skilljar.py --login")
        return

    report = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=storage_state)
        page = context.new_page()

        for local_name, slug, checkout in COURSES:
            print(f"\n{'='*70}")
            print(f"📖 {local_name}")
            print(f"{'='*70}")

            # Enroll if needed
            if checkout:
                try_enroll(page, checkout)

            # Get lesson list
            lessons = scrape_course_lessons(page, slug)
            print(f"   Found {len(lessons)} lessons on Skilljar")

            # Get local inventory
            local_mp4s, local_srts = get_local_videos(local_name)
            print(f"   Local: {len(local_mp4s)} MP4, {len(local_srts)} SRT")

            # Scrape each lesson
            lesson_details = []
            for lesson in lessons:
                info = scrape_lesson_video(page, lesson["href"], lesson["name"])
                lesson_details.append({
                    "name": lesson["name"],
                    "id": lesson["id"],
                    "href": lesson["href"],
                    "video_info": info,
                })

            # Summary
            video_lessons = [l for l in lesson_details if l["video_info"] and l["video_info"]["hasVideo"]]
            non_video = [l for l in lesson_details if l["video_info"] and not l["video_info"]["hasVideo"]]

            print(f"\n   Summary: {len(video_lessons)} video lessons, {len(non_video)} non-video")
            print(f"   Local MP4s: {len(local_mp4s)}, Local SRTs: {len(local_srts)}")

            if len(video_lessons) > len(local_mp4s):
                print(f"   ⚠️  MISSING {len(video_lessons) - len(local_mp4s)} videos!")
            elif len(video_lessons) == len(local_mp4s):
                print(f"   ✅ Video count matches")
            else:
                print(f"   ℹ️  Local has more ({len(local_mp4s)}) than online video lessons ({len(video_lessons)})")

            report[local_name] = {
                "skilljar_slug": slug,
                "total_lessons": len(lessons),
                "video_lessons": len(video_lessons),
                "non_video_lessons": len(non_video),
                "local_mp4": len(local_mp4s),
                "local_srt": len(local_srts),
                "lessons": lesson_details,
                "non_video_names": [l["name"] for l in non_video],
            }

        # Save report
        REPORT_FILE.write_text(json.dumps(report, indent=2, ensure_ascii=False))
        print(f"\n\n💾 Full report: {REPORT_FILE}")

        # Print final summary
        print(f"\n{'='*70}")
        print("FINAL SUMMARY")
        print(f"{'='*70}")
        total_online = 0
        total_local = 0
        for name, data in report.items():
            online = data["video_lessons"]
            local = data["local_mp4"]
            total_online += online
            total_local += local
            status = "✅" if online <= local else f"⚠️  MISSING {online - local}"
            print(f"  {name:50s} Online: {online:3d} | Local: {local:3d} | {status}")
            if data["non_video_names"]:
                for nv in data["non_video_names"]:
                    print(f"    📝 (no video) {nv}")
        print(f"\n  {'TOTAL':50s} Online: {total_online:3d} | Local: {total_local:3d}")

        time.sleep(3)
        browser.close()


if __name__ == "__main__":
    main()
