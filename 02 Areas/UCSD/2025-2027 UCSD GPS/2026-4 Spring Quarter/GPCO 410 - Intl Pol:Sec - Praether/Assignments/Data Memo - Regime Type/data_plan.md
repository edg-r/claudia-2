# Data Plan — Polity IV / Polity V

Operational plan for acquiring the dataset, identifying the Myanmar observations, and scoping the "deconstruction" angle Prather's rubric rewards. This is the working document for the empirical side of the data memo. It does not belong in the memo body itself; it feeds the outline.

---

## 1. Where the data lives

**Provider:** Center for Systemic Peace (CSP), directed by Monty G. Marshall.

**Project umbrella:** PolityProject — the Polity series has rolled through Polity I (1974) → Polity II → Polity III → Polity IV (1999 onward) → Polity IV Annual Time-Series → **Polity5 (Polity V)** released 2020 covering years through 2018. Polity V is the current standard release.

**Canonical access page:** https://www.systemicpeace.org/inscrdata.html ("INSCR Data Page"). From that page the Polity5 dataset and codebook are listed under "Polity 5 Annual Time-Series, 1946–2018."

**Direct download (Polity5):**
- Dataset file (Excel): https://www.systemicpeace.org/inscr/p5v2018.xls
- Dataset file (SPSS): https://www.systemicpeace.org/inscr/p5v2018.sav
- Codebook (PDF): https://www.systemicpeace.org/inscr/p5manualv2018.pdf

**Verify before citing:** the URL path may have updated to a newer year-suffix. Land at the INSCR page first, confirm the current filename, then download. Screenshot the INSCR page with date stamp for the footnote.

**Format:** Excel `.xls` is the primary deliverable format. Columns are country-year observations. Key identifier fields: `ccode` (COW country code), `country`, `year`. Avoid `.sav` unless Edgar is running SPSS.

**Access plan for Edgar:**
1. Open https://www.systemicpeace.org/inscrdata.html in a browser.
2. Download `p5v2018.xls` and `p5manualv2018.pdf`. Save both into `Assignments/Data Memo - Regime Type/` with the original filenames.
3. Screenshot the INSCR page landing view. Save as `INSCR_access_YYYY-MM-DD.png` for the footnote.
4. Note the exact Polity version (Polity5 v2018 covers through 2018; a newer release may extend coverage — check the INSCR page notes).

## 2. Variables that matter for the Myanmar argument

The Polity scheme assigns each country-year observations on the following key variables (see codebook §3–§4):

| Variable | What it is | Range | Relevance |
|---|---|---|---|
| `polity` | Raw combined score (DEMOC − AUTOC) | −10 to +10, plus special codes | The headline variable |
| `polity2` | Revised/imputed version of `polity` suitable for time-series analysis (replaces special codes −66/−77/−88 with interpolated or nearest-neighbor values) | −10 to +10 | Used in most quantitative literature including Cederman et al. 2010 |
| `democ` | Democracy subcomponent | 0 to 10 | Built from competitiveness of exec recruitment, openness of exec recruitment, constraints on exec, competitiveness of political participation |
| `autoc` | Autocracy subcomponent | 0 to 10 | Built from the same underlying indicators scored for autocratic features |
| `durable` | Years since last regime-authority change (defined as ≥3-point shift in `polity` in ≤3 years) | integer ≥0 | Used as the "regime stability" proxy |
| `xrreg`, `xrcomp`, `xropen`, `xconst`, `parreg`, `parcomp` | Six component indicators | Categorical scales | The building blocks. The coding ambiguity often lives at this level |
| `change`, `d5`, `sf` | Regime-change flags | — | Mark transitions |

**Special codes — the heart of the coding puzzle the memo should interrogate:**

- **−66 "Foreign Interruption"** — country under foreign occupation; Polity declines to assign a regime score. Historical examples: France 1940–1944, Germany 1945–1949, Kuwait 1990–1991.
- **−77 "Interregnum / Anarchy"** — complete collapse of central political authority. Examples: Lebanon portions of 1975–1990, Somalia 1991–onward, Afghanistan 1979–onward in some editions.
- **−88 "Transition"** — active regime change in progress; assigned to years during which the polity is mid-transition. Typically spans 1–3 years.

