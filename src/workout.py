#!/usr/bin/env python3
"""
workout_to_md.py
Converts a Health Auto Export workout JSON file into an 11ty-compatible Markdown file.

Usage:
    python3 workout_to_md.py path/to/workout.json
"""

import json
import sys
import math
from datetime import datetime
from pathlib import Path


# ── Helpers ───────────────────────────────────────────────────────────────────

def kj_to_kcal(kj: float) -> int:
    """Convert kilojoules to kilocalories, rounded to nearest integer."""
    return round(kj / 4.184)


def format_duration(seconds: float) -> str:
    """Convert seconds to mm:ss string."""
    total = int(seconds)
    mins, secs = divmod(total, 60)
    return f"{mins}:{secs:02d}"


def parse_start_date(raw: str) -> datetime:
    """
    Parse Health Auto Export date strings.
    Handles formats like '2026-06-02 7:26:43\u202fam +0100'
    (Health Auto Export uses a narrow no-break space \u202f before am/pm)
    """
    # Normalise the narrow no-break space (\u202f) to a regular space,
    # then split on any whitespace
    normalised = raw.strip().replace("\u202f", " ")
    parts = normalised.split()
    # parts: ['2026-06-02', '7:26:43', 'am', '+0100']
    date_part   = parts[0]
    time_part   = parts[1].zfill(8)   # pad to HH:MM:SS
    ampm_part   = parts[2].upper()
    offset_part = parts[3]

    combined = f"{date_part} {time_part} {ampm_part} {offset_part}"
    return datetime.strptime(combined, "%Y-%m-%d %I:%M:%S %p %z")


def safe_qty(d: dict | None, decimals: int = 2) -> float | None:
    """Safely extract and round a qty value from a nested dict."""
    if not d or "qty" not in d:
        return None
    return round(float(d["qty"]), decimals)


# ── Workout type detection ─────────────────────────────────────────────────────

RUNNING_TYPES = {"outdoor run", "indoor run", "running"}
STRENGTH_TYPES = {"strength training", "functional strength training", "traditional strength training"}


def classify(name: str) -> str:
    """Returns 'run', 'strength', or 'other'."""
    lower = name.lower()
    if any(t in lower for t in RUNNING_TYPES):
        return "run"
    if any(t in lower for t in STRENGTH_TYPES):
        return "strength"
    return "other"


# ── Slug builder ─────────────────────────────────────────────────────────────

def build_slug(workout: dict, dt: datetime) -> str:
    """
    Build a URL-friendly filename slug, e.g.:
      outdoor-run-2026-06-02
      strength-training-2026-06-02
    """
    name = workout.get("name", "workout")
    # Lowercase, replace spaces/underscores with hyphens, strip anything non-alphanumeric
    slug_name = name.lower().replace(" ", "-").replace("_", "-")
    slug_name = "".join(c for c in slug_name if c.isalnum() or c == "-")
    # Collapse any double-hyphens that might appear
    while "--" in slug_name:
        slug_name = slug_name.replace("--", "-")
    return f"{slug_name}-{dt.strftime('%Y-%m-%d')}"


# ── Markdown builder ──────────────────────────────────────────────────────────

def build_frontmatter(workout: dict) -> tuple[str, datetime]:
    name     = workout.get("name", "Workout")
    raw_start = workout.get("start", "")
    dt       = parse_start_date(raw_start)
    date_str = dt.strftime("%Y-%m-%d")
    kind     = classify(name)

    duration_raw = workout.get("duration", 0)
    duration_fmt = format_duration(duration_raw)

    calories_raw = safe_qty(workout.get("activeEnergyBurned"), decimals=4)
    calories     = kj_to_kcal(calories_raw) if calories_raw is not None else None

    hr_avg = safe_qty(workout.get("avgHeartRate"), decimals=0)
    hr_max = safe_qty(workout.get("maxHeartRate"), decimals=0)

    lines = [
        "---",
        "layout: workout.njk",
        f'title: "{name} – {dt.strftime("%-d %B %Y")}"',
        f"date: {date_str}",
        f"type: {name}",
        f"duration: {duration_fmt}",
    ]

    # Run-specific fields
    if kind == "run":
        distance = safe_qty(workout.get("distance"), decimals=2)
        if distance is not None:
            lines.append(f"distance: {distance} km")

        elevation = safe_qty(workout.get("elevationUp"), decimals=1)
        if elevation is not None:
            lines.append(f"elevation: {elevation} m")

        cadence = workout.get("stepCadence", {})
        if cadence and "qty" in cadence:
            lines.append(f"cadence: {round(cadence['qty'])} spm")

    # Shared fields
    if calories is not None:
        lines.append(f"calories: {calories} kcal")

    if hr_avg is not None:
        lines.append(f"heart_rate_avg: {int(hr_avg)}")

    if hr_max is not None:
        lines.append(f"heart_rate_max: {int(hr_max)}")

    lines += [
        'notes: ""',
        "---",
        "",  # blank line after front matter
    ]

    return "\n".join(lines), dt


# ── Main ──────────────────────────────────────────────────────────────────────

def convert(json_path: Path) -> Path:
    with open(json_path, "r") as f:
        data = json.load(f)

    workouts = data.get("data", {}).get("workouts", [])
    if not workouts:
        raise ValueError("No workouts found in JSON file.")

    # Use the first (most recent) workout
    workout = workouts[0]

    markdown, dt = build_frontmatter(workout)

    # Write .md file alongside the input JSON, with a URL-friendly name
    out_path = json_path.with_name(build_slug(workout, dt) + ".md")
    out_path.write_text(markdown)

    return out_path


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 workout_to_md.py path/to/workout.json")
        sys.exit(1)

    json_path = Path(sys.argv[1]).resolve()

    if not json_path.exists():
        print(f"Error: file not found — {json_path}")
        sys.exit(1)

    if json_path.suffix.lower() != ".json":
        print(f"Error: expected a .json file, got {json_path.suffix}")
        sys.exit(1)

    try:
        out = convert(json_path)
        print(f"✓ Written to {out}")
    except (ValueError, KeyError) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()