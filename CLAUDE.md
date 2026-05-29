# Agent Instructions — ChemE Roadmap

This is Jonas Choi's personal academic and career roadmap. WAT framework — see `~/JONAS-1/CLAUDE.md` for the full architecture.

## About Jonas

Columbia College freshman planning to transfer internally to **SEAS Chemical Engineering** at the end of Semester II (Spring 2027). Studying ChemE not as an end in itself, but as the most direct path to the dream below.

**The dream:** *"Could you patent the Sun?"* — Jonas Salk's reply when asked who owned the polio vaccine. Jonas wants to build pharma and biotech for underserved populations: medicines, diagnostics, and infrastructure that reach the people most existing systems leave behind. Every course, project, lab, and internship in this roadmap is a step toward that.

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
