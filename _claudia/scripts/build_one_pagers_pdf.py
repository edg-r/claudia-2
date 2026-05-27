import os
import re
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
    HRFlowable,
)

# Configuration Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MD_PATH = BASE_DIR / "edgar" / "2026-05-27_class_reading_one_pagers.md"
PDF_PATH = BASE_DIR / "edgar" / "2026-05-27_class_reading_one_pagers.pdf"

# Design Color Palette
DARK_NAVY = colors.HexColor("#1B2A4A")
MED_BLUE = colors.HexColor("#2C5282")
LIGHT_BLUE = colors.HexColor("#EBF4FF")
ACCENT_GOLD = colors.HexColor("#C69C3F")
WARM_AMBER = colors.HexColor("#FFF5E6")
LIGHT_GREY = colors.HexColor("#F7F7F7")
BORDER_GREY = colors.HexColor("#CCCCCC")
TEXT_COLOR = colors.HexColor("#222222")

# Initialize Styles
styles = getSampleStyleSheet()

# Add Custom Typography Styles
styles.add(ParagraphStyle(
    name="CoverPreTitle", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=9, leading=11, textColor=ACCENT_GOLD, alignment=TA_CENTER, spaceAfter=4))

styles.add(ParagraphStyle(
    name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=22, leading=26, textColor=DARK_NAVY, alignment=TA_CENTER, spaceAfter=8))

styles.add(ParagraphStyle(
    name="CoverSub", parent=styles["Normal"], fontName="Helvetica",
    fontSize=10, leading=14, alignment=TA_CENTER, textColor=colors.HexColor("#555555"), spaceAfter=15))

styles.add(ParagraphStyle(
    name="CourseHeader", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=13, leading=16, textColor=colors.white))

styles.add(ParagraphStyle(
    name="ReadingHeader", parent=styles["Heading2"], fontName="Helvetica-Bold",
    fontSize=12, leading=15, textColor=DARK_NAVY, spaceBefore=8, spaceAfter=6))

styles.add(ParagraphStyle(
    name="CustomBody", parent=styles["Normal"], fontName="Helvetica",
    fontSize=10, leading=14, textColor=TEXT_COLOR, spaceAfter=6))

styles.add(ParagraphStyle(
    name="BulletText", parent=styles["Normal"], fontName="Helvetica",
    fontSize=10, leading=14, textColor=TEXT_COLOR,
    leftIndent=12, firstLineIndent=-8, spaceAfter=4))

styles.add(ParagraphStyle(
    name="DisclosureText", parent=styles["Normal"], fontName="Helvetica",
    fontSize=8.5, leading=12, textColor=colors.HexColor("#444444")))


def escape_xml_entities(text):
    """
    Escapes special XML characters, particularly ampersands, to avoid ReportLab parser failures.
    """
    # Replace raw ampersands with XML entities
    text = text.replace("&", "&amp;")
    # Ensure double escaping doesn't happen
    text = text.replace("&amp;amp;", "&amp;")
    return text


def format_bold_italic(text):
    """
    Parses simple Markdown bold (**) and italic (*) into ReportLab HTML-like tags.
    """
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", text)
    return text


