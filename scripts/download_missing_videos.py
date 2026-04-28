#!/usr/bin/env python3
"""Download all missing course videos.

Part 1: YouTube videos (3 lightweight courses) — uses yt-dlp
Part 2: Wistia/Skilljar videos (building-with-claude-api missing) — uses Playwright
"""
import json
import subprocess
import time
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path("/Volumes/Muse_AI_Core/CCA-Learning")
SESSION_FILE = BASE / "scripts" / "skilljar_session.json"

# ─── Part 1: YouTube videos ───

YOUTUBE_VIDEOS = {
    "claude-101": {
        "chapter": "01-full-course",
        "lessons": [
            ("01-what-is-claude", "https://www.youtube.com/watch?v=VHsp6Hp7Stw"),
            ("02-your-first-conversation-with-claude", "https://www.youtube.com/watch?v=0vZ_UVLhSQQ"),
            ("03-getting-better-results", "https://www.youtube.com/watch?v=Zzn-g8lvLMA"),
            ("05-introduction-to-projects", "https://www.youtube.com/watch?v=GJ5jTgcbRHA"),
            ("07-working-with-skills", "https://www.youtube.com/watch?v=LpGpwhORWr0"),
            ("08-connecting-your-tools", "https://www.youtube.com/watch?v=_jjSS0qGFbI"),
            ("10-research-mode-for-deep-dives", "https://www.youtube.com/watch?v=R-KJgjIrh24"),
            ("12-other-ways-to-work-with-claude", "https://www.youtube.com/watch?v=s-avRazvmLg"),
        ],
    },
    "introduction-to-agent-skills": {
        "chapter": "01-full-course",
        "lessons": [
            ("01-what-are-skills", "https://www.youtube.com/watch?v=bjdBVZa66oU"),
            ("02-creating-your-first-skill", "https://www.youtube.com/watch?v=Wx6_vjFFyHM"),
            ("03-configuration-and-multi-file-skills", "https://www.youtube.com/watch?v=98KaK_rn5rQ"),
            ("04-skills-vs-other-claude-code-features", "https://www.youtube.com/watch?v=IgNN4v0BJdU"),
            ("05-sharing-skills", "https://www.youtube.com/watch?v=OCBi3eScNLk"),
            ("06-troubleshooting-skills", "https://www.youtube.com/watch?v=YBa1cwaG7is"),
        ],
    },
    "introduction-to-subagents": {
        "chapter": "01-full-course",
        "lessons": [
            ("01-what-are-subagents", "https://www.youtube.com/watch?v=jKErNxuxPXg"),
            ("02-creating-a-subagent", "https://www.youtube.com/watch?v=arD6qEWa2Xc"),
            ("03-designing-effective-subagents", "https://www.youtube.com/watch?v=WPxWKT_OaU4"),
            ("04-using-subagents-effectively", "https://www.youtube.com/watch?v=n5LoKZ8Oa-A"),
        ],
    },
}

# ─── Part 2: Skilljar (Wistia) videos ───

SKILLJAR_MISSING = [
    # (lesson_id, lesson_name, chapter_dir, lesson_slug)
    ("287818", "Welcome to the course", "01-api-fundamentals", "02-welcome-to-the-course"),
    ("287756", "Tool functions", "04-tool-use", "23-tool-functions"),
    ("289124", "Quiz on features of Claude", "06-extended-features", "41-quiz-on-features-of-claude"),
    ("289126", "Quiz on Model Context Protocol", "07-mcp", "50-quiz-on-model-context-protocol"),
    ("289130", "Quiz on Agents and Workflows", "08-agents-and-workflows", "58-quiz-on-agents-and-workflows"),
    ("290899", "Final Assessment", "09-assessment", "59-final-assessment"),
]


