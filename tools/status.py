#!/usr/bin/env python3
"""Quick terminal status summary — no build required.

Run: python3 tools/status.py
"""

from __future__ import annotations

import re
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
TODAY = date.today()

FIELD_RE = re.compile(r"^\*\*(.+?):\*\*\s*(.*)$", re.MULTILINE)
LOG_RE = re.compile(r"^###\s+\d{4}-\d{2}-\d{2}", re.MULTILINE)


def fields(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    return {m.group(1).strip(): m.group(2).strip() for m in FIELD_RE.finditer(text)}


def title(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else path.stem


def days_until(deadline: str) -> int | None:
    try:
        d = datetime.strptime(deadline[:10], "%Y-%m-%d").date()
        return (d - TODAY).days
    except (ValueError, TypeError):
        return None


def main() -> int:
    print(f"\n{'='*50}")
    print(f"  ChemE Roadmap — {TODAY.strftime('%B %-d, %Y')}")
    print(f"{'='*50}\n")

    # Courses
    course_dir = DATA_DIR / "courses"
    in_progress = [p for p in course_dir.glob("*.md")
                   if not p.name.startswith("_") and
                   fields(p).get("Status", "") == "in-progress"]
    if in_progress:
        print("IN PROGRESS")
        for p in in_progress:
            print(f"  · {title(p)}")
        print()

    # Projects
    proj_dir = DATA_DIR / "projects"
    active_projects = []
    for p in proj_dir.glob("*.md"):
        if p.name.startswith("_"):
            continue
        f = fields(p)
        if f.get("Status", "") in ("active", "ideation"):
            active_projects.append((title(p), f.get("Status", "")))

    print(f"PROJECTS")
    if active_projects:
        for name, status in active_projects:
            print(f"  · [{status}] {name}")
    else:
        print(f"  No active projects")

    # Research
    print()
    prof_dir = DATA_DIR / "research" / "professors"
    profs = list(prof_dir.glob("*.md")) if prof_dir.exists() else []
    profs = [p for p in profs if not p.name.startswith("_")]
    print(f"RESEARCH PIPELINE")
    if profs:
        status_counts: dict[str, int] = {}
        for p in profs:
            s = fields(p).get("Status", "identified")
            status_counts[s] = status_counts.get(s, 0) + 1
        for s, n in sorted(status_counts.items()):
            print(f"  {n} {s}")
    else:
        print(f"  No researchers tracked")

    # Internships & Deadlines
    print()
    intern_dir = DATA_DIR / "internships"
    upcoming = []
    for p in intern_dir.glob("*.md"):
        if p.name.startswith("_"):
            continue
        f = fields(p)
        d = days_until(f.get("Deadline", ""))
        if d is not None and 0 <= d <= 60:
            upcoming.append((d, title(p), f.get("Organization", ""), f.get("Status", "")))
    upcoming.sort()

    print("UPCOMING DEADLINES (60 days)")
    if upcoming:
        for days, name, org, status in upcoming:
            tag = "TODAY" if days == 0 else f"{days}d"
            print(f"  {tag:>5}  {name}" + (f" ({org})" if org else ""))
    else:
        print("  None in the next 60 days")

    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
