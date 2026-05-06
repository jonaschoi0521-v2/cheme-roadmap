# Workflow: Track an Internship or Opportunity

**When to use:** The moment you identify any opportunity — internship, REU, fellowship, award, conference. Create the file immediately on identification, not when you're ready to apply.

---

## Step 1 — Create the file immediately

```
python3 tools/new_entry.py internship "Org Role Year"
```

Example: `python3 tools/new_entry.py internship "Pfizer Process Chemistry Summer 2027"`

Creates `data/internships/YYYY-MM-org-role-year.md`.

---

## Step 2 — Fill in header fields

- **Organization** — company or institution name
- **Type** — `internship` | `fellowship` | `award` | `REU` | `grant` | `conference`
- **Deadline** — exact date in YYYY-MM-DD format (this is what the dashboard uses for countdown)
- **Program Dates** — when the program runs
- **Application Portal** — URL

Set **Status** to `identified`.

---

## Step 3 — Write the first log entry

Already scaffolded — fill in how you found it and your initial impression.

---

## Step 4 — Work through the requirements checklist

The template includes a checklist. As you complete each item, check it off. Change **Status** as you progress:

`identified` → `drafting` → `submitted` → `interviewing` → `offered` / `rejected` / `accepted`

---

## Step 5 — Log every milestone

Every meaningful step gets a log entry:
- Started drafting cover letter
- Submitted
- Received interview invite
- Completed interview (what was asked, how it went, what to follow up on)
- Received decision

---

## Step 6 — Outcome notes (always write these — especially for rejections)

Even if rejected, fill in `## Outcome Notes`:
- Why you think it went the way it did
- What you would do differently
- Whether to apply again next year
- What this taught you about what to build toward

Rejection outcomes are the most valuable data in this system. Don't skip them.

---

## Deadline tracking

The dashboard and `status.py` automatically show upcoming deadlines. For this to work, `**Deadline:**` must be in `YYYY-MM-DD` format — not "October 15" or "Fall 2026."
