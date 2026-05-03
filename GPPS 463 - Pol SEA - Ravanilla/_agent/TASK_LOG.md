# Poseidon — GPPS 463 Task Log

Record of major completed tasks. Read to avoid duplicate work.

<!-- No entries yet. Append new tasks below this line. -->

## 2026-04-22 — Jansen 2001 reading summary (W4 Asian Miracle)
- Produced BLUF-style memo summary of Jansen, "Thailand: The Making of a Miracle?" for today's (Wed Apr 22) W4 lecture
- Saved to `Study Guides/jansen2001_thailand_miracle_summary.md`
- Note: syllabus has no per-lecture reading schedule; readings inferred from week-folder contents. Jansen was the only un-summarized W4 PDF; Edgar's LD8 discussion post (Apr 21) also keyed on Jansen.

## 2026-04-13 — Discussion Post LD6 (WWII)
- Drafted discussion post question and response for Lecture Day 6 (Apr. 15)
- Required reading: Stubbs (1999) "War and Economic Development"
- Saved to: W3 - Colonial Institutions and Development/Discussion Post LD6 - WWII.md
- Key angle: Philippine exception as the limit case of Stubbs's geostrategic argument; tension with colonial institutions thread from W3

## 2026-04-14 — Simplified Discussion Post LD6 question (Opus override after Sonnet terminations)
**Requested by:** Claudia (Edgar asked for a simpler, shorter version of the LD6 question plus a one-sentence "why it matters" note)
**Context:** Three prior Poseidon dispatches on 2026-04-14 terminated with API errors on Sonnet (initial discussion post retry, follow-up retry, and one mid-run termination after 8 tool calls). Switching to `model: "opus"` override on the Agent dispatch resolved it; this run completed in 24 seconds with 2 tool uses.
**What was done:** Read the existing LD6 draft, replaced the long question block and the three-sentence "Why this matters" paragraph with a plain-language two-sentence question ("Stubbs says war and Cold War pressure built the strong states that drove Asia's export boom. If that is true, why did the Philippines, which went through the same wars, end up weak and poor?") and a one-sentence importance note ("If war alone cannot explain the Philippine failure, then colonial institutions, not geostrategy, may be doing the real work in shaping who develops and who does not."). All other content in the file (notes on argument, Philippine exception, W3 tension) preserved intact.
**Output:** `W3 - Colonial Institutions and Development/Discussion Post LD6 - WWII.md` updated in place. Discussion post submission-ready for 5 PM deadline.
**Notes:** Future Poseidon dispatches should prefer Opus when run in the background until the Sonnet termination pattern is understood. Also: the simplified-question framing is what Edgar actually wanted from the start; the longer version overloaded the prompt. Default to shorter, plainer question phrasings on discussion posts going forward.

## 2026-04-15 — Vietnam, Company Rule, and French Colonialism Clarification
**Requested by:** Edgar
**What was done:** Answered whether Vietnam was colonized by a VOC-style trading company and how much the company/state distinction matters for GPPS 463's colonial institutions frame.
**Output:** Returned to Claudia/Edgar in chat.
**Notes:** Core answer: Vietnam was colonized primarily through French state conquest and French Indochina's colonial bureaucracy, not by a sovereign chartered trading company like the VOC. The distinction matters institutionally, but it is not an absolute divide because company-states depended on state charters and coercion while state empires relied heavily on private concessionaires, merchants, missionaries, and planters.

