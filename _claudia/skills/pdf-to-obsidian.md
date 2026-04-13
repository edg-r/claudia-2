---
name: pdf-to-obsidian
description: >
  Converts PDF files into well-formatted, Obsidian-ready Markdown (.md) files.
  Use this skill whenever a user uploads a PDF — scanned book pages, articles,
  reports, or any document — and wants it converted to Markdown. Triggers on
  phrases like "convert this PDF", "extract this to markdown", "turn this into
  a note", "OCR this", "transcribe this scan", or any time a PDF is attached
  and the user wants readable, editable text output. Always use this skill when
  a PDF is involved and the output should be a .md file, even if the user just
  says "read this and save it" or "put this in my notes."
---

# PDF to Obsidian Skill

Convert PDFs — including scanned documents — into clean, well-structured Markdown
files ready to open in Obsidian. Preserve formatting, flag visual content, and
report transcription confidence when OCR is required.

---

## Step 1: Identify the PDF Type

Examine the PDF carefully before transcribing. Determine which category it falls into:

- **Text-based PDF**: Machine-generated text (research papers, digital articles, reports).
  Extraction is high-fidelity. No OCR confidence score needed.
- **Scanned PDF**: Photos or scans of physical pages. Text must be read visually.
  Assign an OCR confidence score (see Step 4).
- **Mixed PDF**: Some pages are text-based, others are scanned. Handle each page
  type appropriately and note the distinction in the frontmatter.

---

## Step 2: Extract and Structure the Content

Work through the document section by section. Apply these rules:

### Headings
- Infer heading hierarchy from font size, positioning, and context.
- Use `#` for document title (if present in body), `##` for major sections,
  `###` for subsections.
- Do not use heading levels deeper than `####` unless the source clearly warrants it.

### Body Text
- Preserve paragraph breaks.
- Italics and bold should be retained where clearly distinguishable.

### Multi-Column Layouts
- Merge into a single column in reading order (left column → right column,
  top to bottom).
- If column breaks mid-sentence across a page, reconstruct the sentence naturally.

### Tables
- Convert all tables to standard Markdown table syntax:
  ```
  | Column A | Column B | Column C |
  |----------|----------|----------|
  | value    | value    | value    |
  ```
- If a table cell is empty, use a single space or dash.
- Preserve table captions as italicized text immediately above the table:
  `*Table 1: Caption text here*`

### Footnotes and Endnotes
- Render inline footnote markers as `[^1]`, `[^2]`, etc.
- Collect all footnote text at the bottom of the document under a
  `## Footnotes` heading:
  ```
  [^1]: Footnote text here.
  ```
- If the source uses endnotes grouped by chapter, add a `### Chapter N` subheading
  under `## Footnotes`.

### Images, Figures, and Diagrams
- Do not embed images.
- Describe each figure in bracketed text on its own line:
  `> [Figure: Brief description of what the image shows — e.g., bar chart comparing GDP growth rates across 5 countries, 2010–2020]`
- Include captions if present, rendered as italicized text below:
  `*Figure 1: Caption text.*`

### Page Numbers
- Strip all page numbers from the body text. Do not render them as content.
- Record total page count in frontmatter if determinable.

---

## Step 3: Build the YAML Frontmatter

Always include a frontmatter block at the top of the .md file. Populate every
field you can detect or infer. Leave unknown fields as empty strings or omit
optional fields entirely.

```yaml
---
title: "Detected or inferred document title"
author: "Author name(s) if present"
date: "Publication or document date if present (YYYY-MM-DD format preferred)"
source: "Journal name, website, publisher, or 'Unknown'"
tags: [tag1, tag2, tag3]
document_type: "article | book_chapter | report | scan | mixed"
pages: 12
ocr_used: false
ocr_confidence: null
conversion_notes: ""
---
```

**Tag generation rules:**
- Generate 3–6 tags based on the document's subject matter.
- Use lowercase, hyphenated tags (e.g., `foreign-policy`, `drone-proliferation`).
- Include at least one topical tag, one disciplinary tag (e.g., `political-science`,
  `economics`, `history`), and one format tag (e.g., `journal-article`, `book-scan`).

