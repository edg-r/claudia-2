---
name: lecture-to-reference-pdf
description: "Use this skill whenever the user wants to synthesize lecture slides, course notes, or assignment solutions into a structured reference PDF or study guide. Triggers include: 'make a reference manual', 'turn these slides into a study guide', 'summarise this course material', 'build a cheat sheet from', 'create a reference document', or any request to consolidate academic/technical material into a polished PDF. Also use when updating or adding sections to an existing reference manual. Use this skill alongside the pdf skill (for ReportLab mechanics). Do NOT use for single-page summaries, blog posts, or non-PDF outputs."
---

# Lecture-to-Reference-PDF Skill

## Overview

This skill governs how to synthesise lecture slides, course notes, and assignment solutions into a structured, exam-ready reference PDF. It encodes the priorities and patterns derived from building the GPCO 415 Final Exam Reference Manual across multiple iterations.

The goal is a document a student can use during an open-book exam: fast to navigate, plain in language, and complete enough that they never need to flip back to raw slides.

Always use this skill alongside the `pdf` skill for ReportLab mechanics (fonts, table construction, page footers, hyperlinking). This skill governs *what to build*; the pdf skill governs *how to build it*.

---

## Step 0 — Content Inventory Before Writing Anything

Before writing a single line of PDF code, extract and catalogue every item in the source material:

```
For each source file (lecture PDF, assignment solution, etc.):
  1. List every formula or equation
  2. List every defined term or abbreviation
  3. List every worked example or solved problem
  4. Note which assignment/exam question each item connects to
  5. Flag anything that appears in problems but is never explicitly defined
     (these are gaps — foundational content that must be added)
```

**Do not skip this step.** The most common failure mode is producing a PDF that mirrors the slides without noticing what the slides assume the student already knows. Gaps in the source material become gaps in the reference document unless you catch them here.

Common gap categories to watch for:
- Abbreviations used in formulas without a decoder (A/R, COGS, SG&A, DIO, etc.)
- Derived quantities that appear in solutions but have no formula shown (e.g. Purchases = COGS − ΔInventory)
- Period-adjustment rules (quarterly vs annual, monthly vs annual) stated only in passing
- Income statement and balance sheet line item definitions assumed as prior knowledge

---

## Document Structure Template

Every reference manual produced with this skill follows this structure:

```
1. Cover page
   - Title, course, instructor, institution
   - "Generated with [model/tool name] via the Claudia agent system" attribution
   - Clickable Table of Contents (all sections hyperlinked)
   - No version history on the final release

2. Core equation reference sections (one section per topic cluster)
   Each section contains:
   - The formula (using ReportLab Paragraph with proper markup, never raw strings)
   - Plain-English explanation (what it measures, what each variable means)
   - Period-awareness note if the formula changes for sub-annual data
   - Excel function or implementation note
   - Exam anchor (which specific assignment/question tests this)

3. Worked example sections
   - Tied to real numbers from actual assignments or exams
   - Show the full calculation chain, not just the final answer
   - Include "show my work" copy-paste blocks for formula chains

4. Abbreviation / decoder tables
   - One consolidated table per topic area
   - Columns: Abbreviation | Full Name | Plain-English Meaning
   - Every acronym that appears anywhere in the document must appear here

5. Framework / problem-type guide
   - Maps exam question types to the correct solution procedure
   - Concrete examples: "If the question says X, use approach Y"

6. Appendix
   - Supplementary or reference-only material (checklists, lookup tables)
   - Material that supports but doesn't need to be in the main flow

7. Attribution page
   - Course, instructor, institution
   - AI generation disclosure
   - "Always verify against official course materials" note
```

---

## The Three-Layer Rule

**Every formula must have all three layers before it ships:**

| Layer | What it is | Example |
|-------|-----------|---------|
| 1. Formula | The mathematical expression | `Payback = L + (−O_before) / (O_after − O_before)` |
| 2. Plain English | What it does, in one sentence | "The last full negative year, plus the fraction of the recovery year needed to reach zero." |
| 3. Exam anchor | Where it appears in the course | "Used in A7-P1 New Roots and A7-P5 Bangladesh Bridge." |

If any layer is missing, add it. Do not ship a formula that only has layer 1.

---

## Plain Language Standards

Write explanations the way you would explain something to a smart person who has been away from the material for two weeks.

