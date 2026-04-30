from pathlib import Path
import html
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Flowable,
    HRFlowable,
    Image,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.utils import ImageReader


BASE = Path(__file__).resolve().parent
SOURCE = BASE / "QM3_Midterm_Lecture_Reference_v1.4.0_notes.md"
OUT = BASE / "QM3_Midterm_Lecture_Reference_v1.4.0.pdf"
TITLE = "QM3 Midterm Lecture Reference"
SUBTITLE = "Lecture-slide based reference sheet, v1.4.0"

DARK = colors.HexColor("#1B2A4A")
BLUE = colors.HexColor("#2C5282")
LIGHT = colors.HexColor("#F3F6FA")
AMBER = colors.HexColor("#FFF5E6")
GREY = colors.HexColor("#555555")
LINE = colors.HexColor("#D8E0EA")


class BookmarkAnchor(Flowable):
    def __init__(self, name, title):
        super().__init__()
        self.width = 0
        self.height = 0
        self.name = name
        self.title = title

    def draw(self):
        self.canv.bookmarkPage(self.name, fit="XYZ", left=0, top=self.canv._pagesize[1])
        self.canv.addOutlineEntry(self.title, self.name, level=0)


class ConceptDiagram(Flowable):
    def __init__(self, kind, width=6.5 * inch, height=2.05 * inch):
        super().__init__()
        self.kind = kind
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        c.saveState()
        c.setStrokeColor(LINE)
        c.setFillColor(colors.HexColor("#FCFDFE"))
        c.roundRect(0, 0, self.width, self.height, 5, fill=1, stroke=1)
        getattr(self, f"draw_{self.kind}", self.draw_placeholder)(c)
        c.restoreState()

    def _label(self, c, x, y, text, size=10, bold=False, color=DARK, align="center"):
        size = max(size, 12)
        c.setFillColor(color)
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        if align == "center":
            c.drawCentredString(x, y, text)
        else:
            c.drawString(x, y, text)

    def _box(self, c, x, y, w, h, text, fill=LIGHT):
        c.setFillColor(fill)
        c.setStrokeColor(BLUE)
        c.roundRect(x, y, w, h, 4, fill=1, stroke=1)
        self._label(c, x + w / 2, y + h / 2 - 4, text, size=10, bold=True)

    def _arrow(self, c, x1, y1, x2, y2, color=BLUE):
        c.setStrokeColor(color)
        c.setLineWidth(1.2)
        c.line(x1, y1, x2, y2)
        dx = 6 if x2 >= x1 else -6
        c.line(x2, y2, x2 - dx, y2 + 4)
        c.line(x2, y2, x2 - dx, y2 - 4)

    def draw_placeholder(self, c):
        self._label(c, self.width / 2, self.height / 2, self.kind, bold=True)

    def draw_potential_outcomes(self, c):
        self._label(c, self.width / 2, self.height - 18, "Potential outcomes: one unit, two possible worlds, one observed", 11, True)
        self._box(c, 36, 58, 120, 38, "Y(1): treated", colors.HexColor("#E8F3FF"))
        self._label(c, 96, 43, "observed if D=1", 10)
        self._box(c, self.width - 156, 58, 120, 38, "Y(0): untreated", colors.HexColor("#FFF4E0"))
        self._label(c, self.width - 96, 43, "missing if D=1", 10)
        self._arrow(c, 164, 76, self.width - 164, 76)
        self._label(c, self.width / 2, 87, "causal effect = Y(1) - Y(0)", 10, True)
        self._label(c, self.width / 2, 22, "Can a comparison group stand in for the missing counterfactual?", 12)

    def draw_ols(self, c):
        self._label(c, self.width / 2, self.height - 18, "OLS: fit the line that makes squared residuals as small as possible", 11, True)
        ox, oy = 54, 28
        c.setStrokeColor(GREY)
        c.line(ox, oy, ox, self.height - 38)
        c.line(ox, oy, self.width - 38, oy)
        c.setStrokeColor(BLUE)
        c.setLineWidth(1.4)
        c.line(ox + 12, oy + 15, self.width - 70, self.height - 50)
        pts = [(95, 68), (150, 54), (214, 95), (285, 82), (355, 118)]
        for x, y in pts:
            yhat = oy + 15 + (x - ox - 12) * 0.23
            c.setStrokeColor(colors.HexColor("#C43B3B"))
            c.line(x, min(y, yhat), x, max(y, yhat))
            c.setFillColor(DARK)
            c.circle(x, y, 3, fill=1, stroke=0)
        self._label(c, self.width - 150, 45, "coefficient = slope", 12, True, BLUE)
        self._label(c, self.width - 150, 28, "residual = observed - fitted", 12)

    def draw_ovb(self, c):
        self._label(c, self.width / 2, self.height - 18, "OVB: bias needs two links", 11, True)
        self._box(c, 38, 35, 105, 42, "Treatment X")
        self._box(c, self.width / 2 - 52, 82, 104, 34, "Omitted W", colors.HexColor("#FFF4E0"))
        self._box(c, self.width - 143, 35, 105, 42, "Outcome Y")
        self._arrow(c, self.width / 2 - 62, 93, 150, 66, colors.HexColor("#C47A00"))
        self._arrow(c, self.width / 2 + 62, 93, self.width - 150, 66, colors.HexColor("#C47A00"))
        self._arrow(c, 150, 56, self.width - 150, 56)
        self._label(c, self.width / 2, 17, "Bias sign = sign(W with X) x sign(W with Y)", 10, True)

    def draw_bad_controls(self, c):
        self._label(c, self.width / 2, self.height - 18, "Bad control: do not hold fixed something treatment caused", 11, True)
        self._box(c, 42, 49, 100, 36, "Treatment")
        self._box(c, self.width / 2 - 52, 49, 104, 36, "Mediator", colors.HexColor("#FFF4E0"))
        self._box(c, self.width - 142, 49, 100, 36, "Outcome")
        self._arrow(c, 145, 67, self.width / 2 - 56, 67)
        self._arrow(c, self.width / 2 + 56, 67, self.width - 145, 67)
        self._arrow(c, 145, 43, self.width - 145, 43, colors.HexColor("#7A8A99"))
        self._label(c, self.width / 2, 20, "Controlling for the mediator blocks part of the total effect.", 10, True)

    def draw_iv_pipeline(self, c):
        self._label(c, self.width / 2, self.height - 18, "IV logic: first stage plus reduced form equals Wald/LATE", 11, True)
        xs = [36, 180, 324]
        labels = ["Instrument Z", "Treatment D", "Outcome Y"]
        fills = [colors.HexColor("#E8F3FF"), LIGHT, LIGHT]
        for x, label, fill in zip(xs, labels, fills):
            self._box(c, x, 54, 108, 36, label, fill)
        self._arrow(c, xs[0] + 112, 72, xs[1] - 4, 72)
        self._arrow(c, xs[1] + 112, 72, xs[2] - 4, 72)
        self._label(c, 162, 38, "first stage", 12, True, BLUE)
        self._label(c, 306, 38, "reduced form", 12, True, BLUE)
        self._box(c, self.width / 2 - 88, 8, 176, 24, "Wald/LATE = RF / FS", colors.HexColor("#E8F8EF"))

    def draw_compliance(self, c):
        self._label(c, self.width / 2, self.height - 18, "Compliance types under assignment Z", 11, True)
        data = [
            ("Always-taker", "D(1)=1, D(0)=1", "not moved by Z"),
            ("Complier", "D(1)=1, D(0)=0", "moved by Z; LATE group"),
            ("Never-taker", "D(1)=0, D(0)=0", "not moved by Z"),
            ("Defier", "D(1)=0, D(0)=1", "ruled out by monotonicity"),
        ]
        x0, y0 = 32, 6
        row_h, col1, col2 = 22, 110, 118
        for idx, row in enumerate(data):
            y = y0 + (3 - idx) * row_h
            fill = colors.HexColor("#E8F8EF") if row[0] == "Complier" else colors.white
            c.setFillColor(fill)
            c.setStrokeColor(LINE)
            c.rect(x0, y, self.width - 64, row_h, fill=1, stroke=1)
            self._label(c, x0 + 8, y + 7, row[0], 9, True, align="left")
            self._label(c, x0 + col1, y + 7, row[1], 9, align="left")
            self._label(c, x0 + col1 + col2, y + 7, row[2], 9, align="left")

    def draw_assumptions(self, c):
        self._label(c, self.width / 2, self.height - 18, "Assumption checklist: method, comparison, failure", 11, True)
        headers = ["Method", "Causal assumption", "Failure cue"]
        rows = [
            ("Randomization", "D is as-if random", "selection"),
            ("OLS/CIA", "no omitted confounding", "unobserved sorting"),
            ("IV/LATE", "relevance + exclusion", "weak or invalid Z"),
        ]
        x0, y0 = 28, 8
        widths = [112, 190, 130]
        h = 22
        for j, head in enumerate(headers):
            x = x0 + sum(widths[:j])
            c.setFillColor(DARK)
            c.rect(x, y0 + 3 * h, widths[j], h, fill=1, stroke=0)
            self._label(c, x + 6, y0 + 3 * h + 7, head, 8.5, True, colors.white, align="left")
        for i, row in enumerate(rows):
            y = y0 + (2 - i) * h
            for j, cell in enumerate(row):
                x = x0 + sum(widths[:j])
                c.setFillColor(colors.white if i % 2 else LIGHT)
                c.setStrokeColor(LINE)
                c.rect(x, y, widths[j], h, fill=1, stroke=1)
                self._label(c, x + 6, y + 7, cell, 8.5, j == 0, align="left")


