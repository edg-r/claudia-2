# Homework 2 Part I Notes

## Data
- Governance panel: `Africa_GDP.Rda`, filtered to 1985-1998.
- GDP per capita: World Bank indicator `NY.GDP.PCAP.KD` (constant US dollars).
- Population: World Bank indicator `SP.POP.TOTL`, used as weights for the representative-person version.
- Final country-year rows with GDP and governance: 623.
- Country-year rows missing GDP or population after World Bank join: 21.

## Q1 Table: average-country estimates


|model                             |term    | estimate| std_error| statistic| p_value|   n| r_squared| adj_r_squared|
|:---------------------------------|:-------|--------:|---------:|---------:|-------:|---:|---------:|-------------:|
|Pooled OLS + year FE              |pol_lib |  228.965|    55.203|     4.148|   0.000| 623|     0.028|         0.006|
|Within/LSDV: country FE + year FE |pol_lib |   -0.188|    14.113|    -0.013|   0.989| 623|     0.972|         0.970|

Interpretation: the pooled model compares richer and poorer country-years after absorbing common year shocks; the within model asks whether a given country is richer in years when its political-liberty score is higher, net of country and year fixed effects.

## Q2 TWFE big-improvement estimate


|model                          |term   | estimate| std_error| statistic| p_value|   n| r_squared| adj_r_squared|
|:------------------------------|:------|--------:|---------:|---------:|-------:|---:|---------:|-------------:|
|TWFE big improvement indicator |bigimp |   -2.855|    56.887|     -0.05|    0.96| 623|     0.972|          0.97|

The event-study figure should be read as residual GDP per capita after country and year fixed effects. Points before zero are pre-improvement years; points after zero are post-improvement years. A clear upward slope before zero would suggest income growth precedes governance improvement; movement after zero would be more consistent with income changes following the governance event.

## Q4 Table: representative-person estimates


|model                                    |term    | estimate| std_error| statistic| p_value|   n| r_squared| adj_r_squared|
|:----------------------------------------|:-------|--------:|---------:|---------:|-------:|---:|---------:|-------------:|
|Population-weighted pooled OLS + year FE |pol_lib |  179.305|    40.217|     4.458|   0.000| 623|     0.034|         0.012|
|Population-weighted country FE + year FE |pol_lib |   -2.895|     6.922|    -0.418|   0.676| 623|     0.986|         0.985|

Population weighting changes the estimand from the average country-year to the average person-year. Large-population countries, especially Nigeria, Ethiopia, Democratic Republic of Congo, South Africa, Tanzania, Kenya, Sudan, and Uganda, therefore receive much more influence than small countries such as Seychelles, Sao Tome and Principe, and Comoros.

## Files generated
- `part_i_analysis_panel.csv`
- `part_i_missing_wb_join_rows.csv`
- `table_q1_pooled_within.csv`
- `table_q2_twfe_bigimp.csv`
- `event_study_residual_means.csv`
- `event_study_leadlag_coefficients.csv`
- `figure_q2_event_study_residuals.png`
- `table_q4_representative_person.csv`
- `weighted_event_study_residual_means.csv`
- `figure_q4_weighted_event_study_residuals.png`

---
Generated for: Edgar Agunias
Date: 2026-05-18
Model: GPT-5 Codex
Sources: Africa_GDP.Rda; Homework 2 Panel & RDD prompt; World Bank API indicators NY.GDP.PCAP.KD and SP.POP.TOTL
Agent: Tyche
---
