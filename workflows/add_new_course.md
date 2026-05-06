# Workflow: Add a New Course

**When to use:** When you're enrolling in a course, planning a future semester, or adding a course you already took that isn't yet in the system.

---

## Option A — Course from the degree track (already scaffolded)

All degree-track courses (from the Columbia ChemE PDFs) already exist as files in `data/courses/`. To activate one:

1. Open the file (e.g., `data/courses/chem-un1403-general-chemistry-1.md`)
2. Change `**Status:** planned` to `**Status:** in-progress`
3. Fill in `**Semester:**`, `**Professor:**`, and `**Location:**` if known
4. Write a log entry: `### YYYY-MM-DD — Enrolled`
5. Update `data/courses/_index.md` — change the Status column for that row

---

## Option B — Course NOT on the standard degree track

1. **Scaffold a new file:**
   ```
   python3 tools/new_entry.py course "Course Name"
   ```
   This creates `data/courses/slugified-name.md` with the standard template.

2. **Fill in the header fields:** code, semester, credits, what requirement it fulfills, professor.

3. **Update `data/courses/_index.md`:** Add a row to the appropriate table.

4. **Write a first log entry:** Mark the date you enrolled or started.

---

## Naming convention

Files follow `dept-code-description.md`:
- `chen-e3110-transport-phenomena-1.md`
- `chem-un1403-general-chemistry-1.md`

Once created, **never rename** — filenames are stable identifiers.

---

## What to fill in immediately

- Status, Semester, Credits, Fulfills, Professor
- "Why This Course Matters" — one paragraph connecting this course to your ChemE or pharma/biotech goals

## What to fill in over time

- Key Concepts (update as the course progresses)
- Resources Used
- Connections to other courses or projects
- Log entries after each significant session
