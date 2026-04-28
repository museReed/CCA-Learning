#!/usr/bin/env python3
"""
Bilingual pipeline for 3 new courses (YouTube-sourced SRTs).

YouTube auto-captions use progressive-reveal format with 10ms ghost entries.
This script:
  1. preprocess  — Convert YouTube SRTs → clean SRTs (merged sentences)
  2. templates   — Generate translation template JSONs
  3. bilingual   — Generate bilingual SRTs from filled translations
  4. visual      — Extract frames + burn bilingual subtitles

Usage:
  python3 new_course_bilingual.py preprocess
  python3 new_course_bilingual.py templates
  python3 new_course_bilingual.py bilingual
  python3 new_course_bilingual.py visual
  python3 new_course_bilingual.py all
"""

import json
import re
import subprocess
import sys
from pathlib import Path

BASE = Path("/Volumes/Muse_AI_Core/CCA-Learning/courses")

COURSES = [
    "claude-101",
    "introduction-to-agent-skills",
    "introduction-to-subagents",
]


# ============================================================
# SRT Parsing & Preprocessing
# ============================================================

def parse_youtube_srt(srt_path: Path) -> list[dict]:
    """Parse YouTube auto-generated SRT (progressive-reveal format)."""
    content = srt_path.read_text(encoding="utf-8")
    entries = []
    blocks = re.split(r"\n\n+", content.strip())

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 2:
            continue
        try:
            index = int(lines[0])
        except ValueError:
            continue

        # Parse timestamp
        ts_line = lines[1] if len(lines) > 1 else ""
        time_match = re.match(
            r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})",
            ts_line,
        )
        if not time_match:
            continue

        start_ts, end_ts = time_match.group(1), time_match.group(2)
        text = "\n".join(lines[2:]).strip() if len(lines) > 2 else ""

        # Parse timestamps to seconds for duration check
        start_sec = ts_to_sec(start_ts)
        end_sec = ts_to_sec(end_ts)

        entries.append({
            "index": index,
            "start_ts": start_ts,
            "end_ts": end_ts,
            "start_sec": start_sec,
            "end_sec": end_sec,
            "text": text,
        })
    return entries


def ts_to_sec(ts: str) -> float:
    """Convert SRT timestamp to seconds."""
    m = re.match(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})", ts)
    if not m:
        return 0.0
    return int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3]) + int(m[4]) / 1000


