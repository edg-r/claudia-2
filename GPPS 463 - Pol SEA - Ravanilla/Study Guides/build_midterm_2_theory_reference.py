from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Flowable,
    HRFlowable,
    Image as RLImage,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.pdfbase.pdfmetrics import stringWidth


BASE_DIR = Path(__file__).resolve().parent
NOTES_PATH = BASE_DIR / "GPPS_463_Midterm_2_Theory_Reference_v1.0.0_notes.md"
PDF_PATH = BASE_DIR / "GPPS_463_Midterm_2_Theory_Reference_v1.0.0.pdf"
IMAGE_DIR = BASE_DIR / "assets" / "midterm2_theory_images"

DOC_TITLE = "GPPS 463 Midterm 2 Theory Reference"
DOC_SUBTITLE = "Politics of Southeast Asia | Nico Ravanilla | Spring 2026"

DARK = colors.HexColor("#17324D")
BLUE = colors.HexColor("#256D85")
GREEN = colors.HexColor("#2F6F5E")
GOLD = colors.HexColor("#B8872D")
TEXT = colors.HexColor("#202A34")
MUTED = colors.HexColor("#5F6B76")
LIGHT_BLUE = colors.HexColor("#EAF4F7")
LIGHT_GREEN = colors.HexColor("#EDF7F2")
LIGHT_GOLD = colors.HexColor("#FFF7E8")
LIGHT_GREY = colors.HexColor("#F5F6F8")
LINE = colors.HexColor("#C9D1D8")


VISUAL_PAGES = {
    1: {
        "image": "krugman_growth_accounting_inputs_tfp.png",
        "caption": (
            "<b>Visual caption.</b> Mechanism: output growth is split between input mobilization "
            "and total factor productivity. Key assumption: measured inputs can be separated "
            "from efficiency gains. Strength/limit cue: the framework punctures miracle talk, "
            "but it explains accounting sources better than political institutions."
        ),
    },
    2: {
        "image": "thailand_entrepreneur_led_growth_networks.png",
        "caption": (
            "<b>Visual caption.</b> Mechanism: Thai growth flows through open trade, macro stability, "
            "and Chinese-Thai business networks rather than a classic developmental state. "
            "Key assumption: private entrepreneurs can coordinate investment when the state keeps "
            "conditions stable. Strength/limit cue: the model explains market-led growth, but also "
            "points to inequality and financial fragility."
        ),
    },
    3: {
        "image": "singapore_state_created_comparative_advantage.png",
        "caption": (
            "<b>Visual caption.</b> Mechanism: the PAP state uses wages, forced savings, infrastructure, "
            "and MNE attraction to create comparative advantage. Key assumption: a capable state can "
            "shape markets without destroying export signals. Strength/limit cue: the case shows "
            "industrial-policy power, but city-state scale and political control limit portability."
        ),
    },
    4: {
        "image": "wade_afc_global_finance_wheels.png",
        "caption": (
            "<b>Visual caption.</b> Mechanism: domestic vulnerabilities sit inside larger wheels of "
            "global liquidity, capital inflows, and sudden reversal. Key assumption: international "
            "financial architecture shapes crisis risk, not only local governance. Strength/limit cue: "
            "the view corrects domestic blame, but is less precise about country-level variation."
        ),
    },
    5: {
        "image": "macintyre_veto_players_policy_risk.png",
        "caption": (
            "<b>Visual caption.</b> Mechanism: veto-player concentration creates policy risk at both "
            "extremes, through volatility with too few vetoes and rigidity with too many. Key assumption: "
            "investors value both credible commitment and decisive adjustment. Strength/limit cue: "
            "the U-shape clarifies crisis response, but informal veto actors can complicate the count."
        ),
    },
    6: {
        "image": "hicken2008_crisis_severity_reform_momentum.png",
        "caption": (
            "<b>Visual caption.</b> Mechanism: severe crisis can discredit existing institutions and "
            "create reform momentum, while mild shock can preserve weak arrangements. Key assumption: "
            "political urgency is needed to overcome blockers. Strength/limit cue: the Thailand-Philippines "
            "contrast is powerful, but severe crisis can also produce instability or backlash."
        ),
    },
    7: {
        "image": "hicken2006_party_fabrication_thai_rak_thai.png",
        "caption": (
            "<b>Visual caption.</b> Mechanism: the 1997 constitution changes electoral incentives, "
            "reduces fragmentation, and enables Thai Rak Thai to centralize party government. "
            "Key assumption: politicians adapt to new rules and party leaders can enforce discipline. "
            "Strength/limit cue: stronger parties improve decisiveness, but can weaken checks."
        ),
    },
    8: {
        "image": "malesky_abrami_zheng_single_party_inequality.png",
        "caption": (
            "<b>Visual caption.</b> Mechanism: broader internal party coalitions push Vietnam toward "
            "equalizing transfers and public services relative to China's narrower top bodies. "
            "Key assumption: authoritarian leaders still answer to internal winning coalitions. "
            "Strength/limit cue: the framework explains inequality inside single-party rule, but "
            "does not make the regime democratic."
        ),
    },
    9: {
        "image": "vietnam_doing_well_under_communism_public_services.png",
        "caption": (
            "<b>Visual caption.</b> Mechanism: Vietnam's broader party architecture channels provincial "
            "and mass-organization interests into redistribution, education, and basic services. "
            "Key assumption: fiscal choices mediate growth and inequality. Strength/limit cue: the "
            "framework clarifies relative performance, but 'doing well' depends on the value being measured."
        ),
    },
    10: {
        "image": "midterm2_master_synthesis_institutions_filter_pressure.png",
        "caption": (
            "<b>Visual caption.</b> Mechanism: global pressure, domestic institutions, coalitions, and "
            "state capacity filter common regional shocks into different outcomes. Key assumption: "
            "cases should test mechanisms rather than merely illustrate them. Strength/limit cue: "
            "the synthesis links the course arc, but each component theory has a narrower proper use."
        ),
    },
}


