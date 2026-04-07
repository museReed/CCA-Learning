#!/usr/bin/env python3
"""
Generate teaching visuals for 05-hooks chapter using Gemini 2.5 Flash Image.
Each unit gets 2-3 concept illustrations: icon-driven, white background, minimal text.
"""

import subprocess
import sys
from pathlib import Path

from google import genai
from google.genai import types

BASE_DIR = Path("/Volumes/Muse_AI_Core/CCA-Learning/courses/claude-code-in-action/05-hooks")

# ============================================================
# Prompt Definitions — one "aha moment" per image
# Rules: English only, 10-20 words max in image, icon-driven,
#        white background, no code, SF Symbols style
# ============================================================

UNIT_VISUALS = {
    "14-introducing-hooks": {
        "title": "Introducing Hooks",
        "visuals": [
            {
                "filename": "tool-execution-pipeline.png",
                "description": "Tool execution pipeline with Pre/Post hook interception points",
                "prompt": (
                    "Clean minimal diagram on white background. "
                    "A horizontal pipeline with 5 rounded boxes connected by arrows: "
                    "'Prompt' (speech bubble icon) → 'Model' (brain icon) → "
                    "'PreToolUse' (shield icon, red/green glow) → 'Tool' (wrench icon) → "
                    "'PostToolUse' (magnifying glass icon). "
                    "The PreToolUse box has two small arrows: green checkmark going forward, "
                    "red X going back to Model. "
                    "SF Symbols style icons. Soft shadows. No code. Max 10 words of text labels."
                ),
            },
            {
                "filename": "hook-vs-prompt-decision.png",
                "description": "Decision rule: 'must' = Hook, 'prefer' = Prompt",
                "prompt": (
                    "Split comparison diagram on white background. "
                    "LEFT side: a strong steel lock icon with label 'MUST' and subtitle 'Hook' — "
                    "below it: shield, checkmark, 'Guaranteed'. Color: deep blue. "
                    "RIGHT side: a gentle suggestion speech bubble icon with label 'PREFER' and subtitle 'Prompt' — "
                    "below it: star, thumbs up, 'Best effort'. Color: soft purple. "
                    "A clear vertical divider between them. "
                    "SF Symbols style. Clean, minimal. No code."
                ),
            },
            {
                "filename": "settings-hierarchy.png",
                "description": "Three-level settings hierarchy: Global → Project → Local",
                "prompt": (
                    "Vertical stack of 3 layers on white background, like geological strata. "
                    "TOP layer (smallest, brightest blue): 'Local' with a person icon — 'Highest priority'. "
                    "MIDDLE layer (medium, medium blue): 'Project' with a team/group icon — 'Shared'. "
                    "BOTTOM layer (widest, light blue): 'Global' with a globe icon — 'All projects'. "
                    "An arrow on the right side pointing UP labeled 'Priority'. "
                    "SF Symbols style icons. Clean minimal design."
                ),
            },
        ],
    },
    "15-defining-hooks": {
        "title": "Defining Hooks",
        "visuals": [
            {
                "filename": "four-step-process.png",
                "description": "Four-step hook definition: Type → Matcher → Command → Exit Code",
                "prompt": (
                    "Four connected circles in a horizontal line on white background. "
                    "Circle 1: number '1', gate icon, label 'Pre or Post'. "
                    "Circle 2: number '2', target/crosshair icon, label 'Matcher'. "
                    "Circle 3: number '3', terminal/code icon, label 'Command'. "
                    "Circle 4: number '4', exit door icon, label 'Exit Code'. "
                    "Arrows connecting each circle left to right. "
                    "Soft gradient from blue (step 1) to green (step 4). "
                    "SF Symbols style. Clean, minimal. No code."
                ),
            },
            {
                "filename": "exit-code-semantics.png",
                "description": "Exit codes: 0 = Allow (green), 2 = Block (red)",
                "prompt": (
                    "Two large circular badges on white background. "
                    "LEFT badge: green circle with white checkmark and large '0' — label 'Allow'. "
                    "A small arrow pointing forward (right). "
                    "RIGHT badge: red circle with white X and large '2' — label 'Block'. "
                    "A small arrow pointing back (left) with a speech bubble saying 'stderr feedback'. "
                    "Clean, bold, minimal. SF Symbols style. Traffic light metaphor."
                ),
            },
        ],
    },
    "16-implementing-a-hook": {
        "title": "Implementing a Hook",
        "visuals": [
            {
                "filename": "env-guard-flow.png",
                "description": "The .env file guard: complete data flow from request to block",
                "prompt": (
                    "Flowchart on white background. "
                    "START: Claude icon with speech bubble 'Read .env'. "
                    "Arrow down to: Shield icon labeled 'PreToolUse Hook'. "
                    "Arrow down to: Diamond decision 'Contains .env?' "
                    "YES arrow (red) going right to: red X icon 'BLOCKED' with a speech bubble 'Access denied'. "
                    "NO arrow (green) going down to: green checkmark 'ALLOWED' with file icon. "
                    "Clean, minimal. SF Symbols style icons. Max 15 words."
                ),
            },
            {
                "filename": "self-correcting-loop.png",
                "description": "Feedback loop: block → stderr → Claude adjusts",
                "prompt": (
                    "Circular feedback loop diagram on white background. "
                    "Three nodes in a circle: "
                    "Node 1 (top): Brain icon 'Claude tries action'. "
                    "Node 2 (right): Shield icon 'Hook blocks + explains'. "
                    "Node 3 (left): Lightbulb icon 'Claude adjusts approach'. "
                    "Curved arrows connecting them clockwise. "
                    "Center text: 'Self-Correcting'. "
                    "Soft blue tones. SF Symbols style. No code."
                ),
            },
        ],
    },
    "17-gotchas-around-hooks": {
        "title": "Gotchas Around Hooks",
        "visuals": [
            {
                "filename": "security-portability-tradeoff.png",
                "description": "Security (absolute paths) vs Portability (relative paths) solved by template",
                "prompt": (
                    "Three-panel diagram on white background. "
                    "Panel 1 (left): Lock icon + '/absolute/path' label — green checkmark 'Secure' but red X 'Not portable'. "
                    "Panel 2 (middle): Link icon + './relative' label — green checkmark 'Portable' but red X 'Not secure'. "
                    "Panel 3 (right, highlighted with glow): Magic wand icon + 'Template + Init' label — "
                    "green checkmark 'Secure' AND green checkmark 'Portable'. "
                    "An arrow from panels 1 and 2 merging into panel 3. "
                    "SF Symbols style. Clean, minimal."
                ),
            },
            {
                "filename": "template-init-pattern.png",
                "description": "Three-file pattern: example.json → init script → local.json",
                "prompt": (
                    "Horizontal flow on white background with 3 document icons. "
                    "Doc 1 (blue): 'settings.example.json' with a git icon (committed). Contains '$PWD' placeholder text. "
                    "Arrow right through a gear/cog icon labeled 'init script'. "
                    "Doc 2 (green): 'settings.local.json' with a lock icon (gitignored). Contains '/Users/alice/...' text. "
                    "Below the flow: small team icons showing 'Every developer runs init'. "
                    "SF Symbols style. Clean, minimal. No actual code."
                ),
            },
        ],
    },
    "18-useful-hooks": {
        "title": "Useful Hooks",
        "visuals": [
            {
                "filename": "type-check-feedback-loop.png",
                "description": "PostToolUse → tsc --noEmit → errors → Claude auto-fixes",
                "prompt": (
                    "Circular feedback loop on white background. "
                    "Step 1 (top): Pencil icon 'Claude edits file'. "
                    "Step 2 (right): Terminal icon 'tsc runs automatically'. "
                    "Step 3 (bottom): Warning triangle 'Type errors found'. "
                    "Step 4 (left): Wrench icon 'Claude fixes errors'. "
                    "Arrows connecting clockwise. Center: infinity symbol with 'Auto-fix loop'. "
                    "Soft gradient blue-to-green. SF Symbols style."
                ),
            },
            {
                "filename": "multi-agent-review.png",
                "description": "Primary Claude → PostToolUse → Reviewer Claude → feedback",
                "prompt": (
                    "Two brain icons on white background connected by a hook/bridge. "
                    "LEFT brain (blue): 'Primary Claude' with a pencil, writing to a file icon. "
                    "CENTER: a vertical divider with a hook/chain icon labeled 'PostToolUse'. "
                    "RIGHT brain (purple): 'Reviewer Claude' with a magnifying glass, inspecting the file. "
                    "Arrow from reviewer back to primary with speech bubble: 'Duplicate found!' "
                    "SF Symbols style. Clean layout. No code."
                ),
            },
        ],
    },
    "19-another-useful-hook": {
        "title": "Another Useful Hook",
        "visuals": [
            {
                "filename": "hook-taxonomy.png",
                "description": "Complete hook taxonomy: 9 types mapped to lifecycle",
                "prompt": (
                    "Timeline/lifecycle diagram on white background. "
                    "A horizontal timeline with lifecycle phases: "
                    "'Session Start' (play icon) → 'User Prompt' (keyboard icon) → "
                    "'Pre Tool' (shield) → 'Tool Runs' (wrench) → 'Post Tool' (magnifying glass) → "
                    "'Compact' (compress icon) → 'Stop' (flag icon) → 'Session End' (stop icon). "
                    "Below the timeline: 'Notification' (bell icon) floating with dotted line to 'anytime'. "
                    "Each icon in a soft colored circle. SF Symbols style. Clean, minimal."
                ),
            },
            {
                "filename": "debug-hook-pattern.png",
                "description": "Debug pattern: jq . > log.json to discover stdin structure",
                "prompt": (
                    "Three-step vertical flow on white background. "
                    "Step 1: Magnifying glass + question mark icon — 'What data does my hook receive?' "
                    "Step 2: Funnel/filter icon catching JSON data — 'Log everything to file'. "
                    "Step 3: Lightbulb icon with a document — 'Inspect, then build production hook'. "
                    "Arrows connecting steps downward. Side label: 'Discover before you build'. "
                    "SF Symbols style. Soft blue tones. No code."
                ),
            },
        ],
    },
}


