suppressPackageStartupMessages({
  library(dplyr)
  library(lubridate)
  library(readr)
  library(rvest)
  library(stringr)
  library(tibble)
})

dir.create("data_raw", showWarnings = FALSE, recursive = TRUE)
dir.create("data_clean", showWarnings = FALSE, recursive = TRUE)
dir.create("logs", showWarnings = FALSE, recursive = TRUE)

president_party_url <- "https://www.britannica.com/place/United-States/Presidents-of-the-United-States"
congress_url <- "https://en.wikipedia.org/wiki/Party_divisions_of_United_States_Congresses"
gdp_url <- "https://fred.stlouisfed.org/graph/fredgraph.csv?id=GDP"
recession_url <- "https://fred.stlouisfed.org/graph/fredgraph.csv?id=USREC"

normalize_name <- function(x) {
  x |>
    str_replace_all("\\.", "") |>
    str_replace_all(",", "") |>
    str_replace_all(regex("\\b(jr|sr|ii|iii|iv)\\b", ignore_case = TRUE), "") |>
    str_replace_all("\\s+", " ") |>
    str_squish() |>
    str_to_lower()
}

match_name_key <- function(x) {
  normalized <- normalize_name(x)
  key <- vapply(str_split(normalized, "\\s+"), function(parts) {
    parts <- parts[parts != ""]
    if (length(parts) == 0) return(NA_character_)
    paste(parts[1], parts[length(parts)])
  }, character(1))
  case_when(
    normalized == "joseph r biden" ~ "joe biden",
    normalized == "william j clinton" ~ "bill clinton",
    TRUE ~ key
  )
}

party_join_key <- function(x) {
  normalized <- normalize_name(x)
  case_when(
    normalized == "donald j trump" ~ "donald trump",
    normalized == "joseph r biden" ~ "joe biden",
    normalized == "william j clinton" ~ "bill clinton",
    normalized == "richard m nixon" ~ "richard nixon",
    TRUE ~ normalized
  )
}

parse_speech_date <- function(x) {
  suppressWarnings(lubridate::mdy(x))
}

read_president_parties <- function() {
  tryCatch({
    tab <- rvest::html_table(rvest::read_html(president_party_url), fill = TRUE)[[1]]
    tab <- tab[, names(tab) != "", drop = FALSE]
    tab |>
      transmute(
        president_key = normalize_name(president),
        party_join_key = party_join_key(president),
        party = str_squish(`political party`)
      ) |>
      filter(!is.na(president_key), president_key != "", !str_detect(president_key, "died|resigned")) |>
      distinct(party_join_key, party)
  }, error = function(e) tibble(president_key = character(), party_join_key = character(), party = character()))
}

read_congress_control <- function() {
  empty <- tibble(
    congress = integer(),
    congress_year_start = integer(),
    congress_year_end = integer(),
    congress_president = character(),
    trifecta_raw = character(),
    divided_government = logical(),
    congress_control_status = character()
  )
  tryCatch({
    tab <- rvest::html_table(rvest::read_html(congress_url), fill = TRUE)[[1]]
    tab <- tab[, names(tab) != "", drop = FALSE]
    names(tab) <- make.unique(names(tab))
    tab |>
      filter(!is.na(Congress), str_detect(Congress, "^[0-9]")) |>
      transmute(
        congress = as.integer(str_extract(Congress, "\\d+")),
        congress_year_start = as.integer(str_extract(Years, "^\\d{4}")),
        congress_year_end = as.integer(str_extract(Years, "\\d{4}$")),
        congress_president = str_remove_all(President, "\\[[^\\]]+\\]") |> str_squish(),
        trifecta_raw = Trifecta,
        divided_government = case_when(
          str_detect(str_to_lower(trifecta_raw), "^yes$|^yes\\[|yes/") ~ FALSE,
          str_detect(str_to_lower(trifecta_raw), "^no$|^no\\[|no\\*/") ~ TRUE,
          TRUE ~ NA
        ),
        congress_control_status = case_when(
          divided_government == FALSE ~ "unified",
          divided_government == TRUE ~ "divided",
          TRUE ~ "mixed_or_unclear"
        )
      )
  }, error = function(e) empty)
}

read_fred_csv <- function(url) {
  tmp <- tempfile(fileext = ".csv")
  for (attempt in 1:3) {
    ok <- tryCatch({
      download.file(
        url,
        tmp,
        quiet = TRUE,
        method = "curl",
        extra = "--http1.1 --retry 3 --connect-timeout 20 --max-time 60"
      )
      TRUE
    }, error = function(e) FALSE, warning = function(w) FALSE)
    if (ok && file.exists(tmp) && file.info(tmp)$size > 0) {
      return(readr::read_csv(tmp, show_col_types = FALSE))
    }
    Sys.sleep(attempt)
  }
  stop("Could not download FRED CSV from ", url, call. = FALSE)
}

