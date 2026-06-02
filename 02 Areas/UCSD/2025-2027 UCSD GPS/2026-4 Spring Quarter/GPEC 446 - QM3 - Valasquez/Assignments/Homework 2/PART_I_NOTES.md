# Homework 2 Part I Notes

## Data
- Governance panel: `Africa_GDP.Rda`, filtered to 1985-1998.
- GDP per capita: World Bank indicator `NY.GDP.PCAP.KD` (constant US dollars).
- Population: World Bank indicator `SP.POP.TOTL`, used as weights for the representative-person version.
- Final country-year rows with GDP and governance: 623.
- Country-year rows missing GDP or population after World Bank join: 21.

## Q1 Table: average-country estimates
See `table_q1_pooled_within.html` for the standard regression table.

Interpretation: the pooled model compares richer and poorer country-years after absorbing common year shocks; the within model asks whether a given country is richer in years when its political-liberty score is higher, net of country and year fixed effects.

## Q2 TWFE big-improvement estimate
See `table_q2_twfe_bigimp.html` for the standard regression table.

The event-study figure follows the Lab 5 template: construct event time around the treatment year, omit year -1 as the reference period, estimate one TWFE coefficient for each lead/lag, and plot coefficients with 95% confidence intervals. Points before zero are pre-improvement years; points after zero are post-improvement years. A clear upward pre-trend would suggest income growth precedes governance improvement; post-zero movement would be more consistent with income changes following the governance event.

## Q4 Table: representative-person estimates
See `table_q4_representative_person.html` for the standard regression table.

Population weighting changes the estimand from the average country-year to the average person-year. Large-population countries receive much more influence than small countries.

---
Generated for: Edgar Agunias
Date: 2026-05-24
Model: GPT-5 Codex
Sources: Africa_GDP.Rda; World Bank API indicators NY.GDP.PCAP.KD and SP.POP.TOTL
Agent: Tyche
---