def sec_to_ts(sec: float) -> str:
    """Convert seconds to SRT timestamp."""
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int((sec % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def clean_youtube_srt(entries: list[dict]) -> list[dict]:
    """Convert progressive-reveal YouTube SRT to clean sentence-based SRT.

    Strategy:
    1. Skip ghost entries (duration <= 20ms)
    2. Extract last line from multi-line progressive entries
    3. Merge consecutive fragments into complete sentences
    4. Clean [music] and other noise tags
    """
    # Step 1: Filter ghost entries
    real = [e for e in entries if (e["end_sec"] - e["start_sec"]) > 0.05]

    # Step 2: Extract new text from each entry
    # In progressive reveal, multi-line entries show: previous_text\nnew_text
    fragments = []
    for e in real:
        text_lines = e["text"].split("\n")
        # Take the last line (new text); if single line, take all
        new_text = text_lines[-1].strip() if text_lines else ""
        if not new_text:
            # Paragraph break / empty entry
            continue

        # Clean [music] tags
        new_text = re.sub(r'\[music\]\s*', '', new_text, flags=re.IGNORECASE).strip()
        new_text = re.sub(r'\[Music\]\s*', '', new_text).strip()
        if not new_text:
            continue

        fragments.append({
            "start_ts": e["start_ts"],
            "end_ts": e["end_ts"],
            "start_sec": e["start_sec"],
            "end_sec": e["end_sec"],
            "text": new_text,
        })

    # Step 3: Merge fragments into sentences
    merged = []
    current = None

    for frag in fragments:
        if current is None:
            current = {
                "start_ts": frag["start_ts"],
                "end_ts": frag["end_ts"],
                "start_sec": frag["start_sec"],
                "end_sec": frag["end_sec"],
                "text": frag["text"],
            }
            continue

        # Merge if fragment continues the current text (no sentence-ending punctuation)
        combined_text = current["text"] + " " + frag["text"]
        time_gap = frag["start_sec"] - current["end_sec"]

        # Decide whether to merge or start new entry
        # Merge if: current doesn't end with sentence-ending punct AND gap < 2s
        ends_sentence = bool(re.search(r'[.!?]$', current["text"]))
        too_long = len(combined_text) > 120

        if ends_sentence or too_long or time_gap > 2.0:
            merged.append(current)
            current = {
                "start_ts": frag["start_ts"],
                "end_ts": frag["end_ts"],
                "start_sec": frag["start_sec"],
                "end_sec": frag["end_sec"],
                "text": frag["text"],
            }
        else:
            current["text"] = combined_text
            current["end_ts"] = frag["end_ts"]
            current["end_sec"] = frag["end_sec"]

    if current:
        merged.append(current)

    # Step 4: Re-index
    for i, entry in enumerate(merged, 1):
        entry["index"] = i

    return merged


def write_clean_srt(entries: list[dict], output_path: Path):
    """Write clean SRT file."""
    blocks = []
    for e in entries:
        blocks.append(f"{e['index']}\n{e['start_ts']} --> {e['end_ts']}\n{e['text']}")
    output_path.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")


# ============================================================
# Course Discovery
# ============================================================

def discover_lessons(course_name: str) -> list[dict]:
    """Discover all lessons with SRTs in a course."""
    course_dir = BASE / course_name / "01-full-course"
    lessons = []
    for lesson_dir in sorted(course_dir.iterdir()):
        if not lesson_dir.is_dir() or not lesson_dir.name[0].isdigit():
            continue
        srt_dir = lesson_dir / "srt"
        if not srt_dir.exists():
            continue

        # Find .en.srt (YouTube) or .srt
        srts = list(srt_dir.glob("*.en.srt"))
        if not srts:
            srts = [s for s in srt_dir.glob("*.srt") if "bilingual" not in s.name]
        if not srts:
            continue

        srt_path = srts[0]
        # Find matching video
        video_dir = lesson_dir / "videos"
        # YouTube SRT: "foo.en.srt" → video: "foo.mp4"
        video_stem = srt_path.stem.replace(".en", "")
        video_path = video_dir / (video_stem + ".mp4") if video_dir.exists() else None
        if video_path and not video_path.exists():
            # Try glob
            mp4s = list(video_dir.glob("*.mp4")) if video_dir.exists() else []
            video_path = mp4s[0] if mp4s else None

        lessons.append({
            "course": course_name,
            "lesson_dir": lesson_dir,
            "lesson_name": lesson_dir.name,
            "srt_path": srt_path,
            "video_path": video_path,
            "video_stem": video_stem,
        })
    return lessons


# ============================================================
# Stage 1: Preprocess
# ============================================================

def cmd_preprocess():
    """Convert YouTube SRTs to clean format."""
    total = 0
    for course in COURSES:
        lessons = discover_lessons(course)
        print(f"\n{'='*60}")
        print(f"  {course} ({len(lessons)} SRTs)")
        print(f"{'='*60}")

        for lesson in lessons:
            raw_entries = parse_youtube_srt(lesson["srt_path"])
            clean = clean_youtube_srt(raw_entries)

            # Write clean SRT (replace .en.srt → .srt)
            clean_name = lesson["video_stem"] + ".srt"
            clean_path = lesson["srt_path"].parent / clean_name
            write_clean_srt(clean, clean_path)

            total += 1
            print(f"  {lesson['lesson_name']}: {len(raw_entries)} → {len(clean)} entries ({clean_path.name})")

    print(f"\nTotal: {total} SRTs preprocessed")


# ============================================================
# Stage 2: Templates
# ============================================================

def cmd_templates():
    """Generate translation template JSONs."""
    total = 0
    for course in COURSES:
        course_dir = BASE / course
        trans_dir = course_dir / "translations" / "01-full-course"
        trans_dir.mkdir(parents=True, exist_ok=True)

        lessons = discover_lessons(course)
        print(f"\n{course} ({len(lessons)} lessons)")

        for lesson in lessons:
            # Use clean SRT if available
            clean_srt = lesson["srt_path"].parent / (lesson["video_stem"] + ".srt")
            if not clean_srt.exists():
                print(f"  ⚠️ {lesson['lesson_name']} — no clean SRT, run preprocess first")
                continue

            entries = parse_clean_srt(clean_srt)
            template = {
                "srt_file": clean_srt.name,
                "video_file": lesson["video_path"].name if lesson["video_path"] else None,
                "lesson": lesson["lesson_name"],
                "max_valid_entry": entries[-1]["index"] if entries else 0,
                "entries": {
                    str(e["index"]): {
                        "en": e["text"],
                        "zh_tw": "",
                        "zh_cn": "",
                    }
                    for e in entries
                },
            }

            json_path = trans_dir / (lesson["lesson_name"] + ".json")
            json_path.write_text(
                json.dumps(template, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            total += 1
            print(f"  ✅ {lesson['lesson_name']} — {len(entries)} entries → {json_path.name}")

    print(f"\nTotal: {total} templates created")


def parse_clean_srt(srt_path: Path) -> list[dict]:
    """Parse a clean (non-YouTube-progressive) SRT file."""
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
        ts_match = re.match(
            r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})",
            lines[1],
        )
        if not ts_match:
            continue
        text = " ".join(lines[2:]).strip()
        if not text:
            continue
        entries.append({
            "index": index,
            "start_ts": ts_match.group(1),
            "end_ts": ts_match.group(2),
            "start_sec": ts_to_sec(ts_match.group(1)),
            "end_sec": ts_to_sec(ts_match.group(2)),
            "text": text,
            "timestamp": lines[1],
        })
    return entries


# ============================================================
# Stage 3: Bilingual SRT
# ============================================================

def cmd_bilingual():
    """Generate bilingual SRTs from filled translation JSONs."""
    total = 0
    for course in COURSES:
        course_dir = BASE / course
        trans_dir = course_dir / "translations" / "01-full-course"
        if not trans_dir.exists():
            print(f"  ⚠️ {course} — no translations dir")
            continue

        lessons = discover_lessons(course)
        print(f"\n{course}")

        for lesson in lessons:
            json_path = trans_dir / (lesson["lesson_name"] + ".json")
            if not json_path.exists():
                continue

            data = json.loads(json_path.read_text(encoding="utf-8"))
            entries_data = data.get("entries", {})

            # Check if translations exist
            has_tw = any(e.get("zh_tw") for e in entries_data.values())
            has_cn = any(e.get("zh_cn") for e in entries_data.values())
            if not has_tw and not has_cn:
                continue

            # Read clean SRT
            clean_srt = lesson["srt_path"].parent / (lesson["video_stem"] + ".srt")
            if not clean_srt.exists():
                continue
            entries = parse_clean_srt(clean_srt)

            out_dir = lesson["lesson_dir"] / "srt" / "bilingual"
            out_dir.mkdir(parents=True, exist_ok=True)

            if has_tw:
                out_path = out_dir / (lesson["video_stem"] + "_bilingual.srt")
                write_bilingual_srt(entries, entries_data, "zh_tw", out_path)
                print(f"  ✅ {lesson['lesson_name']} zh-TW ({len(entries)} entries)")
                total += 1

            if has_cn:
                out_path = out_dir / (lesson["video_stem"] + "_bilingual_zh-CN.srt")
                write_bilingual_srt(entries, entries_data, "zh_cn", out_path)
                print(f"  ✅ {lesson['lesson_name']} zh-CN ({len(entries)} entries)")
                total += 1

    print(f"\nTotal: {total} bilingual SRTs generated")


def write_bilingual_srt(entries, translations, lang_key, output_path):
    """Write bilingual SRT (EN + ZH)."""
    blocks = []
    for e in entries:
        idx_str = str(e["index"])
        zh = translations.get(idx_str, {}).get(lang_key, "")
        lines = [str(e["index"]), e["timestamp"], e["text"]]
        if zh:
            lines.append(zh)
        blocks.append("\n".join(lines))
    output_path.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")


# ============================================================
# Stage 4: Visual Guides
# ============================================================

def cmd_visual():
    """Extract frames and burn bilingual subtitles."""
    total = 0
    for course in COURSES:
        lessons = discover_lessons(course)
        print(f"\n{course}")

        for lesson in lessons:
            if not lesson["video_path"] or not lesson["video_path"].exists():
                print(f"  ⚠️ {lesson['lesson_name']} — no video")
                continue

            # Check for bilingual SRT
            bi_dir = lesson["lesson_dir"] / "srt" / "bilingual"
            bi_srts = list(bi_dir.glob("*_bilingual.srt")) if bi_dir.exists() else []
            if not bi_srts:
                print(f"  ⚠️ {lesson['lesson_name']} — no bilingual SRT")
                continue

            bi_srt = bi_srts[0]
            entries = parse_clean_srt(bi_srt)
            if not entries:
                continue

            vg_dir = lesson["lesson_dir"] / "visual-guide"
            vg_dir.mkdir(parents=True, exist_ok=True)

            video_path = lesson["video_path"]
            frames = extract_frames(video_path, entries, vg_dir)
            total += frames

            # Generate markdown index
            write_visual_guide_md(lesson, entries, vg_dir)
            print(f"  ✅ {lesson['lesson_name']} — {frames} frames")

    print(f"\nTotal: {total} frames extracted")


def extract_frames(video_path: Path, entries: list[dict], output_dir: Path) -> int:
    """Extract one frame per subtitle entry at midpoint timestamp."""
    count = 0
    for e in entries:
        mid_sec = (e["start_sec"] + e["end_sec"]) / 2
        out_file = output_dir / f"frame_{e['index']:03d}.jpg"
        if out_file.exists():
            count += 1
            continue

        cmd = [
            "ffmpeg", "-y", "-ss", str(mid_sec),
            "-i", str(video_path),
            "-frames:v", "1",
            "-q:v", "3",
            str(out_file),
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=30)
        if result.returncode == 0 and out_file.exists():
            count += 1
    return count


def write_visual_guide_md(lesson: dict, entries: list[dict], vg_dir: Path):
    """Write a Markdown visual guide with frames and bilingual subtitles."""
    lesson_name = lesson["lesson_name"]
    title = lesson_name.split("-", 1)[1].replace("-", " ").title() if "-" in lesson_name else lesson_name

    lines = [
        f"# {title} — Visual Guide",
        "",
        f"> Course: {lesson['course']} | Lesson: {lesson_name}",
        "",
        "---",
        "",
    ]

    for e in entries:
        frame_file = f"frame_{e['index']:03d}.jpg"
        text_lines = e["text"].split("\n")
        en_text = text_lines[0] if text_lines else ""
        zh_text = text_lines[1] if len(text_lines) > 1 else ""

        lines.append(f"### [{e['start_ts']} → {e['end_ts']}]")
        lines.append("")
        lines.append(f"![Frame {e['index']}]({frame_file})")
        lines.append("")
        lines.append(f"**EN:** {en_text}")
        if zh_text:
            lines.append(f"**ZH:** {zh_text}")
        lines.append("")

    (vg_dir / "README.md").write_text("\n".join(lines), encoding="utf-8")


# ============================================================
# Main
# ============================================================

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]
    if cmd == "preprocess":
        cmd_preprocess()
    elif cmd == "templates":
        cmd_templates()
    elif cmd == "bilingual":
        cmd_bilingual()
    elif cmd == "visual":
        cmd_visual()
    elif cmd == "all":
        cmd_preprocess()
        cmd_templates()
        cmd_bilingual()
        cmd_visual()
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
