---
name: theory-reference-pdf
description: "Use this skill whenever the user wants to create a structured theory reference PDF for an exam or study guide in a theory-heavy course. Triggers include: 'theory reference', 'exam reference', 'study guide with theories', 'one page per theory', 'theory cheat sheet', 'reference manual for [course]', or any request to consolidate multiple academic theories/frameworks into a single searchable PDF with consistent structure per theory. Also triggers when the user asks to produce a document where each theory gets its own page with situation, intuition, concepts, assumptions, strengths, and weaknesses. Use this skill alongside the pdf skill (for ReportLab mechanics). Do NOT use for formula-heavy quantitative reference sheets, single-topic summaries, or non-PDF outputs."
---

# Theory Reference PDF Skill

## Overview

This skill governs how to synthesize academic theories, frameworks, and readings from a theory-heavy course into a structured, exam-ready PDF reference document. It encodes patterns derived from building reference manuals for graduate policy and political economy courses.

The goal is a document a student can use during an open-book exam or as final-exam prep: fast to navigate via hyperlinked TOC and PDF bookmarks, plain in language, and complete enough that every theory the student needs is one click away.

Always use this skill alongside the `pdf` skill for ReportLab mechanics (fonts, table construction, page footers, hyperlinking). This skill governs *what to build and in what structure*; the pdf skill governs *low-level ReportLab how-to*.

---

## Step 0 — Content Inventory Before Writing Anything

Before writing a single line of PDF code, extract and catalogue every item in the source material:

```
For each source file (reading PDF, syllabus, annotated text, exam, etc.):
  1. List every distinct theory or framework
  2. Identify the author(s) and reading associated with each theory
  3. Identify the class session / week / module each theory belongs to
  4. Note the syllabus ordering — this determines page order in the reference
  5. Identify which theories are pre-midterm vs. post-midterm (or early vs. late)
  6. If an exam or past exam is provided, note the depth and style expected:
     - Does it test broad application of theories to cases? (most common)
     - Does it test technical edge cases or formal models?
     - Does it require comparing/contrasting multiple theories?
  7. Flag any theories that appear in the exam but are not in the readings (gaps)
```

**Priority rule**: If the user specifies a midterm cutoff or priority weighting (e.g., "post-midterm theories are priority"), give those theories fuller treatment. Pre-priority theories still get the identical structure but may receive slightly less elaboration in concepts and strengths/weaknesses.

**Exam calibration**: If the user provides a past exam, use it *only* to calibrate depth and framing. The exam tells you what kind of understanding is expected — typically broad application to real-world situations, not edge-case testing. Frame every theory page accordingly: anchor to a concrete real-world situation, deploy the vocabulary the student needs for applied essays.

---

## Document Structure

Every reference manual produced with this skill follows this structure:

```
1. Cover / TOC Page (single page)
   - Title, course, instructor, institution
   - Description box: what the document contains, who it's for, how it was calibrated
   - Hyperlinked Table of Contents (every theory clickable)
   - Attribution footnote at bottom of the same page (not a separate page)

2. Theory pages (one page per theory, in syllabus order)
   Each theory page has this identical structure:
   - Colored header bar with class number, theory name, author/reading
   - SITUATION — one sentence, a real-world anchor the theory explains
   - CORE INTUITION — what the theory fundamentally argues, plain language
   - KEY CONCEPTS, KEYWORDS & TERMINOLOGY — the vocabulary to deploy on an exam
   - ASSUMPTIONS — what must be true for the theory to hold
   - STRENGTHS / WEAKNESSES — two-column layout, where theory excels vs. breaks down
```

**No other sections are added unless the user requests them.** The skill is deliberately minimal: one page per theory, identical structure, no diagrams (user adds manually), no appendices unless asked.

---

## The Theory Page Template

Every theory page MUST contain all six components. Here is the specification for each:

### 1. Header Bar
A full-width colored bar containing:
- Class/session number and theory title (bold, white text)
- Author and reading citation (italic, lighter text)
- Color coding: use one color for standard theories, a different color for priority/post-midterm theories
- If priority theories are marked, include a visual tag like `[POST-MIDTERM]` or `[PRIORITY]`

### 2. SITUATION (one sentence)
A concrete, real-world case that the theory explains intuitively. This is NOT a definition of the theory — it is a *hook* that shows the theory in action.

**Good**: "This theory explains why NATO members free-ride on U.S. defense spending: the benefits of alliance security are non-excludable, so smaller members have weak incentives to contribute."

**Bad**: "This theory is about collective action problems in groups."

The situation should:
- Name a specific real-world case (drawn from the course if possible)
- Make the causal mechanism visible in one sentence
- Be memorable enough to anchor recall during an exam