read_fred_gdp <- function() {
  tryCatch({
    read_fred_csv(gdp_url) |>
      transmute(
        gdp_quarter_date = as.Date(observation_date),
        gdp_billions_current_dollars = as.numeric(GDP)
      ) |>
      filter(!is.na(gdp_quarter_date))
  }, error = function(e) {
    stop("GDP metadata download failed. Manual fallback: download https://fred.stlouisfed.org/graph/fredgraph.csv?id=GDP and place it at data_raw/fred_gdp.csv, then update read_fred_gdp() to read that local file.", call. = FALSE)
  })
}

read_fred_recession <- function() {
  tryCatch({
    read_fred_csv(recession_url) |>
      transmute(
        recession_month = floor_date(as.Date(observation_date), "month"),
        recession_indicator = as.integer(USREC)
      ) |>
      filter(!is.na(recession_month))
  }, error = function(e) {
    stop("Recession metadata download failed. Manual fallback: download https://fred.stlouisfed.org/graph/fredgraph.csv?id=USREC and place it at data_raw/fred_usrec.csv, then update read_fred_recession() to read that local file.", call. = FALSE)
  })
}

war_periods <- tibble::tribble(
  ~war_name, ~war_start, ~war_end,
  "War of 1812", "1812-06-18", "1815-02-17",
  "Mexican-American War", "1846-04-25", "1848-02-02",
  "U.S. Civil War", "1861-04-12", "1865-05-26",
  "Spanish-American War", "1898-04-21", "1898-12-10",
  "World War I", "1917-04-06", "1918-11-11",
  "World War II", "1941-12-07", "1945-09-02",
  "Korean War", "1950-06-25", "1953-07-27",
  "Vietnam War", "1964-08-07", "1973-01-27",
  "Persian Gulf War", "1990-08-02", "1991-02-28",
  "Afghanistan War", "2001-10-07", "2021-08-30",
  "Iraq War", "2003-03-20", "2011-12-18"
) |>
  mutate(across(c(war_start, war_end), as.Date))

assign_war <- function(dates) {
  vapply(dates, function(d) {
    if (is.na(d)) return(NA_character_)
    hits <- war_periods |> filter(d >= war_start, d <= war_end) |> pull(war_name)
    if (length(hits) == 0) NA_character_ else paste(hits, collapse = "; ")
  }, character(1))
}

nearest_prior_gdp <- function(dates, gdp) {
  vapply(dates, function(d) {
    if (is.na(d) || nrow(gdp) == 0) return(NA_real_)
    prior <- gdp |> filter(gdp_quarter_date <= d) |> slice_max(gdp_quarter_date, n = 1, with_ties = FALSE)
    if (nrow(prior) == 0) NA_real_ else prior$gdp_billions_current_dollars
  }, numeric(1))
}

nearest_prior_gdp_date <- function(dates, gdp) {
  as.Date(vapply(dates, function(d) {
    if (is.na(d) || nrow(gdp) == 0) return(NA_character_)
    prior <- gdp |> filter(gdp_quarter_date <= d) |> slice_max(gdp_quarter_date, n = 1, with_ties = FALSE)
    if (nrow(prior) == 0) NA_character_ else as.character(prior$gdp_quarter_date)
  }, character(1)))
}

congress_lookup <- function(years, congress_control, field) {
  vapply(years, function(y) {
    if (is.na(y) || nrow(congress_control) == 0) return(NA_character_)
    hit <- congress_control |>
      filter(congress_year_start <= y, congress_year_end > y) |>
      slice_tail(n = 1)
    if (nrow(hit) == 0) NA_character_ else as.character(hit[[field]][1])
  }, character(1))
}

congress_lookup_logical <- function(years, congress_control, field) {
  vapply(years, function(y) {
    if (is.na(y) || nrow(congress_control) == 0) return(NA)
    hit <- congress_control |>
      filter(congress_year_start <= y, congress_year_end > y) |>
      slice_tail(n = 1)
    if (nrow(hit) == 0) NA else as.logical(hit[[field]][1])
  }, logical(1))
}

