#!/usr/bin/env python3
"""
Generate visual study guides from video + SRT for Chapter 04-integrations.
- Extracts one frame per subtitle entry (at midpoint)
- Overlays bilingual subtitles (EN + ZH) on each frame
- Outputs a markdown file with all frames embedded

Processes both videos in 04-integrations:
  - 12-mcp-servers-with-claude-code (40 entries)
  - 13-github-integration (69 entries)
"""

import re
import subprocess
from pathlib import Path

# --- Config ---
BASE_DIR = Path("/Volumes/Muse_AI_Core/CCA-Learning/courses/claude-code-in-action/04-integrations")

# Import zh-TW translations from bilingual SRT script
import sys
sys.path.insert(0, str(BASE_DIR / "scripts"))
from generate_bilingual_srt import (
    MCP_SERVERS_ZH,
    GITHUB_INTEGRATION_ZH,
)

# Video configurations: (unit_dir, srt_filename, video_filename, zh_translations, max_valid_entry, title)
VIDEO_CONFIG = [
    (
        "12-mcp-servers-with-claude-code",
        "MCP_servers_with_Claude_Code_EkzVe83z.srt",
        "MCP_servers_with_Claude_Code_EkzVe83z.mp4",
        MCP_SERVERS_ZH,
        40,
        "MCP Servers with Claude Code — 使用 MCP Server 擴展 Claude Code",
    ),
    (
        "13-github-integration",
        "Github_integration_ZzNXo5m0.srt",
        "Github_integration_ZzNXo5m0.mp4",
        GITHUB_INTEGRATION_ZH,
        69,
        "GitHub Integration — Claude Code GitHub 整合",
    ),
]


def parse_srt(srt_path: Path, zh_translations: dict, max_entry: int) -> list[dict]:
    """Parse SRT file into list of {index, start_sec, end_sec, start_ts, end_ts, text_en, text_zh}."""
    content = srt_path.read_text(encoding="utf-8")
    entries = []
    blocks = re.split(r"\n\n+", content.strip())

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue

        try:
            index = int(lines[0])
        except ValueError:
            continue

        if index > max_entry:
            break

        time_match = re.match(
            r"(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})",
            lines[1],
        )
        if not time_match:
            continue

        g = time_match.groups()
        start_sec = int(g[0]) * 3600 + int(g[1]) * 60 + int(g[2]) + int(g[3]) / 1000
        end_sec = int(g[4]) * 3600 + int(g[5]) * 60 + int(g[6]) + int(g[7]) / 1000
        text = " ".join(lines[2:]).strip()

        if not text:
            continue

        entries.append({
            "index": index,
            "start_sec": start_sec,
            "end_sec": end_sec,
            "start_ts": lines[1].split(" --> ")[0].strip(),
            "end_ts": lines[1].split(" --> ")[1].strip(),
            "text_en": text,
            "text_zh": zh_translations.get(index, ""),
        })

    return entries