### 3. CORE INTUITION (one paragraph)
What the theory is fundamentally arguing, in plain language. No jargon without immediate definition. Write for a smart person who has been away from the material for two weeks.

Requirements:
- State the core claim or mechanism
- Explain *why* the mechanism works (not just *what* it predicts)
- If the theory has a key insight that distinguishes it from similar theories, state it explicitly
- Bold key terms on first use

### 4. KEY CONCEPTS, KEYWORDS & TERMINOLOGY (bulleted list)
The vocabulary the author uses — these are the terms the student needs to deploy in an exam essay. Each entry:
- **Bold term** — plain-English definition, 1-2 sentences
- Include parenthetical examples where helpful
- Include terms that appear in the reading even if they seem obvious — exam graders look for precise vocabulary

Typical count: 5-8 terms per theory. Priority theories may have more.

### 5. ASSUMPTIONS (bulleted list)
What must be true for the theory to hold. These are the conditions under which the theory's predictions follow. Stating assumptions precisely is critical because exam questions often test "where does the theory break down?" — and breakdowns usually trace to violated assumptions.

Typical count: 3-5 assumptions per theory.

### 6. STRENGTHS & WEAKNESSES (two-column layout)
Side-by-side, each as bulleted items:
- **Strengths**: What the theory explains well. Where it has been empirically validated. What real-world phenomena it predicts that rival theories cannot.
- **Weaknesses**: Where the theory struggles or breaks down. What it ignores or assumes away. What empirical anomalies challenge it.

This is the most exam-relevant section. Exam essays almost always require identifying where a theory "fits" a case and where it "breaks down." Structure these entries to be directly deployable in an essay.

Typical count: 3-5 per column.

---

## PDF Layout and Navigation Requirements

### Hyperlinked Table of Contents
The TOC on the cover page must use internal PDF hyperlinks. Every theory entry in the TOC must be a clickable `<a href="#anchor_name">` that jumps to the corresponding theory page. Use ReportLab's `Paragraph` with `<a>` tags and a `BookmarkAnchor` flowable at each target.

### PDF Sidebar Bookmarks
Every theory page must register a named bookmark via `canv.bookmarkPage()` and `canv.addOutlineEntry()`. This creates the sidebar navigation panel in PDF readers. Users expect to be able to click through the bookmark panel without scrolling.

### BookmarkAnchor Flowable Pattern
Use this pattern for both hyperlink targets and sidebar bookmarks:

```python
from reportlab.platypus import Flowable

class BookmarkAnchor(Flowable):
    """Zero-height flowable that places a named bookmark destination."""
    def __init__(self, name, title=""):
        Flowable.__init__(self)
        self.width = 0
        self.height = 0
        self._name = name
        self._title = title

    def draw(self):
        self.canv.bookmarkPage(self._name, fit='XYZ',
            left=0, top=self.canv._pagesize[1])
        if self._title:
            self.canv.addOutlineEntry(self._title, self._name, level=0)
```

Place a `BookmarkAnchor` immediately before each theory's header bar in the story. The `name` is used as the `href` target in the TOC; the `title` appears in the PDF sidebar.

### Cover Page Layout (must fit on ONE page)
The cover page must contain ALL of the following without overflowing to page 2:
1. Document title (large, bold)
2. Course info (course code, term, instructor, institution)
3. Description box (grey background, bordered) — 2-4 sentences explaining what the document is, what it covers, who it's for
4. Hyperlinked Table of Contents — all theories listed with clickable links
5. Attribution footnote — thin rule separator, small grey text at bottom

To fit everything on one page:
- Title top margin: ~0.4 inches
- TOC entries: 9pt font, 1pt spaceBefore/After, 12pt leading
- Description box: 8pt font, compact padding (6pt top/bottom, 12pt left/right)
- Attribution: 7pt font, minimal spacing
- Reduce `spaceAfter` on subtitle styles to control vertical space

### Page Footer
Every page must have a consistent footer with document title (left) and page number (right), using the `onFirstPage` and `onLaterPages` callbacks in `SimpleDocTemplate.build()`.

### Recommended Color Scheme
```
DARK_NAVY   = "#1B2A4A"  (standard theory headers, section titles)
MED_BLUE    = "#2C5282"  (priority theory headers, TOC links)
LIGHT_BLUE  = "#EBF4FF"  (strengths column background)
ACCENT_GOLD = "#C69C3F"  (highlights, scores if used)
LIGHT_GREY  = "#F7F7F7"  (description box background)
BORDER_GREY = "#CCCCCC"  (dividers, table borders)
WARM_AMBER  = "#FFF5E6"  (weaknesses column background)
```
Users may request different colors; these are sensible defaults.

