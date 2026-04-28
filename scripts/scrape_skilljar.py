#!/usr/bin/env python3
"""Scrape Skilljar courses to check for uncaptured content.

Usage:
  Step 1 (first time): python3 scrape_skilljar.py --login
    → Opens browser, you login manually, press Enter in terminal to save session.
  Step 2: python3 scrape_skilljar.py
    → Uses saved session to scrape all 3 courses.
"""
import json
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

SESSION_FILE = Path(__file__).parent / "skilljar_session.json"

COURSES = [
    {
        "name": "claude-101",
        "url": "https://anthropic.skilljar.com/claude-101",
    },
    {
        "name": "introduction-to-agent-skills",
        "url": "https://anthropic.skilljar.com/introduction-to-agent-skills",
    },
    {
        "name": "introduction-to-subagents",
        "url": "https://anthropic.skilljar.com/introduction-to-subagents",
    },
]

# Also check the 4 main courses for any new lessons we might have missed
MAIN_COURSES = [
    {
        "name": "building-with-the-claude-api",
        "url": "https://anthropic.skilljar.com/claude-with-the-anthropic-api",
    },
    {
        "name": "claude-code-in-action",
        "url": "https://anthropic.skilljar.com/claude-code-in-action",
    },
    {
        "name": "introduction-to-model-context-protocol",
        "url": "https://anthropic.skilljar.com/introduction-to-model-context-protocol",
    },
    {
        "name": "model-context-protocol-advanced-topics",
        "url": "https://anthropic.skilljar.com/model-context-protocol-advanced-topics",
    },
]