enrich <- function(df, parties, congress_control, gdp, recession) {
  prior_enrichment <- c(
    "party", "divided_government", "crisis_period", "war_period",
    "speech_date", "congress", "congress_year", "congress_year_end",
    "congress_president", "trifecta_raw", "congress_control_status",
    "recession_indicator", "gdp_billions_current_dollars",
    "gdp_quarter_date", "major_war_period", "war_name",
    "metadata_sources"
  )

  df |>
    select(-any_of(prior_enrichment)) |>
    mutate(
      speech_date = parse_speech_date(date),
      president_key = normalize_name(president),
      party_join_key = party_join_key(president),
      speech_month = floor_date(speech_date, "month")
    ) |>
    left_join(parties |> select(party_join_key, party), by = "party_join_key") |>
    mutate(
      congress_year = if_else(month(speech_date) == 1 & day(speech_date) < 3, year(speech_date) - 1L, year(speech_date)),
      congress = as.integer(congress_lookup(congress_year, congress_control, "congress")),
      congress_year_end = as.integer(congress_lookup(congress_year, congress_control, "congress_year_end")),
      congress_president = congress_lookup(congress_year, congress_control, "congress_president"),
      trifecta_raw = congress_lookup(congress_year, congress_control, "trifecta_raw"),
      divided_government = congress_lookup_logical(congress_year, congress_control, "divided_government"),
      congress_control_status = congress_lookup(congress_year, congress_control, "congress_control_status")
    ) |>
    left_join(recession, by = c("speech_month" = "recession_month")) |>
    mutate(
      war_period = !is.na(assign_war(speech_date)),
      major_war_period = war_period,
      war_name = assign_war(speech_date),
      crisis_period = if_else(coalesce(recession_indicator, 0L) == 1L | major_war_period, TRUE, FALSE),
      gdp_billions_current_dollars = nearest_prior_gdp(speech_date, gdp),
      gdp_quarter_date = nearest_prior_gdp_date(speech_date, gdp),
      metadata_sources = paste(
        "Party: Britannica presidents table",
        "Congress control: Wikipedia party divisions of United States Congresses",
        "Recession and GDP: FRED USREC/GDP",
        "War periods: manually coded major U.S. war date intervals",
        sep = "; "
      )
    ) |>
    select(
      -president_key,
      -party_join_key,
      -speech_month
    )
}

parties <- read_president_parties()
congress_control <- read_congress_control()
gdp <- read_fred_gdp()
recession <- read_fred_recession()

raw <- readr::read_csv("data_raw/presidential_speeches_raw.csv", show_col_types = FALSE)
clean <- readr::read_csv("data_clean/presidential_speeches_clean.csv", show_col_types = FALSE)

raw_enriched <- enrich(raw, parties, congress_control, gdp, recession)
clean_enriched <- enrich(clean, parties, congress_control, gdp, recession)

readr::write_csv(raw_enriched, "data_raw/presidential_speeches_raw.csv")
readr::write_csv(clean_enriched, "data_clean/presidential_speeches_clean.csv")

log_text <- c(
  "# Metadata Enrichment Log",
  "",
  paste0("Date: ", Sys.Date()),
  "Added metadata fields:",
  "- party",
  "- speech_date",
  "- congress, congress_year, congress_year_end, congress_president",
  "- divided_government and congress_control_status",
  "- recession_indicator from FRED USREC by speech month",
  "- gdp_billions_current_dollars and gdp_quarter_date from FRED GDP using nearest prior quarter",
  "- major_war_period, war_period, and war_name from manually coded major U.S. war date intervals",
  "- crisis_period as recession or major_war_period",
  "",
  "Source URLs:",
  paste0("- Presidential parties: ", president_party_url),
  paste0("- Congress party divisions: ", congress_url),
  paste0("- FRED GDP: ", gdp_url),
  paste0("- FRED recession indicator: ", recession_url),
  "",
  paste0("Raw rows enriched: ", nrow(raw_enriched)),
  paste0("Clean rows enriched: ", nrow(clean_enriched)),
  paste0("Party nonmissing in clean: ", sum(!is.na(clean_enriched$party))),
  paste0("Congress status nonmissing in clean: ", sum(!is.na(clean_enriched$congress_control_status))),
  paste0("Recession indicator nonmissing in clean: ", sum(!is.na(clean_enriched$recession_indicator))),
  paste0("GDP nonmissing in clean: ", sum(!is.na(clean_enriched$gdp_billions_current_dollars))),
  "",
  "Limitations:",
  "- GDP begins in 1947, so earlier speeches have missing GDP.",
  "- Recession indicator coverage begins in the FRED USREC historical series and is monthly.",
  "- War periods are broad major-war intervals and do not capture every military operation or crisis.",
  "- Divided government uses Congress-level party control/trifecta status and does not model intra-Congress party switches in detail.",
  "",
  "---",
  "Generated for: Edgar Agunias",
  paste0("Date: ", Sys.Date()),
  "Model: GPT-5 Codex",
  "Sources: Britannica presidents table; Wikipedia party divisions of United States Congresses; FRED GDP; FRED USREC; manually coded major U.S. war intervals",
  "Agent: Hephaestus",
  "---"
)
writeLines(log_text, "logs/metadata_enrichment_log.md")
