#!/usr/bin/env python3
"""Download JW Player videos from Skilljar by intercepting network requests."""
import json
import subprocess
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path("/Volumes/Muse_AI_Core/CCA-Learning")
SESSION_FILE = BASE / "scripts" / "skilljar_session.json"

MISSING = [
    ("287818", "Welcome to the course", "01-api-fundamentals", "02-welcome-to-the-course"),
    ("287756", "Tool functions", "04-tool-use", "23-tool-functions"),
    ("289124", "Quiz on features of Claude", "06-extended-features", "41-quiz-on-features-of-claude"),
    ("289126", "Quiz on Model Context Protocol", "07-mcp", "50-quiz-on-model-context-protocol"),
    ("289130", "Quiz on Agents and Workflows", "08-agents-and-workflows", "58-quiz-on-agents-and-workflows"),
    ("290899", "Final Assessment", "09-assessment", "59-final-assessment"),
]


def main():
    session_data = json.loads(SESSION_FILE.read_text())
    storage_state = session_data.get("storage_state")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=storage_state)

        for i, (lesson_id, name, chapter, slug) in enumerate(MISSING, 1):
            print(f"\n{'='*60}")
            print(f"[{i}/{len(MISSING)}] {name}")
            print(f"{'='*60}")

            video_dir = BASE / "courses" / "building-with-the-claude-api" / chapter / slug / "videos"
            if video_dir.exists() and list(video_dir.glob("*.mp4")):
                print("   ⏭️ Already exists")
                continue

            page = context.new_page()

            # Collect video URLs from network requests
            video_urls = []

            def on_response(response):
                url = response.url
                # JW Player typically streams via .m3u8 or direct .mp4
                if any(ext in url for ext in ['.mp4', '.m3u8', 'manifest', '/deliveries/', 'content.jwplatform']):
                    content_type = response.headers.get('content-type', '')
                    if 'video' in content_type or '.mp4' in url or '.m3u8' in url or 'jwplatform' in url:
                        video_urls.append(url)
                        print(f"   🔗 Found: {url[:100]}")

            page.on("response", on_response)

            url = f"https://anthropic.skilljar.com/claude-with-the-anthropic-api/{lesson_id}"
            print(f"   Loading: {url}")
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(8)  # wait for video player to initialize

            # Try to play the video to trigger loading
            page.evaluate("""() => {
                const video = document.querySelector('video');
                if (video) {
                    video.play().catch(() => {});
                }
                // Try JW Player API
                if (typeof jwplayer !== 'undefined') {
                    try { jwplayer().play(); } catch(e) {}
                }
            }""")
            time.sleep(5)

            # Also check JW Player config for direct URLs
            jw_info = page.evaluate("""() => {
                const data = {sources: [], playlist: []};
                if (typeof jwplayer !== 'undefined') {
                    try {
                        const p = jwplayer();
                        const config = p.getConfig();
                        if (config && config.sources) {
                            config.sources.forEach(s => data.sources.push(s));
                        }
                        const playlist = p.getPlaylist();
                        if (playlist) {
                            playlist.forEach(item => {
                                if (item.sources) item.sources.forEach(s => data.playlist.push(s));
                                if (item.file) data.playlist.push({file: item.file});
                            });
                        }
                        // Try getPlaylistItem
                        const item = p.getPlaylistItem();
                        if (item) {
                            if (item.file) data.sources.push({file: item.file});
                            if (item.sources) item.sources.forEach(s => data.sources.push(s));
                        }
                    } catch(e) {
                        data.error = e.message;
                    }
                }
                return data;
            }""")

            print(f"   JW Player info: {json.dumps(jw_info, indent=2)[:500]}")

            # Combine all found URLs
            all_urls = list(set(video_urls))
            for s in jw_info.get("sources", []) + jw_info.get("playlist", []):
                if isinstance(s, dict) and s.get("file"):
                    all_urls.append(s["file"])

            if all_urls:
                # Prefer .mp4 > .m3u8
                mp4_urls = [u for u in all_urls if '.mp4' in u]
                m3u8_urls = [u for u in all_urls if '.m3u8' in u]
                download_url = mp4_urls[0] if mp4_urls else (m3u8_urls[0] if m3u8_urls else all_urls[0])

                print(f"   Downloading: {download_url[:100]}")
                video_dir.mkdir(parents=True, exist_ok=True)
                out_file = video_dir / f"{name.replace(' ', '_').replace('/', '_')}.mp4"

                # Use yt-dlp for m3u8, curl for direct mp4
                if '.m3u8' in download_url:
                    cmd = ["yt-dlp", "-o", str(out_file), download_url]
                else:
                    cmd = ["curl", "-L", "-o", str(out_file), download_url]

                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                if out_file.exists() and out_file.stat().st_size > 10000:
                    print(f"   ✅ Downloaded: {out_file.name} ({out_file.stat().st_size // 1024 // 1024}MB)")
                else:
                    print(f"   ❌ Download failed or file too small")
                    if out_file.exists():
                        out_file.unlink()
            else:
                print(f"   ❌ No video URLs found")

                # Last resort: check what the page actually contains
                content_type = page.evaluate("""() => {
                    const v = document.querySelector('video');
                    const iframe = document.querySelector('iframe');
                    return {
                        hasVideo: !!v,
                        videoSrc: v ? v.src : null,
                        hasIframe: !!iframe,
                        iframeSrc: iframe ? iframe.src : null,
                        bodyText: document.body.innerText.substring(0, 300),
                    };
                }""")
                print(f"   Page info: {json.dumps(content_type, indent=2)[:400]}")

            page.close()

        time.sleep(2)
        browser.close()

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for _, name, chapter, slug in MISSING:
        vdir = BASE / "courses" / "building-with-the-claude-api" / chapter / slug / "videos"
        mp4s = list(vdir.glob("*.mp4")) if vdir.exists() else []
        status = f"✅ {mp4s[0].name}" if mp4s else "❌ Missing"
        print(f"   {name:45s} {status}")


if __name__ == "__main__":
    main()