def do_login():
    """Open browser for manual login. User presses Enter when done."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        # Go to login page
        page.goto("https://anthropic.skilljar.com/auth/login?next=%2Fclaude-101",
                   wait_until="domcontentloaded", timeout=30000)

        print("\n🔐 Browser opened — please login to Skilljar.")
        print("   Complete the Google SSO / login flow.")
        print("   Once you see the course dashboard, come back here.")

        # Write a signal file; we poll for it instead of input()
        signal = Path("/tmp/skilljar_login_done")
        signal.unlink(missing_ok=True)
        print(f"\n👉  When logged in, run this in another terminal:")
        print(f"      touch /tmp/skilljar_login_done")
        print(f"\n   Waiting for signal file...")

        for i in range(300):  # 5 min max
            time.sleep(1)
            if signal.exists():
                signal.unlink(missing_ok=True)
                print("   ✅ Signal received! Saving session...")
                time.sleep(3)  # let final cookies settle
                break
            if i % 15 == 0 and i > 0:
                print(f"   [{i}s] Still waiting... (current: {page.url[:80]})")
        else:
            print("   ⏰ 5-min timeout. Saving whatever we have.")

        # Collect cookies
        cookies = context.cookies()

        # Collect localStorage + sessionStorage
        storage = page.evaluate("""() => {
            const data = {};
            try {
                for (let i = 0; i < localStorage.length; i++) {
                    const key = localStorage.key(i);
                    data['localStorage:' + key] = localStorage.getItem(key);
                }
            } catch(e) {}
            try {
                for (let i = 0; i < sessionStorage.length; i++) {
                    const key = sessionStorage.key(i);
                    data['sessionStorage:' + key] = sessionStorage.getItem(key);
                }
            } catch(e) {}
            return data;
        }""")

        # Save Playwright browser storage state (includes cookies + origins)
        storage_state = context.storage_state()

        session_data = {
            "cookies": cookies,
            "storage": storage,
            "storage_state": storage_state,
            "saved_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "url_at_save": page.url,
        }
        SESSION_FILE.write_text(json.dumps(session_data, indent=2))

        print(f"\n✅ Session saved to {SESSION_FILE}")
        print(f"   URL at save: {page.url}")
        print(f"   Cookies: {len(cookies)}")
        print(f"   Storage items: {len(storage)}")
        print(f"   ---")
        for c in cookies:
            exp = c.get('expires', -1)
            httponly = '🔒httpOnly' if c.get('httpOnly') else ''
            print(f"   🍪 {c['name']:40s} {c.get('domain',''):30s} {httponly}")
        for k in sorted(storage.keys()):
            print(f"   💾 {k}: {str(storage[k])[:80]}")

        browser.close()


def scrape_course(page, course_info):
    """Scrape a single course page and return structure info."""
    url = course_info["url"]
    name = course_info["name"]
    print(f"\n{'='*60}")
    print(f"📖 {name}")
    print(f"   {url}")
    print(f"{'='*60}")

    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    time.sleep(5)  # let dynamic content load

    # Get page title
    title = page.title()
    print(f"   Title: {title}")

    # Check if we're redirected to login
    current_url = page.url
    if "sign_in" in current_url or "login" in current_url:
        print("   ⚠️  Redirected to login page — session may have expired")
        return {"name": name, "error": "login_required", "url": current_url}

    # Try to find course structure — Skilljar uses various layouts
    result = page.evaluate("""() => {
        const data = {
            url: window.location.href,
            title: document.title,
            sections: [],
            lessons: [],
            videos: [],
            iframes: [],
            links: [],
            bodyText: '',
        };

        // Find section/chapter headers
        document.querySelectorAll('h1, h2, h3, h4, .section-title, .chapter-title, .module-title').forEach(el => {
            const text = el.textContent.trim();
            if (text) data.sections.push({tag: el.tagName, text: text});
        });

        // Find lesson items (common Skilljar patterns)
        document.querySelectorAll('.lesson, .lesson-item, .curriculum-item, [class*="lesson"], [class*="curriculum"]').forEach(el => {
            const text = el.textContent.trim().substring(0, 200);
            if (text) data.lessons.push(text);
        });

        // Find video elements
        document.querySelectorAll('video, iframe[src*="video"], iframe[src*="youtube"], iframe[src*="vimeo"], iframe[src*="wistia"]').forEach(el => {
            data.videos.push({
                tag: el.tagName,
                src: el.src || el.getAttribute('data-src') || '',
                type: el.getAttribute('type') || '',
            });
        });

        // All iframes
        document.querySelectorAll('iframe').forEach(el => {
            data.iframes.push({src: el.src || '', title: el.title || ''});
        });

        // All links on page
        document.querySelectorAll('a[href]').forEach(el => {
            const href = el.getAttribute('href');
            const text = el.textContent.trim().substring(0, 100);
            if (href && !href.startsWith('#') && !href.startsWith('javascript'))
                data.links.push({href, text});
        });

        // Get main content text (truncated)
        const main = document.querySelector('main, .content, .course-content, #content, article');
        if (main) {
            data.bodyText = main.textContent.trim().substring(0, 3000);
        } else {
            data.bodyText = document.body.textContent.trim().substring(0, 3000);
        }

        return data;
    }""")

    # Print findings
    if result.get("sections"):
        print(f"\n   📑 Sections/Headers ({len(result['sections'])}):")
        for s in result["sections"][:20]:
            print(f"      [{s['tag']}] {s['text'][:80]}")

    if result.get("lessons"):
        print(f"\n   📝 Lesson items ({len(result['lessons'])}):")
        for l in result["lessons"][:20]:
            print(f"      • {l[:100]}")

    if result.get("videos"):
        print(f"\n   🎬 Videos ({len(result['videos'])}):")
        for v in result["videos"]:
            print(f"      {v['tag']}: {v['src'][:100]}")

    if result.get("iframes"):
        print(f"\n   📦 Iframes ({len(result['iframes'])}):")
        for i in result["iframes"]:
            print(f"      {i['src'][:100]} | {i['title']}")

    # Find lesson/page links within the course
    course_links = [l for l in result.get("links", [])
                    if "skilljar" in l["href"] or l["href"].startswith("/")]
    if course_links:
        print(f"\n   🔗 Internal links ({len(course_links)}):")
        for l in course_links[:30]:
            print(f"      {l['text'][:50]:50s} → {l['href'][:80]}")

    # Print body text excerpt
    body = result.get("bodyText", "")
    if body:
        print(f"\n   📄 Content preview ({len(body)} chars):")
        for line in body[:1500].split("\n"):
            line = line.strip()
            if line:
                print(f"      {line[:120]}")

    return result


def scrape_lesson_page(page, url, lesson_name):
    """Scrape an individual lesson page for its actual content."""
    print(f"\n   → Scraping lesson: {lesson_name}")
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    time.sleep(5)  # let dynamic content load

    result = page.evaluate("""() => {
        const data = {
            url: window.location.href,
            title: document.title,
            hasVideo: false,
            videoSrc: '',
            contentType: 'unknown',
            textContent: '',
            images: [],
        };

        // Check for video
        const video = document.querySelector('video');
        const videoIframe = document.querySelector('iframe[src*="video"], iframe[src*="wistia"], iframe[src*="youtube"]');
        if (video) {
            data.hasVideo = true;
            data.videoSrc = video.src || video.querySelector('source')?.src || '';
            data.contentType = 'video';
        } else if (videoIframe) {
            data.hasVideo = true;
            data.videoSrc = videoIframe.src || '';
            data.contentType = 'video';
        }

        // Get text content
        const main = document.querySelector('main, .content, .lesson-content, article, .page-content');
        if (main) {
            data.textContent = main.textContent.trim().substring(0, 5000);
        } else {
            data.textContent = document.body.textContent.trim().substring(0, 5000);
        }

        // Check for images
        document.querySelectorAll('img').forEach(img => {
            const src = img.src || '';
            if (src && !src.includes('avatar') && !src.includes('logo'))
                data.images.push(src.substring(0, 200));
        });

        // Detect content type
        if (data.textContent.length > 500 && !data.hasVideo) data.contentType = 'text';
        if (document.querySelector('form, input[type="radio"], .quiz, .assessment')) data.contentType = 'quiz';

        return data;
    }""")

    print(f"      Type: {result['contentType']} | Video: {result['hasVideo']} | Text: {len(result['textContent'])} chars | Images: {len(result['images'])}")
    return result


def main():
    if "--login" in sys.argv:
        do_login()
        return

    if not SESSION_FILE.exists():
        print("❌ No session file. Run with --login first:")
        print("   python3 scrape_skilljar.py --login")
        sys.exit(1)

    session_data = json.loads(SESSION_FILE.read_text())
    # Support both old format (list of cookies) and new format (dict with cookies key)
    if isinstance(session_data, list):
        cookies = session_data
        storage_state = None
    else:
        cookies = session_data.get("cookies", [])
        storage_state = session_data.get("storage_state")
    print(f"🍪 Loaded session (cookies: {len(cookies)}, saved: {session_data.get('saved_at', '?')})")

    all_results = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        # Use storage_state if available (restores cookies + localStorage in one shot)
        if storage_state:
            context = browser.new_context(storage_state=storage_state)
            print("   Restored full storage state (cookies + origins)")
        else:
            context = browser.new_context()
            context.add_cookies(cookies)
            print("   Restored cookies only")
        page = context.new_page()

        # Scrape 3 lightweight courses
        print("\n" + "="*70)
        print("PART 1: 3 Lightweight Courses")
        print("="*70)
        for course in COURSES:
            result = scrape_course(page, course)
            all_results[course["name"]] = result

        # Also check main courses for any new lessons
        print("\n" + "="*70)
        print("PART 2: 4 Main Courses (checking for new lessons)")
        print("="*70)
        for course in MAIN_COURSES:
            result = scrape_course(page, course)
            all_results[course["name"]] = result

        # Save full results
        output = Path(__file__).parent / "scrape_results.json"
        output.write_text(json.dumps(all_results, indent=2, ensure_ascii=False))
        print(f"\n\n💾 Full results saved to {output}")

        print("\n\nDone. Closing browser in 5s...")
        time.sleep(5)
        browser.close()


if __name__ == "__main__":
    main()
