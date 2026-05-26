from pathlib import Path


ROOT = Path(__file__).resolve().parent

TABLES = [
    ("table_q12.html", "Question 1-2: Selected Tract Comparison", "copy_table_q12.html"),
    ("table_q3.html", "Question 3: Poverty and Mobility by City", "copy_table_q3.html"),
    ("table_q4_ovb.html", "Question 4: Omitted-Variable-Bias Calculation", "copy_table_q4_ovb.html"),
    ("table_q5.html", "Question 5: New Orleans Poverty, Race, and Mobility", "copy_table_q5.html"),
    ("table_q79.html", "Questions 7-9: Pooled OLS vs. CZ Fixed Effects", "copy_table_q79.html"),
    (
        "table_open_urban_rural_regression.html",
        "Open Question: Urban/Rural Proxy Regression",
        "copy_table_open_urban_rural_regression.html",
    ),
    ("table_iv_manual_2sls.html", "Questions 10-11: Manual 2SLS", "copy_table_iv_manual_2sls.html"),
    ("table_code_understanding.html", "Code Understanding Sufficiency Test", "copy_table_code_understanding.html"),
]

DISCLOSURE = """---
Generated for: Edgar Agunias
Date: 2026-05-23
Model: GPT-5 Codex
Sources: Existing Homework 1 HTML tables, Homework_1.R, Homework_1_Answers_Compiled.md
Agent: Tyche with Hephaestus-style HTML implementation
---"""

CSS = """
body {
  font-family: "Times New Roman", Times, serif;
  font-size: 12pt;
  color: #111;
  background: #fff;
  margin: 24px;
}
h1 {
  font-size: 16pt;
  font-weight: 700;
  margin: 0 0 18px 0;
}
h2 {
  font-size: 13pt;
  font-weight: 700;
  margin: 22px 0 6px 0;
}
p.copy-note {
  font-size: 10.5pt;
  margin: 0 0 18px 0;
}
table {
  border-collapse: collapse;
  font-family: "Times New Roman", Times, serif;
  font-size: 11pt;
  margin: 8px 0 20px 0;
  width: auto;
}
caption {
  caption-side: top;
  font-weight: 700;
  padding-bottom: 6px;
}
td {
  padding: 3px 8px;
  vertical-align: middle;
  line-height: 1.2;
}
sup {
  font-size: 8pt;
}
.table-block {
  page-break-inside: avoid;
  margin-bottom: 24px;
}
.disclosure {
  font-family: "Times New Roman", Times, serif;
  font-size: 10pt;
  white-space: pre-wrap;
  margin-top: 28px;
  border-top: 1px solid #000;
  padding-top: 8px;
}
"""


def read_fragment(filename: str) -> str:
    path = ROOT / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing source table: {path}")
    fragment = path.read_text(encoding="utf-8").strip()
    return fragment


def document(title: str, body_html: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
{CSS.strip()}
</style>
</head>
<body>
{body_html}
<div class="disclosure">{DISCLOSURE}</div>
</body>
</html>
"""


def build_individual_pages() -> list[tuple[str, str, str]]:
    rendered = []
    for source, heading, output in TABLES:
        fragment = read_fragment(source)
        body = f"""<h1>GPEC 446 Homework 1 Table</h1>
<p class="copy-note">Select the table itself in the browser and paste into Word.</p>
<div class="table-block">
<h2>{heading}</h2>
{fragment}
</div>"""
        (ROOT / output).write_text(document(heading, body), encoding="utf-8")
        rendered.append((source, heading, output))
    return rendered


def build_combined_page(rendered: list[tuple[str, str, str]]) -> None:
    blocks = [
        "<h1>GPEC 446 Homework 1 Copy-Paste Tables</h1>",
        '<p class="copy-note">These tables reuse the existing computed Homework 1 values and are formatted for copying into Word. No statistical results are recomputed here.</p>',
    ]
    for source, heading, _output in rendered:
        blocks.append(f"""<div class="table-block">
<h2>{heading}</h2>
{read_fragment(source)}
</div>""")
    (ROOT / "Homework_1_Tables_Copy_Paste.html").write_text(
        document("GPEC 446 Homework 1 Copy-Paste Tables", "\n".join(blocks)),
        encoding="utf-8",
    )


def main() -> None:
    rendered = build_individual_pages()
    build_combined_page(rendered)
    print("Generated copy-paste HTML tables:")
    for _source, _heading, output in rendered:
        print(f"- {output}")
    print("- Homework_1_Tables_Copy_Paste.html")


if __name__ == "__main__":
    main()