class BookmarkAnchor(Flowable):
    def __init__(self, name, title="", level=0):
        super().__init__()
        self.width = 0
        self.height = 0
        self._name = name
        self._title = title
        self._level = level

    def draw(self):
        self.canv.bookmarkPage(self._name, fit="XYZ", left=0, top=self.canv._pagesize[1])
        if self._title:
            self.canv.addOutlineEntry(self._title, self._name, level=self._level, closed=False)


def slugify(text):
    text = text.lower().replace("&", "and")
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return text or "section"


def xml_escape(text):
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def inline_md(text):
    text = xml_escape(text)
    text = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    return text


def first_page_footer(canvas, doc):
    footer(canvas, doc)


def later_page_footer(canvas, doc):
    footer(canvas, doc)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.35)
    canvas.line(doc.leftMargin, 0.5 * inch, letter[0] - doc.rightMargin, 0.5 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(doc.leftMargin, 0.35 * inch, "GPPS 463 Midterm 2 Theory Reference")
    page = f"Page {doc.page}"
    canvas.drawRightString(letter[0] - doc.rightMargin, 0.35 * inch, page)
    canvas.restoreState()


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=28,
            alignment=TA_CENTER,
            textColor=DARK,
            spaceAfter=7,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverSub",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            alignment=TA_CENTER,
            textColor=TEXT,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=11.4,
            leading=14.2,
            textColor=TEXT,
            spaceAfter=5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Small",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8.2,
            leading=10.1,
            textColor=TEXT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TOC",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9.2,
            leading=11.4,
            leftIndent=4,
            spaceAfter=2,
            textColor=TEXT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H1",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=15.5,
            leading=18.5,
            textColor=colors.white,
            spaceAfter=0,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H2",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=DARK,
            spaceBefore=6,
            spaceAfter=4,
            keepWithNext=True,
        )
    )
    styles.add(
        ParagraphStyle(
            name="StudyBullet",
            parent=styles["Body"],
            leftIndent=16,
            firstLineIndent=-8,
            bulletIndent=3,
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Disclosure",
            parent=styles["Small"],
            fontSize=8.4,
            leading=10.4,
            textColor=MUTED,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Ref",
            parent=styles["Body"],
            fontSize=10.7,
            leading=13.2,
            leftIndent=18,
            firstLineIndent=-18,
            spaceAfter=4,
        )
    )
    return styles