### Strengths/Weaknesses Two-Column Table Pattern
```python
col_w = (usable_width - 12) / 2
combined = [[left_items[i], right_items[i]] for i in range(max_rows)]
t = Table(combined, colWidths=[col_w, col_w])
t.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LINEAFTER', (0,0), (0,-1), 0.5, BORDER_GREY),
    ('BACKGROUND', (0,0), (0,0), LIGHT_BLUE),
    ('BACKGROUND', (1,0), (1,0), WARM_AMBER),
]))
```

---

## Attribution Footnote (required)

The attribution footnote appears at the bottom of the TOC page, separated by a thin horizontal rule (`HRFlowable` at 35% width, left-aligned). It must include:
- AI generation disclosure: "Generated with [model/tool name] via the Claudia agent system."
- Course, instructor, and institution
- Verification note: "Always verify against official course materials and readings. This document is a study aid and does not substitute for careful reading of the assigned texts."

Use 7pt grey text. **Do NOT create a separate attribution page.** The footnote on the TOC page is sufficient.

---

## Workflow Checklist

Follow these steps in order. Do not skip ahead.

```
[ ] 1. Run content inventory on all source files (extract text from all uploaded PDFs)
[ ] 2. Identify the syllabus ordering of theories
[ ] 3. Identify any priority weighting (pre/post-midterm, user-specified emphasis)
[ ] 4. If an exam is provided, analyze it for depth/framing calibration
[ ] 5. For each theory, draft all 6 components:
        - Situation (one sentence, real-world anchor)
        - Core intuition (one paragraph, plain language)
        - Key concepts (bulleted, bold term + definition)
        - Assumptions (bulleted)
        - Strengths (bulleted)
        - Weaknesses (bulleted)
[ ] 6. Build the Python/ReportLab script with:
        - Data structures for all theories (list of dicts)
        - Cover page with description, hyperlinked TOC, attribution footnote
        - Theory page builder function using the 6-component template
        - BookmarkAnchor flowables for navigation
        - Page footer function via onFirstPage/onLaterPages
[ ] 7. Generate PDF and verify:
        - Every TOC link jumps to the correct theory page
        - PDF sidebar bookmarks are present and complete
        - Cover page fits on one page (description + TOC + attribution)
        - No text overflow, no blank pages, no mid-concept splits
        - Page count = 1 cover + N theory pages
[ ] 8. Copy to /mnt/user-data/outputs/ and present to user
```

---

## Extending the Template

The user may request additional sections beyond the core theory pages. Common extensions:

- **Pre-reading / case study pages**: Summary + theory application pages for assigned readings. Use a different header bar color (e.g., green for summaries, purple for theory application). Structure: core argument, key concepts, contribution, assumptions, limitations on page A; scored theory applications on page B.
- **Cross-reference table**: A matrix showing which theories apply to which cases or readings.
- **Concept index**: An alphabetical list of all key terms across all theories, with page references.

These are add-ons. The core theory pages are always the foundation and should be built first.

---

## Common Failure Modes and Fixes

| Failure | Cause | Fix |
|---------|-------|-----|
| TOC overflows to page 2 | Too much spacing in TOC entries | Reduce font to 9pt, spaceBefore/After to 1pt, leading to 12pt |
| Hyperlinks don't work | Missing `BookmarkAnchor` or mismatched anchor names | Ensure every `<a href="#name">` has a corresponding `BookmarkAnchor(name)` |
| No sidebar bookmarks | Forgot `addOutlineEntry` | Include `title` parameter in `BookmarkAnchor` |
| Theory page overflows to 2 pages | Too many concepts or long descriptions | Reduce to 6-7 concepts; trim body text to 8-8.5pt; use compact `body_small` style |
| Strengths/weaknesses columns misaligned | Unequal row counts | Pad shorter list with empty `Paragraph("")` entries |
| Attribution on separate page | Placed after `PageBreak()` | Place before the `PageBreak()` that ends the TOC page |
| Text overflow in table cells | Raw strings instead of `Paragraph()` | Always use `Paragraph()` objects in table cells |

---

## Quality Standards

A theory reference PDF produced with this skill passes these checks:

- **Consistent structure** — every theory page has all 6 components in the same order
- **Real-world anchored** — every situation is a specific, memorable case, not an abstract definition
- **Exam-deployable vocabulary** — key concepts use the exact terms from the readings
- **Navigable** — every TOC entry is a clickable hyperlink; PDF sidebar bookmarks are complete
- **One page per theory** — strict layout discipline; no theory spans two pages
- **Single cover page** — description, TOC, and attribution all fit on page 1
- **No orphaned content** — no blank pages, no content after the last theory page (unless user requested)
- **Priority respected** — if the user specified priority theories, those receive visibly deeper treatment
