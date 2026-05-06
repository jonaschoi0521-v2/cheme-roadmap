# Workflow: Build and Review the Dashboard

**When to use:** After any batch of changes (end of semester, after adding several entries, weekly check-in). Not needed after every single log entry.

---

## Build

```bash
cd /Users/yuhyunchoi/JONAS-1/projects/career/pipeline/expertise
python3 tools/build.py
```

Outputs:
- `site/index.html` — main dashboard
- `site/courses.html` — full course table
- `site/roadmap.html` — timeline view
- `site/projects.html` — project log
- `site/research.html` — professors + learning resources
- `site/internships.html` — opportunities tracker

---

## Preview locally

```bash
python3 tools/serve.py
```

Opens at http://localhost:8000. Ctrl-C to stop.

---

## What to look at

**Dashboard (`index.html`):**
- Transfer prerequisites progress bar — does it match reality?
- Active projects — is anything missing?
- Upcoming deadlines — anything you forgot about?

**Courses (`courses.html`):**
- All courses visible and correctly categorized?
- Grades filled in for completed courses?

**Roadmap (`roadmap.html`):**
- Timeline makes sense for your current plan?
- Target semesters for each course still accurate?

---

## Quick check (no build needed)

For a fast terminal summary:
```bash
python3 tools/status.py
```

Use this for daily "what do I need to do?" queries without rebuilding the full site.

---

## When NOT to rebuild

- After logging a single course activity
- In the middle of a work session
- If you just want a quick status check (use `status.py` instead)

Rebuild at natural checkpoints: end of week, end of semester, after adding multiple new entries.

---

## Troubleshooting

**Missing dependency:**
```bash
pip3 install --user markdown jinja2
```

**Build produces wrong counts:** Check that `**Status:**` values are exactly from the fixed vocabulary in CLAUDE.md — no typos, no synonyms.

**Template not found:** Verify that `templates/` exists with all 6 HTML files present.
