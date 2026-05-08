suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(stringr)
})

dir.create("data_clean", showWarnings = FALSE, recursive = TRUE)
dir.create("logs", showWarnings = FALSE, recursive = TRUE)

raw <- readr::read_csv("data_raw/presidential_speeches_raw.csv", show_col_types = FALSE)

clean_text <- function(x) {
  x |>
    str_replace_all("\\[[^\\]]*(applause|laughter|cheers|inaudible|standing ovation)[^\\]]*\\]", " ") |>
    str_replace_all("\\([^\\)]*(applause|laughter|cheers|inaudible|standing ovation)[^\\)]*\\)", " ") |>
    str_replace_all("\\r|\\n|\\t", " ") |>
    str_replace_all("\\s+", " ") |>
    str_squish()
}

clean <- raw |>
  mutate(
    text_clean = clean_text(text_raw),
    text_lower = str_to_lower(text_clean),
    word_count = str_count(text_lower, "\\b[[:alpha:]][[:alpha:]'-]*\\b")
  ) |>
  filter(!is.na(text_clean), word_count > 20)

readr::write_csv(clean, "data_clean/presidential_speeches_clean.csv")

log_text <- c(
  "# Text Cleaning Log",
  "",
  paste0("Date: ", Sys.Date()),
  "Cleaning decisions:",
  "- Removed bracketed or parenthetical audience reactions and stage directions that explicitly mention applause, laughter, cheers, inaudible audio, or standing ovations.",
  "- Collapsed line breaks, tabs, repeated whitespace, and empty lines.",
  "- Preserved stopwords and politically meaningful phrases for dictionary scoring.",
  "- Created text_clean, text_lower, and word_count fields.",
  "- Lemmas were not produced in this first pass because scoring uses transparent dictionary matching against raw phrases and tokens.",
  "",
  paste0("Input rows: ", nrow(raw)),
  paste0("Clean rows retained: ", nrow(clean)),
  paste0("Rows dropped for missing or very short text: ", nrow(raw) - nrow(clean)),
  "",
  "---",
  "Generated for: Edgar Agunias",
  paste0("Date: ", Sys.Date()),
  "Model: GPT-5 Codex",
  "Sources: data_raw/presidential_speeches_raw.csv",
  "Agent: Hephaestus",
  "---"
)
writeLines(log_text, "logs/text_cleaning_log.md")