def xml_text(text):
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`([^`]+)`", '<font face="Courier">\\1</font>', text)
    return text


def para(text, style):
    return Paragraph(xml_text(text), style)


def slug(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:48] or "section"


def wrap_code_line(line, width=66):
    if len(line) <= width:
        return [line]
    indent = re.match(r"\s*", line).group(0)
    continuation = indent + "    "
    break_chars = " +-*/=,|)]}"
    pieces = []
    remaining = line
    while len(remaining) > width:
        cut = max(remaining.rfind(ch, 0, width + 1) for ch in break_chars)
        if cut <= len(indent):
            cut = width
        pieces.append(remaining[: cut + 1].rstrip())
        remaining = continuation + remaining[cut + 1 :].lstrip()
    pieces.append(remaining)
    return pieces


def code_block(lines, styles):
    wrapped = []
    for line in lines:
        wrapped.extend(wrap_code_line(line))
    return Preformatted("\n".join(wrapped), styles["LectureCode"])


def image_flowable(raw_path, styles):
    image_path = Path(raw_path)
    if not image_path.is_absolute():
        image_path = BASE / image_path
    if not image_path.exists():
        return para(f"[Missing image: {raw_path}]", styles["Body"])

    img = ImageReader(str(image_path))
    width_px, height_px = img.getSize()
    max_width = 6.5 * inch
    max_height = 4.0 * inch
    draw_width = max_width
    draw_height = draw_width * (height_px / width_px)
    if draw_height > max_height:
        draw_height = max_height
        draw_width = draw_height * (width_px / height_px)
    return Image(str(image_path), width=draw_width, height=draw_height)


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            "CoverTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            textColor=DARK,
            alignment=TA_LEFT,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            "CoverSub",
            parent=styles["Normal"],
            fontSize=12,
            leading=15,
            textColor=GREY,
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            "H1",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=17,
            leading=21,
            textColor=DARK,
            spaceBefore=10,
            spaceAfter=5,
        )
    )
    styles.add(
        ParagraphStyle(
            "H2",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=17,
            textColor=BLUE,
            spaceBefore=8,
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            "Body",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=12,
            leading=15.5,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            "LectureBullet",
            parent=styles["Body"],
            leftIndent=8,
            firstLineIndent=0,
            spaceAfter=2,
        )
    )
    styles.add(
        ParagraphStyle(
            "Small",
            parent=styles["Body"],
            fontSize=12,
            leading=15,
            textColor=GREY,
        )
    )
    styles.add(
        ParagraphStyle(
            "LectureCode",
            parent=styles["Code"],
            fontName="Courier",
            fontSize=10.5,
            leading=12.8,
            backColor=colors.HexColor("#F7F8FA"),
            borderColor=LINE,
            borderWidth=0.5,
            borderPadding=5,
            spaceBefore=3,
            spaceAfter=5,
        )
    )
    return styles


def parse_table(lines, start):
    rows = []
    i = start
    while i < len(lines) and lines[i].strip().startswith("|"):
        cells = [cell.strip() for cell in lines[i].strip().strip("|").split("|")]
        if not all(re.fullmatch(r":?-{3,}:?", c or "") for c in cells):
            rows.append(cells)
        i += 1
    return rows, i


def table_flowable(rows, styles):
    data = [[Paragraph(xml_text(cell), styles["Small"]) for cell in row] for row in rows]
    widths = [1.1 * inch, 1.5 * inch, 3.9 * inch] if len(rows[0]) == 3 else None
    table = Table(data, colWidths=widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), DARK),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.25, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 1), (-1, -1), LIGHT),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def markdown_to_story(markdown, styles):
    lines = markdown.splitlines()
    story = []
    i = 0
    in_code = False
    code_lines = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_code:
                story.append(code_block(code_lines, styles))
                code_lines = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        if not stripped:
            story.append(Spacer(1, 4))
            i += 1
            continue

        if stripped == "---":
            story.append(HRFlowable(width="100%", thickness=0.6, color=LINE, spaceBefore=6, spaceAfter=6))
            i += 1
            continue

        visual = re.fullmatch(r"\[\[VISUAL:([a-z_]+)\]\]", stripped)
        if visual:
            story.append(ConceptDiagram(visual.group(1)))
            story.append(Spacer(1, 8))
            i += 1
            continue

        image = re.fullmatch(r"\[\[IMAGE:(.+?)\]\]", stripped)
        if image:
            story.append(image_flowable(image.group(1), styles))
            story.append(Spacer(1, 8))
            i += 1
            continue

        if stripped.startswith("|"):
            rows, i = parse_table(lines, i)
            if rows:
                story.append(table_flowable(rows, styles))
                story.append(Spacer(1, 5))
            continue

        if stripped.startswith("# "):
            title = stripped[2:].strip()
            story.append(BookmarkAnchor(slug(title), title))
            story.append(Paragraph(xml_text(title), styles["H1"]))
            i += 1
            continue

        if stripped.startswith("## "):
            title = stripped[3:].strip()
            story.append(BookmarkAnchor(slug(title), title))
            story.append(PageBreak() if re.match(r"\d+\. ", title) else Spacer(1, 2))
            story.append(Paragraph(xml_text(title), styles["H2"]))
            i += 1
            continue

        if stripped.startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(ListItem(Paragraph(xml_text(lines[i].strip()[2:]), styles["LectureBullet"]), leftIndent=8))
                i += 1
            story.append(ListFlowable(items, bulletType="bullet", start="circle", leftIndent=12, bulletFontSize=5))
            story.append(Spacer(1, 3))
            continue

        if re.match(r"\d+\. ", stripped):
            items = []
            while i < len(lines) and re.match(r"\d+\. ", lines[i].strip()):
                item = re.sub(r"^\d+\. ", "", lines[i].strip())
                items.append(ListItem(Paragraph(xml_text(item), styles["LectureBullet"]), leftIndent=10))
                i += 1
            story.append(ListFlowable(items, bulletType="1", leftIndent=16))
            story.append(Spacer(1, 3))
            continue

        if stripped.startswith("**") and stripped.endswith("**") and ":" in stripped:
            story.append(
                Table(
                    [[Paragraph(xml_text(stripped), styles["Body"])]],
                    colWidths=[6.5 * inch],
                    style=[
                        ("BACKGROUND", (0, 0), (-1, -1), AMBER),
                        ("BOX", (0, 0), (-1, -1), 0.25, colors.HexColor("#E7C27B")),
                        ("LEFTPADDING", (0, 0), (-1, -1), 5),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                        ("TOPPADDING", (0, 0), (-1, -1), 4),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ],
                )
            )
        else:
            story.append(para(stripped, styles["Body"]))
        i += 1

    return story


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 12)
    canvas.setFillColor(GREY)
    canvas.drawString(0.55 * inch, 0.35 * inch, TITLE)
    canvas.drawRightString(7.95 * inch, 0.35 * inch, f"Page {doc.page}")
    canvas.restoreState()


def main():
    styles = build_styles()
    markdown = SOURCE.read_text(encoding="utf-8")
    story = [
        Paragraph(TITLE, styles["CoverTitle"]),
        Paragraph(SUBTITLE, styles["CoverSub"]),
        para(
            "Built from Quantitative Methods 3 (QM3) lecture slides Lecture 1 through Lecture 6 (L1-L6). The document is deliberately exam-facing: concept, lecture source, practical use, traps, cues, and formulas.",
            styles["Body"],
        ),
        HRFlowable(width="100%", thickness=0.8, color=LINE, spaceBefore=8, spaceAfter=8),
    ]
    story.extend(markdown_to_story(markdown, styles))

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        rightMargin=1.0 * inch,
        leftMargin=1.0 * inch,
        topMargin=1.0 * inch,
        bottomMargin=1.0 * inch,
        title=TITLE,
        author="Tyche",
        subject="QM3 midterm lecture reference",
    )
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(OUT)


if __name__ == "__main__":
    main()
