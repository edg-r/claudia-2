---
name: policy-memo
description: "Use this skill whenever the user asks for a policy memo, policy brief, or any short advisory document directed at a decision-maker. Triggers include: 'policy memo', 'memo', 'brief', 'write a memo to', 'advise [person/agency] on', or any request to produce a concise document recommending policy action for a specific audience. Also use when the user asks to revise, restructure, or reformat an existing memo. Do NOT use for academic essays, literature reviews, or research papers longer than 1500 words."
---

# Policy Memo Skill

## Overview

This skill produces policy memos as Word (.docx) files. It enforces a specific writing voice, structural format, and set of principles drawn from David Victor's memo-writing framework and the user's prose preferences.

Before writing any memo, read **references/template.js** for the complete docx-js template and formatting code. The template handles all Word formatting. Your job is to supply the content.

## The Six Questions (Victor & PMP Guidelines)

Every memo must answer these questions on a single read-through:

1. **Who is the decision-maker?** (the TO: line)
2. **What is the issue?**
3. **Why is this problem worth the reader's attention now?**
4. **What action are you advocating?**
5. **On what basis will your proposal produce the effects you claim?** (theory)
6. **Why is your proposal preferable to feasible alternatives?**

If a draft fails any of these, revise before generating the document.

## Structure

A memo has three sections (which may be split or combined). No conclusion section in short memos. The final paragraph ties the core ideas together.

### 1. Executive Summary (≤150 words)

The first 1–2 paragraphs. This is the most important section. It:
- Sets context and frames the need for action.
- States the core argument in 1–2 sentences.
- Is not a mystery novel. The recommendation appears here, not at the end.
- Frames the big ideas so the reader can organize how the analysis that follows supports the argument.

### 2. Context / Analysis

Fills in detail on constraints, opportunities, key actors, and the theoretical mechanism driving the argument. Theory should be woven into the analysis, not presented as a standalone block. Use theory the way a practitioner would: apply the concept to the case, name it only if useful, do not lecture the reader on the theory itself.

Victor's guidance: "The point is not to educate the CEO about Mancur Olson but to use the ideas from theory to shape better policy."

### 3. Recommendations / Policy Options

Two organizing strategies:
- **One central recommendation** with counterarguments and obstacles layered in (preferred for ≤1000-word memos; produces more compact writing).
- **Several distinct recommendations** with a case for one over others.

**Never** present three boxed options and ask the reader to pick. Real policy has many dimensions and tradeoffs. The memo helps the client think, then leads to a meeting.

Recommendations must connect to the theoretical framework. Generic proposals that could appear in any brief on the topic should be cut.

## Word Limit

Default: **1000 words** (references excluded). There is a lot you can say in 1000 words with effective organization.

## Prose Rules

These rules govern all memo text. They are non-negotiable.

1. **No em-dashes.** Use commas, periods, or restructure the sentence.
2. **No comparative asides.** Do not explain significance by contrasting ("a far lower bar than..."). State the fact. Let the reader weigh it.
3. **One idea per sentence.** Break at the verb when a sentence carries two independent actions.
4. **Prefer "the" over "that" as a sentence-opening determiner.**
5. **Cut inline examples that interrupt a claim.** If the example does not advance the argument, it is a footnote at best.
6. **Kill generic recommendations.** Keep only proposals that connect to the memo's theoretical framework.
7. **Avoid semicolons and colons.** Default to periods or commas. Use a semicolon or colon only when the sentence genuinely demands it and no restructure works better.
8. **Active voice.** Passive constructions are acceptable only when the actor is genuinely unknown or irrelevant.
9. **No hedging.** Do not write "it could be argued that" or "one might consider." State the claim.
10. **Integrate citations naturally.** APA 7 in-text citations woven into prose. Full references section at the end (excluded from word count).
11. **Direct and assertive.** Write as an advisor who has done the analysis, not a student summarizing options.

## What NOT to Do (Victor)

- Do not write an essay that indiscriminately summarizes information on the topic.
- Do not dedicate large chunks to theory without connecting it to the case.
- Do not include information the reader already knows unless it frames your argument.
- Consider what would be valuable to the hypothetical reader and dedicate the most attention to those items.

## Formatting (Word Document)

All memos are output as .docx files using docx-js. Read `references/template.js` for the full template before generating. Key formatting:

- **Font:** Times New Roman, 12pt body, justified alignment.
- **Page:** US Letter (12240 × 15840 DXA), 1-inch margins.
- **Header block:** Borderless table with TO, FROM, DATE, RE fields. RE line is bold.
- **Divider:** Single black border below the header block.
- **Section headings:** Bold, slightly larger (13pt for H1, 12pt for H2).
- **Recommendations:** Indented paragraphs. Number + title in bold, body text in regular weight.
- **References:** APA 7, hanging indent (720 DXA), slightly smaller font (11pt). Page break before references.
- **No bullet points or numbered lists in body text.** Recommendations use a numbered format (1a, 1b, etc.) but the body is prose.

## Workflow

1. Read `references/template.js` to load the docx-js template.
2. Draft memo content following the structure, prose rules, and six questions above.
3. Populate the template with content.
4. Run `node` to generate the .docx.
5. Validate with `python scripts/office/validate.py`.
6. Copy to `/mnt/user-data/outputs/` and present via `present_files`.

## Sourcing

Memos include a works cited list (APA 7). This list does not count against the word limit. If data or graphics are included, cite the source. If data cannot be confirmed, state why or do not use it.
