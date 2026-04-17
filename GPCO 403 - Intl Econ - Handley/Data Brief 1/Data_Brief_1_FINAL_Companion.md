# Data Brief 1 — Farm-to-Table Companion

**For:** Edgar Agunias
**Course:** GPCO 403 International Economics (Prof. Handley), Spring 2026
**Partner document:** `Data_Brief_1_FINAL_Agunias.pdf`
**Purpose:** Teaching walkthrough. Every number in the final submission traced back to its source, every formula explained in plain English, every intuition built before the arithmetic. Read this start-to-finish once, then use it as a reference for Data Brief 2.

---

## How to use this document

The "farm to table" framing is literal. Section 1 is the farm: the raw IMF databases where every number grew. Section 2 is the ingredient list: each variable with its official code and what it actually measures in the world. Section 3 is the fork in the road where two cooking methods for the same dish diverge. Sections 4 through 6 are the three Part B dishes, plated one at a time. Section 7 is the recipe card you could hand to a stranger to reproduce the meal. Section 8 is the pantry dictionary.

Read intuition first, then arithmetic. Every number ties back to a named series code or a written formula. There are no bare "approximately" figures.

---

## 1. The Two Data Sources (The Farm)

Every number in Part A comes from one of two IMF databases. Knowing which number comes from which database, and why the IMF publishes them separately, is half the battle for any data brief in this course.

### 1.1 IMF World Economic Outlook (WEO), October 2025 release

**What it is.** The WEO is the IMF's flagship macroeconomic database. It reports GDP, inflation, current account, fiscal balances, and dozens of other headline indicators for roughly 190 countries, going back to 1980 and forward through a five-to-six-year forecast horizon.

**Who publishes it.** The IMF Research Department.

**Release cadence.** Twice a year. The **April** release supports the Spring Meetings; the **October** release supports the Annual Meetings. Each release re-estimates the entire historical series, so the "2024 value" in the October 2025 WEO can differ slightly from the "2024 value" in the April 2026 WEO. Always cite the vintage.

**Why the October 2025 vintage matters here.** The assignment specifies 2024 as the target year. In the October 2025 vintage, 2024 is the most recent year of **actual** data (not a forecast). Using a later vintage would change the numbers marginally; using the April 2025 vintage would still show 2024 as a partial estimate. October 2025 is the clean choice.

**Reproducible navigation path.**
1. Go to `https://data.imf.org/en/Data-Explorer?datasetUrn=IMF.RES:WEO(9.0.0)`
2. In the filter panel: select Countries = Australia, United States.
3. Select Year = 2024.
4. Select Indicators: `NGDPD`, `NGDP`, `NGDPDPC`, `BCA_NGDPD`, `GGXCNL_NGDP`.
5. Export CSV.

**Exact series codes pulled, with plain-English definitions:**

| Code | Plain English | Unit |
|---|---|---|
| `NGDPD` | Nominal GDP converted into US dollars at an IMF-chosen average exchange rate. "Current prices" means no inflation adjustment. | Billions of current USD |
| `NGDP` | Nominal GDP in the country's own currency. For Australia, Australian dollars. For the US, US dollars. | Billions of domestic currency |
| `NGDPDPC` | GDP per capita in current USD. Exactly `NGDPD` divided by mid-year population. Answers "how much output per person, expressed in a common currency." | USD per person |
| `BCA_NGDPD` | Current account balance expressed as a share of nominal USD GDP. Positive means the country exports more than it imports (broadly). Negative means the opposite. | Percent of GDP |
| `GGXCNL_NGDP` | General government net lending (+) or borrowing (-), as a share of GDP. A fiscal surplus is positive. A fiscal deficit is negative. "General government" means federal plus state plus local combined. | Percent of GDP |

### 1.2 IMF International Financial Statistics (IFS), Exchange Rates

**What it is.** IFS is the IMF's monetary-and-financial-markets database. It covers exchange rates, monetary aggregates, interest rates, balance-of-payments detail, and reserves. For this brief, we only pull the AUD/USD exchange rate.

**How it differs from WEO.** WEO is a once-every-six-months analytical product rebuilt from scratch each release. IFS is a continuously updated statistical feed. For exchange rates specifically, IFS averages **daily market spot rates** across a period. WEO uses its own internal exchange rate baked into the `NGDPD` conversion, which does not always equal the IFS period average.

