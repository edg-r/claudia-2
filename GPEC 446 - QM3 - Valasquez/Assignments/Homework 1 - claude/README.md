# Homework 1 - Codex

This folder contains the Codex-assisted working files for `Homework 1` in `GPEC 446 - QM3 - Valasquez`.

## Files Included

- `Homework_1_Codex.R`: main analysis script. It loads the tract-level data, creates the variables used in the assignment, fits the city-specific and national regressions, builds the open-question summaries, and walks through the manual IV example.
- `README.md`: this file.
- `atlas.csv`: source tract-level dataset used for the mobility, poverty, race, and density sections.
- `Homework_1_Codex.Rmd`: R Markdown companion that appears to produce the rendered outputs in this folder.
- `Homework_1_Codex.html`, `Homework_1_Codex.tex`, `Homework_1_Codex.log`: rendered/output artifacts already present in the folder.
- `city_poverty_mobility.png`, `urban_density_deciles.png`: exported figure files already present in the folder.
- `Homework_1_Instructions.docx`: assignment prompt.

## Assignment Section Map

The R script is now divided by the assignment's own sections and questions. Use
this map when walking through the code or explaining what each block does.

# Setup

This is not one of the numbered homework questions. It loads packages, sets
knitting options, and creates formatting helpers used in the tables.

# Opportunity Atlas: Shared Data Preparation

This block loads `atlas.csv` and creates variables used throughout the
Opportunity Atlas questions:

- `majority_non_white`: equals 1 when `share_white2000 < 0.5`.
- `poverty_pp`: poverty rate converted from a fraction to percentage points.
- `mobility_k`: upward mobility converted from dollars to thousands of dollars.
- `fips`: full census tract code used to match a tract from the website to the data.

# Descriptive Statistics

## Question 1

The assignment asks the student to choose one city from Los Angeles, New York,
Chicago, or New Orleans and describe the clustering and variation visible on the
Opportunity Atlas map.

In the code:

- `cities` lists the four allowed cities.
- `city_data` filters the dataset to those cities.
- `chosen_city <- "New Orleans"` records the city used in the write-up.

## Question 2

The assignment asks the student to choose one census tract in the selected city,
compare its upward mobility to the city average, and compare the city's standard
deviation to the state's standard deviation.

In the code:

- `chosen_city_data` keeps only New Orleans tracts.
- `chosen_tract` selects one tract in New Orleans.
- `chosen_city_mean` computes the New Orleans average.
- `chosen_city_sd` computes the New Orleans tract-level standard deviation.
- `chosen_state_sd` computes the Louisiana tract-level standard deviation.

Current selected tract:

```text
City: New Orleans
State: Louisiana
County: Orleans Parish
Census tract: 121.02
Full tract FIPS: 22071012102
```

# Regression Analysis

## Question 3

The assignment asks for one regression per city, using child income for parents
at the 25th percentile as the dependent variable and poverty rate in 1990 as the
independent variable. It also asks for scatter plots.

In the code:

- `city_models` runs `lm(mobility_k ~ poverty_pp)` separately for each city.
- The `city-scatter` chunk creates the four-panel scatter plot with fitted lines.

## Question 4

The assignment asks whether racial composition is an omitted variable. It
requires the `majority_non_white` dummy, a controlled regression for one city,
and the auxiliary regression needed to apply the omitted-variable-bias formula.

In the code:

- `q4_city <- "New Orleans"` chooses the city for this exercise.
- `model_3` is the poverty-only regression.
- `model_4` adds `majority_non_white`.
- `aux_ovb` regresses `majority_non_white` on `poverty_pp`.
- `predicted_bias` applies the OVB formula.
- `actual_change` compares the coefficient before and after adding the control.

## Question 5

The assignment asks whether the poverty relationship differs in majority
non-white tracts and requires Models 3, 4, and 5 in one formatted table.

In the code:

- `model_5` adds `poverty_pp * majority_non_white`.
- `table_345` combines Models 3, 4, and 5.
- The `models-345-table` chunk prints the formatted regression table.

## Question 6

The assignment asks whether the models can be interpreted causally. This is
answered in prose in the R Markdown/PDF, not by a separate code block.

## Questions 7-9

