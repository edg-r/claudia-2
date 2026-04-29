# export_tables.R
# -----------------------------------------------------------------------------
# Standalone export of the four HW1 regression tables to HTML via stargazer.
# Produces table_q3.html, table_q5.html, table_q79.html, table_q11.html
# for archival / regrade / re-import purposes. The docx tables are rebuilt
# separately by rebuild_tables.py from the same coefficient values.
# -----------------------------------------------------------------------------

suppressPackageStartupMessages({
  library(AER)
  library(tidyverse)
  library(stargazer)
})

atlas <- read_csv("atlas.csv", show_col_types = FALSE) %>%
  mutate(
    majority_non_white = as.numeric(share_white2000 < 0.5),
    poverty_pp         = poor_share1990 * 100,
    mobility_k         = kfr_pooled_p25 / 1000
  )

reg_la  <- lm(mobility_k ~ poverty_pp, data = filter(atlas, czname == "Los Angeles"))
reg_ny  <- lm(mobility_k ~ poverty_pp, data = filter(atlas, czname == "New York"))
reg_chi <- lm(mobility_k ~ poverty_pp, data = filter(atlas, czname == "Chicago"))
reg_no  <- lm(mobility_k ~ poverty_pp, data = filter(atlas, czname == "New Orleans"))

no_data   <- atlas %>% filter(czname == "New Orleans")
reg_short <- lm(mobility_k ~ poverty_pp,                      data = no_data)
reg_long  <- lm(mobility_k ~ poverty_pp + majority_non_white, data = no_data)
reg_intx  <- lm(mobility_k ~ poverty_pp * majority_non_white, data = no_data)

reg_all    <- lm(mobility_k ~ poverty_pp + majority_non_white,              data = atlas)
reg_all_fe <- lm(mobility_k ~ poverty_pp + majority_non_white + factor(cz), data = atlas)

data("Fertility2")
fertility2 <- Fertility2 %>%
  mutate(
    morekids_num = as.numeric(morekids == "yes"),
    same_gender  = as.numeric(gender1 == gender2)
  )
iv_first_stage  <- lm(morekids_num ~ same_gender, data = fertility2)
iv_reduced_form <- lm(work         ~ same_gender, data = fertility2)
fertility2 <- fertility2 %>% mutate(morekids_hat = fitted(iv_first_stage))
iv_second_stage <- lm(work ~ morekids_hat, data = fertility2)
iv_aer          <- ivreg(work ~ morekids_num | same_gender, data = fertility2)

stargazer(reg_la, reg_ny, reg_chi, reg_no,
          type = "html", out = "table_q3.html",
          title = "Poverty and Mobility: Simple Regressions by City",
          column.labels = c("Los Angeles", "New York", "Chicago", "New Orleans"),
          dep.var.labels = "Child Income at p25 ($1000s)",
          covariate.labels = c("Poverty Rate 1990 (pp)"),
          omit.stat = c("f", "ser"))

stargazer(reg_short, reg_long, reg_intx,
          type = "html", out = "table_q5.html",
          title = "New Orleans: Poverty, Race, and Upward Mobility",
          column.labels = c("Short (Q3)", "Long (Q4)", "Interaction (Q5)"),
          dep.var.labels = "Child Income at p25 ($1000s)",
          covariate.labels = c("Poverty Rate 1990 (pp)",
                               "Majority Non-White (= 1)",
                               "Poverty x Majority Non-White"),
          omit.stat = c("f", "ser"))

stargazer(reg_all, reg_all_fe,
          type = "html", out = "table_q79.html",
          title = "National Sample: Pooled OLS vs. Commuting-Zone FE",
          column.labels = c("Pooled OLS", "+ CZ Fixed Effects"),
          dep.var.labels = "Child Income at p25 ($1000s)",
          covariate.labels = c("Poverty Rate 1990 (pp)",
                               "Majority Non-White (= 1)"),
          omit = "factor\\(cz\\)",
          omit.stat = c("f", "ser"),
          add.lines = list(c("Commuting-zone FE", "No", "Yes")))

stargazer(iv_first_stage, iv_reduced_form, iv_second_stage, iv_aer,
          type = "html", out = "table_q11.html",
          title = "Angrist-Evans IV: Same-Sex Instrument for Third Child",
          column.labels = c("1st Stage", "Reduced Form", "Manual 2SLS", "AER ivreg()"),
          covariate.labels = c("Same Gender (instrument)",
                               "Predicted More Kids (manual 2SLS)",
                               "More Kids (IV)"),
          omit.stat = c("f", "ser"))

cat("Wrote: table_q3.html table_q5.html table_q79.html table_q11.html\n")
