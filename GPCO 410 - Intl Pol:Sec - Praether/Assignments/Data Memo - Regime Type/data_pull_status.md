# Data Pull Status

Accessed on `2026-04-20` in `GPCO 410 - Intl Pol:Sec - Praether/Assignments/Data Memo - Regime Type/`.

## Downloaded

1. `polity5_v2018_timeseries.xls`
   Source URL: `https://www.systemicpeace.org/inscr/p5v2018.xls`
   Notes: direct download worked (`HTTP 200`). CSP's INSCR access page still points to the same `p5v2018` Excel file.

2. `polity5_v2018_codebook.pdf`
   Source URL: `https://www.systemicpeace.org/inscr/p5manualv2018.pdf`
   Notes: direct download worked (`HTTP 200`). PDF metadata reports 85 pages and a creation date of `2020-04-23`.

3. `systemicpeace_inscrdata_access_page.html`
   Source URL: `https://www.systemicpeace.org/inscrdata.html`
   Notes: saved the canonical access page locally to document the live download landing page referenced in `data_plan.md`. The page source still advertises `p5v2018.xls` and `p5manualv2018.pdf` via `http://www.systemicpeace.org/...` links.

## Extraction completed

Created `myanmar_polity5_2000_2018.csv` from `polity5_v2018_timeseries.xls`.

- Country filter: `ccode = 775` and `country = "Myanmar (Burma)"`
- Year window: `2000` through `2018`
- Rows extracted: `19`
- Variables extracted:
  `country`, `scode`, `ccode`, `year`, `polity`, `polity2`, `democ`, `autoc`, `durable`, `xrreg`, `xrcomp`, `xropen`, `xconst`, `parreg`, `parcomp`, `change`, `d5`, `sf`

## Observed Myanmar trajectory in the live file

- `2000-2003`: `polity = -5`, `polity2 = -5`
- `2004-2010`: `polity = -6`, `polity2 = -6`
- `2011-2014`: `polity = -3`, `polity2 = -3`
- `2015`: `polity = -88` (transition), `polity2 = 2`
- `2016-2018`: `polity = 8`, `polity2 = 8`

Relevant component movement in the extract:

- `xconst` moves from `1-2` in the 2000s to `3` in `2011-2014`, then `7` in `2016-2018`
- `parcomp` is `1-2` through `2014`, `-88` in transition year `2015`, then `4` in `2016-2018`

## Coverage gap / version issue

- The current live CSP/INSCR dataset still appears to be `Polity5 v2018`, not a newer public annual release.
- Coverage ends at `2018`, so the dataset does **not** include the `2021` Myanmar coup or any `2019+` observations.
- This matters for the memo because any discussion of post-2018 Myanmar has to be framed as a codebook-rule implication or compared against another dataset rather than cited as an observed Polity5 value.

## Blockers

- No download blocker on `2026-04-20`; all three target URLs resolved directly.
- One local processing blocker occurred: Python could not read the legacy `.xls` workbook until `xlrd` was installed. After installing `xlrd`, the extraction completed successfully.