def read_lines():
    return NOTES_PATH.read_text(encoding="utf-8").splitlines()


def collect_toc(lines):
    entries = []
    for line in lines:
        if line.startswith("## "):
            title = line[3:].strip()
            if title == "References":
                entries.append(("references", "References"))
            elif re.match(r"^\d+\.", title):
                entries.append((slugify(title), title))
    entries.append(("output_disclosure", "Output Disclosure"))
    return entries


def cover_story(lines, styles):
    toc = collect_toc(lines)
    meta = [line for line in lines[:8] if line.startswith("**")]
    orientation = []
    in_orientation = False
    for line in lines:
        if line == "## Exam Orientation":
            in_orientation = True
            continue
        if in_orientation and line == "---":
            break
        if in_orientation and line.strip() and not line.startswith("- ") and not line.startswith("**"):
            orientation.append(line.strip())
        if len(" ".join(orientation)) > 430:
            break

    story = [
        Paragraph(DOC_TITLE, styles["CoverTitle"]),
        Paragraph(DOC_SUBTITLE, styles["CoverSub"]),
    ]
    if meta:
        meta_text = "<br/>".join(inline_md(line) for line in meta)
        story.append(Paragraph(meta_text, styles["Small"]))
        story.append(Spacer(1, 7))

    desc = (
        "This exam-reference PDF preserves the v1.0.0 notes content and source scope. "
        + " ".join(orientation[:2])
    )
    desc_box = Table(
        [[Paragraph(inline_md(desc), styles["Small"])]],
        colWidths=[7.15 * inch],
        style=[
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
            ("BOX", (0, 0), (-1, -1), 0.6, LINE),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ],
    )
    story.extend([desc_box, Spacer(1, 10), Paragraph("<b>Table of Contents</b>", styles["H2"])])
    for anchor, title in toc:
        story.append(Paragraph(f'<a href="#{anchor}">{inline_md(title)}</a>', styles["TOC"]))

    story.extend(
        [
            Spacer(1, 8),
            HRFlowable(width="35%", thickness=0.45, color=LINE, spaceBefore=2, spaceAfter=4, hAlign="LEFT"),
            Paragraph(
                "Generated with GPT-5 via Codex through the Claudia agent system. "
                "Course: GPPS 463, Politics of Southeast Asia, Nico Ravanilla, UC San Diego GPS. "
                "Always verify against official course materials and readings; this is a study aid.",
                styles["Disclosure"],
            ),
            PageBreak(),
        ]
    )
    return story