def download_youtube_videos():
    """Download YouTube videos using yt-dlp."""
    print("\n" + "=" * 70)
    print("PART 1: Downloading YouTube Videos")
    print("=" * 70)

    total = sum(len(v["lessons"]) for v in YOUTUBE_VIDEOS.values())
    count = 0

    for course_name, course_data in YOUTUBE_VIDEOS.items():
        chapter = course_data["chapter"]
        print(f"\n📖 {course_name}")

        for lesson_slug, yt_url in course_data["lessons"]:
            count += 1
            lesson_dir = BASE / "courses" / course_name / chapter / lesson_slug
            video_dir = lesson_dir / "videos"
            video_dir.mkdir(parents=True, exist_ok=True)

            # Check if already downloaded
            existing = list(video_dir.glob("*.mp4"))
            if existing:
                print(f"   [{count}/{total}] ⏭️  {lesson_slug} (already exists)")
                continue

            print(f"   [{count}/{total}] ⬇️  {lesson_slug}")
            print(f"      URL: {yt_url}")

            # Download with yt-dlp
            output_template = str(video_dir / "%(title)s.%(ext)s")
            cmd = [
                "yt-dlp",
                "-f", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best",
                "--merge-output-format", "mp4",
                "-o", output_template,
                "--write-auto-subs",
                "--sub-langs", "en",
                "--convert-subs", "srt",
                "--no-playlist",
                yt_url,
            ]
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                if result.returncode == 0:
                    # Move any SRT files to srt/ dir
                    for srt in video_dir.glob("*.srt"):
                        srt_dir = lesson_dir / "srt"
                        srt_dir.mkdir(exist_ok=True)
                        srt.rename(srt_dir / srt.name)
                    mp4s = list(video_dir.glob("*.mp4"))
                    if mp4s:
                        print(f"      ✅ Downloaded: {mp4s[0].name} ({mp4s[0].stat().st_size // 1024 // 1024}MB)")
                    else:
                        print(f"      ⚠️ No MP4 found after download")
                else:
                    print(f"      ❌ Failed: {result.stderr[:200]}")
            except subprocess.TimeoutExpired:
                print(f"      ❌ Timeout after 120s")
            except Exception as e:
                print(f"      ❌ Error: {e}")