def parse_markdown_to_story(model_name="Gemini 2.0 Flash"):
    """
    Reads the target markdown file and parses it into ReportLab flowables.
    """
    if not MD_PATH.exists():
        raise FileNotFoundError(f"Markdown source file not found at {MD_PATH}")

    with open(MD_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    story = []
    
    # Block splitting logic
    blocks = []
    current_block = []
    in_yaml = False
    yaml_count = 0

    for line in lines:
        stripped = line.strip()
        
        # Handle YAML header boundary
        if line.startswith("---"):
            yaml_count += 1
            if yaml_count == 1:
                in_yaml = True
                continue
            elif yaml_count == 2:
                in_yaml = False
                continue
                
        if in_yaml:
            continue
            
        if stripped == "\\newpage":
            if current_block:
                blocks.append(current_block)
                current_block = []
            blocks.append(["\\newpage"])
            continue
            
        if stripped == "":
            if current_block:
                blocks.append(current_block)
                current_block = []
        else:
            # Check if block breaks should happen on headers or list items
            if stripped.startswith("# ") or stripped.startswith("## ") or stripped.startswith("- ") or stripped.startswith("* "):
                if current_block:
                    blocks.append(current_block)
                    current_block = []
            current_block.append(stripped)

    if current_block:
        blocks.append(current_block)

    # Process parsed blocks into flowables
    for block in blocks:
        if not block:
            continue
            
        first_line = block[0].strip()
        
        # Page break command
        if first_line == "\\newpage":
            story.append(PageBreak())
            continue
            
        # H1 Headers (Main Title or Course Title)
        elif first_line.startswith("# "):
            heading_text = first_line[2:].strip()
            heading_text = escape_xml_entities(heading_text)
            
            # If it is the main title of the document
            if "Reading One-Pagers" in heading_text:
                story.append(Spacer(1, 15))
                story.append(Paragraph("GRADUATE POLICY STUDY PACKET", styles["CoverPreTitle"]))
                story.append(Paragraph(heading_text, styles["CoverTitle"]))
                story.append(Paragraph("COMPILED FOR WEDNESDAY CLASSES | UNIVERSITY OF CALIFORNIA SAN DIEGO", styles["CoverSub"]))
                story.append(HRFlowable(width="75%", thickness=1.5, color=ACCENT_GOLD, spaceBefore=4, spaceAfter=20))
                story.append(Spacer(1, 10))
            # Otherwise, it's a course name
            else:
                data = [[Paragraph(heading_text, styles["CourseHeader"])]]
                tbl = Table(data, colWidths=[7.1 * inch], style=TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), DARK_NAVY),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ]))
                story.append(Spacer(1, 12))
                story.append(tbl)
                story.append(Spacer(1, 8))
                
        # H2 Headers (Readings)
        elif first_line.startswith("## "):
            reading_text = first_line[3:].strip()
            reading_text = escape_xml_entities(reading_text)
            story.append(Paragraph(reading_text, styles["ReadingHeader"]))
            story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_GREY, spaceBefore=1, spaceAfter=8))
            
        # Bullet list items
        elif first_line.startswith("- ") or first_line.startswith("* "):
            bullet_content = " ".join(block)
            bullet_content = bullet_content[2:].strip() # Strip list marker
            bullet_content = escape_xml_entities(bullet_content)
            bullet_content = format_bold_italic(bullet_content)
            story.append(Paragraph(f"• {bullet_content}", styles["BulletText"]))
            
        # Normal paragraphs
        else:
            para_content = " ".join(block)
            para_content = escape_xml_entities(para_content)
            para_content = format_bold_italic(para_content)
            story.append(Paragraph(para_content, styles["CustomBody"]))
            story.append(Spacer(1, 3))

    # Append Output Disclosure Table
    disclosure_html = f"""
    <b>GRADUATE POLICY BRIEFING DISCLOSURE</b><br/>
    <b>Generated for:</b> Edgar Agunias | <b>Date:</b> 2026-05-27<br/>
    <b>Model:</b> {model_name}<br/>
    <b>Sources:</b> Course syllabi, readings database, lecture notes, and local PDFs for GPCO 410 (Lake) and GPPS 463 (Tajima et al.)<br/>
    <b>Agent:</b> Claudia (Orchestration) with Athena, Plutus, Tyche, Ares, and Poseidon (Course Agents)
    """
    
    disclosure_data = [[Paragraph(disclosure_html, styles["DisclosureText"])]]
    disclosure_table = Table(disclosure_data, colWidths=[7.1 * inch])
    disclosure_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER_GREY),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    
    story.append(Spacer(1, 15))
    story.append(disclosure_table)

    return story


def header_footer(canvas, doc):
    """
    Template page canvas callback to render page numbers and the running header.
    """
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#555555"))
    
    # Running Header (on page 2 and later)
    if doc.page > 1:
        canvas.drawString(0.7 * inch, 10.45 * inch, "Wednesday Class Reading Briefs | Edgar Agunias")
        canvas.setStrokeColor(BORDER_GREY)
        canvas.setLineWidth(0.5)
        canvas.line(0.7 * inch, 10.35 * inch, letter[0] - 0.7 * inch, 10.35 * inch)
        
    # Running Footer (on all pages)
    canvas.drawRightString(letter[0] - 0.7 * inch, 0.4 * inch, f"Page {doc.page}")
    canvas.drawString(0.7 * inch, 0.4 * inch, "Claudia Workspace Briefing Capsule")
    
    canvas.restoreState()


def build_pdf(model_name="Gemini 2.0 Flash"):
    """
    Compiles the Markdown story into a beautifully typeset PDF document.
    """
    print(f"Parsing Markdown: {MD_PATH}")
    story = parse_markdown_to_story(model_name)
    
    print(f"Configuring PDF Template: {PDF_PATH}")
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=letter,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.8 * inch,
        bottomMargin=0.8 * inch,
    )
    
    print("Building document pages...")
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print("PDF compilation completed successfully!")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build PDF from Markdown briefs.")
    parser.add_argument("--model", type=str, default="Gemini 2.0 Flash", help="The name of the AI model executing the build.")
    args = parser.parse_args()
    build_pdf(args.model)
