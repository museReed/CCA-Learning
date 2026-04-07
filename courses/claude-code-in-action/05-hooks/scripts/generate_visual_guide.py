#!/usr/bin/env python3
"""
Generate a visual study guide from video + SRT.
- Extracts one frame per subtitle entry (at midpoint)
- Overlays bilingual subtitles (EN + ZH) on each frame
- Outputs a markdown file with all frames embedded

Supports all ch05-hooks units. Usage:
  python3 generate_visual_guide.py                    # process all units
  python3 generate_visual_guide.py --unit 15-defining-hooks
  python3 generate_visual_guide.py --unit 16-implementing-a-hook
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

# Add scripts dir to path so we can import from generate_bilingual_srt
sys.path.insert(0, str(Path(__file__).parent))

from generate_bilingual_srt import (
    INTRODUCING_HOOKS_ZH,
    DEFINING_HOOKS_ZH,
    IMPLEMENTING_HOOK_ZH,
    USEFUL_HOOKS_ZH,
)

# --- Config ---
BASE_DIR = Path("/Volumes/Muse_AI_Core/CCA-Learning/courses/claude-code-in-action/05-hooks")

VIDEO_CONFIG = [
    {
        "unit_dir": "14-introducing-hooks",
        "video": "Introducing_hooks_3uGhMBFx.mp4",
        "srt": "Introducing_hooks_3uGhMBFx.srt",
        "max_valid_entry": 58,
        "zh_translations": INTRODUCING_HOOKS_ZH,
        "md_filename": "14-introducing-hooks-visual.md",
        "title": "Introducing Hooks — 介紹 Hooks",
        "lesson_num": 14,
    },
    {
        "unit_dir": "15-defining-hooks",
        "video": "Defining_hooks_qzgBYFlx.mp4",
        "srt": "Defining_hooks_qzgBYFlx.srt",
        "max_valid_entry": 48,
        "zh_translations": DEFINING_HOOKS_ZH,
        "md_filename": "15-defining-hooks-visual.md",
        "title": "Defining Hooks — 定義 Hooks",
        "lesson_num": 15,
    },
    {
        "unit_dir": "16-implementing-a-hook",
        "video": "Implementing_a_hook_WpOJxKsp.mp4",
        "srt": "Implementing_a_hook_WpOJxKsp.srt",
        "max_valid_entry": 70,
        "zh_translations": IMPLEMENTING_HOOK_ZH,
        "md_filename": "16-implementing-a-hook-visual.md",
        "title": "Implementing a Hook — 實作 Hook",
        "lesson_num": 16,
    },
    {
        "unit_dir": "18-useful-hooks",
        "video": "Useful_hooks_fXIRG62r.mp4",
        "srt": "Useful_hooks_fXIRG62r.srt",
        "max_valid_entry": 163,
        "zh_translations": USEFUL_HOOKS_ZH,
        "md_filename": "18-useful-hooks-visual.md",
        "title": "Useful Hooks — 實用 Hooks",
        "lesson_num": 18,
    },
]


def parse_srt(srt_path: Path, max_valid_entry: int, zh_translations: dict) -> list[dict]:
    """Parse SRT file into list of {index, start, end, start_sec, end_sec, text}."""
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

        if index > max_valid_entry:
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

        # Skip empty text
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
    """Get video duration in seconds using ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "csv=p=0",
        str(video_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(result.stdout.strip())


def extract_frame(video_path: Path, time_sec: float, output_path: Path,
                  video_duration: float = 0) -> bool:
    """Extract a single frame at the given time. Returns False if beyond video."""
    # Clamp to 0.5s before end if beyond duration
    if video_duration > 0 and time_sec >= video_duration:
        time_sec = video_duration - 0.5

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
        print(f"    WARNING: Failed to extract frame at {time_sec:.1f}s, skipping")
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
        # Black outline
        for dx, dy in [(-1,-1),(-1,1),(1,-1),(1,1)]:
            draw.text((x_zh+dx, y_zh+dy), text_zh, font=font_zh, fill=(0,0,0,255))
        draw.text((x_zh, y_zh), text_zh, font=font_zh, fill=(255,255,255,255))

    # Draw English text (bottom line), centered
    bbox_en = draw.textbbox((0, 0), text_en, font=font_en)
    tw_en = bbox_en[2] - bbox_en[0]
    x_en = (w - tw_en) // 2
    y_en = h - 55
    for dx, dy in [(-1,-1),(-1,1),(1,-1),(1,1)]:
        draw.text((x_en+dx, y_en+dy), text_en, font=font_en, fill=(0,0,0,255))
    draw.text((x_en, y_en), text_en, font=font_en, fill=(204,204,204,255))

    # Save as RGB JPEG
    img.convert("RGB").save(output_path, "JPEG", quality=92)


def generate_markdown(entries: list[dict], frames_dir: Path, output_path: Path,
                      title: str, lesson_num: int):
    """Generate a markdown file embedding all frames with subtitles."""
    lines = [
        f"# {title} — 影片逐幀學習指南",
        "",
        "| 項目 | 內容 |",
        "|------|------|",
        f"| 課程 | claude-code-in-action / 05-hooks / Lesson {lesson_num} |",
        f"| 影片 | {title.split(' — ')[0]} |",
        f"| 字幕數 | {len(entries)} 段 |",
        "| 格式 | 每段字幕一張截圖 + 雙語字幕（英/中） |",
        "",
        "---",
        "",
    ]

    for entry in entries:
        idx = entry["index"]
        ts = entry["start_ts"].split(",")[0]  # Remove milliseconds
        frame_file = f"frame_{idx:03d}.jpg"

        lines.append(f"### [{ts}] 第 {idx} 段")
        lines.append("")
        lines.append(f"![frame {idx}](./frames/{frame_file})")
        lines.append("")
        # Also add text below image for searchability / accessibility
        lines.append(f"> **EN:** {entry['text_en']}")
        lines.append(f">")
        lines.append(f"> **ZH:** {entry['text_zh']}")
        lines.append("")
        lines.append("---")
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Markdown written to {output_path}")


def process_unit(config: dict):
    """Process a single unit: extract frames, burn subtitles, generate markdown."""
    unit_dir = BASE_DIR / config["unit_dir"]
    video_path = unit_dir / "videos" / config["video"]
    srt_path = unit_dir / "srt" / config["srt"]
    out_dir = unit_dir / "visual-guide"
    frames_dir = out_dir / "frames"
    raw_dir = frames_dir / "raw"

    print(f"\n{'='*60}")
    print(f"Processing: {config['unit_dir']}")
    print(f"{'='*60}")

    # Validate inputs
    if not video_path.exists():
        print(f"  ERROR: Video not found: {video_path}")
        return False
    if not srt_path.exists():
        print(f"  ERROR: SRT not found: {srt_path}")
        return False

    # Setup directories
    frames_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(exist_ok=True)

    # Get video duration for boundary checking
    video_duration = get_video_duration(video_path)
    print(f"Video duration: {video_duration:.1f}s")

    # Parse SRT
    print("Parsing SRT...")
    entries = parse_srt(srt_path, config["max_valid_entry"], config["zh_translations"])
    print(f"  Found {len(entries)} valid subtitle entries")

    # Extract frames
    print("Extracting frames...")
    for entry in entries:
        idx = entry["index"]
        mid_time = (entry["start_sec"] + entry["end_sec"]) / 2
        raw_frame = raw_dir / f"frame_{idx:03d}.jpg"

        if not raw_frame.exists():
            extract_frame(video_path, mid_time, raw_frame, video_duration)
            print(f"  [{idx}/{len(entries)}] Extracted at {mid_time:.1f}s")
        else:
            print(f"  [{idx}/{len(entries)}] Already exists, skipping")

    # Burn bilingual subtitles
    print("Burning bilingual subtitles...")
    for entry in entries:
        idx = entry["index"]
        raw_frame = raw_dir / f"frame_{idx:03d}.jpg"
        final_frame = frames_dir / f"frame_{idx:03d}.jpg"

        if not final_frame.exists():
            burn_subtitles(raw_frame, entry["text_en"], entry["text_zh"], final_frame)
            print(f"  [{idx}/{len(entries)}] Subtitled")
        else:
            print(f"  [{idx}/{len(entries)}] Already exists, skipping")

    # Generate markdown
    print("Generating markdown...")
    md_path = out_dir / config["md_filename"]
    generate_markdown(entries, frames_dir, md_path,
                      title=config["title"], lesson_num=config["lesson_num"])

    print(f"\nDone! {len(entries)} frames with bilingual subtitles.")
    print(f"Output: {md_path}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate visual study guides for ch05-hooks units"
    )
    parser.add_argument(
        "--unit",
        type=str,
        help="Process a specific unit (e.g., '15-defining-hooks'). "
             "If not specified, processes all units.",
    )
    args = parser.parse_args()

    if args.unit:
        # Find matching config
        matched = [c for c in VIDEO_CONFIG if c["unit_dir"] == args.unit]
        if not matched:
            valid = [c["unit_dir"] for c in VIDEO_CONFIG]
            print(f"ERROR: Unknown unit '{args.unit}'")
            print(f"Valid units: {', '.join(valid)}")
            sys.exit(1)
        configs = matched
    else:
        configs = VIDEO_CONFIG

    success_count = 0
    for config in configs:
        if process_unit(config):
            success_count += 1

    print(f"\n{'='*60}")
    print(f"Completed: {success_count}/{len(configs)} units processed successfully.")


if __name__ == "__main__":
    main()
