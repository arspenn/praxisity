"""Test PDF generation using praxisity_style with SPEC-002 content."""

import sys
import re
sys.path.insert(0, "/home/arspenn/Dev/praxisity/.praxisity")

from praxisity_style import (
    create_document, styles, build_table, code_block, title_block,
    Paragraph, Spacer, CONTENT_WIDTH
)


def parse_markdown_to_elements(md_text):
    """Simple markdown parser that maps to Praxisity style elements."""
    elements = []
    lines = md_text.split("\n")
    i = 0
    title_found = False

    while i < len(lines):
        line = lines[i]

        # Skip HTML comments
        if line.strip().startswith("<!--"):
            while i < len(lines) and "-->" not in lines[i]:
                i += 1
            i += 1
            continue

        # Title (first # heading)
        if line.startswith("# ") and not title_found:
            title_text = line[2:].strip()
            elements.extend(title_block(title_text))
            title_found = True
            i += 1
            continue

        # Headings
        if line.startswith("## "):
            elements.append(Paragraph(line[3:].strip(), styles["Heading1"]))
            i += 1
            continue
        if line.startswith("### "):
            elements.append(Paragraph(line[4:].strip(), styles["Heading2"]))
            i += 1
            continue
        if line.startswith("#### "):
            elements.append(Paragraph(line[5:].strip(), styles["Heading3"]))
            i += 1
            continue

        # Horizontal rule
        if line.strip() in ("---", "***", "___"):
            elements.append(Spacer(1, 8))
            i += 1
            continue

        # Code block
        if line.strip().startswith("```"):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if code_lines:
                elements.append(code_block("\n".join(code_lines)))
            i += 1
            continue

        # Table (pipe-delimited)
        if "|" in line and line.strip().startswith("|"):
            table_lines = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1

            # Parse table data, skip separator row
            table_data = []
            for tl in table_lines:
                cells = [c.strip() for c in tl.strip().strip("|").split("|")]
                # Skip separator rows (----, :---:, etc.)
                if all(re.match(r'^[-:]+$', c) for c in cells):
                    continue
                table_data.append(cells)

            if table_data:
                elements.append(build_table(table_data))
                elements.append(Spacer(1, 6))
            continue

        # Bullet list
        if line.strip().startswith("- "):
            bullet_text = line.strip()[2:]
            # Handle bold markdown
            bullet_text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', bullet_text)
            elements.append(Paragraph(f"• {bullet_text}", styles["BulletItem"]))
            i += 1
            continue

        # Regular paragraph
        if line.strip():
            # Collect consecutive non-empty, non-special lines
            para_lines = [line.strip()]
            i += 1
            while i < len(lines) and lines[i].strip() and \
                  not lines[i].startswith("#") and \
                  not lines[i].strip().startswith("|") and \
                  not lines[i].strip().startswith("- ") and \
                  not lines[i].strip().startswith("```") and \
                  not lines[i].strip() in ("---", "***", "___"):
                para_lines.append(lines[i].strip())
                i += 1
            text = " ".join(para_lines)
            # Handle bold markdown
            text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
            elements.append(Paragraph(text, styles["BodyText"]))
            continue

        i += 1

    return elements


def main():
    source = "/home/arspenn/Dev/praxisity/.plans/specs/002-build-command.md"
    output = "/home/arspenn/Dev/praxisity/deliverables/002-build-command.pdf"

    with open(source, "r") as f:
        md_content = f.read()

    elements = parse_markdown_to_elements(md_content)

    doc = create_document(output, title="SPEC-002: Build Command", author="Andrew Robert Spenn")
    doc.build(elements)
    print(f"PDF generated: {output}")


if __name__ == "__main__":
    main()