In `polity2`, the `polity` special codes are converted:
- −66 → stays as system-missing
- −77 → converted to 0 (treating complete collapse as "neither autocratic nor democratic")
- −88 → prorated linearly between the pre-transition and post-transition scores across the transition years

Prather's "deconstruction" rubric rewards exactly this kind of coding-rule interrogation: why is a transition prorated linearly rather than step-coded? Why is collapse coded as 0 rather than missing?

## 3. Myanmar observations — the actual data

Polity scheme assigns Myanmar as country code `775` (`ccode 775`, "Myanmar (Burma)"). Expected Polity5 series for the memo window:

| Year | `polity` | `polity2` | Notes |
|---|---|---|---|
| 1988 | −88 (transition) | prorated | 8888 uprising; SLORC takes power |
| 1989–2009 | −8 | −8 | Military junta, full autocracy |
| 2010 | −3 or −6 (check codebook edition) | prorated | 2010 election under 2008 constitution, USDP wins |
| 2011–2014 | −3 to −1 (check) | interpolated | Thein Sein reforms; "disciplined democracy" |
| 2015 | transition or +8 step | prorated | NLD landslide; ASSK as State Counsellor |
| 2016–2020 | +8 | +8 | NLD government. Note: this scoring overlooks the 25%-reserved-seats rule |
| 2021 | −88 or −66 in newer editions | prorated/missing | Feb 2021 coup — the coding puzzle for the memo |
| 2022–2024 | not yet in Polity5 v2018 | — | Polity5 v2018 stops at 2018 — need newer CSP release or V-Dem supplement for post-coup coverage |

**Edgar must verify** these values against the actual downloaded `p5v2018.xls` before citing anything. The table above is Athena's best inference from the codebook logic and Cederman et al.'s reported values for Myanmar pre-2010.

**Critical gap:** Polity5 v2018 stops at 2018. The 2021 coup is OUT of coverage. This is itself an angle: if the memo wants to interrogate how Polity codes the 2021 coup, the memo must either (a) check for a Polity5 update file (CSP sometimes issues year-of-release updates), (b) cite the coding rules the codebook specifies for future coups rather than an observed value, or (c) pivot the question to the 2010–2015 transition coding, which is fully in-sample.

Recommended pivot given the gap: **focus the memo on the 2010–2015 Polity coding of Myanmar's partial democratization** rather than the 2021 coup. The 2010 election under the 2008 constitution is a harder coding puzzle than the coup — Polity must decide whether a constitution that reserves 25% of parliament for the military represents a "democracy." This is a richer data memo than the more obvious "how does Polity code a coup" question.

Alternative framing that keeps the 2021 angle: **compare how Polity coded Thailand 2014, Egypt 2013, and Myanmar 2010–2015** — three cases where reserved military powers sit alongside electoral rules. Generalize the coding question using Myanmar as the anchor case.

## 4. The deconstruction question — what the memo actually argues

The rubric's 9 questions map to this storyline:

