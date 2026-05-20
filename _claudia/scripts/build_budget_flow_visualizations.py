#!/usr/bin/env python3
import json
import math
import re
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "edgar"
NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def col_index(cell_ref):
    match = re.match(r"([A-Z]+)", cell_ref)
    value = 0
    for char in match.group(1):
        value = value * 26 + ord(char) - 64
    return value - 1


def as_money(value):
    if value in (None, ""):
        return 0
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).replace("$", "").replace(",", "").strip())
    except ValueError:
        return 0


class XlsxBook:
    def __init__(self, path):
        self.path = Path(path)
        self.zip = ZipFile(self.path)
        self.shared = self._shared_strings()
        self.sheet_targets = self._sheet_targets()
        self.sheets = {name: self._load_sheet(target) for name, target in self.sheet_targets.items()}

    def close(self):
        self.zip.close()

    def _shared_strings(self):
        if "xl/sharedStrings.xml" not in self.zip.namelist():
            return []
        root = ET.fromstring(self.zip.read("xl/sharedStrings.xml"))
        return ["".join(t.text or "" for t in si.findall(".//m:t", NS)) for si in root.findall("m:si", NS)]

    def _sheet_targets(self):
        workbook = ET.fromstring(self.zip.read("xl/workbook.xml"))
        rels = ET.fromstring(self.zip.read("xl/_rels/workbook.xml.rels"))
        relmap = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels.findall("rel:Relationship", NS)}
        targets = {}
        for sheet in workbook.findall(".//m:sheet", NS):
            rel_id = sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]
            target = relmap[rel_id].lstrip("/")
            if not target.startswith("xl/"):
                target = f"xl/{target}"
            targets[sheet.attrib["name"]] = target
        return targets

    def _cell_value(self, cell):
        cell_type = cell.attrib.get("t")
        value_node = cell.find("m:v", NS)
        formula_node = cell.find("m:f", NS)
        value = None if value_node is None else (value_node.text or "")
        if cell_type == "s" and value not in (None, ""):
            value = self.shared[int(value)]
        elif cell_type == "inlineStr":
            value = "".join(t.text or "" for t in cell.findall(".//m:t", NS))
        formula = None if formula_node is None else (formula_node.text or "")
        return value, formula

    def _load_sheet(self, target):
        root = ET.fromstring(self.zip.read(target))
        cells = {}
        formulas = {}
        for row in root.findall(".//m:sheetData/m:row", NS):
            for cell in row.findall("m:c", NS):
                value, formula = self._cell_value(cell)
                ref = cell.attrib["r"]
                cells[ref] = value
                if formula is not None:
                    formulas[ref] = formula
        return {"cells": cells, "formulas": formulas}

    def value(self, sheet, ref):
        return self.sheets[sheet]["cells"].get(ref)

    def formula(self, sheet, ref):
        return self.sheets[sheet]["formulas"].get(ref)

    def sheet_names(self):
        return list(self.sheet_targets)

    def formula_count(self):
        return sum(len(sheet["formulas"]) for sheet in self.sheets.values())


def item(section, group, name, amount):
    return {"section": section, "group": group, "item": name, "amount": round(float(amount), 2)}


def state(label, funding, items, note=None):
    revenue = sum(source["amount"] for source in funding)
    expenses = sum(row["amount"] for row in items)
    return {
        "label": label,
        "funding": funding,
        "items": items,
        "revenue": round(revenue, 2),
        "expenses": round(expenses, 2),
        "gap": round(revenue - expenses, 2),
        "note": note or "",
    }