**OCR fields:**
- Set `ocr_used: true` if any part of the document required visual text reading.
- Set `ocr_confidence` to your estimated accuracy percentage (see Step 4).
  For mixed documents, use the lowest confidence section as the overall figure
  and explain in `conversion_notes`.
- If no OCR was needed, set both to `null`.

**conversion_notes:**
- Use this field to flag anything unusual: illegible sections, torn pages,
  heavy watermarks, unclear column order, reconstructed sentences, etc.
- Keep it brief (1–3 sentences).

---

## Step 4: Estimate OCR Confidence (Scanned PDFs Only)

When the PDF is a scan, assess and report your confidence in the transcription
accuracy. This is your honest judgment — not a guarantee.

### Confidence Scale

| Score | Label | Meaning |
|-------|-------|---------|
| 95–100% | Excellent | Clean scan, standard font, high contrast. Very few errors expected. |
| 85–94% | Good | Minor degradation — slight blur, small font, minor skew. Occasional uncertain characters. |
| 70–84% | Fair | Noticeable issues — faded ink, handwritten marginalia, non-standard script. Some words reconstructed from context. |
| 50–69% | Poor | Significant degradation — heavy damage, very small print, unusual typography. Meaningful errors likely. |
| <50% | Unreliable | Severe scan issues. Large portions may be inaccurate. Manual review strongly recommended. |

### How to Estimate

Consider:
- **Scan clarity**: Is text sharp and high-contrast, or blurry and faded?
- **Font legibility**: Standard serif/sans-serif vs. ornate, archaic, or very small type?
- **Layout complexity**: Simple single-column prose vs. dense multi-column academic layout?
- **Language and script**: Familiar Latin characters vs. non-Latin scripts or historical orthography?
- **Damage or noise**: Torn edges, handwritten annotations, stamps, watermarks?

Report the score in the frontmatter (`ocr_confidence: 87`) and include a
one-sentence explanation in `conversion_notes` (e.g., "Scan quality is good
but small footnote text introduced some uncertainty in pp. 4–7.").

---

## Step 5: Quality Check

Before delivering the output, run a brief internal review:

1. **Completeness**: Does the document appear fully transcribed? If pages were
   skipped or unreadable, note them with `[PAGE X: Illegible]` in the body.
2. **Frontmatter validity**: Are all YAML fields syntactically correct?
   (No unescaped colons in unquoted strings, no broken lists.)
3. **Markdown rendering**: Do headings, tables, and footnote references look
   correct? Would this render cleanly in Obsidian?
4. **Footnote integrity**: Are all `[^N]` markers matched to entries in
   `## Footnotes`?
5. **Column reconstruction**: Does merged multi-column text read naturally,
   without mid-sentence breaks or duplicated content?

Fix any issues found before saving the file.

---

## Step 6: Output and Save

- Save the file as `[sanitized-title].md` — lowercase, hyphens instead of spaces,
  no special characters (e.g., `the-end-of-history.md`).
- Copy the final file to `/mnt/user-data/outputs/` and present it to the user
  using `present_files`.
- In your response to the user, include:
  - File name
  - OCR confidence score (if applicable) and what it means in plain language
  - Any notable conversion issues flagged in `conversion_notes`
  - A one-paragraph summary of the document (so the user can confirm you got the right content)

---

## Edge Cases

- **Password-protected PDFs**: Inform the user you cannot read the file and ask them to remove the password.
- **Non-English documents**: Transcribe in the source language. Add `language: "es"` (or appropriate ISO code) to frontmatter. Do not translate unless explicitly asked.
- **Very long documents (50+ pages)**: Notify the user before starting. Process in logical sections. If context limits prevent full transcription, complete as much as possible and clearly mark `[TRANSCRIPTION ENDS — page N of M]` at the cutoff point.
- **Handwritten text**: Flag explicitly with `[Handwritten: best attempt at transcription]`. Lower OCR confidence accordingly.
