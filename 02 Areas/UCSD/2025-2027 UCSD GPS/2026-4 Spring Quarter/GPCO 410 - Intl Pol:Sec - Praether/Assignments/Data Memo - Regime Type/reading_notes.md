# Reading Notes — Data Memo (Regime Type / Polity IV)

Structured per `_claudia/skills/memo-summarizer.md` (BLUF first, Georgetown SFS style). Notes serve the **data memo's measurement-critique argument** — not the Myanmar analytic argument. These readings anchor the "deconstruction" of Polity IV's coding philosophy.

**Separation discipline:** Cederman, Hug & Krebs appears in the Orange Memo's `reading_notes.md` (its role there: democratization-violence empirical finding). It is NOT duplicated here. Its role for the **data memo** is different — it is the canonical *user* of Polity IV whose result depends on Polity's coding choices. When cited in the data memo, its role is "this is what gets broken if Polity coded differently." For full notes on the paper itself, see `Assignments/Orange Memo - Myanmar/reading_notes.md`.

---

## Reading 1 — Meng & Little (2024) — PRIMARY MEASUREMENT CRITIQUE

**Title:** "Measuring Democratic Backsliding" (2024) — Andrew T. Little & Anne Meng
**Source/Link:** *PS: Political Science & Politics*, April 2024, pp. 149–? (journal article in Comment & Controversy special issue on Democratic Backsliding); DOI 10.1017/S104909652300063X
**Local file:** `W5 - Negotiated Settlements & Democratization/Meng and Little measuring_democratic_backsliding.pdf` (OCR-clean, 68,137 chars)

### BLUF
The global "democratic backsliding" narrative rests almost entirely on expert-coded indicators (V-Dem, Freedom House) that are vulnerable to coder bias; objective indicators (incumbent electoral performance, term-limit evasions, constitutional executive constraints) show little aggregate decline over the past decade. The authors argue that claims of widespread backsliding are not yet justified by the evidence (p. 149 abstract; pp. 149–150 framing).

### Context & Scope
- Response to the prevailing scholarly and media narrative that democracy is globally declining (pp. 149–150).
- Surveys objective measures of democracy alongside V-Dem and Freedom House expert-coded scores; finds divergence (pp. 149–151).
- Explicitly distances from Polity IV/V in one critical respect: Polity's data "stop in 2018 and we therefore focus less on this source moving forward" (p. 150). But their critique of expert-coder bias cuts at Polity's method just as much as V-Dem's.

### Key Evidence / Claims
- **Objective-vs-subjective indicator divergence** (pp. 149–151). Incumbent-party electoral performance, leader turnover rates, and executive-constraint measures show no aggregate global decline over the past decade. V-Dem and Freedom House show decline. Polity shows no decline. This pattern implicates the expert-coded measures as the source of the "backsliding" narrative.
- **Litmus test for objectivity** (p. 150): "whether multiple qualified experts with access to the needed information would reach the same conclusion" (citing Cheibub, Gandhi & Vreeland 2010). Vote share of an election winner passes; "free and fair" rating fails.
- **Two mechanisms for divergence** (p. 149): (a) coder bias — expert-coder standards have shifted over time, picking up on subtle authoritarian moves more aggressively; (b) strategic substitution — leaders are deploying subtler forms of backsliding that evade objective detection.
- **Media feedback loop** (p. 149): the authors document an increase in media coverage of backsliding even as objective indicators hold steady. They argue media framing feeds coder expectations, which feeds back into scores.
- **Caveats** (p. 149): backsliding is happening in specific countries (Hungary, Venezuela named). Aggregate trend is not evidence about any specific case.
- **Polity-specific call-out** (p. 150): Polity's coverage ends in 2018, which limits its usefulness for the post-2018 backsliding debate. Worth noting that this is an *operational* limitation rather than a *conceptual* critique.

### Implications for Policy/Practice
- Funding and programming around "defending democracy" calibrate to a measurement signal that may be driven by coder bias more than actual regime change. The case for intervention should rest on objective indicators, not expert scores alone.
- For researchers: robustness checks against objective measures should accompany any study that relies on V-Dem, Freedom House, or Polity. Divergence across indicators matters theoretically, not just methodologically.

### Limits / Counterpoints
- The authors acknowledge that **subtle backsliding is hard to measure by definition**. Their argument is the burden is on proponents of the backsliding-narrative to demonstrate the objective effect, but absence of evidence is not evidence of absence.
- Their "quasi-minimalist" conception of democracy (pp. 149, 150) sidelines substantive-democracy concerns — rights, liberties, rule of law — that expert coders weight. A reader who values substantive democracy may argue the objective measures miss what matters.

### Application to the data memo on Myanmar Polity
- Meng & Little's critique runs the **opposite direction** to the data memo's primary argument. The data memo wants to argue Polity *over-scored* Myanmar 2016–2020 as democratic. Meng & Little argue expert coders in general *under-score* democracy (or equivalently, over-score backsliding). Engaging both directions is the sophisticated move.
- Synthesis available to the memo: Polity is a **mixed** source — its rules lean objective (coded from institutional features and observable behavior, not from expert "free and fair" judgments), but its weighting of observed electoral behavior over structural constraints still misreads reserved-domain autocracies like Myanmar pre-2021. Meng & Little's objectivity test sharpens this critique: Polity passes the objectivity test but still mis-weights the substantive content of the democracy it measures.
- Citation role in the memo: one footnote in the methodology / interpretation section to establish that measurement critiques of democracy indicators are a live research program, not an idiosyncratic complaint.

