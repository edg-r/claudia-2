---
name: class-one-pagers
description: Build a single Edgar-facing PDF packet with one concise prep page for each class on a given day
---

# Class One-Pagers

Use this skill when Edgar asks for "a one pager for every class today," "class prep pages," or a combined daily class packet.

## Routing

1. Ground the date with the calendar. Edgar usually means the current local date in America/Los_Angeles.
2. Identify actual class blocks only. Exclude meetings, meals, office hours, and administrative events unless Edgar explicitly asks for them.
3. Route each course section to the owning course agent. Each course agent should load its definition, `AGENT_CONTEXT.md`, `FEEDBACK.md`, and selective `TASK_LOG.md`, then return a concise section.
4. Each course agent should update its `TASK_LOG.md` with the work and output as "returned to Claudia for combined Edgar document."
5. Claudia assembles the final packet and saves it in `edgar/` unless Edgar names another destination.

## One-Page Section Shape

Each course section should include:

- Full course code and title as the heading.
- Today's likely focus.
- BLUF.
- Key concepts.
- 3-5 discussion-ready points.
- Due / bring-up items, including ambiguity when visible.

Keep each course concise enough to fit roughly one printed page when possible. Do not invent submission status if local files or connectors do not show it.

## Preferred PDF Layout

For Edgar-facing daily class packets, default to:

- PDF as the final deliverable when Edgar asks for a document or PDF packet.
- Keep the Markdown source in `edgar/` unless Edgar asks to delete it.
- Do not leave intermediate HTML or DOCX files in `edgar/` after final PDF generation unless Edgar asks for them.
- Title page allowed and preferred for multi-class packets.
- Put provenance/disclosure on the title page, not at the end.
- Times New Roman, 12 pt body text.
- 0.5 inch margins on all sides.
- 1.25 line spacing.
- Hard page break before every class heading so each class starts on its own page.
- Suppress browser-generated headers and footers in the PDF.

## Title Page Provenance

Use this title-page block after the schedule summary:

```text
Generated for: Edgar Agunias
Date: YYYY-MM-DD
Model: [model/session provenance]
Sources: [calendar, course-agent handoffs, local course folders, syllabus extracts, assignment trackers, study guides, reading notes, or other inputs]
Agent: Claudia, with [contributing agents]
```

This satisfies the output-disclosure SOP for this class-packet format.

## PDF Generation Notes

If `xelatex`, `typst`, or `wkhtmltopdf` are unavailable, render Markdown to temporary HTML with Pandoc and use installed Google Chrome headless printing:

```bash
pandoc edgar/YYYY-MM-DD_class_one_pagers.md -o scratch/pdf_render/YYYY-MM-DD_class_one_pagers.html --standalone
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless --disable-gpu --no-first-run \
  --user-data-dir="$(pwd)/scratch/chrome-profile" \
  --print-to-pdf="$(pwd)/edgar/YYYY-MM-DD_class_one_pagers.pdf" \
  "file://$(pwd)/scratch/pdf_render/YYYY-MM-DD_class_one_pagers.html"
```

Prefer a tiny scratch print script when custom CSS is needed. Keep generated scratch files out of `edgar/`.

## Verification

Before final handoff:

1. Confirm the PDF exists and is readable.
2. Check the page count and first text on each page with `pypdf` or `PyPDF2`.
3. Verify page 1 is the title/provenance page.
4. Verify each class starts on its own page.
5. Verify no unwanted `.html` or `.docx` files remain in `edgar/` when Edgar asked for PDF only.
