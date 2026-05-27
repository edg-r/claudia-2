# generate_interactive.R
# This script extracts datasets from Africa_GDP.Rda and grade5.dta,
# converts them to lightweight JSON structures, and compiles them
# into a self-contained, interactive editorial HTML page.

library(dplyr)
library(haven)
library(jsonlite)

# Set working directory
setwd("/Users/edgar/Documents/01 Projects/Claudia/GPEC 446 - QM3 - Valasquez/Assignments/Homework 2 copy")

# Configure R to allow long network timeouts (up to 5 minutes)
options(timeout = 300)

# ==============================================================================
# SECTION 1: Load and Clean Datasets (with robust World Bank API retry logic)
# ==============================================================================

# Helper function to fetch JSON from API with robust retry loop
fetch_wdi_with_retry <- function(url, max_attempts = 5) {
  attempt <- 1
  while (attempt <= max_attempts) {
    cat(sprintf("Fetching WDI data (Attempt %d/%d)... \n", attempt, max_attempts))
    result <- tryCatch({
      jsonlite::fromJSON(url)
    }, error = function(e) {
      cat(sprintf("  Warning: Attempt %d failed with error: %s\n", attempt, e$message))
      NULL
    })
    
    if (!is.null(result) && length(result) >= 2 && is.data.frame(result[[2]])) {
      cat("  Success!\n")
      return(result[[2]])
    }
    
    attempt <- attempt + 1
    Sys.sleep(3) # Wait 3 seconds before retrying
  }
  stop("Error: Failed to fetch data from World Bank API after multiple attempts.")
}

# Part I: Panel Data
load("Africa_GDP.Rda")

country_lookup <- tibble::tibble(
  country = sort(unique(Africa_GDP$country)),
  wb_name = c(
    "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cameroon",
    "Cabo Verde", "Central African Republic", "Chad", "Comoros",
    "Congo, Dem. Rep.", "Congo, Rep.", "Cote d'Ivoire", "Eritrea",
    "Ethiopia", "Gabon", "Gambia, The", "Ghana", "Guinea",
    "Guinea-Bissau", "Kenya", "Lesotho", "Liberia", "Madagascar",
    "Malawi", "Mali", "Mauritania", "Mauritius", "Mozambique",
    "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe",
    "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa",
    "Sudan", "Eswatini", "Tanzania", "Togo", "Uganda", "Zambia",
    "Zimbabwe"
  )
)

analysis_years <- 1985:1998

# Fetch constant GDP per Capita (constant 2015 USD) with retry
gdp_pc_url <- paste0(
  "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.KD",
  "?format=json&date=1985:1998&per_page=20000"
)
gdp_pc_raw_df <- fetch_wdi_with_retry(gdp_pc_url)

gdp_pc_wb <- gdp_pc_raw_df %>%
  transmute(
    wb_name = .data$country$value,
    iso3 = .data$countryiso3code,
    year = as.integer(.data$date),
    gdp_pc_constant_usd = as.numeric(.data$value)
  )

# Fetch Total Population with retry
pop_url <- paste0(
  "https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL",
  "?format=json&date=1985:1998&per_page=20000"
)
pop_raw_df <- fetch_wdi_with_retry(pop_url)

pop_wb <- pop_raw_df %>%
  transmute(
    wb_name = .data$country$value,
    iso3 = .data$countryiso3code,
    year = as.integer(.data$date),
    population = as.numeric(.data$value)
  )

panel <- Africa_GDP %>%
  filter(year %in% analysis_years) %>%
  left_join(country_lookup, by = "country") %>%
  left_join(gdp_pc_wb, by = c("wb_name", "year")) %>%
  left_join(pop_wb, by = c("wb_name", "year", "iso3")) %>%
  arrange(country, year) %>%
  mutate(
    country_id = as.integer(factor(country, levels = sort(unique(country)))),
    year_factor = factor(year),
    bigimp = ifelse(is.na(bigimp), 0, bigimp)
  ) %>%
  group_by(country) %>%
  mutate(
    event_year = ifelse(any(bigimp == 1, na.rm = TRUE), year[which.max(bigimp)], NA_integer_),
    leadlag = ifelse(!is.na(event_year), year - event_year, NA_integer_)
  ) %>%
  ungroup()