def get_api_key():
    result = subprocess.run(
        ["security", "find-generic-password", "-s", "GOOGLE_AI_STUDIO_KEY", "-w"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError("GOOGLE_AI_STUDIO_KEY not found in Keychain")
    return result.stdout.strip()


def generate_image(client, prompt: str, output_path: Path) -> bool:
    """Generate a single educational image via Gemini Flash."""
    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[prompt],
        config=types.GenerateContentConfig(
            response_modalities=["image", "text"],
        ),
    )

    for part in response.parts:
        if part.inline_data is not None:
            image = part.as_image()
            image.save(str(output_path))
            print(f"    Saved: {output_path.name}")
            return True
        elif part.text is not None:
            print(f"    Text response: {part.text[:100]}...")

    print(f"    WARNING: No image generated")
    return False


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate teaching visuals for 05-hooks")
    parser.add_argument("--unit", type=str, help="Process specific unit (e.g., 14-introducing-hooks)")
    parser.add_argument("--dry-run", action="store_true", help="Show prompts without generating")
    args = parser.parse_args()

    units = UNIT_VISUALS
    if args.unit:
        if args.unit not in units:
            print(f"ERROR: Unknown unit '{args.unit}'")
            print(f"Valid: {', '.join(units.keys())}")
            sys.exit(1)
        units = {args.unit: units[args.unit]}

    if args.dry_run:
        for unit_id, unit_data in units.items():
            print(f"\n=== {unit_id}: {unit_data['title']} ===")
            for v in unit_data["visuals"]:
                print(f"  [{v['filename']}] {v['description']}")
                print(f"    Prompt: {v['prompt'][:120]}...")
        return

    api_key = get_api_key()
    client = genai.Client(api_key=api_key)
    print(f"Gemini client ready")

    total = sum(len(u["visuals"]) for u in units.values())
    generated = 0
    skipped = 0
    failed = 0

    for unit_id, unit_data in units.items():
        unit_dir = BASE_DIR / unit_id / "visuals"
        unit_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n{'='*60}")
        print(f"{unit_id}: {unit_data['title']} ({len(unit_data['visuals'])} images)")
        print(f"{'='*60}")

        for v in unit_data["visuals"]:
            filepath = unit_dir / v["filename"]
            if filepath.exists():
                print(f"  [{v['filename']}] Already exists, skipping")
                skipped += 1
                continue

            print(f"  [{v['filename']}] {v['description']}")
            if generate_image(client, v["prompt"], filepath):
                generated += 1
            else:
                failed += 1

    print(f"\n{'='*60}")
    print(f"Done! Generated: {generated}, Skipped: {skipped}, Failed: {failed} / Total: {total}")


if __name__ == "__main__":
    main()
