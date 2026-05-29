#!/usr/bin/env python3
"""Build the Chemical Engineering Roadmap dashboard: data/ + templates/ + static/ -> site/.

Parses **Field:** value headers from markdown files (no YAML frontmatter).
Renders Jinja2 templates to site/ as static HTML.

Run: python3 tools/build.py
"""

from __future__ import annotations

import re
import shutil
import sys
from datetime import date, datetime
from pathlib import Path

try:
    import markdown
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except ImportError as e:
    sys.stderr.write(
        f"Missing dependency: {e.name}\n"
        "Install with: pip3 install --user markdown jinja2\n"
    )
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
SITE_DIR = ROOT / "site"

TODAY = date.today()

FIELD_RE = re.compile(r"^\*\*(.+?):\*\*[ \t]*(.*)$", re.MULTILINE)
LOG_ENTRY_RE = re.compile(r"^###\s+\d{4}-\d{2}-\d{2}", re.MULTILINE)
SECTION_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)


# ── Parsing helpers ──────────────────────────────────────────────────────────

def parse_fields(text: str) -> dict[str, str]:
    """Extract all **Field:** value pairs from a markdown file."""
    return {m.group(1).strip(): m.group(2).strip() for m in FIELD_RE.finditer(text)}


def parse_title(text: str) -> str:
    """Extract the first # H1 title."""
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else "Untitled"


def log_entry_count(text: str) -> int:
    """Count dated log entries (### YYYY-MM-DD lines)."""
    return len(LOG_ENTRY_RE.findall(text))