def download_skilljar_videos():
    """Download Skilljar (Wistia) videos using Playwright + yt-dlp."""
    print("\n" + "=" * 70)
    print("PART 2: Downloading Skilljar Videos (building-with-the-claude-api)")
    print("=" * 70)

    session_data = json.loads(SESSION_FILE.read_text())
    storage_state = session_data.get("storage_state")
    if not storage_state:
        print("❌ No valid session for Skilljar")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=storage_state)
        page = context.new_page()

        for i, (lesson_id, name, chapter, slug) in enumerate(SKILLJAR_MISSING, 1):
            lesson_dir = BASE / "courses" / "building-with-the-claude-api" / chapter / slug
            video_dir = lesson_dir / "videos"

            # Check if already exists
            if video_dir.exists() and list(video_dir.glob("*.mp4")):
                print(f"\n   [{i}/{len(SKILLJAR_MISSING)}] ⏭️  {name} (already exists)")
                continue

            url = f"https://anthropic.skilljar.com/claude-with-the-anthropic-api/{lesson_id}"
            print(f"\n   [{i}/{len(SKILLJAR_MISSING)}] ⬇️  {name}")
            print(f"      URL: {url}")

            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(5)

            # Extract video source — try multiple methods
            video_info = page.evaluate("""() => {
                const data = {sources: [], wistiaId: null};

                // Method 1: Direct video source
                document.querySelectorAll('video source').forEach(s => {
                    if (s.src && !s.src.startsWith('blob:'))
                        data.sources.push(s.src);
                });

                // Method 2: Wistia embed
                document.querySelectorAll('[class*="wistia"]').forEach(el => {
                    const m = el.className.match(/wistia_async_([a-z0-9]+)/);
                    if (m) data.wistiaId = m[1];
                });

                // Method 3: Check scripts for Wistia
                document.querySelectorAll('script').forEach(s => {
                    const t = s.textContent || '';
                    const m = t.match(/wistia_async_([a-z0-9]+)/);
                    if (m) data.wistiaId = m[1];
                    // Also check for direct video URLs
                    const urlMatch = t.match(/(https?:\/\/[^\s"']+\.mp4[^\s"']*)/);
                    if (urlMatch) data.sources.push(urlMatch[1]);
                });

                // Method 4: Wistia API
                if (typeof Wistia !== 'undefined') {
                    try {
                        const videos = Wistia.api.all();
                        videos.forEach(v => {
                            const assets = v.data && v.data.media && v.data.media.assets;
                            if (assets) {
                                assets.forEach(a => {
                                    if (a.url && a.type === 'original')
                                        data.sources.push(a.url);
                                });
                            }
                        });
                    } catch(e) {}
                }

                return data;
            }""")

            # Try to get the Wistia video URL via their embed API
            wistia_url = None
            if video_info.get("wistiaId"):
                wid = video_info["wistiaId"]
                wistia_url = f"https://fast.wistia.net/embed/medias/{wid}"
                print(f"      Wistia ID: {wid}")

            # Try yt-dlp on the lesson page URL or Wistia URL
            download_url = wistia_url or url
            video_dir.mkdir(parents=True, exist_ok=True)
            output_template = str(video_dir / f"{name.replace(' ', '_').replace('/', '_')}.%(ext)s")

            cmd = [
                "yt-dlp",
                "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
                "--merge-output-format", "mp4",
                "-o", output_template,
                "--no-playlist",
                download_url,
            ]

            # If wistia didn't work, also try with cookies
            if not wistia_url:
                # Export cookies for yt-dlp
                cookies = context.cookies()
                cookie_file = BASE / "scripts" / ".yt-dlp-cookies.txt"
                with open(cookie_file, "w") as f:
                    f.write("# Netscape HTTP Cookie File\n")
                    for c in cookies:
                        secure = "TRUE" if c.get("secure") else "FALSE"
                        httponly = "TRUE" if c.get("httpOnly") else "FALSE"
                        domain = c.get("domain", "")
                        path = c.get("path", "/")
                        expires = str(int(c.get("expires", 0)))
                        f.write(f"{domain}\tTRUE\t{path}\t{secure}\t{expires}\t{c['name']}\t{c['value']}\n")
                cmd.extend(["--cookies", str(cookie_file)])

            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                if result.returncode == 0 and list(video_dir.glob("*.mp4")):
                    mp4 = list(video_dir.glob("*.mp4"))[0]
                    print(f"      ✅ Downloaded: {mp4.name} ({mp4.stat().st_size // 1024 // 1024}MB)")
                else:
                    print(f"      ❌ yt-dlp failed: {result.stderr[:200]}")
                    print(f"      Trying direct page capture...")

                    # Fallback: try to get video URL from page network requests
                    video_url = page.evaluate("""() => {
                        const v = document.querySelector('video');
                        if (v && v.src && !v.src.startsWith('blob:')) return v.src;
                        // Check performance entries for video URLs
                        const entries = performance.getEntriesByType('resource');
                        for (const e of entries) {
                            if (e.name.includes('.mp4') || e.name.includes('.bin') || e.name.includes('deliveries'))
                                return e.name;
                        }
                        return null;
                    }""")
                    if video_url:
                        print(f"      Found direct URL: {video_url[:80]}")
                        cmd2 = ["yt-dlp", "-o", output_template, video_url]
                        subprocess.run(cmd2, capture_output=True, timeout=120)
                        if list(video_dir.glob("*.mp4")):
                            print(f"      ✅ Downloaded via direct URL")
                        else:
                            print(f"      ❌ Still failed")
                    else:
                        print(f"      ❌ No downloadable URL found")
            except Exception as e:
                print(f"      ❌ Error: {e}")

        time.sleep(2)
        browser.close()


def print_summary():
    """Print final video inventory."""
    print("\n" + "=" * 70)
    print("FINAL INVENTORY")
    print("=" * 70)
    total = 0
    for course in ["claude-101", "introduction-to-agent-skills", "introduction-to-subagents",
                    "building-with-the-claude-api", "claude-code-in-action",
                    "introduction-to-model-context-protocol", "model-context-protocol-advanced-topics"]:
        course_dir = BASE / "courses" / course
        mp4s = list(course_dir.rglob("*.mp4"))
        total += len(mp4s)
        size_mb = sum(f.stat().st_size for f in mp4s) // 1024 // 1024
        print(f"   {course:50s} {len(mp4s):3d} MP4 ({size_mb} MB)")
    print(f"\n   {'TOTAL':50s} {total:3d} MP4")


if __name__ == "__main__":
    download_youtube_videos()
    download_skilljar_videos()
    print_summary()
