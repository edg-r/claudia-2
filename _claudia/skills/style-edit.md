---
name: style-edit
description: "Use this skill whenever the task is prose review: line editing a draft, giving developmental feedback on structure, running a targeted style pass (cut passive voice, kill nominalizations, tighten by X%), rewriting a stuck sentence or paragraph multiple ways, or consulting on a specific word choice. Triggers include: 'proofread,' 'line edit,' 'clean this up,' 'does this work,' 'read this and tell me what's wrong,' 'cut passive voice,' 'tighten this,' 'is [word] right here,' 'rewrite this paragraph,' or any request focused on the prose rather than the substance. Calliope is the primary agent for this skill, though any agent can invoke it for lightweight prose review."
---

# Style Edit Skill

## Overview

This skill encodes five reproducible review modes for prose editing in Edgar's graduate writing. It is the operational companion to Calliope, the cross-course writing agent, but any agent can invoke it for lightweight prose review. It is grounded in Strunk and White's *The Elements of Style*, with supplements from Joseph Williams, William Zinsser, George Orwell, and Steven Pinker.

Every mode respects Edgar's hard rules: no emdashes, no "it's not X, it's Y" framing, avoid semicolons and colons where possible, prefer "the" over "that" as a sentence-opening determiner, one idea per sentence, preserve the original file as `_ORIGINAL.docx` before producing `_TRACKED.docx`, and end every output with the standard disclosure block.

## The Five Modes

Edgar signals which mode he wants. Ask once if the signal is unclear. Do not assume.

### Mode 1: Full Line Edit

**Invoke when:** Edgar says "proofread this," "line edit," "clean this up," "give this a pass," or hands over a draft with the implication that the prose is near-final and needs polish.

**What you do:** Read the entire document first. Then revise sentence by sentence. Apply the full Strunk-Williams-Zinsser-Orwell stack. Walk the failure-mode checklist (nominalizations, zombie nouns, passive voice overuse, throat-clearing, weak verbs, buried subjects, hedge piles, empty qualifiers, abstract diction, comparative asides, false parallelism, misplaced modifiers, jargon without payoff, citation dumps). Make substantive changes visible. Explain every substantive change in a margin comment.

**Output:**
1. `<filename>_ORIGINAL.docx` — the unchanged original, preserved as backup. Never overwrite an existing `_ORIGINAL.docx`.
2. `<filename>_TRACKED.docx` — Word tracked changes (`w:ins` and `w:del` XML elements) authored by `Claudia/Calliope` or `Codex/Calliope` per the orchestrator detection rule. Margin comments for every substantive change.
3. Chat summary pointing to both files and highlighting the three or four most consequential changes.

**Tools:** See `_claudia/skills/docx.md` for the full docx-js and XML reference, including the Tracked Changes and Comments sections and the `scripts/accept_changes.py` utility.

### Mode 2: Developmental Feedback

**Invoke when:** Edgar says "does this work," "read this and tell me what's wrong," "is the argument sound," or hands over an early draft where the structure is still in flux. Also invoke when line-editing would be premature because the argument itself still needs work.

**What you do:** Read the entire document. Do not edit the document. Write a section-by-section critique focused on structure, argument, BLUF clarity, theory integration, and recommendation specificity. Check whether the thesis or recommendation appears in the first two to three sentences. Check whether theory is applied rather than lectured. Check whether recommendations connect to the paper's theoretical frame or are generic filler. Flag weak paragraphs and say why they are weak. If the draft is strong in a section, say that too.

**Output:**
1. `<filename>_REVIEW.md` — a companion markdown file next to the source document. Section headings mirror the draft. Under each section, a paragraph of critique. Close with a "Top Three Priorities" section naming the three changes that would most improve the draft.
2. Chat summary pointing to the file and naming the top three priorities.

**No document edits in this mode.** The point is to fix structure before polishing prose.

### Mode 3: Targeted Style Pass

**Invoke when:** Edgar knows the specific weakness. Triggers: "cut passive voice," "kill nominalizations," "tighten by 20%," "remove all hedging," "fix the parallelism," "make the verbs stronger."

**What you do:** Scope your edits to the named rule. Do not expand scope. A passive-voice pass is a passive-voice pass; do not also fix word choice unless the passive fix requires it. Walk the document once, apply the rule, and produce the tracked version.

**Output:**
1. `<filename>_ORIGINAL.docx` — preserved.
2. `<filename>_TRACKED.docx` — tracked changes scoped to the named rule. Margin comments reference the rule ("passive to active," "nominalization to verb").
3. Chat summary with a count (e.g., "cut twenty-three passives, retained four where the agent was genuinely unknown") and the three or four most consequential changes.

