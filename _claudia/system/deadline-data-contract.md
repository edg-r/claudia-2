# Deadline Data Contract

This contract defines how Claudia agents pass syllabus and deadline information without turning `claudia.db` into a multi-agent free-for-all.

## Ownership

- Course agents own course interpretation. They read syllabi, Canvas notices, course files, and course memory, then write durable course-folder Markdown such as `Course Admin/syllabus_extracted.md`.
- Mnemosyne owns database normalization. Mnemosyne reads course-agent Markdown and handoffs, then writes canonical structured rows to `_claudia/claudia.db`.
- Hephaestus owns infrastructure. Hephaestus maintains migrations, dashboard code, validation scripts, and display behavior.
- Eos consumes normalized data. Daily dispatches should read the structured DB plus previous dispatch carryovers before calling a day open.
- Claudia coordinates delegation and handoffs.

## Course-Agent Handoff

Each course agent should produce or refresh:

```text
[Course Folder]/Course Admin/syllabus_extracted.md
```

That Markdown should include:

- Source files inspected.
- Assignment list with deadline date, time, timezone, weight, submission channel, and source.
- Recurring obligations and recurrence pattern.
- Exams and in-class assessments.
- Readings by week or session.
- Course policies relevant to planning, submission, AI use, late work, and grading.
- Gaps and ambiguities that need Canvas or instructor verification.

Agent memory should store durable lessons and quirks only, not the full syllabus.

## Assignment Fields

`assignments` keeps its legacy fields and adds normalized deadline metadata:

- `due_date`: local calendar date, `YYYY-MM-DD`.
- `due_time`: local due time, `HH:MM`, nullable.
- `timezone`: IANA timezone, default `America/Los_Angeles` for UCSD courses.
- `deadline_source`: source category, such as `syllabus`, `canvas`, `email`, `agent_memory`, `legacy_db`, or `inferred`.
- `source_path`: exact local path or source identifier used to verify the deadline.
- `source_confidence`: `verified`, `inferred`, `legacy`, or `ambiguous`.
- `date_kind`: `hard`, `window_end`, `recurring`, `in_class`, `opens_at`, or `ambiguous`.
- `is_recurring`: `0` or `1`.
- `recurrence_rule`: plain-language recurrence rule until an RFC5545 rule is needed.
- `opens_at`: ISO-like local datetime or date for assignments that open before they are due.
- `submitted_at`: ISO-like local datetime when Edgar confirms submission.
- `last_verified_at`: local date when Mnemosyne last verified the row.
- `external_id`: Canvas/email/event identifier when available.

## Rules

- Do not infer a due time unless the source explicitly gives one.
- If the syllabus gives a deadline window with several prompt options, use the final active option date as `due_date`, set `date_kind='window_end'`, and preserve option dates in `notes`.
- Recurring obligations must have `is_recurring=1`, `date_kind='recurring'`, and a useful `recurrence_rule`, even when they do not have individual dated rows yet.
- Canvas or email updates override syllabus dates, but the override source must be recorded.
- Daily dispatches must scan dated rows due today/tomorrow, recurring obligations, and previous-dispatch carryovers.
