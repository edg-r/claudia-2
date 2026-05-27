# Metadata Enrichment Log

Date: 2026-04-29
Added metadata fields:
- party
- speech_date
- congress, congress_year, congress_year_end, congress_president
- divided_government and congress_control_status
- recession_indicator from FRED USREC by speech month
- gdp_billions_current_dollars and gdp_quarter_date from FRED GDP using nearest prior quarter
- major_war_period, war_period, and war_name from manually coded major U.S. war date intervals
- crisis_period as recession or major_war_period

Source URLs:
- Presidential parties: https://www.britannica.com/place/United-States/Presidents-of-the-United-States
- Congress party divisions: https://en.wikipedia.org/wiki/Party_divisions_of_United_States_Congresses
- FRED GDP: https://fred.stlouisfed.org/graph/fredgraph.csv?id=GDP
- FRED recession indicator: https://fred.stlouisfed.org/graph/fredgraph.csv?id=USREC

Raw rows enriched: 309
Clean rows enriched: 309
Party nonmissing in clean: 309
Congress status nonmissing in clean: 309
Recession indicator nonmissing in clean: 226
GDP nonmissing in clean: 110

Limitations:
- GDP begins in 1947, so earlier speeches have missing GDP.
- Recession indicator coverage begins in the FRED USREC historical series and is monthly.
- War periods are broad major-war intervals and do not capture every military operation or crisis.
- Divided government uses Congress-level party control/trifecta status and does not model intra-Congress party switches in detail.

---
Generated for: Edgar Agunias
Date: 2026-04-29
Model: GPT-5 Codex
Sources: Britannica presidents table; Wikipedia party divisions of United States Congresses; FRED GDP; FRED USREC; manually coded major U.S. war intervals
Agent: Hephaestus
---