def section_header(title, number=None):
    color = DARK
    if number in {4, 5, 6, 7}:
        color = BLUE
    elif number in {8, 9}:
        color = GREEN
    elif number == 10:
        color = GOLD
    return Table(
        [[Paragraph(inline_md(title), STYLES["H1"])]],
        colWidths=[7.15 * inch],
        style=[
            ("BACKGROUND", (0, 0), (-1, -1), color),
            ("LEFTPADDING", (0, 0), (-1, -1), 9),
            ("RIGHTPADDING", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ],
    )


def visual_page(title, number, anchor):
    visual = VISUAL_PAGES.get(number)
    if not visual:
        return []

    image_path = IMAGE_DIR / visual["image"]
    if not image_path.exists():
        raise FileNotFoundError(f"Missing visual asset for section {number}: {image_path}")

    image = RLImage(str(image_path))
    max_width = 7.15 * inch
    max_height = 4.55 * inch
    scale = min(max_width / image.imageWidth, max_height / image.imageHeight)
    image.drawWidth = image.imageWidth * scale
    image.drawHeight = image.imageHeight * scale

    caption = Paragraph(visual["caption"], STYLES["Disclosure"])
    caption_box = Table(
        [[caption]],
        colWidths=[7.15 * inch],
        style=[
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
            ("BOX", (0, 0), (-1, -1), 0.5, LINE),
            ("LEFTPADDING", (0, 0), (-1, -1), 9),
            ("RIGHTPADDING", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ],
    )
    image_table = Table(
        [[image]],
        colWidths=[7.15 * inch],
        style=[
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ],
    )
    return [
        PageBreak(),
        BookmarkAnchor(f"{anchor}_visual", f"Visual: {title}", level=1),
        section_header(f"Visual: {title}", number=number),
        Spacer(1, 12),
        image_table,
        Spacer(1, 12),
        caption_box,
    ]


def is_numbered_section(title):
    return re.match(r"^(\d+)\.", title)


def parse_body(lines, styles):
    story = []
    paragraph_buffer = []
    in_disclosure = False
    pending_anchor = None
    current_section = None
    disclosure_start = next(
        (
            i
            for i, line in enumerate(lines[:-1])
            if line.strip() == "---" and lines[i + 1].startswith("Generated for:")
        ),
        None,
    )

    def flush_paragraph():
        nonlocal paragraph_buffer
        if paragraph_buffer:
            text = " ".join(x.strip() for x in paragraph_buffer)
            story.append(Paragraph(inline_md(text), styles["Body"]))
            paragraph_buffer = []

    def append_pending_visual():
        nonlocal current_section
        if current_section:
            story.extend(visual_page(*current_section))
            current_section = None

    for i, raw in enumerate(lines):
        line = raw.rstrip()

        if not line.strip():
            flush_paragraph()
            story.append(Spacer(1, 2))
            continue

        if line.startswith("# "):
            continue

        if line == "---":
            flush_paragraph()
            if disclosure_start is not None and i == disclosure_start:
                in_disclosure = True
                story.append(PageBreak())
                story.append(BookmarkAnchor("output_disclosure", "Output Disclosure"))
                story.append(section_header("Output Disclosure"))
            else:
                story.append(HRFlowable(width="100%", thickness=0.45, color=LINE, spaceBefore=2, spaceAfter=3))
            continue

        if line.startswith("## "):
            flush_paragraph()
            append_pending_visual()
            title = line[3:].strip()
            anchor = "references" if title == "References" else slugify(title)
            match = is_numbered_section(title)
            number = int(match.group(1)) if match else None
            if story:
                story.append(PageBreak())
            story.append(BookmarkAnchor(anchor, title))
            story.append(section_header(title, number=number))
            story.append(Spacer(1, 6))
            pending_anchor = anchor
            current_section = (title, number, anchor) if number else None
            continue

        if line.startswith("### "):
            flush_paragraph()
            title = line[4:].strip()
            story.append(Paragraph(inline_md(title), styles["H2"]))
            continue

        if line.startswith("- "):
            flush_paragraph()
            story.append(Paragraph(inline_md(line[2:].strip()), styles["StudyBullet"], bulletText="-"))
            continue

        if re.match(r"^\d+\.\s+", line):
            flush_paragraph()
            item = re.sub(r"^\d+\.\s+", "", line).strip()
            story.append(Paragraph(inline_md(item), styles["StudyBullet"], bulletText="-"))
            continue

        if line.startswith("**") and line.endswith("  "):
            flush_paragraph()
            story.append(Paragraph(inline_md(line), styles["Body"]))
            continue

        if line.startswith("Generated for:") or line.startswith("Date:") or line.startswith("Model:") or line.startswith("Sources:") or line.startswith("Agent:"):
            flush_paragraph()
            story.append(Paragraph(inline_md(line), styles["Disclosure"]))
            continue

        if pending_anchor == "references" and line.strip():
            flush_paragraph()
            story.append(Paragraph(inline_md(line.strip()), styles["Ref"]))
            continue

        paragraph_buffer.append(line)

    flush_paragraph()
    return story


def build_pdf():
    lines = read_lines()
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=letter,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.62 * inch,
        bottomMargin=0.72 * inch,
        title=DOC_TITLE,
        author="Poseidon via Claudia",
        subject="GPPS 463 Midterm 2 study reference",
    )
    story = cover_story(lines, STYLES)
    story.extend(parse_body(lines, STYLES))
    doc.build(story, onFirstPage=first_page_footer, onLaterPages=later_page_footer)


STYLES = make_styles()


if __name__ == "__main__":
    build_pdf()
    size_kb = PDF_PATH.stat().st_size / 1024
    print(f"Wrote {PDF_PATH} ({size_kb:.1f} KB)")