**Why both rates exist and when they diverge.** IFS gives you the best single-number answer to "what was the market rate during 2024?" WEO gives you internal consistency between its own GDP-in-USD and GDP-in-domestic-currency series. They agree to within a fraction of a percent in most years, but the tiny gap matters for Q3 arithmetic (Section 3 explains this).

**Reproducible navigation path.**
1. Go to `https://data.imf.org/en/Data-Explorer?datasetUrn=IMF.STA:ER(4.0.1)`
2. Country = Australia.
3. Indicator = Domestic currency per US Dollar.
4. Type of Transformation = Period average.
5. Frequency = Annual.
6. Year = 2024.
7. Export.

**Exact series code pulled.**

| Code | Plain English | Unit |
|---|---|---|
| `AUS.XDC_USD.PA_RT.A` | Australian dollars per one US dollar, arithmetic average of daily market rates across the 2024 calendar year. The "PA" in the code stands for period average. The "A" at the end means annual frequency. | AUD per USD |

---

## 2. The Variables (The Ingredients)

Each row below corresponds to one line in Part A of the submission.

| Display name | Series code | Source | Unit | Year | Australia | United States | What it actually measures |
|---|---|---|---|---|---:|---:|---|
| GDP, current US$ (billions) | `NGDPD` | WEO | Billions USD | 2024 | 1,778 | 29,184 | Total output of the economy in one year, valued at that year's prices, expressed in US dollars so you can compare across countries. |
| GDP, current domestic currency (billions) | `NGDP` | WEO | Billions local ccy | 2024 | A$ 2,693 | US$ 29,184 | Same total output, but in the country's own currency. For the US this equals the USD figure by definition. |
| GDP per capita, current USD | `NGDPDPC` | WEO | USD per person | 2024 | 65,373 | 86,601 | Average output per person in USD. First-pass proxy for average material living standards. |
| Exchange rate, domestic per USD | `AUS.XDC_USD.PA_RT.A` | IFS | AUD per USD | 2024 | 1.5167 | 1.0000 (numeraire) | How many Australian dollars it took, on average, to buy one US dollar across 2024. The US entry is 1.0000 by definition since we are measuring dollars per dollar. |
| Current account balance (% GDP) | `BCA_NGDPD` | WEO | Percent of GDP | 2024 | -2.1% | -3.9% | Net flow of goods, services, primary income, and secondary income between the country and the rest of the world, scaled by GDP. Negative means net borrowing from abroad. |
| General government net lending/borrowing (% GDP) | `GGXCNL_NGDP` | WEO | Percent of GDP | 2024 | -1.8% | -7.6% | Fiscal balance of the consolidated public sector. Negative means the government spent more than it collected in revenue. |

Two things to notice.

First, `NGDPD` and `NGDP` for the United States are identical (29,184) because the US dollar is both the domestic currency and the numeraire for international comparison. For Australia the two differ because AUD has to be converted to USD.

Second, `NGDPDPC` is not a convenience calculation. The IMF publishes it directly. If you divide `NGDPD` by population you get roughly the same number, but `NGDPDPC` uses the IMF's own mid-year population estimate and avoids rounding drift.

---

## 3. Exchange Rate Reconciliation (The Fork in the Road)

This is the subtle step that separated a weak draft from a clean final.

### 3.1 The two rates

The assignment permits either of two valid exchange-rate methods for 2024.

**Method 1: IFS annual period-average rate.**
- Source: `AUS.XDC_USD.PA_RT.A` pulled directly from IFS.
- Value: **1.5167 AUD per USD**.
- How it is built: the IMF averages each daily AUD/USD market spot rate across all trading days in 2024, then takes an annual arithmetic mean.

**Method 2: WEO-implied rate (reverse-engineered).**
- Source: derived from two WEO series using GDP identity `NGDP = NGDPD × E`, rearranged to `E = NGDP / NGDPD`.
- Arithmetic: `2,693 / 1,778 = 1.5146 AUD per USD`.
- How it is built: the WEO team picks its own internal exchange rate when converting Australia's GDP from AUD into USD. Dividing the two WEO series reveals that rate.

### 3.2 Why they differ

Both rates describe "AUD per USD on average during 2024," but the averaging methodology is different.

- IFS uses **daily spot market observations**, arithmetically averaged.
- WEO uses a method closer to a **trade-weighted or revenue-weighted average** that emphasizes the exchange rate on days when large economic flows actually occurred. The IMF does not document the exact averaging for every country-year, which is why the number cannot be recovered from first principles and must be backed out from the two GDP series.