1. **Dataset:** Polity5 (Polity V) from the Center for Systemic Peace, Annual Time-Series 1946–2018.
2. **Observation:** Myanmar (Burma), `ccode 775`, years 2010–2015 (or 2010–2018 for the full post-reform arc).
3. **Aspect investigated:** the `polity`/`polity2` score during Myanmar's partial democratization, specifically the treatment of the 2008 constitution's reserved military powers in Polity's executive-constraints and political-participation subcomponents.
4. **How coded:** per the codebook, Myanmar transitions from −8 (1988–2009) to a mid-range and then to +8 (2016). Executive constraints (`xconst`) and political participation (`parcomp`) are scored from the electoral rules and observed behavior rather than from structural features of the constitution itself.
5. **Why coded that way:** Polity's conceptual framework privileges *observed* regime behavior (did elections occur? Were they competitive?) over *structural* constraints (is the military constitutionally entrenched?). The 2008 constitution's reserved seats, military ministries, and constitutional veto do not directly enter the executive-constraints score because Polity does not code constitutional military roles in a standard way.
6. **Problematic?** Yes. A government where 25% of the legislature and all security ministries are unaccountable to civilian electoral processes is not substantively a democracy, regardless of how competitive the elected portion of parliament was. Polity's observed-behavior bias inflates the score.
7. **Alternative coding:** lower Myanmar's 2016–2020 `xconst` score to reflect the hard military veto. Alternatively, introduce a new component (or use V-Dem's `v2x_veto` family) that captures reserved-domain constraints on civilian authority. The Meng & Little (2024) critique of subjective-indicator bias cuts in the opposite direction — they argue Polity and V-Dem overstate backsliding because coders read subtle authoritarian moves too aggressively. Engaging both critiques (Polity under-codes reserved-domain autocracy; V-Dem over-codes subjective backsliding) is the sophisticated move.
8. **Example:** Myanmar 2016. Polity2 = +8. Substantive reading: the NLD-led government could not direct the armed forces, could not pass constitutional amendments without military consent, and could not appoint the security cabinet. A score reflecting those structural constraints would sit around +2 to +4 at most. The Cederman et al. 2010 test for democratization periods would then not code 2010–2015 as a major democratization episode — which would materially change the empirical support for the democratization-violence hypothesis.
9. **Implication for IR:** quantitative work on democratization and civil war risk is partially dependent on Polity's observed-behavior coding philosophy. If reserved-domain autocracy (the "guardianship" model — Turkey pre-2001, Pakistan multiple eras, Thailand, Myanmar) were coded more skeptically, the distribution of "democratizations" would shrink. Some of Cederman et al.'s democratization effect may be driven by reserved-domain cases that are not actually democratizing. Myanmar 2021 is then less of a coup against democracy and more of an expected outcome of the military's preserved capacity.

## 5. Resources beyond the core dataset

- **Polity V codebook (`p5manualv2018.pdf`):** read §3 (conceptual framework), §4 (component coding rules), and the country-case narratives for Myanmar.
- **Meng & Little 2024 "Measuring Democratic Backsliding":** methodological critique of subjective indicators. Local file: `W5 - Negotiated Settlements & Democratization/Meng and Little measuring_democratic_backsliding.pdf`. Anchors the measurement-critique side of the argument.
- **V-Dem dataset** (https://v-dem.net/data/the-v-dem-dataset/) as a comparator: Myanmar's V-Dem `v2x_polyarchy` score for 2016–2020 can be contrasted with Polity2 for the same years.
- **Polity IV Country Reports** on Myanmar — CSP produces country-specific narrative reports. Worth downloading if available: https://www.systemicpeace.org/polityproject.html
- **Paul Poast deconstruction thread (COW / Kosovo):** https://twitter.com/ProfPaulPoast/status/1092773608722714624 — tone and format model.
- **Austin Carson deconstruction thread (COW / Korean War):** https://twitter.com/carsonaust/status/1092849151539400704 — same.

## 6. Tooling

Edgar works in Python for QM3 (Tyche). For this data memo, the analysis is descriptive rather than inferential — a table of Myanmar's `polity`/`polity2`/`xconst`/`parcomp` values 2010–2018 plus one or two plots is sufficient. Suggested tooling:

- Pandas to load `p5v2018.xls` (or convert to CSV first via Excel / LibreOffice).
- Matplotlib for a simple time-series plot of Myanmar's `polity2` vs `xconst` 2000–2018.
- Alternative: do the whole thing in Excel and export PNG. For a 3-page memo this is sufficient.

Coordinate with Tyche (GPEC 446) if Edgar wants a cleaner reproducible analysis pipeline — Tyche already maintains Edgar's Python/Jupyter environment. But this is optional; the memo does not require a reproducibility standard beyond a cited codebook version.

---

Generated for: Edgar Agunias
Date: 2026-04-16
Model: Claude Opus 4.7 (1M context)
Sources: Center for Systemic Peace Polity5 codebook structure (Marshall, Gurr, Jaggers), Cederman Hug & Krebs 2010 reported values for Myanmar, V-Dem dataset documentation, Paul Poast and Austin Carson Twitter threads (referenced by syllabus), Meng & Little 2024. Edgar to verify current INSCR URLs and Polity5 release year at data acquisition.
Agent: Athena
