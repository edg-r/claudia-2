suppressPackageStartupMessages({
  library(dplyr)
  library(purrr)
  library(readr)
  library(rvest)
  library(stringr)
  library(tibble)
  library(xml2)
})

dir.create("data_raw", showWarnings = FALSE, recursive = TRUE)
dir.create("logs", showWarnings = FALSE, recursive = TRUE)

base_url <- "https://www.presidency.ucsb.edu"
categories <- tibble::tribble(
  ~speech_type, ~category_url,
  "inaugural_address", "https://www.presidency.ucsb.edu/documents/app-categories/spoken-addresses-and-remarks/presidential/inaugural-addresses",
  "state_of_the_union", "https://www.presidency.ucsb.edu/documents/app-categories/spoken-addresses-and-remarks/presidential/state-the-union-addresses",
  "state_of_the_union", "https://www.presidency.ucsb.edu/documents/app-categories/citations/presidential/state-the-union-written-messages"
)

abs_url <- function(x) {
  ifelse(str_detect(x, "^https?://"), x, paste0(base_url, x))
}

read_page <- function(url) {
  tryCatch({
    Sys.sleep(0.25)
    read_html(url)
  }, error = function(e) NULL)
}

extract_listing_links <- function(url, speech_type, max_pages = 20) {
  pages <- paste0(url, c("", paste0("?page=", 1:(max_pages - 1))))
  map_dfr(pages, function(page_url) {
    doc <- read_page(page_url)
    if (is.null(doc)) return(tibble(speech_type = character(), title = character(), source_url = character()))
    links <- html_elements(doc, ".node-teaser .field-title a")
    tibble(
      speech_type = speech_type,
      title = html_text2(links),
      source_url = as.character(abs_url(html_attr(links, "href")))
    ) |>
      filter(!is.na(source_url), str_detect(source_url, "/documents/")) |>
      distinct(source_url, .keep_all = TRUE)
  }) |>
    distinct(source_url, .keep_all = TRUE)
}

extract_document <- function(source_url, speech_type, title_hint) {
  doc <- read_page(source_url)
  if (is.null(doc)) {
    return(tibble(
      speech_type = speech_type,
      title = title_hint,
      source_url = source_url,
      president = NA_character_,
      date = NA_character_,
      text_raw = NA_character_,
      notes_on_metadata = "Fetch failed"
    ))
  }

  title <- html_element(doc, "h1") |> html_text2()
  if (is.na(title) || title == "") title <- title_hint

  date <- html_element(doc, ".field-docs-start-date-time .field-item, .date-display-single") |> html_text2()
  president <- html_element(doc, ".field-docs-person .diet-title a, .field-docs-person h3 a") |> html_text2()
  president <- str_remove(president, "\\s*\\([^\\)]*\\)\\s*$")

  body_nodes <- html_elements(doc, ".field-docs-content, .field-name-field-docs-content, .node-documents .field-item")
  text_raw <- html_text2(body_nodes)
  text_raw <- paste(text_raw[nchar(text_raw) > 0], collapse = "\n\n")

  tibble(
    speech_type = speech_type,
    title = title,
    source_url = source_url,
    president = ifelse(is.na(president) || president == "", NA_character_, president),
    date = ifelse(is.na(date) || date == "", NA_character_, date),
    text_raw = ifelse(text_raw == "", NA_character_, text_raw),
    notes_on_metadata = ifelse(is.na(text_raw), "No text extracted", "Scraped from American Presidency Project")
  )
}

seed_corpus <- function() {
  tibble::tribble(
    ~speech_type, ~title, ~president, ~date, ~source_url, ~text_raw, ~notes_on_metadata,
    "inaugural_address", "First Inaugural Address", "George Washington", "April 30, 1789", "https://www.presidency.ucsb.edu/documents/inaugural-address-14",
    "Among the vicissitudes incident to life no event could have filled me with greater anxieties than that of which the notification was transmitted by your order. The preservation of liberty and the destiny of the republican model of government are justly considered as deeply staked on the experiment entrusted to the hands of the American people.",
    "Seed fallback excerpt, not a full corpus",
    "state_of_the_union", "Annual Message to Congress", "George Washington", "January 8, 1790", "https://www.presidency.ucsb.edu/documents/first-annual-message-0",
    "I embrace with great satisfaction the opportunity which now presents itself of congratulating you on the present favorable prospects of our public affairs. Among the many interesting objects which will engage your attention that of providing for the common defense will merit particular regard. To be prepared for war is one of the most effectual means of preserving peace.",
    "Seed fallback excerpt, not a full corpus",
    "inaugural_address", "First Inaugural Address", "Abraham Lincoln", "March 4, 1861", "https://www.presidency.ucsb.edu/documents/inaugural-address-24",
    "I hold that in contemplation of universal law and of the Constitution the Union of these States is perpetual. No State upon its own mere motion can lawfully get out of the Union. The laws of the Union must be faithfully executed in all the States.",
    "Seed fallback excerpt, not a full corpus",
    "state_of_the_union", "Address Before a Joint Session of Congress on the State of the Union", "Donald J. Trump", "February 4, 2020", "https://www.presidency.ucsb.edu/documents/address-before-joint-session-the-congress-the-state-the-union-27",
    "The years of economic decay are over. The days of our country being used, taken advantage of, and even scorned by other nations are long behind us. We are moving forward at a pace that was unimaginable just a short time ago, and we are never going back.",
    "Seed fallback excerpt, not a full corpus"
  )
}

links <- categories |>
  mutate(data = map2(category_url, speech_type, extract_listing_links)) |>
  select(data) |>
  tidyr::unnest(data) |>
  distinct(source_url, .keep_all = TRUE)

raw <- if (nrow(links) == 0) {
  seed_corpus()
} else {
  pmap_dfr(
    links,
    function(speech_type, title, source_url) {
      extract_document(source_url = source_url, speech_type = speech_type, title_hint = title)
    }
  )
}

if (sum(!is.na(raw$text_raw)) < 10) {
  raw <- seed_corpus()
}

raw <- raw |>
  mutate(
    speech_id = sprintf("us_%s_%04d", speech_type, row_number()),
    year = as.integer(str_extract(date, "\\d{4}")),
    party = NA_character_,
    crisis_period = NA,
    war_period = NA,
    divided_government = NA
  ) |>
  select(speech_id, president, date, year, title, speech_type, source_url, text_raw,
         party, crisis_period, war_period, divided_government, notes_on_metadata)

readr::write_csv(raw, "data_raw/presidential_speeches_raw.csv")

log_text <- c(
  "# Data Collection Log",
  "",
  paste0("Date accessed: ", Sys.Date()),
  "Primary source: American Presidency Project category pages for inaugural addresses and annual messages/State of the Union documents.",
  paste0("Listing URLs: ", paste(categories$category_url, collapse = "; ")),
  paste0("Speeches saved: ", nrow(raw)),
  paste0("Speeches with extracted text: ", sum(!is.na(raw$text_raw))),
  "",
  "Failures or limitations:",
  paste0("- Rows with missing text: ", sum(is.na(raw$text_raw))),
  "- Party, crisis, war, and divided-government metadata were not collected in this first pass and remain blank.",
  "- If APP retrieval returned too few rows, the script used a small seed fallback corpus and marks it in notes_on_metadata.",
  "",
  "---",
  "Generated for: Edgar Agunias",
  paste0("Date: ", Sys.Date()),
  "Model: GPT-5 Codex",
  "Sources: American Presidency Project category pages and selected document pages",
  "Agent: Hephaestus",
  "---"
)
writeLines(log_text, "logs/data_collection_log.md")