The gap for Australia in 2024 is `1.5167 - 1.5146 = 0.0021`, which is `0.0021 / 1.5167 = 0.14%`. Tiny in absolute terms. Large enough to matter for Q3 arithmetic.

### 3.3 Why the final draft used the WEO-implied rate for Q3

If Q3 applies a 10% depreciation and then divides `NGDP` by the new exchange rate to get a new `NGDPD`, you want the exchange rate that is internally consistent with the `NGDPD` you are dividing into. Otherwise the "before" and "after" numbers are drawn from two different conversion conventions and the percentage change picks up noise from the methodology gap, not from the depreciation itself.

Using the WEO-implied 1.5146:
- Before: `2,693 / 1.5146 = 1,778` (matches the published `NGDPD` exactly)
- After: `2,693 / (1.5146 × 1.10) = 2,693 / 1.6661 = 1,616.4`
- Percent change: `(1,616.4 - 1,778) / 1,778 = -9.09%`

This is the clean textbook answer because the pass-through from a 10% depreciation is exactly `1/(1+0.10) - 1 = -9.0909...%`.

Using the IFS 1.5167 instead would give:
- Before: `2,693 / 1.5167 = 1,775.5` (this does not match the published `NGDPD` of 1,778)
- After: `2,693 / (1.5167 × 1.10) = 2,693 / 1.66837 = 1,614.1`
- Percent change relative to published `NGDPD` of 1,778: `(1,614.1 - 1,778) / 1,778 = -9.22%`

The `-9.22%` answer mixes the depreciation shock with the IFS-vs-WEO methodology gap. The `-9.09%` answer isolates only the depreciation shock. That is why the final draft uses the WEO-implied rate for Q3 and flags the IFS rate separately in the sources footnote for source discipline.

### 3.4 Arithmetic both ways, for the record

| Method | Rate | Before USD GDP | After rate | After USD GDP | Percent change |
|---|---:|---:|---:|---:|---:|
| WEO-implied | 1.5146 | 1,778.0 | 1.6661 | 1,616.4 | **-9.09%** |
| IFS period avg | 1.5167 | 1,775.5 | 1.6684 | 1,614.1 | -9.22% |

The submitted answer is the first row.

---

## 4. Part B Q1 — Living Standards (Walk Through)

**The question.** Which indicator best captures average living standards, and what does it say?

### 4.1 Intuition first

You are comparing how well the typical person lives in two countries. You need a measure that:

1. **Totals all the output** produced, so you do not undercount services or home-grown food.
2. **Divides by population**, so a country with more people does not automatically look richer.
3. **Uses a common currency**, so 65,373 in one country and 86,601 in another are on the same scale.

GDP per capita in current USD (`NGDPDPC`) does all three. It is not perfect. It ignores how unequally income is distributed, it leaves out unpaid household labor, and it says nothing about life expectancy or freedom. For a first-pass comparison across two rich democracies in one year, it is the standard workhorse.

### 4.2 The PPP limitation

Prices are not the same across countries. A Big Mac in Sydney costs about AUD 7.70, which at 1.5167 AUD/USD is roughly 5.08 USD. The same Big Mac in Buenos Aires converts to roughly 3.00 USD. In one city a dollar-equivalent buys a smaller portion of the sandwich than in the other.

Apply this to a whole consumption basket and you see the problem. Current-USD GDP per capita tells you how many US-dollar bills of output each person produces. It does not tell you how much that person can actually buy with those dollars at local prices.

Purchasing Power Parity (PPP) adjustments fix this by re-pricing every country's output at a common international price level. For Australia versus the US the PPP adjustment narrows the gap but does not close it.

The final draft names the limitation and states the direction of the adjustment. It does not report a PPP number because the table does not include one.

### 4.3 Arithmetic

| Country | `NGDPDPC` (USD) |
|---|---:|
| Australia | 65,373 |
| United States | 86,601 |

Ratio of Australia to US:
- `65,373 / 86,601 = 0.7549`
- Australia has **about 75.5% of US GDP per capita**, or equivalently Australia is **about 24.5% poorer** by this measure.

The draft rounds to "roughly 25%" which is both accurate and simpler to read.

### 4.4 Direction

Australia is **poorer** than the US on this first-pass measure. PPP would narrow, not reverse, the gap.

---

## 5. Part B Q2 — Sectoral Balances Identity (Walk Through)

**The question.** Given the current account and government balances, what is the private sector balance, and how do you interpret it?

### 5.1 Intuition first

