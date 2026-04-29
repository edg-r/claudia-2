# Data Memo — Regime Type (Polity5): Myanmar, 2000–2018

**Status:** Outline only. Prose draft pending Edgar's sign-off on structure + any open data pulls.
**Course:** GPCO 410 — Praether (Spring 2026)
**Dataset:** Polity5 v2018 annual time-series (Center for Systemic Peace / INSCR)
**Unit/window:** Myanmar (ccode 775), 2000–2018

---

## BLUF / Thesis Placeholder

> Myanmar's Polity5 score moves from entrenched autocracy (`polity2 = -6` through 2010) to an anocratic opening (`-3`, 2011–2014) and then to a codified democracy (`+8`, 2016–2018), with 2015 flagged as a formal transition year (`polity = -88`, interpolated `polity2 = 2`). The trajectory is driven almost entirely by changes in executive constraints (`xconst`: 1–2 → 3 → 7) and competitiveness of participation (`parcomp`: 1–2 → 4), not by changes in executive recruitment openness. That component pattern is diagnostic: the score jump reflects elite-negotiated rules constraining the executive, **not** a regime where the military's veto is dissolved — which is why the Polity5-coded democracy still rested on an unresolved commitment problem that later realized in the 2021 coup (outside the dataset window).

Thesis will be sharpened after Edgar confirms whether the memo's analytical payoff should be (a) component-level diagnosis of what Polity is actually measuring in Myanmar, (b) a cross-reference against V-Dem / Freedom House for triangulation, or (c) a bridge back to the ORANGE-memo commitment-problem argument.

---

## Section 1 — Framing the Question (≈1 short para)

- What regime-type question is the memo answering: does Polity5 capture the 2010–2015 Myanmar transition, and if so, through which components.
- Why Myanmar 2000–2018 is a useful case: one of the sharpest single-country Polity2 movements in the v2018 release (-6 → +8 across six years), and a case where the "democratization" label is contested.
- Flag the 2018 cutoff up front so the reader knows the 2021 coup is out of sample.

## Section 2 — Data and Measurement (≈1 short para)

- Source: CSP/INSCR Polity5 v2018 annual time-series (`p5v2018.xls`), pulled 2026-04-20 from `systemicpeace.org/inscr/`.
- Unit: country-year, `ccode = 775`, 19 observations (2000–2018).
- Key variables used: `polity`, `polity2`, `democ`, `autoc`, `xconst`, `parcomp`, `xrreg`, `xrcomp`, `xropen`, `parreg`, `durable`, plus transition flags (`change`, `d5`, `sf`).
- Note the Polity2 convention: transition/interruption codes (`-66`, `-77`, `-88`) are interpolated in `polity2` so the series is usable as a continuous scale. 2015's `polity2 = 2` is an interpolated midpoint, not a coded observation.
- Codebook anchor: `polity5_v2018_codebook.pdf`, pp. cite-specific-pages-once-pulled.

## Section 3 — The Myanmar Trajectory, 2000–2018 (core empirical section)

Structured as three regimes with a transition year:

**3.1 Entrenched autocracy, 2000–2010**
- 2000–2003: `polity2 = -5`.
- 2004–2010: `polity2 = -6` (slight tightening around the 2003 Depayin incident / post-2004 Khin Nyunt purge — confirm dating).
- Component reading: `xconst = 1-2` (unlimited executive), `parcomp = 1-2` (repressed/suppressed), `xropen` closed. Classic closed military regime coding.

**3.2 Anocratic opening, 2011–2014**
- `polity2 = -3` across all four years.
- Driver: `xconst` moves from `1-2` to `3` following the 2008 constitution entering force (2011) and the Thein Sein quasi-civilian government.
- `parcomp` remains `1-2` — participation still tightly managed. The jump is about *executive constraints*, not contestation.
- Analytical beat: Polity is picking up the 2008 constitution's institutional caps on the presidency, not mass-level opening.

**3.3 Transition year, 2015**
- `polity = -88` (coded transition), `polity2 = 2` (interpolated).
- Corresponds to the November 2015 general election, NLD landslide, and the 2016 transfer of government.
- Flag for the reader: the `2` is not an observation; it is Polity's standard linear interpolation across a transition window.

**3.4 Codified democracy, 2016–2018**
- `polity2 = +8` (democracy threshold is +6).
- `xconst = 7` (executive parity / accountability), `parcomp = 4` (competitive).
- But: `xrcomp`, `xropen`, and the military's 25% reserved legislative seats + defense/home/border ministries are **not** legible in the aggregate Polity score. This is where the memo earns its analytical keep — the `+8` codes the civilian-side rules while the Tatmadaw's constitutional veto sits outside the index.

