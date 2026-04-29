---
name: ai-disclosure
description: Edgar-to-grader disclosure appended to any graded submission where a Claudia agent produced, edited, or materially assisted the work
applies_to: Edgar (author disclosure on submitted work)
---

# AI Use Disclosure (Edgar-to-Grader)

When Edgar submits work for a grade and any Claudia agent produced, edited, reviewed, or materially assisted the content, the submission must carry a disclosure block addressed to the grader. This SOP specifies the substance, placement, and template.

This SOP is distinct from `output-disclosure.md`. That SOP covers agent-to-Edgar provenance, which is internal to the Claudia system. This SOP covers author-to-grader disclosure, which leaves the system and goes to a UCSD instructor.

## Source Framing

The language is grounded in the general academic-integrity principle that AI-assisted work must not be submitted without proper permission, attribution, and author review. UCSD and the Graduate School of Global Policy and Strategy do not prescribe a campus-wide student disclosure template as of April 2026. The Academic Integrity Office directs students to follow the instructor's course-level AI policy. Edgar's disclosure must therefore be compatible with any instructor policy stated in the syllabus. If a syllabus forbids AI use for a given assignment, no disclosure is sufficient, and the agent pipeline should not be used for that assignment at all.

## When the Disclosure Is Required

Attach the disclosure to any assignment submitted for a grade when any of the following is true:

- A Claudia agent drafted any portion of the submitted prose, code, tables, charts, or slides.
- A Claudia agent edited, proofread, or line-edited the submission.
- A Claudia agent performed research, summarization, or synthesis that informed the submission, even if Edgar wrote the final prose.
- A Claudia agent ran analysis, transformation, or computation whose output appears in the submission.

If the assignment's course policy forbids AI use, do not submit AI-assisted work. Disclosure does not cure a policy violation.

If the assignment's course policy is silent on AI, default to attaching the disclosure. Silence is not permission, but transparent disclosure is the safer posture.

## Four Substantive Elements

Every disclosure must cover all four of the following:

1. **Tools used.** Name the model and the orchestrator. Example: "GPT-5, accessed through the Claudia agent system."
2. **How they were used.** State the function honestly. Research, drafting, editing, proofreading, coding, analysis, translation, formatting. Be specific enough that the grader can judge the scope of assistance. Do not euphemize.
3. **Author review and verification.** Affirm that Edgar personally read the final submission, verified factual claims and citations, and agrees with the content as his own considered work.
4. **Acceptance of responsibility.** Affirm that Edgar accepts full intellectual and academic responsibility for the submission, including any errors.

## Placement

Default location is a short block at the end of the document, after the reference list or bibliography, under the heading "AI Use Disclosure."

Exceptions:

- **Cover page required.** If the assignment has a cover page or title page, place the disclosure on the cover page instead of the footer, so the grader sees it before reading.
- **Slide decks.** Place the disclosure on the final slide, titled "AI Use Disclosure," before any appendix slides.
- **Code or notebook submissions.** Place the disclosure as a comment block at the top of the primary file, or in a `DISCLOSURE.md` sibling file if multiple files are submitted.
- **Short-form submissions (discussion posts, reflections).** Place a single-line disclosure at the end, using the compact variant in the template file.

## Interaction With `output-disclosure.md`

The two disclosures serve different audiences and must not be confused.

| SOP | Audience | Purpose | Lives Where |
|---|---|---|---|
| `output-disclosure.md` | Edgar, internal | Provenance trail for agent outputs inside Claudia | Every agent deliverable |
| `ai-disclosure.md` (this one) | UCSD grader, external | Academic integrity disclosure on graded submissions | Only on work Edgar submits for a grade |

Before submission, strip any agent-level disclosure block from the file. The grader should see only the author-to-grader disclosure defined here. Carrying internal Claudia provenance into a submitted file is noise at best and confusing at worst.

## Template

The reusable block lives at `_claudia/sop/ai-disclosure-template.md`. Copy the variant that matches the actual use. If use exceeds a variant, use the next-heavier variant, never a lighter one.

## Operating Rules

- Be honest about the spectrum of use. If an agent wrote the first draft and Edgar revised it, say so. Do not describe heavy drafting as "light editing."
- Never omit the disclosure because the use was small. A grammar pass still counts.
- If multiple agents contributed, list the function of each.
- If a syllabus prescribes its own disclosure format, use the syllabus format and, if compatible, add the four substantive elements above as a supplement.
- Update this SOP if UCSD, GPS, or a course adopts a prescribed template. Flag the conflict to Claudia before submitting.