The sectoral balances identity is one of the most important accounting truths in open-economy macro. In plain English: **every dollar a country earns from the rest of the world has to be matched by a dollar somebody inside the country saved rather than spent.**

There are only three "sectors" that can save or dissave in this framework:

1. **The rest of the world.** Its net saving with respect to us is the flip of our current account. If we run a current account deficit, the rest of the world is lending to us; equivalently, we are dissaving relative to the world.
2. **The government.** Its net saving is tax revenue minus total spending. Positive means surplus; negative means deficit.
3. **The private sector.** Households and firms combined. Their net saving is household saving plus retained corporate earnings minus private investment.

The identity forces these three to sum correctly. If the current account is -2.1% of GDP and the government is -1.8% of GDP, the private sector balance is whatever makes the accounting close.

### 5.2 The formula

Start from the macro identity:

```
CA = (S_private − I_private) + (T − G)
```

Where `S_private − I_private` is private net lending (saving minus investment) and `T − G` is government net lending (revenue minus spending).

Rearrange to solve for the private sector:

```
Private net lending = CA − Government net lending
```

### 5.3 Why a negative government balance gets subtracted

This is the step that confuses people. The formula says "subtract government from CA." If government is negative (a deficit), you are subtracting a negative, which flips to adding a positive.

```
Private = CA − Government
Private = (−2.1%) − (−1.8%)
Private = −2.1% + 1.8%
Private = −0.3%
```

The minus-minus flip is not a trick. It is the correct handling of signs. The government ran a 1.8%-of-GDP deficit, meaning it dissaved. That 1.8% of dissaving has to come from somewhere, so it reduces the amount of dissaving the private sector needs to do for the CA to balance.

### 5.4 Plug in 2024 Australia

| Component | Value |
|---|---:|
| Current account balance (`BCA_NGDPD`) | -2.1% |
| Government net lending (`GGXCNL_NGDP`) | -1.8% |
| **Private net lending (derived)** | **-0.3%** |

### 5.5 Interpretation

Private sector net lending of **-0.3% of GDP** means the private sector was a **small net borrower** in 2024. Households and firms together invested slightly more than they saved and financed the shortfall by borrowing.

Intuition check: Australia ran a 2.1% current account deficit. 1.8 percentage points of that came from the government's fiscal deficit. The remaining 0.3 percentage points came from the private sector borrowing modestly. The current account deficit is mostly driven by public dissaving, with private saving-investment roughly balanced but tilting slightly toward borrowing.

### 5.6 Why this was the single biggest substantive change from draft to final

The draft used 2025 numbers: CA = -1.8%, Gov = -2.7%. Under those inputs, `Private = -1.8 - (-2.7) = +0.9%`, a net lender. Under the correct 2024 numbers, the sign flips. Same formula, different year, opposite conclusion. This is a clean lesson in why getting the data year right is not a cosmetic fix.

---

## 6. Part B Q3 — Exchange Rate Pass-Through (Walk Through)

**The question.** If the AUD depreciates 10%, what is the new USD value of Australia's GDP, and what is the percentage change?

### 6.1 Intuition first

"AUD depreciates 10%" means one Australian dollar buys fewer US dollars. Equivalently, it takes more Australian dollars to buy one US dollar. The AUD/USD exchange rate (quoted as AUD per USD) **rises** by 10%.

Now think about what happens to GDP expressed in USD. The conversion is:

```
GDP in USD = GDP in AUD / exchange rate
```

If the denominator goes up, the result goes down. Australia's GDP in AUD has not changed. The economy still produces the same real goods and services. Only the yardstick changed. A bigger denominator means a smaller USD figure.

### 6.2 The setup

| Variable | Value |
|---|---:|
| `NGDP` (Australia, AUD billions) | 2,693 |
| Old exchange rate (WEO-implied) | 1.5146 AUD/USD |
| Published `NGDPD` (USD billions) | 1,778 |
| Depreciation shock | +10% on AUD/USD |

### 6.3 Arithmetic, step by step

**Step 1. New exchange rate.**
```
E_new = 1.5146 × 1.10 = 1.6661 AUD/USD
```

**Step 2. New GDP in USD.**
```
NGDPD_new = NGDP / E_new
NGDPD_new = 2,693 / 1.6661
NGDPD_new = 1,616.4 billion USD
```

**Step 3. Percent change.**
```
% change = (NGDPD_new − NGDPD_old) / NGDPD_old
% change = (1,616.4 − 1,778) / 1,778
% change = −161.6 / 1,778
% change = −0.0909
% change = −9.09%
```

