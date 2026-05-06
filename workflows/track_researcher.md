# Workflow: Track a Researcher

**When to use:** When you discover a professor or researcher whose work is relevant to ChemE, biotech, or pharma — from a class, a paper, Columbia's website, or a network contact.

---

## Step 1 — Create the file

```
python3 tools/new_entry.py researcher "First Last institution"
```

Example: `python3 tools/new_entry.py researcher "Jane Doe Columbia ChemE"`

Creates `data/research/professors/first-last-institution.md`.

---

## Step 2 — Background research (fill the file)

Go to their lab website / Google Scholar and fill in:

- **Lab** — lab name
- **Focus Areas** — 3–5 keywords (e.g., "bioreactor design, continuous manufacturing, bioseparations")
- **Website** — URL
- **Lab Research Summary** — 2–3 sentences on what they're currently working on
- **Papers of Interest** — list 2–3 papers that are most relevant to you, with one-line summaries

This should take 15–20 minutes. Do not skip it — you need this context before any contact.

---

## Step 3 — Decide whether to reach out

Ask: do I have a genuine reason to contact this person right now? Good reasons:
- I want to join their lab for undergraduate research
- I have a specific question about their work that I can't answer from the papers
- I was referred by someone in the network

Not a good reason: "I should build my network."

---

## Step 4 — Contact

Cold email template structure:
1. One sentence on who you are and your affiliation
2. One sentence on what specifically caught your attention in their research (cite a paper or project by name)
3. One sentence on why you're reaching out (research interest, lab opening, specific question)
4. Clear ask: coffee chat, lab tour, 15-minute call

Keep it under 150 words. No flattery. Be specific.

Log the contact attempt: `### YYYY-MM-DD — Email sent` with the gist of what you wrote.

---

## Step 5 — Follow up and update status

Update `**Status:**` as the relationship evolves:
- `identified` → `contacted` → `meeting-scheduled` → `active-relationship`
- If they don't respond after one follow-up: `cold`

Always fill in `## Next Action` with a specific dated item.

---

## Papers

When a paper graduates from "of interest" to "deeply relevant and read," create its own file:
```
python3 tools/new_entry.py paper "Paper title year"
```
This creates `data/research/papers/slug.md` for deeper notes.