---

## Reading 2 — Cederman, Hug & Krebs (2010) — CROSS-REFERENCED FROM ORANGE

**Title:** "Democratization and Civil War: Empirical Evidence" (2010) — Lars-Erik Cederman, Simon Hug, Lutz F. Krebs
**Source/Link:** *Journal of Peace Research* 47(4): 377–394
**Full reading notes:** `Assignments/Orange Memo - Myanmar/reading_notes.md` §1.

**Role in the data memo (distinguished from its role in the Orange memo):**
- Orange memo role: primary theoretical anchor for Myanmar civil war risk.
- **Data memo role: exemplar user of Polity IV whose findings depend on Polity's coding choices.** Cederman et al. build their period-finding algorithm directly on top of Polity IV's score values and `polity2` interpolation rules. If Polity's coding rules changed (specifically, if reserved-domain autocracy were weighted more heavily in `xconst`), the "democratization period" Cederman et al. identify for Myanmar 2010–2015 might shrink or disappear. The democratization-civil-war finding is therefore contingent on Polity's specific coding philosophy.

**Specific data-memo-relevant points:**
- Cederman et al. use Polity IV **with** the PARREG and PARCOMP components removed, and separately **without** (see fn 11–12, p. 382). They flag that the period count changes materially based on this choice. This is the kind of coding-dependency the data memo should highlight.
- They use `polity2` (the interpolated version that replaces −66/−77/−88 special codes). Their results depend on the interpolation rules.
- They explicitly discuss the Yugoslavian case where Polity fails to register the 1990 multiparty opening at the federal level — this is a concrete example of Polity's observed-behavior bias missing structural change (p. 384).

**Citation role in the data memo:** one or two footnotes demonstrating that quantitative IR findings depend on Polity's coding rules, Myanmar's 2010–2015 period coding is itself a live example.

---

## Reading 3 — Polity V Codebook (Marshall & Gurr) — PRIMARY SOURCE

**Title:** "Polity5 Project, Political Regime Characteristics and Transitions, 1800-2018: Dataset Users' Manual"
**Authors:** Monty G. Marshall, Ted Robert Gurr
**Year:** 2020 release
**Source/Link:** Center for Systemic Peace; download at https://www.systemicpeace.org/inscr/p5manualv2018.pdf
**Local file:** Edgar to download to `Assignments/Data Memo - Regime Type/` on data acquisition.

### BLUF
The codebook is the primary source for the memo. Three sections matter most: §3 (conceptual framework — why Polity measures what it measures), §4 (component coding rules — how `xconst`, `parcomp`, etc. are scored), and the country-case narratives (how Myanmar specifically has been coded over time). Edgar should read §3 and §4 before drafting; cite the codebook by section number in footnotes.

### Key sections (structure predicted from prior Polity IV codebook — Edgar to verify on download)
- §1 Introduction
- §2 Concept and Dataset Overview
- §3 Conceptual Framework — democracy and autocracy as opposite ends of the same authority dimension; institutional focus
- §4 Component Variables (`xrreg`, `xrcomp`, `xropen`, `xconst`, `parreg`, `parcomp`) — coding rules for each
- §5 Special Codes (−66, −77, −88)
- §6 `polity2` Construction Rules — interpolation treatment
- §7 Country Coding Narratives — per-country histories
- Appendices: authority codes, regime change events, etc.

**Edgar to cite specifically:**
- The §5 special-codes rule when discussing Myanmar 2010 or 2021 transition coding.
- The §6 `polity2` interpolation rule when discussing how research datasets consume Polity.
- The §7 Myanmar narrative for direct quotes or paraphrases about CSP's coding decisions.

**Placeholder until Edgar downloads:**
- Polity V (Polity5) v2018 covers 1800–2018.
- Scoring runs −10 (fully autocratic) to +10 (fully democratic).
- Component scale caps: `xconst` 1–7, `parcomp` 0–5, etc.
- Regime change defined as a ≥3-point shift in `polity` within 3 years.

---

## Readings considered and NOT used here (distinguished from the Orange memo)

- **Walter 2009 "Bargaining Failures and Civil War":** Orange memo reading. Its role is explaining why civil wars happen, not how datasets code them. Skip for data memo.
- **Powell 2006 "War as a Commitment Problem":** background for the Orange memo's commitment-problem vocabulary. Irrelevant for the data memo. Skip.
- **V-Dem codebook and methods papers:** useful if the memo engages the Polity-vs-V-Dem comparison, but one dataset is the assignment. Polity is the anchor. V-Dem comparisons belong in one footnote at most.

---

## Blockers / extraction notes

- Meng & Little extracted cleanly. No OCR work needed.
- Polity V codebook not yet downloaded. Edgar to download from https://www.systemicpeace.org/inscr/p5manualv2018.pdf during Week 6 / Week 7.
- Neither reading needs pagination matched to local file — both are cleanly paginated PDFs.

---

Generated for: Edgar Agunias
Date: 2026-04-16
Model: Claude Opus 4.7 (1M context)
Sources: Meng & Little (PS 2024); Cederman Hug & Krebs (JPR 2010) via Orange memo reading notes; Polity V codebook structure (predicted from Polity IV codebook conventions — Edgar to verify on download); skill `_claudia/skills/memo-summarizer.md`
Agent: Athena