def build_spring_data():
    book = XlsxBook(ROOT / "inbox/Spring Fling_Formal 2026.xlsx")
    try:
        master = "Master Budget"
        planned_decor = as_money(book.value(master, "D9"))
        current_decor = as_money(book.value("Decor", "G4"))
        base_items = [
            item("Venue and Operations", "Venue", "Scripps Forum space rental", as_money(book.value(master, "C3"))),
            item("Venue and Operations", "Operations", "Parking permits", as_money(book.value(master, "C6"))),
            item("Venue and Operations", "Operations", "Bottled water for end of night", as_money(book.value(master, "C7"))),
            item("Entertainment", "Music", "DJ - Danny Adams", as_money(book.value(master, "C8"))),
            item("Decor and Setup", "Decor", "Decorations - Amazon expected tracker", planned_decor),
            item("Venue and Operations", "Operations", "Wrist bands", as_money(book.value(master, "C11"))),
            item("Decor and Setup", "Rentals", "Tables, chairs, lights", as_money(book.value(master, "C12"))),
            item("Catering and Bar", "Food", "Saltaire UCSD Catering", as_money(book.value(master, "C13"))),
            item("Catering and Bar", "Beer and Wine", "Guiseppe beer and wine", as_money(book.value(master, "C14"))),
            item("Entertainment", "Photo Booth", "Jerry's Photo Booth", as_money(book.value(master, "C16"))),
        ]
        current_items = [dict(row) for row in base_items]
        for row in current_items:
            if row["item"] == "Decorations - Amazon expected tracker":
                row["item"] = "Decorations - Amazon actual tracker"
                row["amount"] = round(current_decor, 2)
        data = {
            "slug": "spring_fling_formal_2026",
            "kicker": "SPRING FORMAL / FLING MONEY MAP - Created for Edgar Agunias 5/19/2026",
            "title": "Follow the event budget as tickets offset costs.",
            "subhead": "A portable flow view of the Spring Fling/Formal 2026 workbook, comparing the allocation-only plan with the current snapshot after May 11 ticket sales and decor tracker updates.",
            "source": "inbox/Spring Fling_Formal 2026.xlsx",
            "sheetNames": book.sheet_names(),
            "formulaCount": book.formula_count(),
            "sections": ["All", "Catering and Bar", "Venue and Operations", "Decor and Setup", "Entertainment"],
            "states": {
                "base": state(
                    "Allocation Plan",
                    [{"name": "GO GPS event budget", "amount": as_money(book.value(master, "C21"))}],
                    base_items,
                    "Uses the Master Budget event allocation plus the expected decor tracker amount.",
                ),
                "current": state(
                    "Current Snapshot",
                    [
                        {"name": "GO GPS event budget", "amount": as_money(book.value(master, "C21"))},
                        {"name": "Ticket sales as of May 11", "amount": as_money(book.value(master, "I22"))},
                    ],
                    current_items,
                    "Uses May 11 ticket revenue and the Decor sheet actual-spent tracker.",
                ),
            },
            "sourceNotes": [
                f"Workbook sheets inspected: {', '.join(book.sheet_names())}.",
                "Formula and cached-value views were inspected from the XLSX XML package.",
                "The Master Budget cached total in C17 excludes the blank decor cost cell. This visualization includes the Decor sheet tracker because decor is a material event cost.",
                "Ticket-sales cells contain multiple scenarios. The current snapshot uses the row labeled Ticket Sales as of May 11, 2026.",
            ],
        }
        return data
    finally:
        book.close()