### Mode 4: Sentence-Level Surgery

**Invoke when:** Edgar is stuck on a specific sentence, paragraph, or transition. He will quote the passage and ask for alternatives or for a rewrite.

**What you do:** Read the surrounding context (at least the preceding and following paragraph). Produce three to five rewrites of the passage. Rank them by tradeoffs: which is most concise, which preserves voice most faithfully, which lands the emphatic word hardest, which is most direct. Explain each tradeoff in one sentence.

**Output:**
1. If the passage is a single sentence: deliver inline in chat with a ranked list of alternatives.
2. If the passage is a paragraph or longer: write a short `<filename>_REWRITES.md` with the alternatives and tradeoffs, and deliver a chat summary pointing to it.

### Mode 5: Word-Choice Consultation

**Invoke when:** Edgar asks about a specific word or phrase. Triggers: "is 'leverage' the right word here," "what's a better word for X," "does 'galvanize' work in this context."

**What you do:** Offer two to four candidate words. For each, give denotation (what it literally means), connotation (what it suggests), and register (formal, informal, technical, journalistic). Recommend one, explain why, and name the context in which a different candidate would beat it.

**Output:** Chat response. No file unless the consultation runs long enough that Edgar will want to refer back to it, in which case deliver `<filename>_WORDNOTES.md`.

## Hard Rules (Apply to All Modes)

1. **No emdashes.** Use commas, periods, parentheses, or restructure. If you find an emdash in the source, flag and replace.
2. **No "it's not X, it's Y" framing.** State the claim directly.
3. **Avoid semicolons and colons unless the sentence genuinely demands them.** Default to periods or commas.
4. **Prefer "the" over "that" as a sentence-opening determiner.**
5. **One idea per sentence.** Break compound sentences at the verb when they carry two independent actions.
6. **Preserve Edgar's voice.** The goal is cleaner Edgar, not a different writer. Sharpen his direct, assertive, specific, active academic voice. Do not replace it. Never over-polish his personal writing into someone else's voice.
7. **Explain every substantive change in a margin comment.** Silent substantive edits are not permitted. "Cut for concision" or "active voice" is enough.
8. **Never overwrite the source file.** Always preserve the original as `_ORIGINAL.docx` before producing `_TRACKED.docx`. If an `_ORIGINAL.docx` already exists, do not touch it.
9. **Tracked-changes author string reflects orchestrator chain.** `Claudia/Calliope` when dispatched by Claudia or Claude Code. `Codex/Calliope` when dispatched by Codex. Default to `Claudia/Calliope` if ambiguous.
10. **Do not generate citations.** Flag missing or malformed citations. Do not invent them. Atlas sources, Mnemosyne indexes, course agents verify.
11. **Do not overrule course agents on substance.** Flag suspected factual or theoretical errors as margin comments for Edgar to raise with the relevant course agent.
12. **Honest feedback.** If a paragraph is weak, say so and show why. If a draft is strong, say that only when true.

## Core Edit Loop (Applies to Modes 1, 3, and Parts of 4)

For every sentence you touch:

1. Find the needless words. Cut throat-clearing, redundant pairs, empty qualifiers, filler verbs.
2. Convert passive to active where it helps. Retain passive only when the agent is unknown or the object genuinely deserves subject position.
3. Replace abstractions with specifics. Name the thing. Numbers over adjectives.
4. Fix parallelism in any series.
5. Check that the emphatic word ends the sentence.
6. Check that subject and verb are not separated by a long prepositional stack.
7. Convert nominalizations back to verbs. Characters as subjects, actions as verbs (Williams).

## Failure-Mode Checklist

Walk any draft against this list:

- Nominalizations
- Zombie nouns
- Passive voice overuse
- Throat-clearing openings
- Weak verbs (forms of "to be" and "to have" doing work stronger verbs should do)
- Buried subjects
- Hedge piles
- Empty qualifiers ("very," "really," "quite," "somewhat," "relatively")
- Abstract diction ("factors," "aspects," "elements," "issues")
- Comparative asides ("a far lower bar than...")
- False parallelism
- Misplaced modifiers
- Jargon without payoff
- Citation dumps

## Disclosure

Every output from this skill ends with the standard disclosure block per `_claudia/sop/output-disclosure.md`:

```
---
Generated for: Edgar Agunias
Date: [YYYY-MM-DD]
Model: [model name and version]
Sources: [inputs used, e.g., "source draft, Strunk and White, Williams"]
Agent: Calliope (or invoking agent)
---
```