**For every formula component:**
- State what the variable *is* (not just its symbol)
- State what it *measures* in the real world
- State what happens when it increases or decreases

**For ratios and metrics:**
- State the direction of "better" (e.g. "shorter CCC = more efficient")
- Anchor to a real-world intuition (e.g. "DPO = how many days before you pay your suppliers")
- Include a one-sentence interpretation of an extreme value

**Prohibited phrases:**
- "As can be seen from the formula..." (redundant)
- "It is important to note that..." (filler)
- Any explanation that just restates the formula in words without adding meaning

---

## Copy-Paste Formula Blocks

Any time there is a sequential formula chain (where outputs of step N feed into step N+1), produce a copy-paste block in `variable|formula` format alongside the worked example table.

**Format:**
```
# SECTION HEADING
VariableName|=ExcelFormula
VariableName2|=ExcelFormula using VariableName
```

**Rules:**
- Variable names must match the spreadsheet column/cell naming convention the user uses
- Use `=` prefix on all formulas to signal Excel entry
- Group by logical step with `# comment` headers
- Always include an annual and quarterly variant when the formula involves a time period (replace `365` with `(365/4)` for quarterly)
- The block must be inside a styled table using per-line `Paragraph()` objects — never use `Preformatted()` or raw strings, as these do not wrap and will overflow the page

**Example block (working capital, quarterly):**
```
# STEP 1 - DERIVED INPUT
Purchases|=COGS - ChangeInInventory

# STEP 2 - TURNOVER RATIOS
InventoryTurnoverRatio|=COGS / AverageInventory
AccountsReceivableTurnoverRatio|=Revenue / AvgAccountsReceivable
AccountsPayableTurnoverRatio|=Purchases / AvgAccountsPayable

# STEP 3 - DAYS RATIOS  (quarterly: 365/4)
DIO|=(365/4) / InventoryTurnoverRatio
DSO|=(365/4) / AccountsReceivableTurnoverRatio
DPO|=(365/4) / AccountsPayableTurnoverRatio

# STEP 4 - CYCLE SUMMARIES
OperatingCycleDays|=DIO + DSO
CashConversionCycle|=DIO + DSO - DPO
```

---

## Period-Awareness Rule

Whenever a formula involves a time-based denominator (days, months, quarters), explicitly state the adjustment rule:

| Data frequency | Replace | With |
|----------------|---------|------|
| Annual | — | 365 |
| Quarterly | 365 | 365/4 = 91.25 |
| Monthly | 365 | 365/12 ≈ 30.4 |

State this rule in a callout box (italicised tip paragraph) immediately before the formula table where it applies. Do not bury it in a footnote.

---

## ReportLab Layout Rules

These rules prevent the most common rendering failures. Apply all of them unconditionally.

### Cell content — always use Paragraph objects

```python
# WRONG — raw strings in table cells cause overflow
row = [["Net PPE", "Gross PPE - Accumulated Depreciation", "Midterm Q7"]]

# RIGHT — Paragraph objects wrap correctly within column width
from reportlab.platypus import Paragraph
row = [[
    Paragraph("Net PPE", style),
    Paragraph("Gross PPE \u2212 Accumulated Depreciation", style),
    Paragraph("Midterm Q7. Shows remaining book value.", style),
]]
```

### Column width validation

Before building any table, verify that the longest cell content fits:

```python
# Rule of thumb: Helvetica 8.5pt ≈ 5.5px per character
# Paragraph() wraps automatically, but the cell must be wide enough for ≥1 word
# Minimum column width = longest single word in that column × 5.5pt + 12pt padding

# For a 3-column table on letter with 1in margins (6.5in = 468pt usable):
# Apportion widths based on content type:
# - Short labels (item names): 0.8–1.1 in
# - Formulas (medium): 1.8–2.2 in
# - Explanatory text (longest): remaining width
```

### KeepTogether on logical blocks

Wrap every logical block in `KeepTogether` to prevent mid-concept page breaks:

```python
from reportlab.platypus import KeepTogether

# Each "step" block = header row + formula rows → keep together
step_block = KeepTogether([header_table, formula_row_1, formula_row_2])
story.append(step_block)

# Copy-paste section = heading + hint + code table + footer note → keep together
copy_paste_block = KeepTogether([heading, hint_para, code_table, Spacer(1,6), note_para])
story.append(copy_paste_block)
```

### Hyperlinked Table of Contents