## Section 4 — What Polity Captures and What It Misses (analysis)

- Component decomposition: show that the 2010–2016 score movement is ~entirely `xconst` + `parcomp`, with executive-recruitment variables flat or weakly moving.
- Interpretive claim: Polity5 is, in Myanmar, measuring **constitutional form**, not **effective civilian control**. A measurement story, not a regime-change story.
- Bridge (optional, only if it fits the word cap): this is the same commitment-problem gap the ORANGE memo argues — the 2008 constitution's reserved military powers mean the `+8` regime never eliminated the Tatmadaw's ability to reset the rules, which the 2021 coup (out of sample) realized.
- If space allows, one sentence comparing to a second dataset (V-Dem liberal democracy index or Freedom House) to triangulate. **Open question — see §6.**

## Section 5 — Implications for Measuring Regime Type (≈1 short para)

- Polity5 is strong for detecting **rule changes** (executive constraints, participation rules) and weak for detecting **veto-player structures** that sit behind those rules.
- For Myanmar specifically, a researcher who stops at `polity2` misses the mechanism that later drove the 2021 coup. Component-level reading is not optional.
- Short, one-sentence generalization: anocratic-to-democratic transitions coded via `xconst` alone should be treated as measurement-fragile.

## Section 6 — Open Data Questions / Still to Pull

1. **Codebook page citations** for the `xconst = 7` and `parcomp = 4` category definitions — need exact page numbers from `p5manualv2018.pdf` for the memo's footnotes.
2. **V-Dem or Freedom House comparison series** for Myanmar 2000–2018 — only if Edgar wants Section 4's triangulation sentence. Not pulled yet.
3. **`change`, `d5`, `sf` flag audit** — the extract includes these columns; need to confirm whether any non-zero values in Myanmar 2000–2018 map to CSP's state-failure / regime-change episode list in a way the memo should cite.
4. **Post-2018 framing decision** — confirm with Edgar whether the memo mentions the 2021 coup at all (as a codebook-rule implication / measurement stress test) or stays strictly inside the 2000–2018 window. Current default is a single framing sentence, no post-2018 data claim.
5. **Word/page cap** — confirm target length. Default assumption: 3-page cap per GPCO 410 memo convention (see FEEDBACK.md 2026-04-14).

## Figures / Tables to Build

**Figure 1 — Myanmar Polity2, 2000–2018 (line chart).**
- X: year. Y: `polity2` on the -10/+10 scale.
- Horizontal reference lines at ±6 (democracy / autocracy thresholds).
- Shaded transition band at 2015.
- Annotations: "2008 constitution in force (2011)", "2015 election", "2016 NLD government".

**Figure 2 — Component decomposition, 2000–2018 (small-multiples or stacked line).**
- Panels: `xconst`, `parcomp`, `xrcomp`, `xropen`.
- Purpose: make visible that the score jump is carried by `xconst` and `parcomp`, not by recruitment-side variables.

**Table 1 — Myanmar regime-period summary.**
- Rows: 2000–2010, 2011–2014, 2015, 2016–2018.
- Columns: `polity2`, `xconst`, `parcomp`, short qualitative label, key institutional anchor (e.g., "2008 constitution", "Nov 2015 election").

Optional **Table 2** — side-by-side with V-Dem liberal democracy index for same windows, if §6.2 gets greenlit.

---

## Draft-stage checklist (before Edgar gets prose)

- [ ] Thesis locked (option a/b/c in BLUF section)
- [ ] Codebook page citations pulled
- [ ] Post-2018 framing decision
- [ ] Word cap confirmed
- [ ] Figures 1–2 + Table 1 rendered
- [ ] Second-dataset triangulation decision (V-Dem / FH or skip)

---

## Output Disclosure

- **Model:** Claude Opus 4.7 (1M context) — `claude-opus-4-7[1m]`
- **Date:** 2026-04-24
- **Sources:** `data_pull_status.md` (Athena assignment folder, 2026-04-20); Polity5 v2018 time-series (`p5v2018.xls`), Center for Systemic Peace / INSCR; `polity5_v2018_codebook.pdf`; `COURSE_MEMORY.md` + `FEEDBACK.md` (GPCO 410 Claudia memory, through 2026-04-23).
- **Agent:** Athena (GPCO 410 course agent)
- **Generated for:** Edgar Agunias