### 6.4 Why it is -9.09% and not -10%

If the exchange rate rises by factor `(1 + Δ)`, then the new USD GDP is:

```
NGDPD_new = NGDP / (E × (1 + Δ))
         = NGDPD_old / (1 + Δ)
```

So the percent change is:

```
(NGDPD_new − NGDPD_old) / NGDPD_old
= (1/(1+Δ)) − 1
= −Δ / (1+Δ)
```

For `Δ = 0.10`:
```
−0.10 / 1.10 = −0.0909...
```

A 10% depreciation of the AUD produces a 9.09% fall in USD-measured GDP, not a 10% fall. This pass-through asymmetry matters. It is the same reason a 10% gain followed by a 10% loss does not leave you flat (you end up at 99% of where you started). Small shocks are close to symmetric; bigger shocks show this curvature more.

Sanity check: a 100% depreciation (rate doubles) would cut USD GDP in half, not to zero. The formula gives `-1.00 / 2.00 = -50%`, which is correct.

### 6.5 What it means in the real world

Nothing about the Australian economy's productive capacity has changed. Real output is identical. What changed is how much of the world's accounting yardstick (the US dollar) Australia's output is worth.

This matters for:

- **IMF quota share** — which is partly weighted by GDP in USD.
- **Global GDP rankings** — a 9% drop can move a country several places in a league table even with no change in actual living standards.
- **External-debt math** — if Australia owes money denominated in USD, a depreciation makes that debt feel heavier relative to the AUD it now earns.
- **Cross-country salary benchmarking** — expats' USD-denominated salaries in Sydney convert to more AUD, but Sydney residents earning AUD now look poorer on Expedia or on international house-price rankings.

What does **not** change: the real wage a Sydney worker earns in AUD, the real price of Australian-produced goods in Australia, or the physical volume of Australian exports.

---

## 7. Reproducibility Checklist (From Farm to Plate)

Follow these steps to pull every number in this brief cold, with no prior context.

### 7.1 Pull the WEO data

1. Open `https://data.imf.org/en/Data-Explorer?datasetUrn=IMF.RES:WEO(9.0.0)`
2. Confirm the release label reads "October 2025" (the URN ends in `(9.0.0)` which is the October 2025 version).
3. Filter Countries: Australia, United States.
4. Filter Year: 2024. (Make sure 2024 is in the "actual" range, not the forecast range.)
5. Filter Indicators: `NGDPD`, `NGDP`, `NGDPDPC`, `BCA_NGDPD`, `GGXCNL_NGDP`.
6. Click Export to CSV.
7. Open the CSV and confirm you see ten rows (five indicators times two countries).

### 7.2 Pull the IFS exchange rate

1. Open `https://data.imf.org/en/Data-Explorer?datasetUrn=IMF.STA:ER(4.0.1)`
2. Country: Australia.
3. Indicator: Domestic currency per US Dollar.
4. Type of Transformation: Period average.
5. Frequency: Annual.
6. Year: 2024.
7. Export.
8. Result should read 1.5167 AUD per USD (small revisions are possible; anything between 1.50 and 1.53 is plausible).

### 7.3 Paste into the Part A table template

Use the units from Section 2. Label every row with its unit and the year.

### 7.4 Compute the implied rate as a cross-check

```
Implied rate = NGDP_AUD / NGDPD_USD = 2,693 / 1,778 = 1.5146
```

If the implied rate differs from the IFS rate by more than 1%, something is wrong. Re-check the year and the country filters.

### 7.5 Run the Q2 identity

```
Private balance = CA (%) − Government (%)
                = -2.1 − (-1.8)
                = -0.3
```

### 7.6 Run the Q3 arithmetic

```
E_new    = E_old × 1.10
NGDPD_new = NGDP_AUD / E_new
% change  = (NGDPD_new − NGDPD_old) / NGDPD_old
          = −0.10 / 1.10
          = −9.09%
```

Use the WEO-implied rate for E_old to get the clean −9.09% result.

### 7.7 Write the prose

Keep Part B at or under the word cap. State each conclusion's direction first, then the number, then the limitation or caveat. Every number in the prose should trace to a cell in Part A or a formula in Sections 5 and 6.

---

## 8. Concept Glossary (Ingredients Dictionary)

**Appreciation.** A currency is worth more in terms of another. One AUD buys more USD than before. Quoted as AUD/USD, appreciation shows up as the rate falling.