def get_video_duration(video_path: Path) -> float:
    """Get video duration in seconds."""
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(video_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(result.stdout.strip())


def extract_frame(video_path: Path, time_sec: float, output_path: Path) -> bool:
    """Extract a single frame at the given time. Returns True if successful."""
    cmd = [
        "ffmpeg", "-y", "-ss", f"{time_sec:.3f}",
        "-i", str(video_path),
        "-frames:v", "1",
        "-q:v", "2",
        str(output_path),
    ]
    try:
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def burn_subtitles(frame_path: Path, text_en: str, text_zh: str, output_path: Path):
    """Burn bilingual subtitles onto a frame using Pillow."""
    from PIL import Image, ImageDraw, ImageFont

    img = Image.open(frame_path)
    w, h = img.size

    # Semi-transparent black bar at bottom
    overlay = Image.new("RGBA", (w, 120), (0, 0, 0, 180))
    img = img.convert("RGBA")
    img.paste(overlay, (0, h - 120), overlay)

    draw = ImageDraw.Draw(img)

    # Load fonts
    try:
        font_zh = ImageFont.truetype("/System/Library/Fonts/STHeiti Light.ttc", 28)
    except Exception:
        font_zh = ImageFont.load_default()
    try:
        font_en = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
    except Exception:
        font_en = ImageFont.load_default()

    # Draw Chinese text (top line of subtitle area), centered
    if text_zh:
        bbox_zh = draw.textbbox((0, 0), text_zh, font=font_zh)
        tw_zh = bbox_zh[2] - bbox_zh[0]
        x_zh = (w - tw_zh) // 2
        y_zh = h - 110
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            draw.text((x_zh + dx, y_zh + dy), text_zh, font=font_zh, fill=(0, 0, 0, 255))
        draw.text((x_zh, y_zh), text_zh, font=font_zh, fill=(255, 255, 255, 255))

    # Draw English text (bottom line), centered
    bbox_en = draw.textbbox((0, 0), text_en, font=font_en)
    tw_en = bbox_en[2] - bbox_en[0]
    x_en = (w - tw_en) // 2
    y_en = h - 55
    for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        draw.text((x_en + dx, y_en + dy), text_en, font=font_en, fill=(0, 0, 0, 255))
    draw.text((x_en, y_en), text_en, font=font_en, fill=(204, 204, 204, 255))

    # Save as RGB JPEG
    img.convert("RGB").save(output_path, "JPEG", quality=92)


def generate_markdown(entries: list[dict], unit_dir: str, title: str, output_path: Path):
    """Generate a markdown file embedding all frames with subtitles."""
    lines = [
        f"# {title} — 影片逐幀學習指南",
        "",
        "| 項目 | 內容 |",
        "|------|------|",
        f"| 課程 | claude-code-in-action / 04-integrations / {unit_dir} |",
        f"| 影片 | {title.split(' — ')[0]} |",
        f"| 字幕數 | {len(entries)} 段 |",
        "| 格式 | 每段字幕一張截圖 + 雙語字幕（英/中） |",
        "",
        "---",
        "",
    ]

    for entry in entries:
        idx = entry["index"]
        ts = entry["start_ts"].split(",")[0]
        frame_file = f"frame_{idx:03d}.jpg"

        lines.append(f"### [{ts}] 第 {idx} 段")
        lines.append("")
        lines.append(f"![frame {idx}](./frames/{frame_file})")
        lines.append("")
        lines.append(f"> **EN:** {entry['text_en']}")
        lines.append(f">")
        lines.append(f"> **ZH:** {entry['text_zh']}")
        lines.append("")
        lines.append("---")
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Markdown: {output_path}")


def process_video(unit_dir, srt_filename, video_filename, zh_translations, max_entry, title):
    """Process a single video: extract frames, burn subtitles, generate markdown."""
    unit_path = BASE_DIR / unit_dir
    srt_path = unit_path / "srt" / srt_filename
    video_path = unit_path / "videos" / video_filename

    if not video_path.exists():
        print(f"  SKIP: {video_path} not found")
        return

    if not srt_path.exists():
        print(f"  SKIP: {srt_path} not found")
        return

    out_dir = unit_path / "visual-guide"
    frames_dir = out_dir / "frames"
    raw_dir = frames_dir / "raw"
    out_dir.mkdir(parents=True, exist_ok=True)
    frames_dir.mkdir(exist_ok=True)
    raw_dir.mkdir(exist_ok=True)

    # Parse SRT
    entries = parse_srt(srt_path, zh_translations, max_entry)
    print(f"  Parsed {len(entries)} subtitle entries")

    # Get video duration to handle edge cases
    video_duration = get_video_duration(video_path)
    print(f"  Video duration: {video_duration:.1f}s")

    # Track successfully extracted frames
    successful_entries = []

    # Extract frames
    for entry in entries:
        idx = entry["index"]
        mid_time = (entry["start_sec"] + entry["end_sec"]) / 2
        raw_frame = raw_dir / f"frame_{idx:03d}.jpg"

        if not raw_frame.exists():
            # Skip if frame time is beyond video duration
            if mid_time > video_duration:
                print(f"    [{idx}/{len(entries)}] SKIP: frame time {mid_time:.1f}s > video duration {video_duration:.1f}s")
                continue

            success = extract_frame(video_path, mid_time, raw_frame)
            if success:
                print(f"    [{idx}/{len(entries)}] Extracted at {mid_time:.1f}s")
            else:
                print(f"    [{idx}/{len(entries)}] FAILED to extract at {mid_time:.1f}s")
                continue

        successful_entries.append(entry)

    # Burn bilingual subtitles
    for entry in successful_entries:
        idx = entry["index"]
        raw_frame = raw_dir / f"frame_{idx:03d}.jpg"
        final_frame = frames_dir / f"frame_{idx:03d}.jpg"

        if not final_frame.exists():
            burn_subtitles(raw_frame, entry["text_en"], entry["text_zh"], final_frame)
            print(f"    [{idx}/{len(successful_entries)}] Subtitled")

    # Generate markdown with successful entries only
    slug = unit_dir.split("-", 1)[1] if "-" in unit_dir else unit_dir
    md_path = out_dir / f"{unit_dir}-visual.md"
    generate_markdown(successful_entries, unit_dir, title, md_path)

    print(f"  Done: {len(successful_entries)} frames successfully processed")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate visual guides for 04-integrations")
    parser.add_argument("--unit", help="Process specific unit (e.g., 12-mcp-servers-with-claude-code)")
    args = parser.parse_args()

    for unit_dir, srt_fn, video_fn, zh, max_entry, title in VIDEO_CONFIG:
        if args.unit and unit_dir != args.unit:
            continue

        print(f"\n{'='*60}")
        print(f"Processing: {unit_dir} — {title}")
        print(f"{'='*60}")
        process_video(unit_dir, srt_fn, video_fn, zh, max_entry, title)

    print("\nAll done!")


if __name__ == "__main__":
    main()
