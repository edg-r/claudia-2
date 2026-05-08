# Validation Memo

This memo records first-pass validation checks for the Bureaucratic Boredom Index.

## What Was Checked

- The 10 highest-BBI speeches, 10 lowest-BBI speeches, and 10 middle-range speeches were exported to `outputs/tables/validation_extremes.csv`.
- A reproducible random sample of up to 25 speeches was exported to `outputs/tables/validation_random_sample.csv`.
- Each validation table includes an excerpt for close reading rather than silently trusting the score.

## How To Read the Checks

High-BBI speeches should contain comparatively more references to law, Congress, courts, budgets, agencies, programs, implementation, oversight, reports, or federal/state/local administration. Low-BBI speeches should contain comparatively more language of crisis, destiny, greatness, enemies, betrayal, restoration, sacrifice, or direct claims about the people.

## False Positive Risks

- A speech can score high because it is administratively dense without being democratically constrained. The index may capture bureaucratic governance, not democracy by itself.
- Some early annual messages may use formal institutional vocabulary because of genre conventions rather than stronger democratic accountability.

## False Negative Risks

- War, depression, attacks, or other crisis speeches may score low because legitimate democratic executives use crisis rhetoric during emergencies.
- Charismatic language is not inherently anti-democratic. The concern is whether it replaces procedural accountability, not whether it appears at all.

## Next Validation Step

Hand-code the exported sample for procedural constraint, institutional deference, legal justification, charismatic sovereignty, crisis exceptionalism, enemy construction, and people-as-one rhetoric. Compare hand codes with BBI_z and adjust dictionary terms only after reviewing concrete false positives and false negatives.

---
Generated for: Edgar Agunias
Date: 2026-04-29
Model: GPT-5 Codex
Sources: data_clean/presidential_speeches_bbi_scored.csv; validation exports
Agent: Hephaestus
---
