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
    "Semester VIII": 8, "Semester VII": 7, "Semester VI": 6, "Semester V": 5,
    "Semester IV": 4, "Semester III": 3, "Semester II": 2, "Semester I": 1,
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
    elif code in ("COMS", "ECBM", "STAT"):
        return "Programming"
    else:
        return "Core Curriculum"


SUBJECT_ORDER = [
    "Core Curriculum", "Chemistry", "Physics", "Mathematics", "Programming",
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
        if fields.get("Status", "planned").lower() == "waived":
            continue
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
    {"label": "Sem I", "season": "Fall 2026", "note": "Calc III, Physics I", "milestone": False},
    {"label": "Sem II", "season": "Spr 2027", "note": "Calc IV, Java", "milestone": False},
    {"label": "Sem III", "season": "Fall 2027", "note": "Orgo I, ODE, LA", "milestone": False},
    {"label": "Sem IV", "season": "Spr 2028", "note": "Orgo II, Mechanics", "milestone": False},
    {"label": "Sem V", "season": "Fall 2028", "note": "Phys Chem I, QM I", "milestone": False},
    {"label": "Sem VI", "season": "Spr 2029", "note": "Phys Chem II, QM II", "milestone": False},
    {"label": "Sem VII", "season": "Fall 2029", "note": "QSim Lab, ML, DL", "milestone": False},
    {"label": "Sem VIII", "season": "Spr 2030", "note": "Mol Modeling, Graduation", "milestone": False},
]


# ── Professor data ────────────────────────────────────────────────────────────

