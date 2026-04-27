#!/usr/bin/env python3
"""
Universal Bilingual Subtitle & Visual Guide Pipeline
=====================================================

Follows the claude-code-in-action pattern to generate bilingual (EN + ZH)
subtitle files and frame-by-frame visual guides for any course.

Pipeline stages:
  1. scan       — Discover all SRT + MP4 pairs in a course
  2. templates  — Generate translation template JSON files (EN text, empty ZH)
  3. bilingual  — Generate bilingual SRTs from completed translation JSON files
  4. visual     — Extract video frames and burn bilingual subtitles
  5. all        — Run templates + bilingual + visual in sequence

Usage:
  python3 bilingual_pipeline.py scan    <course_dir>
  python3 bilingual_pipeline.py templates <course_dir>
  python3 bilingual_pipeline.py bilingual <course_dir> [--chapter <name>]
  python3 bilingual_pipeline.py visual   <course_dir> [--chapter <name>]
  python3 bilingual_pipeline.py all      <course_dir> [--chapter <name>]

Translation JSON format (per SRT file):
  {
    "srt_file": "Accessing_the_API_Ju43Csrd.srt",
    "video_file": "Accessing_the_API_Ju43Csrd.mp4",
    "max_valid_entry": 48,
    "entries": {
      "1": {
        "en": "In this video, we are going to examine...",
        "zh_tw": "",
        "zh_cn": ""
      },
      ...
    }
  }
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


# ============================================================
# SRT Parsing
# ============================================================

def parse_srt(srt_path: Path, max_entry: int = 9999) -> list[dict]:
    """Parse SRT file into list of {index, timestamp, text_en, start_sec, end_sec}."""
    content = srt_path.read_text(encoding="utf-8")
    entries = []
    blocks = re.split(r"\n\n+", content.strip())

    seen_texts = set()
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

        text = " ".join(lines[2:]).strip()
        if not text:
            continue

        # Detect duplicate tail entries (common transcription artifact)
        if text in seen_texts and index > 5:
            break
        seen_texts.add(text)

        # Parse timestamp
        time_match = re.match(
            r"(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})",
            lines[1],
        )
        start_sec = end_sec = 0.0
        if time_match:
            g = time_match.groups()
            start_sec = int(g[0]) * 3600 + int(g[1]) * 60 + int(g[2]) + int(g[3]) / 1000
            end_sec = int(g[4]) * 3600 + int(g[5]) * 60 + int(g[6]) + int(g[7]) / 1000

        entries.append({
            "index": index,
            "timestamp": lines[1],
            "text_en": text,
            "start_sec": start_sec,
            "end_sec": end_sec,
            "start_ts": lines[1].split(" --> ")[0].strip() if " --> " in lines[1] else "",
            "end_ts": lines[1].split(" --> ")[1].strip() if " --> " in lines[1] else "",
        })

    return entries


# ============================================================
# Discovery
# ============================================================

def discover_pairs(course_dir: Path) -> list[dict]:
    """Find all SRT + MP4 pairs in a course directory."""
    pairs = []
    for srt_path in sorted(course_dir.rglob("*.srt")):
        # Skip bilingual SRTs
        if "bilingual" in srt_path.name:
            continue
        # Look for matching video
        chapter_dir = srt_path.parent
        video_path = chapter_dir / "videos" / (srt_path.stem + ".mp4")
        if not video_path.exists():
            # Also check if video is in same dir
            video_path = chapter_dir / (srt_path.stem + ".mp4")

        pairs.append({
            "srt_path": srt_path,
            "video_path": video_path if video_path.exists() else None,
            "chapter_dir": chapter_dir,
            "chapter_name": chapter_dir.name,
            "basename": srt_path.stem,
        })
    return pairs


# ============================================================
# Stage 1: Scan
# ============================================================

def cmd_scan(course_dir: Path, **kwargs):
    """List all discovered SRT + MP4 pairs."""
    pairs = discover_pairs(course_dir)
    print(f"Course: {course_dir.name}")
    print(f"Found {len(pairs)} SRT files\n")

    by_chapter = {}
    for p in pairs:
        by_chapter.setdefault(p["chapter_name"], []).append(p)

    for chapter, items in by_chapter.items():
        print(f"  {chapter}/ ({len(items)} videos)")
        for item in items:
            video_status = "OK" if item["video_path"] else "MISSING"
            entries = parse_srt(item["srt_path"])
            print(f"    {item['basename']}.srt ({len(entries)} entries, video: {video_status})")


# ============================================================
# Stage 2: Translation Templates
# ============================================================

def get_translations_dir(course_dir: Path) -> Path:
    return course_dir / "translations"


def cmd_templates(course_dir: Path, chapter_filter: str = None, **kwargs):
    """Generate translation template JSON files."""
    pairs = discover_pairs(course_dir)
    trans_dir = get_translations_dir(course_dir)

    created = 0
    skipped = 0
    for pair in pairs:
        if chapter_filter and pair["chapter_name"] != chapter_filter:
            continue

        chapter_trans_dir = trans_dir / pair["chapter_name"]
        chapter_trans_dir.mkdir(parents=True, exist_ok=True)

        json_path = chapter_trans_dir / (pair["basename"] + ".json")
        if json_path.exists():
            skipped += 1
            continue

        entries = parse_srt(pair["srt_path"])
        template = {
            "srt_file": pair["srt_path"].name,
            "video_file": pair["video_path"].name if pair["video_path"] else None,
            "max_valid_entry": entries[-1]["index"] if entries else 0,
            "entries": {
                str(e["index"]): {
                    "en": e["text_en"],
                    "zh_tw": "",
                    "zh_cn": "",
                }
                for e in entries
            },
        }

        json_path.write_text(
            json.dumps(template, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        created += 1
        print(f"  Created: {json_path.relative_to(course_dir)}")

    print(f"\nTemplates: {created} created, {skipped} already exist")
    print(f"Location: {trans_dir.relative_to(course_dir)}/")
    print("\nNext: Fill in zh_tw and zh_cn fields, then run 'bilingual' stage.")


# ============================================================
# Stage 3: Bilingual SRT Generation
# ============================================================

def load_translations(json_path: Path) -> dict:
    """Load translation JSON and return {index: {zh_tw, zh_cn}} dict."""
    data = json.loads(json_path.read_text(encoding="utf-8"))
    translations = {"zh_tw": {}, "zh_cn": {}, "max_valid_entry": data.get("max_valid_entry", 9999)}
    for idx_str, entry in data.get("entries", {}).items():
        idx = int(idx_str)
        if entry.get("zh_tw"):
            translations["zh_tw"][idx] = entry["zh_tw"]
        if entry.get("zh_cn"):
            translations["zh_cn"][idx] = entry["zh_cn"]
    return translations


def generate_bilingual_srt(entries: list[dict], translations: dict, output_path: Path):
    """Generate bilingual SRT with ZH line below EN line."""
    blocks = []
    for entry in entries:
        idx = entry["index"]
        zh = translations.get(idx, "")
        lines = [str(idx), entry["timestamp"], entry["text_en"]]
        if zh:
            lines.append(zh)
        blocks.append("\n".join(lines))
    output_path.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")


def cmd_bilingual(course_dir: Path, chapter_filter: str = None, **kwargs):
    """Generate bilingual SRT files from translation JSONs."""
    pairs = discover_pairs(course_dir)
    trans_dir = get_translations_dir(course_dir)

    generated = 0
    skipped = 0
    no_trans = 0

    for pair in pairs:
        if chapter_filter and pair["chapter_name"] != chapter_filter:
            continue

        json_path = trans_dir / pair["chapter_name"] / (pair["basename"] + ".json")
        if not json_path.exists():
            no_trans += 1
            continue

        translations = load_translations(json_path)
        max_entry = translations["max_valid_entry"]

        # Check if there are any translations filled in
        if not translations["zh_tw"] and not translations["zh_cn"]:
            skipped += 1
            continue

        entries = parse_srt(pair["srt_path"], max_entry)

        # Output to srt/bilingual/ in the chapter directory
        out_dir = pair["chapter_dir"] / "srt" / "bilingual"
        out_dir.mkdir(parents=True, exist_ok=True)

        if translations["zh_tw"]:
            out_tw = out_dir / (pair["basename"] + "_bilingual.srt")
            generate_bilingual_srt(entries, translations["zh_tw"], out_tw)
            print(f"  Written: {out_tw.relative_to(course_dir)} ({len(entries)} entries)")
            generated += 1

        if translations["zh_cn"]:
            out_cn = out_dir / (pair["basename"] + "_bilingual_zh-CN.srt")
            generate_bilingual_srt(entries, translations["zh_cn"], out_cn)
            print(f"  Written: {out_cn.relative_to(course_dir)} ({len(entries)} entries)")
            generated += 1

    print(f"\nBilingual SRTs: {generated} generated, {skipped} skipped (empty translations), {no_trans} no template")


# ============================================================
# Stage 4: Visual Guide Generation
# ============================================================

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
    """Extract a single frame at the given time."""
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
        return False


def burn_subtitles(frame_path: Path, text_en: str, text_zh: str, output_path: Path):
    """Burn bilingual subtitles onto a frame using Pillow."""
    from PIL import Image, ImageDraw, ImageFont

    img = Image.open(frame_path)
    w, h = img.size

    # Taller overlay for two lines of subtitles
    overlay_h = 140 if text_zh else 80
    overlay = Image.new("RGBA", (w, overlay_h), (0, 0, 0, 180))
    img = img.convert("RGBA")
    img.paste(overlay, (0, h - overlay_h), overlay)

    draw = ImageDraw.Draw(img)

    try:
        font_zh = ImageFont.truetype("/System/Library/Fonts/STHeiti Light.ttc", 30)
    except Exception:
        font_zh = ImageFont.load_default()
    try:
        font_en = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
    except Exception:
        font_en = ImageFont.load_default()

    if text_zh:
        # Chinese on top line, English below
        bbox_zh = draw.textbbox((0, 0), text_zh, font=font_zh)
        tw_zh = bbox_zh[2] - bbox_zh[0]
        x_zh = (w - tw_zh) // 2
        y_zh = h - overlay_h + 15
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            draw.text((x_zh + dx, y_zh + dy), text_zh, font=font_zh, fill=(0, 0, 0, 255))
        draw.text((x_zh, y_zh), text_zh, font=font_zh, fill=(255, 255, 255, 255))

        bbox_en = draw.textbbox((0, 0), text_en, font=font_en)
        tw_en = bbox_en[2] - bbox_en[0]
        x_en = (w - tw_en) // 2
        y_en = h - overlay_h + 80
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            draw.text((x_en + dx, y_en + dy), text_en, font=font_en, fill=(0, 0, 0, 255))
        draw.text((x_en, y_en), text_en, font=font_en, fill=(204, 204, 204, 255))
    else:
        bbox_en = draw.textbbox((0, 0), text_en, font=font_en)
        tw_en = bbox_en[2] - bbox_en[0]
        x_en = (w - tw_en) // 2
        y_en = h - overlay_h + 25
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            draw.text((x_en + dx, y_en + dy), text_en, font=font_en, fill=(0, 0, 0, 255))
        draw.text((x_en, y_en), text_en, font=font_en, fill=(204, 204, 204, 255))

    img.convert("RGB").save(output_path, "JPEG", quality=92)


def generate_markdown(entries: list[dict], frames_dir: Path, output_path: Path,
                      title: str, course_name: str, chapter_name: str):
    """Generate a markdown file embedding all frames with subtitles."""
    lines = [
        f"# {title} — 影片逐幀學習指南",
        "",
        "| 項目 | 內容 |",
        "|------|------|",
        f"| 課程 | {course_name} / {chapter_name} |",
        f"| 影片 | {title} |",
        f"| 字幕數 | {len(entries)} 段 |",
        "| 格式 | 每段字幕一張截圖 + 雙語字幕（英/中） |",
        "",
        "---",
        "",
    ]

    for entry in entries:
        idx = entry["index"]
        ts = entry.get("start_ts", "").split(",")[0]
        frame_file = f"frame_{idx:03d}.jpg"
        zh = entry.get("text_zh", "")

        lines.append(f"### [{ts}] 第 {idx} 段")
        lines.append("")
        lines.append(f"![frame {idx}](./frames/{frame_file})")
        lines.append("")
        lines.append(f"> **EN:** {entry['text_en']}")
        if zh:
            lines.append(f">")
            lines.append(f"> **ZH:** {zh}")
        lines.append("")
        lines.append("---")
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")


def cmd_visual(course_dir: Path, chapter_filter: str = None, **kwargs):
    """Generate visual study guides with frame extraction."""
    pairs = discover_pairs(course_dir)
    trans_dir = get_translations_dir(course_dir)

    processed = 0
    skipped = 0

    for pair in pairs:
        if chapter_filter and pair["chapter_name"] != chapter_filter:
            continue
        if not pair["video_path"]:
            print(f"  SKIP (no video): {pair['basename']}")
            skipped += 1
            continue

        # Load translations if available
        zh_translations = {}
        json_path = trans_dir / pair["chapter_name"] / (pair["basename"] + ".json")
        max_entry = 9999
        if json_path.exists():
            trans_data = load_translations(json_path)
            zh_translations = trans_data["zh_tw"]  # Use zh-TW for visual guides
            max_entry = trans_data["max_valid_entry"]

        entries = parse_srt(pair["srt_path"], max_entry)
        for e in entries:
            e["text_zh"] = zh_translations.get(e["index"], "")

        # Output dirs
        vg_dir = pair["chapter_dir"] / "visual-guides" / pair["basename"]
        frames_dir = vg_dir / "frames"
        raw_dir = frames_dir / "raw"
        frames_dir.mkdir(parents=True, exist_ok=True)
        raw_dir.mkdir(exist_ok=True)

        print(f"\n{'='*60}")
        print(f"Processing: {pair['chapter_name']}/{pair['basename']}")
        print(f"{'='*60}")

        video_duration = get_video_duration(pair["video_path"])
        print(f"Video duration: {video_duration:.1f}s, {len(entries)} subtitle entries")

        # Extract raw frames
        for entry in entries:
            idx = entry["index"]
            mid_time = (entry["start_sec"] + entry["end_sec"]) / 2
            raw_frame = raw_dir / f"frame_{idx:03d}.jpg"

            if not raw_frame.exists():
                if extract_frame(pair["video_path"], mid_time, raw_frame, video_duration):
                    pass  # silent success
                else:
                    print(f"  WARNING: Failed frame {idx} at {mid_time:.1f}s")

        # Burn subtitles
        for entry in entries:
            idx = entry["index"]
            raw_frame = raw_dir / f"frame_{idx:03d}.jpg"
            final_frame = frames_dir / f"frame_{idx:03d}.jpg"

            if not final_frame.exists() and raw_frame.exists():
                burn_subtitles(raw_frame, entry["text_en"], entry.get("text_zh", ""), final_frame)

        # Generate markdown
        title = pair["basename"].rsplit("_", 1)[0].replace("_", " ")
        md_path = vg_dir / f"{pair['basename']}-visual.md"
        generate_markdown(entries, frames_dir, md_path,
                          title=title, course_name=course_dir.name,
                          chapter_name=pair["chapter_name"])

        frame_count = len(list(frames_dir.glob("frame_*.jpg")))
        has_zh = "bilingual" if zh_translations else "EN only"
        print(f"  Done: {frame_count} frames ({has_zh}), markdown: {md_path.name}")
        processed += 1

    print(f"\n{'='*60}")
    print(f"Visual guides: {processed} processed, {skipped} skipped")


# ============================================================
# Stage 5: All
# ============================================================

def cmd_all(course_dir: Path, **kwargs):
    """Run all stages in sequence."""
    print("=" * 60)
    print("STAGE 1: Generate translation templates")
    print("=" * 60)
    cmd_templates(course_dir, **kwargs)

    print("\n" + "=" * 60)
    print("STAGE 2: Generate bilingual SRTs")
    print("=" * 60)
    cmd_bilingual(course_dir, **kwargs)

    print("\n" + "=" * 60)
    print("STAGE 3: Generate visual guides")
    print("=" * 60)
    cmd_visual(course_dir, **kwargs)


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Universal Bilingual Subtitle & Visual Guide Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "stage",
        choices=["scan", "templates", "bilingual", "visual", "all"],
        help="Pipeline stage to run",
    )
    parser.add_argument(
        "course_dir",
        type=Path,
        help="Path to course directory",
    )
    parser.add_argument(
        "--chapter",
        type=str,
        default=None,
        help="Filter to a specific chapter directory name",
    )

    args = parser.parse_args()

    course_dir = args.course_dir.resolve()
    if not course_dir.is_dir():
        print(f"ERROR: Not a directory: {course_dir}")
        sys.exit(1)

    stage_fn = {
        "scan": cmd_scan,
        "templates": cmd_templates,
        "bilingual": cmd_bilingual,
        "visual": cmd_visual,
        "all": cmd_all,
    }

    stage_fn[args.stage](course_dir, chapter_filter=args.chapter)


if __name__ == "__main__":
    main()