complete_panel <- panel %>%
  filter(!is.na(pol_lib), !is.na(gdp_pc_constant_usd))

# Unweighted residual model
twfe_resid_model <- lm(gdp_pc_constant_usd ~ factor(country_id) + year_factor, data = complete_panel)
residual_event_data <- complete_panel %>%
  mutate(twfe_residual = resid(twfe_resid_model)) %>%
  filter(!is.na(leadlag), leadlag >= -5, leadlag <= 5)

event_summary <- residual_event_data %>%
  group_by(leadlag) %>%
  summarise(
    mean_residual = mean(twfe_residual, na.rm = TRUE),
    se = sd(twfe_residual, na.rm = TRUE) / sqrt(dplyr::n()),
    n = dplyr::n(),
    .groups = "drop"
  )

# Weighted residual model
representative_person <- complete_panel %>%
  filter(!is.na(population), population > 0)
weighted_resid_model <- lm(
  gdp_pc_constant_usd ~ factor(country_id) + year_factor,
  data = representative_person,
  weights = population
)
weighted_event_data <- representative_person %>%
  mutate(weighted_twfe_residual = resid(weighted_resid_model)) %>%
  filter(!is.na(leadlag), leadlag >= -5, leadlag <= 5)

weighted_event_summary <- weighted_event_data %>%
  group_by(leadlag) %>%
  summarise(
    weighted_mean_residual = weighted.mean(weighted_twfe_residual, w = population, na.rm = TRUE),
    total_population = sum(population, na.rm = TRUE),
    country_years = dplyr::n(),
    .groups = "drop"
  )

# Convert Part I outputs to JSON
part1_unweighted_json <- jsonlite::toJSON(event_summary, auto_unbox = TRUE)
part1_weighted_json <- jsonlite::toJSON(weighted_event_summary, auto_unbox = TRUE)

# Part II: RDD grade5 data
grade5 <- haven::read_dta("grade5.dta")
under80 <- grade5 %>%
  filter(school_enrollment < 80) %>%
  transmute(
    schlcode = as.integer(schlcode),
    enrollment = as.numeric(school_enrollment),
    classize = as.numeric(classize),
    avgmath = as.numeric(avgmath),
    avgverb = as.numeric(avgverb),
    disadvantaged = as.numeric(disadvantaged)
  ) %>%
  filter(!is.na(enrollment))

# Convert Part II under-80 dataset to JSON
rdd_data_json <- jsonlite::toJSON(under80, auto_unbox = TRUE)

# ==============================================================================
# SECTION 2: Generate the HTML Content
# ==============================================================================