**Current account.** The broadest measure of a country's trade and income flows with the rest of the world. Equals net exports of goods and services, plus net primary income (interest, dividends, wages earned abroad), plus net secondary income (remittances, transfers). A current account deficit means the country is drawing net resources from abroad and must be financed by net borrowing or asset sales.

**Depreciation.** A currency is worth less in terms of another. One AUD buys fewer USD than before. Quoted as AUD/USD, depreciation shows up as the rate rising.

**Exchange rate, nominal.** The market price of one currency in terms of another. Not inflation-adjusted. The IFS 1.5167 AUD/USD figure is a nominal rate.

**Exchange rate, real.** The nominal rate adjusted for price-level differences between the two countries. Tells you the relative purchasing power of the two currencies over a basket of goods.

**GDP, nominal (current prices).** The money value of all final goods and services produced in a year, measured at that year's prices. Changes year-to-year both because of real output changes and because of price changes.

**GDP, real.** Nominal GDP stripped of inflation, expressed in a base year's prices. Captures actual changes in output volume.

**GDP, PPP-adjusted.** GDP converted into a common currency using purchasing-power-parity exchange rates rather than market exchange rates. Makes cross-country living-standard comparisons more honest by pricing every country's output at a shared international price level.

**GDP per capita.** GDP divided by population. First-pass proxy for average material living standards.

**General government.** All levels of the public sector combined: federal, state, and local. The counterpart to "private sector" in the sectoral balances identity.

**IFS period average.** The arithmetic average of daily market exchange rates across a period (annual or monthly). In this brief, specifically the 2024 annual average from IMF's International Financial Statistics.

**Net lending/borrowing.** The difference between a sector's income and its spending. Positive means the sector saves more than it invests and lends the surplus to others. Negative means the sector spends more than it earns and borrows the shortfall.

**Numeraire.** The currency in which comparisons are denominated. In this brief, the USD is the numeraire. The US exchange rate row reads 1.0000 because the USD is priced in itself.

**Pass-through (exchange rate).** How much of an exchange-rate change transmits into a price or a measured variable. For GDP-in-USD, pass-through is `−Δ / (1 + Δ)`, which is close to but smaller in magnitude than the raw depreciation for any positive Δ.

**PPP (purchasing power parity).** A method for comparing currencies by asking how many units of each would be needed to buy the same basket of goods. The "Big Mac Index" is the most famous informal PPP.

**Private sector.** Households and firms combined. The residual claimant in the sectoral balances identity.

**Sectoral balances identity.** `CA = (S_private − I_private) + (T − G)`. Says that the country's net financial position with the rest of the world equals the sum of private and government net saving. An accounting truth, not a behavioral theory.

**WEO vintage.** The specific release of the IMF World Economic Outlook that the data came from. Always cite the vintage because each release revises historical numbers.

---

## Edgar's study takeaway

The single biggest lesson from Data Brief 1 was that **wrong year, right formula still fails**. Every formula in the draft was correct. Every arithmetic step was correct. One data-filter mistake (2025 instead of 2024) produced a sign flip on Q2 and a wrong magnitude on Q3. For Data Brief 2 the first step after reading the prompt should be to write the target year in big letters at the top of the scratchpad and confirm it before touching any database.

The second lesson is that **IFS and WEO exchange rates disagree by small amounts, and you have to pick the one that matches the GDP series you are dividing into**. Use the WEO-implied rate when you are doing arithmetic on WEO GDP. Use the IFS rate when you are reporting the market rate.

The third lesson is structural. Every data brief in this course will want a Part A table, source citations, and a Part B short interpretation. Build a reusable template file that locks in the five or six most common WEO series codes (`NGDPD`, `NGDP`, `NGDPDPC`, `BCA_NGDPD`, `GGXCNL_NGDP`, possibly `GGXWDG_NGDP` for debt) and always pull them first. You can add others as the specific brief demands, but these five are the core vocabulary of any macro snapshot.

---

## Output Disclosure

- **Model:** Claude Opus 4.6 (1M context)
- **Date:** 2026-04-15
- **Agent:** Plutus (GPCO 403 class agent)
- **Generated for:** Edgar Agunias
- **Sources:** `Data_Brief_1_FINAL_Agunias.pdf`, `Data_Brief_1_FINAL_Agunias.md`, `crosscheck_plutus.md`, `Data_Brief_1_Calculations_Companion.pdf`, IMF WEO October 2025 release metadata, IMF IFS metadata.
- **Purpose:** Learning companion for Edgar. Not part of the graded submission.