Use a `TrackingDoc` to capture TOC row positions during the build pass, then add `Link` annotations in a second pass with `pypdf`:

```python
from reportlab.platypus import SimpleDocTemplate
from pypdf.annotations import Link
from pypdf.generic import Fit

class TrackingDoc(SimpleDocTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toc_positions = {}
        self._cur_page = 0

    def handle_pageBegin(self):
        self._cur_page += 1
        super().handle_pageBegin()

    def afterFlowable(self, flowable):
        if hasattr(flowable, '_toc_key'):
            bottom_y = self.frame._y
            rh = sum(flowable._rowHeights) if (
                hasattr(flowable, '_rowHeights') and flowable._rowHeights) else 14
            self.toc_positions[flowable._toc_key] = {
                'page': self._cur_page - 1,
                'rect': (self.frame._x1, bottom_y, self.frame._x2, bottom_y + rh)
            }

# Mark each TOC row with a key
toc_row._toc_key = "1A."

# After assembling the full PDF with pypdf:
for section, info in doc.toc_positions.items():
    annotation = Link(
        rect=info['rect'],
        target_page_index=toc_targets[section],
        fit=Fit.fit()
    )
    writer.add_annotation(page_number=info['page'], annotation=annotation)
```

### Footer consistency

Every page must have a consistent footer showing the document title and page number:

```python
def make_footer(page_num, title="Reference Manual"):
    def _footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.grey)
        canvas.drawString(1*inch, 0.5*inch, title)
        canvas.drawRightString(W - 1*inch, 0.5*inch, f"Page {page_num}")
        canvas.restoreState()
    return _footer
```

### Avoid these common failures

| Failure | Cause | Fix |
|---------|-------|-----|
| Text overflows table cell | Raw string instead of `Paragraph()` | Always use `Paragraph()` |
| Content splits mid-concept across pages | No `KeepTogether` | Wrap every logical block |
| Copy-paste block renders blank | `Preformatted()` or line-level strings | Use per-line `Paragraph()` in a `Table` |
| Side-by-side columns overlap | ReportLab renders two-table layout as one | Use a 6-column single table with spacer columns |
| TOC links point to wrong page | Page index off-by-one after inserting pages | Recalculate all `toc_targets` after final assembly |
| Subscripts render as black boxes | Unicode subscript characters (₁₂₃) | Use `<sub>` tags in `Paragraph()` |

---

## Versioning and Attribution

### During development
- Use a version suffix in the filename: `Manual_v2.pdf`, `Manual_v3.pdf`
- Include a version history table on the cover page showing: version, what was added, page count
- Tag new sections in the TOC with `[v#]` in blue text

### On final release
- Remove the version history table from the cover
- Keep the version number in the filename for reference
- Add to the attribution page: "Generated with [model/tool name] via the Claudia agent system"
- Add: "Always verify formulas against official course materials"

---

## Workflow Checklist

Follow these steps in order. Do not skip ahead.

```
[ ] 1. Run content inventory on all source files
[ ] 2. Identify gaps — terms used but never defined
[ ] 3. Draft the section outline (which sections, what order)
[ ] 4. For each formula: write all three layers (formula, plain English, exam anchor)
[ ] 5. Identify all abbreviations → build decoder table
[ ] 6. Identify all formula chains → write copy-paste blocks
[ ] 7. Note any period-adjustment rules → add callout boxes
[ ] 8. Build PDF pages using Paragraph() cells, KeepTogether blocks
[ ] 9. Validate: open PDF, check for text overflow, blank blocks, mid-concept splits
[ ] 10. Assemble final document in correct page order
[ ] 11. Add TOC hyperlinks via TrackingDoc + pypdf annotations
[ ] 12. Update cover (version history or clean final cover as appropriate)
[ ] 13. Update attribution page
[ ] 14. Final check: every TOC entry links to the correct page
```

---

## Quality Standards

A reference manual produced with this skill passes these checks:

- **No orphaned formulas** — every formula has a plain-English explanation
- **No undefined abbreviations** — every acronym appears in a decoder table
- **No missing foundations** — any concept used in worked examples is explicitly defined
- **No layout failures** — no text overflows, no blank copy-paste blocks, no mid-concept page breaks
- **No generic examples** — every worked example uses real numbers from the actual course
- **Period-explicit** — any formula involving time states both the annual and sub-annual variants
- **Fully navigable** — every TOC entry is a clickable hyperlink to the correct page
