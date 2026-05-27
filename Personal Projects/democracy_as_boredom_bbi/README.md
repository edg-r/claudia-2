# Democracy as Boredom BBI

This R project builds a first-pass quantitative pipeline for the Bureaucratic Boredom Index (BBI), a speech-based measure of the rhetorical presence of institutional, procedural, and administrative constraint in U.S. presidential speech.

## Research Question

Can presidential speeches be scored for bureaucratic boredom as a proxy for the rhetorical presence of institutional constraint?

## Theoretical Logic

Democracy does not only structure who gets power. It structures how power must justify itself. A constrained executive must speak through institutions, procedures, agencies, budgets, legal authority, and implementation. A less constrained or more personalistic executive has stronger incentives to speak through destiny, unity, crisis, enemies, betrayal, and direct identification with the people.

## Data Source and Corpus

The acquisition script uses American Presidency Project category pages for:

- Inaugural addresses
- Annual messages and State of the Union documents

The script saves raw text and metadata in `data_raw/presidential_speeches_raw.csv`, then cleaned text in `data_clean/presidential_speeches_clean.csv`. If live retrieval fails or yields too few rows, the script falls back to a small seed corpus and marks those rows in `notes_on_metadata`.

The enrichment step adds presidential party, divided or unified government, major-war period, recession, and GDP metadata. Party comes from Britannica's presidents table. Congress control comes from the Wikipedia party-divisions table. Recession and GDP come from FRED's USREC and GDP CSV endpoints.

## Dictionary Logic

The BBI uses two transparent dictionaries:

- `procedural_constraint`: law, Congress, courts, budgets, agencies, programs, oversight, implementation, administration, and related terms.
- `charismatic_sovereignty`: destiny, greatness, enemies, betrayal, crisis, restoration, sacrifice, people-as-one rhetoric, and related terms.

Main score:

```text
BBI_z = z(procedural terms per 1,000 words) - z(charismatic terms per 1,000 words)
```

Alternative scores include a smoothed ratio and a raw net difference. The dictionary lives in `dictionaries/bbi_dictionary.csv`.

## How To Rerun

From the project folder:

```sh
Rscript scripts/00_run_pipeline.R
```

To render the report:

```sh
Rscript -e "rmarkdown::render('docs/bbi_report.Rmd')"
```

## Outputs

- Raw data: `data_raw/presidential_speeches_raw.csv`
- Clean data: `data_clean/presidential_speeches_clean.csv`
- Scored data: `data_clean/presidential_speeches_bbi_scored.csv`
- Figures: `outputs/figures/`
- Tables: `outputs/tables/`
- Logs: `logs/`
- Report and memos: `docs/`

## Known Limitations

This is a U.S.-only pilot and does not identify democracy cross-nationally. GDP begins in 1947, so earlier speeches have missing GDP. War periods are broad major-war intervals and do not capture every military operation or foreign-policy crisis. Divided government is coded from Congress-level party control/trifecta status and does not capture every intra-Congress party switch. Dictionary scores are transparent but blunt, and they require close-reading validation before substantive claims.

## Next Steps

Validate the high, low, and random sample exports by hand or in ATLAS.ti. Then audit the new metadata, add term-level score diagnostics, refine the dictionary after validation, and test the index on cross-national executive speeches against V-Dem measures.

---
Generated for: Edgar Agunias
Date: 2026-04-29
Model: GPT-5 Codex
Sources: inbox/bbi_autonomous_agent_prompt.md; American Presidency Project category pages; Britannica presidents table; Wikipedia party divisions of United States Congresses; FRED GDP and USREC; local R scripts
Agent: Hephaestus
---
