"""
Praxisity Style Module
======================
ReportLab style definitions for consistent PDF output.
Provides fonts, colors, paragraph styles, table styles, and builder functions.

Usage:
    from praxisity_style import create_document, styles, table_style, build_table, code_block
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph,
    Table, TableStyle, Spacer, Preformatted, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# =============================================================================
# 1. Font Registration
# =============================================================================

FONT_DIR = "/usr/share/fonts/truetype/liberation"

_FONT_MAP = {
    "PraxisSans": "LiberationSans-Regular.ttf",
    "PraxisSans-Bold": "LiberationSans-Bold.ttf",
    "PraxisSans-Italic": "LiberationSans-Italic.ttf",
    "PraxisSans-BoldItalic": "LiberationSans-BoldItalic.ttf",
    "PraxisMono": "LiberationMono-Regular.ttf",
    "PraxisMono-Bold": "LiberationMono-Bold.ttf",
    "PraxisMono-Italic": "LiberationMono-Italic.ttf",
    "PraxisMono-BoldItalic": "LiberationMono-BoldItalic.ttf",
}

_fonts_registered = False

def register_fonts():
    """Register Liberation fonts with ReportLab. Falls back to Helvetica/Courier."""
    global _fonts_registered
    if _fonts_registered:
        return True

    try:
        for name, filename in _FONT_MAP.items():
            path = os.path.join(FONT_DIR, filename)
            if os.path.exists(path):
                pdfmetrics.registerFont(TTFont(name, path))
            else:
                return False

        pdfmetrics.registerFontFamily(
            "PraxisSans",
            normal="PraxisSans",
            bold="PraxisSans-Bold",
            italic="PraxisSans-Italic",
            boldItalic="PraxisSans-BoldItalic",
        )
        pdfmetrics.registerFontFamily(
            "PraxisMono",
            normal="PraxisMono",
            bold="PraxisMono-Bold",
            italic="PraxisMono-Italic",
            boldItalic="PraxisMono-BoldItalic",
        )
        _fonts_registered = True
        return True
    except Exception:
        return False


# Register on import
_USE_CUSTOM_FONTS = register_fonts()

# Font names (fall back to built-ins if registration failed)
FONT_BODY = "PraxisSans" if _USE_CUSTOM_FONTS else "Helvetica"
FONT_BODY_BOLD = "PraxisSans-Bold" if _USE_CUSTOM_FONTS else "Helvetica-Bold"
FONT_BODY_ITALIC = "PraxisSans-Italic" if _USE_CUSTOM_FONTS else "Helvetica-Oblique"
FONT_MONO = "PraxisMono" if _USE_CUSTOM_FONTS else "Courier"
FONT_MONO_BOLD = "PraxisMono-Bold" if _USE_CUSTOM_FONTS else "Courier-Bold"


# =============================================================================
# 2. Color Constants
# =============================================================================

COLOR_BODY = HexColor("#1a1a1a")        # Near-black body text
COLOR_SECONDARY = HexColor("#555555")   # Metadata, captions
COLOR_ACCENT = HexColor("#2c3e50")      # Headings
COLOR_BORDER = HexColor("#cccccc")      # Table rules
COLOR_BG_LIGHT = HexColor("#f5f5f5")    # Code blocks, table header background
COLOR_WHITE = white


# =============================================================================
# 3. Page Layout
# =============================================================================

PAGE_WIDTH, PAGE_HEIGHT = letter  # 8.5 x 11 inches
MARGIN = 1 * inch
CONTENT_WIDTH = PAGE_WIDTH - 2 * MARGIN


def _build_page_template():
    """Create page template with 1-inch margins, no header/footer."""
    content_frame = Frame(
        MARGIN, MARGIN,
        CONTENT_WIDTH, PAGE_HEIGHT - 2 * MARGIN,
        id="content",
        leftPadding=0, rightPadding=0,
        topPadding=0, bottomPadding=0,
    )
    return PageTemplate(id="default", frames=[content_frame])


# =============================================================================
# 4. Paragraph Styles
# =============================================================================

styles = {}

styles["Title"] = ParagraphStyle(
    "Title",
    fontName=FONT_BODY_BOLD,
    fontSize=22,
    leading=28,
    textColor=COLOR_ACCENT,
    spaceAfter=6,
    alignment=TA_LEFT,
)

styles["Subtitle"] = ParagraphStyle(
    "Subtitle",
    fontName=FONT_BODY,
    fontSize=12,
    leading=16,
    textColor=COLOR_SECONDARY,
    spaceAfter=24,
    alignment=TA_LEFT,
)

styles["Heading1"] = ParagraphStyle(
    "Heading1",
    fontName=FONT_BODY_BOLD,
    fontSize=16,
    leading=22,
    textColor=COLOR_ACCENT,
    spaceBefore=18,
    spaceAfter=8,
    keepWithNext=True,
    alignment=TA_LEFT,
)

styles["Heading2"] = ParagraphStyle(
    "Heading2",
    fontName=FONT_BODY_BOLD,
    fontSize=13,
    leading=18,
    textColor=COLOR_ACCENT,
    spaceBefore=14,
    spaceAfter=6,
    keepWithNext=True,
    alignment=TA_LEFT,
)

styles["Heading3"] = ParagraphStyle(
    "Heading3",
    fontName=FONT_BODY_BOLD,
    fontSize=11,
    leading=15,
    textColor=COLOR_BODY,
    spaceBefore=10,
    spaceAfter=4,
    keepWithNext=True,
    alignment=TA_LEFT,
)

styles["BodyText"] = ParagraphStyle(
    "BodyText",
    fontName=FONT_BODY,
    fontSize=10,
    leading=14,
    textColor=COLOR_BODY,
    spaceBefore=2,
    spaceAfter=6,
    alignment=TA_LEFT,
)

styles["BulletItem"] = ParagraphStyle(
    "BulletItem",
    parent=styles["BodyText"],
    leftIndent=18,
    bulletIndent=6,
    spaceBefore=1,
    spaceAfter=3,
)

styles["CodeBlock"] = ParagraphStyle(
    "CodeBlock",
    fontName=FONT_MONO,
    fontSize=8.5,
    leading=12,
    textColor=COLOR_BODY,
    spaceBefore=6,
    spaceAfter=6,
    leftIndent=6,
    rightIndent=6,
    backColor=COLOR_BG_LIGHT,
    alignment=TA_LEFT,
)

styles["Caption"] = ParagraphStyle(
    "Caption",
    fontName=FONT_BODY_ITALIC,
    fontSize=9,
    leading=12,
    textColor=COLOR_SECONDARY,
    spaceBefore=4,
    spaceAfter=10,
    alignment=TA_LEFT,
)

styles["Metadata"] = ParagraphStyle(
    "Metadata",
    fontName=FONT_BODY,
    fontSize=9,
    leading=13,
    textColor=COLOR_SECONDARY,
    spaceAfter=2,
    alignment=TA_LEFT,
)


# =============================================================================
# 5. Table Style Defaults
# =============================================================================

table_style = TableStyle([
    # Header row
    ("BACKGROUND", (0, 0), (-1, 0), COLOR_BG_LIGHT),
    ("FONTNAME", (0, 0), (-1, 0), FONT_BODY_BOLD),
    ("FONTSIZE", (0, 0), (-1, 0), 9),

    # All cells
    ("FONTNAME", (0, 1), (-1, -1), FONT_BODY),
    ("FONTSIZE", (0, 1), (-1, -1), 9),
    ("TEXTCOLOR", (0, 0), (-1, -1), COLOR_BODY),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("ALIGN", (0, 0), (-1, -1), "LEFT"),

    # Minimal horizontal rules (IEEE-inspired)
    ("LINEABOVE", (0, 0), (-1, 0), 0.8, COLOR_BORDER),
    ("LINEBELOW", (0, 0), (-1, 0), 0.8, COLOR_BORDER),
    ("LINEBELOW", (0, -1), (-1, -1), 0.8, COLOR_BORDER),
])


# =============================================================================
# 6. Convenience Builder Functions
# =============================================================================

def create_document(filename, title="Untitled", author="Praxisity"):
    """Create a configured BaseDocTemplate ready for content."""
    doc = BaseDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
        title=title,
        author=author,
    )
    doc.addPageTemplates([_build_page_template()])
    return doc


def build_table(data, col_widths=None):
    """Build a styled table from a list of lists.

    Args:
        data: List of rows, where each row is a list of cell values.
              First row is treated as the header.
        col_widths: Optional list of column widths. If None, auto-sized
                    to fill CONTENT_WIDTH evenly.
    """
    if not data:
        return Spacer(1, 0)

    if col_widths is None:
        num_cols = len(data[0])
        col_widths = [CONTENT_WIDTH / num_cols] * num_cols

    # Wrap cell content in Paragraphs for text wrapping
    styled_data = []
    for i, row in enumerate(data):
        styled_row = []
        for cell in row:
            cell_style = styles["BodyText"]
            if i == 0:
                cell_style = ParagraphStyle(
                    "TableHeader",
                    parent=styles["BodyText"],
                    fontName=FONT_BODY_BOLD,
                    fontSize=9,
                )
            styled_row.append(Paragraph(str(cell), cell_style))
        styled_data.append(styled_row)

    t = Table(styled_data, colWidths=col_widths, repeatRows=1)
    t.setStyle(table_style)
    return t


def code_block(text):
    """Create a styled code block from preformatted text."""
    # Escape XML entities for ReportLab Paragraph
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return Preformatted(text, styles["CodeBlock"])


def title_block(title, subtitle=None, metadata=None):
    """Create a title block for the first page.

    Args:
        title: Document title string
        subtitle: Optional subtitle string
        metadata: Optional dict of metadata (e.g., {"Author": "...", "Date": "..."})

    Returns:
        List of flowable elements for the title block.
    """
    elements = []
    elements.append(Paragraph(title, styles["Title"]))

    if subtitle:
        elements.append(Paragraph(subtitle, styles["Subtitle"]))

    if metadata:
        for key, value in metadata.items():
            elements.append(Paragraph(f"<b>{key}:</b> {value}", styles["Metadata"]))
        elements.append(Spacer(1, 12))

    elements.append(Spacer(1, 18))
    return elements