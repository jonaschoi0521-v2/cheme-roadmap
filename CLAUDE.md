# Agent Instructions — ChemE Roadmap

This is Jonas Choi's personal academic and career roadmap. WAT framework — see `~/JONAS-1/CLAUDE.md` for the full architecture.

## About Jonas

Columbia College student. **Decided major: Chemical Physics** (not transferring to SEAS ChemE — Chemical Physics gives the deeper molecular foundation needed for the path below). Treating CS as a de facto second major through coursework and self-study.

**The dream:** *"Could you patent the Sun?"* — Jonas Salk's reply when asked who owned the polio vaccine. Jonas wants to build pharma and biotech for underserved populations: medicines, diagnostics, and infrastructure that reach the people most existing systems leave behind. Every course, project, lab, and internship in this roadmap is a step toward that.

**The path:** Founder, not scientist-employee. The goal is to build a platform company — the infrastructure that creates medicines, not just to discover one drug inside someone else's system. This requires builder-level scientific depth, not user-level. Being a cheminformatics scientist at a pharma company is not the goal.

**Builder vs. User — critical distinction, do not conflate:**

*User* — a computational medicinal chemist or cheminformatics scientist who applies existing platforms (Schrödinger, AlphaFold, RDKit) to find drugs inside someone else's program. Deep scientific judgment, but works within tools others built. Career ceiling: senior/principal scientist or director at pharma/biotech. Does not control the platform. **This is not Jonas's goal.**

*Builder* — someone who creates the computational tools and platforms others use. Requires implementation-level depth in ML (graph neural networks, generative models, equivariant architectures), physics-based simulation, and software engineering. Examples: Friesner built FEP+/Schrödinger, Coley built synthesis planning systems, the Boltz-2 team built a model that approaches FEP+ accuracy at 1000× speed. **This is the required depth level — but Jonas's end goal is not to be a pure builder either.**

*Jonas's actual target* — scientific entrepreneur who has builder-level depth. Understands the frontier well enough to see a platform-level gap others don't see, then founds the company around it. Friesner didn't just write algorithms — he built Schrödinger. Sames didn't just study ibogaine — he co-founded Gilgamesh. Builder depth is the prerequisite for founder credibility, not the destination. The destination is the platform company itself.

**The sequencing:**
1. Chemical Physics major + aggressive CS self-study (treat as second major — daily coding starting now)
2. PhD at the right computational lab (Friesner, Coley, or equivalent) — a means to scientific credibility and frontier insight, not the destination
3. Early role inside a serious platform company — learn how these things scale
4. Found the platform

**The financial framing:** Willing to earn below $100K for years during the PhD and early founding period. The target outcome is equity — founding or being early enough at the right company. Salary is not the metric.

This system is how the dream stays accountable to itself — what's been done, what's next, and what's still missing.

## Data architecture

Source of truth lives in `data/`. Each entity = one markdown file.

| Directory | What's in it |
|---|---|
| `data/courses/` | One file per course |
| `data/projects/` | One file per project (research, class, personal) |
| `data/research/professors/` | Professors and labs of interest |
| `data/research/papers/` | Papers worth tracking |
| `data/research/opportunities/` | REUs, lab openings, conferences |
| `data/learning/` | Textbooks, online courses, workshops |
| `data/internships/` | Applications, fellowships, awards |

## Status vocabulary

The build tool reads these literally. Use exact strings — no synonyms.

- **Courses:** `planned` | `in-progress` | `completed` | `waived`
- **Projects:** `ideation` | `active` | `paused` | `completed` | `abandoned`
- **Researchers:** `identified` | `contacted` | `meeting-scheduled` | `active-relationship` | `cold`
- **Internships:** `identified` | `drafting` | `submitted` | `interviewing` | `offered` | `rejected` | `accepted` | `withdrawn`
- **Learning:** `identified` | `in-progress` | `completed` | `paused`

## Core operations

```bash
python3 tools/new_entry.py <type> "<name>"   # course | project | researcher | internship | learning
python3 tools/build.py                        # rebuild site/ (for local check only)
```

Dashboard is deployed via GitHub Pages — push to `main` to publish.

When status changes, update the `**Status:**` field too.

## Change Workflow

Follow this process for every modification, no matter how small.

**Step 1 — Build locally**
Run `python3 tools/build.py` to regenerate `site/` from scratch.
Every change across all files (`data/`, `templates/`, `static/`) is reflected.
Then `python3 tools/serve.py` — kills any previous server, finds the next free port, and auto-opens the browser. Run this after every change to preview.

**Step 2 — Review and selectively stage**
Browse the local preview. Stage only the files you want to push:
- `git add path/to/file` to accept a change
- Leave unstaged to reject it

**Step 3 — Push final changes**
Do not push without explicit user consent. Before committing, scan staged files for sensitive info (emails, phone numbers, passwords, personal IDs, API keys). Present the staged changes and wait for approval before running:
```bash
git commit -m "describe what changed"
git push
```

**Step 4 — Verify live URL**
Wait ~1 min, then check https://jonaschoi0521-v2.github.io/cheme-roadmap

## Automation Infrastructure

- **GitHub repo:** `jonaschoi0521-v2/cheme-roadmap` (public)
- **Live URL:** https://jonaschoi0521-v2.github.io/cheme-roadmap
- **Git auth:** SSH via `github-v2` host alias (`~/.ssh/id_ed25519_v2`)
- **Remote:** `git@github-v2:jonaschoi0521-v2/cheme-roadmap.git`
- **Deploy action:** `peaceiris/actions-gh-pages@v3` → pushes `site/` to `gh-pages` branch
- **Pages source:** Deploy from branch → `gh-pages`, `/ (root)`

## Constraints

- **Visa:** F-1 international student — eliminates Goldwater, NSF GRFP, Churchill, Hertz, and most US-only fellowships when tracking opportunities
- **Presidential Scholarship:** sole-scholarship clause — no additional scholarships; fellowships, prizes, competitions, and research grants are fine

## Rules

1. **"Active projects: 0" is correct behavior** when all projects are in `ideation` status — not a bug. Update status to `active` when work actually begins.
2. **`site/` is build output.** Never edit by hand.
3. **One entity per file.** Never combine two courses or two projects.
4. **Filenames are stable.** Once created, don't rename.
5. **Never push `private/` or `research/`.** These are gitignored — keep them local only.
6. **Course changes always touch both files.** When adding, removing, or switching a course between semesters: update the course's `data/courses/<file>.md` (Semester field) AND `templates/registration.html` (the correct semester table). Also update `private/course-plan/chem-phy/chemical-physics-semester-schedule.md` if the semester totals change. Never update only one without the others.
