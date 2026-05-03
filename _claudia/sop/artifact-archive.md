---
name: artifact-archive
description: Course-local archive protocol for superseded iterative artifacts
applies_to: all agents
---

# Artifact Archive Protocol

Use course-local hidden archives to keep Edgar's visible course folders clean while preserving rollback paths inside the owning agent's course context.

## Archive Location

Superseded AI-generated or iterative artifacts belong under:

```text
[Course Folder]/.archive/<project_slug>/
```

Each course-local archive index lives at:

```text
[Course Folder]/.archive/ARCHIVE_INDEX.md
```

## What Stays Visible

Keep these in the ordinary course folder:

- latest active `_working`, `_clean`, or `_submission` candidate
- final submitted files
- source readings and professor-provided files
- current build scripts needed to regenerate the visible artifact
- small README, VERSION_MAP, or notes files that explain active work

## What Gets Archived

Move these to the course-local archive when superseded:

- older AI-generated drafts
- older generated PDFs and notes sidecars for the same deliverable
- tracked-change variants after a clean or submission copy exists
- failed or partial build outputs
- older build scripts tied to archived generated versions
- intermediate exports retained only for rollback or provenance

Do not archive source readings, syllabi, professor handouts, or Edgar's final submitted file unless Edgar explicitly asks.

## Index Entries

Every archive family should have an entry in the owning course's `.archive/ARCHIVE_INDEX.md` with:

- course code
- project slug
- current visible path or paths
- archive path
- reason archived
- restore guidance

When an archive grows large, Mnemosyne may mirror the index into SQLite, but the course-local Markdown index remains the human-readable source of truth.

## Restore Guidance

To restore an archived file, copy it from the archive path back to the relevant working folder. Do not move it out of the archive unless Edgar explicitly wants the archive entry removed.

Example:

```bash
cp "GPCO 410 - Intl Pol:Sec - Praether/.archive/orange_memo_myanmar/Orange_Memo_Myanmar_v3.1.0_working_cederman-actor-preferences.docx" \
  "GPCO 410 - Intl Pol:Sec - Praether/Assignments/Orange Memo - Myanmar/"
```

## Git and Binary Files

Git history is useful, but it is not enough for rollback because many high-value artifacts are binaries or may be ignored unless explicitly added. Keep archived binaries in the course-local archive. When Edgar asks to save or publish a specific PDF, DOCX, PPTX, or XLSX, verify whether it is ignored and use scoped `git add -f` only for the requested artifact.

## Agent Responsibilities

- Course agents should check their local `.archive/ARCHIVE_INDEX.md` before recreating old versions.
- Mnemosyne owns discovery and indexing conventions for archived artifacts.
- Hephaestus owns scripts and mechanical cleanup when archive moves are requested.
- Calliope should check the archive before restoring older drafts, tracked copies, clean copies, or review notes.
- Claudia should keep archive changes scoped and avoid sweeping unrelated dirty files into a save.
