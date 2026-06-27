#!/usr/bin/env python3
"""Scaffold generator for expertise project entries.

Usage:
    python3 tools/new_entry.py course "Transport Phenomena I"
    python3 tools/new_entry.py project "nanoparticle synthesis"
    python3 tools/new_entry.py researcher "Jane Doe columbia"
    python3 tools/new_entry.py internship "Pfizer Summer 2027"
    python3 tools/new_entry.py learning "MIT OCW 5.60 Thermodynamics"
    python3 tools/new_entry.py paper "Drug Delivery Nanoparticles 2024"
    python3 tools/new_entry.py opportunity "NSF REU Summer 2027"
    python3 tools/new_entry.py note "Why quantum chemistry, not quantum mechanics"
"""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TODAY = date.today().isoformat()


def slugify(name: str) -> str:
    s = name.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s.strip())
    return s[:60]


TEMPLATES = {
    "course": {
        "dir": ROOT / "data" / "courses",
        "filename": lambda name: f"{slugify(name)}.md",
        "content": lambda name: f"""# {name}

**Status:** planned
**Semester:**
**Credits:**
**Fulfills:**
**Grade:**

---

## Why This Course Matters

[Fill in: how does this course connect to chemical engineering and the pharma/biotech mission?]

---

## Log

---

## Key Concepts

---

## Resources Used

---

## Connections
""",
    },
    "project": {
        "dir": ROOT / "data" / "projects",
        "filename": lambda name: f"{TODAY[:7]}-{slugify(name)}.md",
        "content": lambda name: f"""# {name}

**Type:** research | class | personal | collaboration
**Status:** ideation
**Started:** {TODAY}
**Completed:**
**Course Context:**
**Collaborators:**
**PI / Supervisor:**
**Outcome:**

---

## Mission Relevance

[One sentence: why does this project connect to building pharma/biotech for underserved populations?]

---

## Log

### {TODAY} — Initiated

[What you're starting, why, what the initial plan is.]

---

## Notes & Findings

---

## Deliverables

- [ ]
""",
    },
    "researcher": {
        "dir": ROOT / "data" / "research" / "professors",
        "filename": lambda name: f"{slugify(name)}.md",
        "content": lambda name: f"""# {name}

**Institution:**
**Department:**
**Lab:**
**Focus Areas:**
**Website:**
**Email:**
**Status:** identified

---

## Why Relevant

[Two sentences: what specifically about their work connects to the pharma/biotech mission?]

---

## Lab Research Summary

[What their lab is currently working on — from website or papers.]

---

## Papers of Interest

-

---

## Opportunities in This Lab

- Undergraduate research position: unknown
- REU: n/a
- Notes:

---

## Contact Log

---

## Next Action

[Specific, dated action item.]
""",
    },
    "internship": {
        "dir": ROOT / "data" / "internships",
        "filename": lambda name: f"{TODAY[:7]}-{slugify(name)}.md",
        "content": lambda name: f"""# {name}

**Organization:**
**Type:** internship | fellowship | award | REU | grant | conference
**Status:** identified
**Deadline:**
**Program Dates:**
**Location:**
**Compensation:** paid | unpaid | stipend
**Application Portal:**

---

## Why This Opportunity

[One paragraph: why specifically this organization and role.]

---

## Requirements Checklist

- [ ] Resume updated
- [ ] Cover letter drafted
- [ ] Transcript requested
- [ ] Recommendation requested from:
- [ ] Application submitted

---

## Log

### {TODAY} — Identified

[How I found this, initial impression.]

---

## Outcome Notes

""",
    },
    "learning": {
        "dir": ROOT / "data" / "learning",
        "filename": lambda name: f"{slugify(name)}.md",
        "content": lambda name: f"""# {name}

**Type:** online-course | textbook | workshop | certification | lecture-series
**Source:**
**URL:**
**Status:** identified
**Started:**
**Completed:**
**Time invested:** 0 hours
**Relevance:** core-cheme | supplemental | mission-research | math-support

---

## Why This Resource

[One sentence: what gap does this fill?]

---

## Progress Log

---

## Key Takeaways

---

## Connections to Coursework

""",
    },
    "paper": {
        "dir": ROOT / "data" / "research" / "papers",
        "filename": lambda name: f"{slugify(name)}.md",
        "content": lambda name: f"""# {name}

**Authors:**
**Year:**
**Journal:**
**DOI / URL:**
**Status:** identified
**Read date:**

---

## Why Relevant

[One sentence: how does this connect to ChemE goals or pharma/biotech mission?]

---

## Summary

[Fill after reading.]

---

## Key Findings

---

## Questions & Follow-ups

""",
    },
    "note": {
        "dir": ROOT / "data" / "notes",
        "filename": lambda name: f"{slugify(name)}.md",
        "content": lambda name: f"""# {name}

**Date:** {TODAY}
**Category:** Decision

---

[Write the note here in plain markdown — ## subheadings, **bold**, lists, and
$inline math$ all render. Category is either Decision (why a choice was made)
or Concept (something learned, explained to yourself).]
""",
    },
    "opportunity": {
        "dir": ROOT / "data" / "research" / "opportunities",
        "filename": lambda name: f"{slugify(name)}.md",
        "content": lambda name: f"""# {name}

**Type:** REU | lab-position | conference | fellowship | grant
**Institution:**
**PI / Contact:**
**Status:** identified
**Deadline:**
**Dates:**
**Stipend / Funding:**
**Application:**

---

## Why Relevant

[One sentence: why is this opportunity worth pursuing?]

---

## Requirements

- [ ]

---

## Log

### {TODAY} — Identified

[How found, initial impression.]

---

## Outcome

""",
    },
}


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 1

    entity_type = sys.argv[1].lower()
    name = " ".join(sys.argv[2:])

    if entity_type not in TEMPLATES:
        print(f"Unknown type: {entity_type!r}")
        print(f"Valid types: {', '.join(TEMPLATES)}")
        return 1

    tmpl = TEMPLATES[entity_type]
    output_dir: Path = tmpl["dir"]
    output_dir.mkdir(parents=True, exist_ok=True)

    filename: str = tmpl["filename"](name)
    output_path = output_dir / filename

    if output_path.exists():
        print(f"Already exists: {output_path.relative_to(ROOT)}")
        print("Refusing to overwrite. Edit the file directly or choose a different name.")
        return 1

    content: str = tmpl["content"](name)
    output_path.write_text(content, encoding="utf-8")

    print(f"Created: {output_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