PROFESSORS = [
    # Chemistry-first: organic/materials/computational chemistry → pharma tech → company
    {"rank": 1,  "contact": "1st",  "name": "Santiago Correa",           "division": "BME",           "why": "Materials chemistry → bioinspired LNPs for immune reprogramming; direct fit with SNU ionizable lipid work; new lab (2023), actively building, on main campus"},
    {"rank": 2,  "contact": "2nd",  "name": "Dalibor Sames",             "division": "Chemistry",      "why": "Organic synthesis → CNS drug discovery → $1.2B AbbVie deal (Aug 2025); ibogaine pharmacophore in Nature 2024; 7 undergrads currently in lab"},
    {"rank": 3,  "contact": "3rd",  "name": "Brent Stockwell",           "division": "Chemistry",      "why": "Small molecule chemistry → ferroptosis discovery → 4 founded companies (one NASDAQ); NAM 2023; hottest cancer drug target in pharma"},
    {"rank": 4,  "contact": "4th",  "name": "Mohammed AlQuraishi",       "division": "Computational",  "why": "ML + structural chemistry → OpenFold3; AbbVie and J&J directly training his model on proprietary protein-drug data (2025)"},
    {"rank": 5,  "contact": "5th",  "name": "Scott Banta",               "division": "ChemE",          "why": "Protein engineering + synthetic biology → virus-particle cancer immunotherapy; two issued patents (2022–2023); dept chair = accessible after SEAS transfer"},
    {"rank": 6,  "contact": "6th",  "name": "Richard Friesner",          "division": "Computational",  "why": "Computational chemistry → built Glide, WaterMap, Jaguar → co-founded Schrödinger (NASDAQ: SDGR); the infrastructure the entire field runs on; NAS member"},
    {"rank": 7,  "contact": "7th",  "name": "Oleg Gang",                 "division": "ChemE",          "why": "DNA nanotechnology → origami delivers doxorubicin to HER2+ cells; Brookhaven patent; Vannevar Bush Fellow 2024"},
    {"rank": 8,  "contact": "8th",  "name": "Neel Shah",                 "division": "Chemistry",      "why": "Chemical biology + ML → kinase drug target platform (100+ kinases); 2024 NSF CAREER ($801K) explicitly for drug development"},
    {"rank": 9,  "contact": "9th",  "name": "Jingyue Ju",                "division": "ChemE",          "why": "Nucleotide chemistry → Roche/Genia acquisition ($350M); active antiviral drug discovery generating lead compounds"},
    {"rank": 10, "contact": "10th", "name": "Hashim Al-Hashimi",         "division": "CUMC",           "why": "NMR chemistry → RNA conformational dynamics → co-founded Nymirum + Base4 (2023, active); RNA-targeted small molecules fastest-growing drug modality"},
    # Chemistry-adjacent: engineering/materials with pharma application
    {"rank": 11, "contact": "11th", "name": "Kam Leong",                 "division": "BME",            "why": "Polymer + LNP chemistry → 60+ patents in drug/gene delivery; NAE + NAS + NAM; oral LNP biologics for hemophilia"},
    {"rank": 12, "contact": "12th", "name": "James Leighton",            "division": "Chemistry",      "why": "Total synthesis → ADC natural product payloads (picomolar potency); NIH-funded for pharmaceutical targets; ADCs fastest-growing oncology modality"},
    {"rank": 13, "contact": "13th", "name": "Yonghao Yu",               "division": "CUMC",           "why": "Chemoproteomic chemistry → covalent hotspot identification on undruggable targets; first-in-class covalent inhibitors for cancer and neurodegeneration"},
    {"rank": 14, "contact": "14th", "name": "Allie Obermeyer",           "division": "ChemE",          "why": "Protein condensate/coacervate chemistry → drug delivery platform; co-founder Werewool (venture-backed, 2022)"},
    {"rank": 15, "contact": "15th", "name": "Barry Honig",               "division": "Computational",  "why": "Built DelPhi and GRASP (foundational electrostatics); PrePCI (proteome-scale protein-compound predictions) embedded in commercial pharma pipelines; former HHMI"},
    # Biology-anchored: strong translational output but biology is the primary instrument
    {"rank": 16, "contact": "16th", "name": "Elisa Konofagou",           "division": "BME",            "why": "Biophysics + ultrasound → Delsona Therapeutics (FDA IND; Phase I/II results Nov 2025); noninvasive CNS drug delivery"},
    {"rank": 17, "contact": "17th", "name": "Henry Colecraft",           "division": "CUMC",           "why": "Ion channel biology → enDUB platform → Stablix ($63M Series A) + Flux Therapeutics; active pharma collaboration with DyNAbind"},
    {"rank": 18, "contact": "18th", "name": "Michel Sadelain",           "division": "CUMC",           "why": "Cell engineering → CAR-T (Kymriah + Breyanzi FDA-approved); co-founder Alaya.bio (SRA Jan 2025); CICET brand new"},
    {"rank": 19, "contact": "19th", "name": "Jonathan Javitch",          "division": "CUMC",           "why": "GPCR pharmacology → licensed drug discovery platform (CU15098); GPCRs are targets of ~35% of all approved drugs"},
    {"rank": 20, "contact": "20th", "name": "Gordana Vunjak-Novakovic",  "division": "BME",            "why": "Tissue engineering → four founded companies; TARA Biosystems (pharma cardiac drug testing, exclusive Columbia license); Venture Partner at Catalio Capital"},
    {"rank": 21, "contact": "21st", "name": "Ke Cheng",                  "division": "BME",            "why": "Exosome biology → Xsome Biotech + Xollent; Capricor Therapeutics licensee; two IND-enabling programs since 2023"},
    {"rank": 22, "contact": "22nd", "name": "Tal Danino",                "division": "BME",            "why": "Synthetic biology → probiotic tumor-colonizing cancer vaccine; Nature 2024; active Columbia Tech Ventures licensing (CU18339)"},
    {"rank": 23, "contact": "23rd", "name": "Harris Wang",               "division": "Computational",  "why": "Microbial engineering → SAB SNIPR Biome + Kingdom Supercultures; co-founded two companies; microbiome therapeutics emerging modality"},
    {"rank": 24, "contact": "24th", "name": "Saeed Tavazoie",            "division": "Computational",  "why": "RNA biology → Inspirna (co-founder); two drugs in Phase 1b/2 trials (RGX-104, RGX-202); $73M total raised"},
    {"rank": 25, "contact": "25th", "name": "Siddhartha Mukherjee",      "division": "CUMC",           "why": "Oncology → Manas AI CEO (launched Jan 2025, $24.6M seed); generative chemistry + docking + wet-lab for cancer drug discovery"},
    {"rank": 26, "contact": "26th", "name": "Andrea Califano",           "division": "Computational",  "why": "Computational systems biology → DarwinHealth; Daiichi Sankyo collaboration; clinical trials in 14 cancer types"},
    {"rank": 27, "contact": "27th", "name": "Parisa Yousefpour",         "division": "BME",            "why": "saRNA with drug-responsive gene expression control; next frontier beyond mRNA vaccines; joined Columbia Jan 2025"},
    {"rank": 28, "contact": "28th", "name": "Cory Abate-Shen",           "division": "CUMC",           "why": "Cancer systems biology → Selisistat (SIRT1 inhibitor) tested in mouse models; FOXM1/CENPF as druggable prostate cancer targets; NAS member"},
    {"rank": 29, "contact": "29th", "name": "Elham Azizi",               "division": "Computational",  "why": "ML for tumor ecosystem modeling and immunotherapy resistance prediction; Takeda/NYAS award (2024) signals early pharma interest"},
    {"rank": 30, "contact": "30th", "name": "Xuebing Wu",                "division": "Computational",  "why": "CRISPR + ML for RNA regulatory drug target identification; RNA-targeting small molecules one of the fastest-growing modalities; NIH New Innovator"},
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
