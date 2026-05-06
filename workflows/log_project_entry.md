# Workflow: Log a Project Entry

**When to use:** Starting a new project, logging progress on an existing one, or recording an outcome.

---

## Starting a new project

1. **Create the file:**
   ```
   python3 tools/new_entry.py project "descriptive name"
   ```
   Creates `data/projects/YYYY-MM-descriptive-name.md`.

2. **Fill in the header:**
   - **Type:** `research` | `class` | `personal` | `collaboration`
   - **Status:** starts as `ideation` — change to `active` when you begin working
   - **Mission Relevance:** one sentence connecting this project to pharma/biotech for underserved populations. If you can't write this sentence, ask whether this project belongs in this system.

3. **Write the first log entry** (already scaffolded — fill it in).

4. **Update `data/projects/_index.md`:** Add a row.

---

## Logging ongoing progress

1. Find the project file in `data/projects/`
2. Scroll to the bottom of `## Log`
3. Append:
   ```
   ### YYYY-MM-DD — What happened

   Narrative: what you did, what you found, what surprised you, what's next.
   ```
4. **Never edit past entries.** They are an immutable record.

---

## Closing a project

1. Change `**Status:**` to `completed` (or `abandoned` / `paused` with a reason)
2. Fill in `**Completed:**` with today's date
3. Fill in `**Outcome:**` with what was produced
4. Write a final log entry summarizing what you learned and what you'd do differently

---

## Log entry discipline

The log is the most valuable part. Write entries in real time — not reconstructed a week later.

Good log entry: *"Ran the synthesis at 60°C as planned. Yield was 34%, lower than expected. Checked protocol — realized I used 1.2 equivalents instead of 1.5. Will rerun tomorrow with corrected amount."*

Bad log entry: *"Worked on the project."*