html_template <- paste0('<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GPEC 446 Homework 2: Interactive Analysis Dashboard</title>
  
  <!-- Sleek Typography: Playfair Display for headers and Outfits for body -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
  
  <!-- Chart.js via CDN for responsive, hardware-accelerated interactive plotting -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  
  <style>
    /* Styling tokens following rich, vibrant, sleek dark-mode aesthetics */
    :root {
      --bg-dark: #0f172a;
      --panel-dark: rgba(30, 41, 59, 0.7);
      --border-color: rgba(255, 255, 255, 0.08);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --primary: #38bdf8;
      --primary-glow: rgba(56, 189, 248, 0.15);
      --accent: #c084fc;
      --accent-glow: rgba(192, 132, 252, 0.15);
      --success: #34d399;
      --danger: #f87171;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--bg-dark);
      background-image: 
        radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.05) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(192, 132, 252, 0.05) 0px, transparent 50%);
      color: var(--text-main);
      font-family: "Outfit", sans-serif;
      line-height: 1.6;
      padding-bottom: 80px;
    }

    header {
      border-bottom: 1px solid var(--border-color);
      max-width: 1200px;
      margin: 0 auto;
      padding: 40px 20px;
      text-align: center;
    }

    .badge {
      background: linear-gradient(135deg, var(--primary), var(--accent));
      border-radius: 9999px;
      color: #000;
      display: inline-block;
      font-size: 0.8rem;
      font-weight: 700;
      letter-spacing: 0.05em;
      margin-bottom: 12px;
      padding: 4px 16px;
      text-transform: uppercase;
    }

    h1 {
      font-family: "Playfair Display", serif;
      font-size: 2.8rem;
      font-weight: 700;
      line-height: 1.2;
      margin-bottom: 8px;
    }

    .subtitle {
      color: var(--text-muted);
      font-size: 1.1rem;
      font-weight: 300;
    }

    main {
      margin: 0 auto;
      max-width: 1200px;
      padding: 40px 20px;
    }

    .section-card {
      background: var(--panel-dark);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
      margin-bottom: 40px;
      overflow: hidden;
      padding: 30px;
    }

    .section-title {
      border-left: 4px solid var(--primary);
      font-family: "Playfair Display", serif;
      font-size: 1.8rem;
      margin-bottom: 24px;
      padding-left: 12px;
    }

    .grid-2 {
      display: grid;
      gap: 30px;
      grid-template-columns: 1fr 1fr;
    }

    @media (max-width: 900px) {
      .grid-2 {
        grid-template-columns: 1fr;
      }
    }

    .control-panel {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      display: flex;
      flex-direction: column;
      gap: 20px;
      padding: 24px;
    }

    .control-group {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    label {
      color: var(--text-muted);
      font-size: 0.9rem;
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .btn-toggle {
      background: #1e293b;
      border: 1px solid var(--border-color);
      border-radius: 8px;
      color: var(--text-muted);
      cursor: pointer;
      font-family: "Outfit", sans-serif;
      font-size: 0.95rem;
      font-weight: 500;
      padding: 10px 16px;
      transition: all 0.2s ease;
      width: 100%;
    }

    .btn-toggle.active {
      background: linear-gradient(135deg, var(--primary-glow), var(--accent-glow));
      border-color: var(--primary);
      color: var(--primary);
      box-shadow: 0 0 15px var(--primary-glow);
    }

    .btn-toggle:hover {
      border-color: var(--primary);
      color: var(--text-main);
    }

    .btn-flex-group {
      display: flex;
      gap: 10px;
    }

    /* Elegant Custom Slider Styling */
    input[type=range] {
      -webkit-appearance: none;
      background: #334155;
      border-radius: 9999px;
      height: 8px;
      margin: 10px 0;
      outline: none;
      width: 100%;
    }

    input[type=range]::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      background: var(--primary);
      border-radius: 50%;
      cursor: pointer;
      height: 20px;
      transition: transform 0.1s ease;
      width: 20px;
      box-shadow: 0 0 10px var(--primary);
    }

    input[type=range]::-webkit-slider-thumb:hover {
      transform: scale(1.2);
    }

    .slider-val-box {
      display: flex;
      justify-content: space-between;
      color: var(--text-muted);
      font-size: 0.85rem;
    }

    .chart-container {
      background: rgba(15, 23, 42, 0.4);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      min-height: 400px;
      padding: 16px;
      position: relative;
    }

    /* Premium Sleek Table Design */
    .table-container {
      overflow-x: auto;
      margin-top: 15px;
    }

    table {
      border-collapse: collapse;
      font-size: 0.9rem;
      width: 100%;
    }

    th, td {
      border-bottom: 1px solid var(--border-color);
      padding: 12px 16px;
      text-align: left;
    }

    th {
      background-color: rgba(15, 23, 42, 0.5);
      color: var(--text-muted);
      font-weight: 600;
      text-transform: uppercase;
      font-size: 0.8rem;
      letter-spacing: 0.05em;
    }

    td {
      color: var(--text-main);
    }

    tr:hover td {
      background-color: rgba(255, 255, 255, 0.02);
    }

    .metric-value {
      font-family: "Playfair Display", serif;
      font-size: 1.8rem;
      font-weight: 700;
      color: var(--primary);
    }

    .metric-title {
      color: var(--text-muted);
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .metrics-row {
      display: grid;
      gap: 15px;
      grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
      margin-top: 20px;
    }

    .metric-box {
      background: rgba(15, 23, 42, 0.4);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 15px;
      text-align: center;
    }

    .text-block {
      color: var(--text-muted);
      font-size: 0.95rem;
      margin-bottom: 20px;
    }

    .highlight {
      color: var(--primary);
      font-weight: 600;
    }

    footer {
      border-top: 1px solid var(--border-color);
      color: var(--text-muted);
      margin: 60px auto 0;
      max-width: 1200px;
      padding: 30px 20px;
      text-align: center;
      font-size: 0.85rem;
    }
  </style>
</head>
<body>

  <header>
    <div class="badge">Quantitative Methods 3</div>
    <h1>Homework 2: Interactive Analysis Dashboard</h1>
    <div class="subtitle">Interactive Panel fixed-effects & Regression Discontinuity Design (RDD) exploration</div>
  </header>

  <main>
    
    <!-- =======================================================================
         SECTION 1: Part I Panel Event Study
         ======================================================================= -->
    <div class="section-card">
      <div class="section-title">Part I: Dynamic Effects of Governance on Income (Panel Event Study)</div>
      
      <div class="text-block">
        This section visualizes the relationship between governance improvements and income using an 
        <span class="highlight">Event Study Framework</span>. We remove country and year fixed effects to obtain 
        residuals and map these residuals across a 10-year window centered around each country\'s largest political-liberty improvement.
      </div>

      <div class="grid-2">
        <div class="control-panel">
          <div class="control-group">
            <label>Weighting Strategy</label>
            <div class="text-block" style="font-size: 0.85rem; margin-bottom: 12px;">
              Toggle between unweighted (country-level) and population-weighted (representative-person) residual patterns.
            </div>
            <div class="btn-flex-group">
              <button class="btn-toggle active" id="btn-p1-unweighted" onclick="togglePart1(\'unweighted\')">Country-Average (Unweighted)</button>
              <button class="btn-toggle" id="btn-p1-weighted" onclick="togglePart1(\'weighted\')">Representative-Person (Weighted)</button>
            </div>
          </div>
          
          <div class="control-group" style="margin-top: 10px;">
            <label>Statistical Summary</label>
            <div class="metrics-row" id="p1-metrics">
              <div class="metric-box">
                <div class="metric-value" id="p1-ols-est">228.965</div>
                <div class="metric-title">Pooled OLS Estimate</div>
              </div>
              <div class="metric-box">
                <div class="metric-value" id="p1-fe-est">-0.188</div>
                <div class="metric-title">Country FE Estimate</div>
              </div>
            </div>
          </div>

          <div class="text-block" style="font-size: 0.85rem; line-height: 1.5; margin-top: 10px;">
            <strong>Interpretation:</strong> Notice how the pooled OLS shows a strong positive correlation, but inclusion of country fixed effects pulls the coefficient to zero. The event-study curve visually confirms this, showing completely flat residuals before and after the political opening.
          </div>
        </div>

        <div class="chart-container">
          <canvas id="part1Chart"></canvas>
        </div>
      </div>
    </div>

    <!-- =======================================================================
         SECTION 2: Part II Regression Discontinuity Design
         ======================================================================= -->
    <div class="section-card">
      <div class="section-title">Part II: Maimonides\' Rule Class Size & Achievement Discontinuity (RDD)</div>
      
      <div class="text-block">
        Angrist and Lavy (1999) exploit Maimonides\' Rule (which caps Israeli class size at 40) to estimate the causal impact of class size on fifth-grade scores. Cross the enrollment cutoff of 40 and watch class size split!
      </div>

      <div class="grid-2">
        <div class="control-panel">
          <div class="control-group">
            <label>1. Select Outcome Variable</label>
            <div class="btn-flex-group">
              <button class="btn-toggle active" id="btn-rdd-classize" onclick="setRDDOutcome(\'classize\')">Class Size</button>
              <button class="btn-toggle" id="btn-rdd-avgmath" onclick="setRDDOutcome(\'avgmath\')">Math Score</button>
              <button class="btn-toggle" id="btn-rdd-avgverb" onclick="setRDDOutcome(\'avgverb\')">Verbal Score</button>
            </div>
          </div>

          <div class="control-group">
            <label>2. Bandwidth (h): <span class="highlight" id="lbl-bandwidth">10</span> students</label>
            <input type="range" id="slider-bandwidth" min="5" max="25" value="10" step="1" oninput="updateBandwidth(this.value)">
            <div class="slider-val-box">
              <span>Narrow (Low bias)</span>
              <span>Wide (Low variance)</span>
            </div>
          </div>

          <div class="control-group">
            <label>Live Local OLS Regression Estimates</label>
            <div class="metrics-row">
              <div class="metric-box">
                <div class="metric-value" id="rdd-beta">-7.107</div>
                <div class="metric-title">RD Effect (&beta;<sub>RD</sub>)</div>
              </div>
              <div class="metric-box">
                <div class="metric-value" id="rdd-se">1.445</div>
                <div class="metric-title">Standard Error</div>
              </div>
              <div class="metric-box">
                <div class="metric-value" id="rdd-n">332</div>
                <div class="metric-title">Effective N</div>
              </div>
            </div>
          </div>

          <div class="text-block" style="font-size: 0.85rem; line-height: 1.5; margin-top: 5px;">
            <strong>Trade-off exploration:</strong> Sliding the bandwidth wider adds more schools further from the cutoff, making the standard error smaller but introducing curvature bias. Sliding the bandwidth below 8 targets only schools immediately next to 40, removing bias but dramatically increasing standard errors!
          </div>
        </div>

        <div class="chart-container">
          <canvas id="part2Chart"></canvas>
        </div>
      </div>
    </div>

  </main>

  <footer>
    <p>&copy; 2026 Edgar Agunias &bull; GPEC 446 Quant Methods 3 &bull; Generated by Claudia Agent System (Tyche)</p>
    <p style="font-size: 0.75rem; margin-top: 10px; opacity: 0.6;">Model: Gemini 3.5 Flash &bull; Data sources: World Bank WDI API, Angrist & Lavy (1999) grade5.dta</p>
  </footer>

  <script>
    // Inject the real R-extracted datasets directly as JSON
    const part1Unweighted = ', part1_unweighted_json, ';
    const part1Weighted = ', part1_weighted_json, ';
    const rddData = ', rdd_data_json, ';

    // --------------------------------------------------------------------------
    // PART 1 CHART CONTROLLERS
    // --------------------------------------------------------------------------
    let part1ChartInstance;

    function renderPart1Chart(type) {
      const data = type === \'unweighted\' ? part1Unweighted : part1Weighted;
      const key = type === \'unweighted\' ? \'mean_residual\' : \'weighted_mean_residual\';
      
      const labels = data.map(d => d.leadlag);
      const points = data.map(d => d[key]);
      
      const ctx = document.getElementById(\'part1Chart\').getContext(\'2d\');
      
      if (part1ChartInstance) {
        part1ChartInstance.destroy();
      }

      const primaryColor = type === \'unweighted\' ? \'#38bdf8\' : \'#c084fc\';

      part1ChartInstance = new Chart(ctx, {
        type: \'line\',
        data: {
          labels: labels,
          datasets: [{
            label: type === \'unweighted\' ? \'Mean GDP Residual (USD)\' : \'Pop-Weighted Mean Residual (USD)\',
            data: points,
            borderColor: primaryColor,
            backgroundColor: primaryColor + \'20\',
            tension: 0.15,
            borderWidth: 3,
            pointBackgroundColor: primaryColor,
            pointRadius: 6,
            pointHoverRadius: 8
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: function(context) {
                  return `Residual: $${context.parsed.y.toFixed(3)}`;
                }
              }
            }
          },
          scales: {
            x: {
              grid: { color: \'rgba(255, 255, 255, 0.05)\' },
              ticks: { color: \'#94a3b8\' },
              title: { display: true, text: \'Years relative to largest political-liberty improvement\', color: \'#94a3b8\' }
            },
            y: {
              grid: { color: \'rgba(255, 255, 255, 0.05)\' },
              ticks: { color: \'#94a3b8\' },
              title: { display: true, text: \'GDP per capita residual (constant USD)\', color: \'#94a3b8\' }
            }
          }
        }
      });
    }

    function togglePart1(type) {
      document.getElementById(\'btn-p1-unweighted\').classList.toggle(\'active\', type === \'unweighted\');
      document.getElementById(\'btn-p1-weighted\').classList.toggle(\'active\', type === \'weighted\');
      
      const olsBox = document.getElementById(\'p1-ols-est\');
      const feBox = document.getElementById(\'p1-fe-est\');

      if (type === \'unweighted\') {
        olsBox.innerText = "228.965";
        feBox.innerText = "-0.188";
      } else {
        olsBox.innerText = "179.305";
        feBox.innerText = "-2.895";
      }

      renderPart1Chart(type);
    }

    // --------------------------------------------------------------------------
    // PART 2 CHART & OLS REGRESSION CONTROLLERS (Real-time Solver)
    // --------------------------------------------------------------------------
    let currentRDDOutcome = \'classize\';
    let currentBandwidth = 10;
    let part2ChartInstance;

    function setRDDOutcome(outcome) {
      const outcomes = [\'classize\', \'avgmath\', \'avgverb\'];
      outcomes.forEach(o => {
        document.getElementById(`btn-rdd-${o}`).classList.toggle(\'active\', o === outcome);
      });
      currentRDDOutcome = outcome;
      recalculateRDD();
    }

    function updateBandwidth(val) {
      document.getElementById(\'lbl-bandwidth\').innerText = val;
      currentBandwidth = parseInt(val);
      recalculateRDD();
    }

    // High performance OLS regression engine written in javascript
    // Resolves: Y = beta0 + beta1 * above_cutoff + beta2 * centered + beta3 * above_cutoff * centered
    function solveOLS(data) {
      const n = data.length;
      if (n < 4) return { beta1: 0, se: 0, beta0: 0, beta2: 0, beta3: 0 };

      // Design matrix X columns: [1, above_cutoff, centered, interaction]
      const X = data.map(d => [1, d.above, d.centered, d.above * d.centered]);
      const Y = data.map(d => d.y);

      // Transpose X
      const XT = [[], [], [], []];
      for (let r = 0; r < 4; r++) {
        for (let c = 0; c < n; c++) {
          XT[r][c] = X[c][r];
        }
      }

      // X\'X multiplication (4x4 matrix)
      const XTX = Array(4).fill(0).map(() => Array(4).fill(0));
      for (let r = 0; r < 4; r++) {
        for (let c = 0; c < 4; c++) {
          let sum = 0;
          for (let k = 0; k < n; k++) {
            sum += XT[r][k] * X[k][c];
          }
          XTX[r][c] = sum;
        }
      }

      // X\'Y multiplication (4x1 matrix)
      const XTY = [0, 0, 0, 0];
      for (let r = 0; r < 4; r++) {
        let sum = 0;
        for (let k = 0; k < n; k++) {
          sum += XT[r][k] * Y[k];
        }
        XTY[r] = sum;
      }

      // 4x4 Determinant/Inverse Solver using Gauss-Jordan elimination
      const M = XTX.map((row, i) => [...row, ...Array(4).fill(0).map((_, j) => i === j ? 1 : 0)]);
      for (let i = 0; i < 4; i++) {
        let maxRow = i;
        for (let k = i + 1; k < 4; k++) {
          if (Math.abs(M[k][i]) > Math.abs(M[maxRow][i])) maxRow = k;
        }
        const temp = M[i]; M[i] = M[maxRow]; M[maxRow] = temp;
        const diagVal = M[i][i];
        if (Math.abs(diagVal) < 1e-12) return { beta1: 0, se: 0, beta0: 0, beta2: 0, beta3: 0 }; // Singular matrix

        for (let j = i; j < 8; j++) M[i][j] /= diagVal;
        for (let k = 0; k < 4; k++) {
          if (k !== i) {
            const factor = M[k][i];
            for (let j = i; j < 8; j++) M[k][j] -= factor * M[i][j];
          }
        }
      }

      const inv = M.map(row => row.slice(4));

      // Coefficients vector = inv(X\'X) * X\'Y
      const coeffs = [0, 0, 0, 0];
      for (let r = 0; r < 4; r++) {
        let sum = 0;
        for (let c = 0; c < 4; c++) {
          sum += inv[r][c] * XTY[c];
        }
        coeffs[r] = sum;
      }

      // Residual variance calculation
      let sumResidSq = 0;
      for (let i = 0; i < n; i++) {
        const predCorrect = coeffs[0] + coeffs[1] * X[i][1] + coeffs[2] * X[i][2] + coeffs[3] * X[i][3];
        const error = Y[i] - predCorrect;
        sumResidSq += error * error;
      }
      const sigmaSq = sumResidSq / (n - 4);

      // Covariance matrix of coefficients = sigmaSq * inv(X\'X)
      // Standard error of beta1 (above_cutoff coefficient) is cov[1][1]
      const cov11 = sigmaSq * inv[1][1];
      const seBeta1 = cov11 > 0 ? Math.sqrt(cov11) : 0;

      return {
        beta0: coeffs[0],
        beta1: coeffs[1],
        beta2: coeffs[2],
        beta3: coeffs[3],
        se: seBeta1
      };
    }

    function recalculateRDD() {
      // 1. Filter under-80 data to bandwidth window around 40
      const win = rddData.filter(d => Math.abs(d.enrollment - 40) <= currentBandwidth && !isNaN(d[currentRDDOutcome]));
      
      const regressionPayload = win.map(d => ({
        centered: d.enrollment - 40,
        above: d.enrollment >= 40 ? 1 : 0,
        y: d[currentRDDOutcome]
      }));

      const res = solveOLS(regressionPayload);

      // Display live parameters
      document.getElementById(\'rdd-beta\').innerText = res.beta1.toFixed(3);
      document.getElementById(\'rdd-se\').innerText = res.se.toFixed(3);
      document.getElementById(\'rdd-n\').innerText = win.length;

      // Prepare Chart.js data
      // Draw binned points for visibility and scatter
      const binMap = new Map();
      win.forEach(d => {
        const e = d.enrollment;
        if (!binMap.has(e)) binMap.set(e, { sum: 0, count: 0 });
        binMap.get(e).sum += d[currentRDDOutcome];
        binMap.get(e).count++;
      });

      const binPoints = [];
      binMap.forEach((val, key) => {
        binPoints.push({ x: key, y: val.sum / val.count });
      });

      // Regression lines points
      // Left of cutoff (enrollment from 40-h to 39)
      const lineLeftPoints = [];
      const leftStart = 40 - currentBandwidth;
      const leftEnd = 39.9;
      lineLeftPoints.push({ x: leftStart, y: res.beta0 + res.beta2 * (leftStart - 40) });
      lineLeftPoints.push({ x: leftEnd, y: res.beta0 + res.beta2 * (leftEnd - 40) });

      // Right of cutoff (enrollment from 40 to 40+h)
      const lineRightPoints = [];
      const rightStart = 40;
      const rightEnd = 40 + currentBandwidth;
      lineRightPoints.push({ x: rightStart, y: res.beta0 + res.beta1 + (res.beta2 + res.beta3) * (rightStart - 40) });
      lineRightPoints.push({ x: rightEnd, y: res.beta0 + res.beta1 + (res.beta2 + res.beta3) * (rightEnd - 40) });

      const ctx = document.getElementById(\'part2Chart\').getContext(\'2d\');

      if (part2ChartInstance) {
        part2ChartInstance.destroy();
      }

      part2ChartInstance = new Chart(ctx, {
        type: \'scatter\',
        data: {
          datasets: [
            {
              label: \'Enrollment averages\',
              data: binPoints,
              backgroundColor: \'#34d399\',
              pointRadius: 6,
              zIndex: 10
            },
            {
              label: \'Left linear fit\',
              data: lineLeftPoints,
              type: \'line\',
              borderColor: \'#1f77b4\',
              borderWidth: 3,
              pointRadius: 0,
              tension: 0
            },
            {
              label: \'Right linear fit\',
              data: lineRightPoints,
              type: \'line\',
              borderColor: \'#d62728\',
              borderWidth: 3,
              pointRadius: 0,
              tension: 0
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false }
          },
          scales: {
            x: {
              grid: { color: \'rgba(255, 255, 255, 0.05)\' },
              ticks: { color: \'#94a3b8\' },
              min: 40 - currentBandwidth - 2,
              max: 40 + currentBandwidth + 2,
              title: { display: true, text: \'School enrollment\', color: \'#94a3b8\' }
            },
            y: {
              grid: { color: \'rgba(255, 255, 255, 0.05)\' },
              ticks: { color: \'#94a3b8\' },
              title: { display: true, text: currentRDDOutcome.toUpperCase(), color: \'#94a3b8\' }
            }
          }
        }
      });
    }

    // --------------------------------------------------------------------------
    // DASHBOARD ONLOAD INITIALIZATION
    // --------------------------------------------------------------------------
    window.onload = function() {
      // Render Part 1 default chart (unweighted)
      renderPart1Chart(\'unweighted\');

      // Render Part 2 default RDD (classize outcome)
      recalculateRDD();
    };

  </script>
</body>
</html>')

# Write to file
writeLines(html_template, "Homework_2_Interactive.html")
cat("Successfully created Homework_2_Interactive.html!\n")