The assignment asks for a national model with commuting-zone fixed effects,
an explanation of why this is analogous to Dale and Krueger, and a table
comparing the fixed-effects model to the previous model.

In the code:

- `all_base` runs the pooled national regression.
- `all_fe` adds `factor(cz)` for commuting-zone fixed effects.
- `table_fe` compares the two models.
- The `fe-table` chunk prints the fixed-effects comparison table.

# Open Question

The assignment asks for one table, one figure, and one paragraph on urban versus
rural intergenerational mobility.

In the code:

- `popdensity2000` is used as the urban/rural proxy.
- `density_group` separates bottom-density, middle-density, and top-density tracts.
- `open_table` summarizes the top and bottom density quartiles.
- `open_deciles` summarizes mobility by density decile.
- The `open-table` chunk prints the table.
- The `open-figure` chunk prints the figure.

# Instrumental Variable

The assignment asks for the Angrist and Evans fertility example, using same-sex
first two children as an instrument for having a third child. It specifically
asks to run the three regressions manually instead of using `ivreg()`.

In the code:

- `Fertility2` loads the dataset from the `AER` package.
- `same_gender` is the instrument.
- `iv_first_stage` regresses `morekids_num` on `same_gender`.
- `iv_reduced_form` regresses `work` on `same_gender`.
- `morekids_hat` stores fitted values from the first stage.
- `iv_second_stage` regresses `work` on `morekids_hat`.
- The `iv-table` chunk prints the manual 2SLS table.

# Code Understanding Sufficiency Test

The assignment asks the student to list all libraries used and explain 15
functions from those libraries in their own words.

In the code:

- `code_understanding` stores the package/function glossary.
- The final chunk prints the glossary table.

## How The Assignment Was Completed

The code follows the homework in the same order as the prompt. It starts by cleaning and rescaling the tract-level Opportunity Atlas data, then answers the city comparison and OVB questions using New Orleans as the focal city. After that it expands to pooled national regressions with commuting-zone fixed effects, builds a density-based answer to the urban-versus-rural open question, and closes with a manual IV walkthrough using `Fertility2`. The write-up-oriented parts of the script format the regression output into tables and export the two main figures.

## Main Analytical Choices

- Poverty is converted to percentage points to make coefficients easier to read.
- Upward mobility is rescaled into thousands of dollars for cleaner regression output.
- The race control is defined as a majority-non-white indicator based on `share_white2000 < 0.5`.
- The city regression section uses four commuting zones: Los Angeles, New York, Chicago, and New Orleans.
- The regression comparison section uses New Orleans for Models 3-5.
- The fixed-effects extension uses `factor(cz)` to absorb commuting-zone differences.
- The open question uses tract population density as a proxy for urbanicity:
  - quartiles for the urban/rural comparison table
  - deciles for the gradient figure
- The IV section is implemented manually rather than through `ivreg()`, which keeps each stage visible for class purposes.

## How To Re-Run The Analysis

### Option 1: Run the R script directly

From this folder:

```bash
Rscript Homework_1_Codex.R
```

This works if the required packages are already installed and the current working directory is this folder.

### Option 2: Render the R Markdown file

From this folder:

```bash
Rscript -e "rmarkdown::render('Homework_1_Codex.Rmd')"
```

Use this if the intended deliverable is the knitted HTML/PDF-style output rather than the raw script execution.

## Required R Packages

The script loads these packages:

- `dplyr`
- `ggplot2`
- `readr`
- `broom`
- `knitr`
- `kableExtra`
- `stargazer`
- `AER`

If any are missing, install them before rerunning:

```r
install.packages(c("dplyr", "ggplot2", "readr", "broom", "knitr", "kableExtra", "stargazer", "AER"))
```

## Current Limitations / Blockers

- `Homework_1_Codex.R` depends on local relative paths, so it should be run from this folder unless the paths are rewritten.
- The script assumes `atlas.csv` is present and unchanged.
- The IV section uses a manual fitted-value second stage for transparency. That is useful pedagogically, but it does not add the convenience diagnostics that come with a dedicated IV estimator such as `AER::ivreg()`.
- This pass was intentionally limited to readability/documentation changes. It does not audit whether every analytical choice matches the instructor's preferred specification.