def section_text(text: str, section_name: str) -> str:
    """Extract the content of a ## Section."""
    m = re.search(rf"^##\s+{re.escape(section_name)}\s*$(.*?)(?=^##\s|\Z)",
                  text, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else ""


def days_until(deadline_str: str) -> int | None:
    """Parse YYYY-MM-DD deadline and return days from today. None if unparseable."""
    try:
        d = datetime.strptime(deadline_str[:10], "%Y-%m-%d").date()
        return (d - TODAY).days
    except (ValueError, TypeError):
        return None


_SEM_ORDER = {
    "Semester I": 1, "Semester II": 2, "Semester III": 3, "Semester IV": 4,
    "Semester V": 5, "Semester VI": 6, "Semester VII": 7, "Semester VIII": 8,
}

def semester_order(sem: str) -> int:
    for key, val in _SEM_ORDER.items():
        if key in sem:
            return val
    return 99


def classify_subject(title: str) -> str:
    code = title.split()[0].upper() if title else ""
    if code in ("MATH", "APMA"):
        return "Mathematics"
    elif code == "CHEM":
        return "Chemistry"
    elif code == "PHYS":
        return "Physics"
    elif code == "BIOL":
        return "Biology"
    elif code in ("CHEN", "CHEE", "CHAP"):
        return "Chemical Engineering"
    elif code == "ENGI":
        return "Engineering & CS"
    elif code == "PHED":
        return "Physical Education"
    else:
        return "Humanities & General"


SUBJECT_ORDER = [
    "Mathematics", "Chemistry", "Physics", "Biology",
    "Chemical Engineering", "Engineering & CS",
    "Humanities & General", "Physical Education",
]


# ── Data loaders ─────────────────────────────────────────────────────────────

def load_courses() -> list[dict]:
    courses = []
    course_dir = DATA_DIR / "courses"
    for path in sorted(course_dir.glob("*.md")):
        if path.name.startswith("_"):
            continue
        text = path.read_text(encoding="utf-8")
        fields = parse_fields(text)
        title = parse_title(text)
        sem = fields.get("Semester", "")
        courses.append({
            "title": title,
            "file": path.name,
            "status": fields.get("Status", "planned").lower(),
            "semester": sem,
            "semester_order": semester_order(sem),
            "subject": classify_subject(title),
            "credits": fields.get("Credits", ""),
            "fulfills": fields.get("Fulfills", ""),
            "grade": fields.get("Grade", ""),
            "professor": fields.get("Professor", ""),
            "log_count": log_entry_count(text),
            "connections": section_text(text, "Connections"),
            "why": section_text(text, "Why This Course Matters"),
        })
    return courses


def load_projects() -> list[dict]:
    projects = []
    project_dir = DATA_DIR / "projects"
    for path in sorted(project_dir.glob("*.md"), reverse=True):
        if path.name.startswith("_"):
            continue
        text = path.read_text(encoding="utf-8")
        fields = parse_fields(text)
        projects.append({
            "title": parse_title(text),
            "file": path.name,
            "type": fields.get("Type", "").split("|")[0].strip(),
            "status": fields.get("Status", "ideation").lower(),
            "started": fields.get("Started", ""),
            "completed": fields.get("Completed", ""),
            "mission": section_text(text, "Mission Relevance"),
            "log_count": log_entry_count(text),
            "deliverables": section_text(text, "Deliverables"),
        })
    return projects


def load_researchers() -> list[dict]:
    researchers = []
    prof_dir = DATA_DIR / "research" / "professors"
    for path in sorted(prof_dir.glob("*.md")):
        if path.name.startswith("_"):
            continue
        text = path.read_text(encoding="utf-8")
        fields = parse_fields(text)
        researchers.append({
            "title": parse_title(text),
            "file": path.name,
            "institution": fields.get("Institution", ""),
            "department": fields.get("Department", ""),
            "lab": fields.get("Lab", ""),
            "focus": fields.get("Focus Areas", ""),
            "status": fields.get("Status", "identified").lower(),
            "next_action": section_text(text, "Next Action"),
            "log_count": log_entry_count(text),
        })
    return researchers


def load_internships() -> list[dict]:
    internships = []
    intern_dir = DATA_DIR / "internships"
    for path in sorted(intern_dir.glob("*.md"), reverse=True):
        if path.name.startswith("_"):
            continue
        text = path.read_text(encoding="utf-8")
        fields = parse_fields(text)
        deadline = fields.get("Deadline", "")
        internships.append({
            "title": parse_title(text),
            "file": path.name,
            "org": fields.get("Organization", ""),
            "type": fields.get("Type", "internship").split("|")[0].strip(),
            "status": fields.get("Status", "identified").lower(),
            "deadline": deadline,
            "days_until": days_until(deadline),
            "program_dates": fields.get("Program Dates", ""),
            "location": fields.get("Location", ""),
            "log_count": log_entry_count(text),
        })
    internships.sort(key=lambda x: (x["days_until"] is None, x["days_until"] or 9999))
    return internships


def load_learning() -> list[dict]:
    resources = []
    learn_dir = DATA_DIR / "learning"
    for path in sorted(learn_dir.glob("*.md")):
        if path.name.startswith("_"):
            continue
        text = path.read_text(encoding="utf-8")
        fields = parse_fields(text)
        resources.append({
            "title": parse_title(text),
            "file": path.name,
            "type": fields.get("Type", "").split("|")[0].strip(),
            "status": fields.get("Status", "identified").lower(),
            "source": fields.get("Source", ""),
            "started": fields.get("Started", ""),
            "time_invested": fields.get("Time invested", ""),
            "relevance": fields.get("Relevance", ""),
        })
    return resources


# ── Stats computation ─────────────────────────────────────────────────────────

def compute_stats(courses, projects, researchers, internships, learning) -> dict:
    all_courses_complete = sum(1 for c in courses if c["status"] == "completed")
    all_courses_total = max(len(courses), 1)

    cheme_core = [c for c in courses if c.get("subject") == "Chemical Engineering"]
    cheme_core_complete = sum(1 for c in cheme_core if c["status"] == "completed")
    cheme_core_total = max(len(cheme_core), 1)

    active_projects = [p for p in projects if p["status"] == "active"]
    upcoming_deadlines = [i for i in internships
                          if i["days_until"] is not None and 0 <= i["days_until"] <= 30]
    active_learning = [r for r in learning if r["status"] == "in-progress"]

    researcher_counts = {}
    for r in researchers:
        s = r["status"]
        researcher_counts[s] = researcher_counts.get(s, 0) + 1

    internship_counts = {}
    for i in internships:
        s = i["status"]
        internship_counts[s] = internship_counts.get(s, 0) + 1

    return {
        "today": TODAY.strftime("%B %-d, %Y"),
        "all_courses_complete": all_courses_complete,
        "all_courses_total": all_courses_total,
        "all_courses_pct": int(all_courses_complete / all_courses_total * 100),
        "cheme_core_complete": cheme_core_complete,
        "cheme_core_total": cheme_core_total,
        "cheme_core_pct": int(cheme_core_complete / cheme_core_total * 100),
        "active_projects": active_projects,
        "upcoming_deadlines": upcoming_deadlines,
        "active_learning": active_learning,
        "researcher_counts": researcher_counts,
        "internship_counts": internship_counts,
        "total_researchers": len(researchers),
        "total_internships": len(internships),
    }


# ── Timeline data ─────────────────────────────────────────────────────────────

ROADMAP_SEMESTERS = [
    {"label": "Sem I", "season": "Fall 2026", "note": "CC start", "milestone": False},
    {"label": "Sem II", "season": "Spr 2027", "note": "Apply to SEAS", "milestone": False},
    {"label": "TRANSFER", "season": "→ SEAS", "note": "Transfer milestone", "milestone": True},
    {"label": "Sem III", "season": "Fall 2027", "note": "First SEAS semester", "milestone": False},
    {"label": "Sem IV", "season": "Spr 2028", "note": "", "milestone": False},
    {"label": "Sem V", "season": "Fall 2028", "note": "Transport, Thermo", "milestone": False},
    {"label": "Sem VI", "season": "Spr 2029", "note": "Kinetics, Separations", "milestone": False},
    {"label": "Sem VII", "season": "Fall 2029", "note": "Design, Control", "milestone": False},
    {"label": "Sem VIII", "season": "Spr 2030", "note": "ChemE Lab, Graduation", "milestone": False},
]


# ── Professor data ────────────────────────────────────────────────────────────

PROFESSORS = [
    # Tier 1 — Primary Targets
    {"rank": 1, "tier": 1, "name": "Michel Sadelain", "division": "CUMC",
     "why": "CAR-T pioneer (Kymriah + Breyanzi FDA-approved); co-founder Alaya.bio (SRA Jan 2025); CICET brand new and actively recruiting"},
    {"rank": 2, "tier": 1, "name": "Dalibor Sames", "division": "Chemistry",
     "why": "AbbVie acquired Bretisilocin from his startup Gilgamesh for up to $1.2B (Aug 2025); co-founded Kures (acquired by ATAI); multiple clinical-stage CNS programs"},
    {"rank": 3, "tier": 1, "name": "Saeed Tavazoie", "division": "Computational",
     "why": "Two drugs in active Phase 1b/2 trials (RGX-104, RGX-202) at Inspirna, which he co-founded; $73M total raised"},
    {"rank": 4, "tier": 1, "name": "Richard Friesner", "division": "Computational",
     "why": "Co-founder and SAB Chair, Schrödinger (NASDAQ: SDGR); built Glide, WaterMap, and Jaguar — the industry-standard backbone of computational drug discovery; NAS member"},
    {"rank": 5, "tier": 1, "name": "Brent Stockwell", "division": "Chemistry",
     "why": "Discovered ferroptosis (one of the hottest cancer drug targets); co-founded four companies (CombinatoRx NASDAQ, Inzen, ProJenX, Exarta); NAM 2023"},
    # Tier 2 — Strong Fits
    {"rank": 6, "tier": 2, "name": "Henry Colecraft", "division": "CUMC",
     "why": "Co-founder Stablix ($63M Series A) and Flux Therapeutics; active pharma collaboration with DyNAbind; enDUB platform directly addresses ion channel diseases"},
    {"rank": 7, "tier": 2, "name": "Elisa Konofagou", "division": "BME",
     "why": "Founder Delsona Therapeutics (FDA IND cleared; Phase I/II results, Sci. Transl. Med. Nov 2025); focused ultrasound BBB opening for CNS drug delivery"},
    {"rank": 8, "tier": 2, "name": "Andrea Califano", "division": "Computational",
     "why": "Co-founder + CSO DarwinHealth (clinical-use cancer diagnostics); exclusive Daiichi Sankyo collaboration; active clinical trials in 14 cancer types"},
    {"rank": 9, "tier": 2, "name": "Gordana Vunjak-Novakovic", "division": "BME",
     "why": "Co-founded four companies including TARA Biosystems (pharma cardiac drug testing, exclusive Columbia license) and EpiBone; Venture Partner at Catalio Capital"},
    {"rank": 10, "tier": 2, "name": "Siddhartha Mukherjee", "division": "CUMC",
     "why": "Founder + CEO Manas AI (launched Jan 2025, $24.6M seed, General Catalyst + Reid Hoffman); generative chemistry + docking + wet-lab for cancer drug discovery"},
    # Tier 3 — Solid
    {"rank": 11, "tier": 3, "name": "Kam Leong", "division": "BME",
     "why": "60+ issued/licensed patents in drug, gene, and immunotherapy delivery; NAE + NAS + NAM (all three); oral LNP biologics for hemophilia directly relevant to Jonas's background"},
    {"rank": 12, "tier": 3, "name": "Ke Cheng", "division": "BME",
     "why": "Co-founded Xsome Biotech + Xollent Biotech; Capricor Therapeutics and Selsym Biotech are active licensees; two IND-enabling programs running at Columbia since 2023"},
    {"rank": 13, "tier": 3, "name": "Mohammed AlQuraishi", "division": "Computational",
     "why": "Co-founder OpenFold; AbbVie and J&J directly training OpenFold3 on proprietary protein-drug interaction data (2025); hottest intersection of structure-based design + generative AI"},
    {"rank": 14, "tier": 3, "name": "Jingyue Ju", "division": "ChemE",
     "why": "Roche/Genia acquisition ($350M) licensed his nucleotide chemistry; active antiviral drug discovery program generating lead compounds against pandemic-risk viruses"},
    {"rank": 15, "tier": 3, "name": "Hashim Al-Hashimi", "division": "CUMC",
     "why": "Co-founded Nymirum and Base4 Inc. (2023, active); RNA conformational dynamics platform enables docking against RNA — fastest-growing new drug modality"},
    # Tier 4 — Relevant
    {"rank": 16, "tier": 4, "name": "Jonathan Javitch", "division": "CUMC",
     "why": "GPCR drug discovery platform licensed via Columbia Tech Ventures; GPCRs are targets of ~35% of all approved drugs; Director, Lieber Center for Schizophrenia Research"},
    {"rank": 17, "tier": 4, "name": "Tal Danino", "division": "BME",
     "why": "Probiotic tumor-colonizing cancer vaccine; Nature 2024 paper; active Columbia Tech Ventures licensing (CU18339); Chan Zuckerberg Biohub NY Investigator"},
    {"rank": 18, "tier": 4, "name": "Harris Wang", "division": "Computational",
     "why": "SAB member SNIPR Biome and Kingdom Supercultures; co-founded two companies; microbiome therapeutics is an emerging drug modality"},
    {"rank": 19, "tier": 4, "name": "Santiago Correa", "division": "BME",
     "why": "LNP platform using biological components for immune reprogramming; collaborating with Unchained Labs on automated LNP manufacturing; early-career and approachable"},
    {"rank": 20, "tier": 4, "name": "Scott Banta", "division": "ChemE",
     "why": "Patents US 11,260,121 and US 11,730,803 in virus-particle cancer immunotherapy; site-clickable EGF variants for targeted therapy (2025); co-founder Ironic Chemicals"},
    # Tier 5 — Worth Knowing
    {"rank": 21, "tier": 5, "name": "Cory Abate-Shen", "division": "CUMC",
     "why": "Directly tested Selisistat (SIRT1 inhibitor) in mouse models; identified FOXM1/CENPF as druggable prostate cancer targets; NAS member"},
    {"rank": 22, "tier": 5, "name": "Parisa Yousefpour", "division": "BME",
     "why": "Self-amplifying RNA (saRNA) with drug-responsive gene expression control; next frontier beyond mRNA vaccines; joined Columbia Jan 2025"},
    {"rank": 23, "tier": 5, "name": "Neel Shah", "division": "Chemistry",
     "why": "ML-driven kinase drug target profiling (100+ kinases); 2024 NSF CAREER ($801K) oriented toward drug development; kinases are the #1 oncology target class"},
    {"rank": 24, "tier": 5, "name": "Oleg Gang", "division": "ChemE",
     "why": "DNA origami delivers doxorubicin to HER2+ breast cancer cells; Brookhaven provisional patent; Vannevar Bush Fellow 2024 — platform validated, no company yet"},
    {"rank": 25, "tier": 5, "name": "Yonghao Yu", "division": "CUMC",
     "why": "Chemoproteomic platform for covalent hotspot identification on undruggable targets; first-in-class covalent inhibitors for cancer, diabetes, and neurodegeneration"},
    {"rank": 26, "tier": 5, "name": "Elham Azizi", "division": "Computational",
     "why": "ML for tumor ecosystem modeling and immunotherapy resistance prediction; Takeda/NYAS award (2024) signals early pharma interest"},
    {"rank": 27, "tier": 5, "name": "James Leighton", "division": "Chemistry",
     "why": "Synthesis of ADC natural product payloads (picomolar potency); NIH-funded for pharmaceutical targets; ADCs are one of pharma's fastest-growing modalities"},
    {"rank": 28, "tier": 5, "name": "Allie Obermeyer", "division": "ChemE",
     "why": "Co-founder Werewool (venture-backed, 2022); protein condensate/coacervate drug delivery platform — startup founded, not yet pharma-industry-scale"},
    {"rank": 29, "tier": 5, "name": "Barry Honig", "division": "Computational",
     "why": "Built DelPhi and GRASP (foundational electrostatics tools); PrePCI database (proteome-scale protein-compound interaction predictions) embedded in commercial pipelines; former HHMI"},
    {"rank": 30, "tier": 5, "name": "Xuebing Wu", "division": "Computational",
     "why": "CRISPR + ML for RNA regulatory drug target identification; RNA-targeting small molecules one of the fastest-growing modalities; NIH New Innovator, Pew-Stewart Scholar"},
]


# ── Milestone data ────────────────────────────────────────────────────────────

MILESTONES = [
    {
        "phase": "20s",
        "name": "Hello Tomorrow Deep Tech Challenge",
        "signal": "First global deep tech founder recognition",
    },
    {
        "phase": "20s",
        "name": "Y Combinator (acceptance)",
        "signal": "Top-tier startup validation, global",
    },
    {
        "phase": "20s",
        "name": "Forbes 30 Under 30",
        "signal": "Mainstream visibility, entrepreneurship/science",
    },
    {
        "phase": "30s",
        "name": "MacArthur \"Genius\" Grant",
        "signal": "$800K, no strings. Signals genuinely original work. They find you — you can't apply",
    },
    {
        "phase": "30s",
        "name": "MIT TR35 (Innovators Under 35)",
        "signal": "The science/tech world's Forbes, but harder",
    },
    {
        "phase": "30s",
        "name": "POSCO TJ Park Prize",
        "signal": "Top Korean-heritage scientist recognition, globally respected",
    },
    {
        "phase": "30s",
        "name": "TIME 100",
        "signal": "Global cultural/leadership recognition at scale",
    },
    {
        "phase": "30s",
        "name": "TED main stage invitation",
        "signal": "Platform milestone — your idea is worth the world hearing",
    },
]


# ── Render ────────────────────────────────────────────────────────────────────

def render(env, template_name: str, **ctx) -> str:
    return env.get_template(template_name).render(**ctx)


def main() -> int:
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir(parents=True)

    if STATIC_DIR.exists():
        shutil.copytree(STATIC_DIR, SITE_DIR / "static")

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    courses = load_courses()
    projects = load_projects()
    researchers = load_researchers()
    internships = load_internships()
    learning = load_learning()
    stats = compute_stats(courses, projects, researchers, internships, learning)

    common = {
        "stats": stats,
        "today_str": TODAY.strftime("%B %-d, %Y"),
    }

    pages = [
        ("about.html", "index.html", {}),
        ("dashboard.html", "dashboard.html", {
            "courses": courses,
            "projects": projects,
            "researchers": researchers,
            "internships": internships,
            "learning": learning,
            "semesters": ROADMAP_SEMESTERS,
        }),
        ("courses.html", "courses.html", {
            "courses": courses,
            "subject_order": SUBJECT_ORDER,
            "total_credits": sum(
                float(c["credits"]) for c in courses if c["credits"]
            ),
        }),
        ("registration.html", "registration.html", {}),
        ("projects.html", "projects.html", {"projects": projects}),
        ("professors.html", "professors.html", {"professors": PROFESSORS}),
        ("research.html", "research.html", {"researchers": researchers, "learning": learning}),
        ("internships.html", "internships.html", {"internships": internships}),
        ("milestones.html", "milestones.html", {"milestones": MILESTONES}),
        ("advice.html", "advice.html", {}),
    ]

    for template_name, out_name, ctx in pages:
        html = render(env, template_name, **common, **ctx)
        (SITE_DIR / out_name).write_text(html, encoding="utf-8")

    print(f"Built {len(pages)} pages → {SITE_DIR.relative_to(ROOT)}/")
    print(f"  All courses:            {stats['all_courses_complete']}/{stats['all_courses_total']} complete")
    print(f"  ChemE core courses:     {stats['cheme_core_complete']}/{stats['cheme_core_total']} complete")
    print(f"  Active projects:        {len(stats['active_projects'])}")
    print(f"  Upcoming deadlines:     {len(stats['upcoming_deadlines'])} (next 30 days)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
