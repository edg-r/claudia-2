# Methods Memo

## Overview

This project implements a first-pass Bureaucratic Boredom Index pipeline in R. The pipeline collects U.S. presidential speeches, cleans text, constructs a transparent dictionary, scores each speech, generates exploratory plots, estimates preliminary models, and exports validation samples.

## Corpus

The acquisition script targets the American Presidency Project category pages for inaugural addresses and annual messages/State of the Union documents. The raw corpus is saved to `data_raw/presidential_speeches_raw.csv`. The clean corpus is saved to `data_clean/presidential_speeches_clean.csv`.

## Metadata

The enrichment script adds presidential party, Congress number, divided or unified government, recession indicator, current-dollar GDP, major-war period, and a combined crisis indicator. Party is drawn from Britannica's presidents table. Congress control is drawn from the Wikipedia party-divisions table. Recession and GDP use FRED's USREC and GDP CSV endpoints. Major-war periods are coded as broad date intervals for major U.S. wars.

## Cleaning

The cleaning script removes bracketed and parenthetical stage directions that explicitly mention audience reactions, collapses whitespace, preserves stopwords, and creates `text_clean`, `text_lower`, and `word_count`.

## Scoring

The main BBI score is:

```text
BBI_z = z(procedural terms per 1,000 words) - z(charismatic terms per 1,000 words)
```

The pipeline also exports `BBI_ratio` with a 0.1 smoothing adjustment and `BBI_net_raw` as a raw per-1,000-word difference.

## Models

The preliminary models estimate BBI as a function of year and speech type, BBI as a function of president and speech type, BBI as a function of divided government, major-war period, recession, and speech type, and procedural and charismatic scores as separate dependent variables.

---
Generated for: Edgar Agunias
Date: 2026-04-29
Model: GPT-5 Codex
Sources: inbox/bbi_autonomous_agent_prompt.md; scripts in democracy_as_boredom_bbi/; Britannica presidents table; Wikipedia party divisions of United States Congresses; FRED GDP and USREC
Agent: Hephaestus
---