## 2026-04-16 — Week 4 Theory Reference PDF (Asian Miracle / Jansen 2001)
**Requested by:** Claudia (Edgar wants W4 prep in hand before next week's class)
**Context:** W4 = Lecture Day 8 (Apr 22): "Why did only some countries experience the Asian Miracle?" Required reading: Jansen, Karel (2001), "Thailand: The Making of a Miracle?" *Development and Change* 32: 343-370. LD7 (Apr 20) is the in-class Midterm Exam 1 with no reading. The Canvas schedule PDF (GPPS 463 - Politics of Southeast Asia - Ravanilla [SP26].pdf) is the per-week reading map — the main syllabus PDF does not list readings by week, only course-wide info. Optional W4 readings (Kim 2010, Doner 1991) are listed on Canvas but are NOT in the workspace and were explicitly excluded from this pass with a scope note on the disclosure page.
**Skills wired in:** `_claudia/skills/lecture-to-reference-pdf.md` (three-layer rule, TOC, decoder tables, country-awareness callouts, quotation blocks); `_claudia/skills/pdf.md` (ReportLab + pypdf mechanics).
**What was done:** Read the full 28-page Jansen article in two halves. Built an 18-page reference PDF with: clickable TOC (12/12 targets mapped via TrackingDoc + pypdf Link annotations), cover with BLUF card and reading anchor, three-layer analysis (growth accounting → political economy → distribution), concept decoder (TFP, NICs, growth accounting, developmental state, social capital, demographic transition, land frontier, NESDB/BoI, etc.) split cleanly across two pages with repeating headers, author-argument decoder (Young/Krugman/Collins-Bosworth/WB/Campos-Root/Phongpaichit-Baker/Unger/Kunio/Myrdal/Bello), three cross-country comparison tables (TFP contribution, state type, colonial experience), country-awareness callouts per country (TH, PH, SG, KR/TW, MY/ID, CN), nine direct quotations with page cites, cross-week threads to W1/W2/W3, cross-course connections to Plutus/Athena/Tyche, 7 midterm index-card candidate lines, and a disclosure page.
**Output:** `GPPS 463 - Pol SEA - Ravanilla/Study Guides/GPPS_463_Week_4_Reference.pdf` (18 pages, 51 KB).
**Key argument frames encoded in the PDF:**
- Thailand is the uncolonized control case — use it to isolate what colonial institutions did and did not do in W3's Dell-Olken/Acemoglu/Stubbs framework.
- Jansen's mechanism: dynamic Chinese-Thai entrepreneurial class + cautious pro-business state (NOT developmental state — Thai govt expenditure averaged 16.4% GDP, 1970-97).
- Four East Asian commonalities: entrepreneurs, macro stability, openness, human capital.
- Four Thai uniques: no colony, land frontier, non-interventionist state, rapid demographic transition.
- Thailand is the only East Asian miracle country with *rising* inequality over 1965/70-1981/90 — no land reform, because no colonial disruption forced one.
- Key comparison stat: Thai TFP ~+1.8%/yr vs. Philippine TFP -0.4%/yr (Collins & Bosworth 1996, via Jansen p. 346). The PH contrast carries the institutions thesis.
**Notes:** Keep this PDF open during lecture on Apr 22 and update with lecture-slide emphasis afterwards — Jansen's framing may diverge from what Ravanilla actually pushes. Also: the Philippines TFP number (-0.4%) is the exam-gold stat to link W3 → W4 — pair it with the Stubbs-Philippine-exception move already encoded in the LD6 discussion post.

## 2026-04-17 — Midterm 1 Study Guide (W1–W3, all six required readings)
**Requested by:** Claudia (Edgar prepping for Apr 20 in-class Midterm Exam 1)
**Context:** Midterm 1 is LD7 Apr 20, covers LD1–LD6 (W1 Ancient Kingdoms, W2 Sinicized vs. Indianised + Guns Germs & Steel, W3 Colonial Institutions + WWII). The syllabus says only "first portion of the course"; the Canvas reading schedule (`GPPS 463 - Politics of Southeast Asia - Ravanilla [SP26].pdf`) resolves the ambiguity. Six required readings: Hayton Ch. 1, Dell-Lane-Querubin 2018 (the `dai viet.pdf` file), Diamond 1997 Prologue, Acemoglu-Robinson 2012 Ch. 9, Dell-Olken 2020, Stubbs 1999. A prior run had produced a 360-line draft that was already comprehensive and accurate; this run verified scope, verified the Dai Viet file identity, fixed one emdash (line 279 Philippines negative case), added `---` delimiters to the disclosure block per SOP, and produced the PDF deliverable.
**Skills wired in:** None explicit; SAQ-pattern extracted from `Midterm 1/Sample Short Essay Responses.pdf` (two model answers + graded commentary) and made the structural anchor of the guide.
**Output:**
- `Study Guides/Midterm_1_Study_Guide.md` (360 lines, ~36 pp worth, Edgar-style prose)
- `Study Guides/Midterm_1_Study_Guide.pdf` (22 pages, 336 KB, via Chrome headless → styled HTML → PDF since pandoc/xelatex/weasyprint were unavailable)
**PDF pipeline note:** pandoc, xelatex, wkhtmltopdf, weasyprint all absent or unusable on this machine. Fallback: python-markdown (pip installed) → styled HTML → Chrome headless `--print-to-pdf`. Worked cleanly. If a future run needs identical output, Chrome headless is the reliable macOS-only route.
**SAQ pattern captured:** Ravanilla wants causal, comparative, path-dependent institutional analysis with named course concepts (mandala, extractive institutions, reversal of development, EOI, crowd-in). Chronological narrative loses points. Europe-only or SEA-only answers lose. Technology and geography must be framed as *amplifiers* of institutional capacity, not standalone explanations. This is exactly the A/A+ model answer's move on "Why did Europe win colonisation."
**Key synthesis moves encoded:** (1) the two Dutch colonialisms tension (Acemoglu-Robinson Moluccas reversal vs. Dell-Olken Java positive persistence, reconciled via rent-vs.-output extraction logic); (2) the strong-state paradox (Dell-Lane-Querubin's delegating strong state vs. Stubbs's centralising strong state, reconciled via timescale and function); (3) Philippine negative case as the limit case binding W3 and the Stubbs thesis; (4) path dependence as the silent common framework across all six readings.

## 2026-04-19 — Midterm 1 Lecture-vs-Study-Guide Gap Memo
**Requested by:** Claudia (Edgar) — six Ravanilla lecture PDFs (file IDs 941–946) just indexed; needed to know what the 2026-04-17 study guide missed.
**Method:** Read all six lecture PDFs (Day 1 through Day 6) in chunked page reads, then cross-checked against `Study Guides/Midterm_1_Study_Guide.md`.
**Output:** `Study Guides/Midterm_1_Lecture_Gaps.md` — per-lecture gap list + "highest-priority adds" section + verdict on whether the 37pp guide needs a v2.
**Top findings:** The reading-content portion of the study guide is solid, but the lectures contain large blocks of *theoretical scaffolding* and *non-reading material* the guide misses entirely:
1. The five-constraints-to-five-institutions table (LD2) — Ravanilla's master analytical move, used to explain mandala formation AND decline AND European feudalism.
2. The European Diversion arc (LD4 slides 13–22) — Fall of Rome → feudalism → free towns → nation-states → expeditions. THE template for "Why Europe won," and the sample A/A+ essay implicitly uses it.
3. The Inclusive/Extractive 2x2 with non-SEA worked cases (USA, South Africa, China, North Korea) — LD4.
4. The Dutch optimisation menu in the Moluccas (Ambon/Banda/Tidore-Ternate-Bacan as three different extractive-institution choices) — LD5.
5. The Philippines deep-dive (LD6 slides 33–55) — 23 slides of encomienda → principalia → American compromise → today's oligarchy chain. Almost certainly testable as a long SAQ, more than the study guide's brief "Stubbs negative case" treatment.
6. Named concepts likely as MC definition stems: Douglass North on institutions (formal/informal, "rules of the game"); Benedict Anderson's "imagined communities" (imagined/limited/sovereign/comradeship); Treaty of Tordesillas 1494; reversal of fortune (AJR scatter); "shared experience in diversity" as the regional definition.
**Verdict:** No full v2 needed. Add a one-page "Lecture-Only Frameworks" supplement to the index card, anchored on items 1–5 above.

## 2026-04-20 — Discussion Post LD8 (Asian Miracle / Jansen 2001)
**Requested by:** Claudia (Edgar) — next discussion post, due Apr 21 by 5 PM (post before LD8 on Apr 22).
**Context:** LD7 today is the in-class Midterm 1 (no reading, no post). LD8 asks "Why did only some countries experience the Asian Miracle?" Required reading is Jansen (2001). Built on the W4 Theory Reference PDF from 2026-04-16 which had already encoded Jansen's BLUF, four commonalities, four Thai uniques, and the Philippine TFP contrast.
**Format followed:** Same template as LD6 — short 2-sentence question, one-sentence "why it matters," extended notes on the argument, output-disclosure block, AI-disclosure template pointer. No emdashes; no "is it X or Y" framing.
**Output:** `W4 - Asian Miracle/Discussion Post LD8 - Asian Miracle.md`
**Key angle:** If the miracle can run on Thailand's non-interventionist state AND Korea's developmental state, then state architecture is not the binding constraint — the common variable is an entrepreneurial class the state does not capture, which pushes the explanation back toward W3's institutions lens. Directly continues the LD6 Philippine-exception thread.
**Notes:** Didn't need to re-read Jansen; the reference PDF built 4 days ago carried all the page cites and stat anchors needed. When a week's reference PDF exists, use it as the discussion-post substrate.

## 2026-04-22 — Jansen (2001) "Thailand: The Making of a Miracle?" Summary (W4)
**Requested by:** Claudia (Edgar) for W4 Asian Miracle prep.
**Output:** `GPPS 463 - Pol SEA - Ravanilla/Study Guides/jansen2001_thailand_miracle_summary.md` (BLUF format).
**Takeaway:** Thailand's 6.6%/yr growth came from factor accumulation under a pragmatic non-interventionist state plus a Chinese-origin entrepreneurial class — distinct from the Korea/Taiwan/Singapore developmental-state model.
**Process note:** Last BLUF-default summary. Going forward use `_claudia/skills/theory-reference-pdf.md` as the new default for reading summaries (effective 2026-04-22).

## 2026-04-27 — Huff (1995) Singapore Model 1-Page Summary
**Requested by:** Edgar via Claudia/Poseidon invocation.
**What was done:** Identified Monday Apr 27, 2026 as GPPS 463 Lecture Day 9, "How did Singapore do it?", using the Canvas reading schedule PDF; required reading is Huff (1995), "What is the Singapore model of economic development?" Created a concise Markdown study guide with APA 7 reference and Claudia disclosure block.
**Output:** `GPPS 463 - Pol SEA - Ravanilla/Study Guides/huff1995_singapore_model_summary.md`
**Notes:** Core frame: Singapore is a disciplined state-capitalist, market-facing planning case, not a laissez-faire Asian miracle story. Main mechanisms are wage/labor control, MNE-led manufacturing, forced saving, infrastructure-led crowding in, and financial/business services.

## 2026-04-28 -- Discussion Post LD10 (Asian Financial Crisis / Hicken 2008)
**Requested by:** Edgar via Claudia/Poseidon invocation.
**What was done:** Drafted Edgar-usable Canvas text for Lecture Day 10, "Why was the Asian Financial Crisis unequally felt in the region?", using Hicken (2008) on Thailand and the Philippines. Included compact grader AI disclosure because the syllabus extraction found no explicit AI policy but Claudia SOP requires disclosure for graded AI-assisted work.
**Output:** `GPPS 463 - Pol SEA - Ravanilla/W5 - Singapore & Asian Financial Crisis/Discussion Post LD10 - Asian Financial Crisis.md`
**Notes:** Key angle is the crisis-severity paradox: Thailand was hit harder but the shock created reform pressure, while the Philippines was hit less hard and therefore postponed costly reforms. Claudia clarified the Orange Memo on Myanmar belongs to Athena/GPCO 410, so Poseidon only added quick GPPS 463 regional-context pointers.

## 2026-04-29 -- LD10 Discussion Question Revision
**Requested by:** Claudia (delegated Poseidon worker for Edgar's "draft the discussion question for today")
**What was done:** Verified the Canvas schedule places LD10 on Apr. 29, then tightened the existing Hicken discussion question around the crisis-severity paradox and removed unrelated Myanmar memo notes from the deliverable.
**Output:** `GPPS 463 - Pol SEA - Ravanilla/W5 - Singapore & Asian Financial Crisis/Discussion Post LD10 - Asian Financial Crisis.md`
**Notes:** Submission-ready Canvas text now asks how the 2008 global financial crisis should change the reading of Hicken's warning that surviving 1997 too easily may have delayed harder reforms.

## 2026-04-29 -- Discussion Post LD11 (Vietnam Under Communism / Malesky, Abrami & Zheng 2011)
**Requested by:** Edgar via Claudia/Poseidon follow-up after LD10 was already complete.
**What was done:** Confirmed the next GPPS 463 discussion post is LD11, "How is Vietnam doing under communism?", for May 4 with Malesky, Abrami, and Zheng (2011) as the required reading. Drafted a concise Canvas-ready discussion question and supporting notes.
**Output:** `GPPS 463 - Pol SEA - Ravanilla/W6 - Vietnam Under Communism/Discussion Post LD11 - Vietnam Under Communism.md`
**Notes:** Key angle is Vietnam as a single-party regime with broader elite accountability than China, producing more redistribution and lower inequality without democratization.

## 2026-04-29 -- Midterm Theory Reference PDF v1.0.0
**Requested by:** Claudia (delegated Poseidon worker for GPPS 463 midterm theory/reference update)
**What was done:** Built an exam-ready theory reference PDF using `_claudia/skills/theory-reference-pdf.md` and `_claudia/skills/pdf.md`, starting from existing generated GPPS 463 study guides rather than re-summarizing readings from scratch. The PDF has one cover/TOC page plus 11 framework pages with sidebar bookmarks: constructed region, mandala, Sinic village governance, Diamond geography, European Diversion, AJR reversal, Dell-Olken positive persistence, Stubbs war/EOI, Jansen Thailand, Huff Singapore, and Hicken Asian Financial Crisis.
**Output:** `GPPS 463 - Pol SEA - Ravanilla/Study Guides/GPPS_463_Midterm_Theory_Reference_v1.0.0.pdf`; notes at `GPPS 463 - Pol SEA - Ravanilla/Study Guides/GPPS_463_Midterm_Theory_Reference_v1.0.0_notes.md`; builder at `GPPS 463 - Pol SEA - Ravanilla/Study Guides/build_midterm_theory_reference.py`
**Notes:** Machine-readable sources only. No OCR was run because the relevant existing reference PDFs extracted with `pypdf` and the task asked not to redo already summarized material from scratch. Inbox files were checked and skipped as unrelated to GPPS 463.

## 2026-04-29 -- Midterm Theory Reference PDF v1.1.0 Revision
**Requested by:** Claudia (delegated Poseidon worker for Edgar feedback)
**What was done:** Revised the existing midterm theory-reference generator instead of rebuilding from scratch. Expanded each framework page's theory explanation, key concepts, assumptions, strengths, and weaknesses; added full article/paper/book-chapter or lecture-framework title plus author/instructor in each header; updated model provenance to `GPT-5.5 (medium reasoning)`.
**Output:** `GPPS 463 - Pol SEA - Ravanilla/Study Guides/GPPS_463_Midterm_Theory_Reference_v1.1.0.pdf`; notes at `GPPS 463 - Pol SEA - Ravanilla/Study Guides/GPPS_463_Midterm_Theory_Reference_v1.1.0_notes.md`; revised builder at `GPPS 463 - Pol SEA - Ravanilla/Study Guides/build_midterm_theory_reference.py`
**Notes:** Verification passed with 12 pages total, 11 sidebar bookmarks, bookmark destinations on pages 2-12, 34,420 extracted text characters, and extracted text containing the new model provenance plus representative full-title headers for Hayton, Dell/Lane/Querubin, and Hicken. No files staged or committed.

## 2026-04-29 -- Midterm Theory Reference PDF v1.2.0 Revision
**Requested by:** Claudia (delegated Poseidon worker for Edgar feedback)
**What was done:** Revised the v1.1.0 midterm theory-reference generator to produce v1.2.0 with 12pt body text, fuller author/time-period context, deeper mechanism framing, compact course-vocabulary/assumption tables, explicit exam-application sections, and case/comparison cues for each GPPS 463 framework. History of Warfare remains skipped.
**Output:** `GPPS 463 - Pol SEA - Ravanilla/Study Guides/GPPS_463_Midterm_Theory_Reference_v1.2.0.pdf`; notes at `GPPS 463 - Pol SEA - Ravanilla/Study Guides/GPPS_463_Midterm_Theory_Reference_v1.2.0_notes.md`; revised builder at `GPPS 463 - Pol SEA - Ravanilla/Study Guides/build_midterm_theory_reference.py`
**Notes:** Verification passed with 23 pages total, 11 sidebar bookmarks, bookmark destinations on pages 2/4/6/8/10/12/14/16/18/20/22, 11 clickable TOC links, no blank pages, 45,979 extracted text characters, extracted text containing `GPT-5.5 (medium reasoning)`, `AUTHOR / TIME-PERIOD CONTEXT`, `EXAM APPLICATION`, and `CASE / COMPARISON CUES`, and builder body style set to `fontSize=12`. No files staged or committed.

## 2026-04-30 -- Midterm Theory Reference PDF v1.3.0 Visual-Slot Revision
**Requested by:** Edgar via Claudia/Poseidon invocation.
**What was done:** Preserved v1.2.0 unchanged and revised the current midterm theory-reference builder to output v1.3.0 with imagegen-style conceptual visual slots/graph logic and short ELI5 conclusions for all 11 GPPS 463 theory/topic pages. Actual image assets were not generated; exact prompts and target asset paths were written into the PDF and notes file.
**Output:** `GPPS 463 - Pol SEA - Ravanilla/Study Guides/GPPS_463_Midterm_Theory_Reference_v1.3.0.pdf`; notes at `GPPS 463 - Pol SEA - Ravanilla/Study Guides/GPPS_463_Midterm_Theory_Reference_v1.3.0_notes.md`; revised builder at `GPPS 463 - Pol SEA - Ravanilla/Study Guides/build_midterm_theory_reference.py`
**Notes:** Verification passed with 23 pages total, 11 sidebar bookmarks, bookmark destinations on pages 2/4/6/8/10/12/14/16/18/20/22, 11 clickable TOC links, no blank pages, 55,832 extracted text characters, extracted text containing `CONCEPTUAL VISUAL SLOT`, `ELI5 CONCLUSION`, `Study Guides/assets/midterm_theory_reference_v1.3.0`, and `GPT-5 via Codex (reasoning effort not exposed)`. Pre-existing dirty W5/W6 and ASSIGNMENTS files were deliberately left untouched.

## 2026-04-30 -- Midterm Theory Reference PDF v1.3.1 Asset Integration
**Requested by:** Edgar via Claudia/Poseidon invocation.
**What was done:** Preserved v1.2.0 and v1.3.0 unchanged, then revised the midterm theory-reference builder to output v1.3.1 with the 11 generated PNG assets embedded as actual images instead of prompt/placeholder visual-slot tables.
**Output:** `GPPS 463 - Pol SEA - Ravanilla/Study Guides/GPPS_463_Midterm_Theory_Reference_v1.3.1.pdf`; notes at `GPPS 463 - Pol SEA - Ravanilla/Study Guides/GPPS_463_Midterm_Theory_Reference_v1.3.1_notes.md`; revised builder at `GPPS 463 - Pol SEA - Ravanilla/Study Guides/build_midterm_theory_reference.py`
**Notes:** Verification passed with 23 pages total, 11 sidebar bookmarks, 11 embedded image XObjects, image pages 3/5/7/9/11/13/15/17/19/21/23, all 23 pages rendered nonblank, and contact-sheet visual inspection showing no obvious overflow. Unrelated dirty W5/W6 and ASSIGNMENTS files were left untouched.
### 2026-05-02 - Artifact Archive Protocol Notification
**Requested by:** Claudia
**What was done:** Recorded the new course-local archive convention and archived superseded GPPS 463 midterm theory reference iterations.
**Output:** `GPPS 463 - Pol SEA - Ravanilla/.archive/midterm_theory_reference/`
**Notes:** Current visible candidate is v1.3.1; older generated versions are indexed in `GPPS 463 - Pol SEA - Ravanilla/.archive/ARCHIVE_INDEX.md`.
