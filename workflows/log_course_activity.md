# Workflow: Log Course Activity

**When to use:** After a class session, problem set, exam, or any course-related activity you want to capture.

---

## Inputs

- Which course (name or code is fine)
- What happened / what you want to log
- Whether the status changed (e.g., course started, exam completed)

---

## Steps

1. **Identify the file.** In `data/courses/`, find the file for that course. Filenames follow `dept-code-slug.md` (e.g., `math-un1101-calculus-1.md`).

2. **Find the `## Log` section.** Scroll to the end of the log — new entries always go at the bottom.

3. **Append a new dated block:**
   ```
   ### YYYY-MM-DD — Brief title

   What happened. What confused you. What clicked. What the next step is.
   ```

4. **Never edit past entries.** The log is append-only. Past entries are immutable.

5. **Update status if needed:**
   - Starting a course for the first time → change `planned` to `in-progress`
   - Just finished the course → change `in-progress` to `completed`, fill in the `**Grade:**` field

---

## Voice-to-log usage

Say something like: *"Log for General Chemistry 1 — today we covered periodic trends and electronegativity. I'm confused about why ionization energy dips at Group 15. Next step: re-read section 8.3."*

Claude will find the right file and append the entry.

---

## What to log

- Key concepts covered
- Things that confused you
- Connections to other courses or to the pharma/biotech mission
- Exam results and reflections
- Professor comments worth keeping
- Next action (reading, problem set, office hours)

## What NOT to log here

- Full lecture notes → put those in `lecturenote/`
- Problem set solutions → keep in your course folder
