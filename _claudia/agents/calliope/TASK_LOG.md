# Calliope — Task Log

Record of completed prose reviews. Keep entries concise but written as prose, not bullet points.

## Entry Format

```
### [DATE] — [Task Title]
**Requested by:** Claudia | Edgar | Codex
**Mode:** full line edit | developmental feedback | targeted style pass | sentence surgery | word-choice consultation
**What was done:** [1-2 sentence summary]
**Output:** [file paths or "returned to chat"]
**Notes:** [anything worth remembering for next time]
```

---

### 2026-04-15 — GPCO 410 Memo 1 "Oil and Water" full line edit
**Requested by:** Claudia
**Mode:** full line edit
**What was done:** First real Calliope pass. Ran a full line edit against the footnoted version of Memo 1 after Athena had cleared substance. Delivered paragraph-level tracked rewrites of all seven body paragraphs, moving the BLUF to sentence one of the thesis, fixing a run-on in the Bush paragraph, cutting the banned "not because one didn't exist, but because they could not trust the other" construction from the conclusion, and tightening roughly 210 words out of the body. Normalized capitalization of "war," fixed recurring "Husseins" possessive error, and repaired sentence fragments and a pronoun mismatch. Preserved both footnote references at appropriate positions in the rewritten text. Flagged the title's restrictive "which" as a margin comment rather than rewriting it.
**Output:** `/Users/edgar/Documents/01 Projects/Claudia/GPCO 410 - Intl Pol:Sec - Praether/Assignments/Blue Memo/Memo 1 - Oil and Water_CALLIOPE_TRACKED.docx` and `/Users/edgar/Documents/01 Projects/Claudia/GPCO 410 - Intl Pol:Sec - Praether/Assignments/Blue Memo/Memo 1 - Oil and Water_ORIGINAL.docx`.
**Notes:** The source had no emdashes but did contain one banned "not X, but Y" construction in the conclusion. The run-level XML in the source was heavily fragmented (dozens of small w:r blocks per paragraph with varied rsid wrappers), so the cleanest tracked-changes approach was paragraph-level wholesale rewrite: one w:del wrapping all original runs plus preserved footnoteReference elements, one w:ins with the rewritten text plus footnote refs repositioned. That gave Edgar a clean per-paragraph accept/reject surface instead of hundreds of noisy diffs. Author string `Claudia/Calliope` used throughout. No pandoc available in this environment; extracted text and manipulated XML directly with stdlib.

### 2026-04-16 — GPCO 403 AI-policy clarification email to TA Chloe Margulis
**Requested by:** Claudia
**Mode:** short-form drafting (correspondence)
**What was done:** Drafted a ≤150-word professional email from Edgar to Chloe Margulis (`cmargulis@ucsd.edu`), GPCO 403 TA, asking for clarification on AI-tool use for course assignments. Context: syllabus is silent on GenAI, Edgar wanted clarity before submitting Data Brief 1 on Fri Apr 17. Returned a three-question draft (AI permission scope, disclosure format, per-assignment variation) opening "Dear Chloe," plus closing "Best regards, Edgar Agunias." Honored the no-emdash and no-"not X but Y" rules. Returned to Claudia in chat, no file.
**Output:** returned to chat; Claudia subsequently handed the edited draft to the Gmail MCP and Edgar sent it.
**Notes:** Two post-delivery corrections from Edgar reshaped the draft. First, salutation must use last name plus title ("Dear Ms. Margulis"), never first name, on any correspondence — durable default, not per-recipient. Second, the third question (whether policy varies across Concept Checks, Data Briefs, midterm, final) was pruned because the answer is self-evident from the assignment types. Both corrections also captured as cross-agent feedback memories in Claudia's memory folder (`feedback_correspondence_formality.md`, `feedback_drafting_obvious_questions.md`) and should be read into any future correspondence-drafting brief. Edgar's close ("good edits") confirmed the corrected draft shipped clean.