def build_go_gps_data():
    book = XlsxBook(ROOT / "inbox/GO GPS Finance 2025-26.xlsx")
    try:
        m = "Master Budget"
        predicted = {
            "Club allocation": as_money(book.value(m, "C4")),
            "Club Day": as_money(book.value(m, "C5")),
            "Mid Term Surprise": as_money(book.value(m, "C6")),
            "Halloween": as_money(book.value(m, "C7")),
            "Friendsgiving Potluck": as_money(book.value(m, "C8")),
            "Mentor Mentee Events": as_money(book.value(m, "C9")),
            "Valentine": as_money(book.value(m, "C10")),
            "Lunar Festival": as_money(book.value(m, "C11")),
            "Lasso Fest": as_money(book.value(m, "C12")),
            "Game Night": as_money(book.value(m, "C13")),
            "Karaoke": as_money(book.value(m, "C14")),
            "Lounge Supplies Fund": as_money(book.value(m, "C15")),
            "Spring Fling": as_money(book.value(m, "C16")),
            "Canva Subscription": as_money(book.value(m, "C17")),
            "Senior Gift": as_money(book.value(m, "C18")),
        }
        current = {
            "Club allocation": as_money(book.value(m, "C4")),
            "Club Day": as_money(book.value(m, "D5")),
            "Mid Term Surprise": as_money(book.value(m, "D6")),
            "Halloween": as_money(book.value(m, "D7")),
            "Friendsgiving Potluck": as_money(book.value(m, "D8")),
            "Mentor Mentee Events": as_money(book.value(m, "D9")),
            "Valentine": as_money(book.value(m, "D10")),
            "Lunar Festival": as_money(book.value(m, "D11")),
            "Lasso Fest": as_money(book.value(m, "C12")),
            "Game Night": as_money(book.value(m, "D13")),
            "Karaoke": as_money(book.value(m, "D14")),
            "Lounge Supplies Fund": as_money(book.value(m, "C15")),
            "Spring Fling": as_money(book.value(m, "D16")),
            "Canva Subscription": as_money(book.value(m, "D17")),
            "Senior Gift": as_money(book.value(m, "C18")),
        }
        groups = {
            "Club allocation": ("Clubs", "Club Allocations"),
            "Club Day": ("Student Life Events", "Fall Events"),
            "Mid Term Surprise": ("Student Life Events", "Fall Events"),
            "Halloween": ("Student Life Events", "Fall Events"),
            "Friendsgiving Potluck": ("Student Life Events", "Fall Events"),
            "Mentor Mentee Events": ("Student Life Events", "Community Events"),
            "Valentine": ("Student Life Events", "Winter Events"),
            "Lunar Festival": ("Student Life Events", "Winter Events"),
            "Lasso Fest": ("Student Life Events", "Spring Events"),
            "Game Night": ("Student Life Events", "Spring Events"),
            "Karaoke": ("Student Life Events", "Spring Events"),
            "Lounge Supplies Fund": ("Operations", "Lounge and Supplies"),
            "Spring Fling": ("Major Programs", "Spring Fling"),
            "Canva Subscription": ("Operations", "Subscriptions"),
            "Senior Gift": ("Major Programs", "Senior Gift"),
        }

        def rows(values):
            return [item(*groups[name], name, amount) for name, amount in values.items() if amount != 0]

        data = {
            "slug": "go_gps_finance_2025_26",
            "kicker": "GO GPS FINANCE MONEY MAP - Created for Edgar Agunias 5/19/2026",
            "title": "Track GO GPS funds from budget to current commitments.",
            "subhead": "A portable flow view of the 2025-26 GO GPS finance workbook, comparing the predicted budget against entered actuals and still-reserved commitments.",
            "source": "inbox/GO GPS Finance 2025-26.xlsx",
            "sheetNames": book.sheet_names(),
            "formulaCount": book.formula_count(),
            "sections": ["All", "Student Life Events", "Clubs", "Major Programs", "Operations"],
            "states": {
                "base": state(
                    "Predicted Budget",
                    [{"name": "Beginning GO GPS funds", "amount": as_money(book.value(m, "C3"))}],
                    rows(predicted),
                    "Uses predicted budget cells C4:C18.",
                ),
                "current": state(
                    "Current Commitments",
                    [{"name": "Beginning GO GPS funds", "amount": as_money(book.value(m, "D3"))}],
                    rows(current),
                    "Uses entered actuals where present, keeps the full club allocation, and keeps planned amounts for unresolved spring or future items.",
                ),
            },
            "sourceNotes": [
                f"Workbook sheets inspected: {', '.join(book.sheet_names())}.",
                "Formula and cached-value views were inspected from the XLSX XML package.",
                "The Master Budget D19 summary formula omits some entered actuals and uses the budgeted Spring Fling cell rather than the entered Spring Fling actual. This view uses concrete line rows instead of that summary formula.",
                f"Club sheet detail shows spent {as_money(book.value('Clubs', 'F16')):,.2f}, remaining {as_money(book.value('Clubs', 'G16')):,.2f}, allocated back {as_money(book.value('Clubs', 'H16')):,.2f}, and current available {as_money(book.value('Clubs', 'I16')):,.2f}.",
            ],
        }
        return data
    finally:
        book.close()


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
  <script src="https://cdn.jsdelivr.net/npm/d3-sankey@0.12.3/dist/d3-sankey.min.js"></script>
  <style>
    :root {{
      color-scheme: light;
      --ink: #24313f;
      --muted: #667381;
      --line: #d9e1e8;
      --paper: #fbf8f2;
      --panel: #ffffff;
      --gain: #288f67;
      --loss: #bf4c57;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font-family: Avenir Next, Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif;
    }}
    .shell {{ width: min(1480px, calc(100vw - 44px)); margin: 0 auto; padding: 28px 0 44px; }}
    header {{ padding: 10px 0 20px; }}
    .kicker {{ margin: 0 0 8px; font-size: .78rem; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; color: #596675; }}
    h1 {{ margin: 0; max-width: 960px; font-family: Georgia, Charter, serif; font-size: clamp(2.4rem, 5vw, 5.6rem); line-height: .94; letter-spacing: 0; }}
    .subhead {{ margin: 16px 0 0; max-width: 860px; color: var(--muted); font-size: 1.05rem; line-height: 1.48; }}
    .controls {{ display: grid; grid-template-columns: minmax(280px, 1fr) auto auto auto; gap: 12px; align-items: center; margin: 12px 0 18px; }}
    .chipbar, .segmented {{ display: flex; flex-wrap: wrap; gap: 8px; }}
    button {{
      appearance: none;
      border: 1px solid var(--line);
      background: rgba(255,255,255,.72);
      color: var(--ink);
      border-radius: 8px;
      min-height: 38px;
      padding: 8px 12px;
      font: inherit;
      font-weight: 750;
      cursor: pointer;
    }}
    button:hover {{ border-color: #9ab0c3; }}
    button.active {{ background: #24313f; color: white; border-color: #24313f; }}
    #compareBtn {{ min-width: 142px; }}
    .layout {{ display: grid; grid-template-columns: minmax(680px, 1fr) 390px; gap: 16px; align-items: stretch; }}
    .viz-card, .side-card, .table-card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: 0 16px 50px rgba(53,64,76,.08);
    }}
    .viz-card {{ min-height: 680px; position: relative; overflow: hidden; }}
    .viz-top {{ position: absolute; inset: 18px 18px auto 18px; z-index: 1; pointer-events: none; }}
    .stat-row {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; max-width: 640px; }}
    .stat {{ background: rgba(255,255,255,.86); border: 1px solid rgba(217,225,232,.86); border-radius: 8px; padding: 10px 12px; backdrop-filter: blur(6px); }}
    .stat span {{ display: block; color: var(--muted); font-size: .72rem; text-transform: uppercase; font-weight: 800; }}
    .stat strong {{ display: block; margin-top: 3px; font-size: 1.34rem; line-height: 1.1; white-space: nowrap; }}
    .gain {{ color: var(--gain); }}
    .loss {{ color: var(--loss); }}
    svg {{ display: block; width: 100%; height: 680px; }}
    .node rect {{ cursor: pointer; stroke: rgba(36,49,63,.28); stroke-width: 1; }}
    .node text {{ font-size: 12px; font-weight: 760; fill: #263340; paint-order: stroke; stroke: rgba(255,255,255,.8); stroke-width: 3px; }}
    .link {{ fill: none; stroke-opacity: .62; cursor: pointer; mix-blend-mode: multiply; }}
    .link:hover {{ stroke-opacity: .9; }}
    .dim {{ opacity: .16; }}
    .focus {{ opacity: 1; stroke-opacity: .92; }}
    .side-card {{ max-height: 680px; display: flex; flex-direction: column; overflow: hidden; }}
    .side-card h2, .table-card h2 {{ margin: 0; padding: 18px 18px 10px; font-size: 1.02rem; letter-spacing: 0; }}
    .delta-list {{ overflow-y: scroll; padding: 0 14px 16px; scrollbar-gutter: stable; }}
    .delta-card {{ border: 1px solid var(--line); border-radius: 8px; padding: 12px; margin: 0 0 10px; background: #fffdf9; }}
    .delta-top {{ display: flex; align-items: flex-start; justify-content: space-between; gap: 10px; }}
    .delta-name {{ font-weight: 820; line-height: 1.2; }}
    .badge {{ border-radius: 999px; padding: 3px 7px; font-size: .7rem; font-weight: 850; background: #edf7f1; color: var(--gain); white-space: nowrap; }}
    .delta-meta {{ margin-top: 5px; color: var(--muted); font-size: .82rem; }}
    .delta-money {{ margin-top: 8px; display: flex; justify-content: space-between; gap: 8px; font-weight: 760; }}
    .bar {{ position: relative; height: 10px; margin-top: 10px; background: #eef2f5; border-radius: 999px; overflow: hidden; }}
    .bar::after {{ content: ""; position: absolute; left: 50%; top: 0; bottom: 0; width: 1px; background: rgba(36,49,63,.34); }}
    .bar span {{ position: absolute; top: 0; bottom: 0; width: var(--w); background: var(--c); }}
    .bar .pos {{ left: 50%; }}
    .bar .neg {{ right: 50%; }}
    .table-card {{ margin-top: 16px; overflow: hidden; }}
    table {{ width: 100%; border-collapse: collapse; font-size: .91rem; }}
    th, td {{ padding: 10px 14px; border-top: 1px solid var(--line); text-align: left; vertical-align: top; }}
    th {{ color: var(--muted); font-size: .75rem; text-transform: uppercase; letter-spacing: .05em; }}
    td.num, th.num {{ text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }}
    .note {{ color: var(--muted); font-size: .88rem; line-height: 1.45; padding: 0 16px 16px; margin: 0; }}
    .tooltip {{ position: fixed; display: none; pointer-events: none; z-index: 10; max-width: 260px; padding: 10px 12px; border-radius: 8px; background: #24313f; color: #fff; box-shadow: 0 18px 46px rgba(36,49,63,.32); font-size: .9rem; line-height: 1.35; transform: translate(-50%, calc(-100% - 12px)); }}
    .tooltip b {{ display: block; margin-bottom: 4px; }}
    @media (max-width: 1120px) {{
      .controls, .layout {{ grid-template-columns: 1fr; }}
      .viz-card, .side-card {{ min-height: 620px; max-height: none; }}
      svg {{ height: 620px; }}
      .viz-top {{ position: static; padding: 14px; }}
    }}
  </style>
</head>
<body>
  <main class="shell">
    <header>
      <p class="kicker">{kicker}</p>
      <h1>{h1}</h1>
      <p class="subhead">{subhead}</p>
    </header>
    <section class="controls" aria-label="Budget controls">
      <div class="chipbar" id="filterButtons"></div>
      <div class="segmented">
        <button data-state="base" class="active"></button>
        <button data-state="current"></button>
      </div>
      <div class="segmented">
        <button data-depth="groups" class="active">Groups</button>
        <button data-depth="items">Line items</button>
      </div>
      <div class="segmented">
        <button id="compareBtn">Animate change</button>
      </div>
    </section>
    <section class="layout">
      <div class="viz-card">
        <div class="viz-top">
          <div class="stat-row">
            <div class="stat"><span>Funding</span><strong id="revenueStat"></strong></div>
            <div class="stat"><span>Expenses</span><strong id="expenseStat"></strong></div>
            <div class="stat"><span>Net</span><strong id="gapStat"></strong></div>
          </div>
        </div>
        <svg id="chart" role="img" aria-label="Budget flow chart"></svg>
      </div>
      <aside class="side-card">
        <h2>Reallocation Signals</h2>
        <div class="delta-list" id="deltaList"></div>
      </aside>
    </section>
    <section class="table-card">
      <h2>Scenario ledger</h2>
      <table class="money-table">
        <thead>
          <tr>
            <th>Line item</th>
            <th>Group</th>
            <th class="num" id="baseHead"></th>
            <th class="num" id="currentHead"></th>
            <th class="num">Change</th>
          </tr>
        </thead>
        <tbody id="ledgerBody"></tbody>
      </table>
      <p class="note" id="sourceNote"></p>
    </section>
  </main>
  <div class="tooltip" id="tooltip"></div>
  <script>
    const budget = {data_json};
    const palette = {{
      "Available Funding": "#9bd9e7",
      "GO GPS event budget": "#bfe8d6",
      "Ticket sales as of May 11": "#fbe69b",
      "Beginning GO GPS funds": "#bfe8d6",
      "Unfunded gap": "#f7a7a7",
      "Surplus / buffer": "#a8dfc8",
      "Catering and Bar": "#ffc2d6",
      "Venue and Operations": "#a9d6ff",
      "Decor and Setup": "#d7c8ff",
      "Entertainment": "#ffd3bf",
      "Student Life Events": "#ffd3bf",
      "Clubs": "#bfe8d6",
      "Major Programs": "#d7c8ff",
      "Operations": "#fbe69b",
      "default": "#cbd7e3"
    }};
    const state = {{ key: "base", depth: "groups", section: "All", compare: false, mix: 0 }};
    const fmt = d3.format("$,.0f");
    const fmtDelta = d => (d >= 0 ? "+" : "") + fmt(d);
    const chart = d3.select("#chart");
    const tooltip = d3.select("#tooltip");
    let focusedLinks = new Set();
    let focusedNodes = new Set();
    let animation = null;

    function cleanKey(text) {{
      return text.toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
    }}

    function stateData() {{
      if (!state.compare) return budget.states[state.key];
      return interpolateState(state.mix);
    }}

    function interpolateState(mix) {{
      const base = budget.states.base;
      const current = budget.states.current;
      const itemMap = new Map();
      for (const row of base.items) itemMap.set(cleanKey(row.item), {{...row, oldAmount: row.amount, newAmount: 0}});
      for (const row of current.items) {{
        const key = cleanKey(row.item);
        const prior = itemMap.get(key) || {{...row, oldAmount: 0, newAmount: 0}};
        prior.section = row.section;
        prior.group = row.group;
        prior.item = row.item;
        prior.newAmount = row.amount;
        itemMap.set(key, prior);
      }}
      const fundingMap = new Map();
      for (const row of base.funding) fundingMap.set(cleanKey(row.name), {{name: row.name, oldAmount: row.amount, newAmount: 0}});
      for (const row of current.funding) {{
        const key = cleanKey(row.name);
        const prior = fundingMap.get(key) || {{name: row.name, oldAmount: 0, newAmount: 0}};
        prior.name = row.name;
        prior.newAmount = row.amount;
        fundingMap.set(key, prior);
      }}
      const items = Array.from(itemMap.values()).map(row => ({{
        section: row.section,
        group: row.group,
        item: row.item,
        amount: row.oldAmount + (row.newAmount - row.oldAmount) * mix
      }}));
      const funding = Array.from(fundingMap.values()).map(row => ({{
        name: row.name,
        amount: row.oldAmount + (row.newAmount - row.oldAmount) * mix
      }}));
      const revenue = d3.sum(funding, d => d.amount);
      const expenses = d3.sum(items, d => d.amount);
      return {{ label: "Animated Change", funding, items, revenue, expenses, gap: revenue - expenses, note: "" }};
    }}

    function filteredItems(data) {{
      return data.items.filter(d => d.amount > 0 && (state.section === "All" || d.section === state.section));
    }}

    function aggregate(rows, keyFn, makeRow) {{
      const map = new Map();
      for (const row of rows) {{
        const key = keyFn(row);
        const existing = map.get(key) || makeRow(row);
        existing.amount += row.amount;
        map.set(key, existing);
      }}
      return Array.from(map.values());
    }}

    function graphData(data) {{
      const rows = filteredItems(data);
      const sections = aggregate(rows, d => d.section, d => ({{section: d.section, amount: 0}}));
      const groups = aggregate(rows, d => `${{d.section}}|${{d.group}}`, d => ({{section: d.section, group: d.group, amount: 0}}));
      const nodes = new Map();
      const links = [];
      const addNode = (id, label, kind, amount) => {{
        if (!nodes.has(id)) nodes.set(id, {{id, label, kind, amount: 0}});
        nodes.get(id).amount += amount || 0;
      }};
      const addLink = (source, target, value, colorKey, sourceLabel, targetLabel) => {{
        const real = Math.max(0, value);
        if (real <= 0) return;
        addNode(source, sourceLabel, "source", real);
        addNode(target, targetLabel, "target", real);
        links.push({{source, target, value: Math.max(real, 1), realValue: real, colorKey, id: `${{source}}=>${{target}}`}});
      }};
      const hubId = "hub:Available Funding";
      addNode(hubId, "Available Funding", "hub", data.revenue);
      for (const source of data.funding) addLink(`funding:${{source.name}}`, hubId, source.amount, source.name, source.name, "Available Funding");
      if (data.expenses > data.revenue) addLink("funding:Unfunded gap", hubId, data.expenses - data.revenue, "Unfunded gap", "Unfunded gap", "Available Funding");
      for (const section of sections) addLink(hubId, `section:${{section.section}}`, section.amount, section.section, "Available Funding", section.section);
      for (const group of groups) addLink(`section:${{group.section}}`, `group:${{group.section}}|${{group.group}}`, group.amount, group.section, group.section, group.group);
      if (state.depth === "items") {{
        const ranked = [...rows].sort((a, b) => b.amount - a.amount);
        for (const row of ranked) addLink(`group:${{row.section}}|${{row.group}}`, `item:${{row.section}}|${{row.group}}|${{row.item}}`, row.amount, row.section, row.group, row.item);
      }}
      if (data.revenue > data.expenses && state.section === "All") addLink(hubId, "sink:Surplus / buffer", data.revenue - data.expenses, "Surplus / buffer", "Available Funding", "Surplus / buffer");
      return {{nodes: Array.from(nodes.values()), links}};
    }}

    function makeButtons() {{
      d3.select("[data-state='base']").text(budget.states.base.label);
      d3.select("[data-state='current']").text(budget.states.current.label);
      d3.select("#baseHead").text(budget.states.base.label);
      d3.select("#currentHead").text(budget.states.current.label);
      d3.select("#filterButtons").selectAll("button")
        .data(budget.sections)
        .join("button")
        .classed("active", d => d === state.section)
        .text(d => d)
        .on("click", (_, d) => {{
          state.section = d;
          clearFocus();
          render();
          makeButtons();
        }});
      d3.selectAll("[data-state]").on("click", function() {{
        state.key = this.dataset.state;
        state.compare = false;
        state.mix = 0;
        d3.select("#compareBtn").classed("active", false).text("Animate change");
        d3.selectAll("[data-state]").classed("active", false);
        d3.select(this).classed("active", true);
        clearFocus();
        render();
      }});
      d3.selectAll("[data-depth]").on("click", function() {{
        state.depth = this.dataset.depth;
        d3.selectAll("[data-depth]").classed("active", false);
        d3.select(this).classed("active", true);
        clearFocus();
        render();
      }});
      d3.select("#compareBtn").on("click", animateChange);
    }}

    function animateChange() {{
      if (animation) cancelAnimationFrame(animation);
      state.compare = true;
      state.mix = 0;
      clearFocus();
      d3.select("#compareBtn").classed("active", true).text("Replaying...");
      const duration = 1250;
      const start = performance.now();
      function frame(now) {{
        const t = Math.min(1, (now - start) / duration);
        state.mix = 1 - Math.pow(1 - t, 3);
        render();
        if (t < 1) animation = requestAnimationFrame(frame);
        else {{
          d3.select("#compareBtn").text("Replay change");
          state.key = "current";
          d3.selectAll("[data-state]").classed("active", function() {{ return this.dataset.state === "current"; }});
        }}
      }}
      animation = requestAnimationFrame(frame);
    }}

    function render() {{
      const data = stateData();
      d3.select("#revenueStat").text(fmt(data.revenue));
      d3.select("#expenseStat").text(fmt(data.expenses));
      d3.select("#gapStat").text(fmt(data.gap)).attr("class", data.gap >= 0 ? "gain" : "loss");
      d3.select("#sourceNote").html(budget.sourceNotes.map(d => `- ${{d}}`).join("<br>"));
      renderChart(data);
      renderDeltas();
      renderLedger();
    }}

    function renderChart(data) {{
      const box = chart.node().getBoundingClientRect();
      const width = Math.max(720, box.width);
      const height = Math.max(620, box.height || 680);
      chart.attr("viewBox", [0, 0, width, height]);
      chart.selectAll("*").remove();
      const graph = graphData(data);
      const sankey = d3.sankey()
        .nodeId(d => d.id)
        .nodeWidth(18)
        .nodePadding(12)
        .nodeAlign(d3.sankeyJustify)
        .extent([[24, 112], [width - 24, height - 30]]);
      sankey(graph);
      const color = d => palette[d] || palette.default;
      chart.append("g")
        .attr("fill", "none")
        .selectAll("path")
        .data(graph.links)
        .join("path")
        .attr("class", d => linkClass(d))
        .attr("d", d3.sankeyLinkHorizontal())
        .attr("stroke", d => color(d.colorKey))
        .attr("stroke-width", d => Math.max(1, d.width))
        .on("mousemove", showLinkTip)
        .on("mouseleave", hideTip)
        .on("click", (event, d) => {{
          event.stopPropagation();
          focusFrom(d.source.id, d.target.id, graph.links);
        }});
      const node = chart.append("g")
        .selectAll("g")
        .data(graph.nodes)
        .join("g")
        .attr("class", d => nodeClass(d))
        .on("mousemove", showNodeTip)
        .on("mouseleave", hideTip)
        .on("click", (event, d) => {{
          event.stopPropagation();
          focusFrom(null, d.id, graph.links);
        }});
      node.append("rect")
        .attr("x", d => d.x0)
        .attr("y", d => d.y0)
        .attr("height", d => Math.max(1, d.y1 - d.y0))
        .attr("width", d => d.x1 - d.x0)
        .attr("rx", 4)
        .attr("fill", d => color(d.label));
      node.append("text")
        .attr("x", d => d.x0 < width / 2 ? d.x1 + 7 : d.x0 - 7)
        .attr("y", d => (d.y0 + d.y1) / 2)
        .attr("dy", "0.35em")
        .attr("text-anchor", d => d.x0 < width / 2 ? "start" : "end")
        .text(d => d.label.length > 34 ? d.label.slice(0, 31) + "..." : d.label);
      chart.on("click", clearFocus);
    }}

    function linkClass(d) {{
      const id = `${{d.source.id}}=>${{d.target.id}}`;
      if (!focusedLinks.size) return "link";
      return focusedLinks.has(id) ? "link focus" : "link dim";
    }}

    function nodeClass(d) {{
      if (!focusedNodes.size) return "node";
      return focusedNodes.has(d.id) ? "node focus" : "node dim";
    }}

    function focusFrom(sourceId, targetId, links) {{
      focusedLinks = new Set();
      focusedNodes = new Set([targetId]);
      if (sourceId) focusedNodes.add(sourceId);
      let frontier = new Set([targetId]);
      while (frontier.size) {{
        const next = new Set();
        for (const link of links) {{
          if (frontier.has(link.target.id)) {{
            focusedLinks.add(`${{link.source.id}}=>${{link.target.id}}`);
            focusedNodes.add(link.source.id);
            next.add(link.source.id);
          }}
        }}
        frontier = next;
      }}
      renderChart(stateData());
    }}

    function clearFocus() {{
      focusedLinks = new Set();
      focusedNodes = new Set();
      renderChart(stateData());
    }}

    function share(value) {{
      const data = stateData();
      return d3.format(".1%")(value / Math.max(1, data.expenses));
    }}

    function showLinkTip(event, d) {{
      tooltip.style("display", "block")
        .style("left", event.clientX + "px")
        .style("top", event.clientY + "px")
        .html(`<b>${{d.source.label}} to ${{d.target.label}}</b>${{fmt(d.realValue)}}<br>${{share(d.realValue)}} of expenses`);
    }}

    function showNodeTip(event, d) {{
      const total = Math.max(d.value || 0, d.amount || 0);
      tooltip.style("display", "block")
        .style("left", event.clientX + "px")
        .style("top", event.clientY + "px")
        .html(`<b>${{d.label}}</b>${{fmt(total)}}<br>${{share(total)}} of expenses`);
    }}

    function hideTip() {{
      tooltip.style("display", "none");
    }}

    function changeRows() {{
      const rows = new Map();
      for (const source of budget.states.base.funding) rows.set("funding|" + cleanKey(source.name), {{name: source.name, group: "Funding", oldValue: source.amount, newValue: 0}});
      for (const source of budget.states.current.funding) {{
        const key = "funding|" + cleanKey(source.name);
        const row = rows.get(key) || {{name: source.name, group: "Funding", oldValue: 0, newValue: 0}};
        row.newValue = source.amount;
        rows.set(key, row);
      }}
      for (const item of budget.states.base.items) rows.set("item|" + cleanKey(item.item), {{name: item.item, group: item.group, section: item.section, oldValue: item.amount, newValue: 0}});
      for (const item of budget.states.current.items) {{
        const key = "item|" + cleanKey(item.item);
        const row = rows.get(key) || {{name: item.item, group: item.group, section: item.section, oldValue: 0, newValue: 0}};
        row.name = item.item;
        row.group = item.group;
        row.section = item.section;
        row.newValue = item.amount;
        rows.set(key, row);
      }}
      return Array.from(rows.values())
        .filter(d => (state.section === "All" || d.section === state.section || d.group === "Funding") && Math.abs(d.newValue - d.oldValue) > 0.005)
        .map(d => ({{...d, delta: d.newValue - d.oldValue}}))
        .sort((a, b) => Math.abs(b.delta) - Math.abs(a.delta));
    }}

    function renderDeltas() {{
      const rows = changeRows();
      const max = Math.sqrt(d3.max(rows, d => Math.abs(d.delta)) || 1);
      d3.select("#deltaList").selectAll(".delta-card")
        .data(rows, d => d.name)
        .join("div")
        .attr("class", "delta-card")
        .html(d => {{
          const width = Math.max(3, Math.sqrt(Math.abs(d.delta)) / max * 48);
          const positive = d.delta >= 0;
          const badge = d.oldValue === 0 && d.newValue > 0 ? '<span class="badge">New</span>' : '';
          return `<div class="delta-top"><div class="delta-name">${{d.name}}</div>${{badge}}</div>
            <div class="delta-meta">${{d.group}}</div>
            <div class="delta-money"><span>${{fmt(d.oldValue)}} to ${{fmt(d.newValue)}}</span><span class="${{positive ? "gain" : "loss"}}">${{fmtDelta(d.delta)}}</span></div>
            <div class="bar">${{positive ? `<span class="pos" style="--w:${{width}}%;--c:#71c69c"></span>` : `<span class="neg" style="--w:${{width}}%;--c:#e48888"></span>`}}</div>`;
        }});
    }}

    function renderLedger() {{
      const rows = changeRows().slice(0, 100);
      d3.select("#ledgerBody").selectAll("tr")
        .data(rows, d => d.name)
        .join("tr")
        .html(d => `<td>${{d.name}}</td><td>${{d.group}}</td><td class="num">${{fmt(d.oldValue)}}</td><td class="num">${{fmt(d.newValue)}}</td><td class="num ${{d.delta >= 0 ? "gain" : "loss"}}">${{fmtDelta(d.delta)}}</td>`);
    }}

    makeButtons();
    render();
    window.addEventListener("resize", () => renderChart(stateData()));
  </script>
</body>
</html>
<!--
---
Generated for: Edgar Agunias
Date: 2026-05-19
Model: GPT-5 Codex
Sources: {source}
Agent: Hephaestus
---
-->
"""


def write_html(data):
    target = OUT / f"{data['slug']}_budget_flow.html"
    payload = json.dumps(data, ensure_ascii=False)
    html = HTML_TEMPLATE.format(
        title=data["title"],
        kicker=data["kicker"],
        h1=data["title"],
        subhead=data["subhead"],
        data_json=payload,
        source=f"{data['source']}; cached values and formula text inspected; edgar/gpsa_budget_flow.html benchmark",
    )
    target.write_text(html, encoding="utf-8")
    return target


def main():
    OUT.mkdir(exist_ok=True)
    outputs = [write_html(build_spring_data()), write_html(build_go_gps_data())]
    for output in outputs:
        print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
