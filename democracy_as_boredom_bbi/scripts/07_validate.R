suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(stringr)
})

dir.create("docs", showWarnings = FALSE, recursive = TRUE)
dir.create("outputs/tables", showWarnings = FALSE, recursive = TRUE)

scored <- readr::read_csv("data_clean/presidential_speeches_bbi_scored.csv", show_col_types = FALSE)

validation <- bind_rows(
  scored |> slice_max(BBI_z, n = 10, with_ties = FALSE) |> mutate(validation_group = "highest_bbi"),
  scored |> slice_min(BBI_z, n = 10, with_ties = FALSE) |> mutate(validation_group = "lowest_bbi"),
  scored |> arrange(abs(BBI_z - median(BBI_z, na.rm = TRUE))) |> slice_head(n = 10) |> mutate(validation_group = "middle_bbi")
) |>
  transmute(
    validation_group,
    speech_id,
    president,
    date,
    year,
    title,
    speech_type,
    BBI_z,
    procedural_terms_per_1000_words,
    charismatic_terms_per_1000_words,
    excerpt = str_trunc(text_clean, 350)
  )

set.seed(20260429)
random_sample <- scored |>
  slice_sample(n = min(25, nrow(scored))) |>
  transmute(speech_id, president, date, year, title, speech_type, BBI_z,
            procedural_terms_per_1000_words, charismatic_terms_per_1000_words,
            excerpt = str_trunc(text_clean, 350))

readr::write_csv(validation, "outputs/tables/validation_extremes.csv")
readr::write_csv(random_sample, "outputs/tables/validation_random_sample.csv")

memo <- c(
  "# Validation Memo",
  "",
  "This memo records first-pass validation checks for the Bureaucratic Boredom Index.",
  "",
  "## What Was Checked",
  "",
  "- The 10 highest-BBI speeches, 10 lowest-BBI speeches, and 10 middle-range speeches were exported to `outputs/tables/validation_extremes.csv`.",
  "- A reproducible random sample of up to 25 speeches was exported to `outputs/tables/validation_random_sample.csv`.",
  "- Each validation table includes an excerpt for close reading rather than silently trusting the score.",
  "",
  "## How To Read the Checks",
  "",
  "High-BBI speeches should contain comparatively more references to law, Congress, courts, budgets, agencies, programs, implementation, oversight, reports, or federal/state/local administration. Low-BBI speeches should contain comparatively more language of crisis, destiny, greatness, enemies, betrayal, restoration, sacrifice, or direct claims about the people.",
  "",
  "## False Positive Risks",
  "",
  "- A speech can score high because it is administratively dense without being democratically constrained. The index may capture bureaucratic governance, not democracy by itself.",
  "- Some early annual messages may use formal institutional vocabulary because of genre conventions rather than stronger democratic accountability.",
  "",
  "## False Negative Risks",
  "",
  "- War, depression, attacks, or other crisis speeches may score low because legitimate democratic executives use crisis rhetoric during emergencies.",
  "- Charismatic language is not inherently anti-democratic. The concern is whether it replaces procedural accountability, not whether it appears at all.",
  "",
  "## Next Validation Step",
  "",
  "Hand-code the exported sample for procedural constraint, institutional deference, legal justification, charismatic sovereignty, crisis exceptionalism, enemy construction, and people-as-one rhetoric. Compare hand codes with BBI_z and adjust dictionary terms only after reviewing concrete false positives and false negatives.",
  "",
  "---",
  "Generated for: Edgar Agunias",
  paste0("Date: ", Sys.Date()),
  "Model: GPT-5 Codex",
  "Sources: data_clean/presidential_speeches_bbi_scored.csv; validation exports",
  "Agent: Hephaestus",
  "---"
)
writeLines(memo, "docs/validation_memo.md")
