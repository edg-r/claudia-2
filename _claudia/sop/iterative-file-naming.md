---
name: iterative-file-naming
description: Versioned naming convention for drafts and other iterated files
applies_to: all agents
---

# Iterative File Naming

When a document, script, deck, spreadsheet, or other artifact will move through multiple AI/human revision passes, use software-style versions instead of state-only suffixes such as `_DRAFT`, `_REVISED`, `_FINAL_REVIEW`, `_MACRO_REWRITE`, or `_TRACKED` as the primary identifier.

## Core Pattern

```text
[project_slug]_vMAJOR.MINOR.PATCH[_channel][_short_note].[ext]
```

Example:

```text
Orange_Memo_Myanmar_v1.2.0_tracked_macro-rewrite.docx
```

## Version Meaning

- `MAJOR`: argument, structure, scope, or deliverable format changes. Use this when the file is no longer just a refinement of the prior draft.
- `MINOR`: substantive improvements inside the same architecture. Use this for added evidence, theory tightening, section rewrites, or instructor-feedback integration.
- `PATCH`: light corrections. Use this for typo fixes, citation cleanup, formatting, word-count trimming, or small line edits.

## Channel Suffixes

Use optional channel suffixes after the version when they clarify the artifact's role:

- `_source`: untouched user-provided original.
- `_working`: live editable copy.
- `_tracked`: Word tracked-changes copy.
- `_clean`: accepted-changes / no-markup copy.
- `_submission`: exact file intended for upload.
- `_archive`: retained for context, not a live candidate.

The version is the source of ordering truth. The channel only describes the file's role.

## Practical Rules

1. Never use `_FINAL` unless the file is actually submitted or frozen. Prefer `_submission`.
2. Keep one current candidate obvious: the highest version with `_working`, `_clean`, or `_submission`.
3. Preserve originals as `v0.1.0_source` or `v1.0.0_source` depending on whether the original is pre-draft material or Edgar's first complete draft.
4. When changing the direction of the piece, bump `MAJOR`; when improving the same direction, bump `MINOR`; when only polishing, bump `PATCH`.
5. If an existing folder already contains state-only names, create a short `VERSION_MAP.md` before renaming or continuing the sequence.

## Archiving Superseded Versions

When a newer version supersedes older iterative artifacts, keep the latest active candidate visible and move older generated versions to the owning course's local artifact archive:

```text
[Course Folder]/.archive/<project_slug>/
```

Record the move in `[Course Folder]/.archive/ARCHIVE_INDEX.md`. Follow `_claudia/sop/artifact-archive.md` for what stays visible, what gets archived, and how to restore older files.

Do not use `_archive` folders for new cleanup work. Use the course root `.archive/` folder so the context stays local to the owning course agent while remaining hidden from normal folder browsing.

## Myanmar Memo Example

Current confusing style:

```text
Orange_Memo_Myanmar_ORIGINAL.docx
Orange_Memo_Myanmar_DRAFT.docx
Orange_Memo_Myanmar_TRACKED.docx
Orange_Memo_Myanmar_FINAL_REVIEW.docx
Orange_Memo_Myanmar_MACRO_REWRITE.docx
```

Clear versioned style:

```text
Orange_Memo_Myanmar_v1.0.0_source.docx
Orange_Memo_Myanmar_v1.1.0_working.docx
Orange_Memo_Myanmar_v1.1.0_tracked.docx
Orange_Memo_Myanmar_v1.2.0_clean_strategic-choice.docx
Orange_Memo_Myanmar_v2.0.0_working_macro-rewrite.docx
Orange_Memo_Myanmar_v2.0.1_submission.docx
```

In this example, the macro rewrite becomes `v2.0.0` because it changes the architecture of the memo, not merely the wording.
