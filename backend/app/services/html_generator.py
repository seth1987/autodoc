"""HTML generator from document structure."""

import html
from typing import Optional
from ..models import DocumentStructure, Metadata, Section, ConclusionSection, Source
from ..templates.base_template import get_html_template


class HTMLGenerator:
    """Generate HTML from DocumentStructure."""

    def generate(self, doc: DocumentStructure) -> str:
        """
        Generate complete HTML document.

        Args:
            doc: Parsed document structure.

        Returns:
            Complete HTML string.
        """
        parts = []

        # Cover page
        parts.append(self._generate_cover(doc.metadata))

        # Content wrapper
        parts.append('<div class="content">')

        # Table of contents
        if doc.toc and doc.sections:
            parts.append(self._generate_toc(doc.sections))

        # Sections
        for i, section in enumerate(doc.sections, 1):
            parts.append(self._generate_section(section, i))
            if i < len(doc.sections):
                parts.append('<div class="divider">· · ·</div>')

        # Conclusion
        if doc.conclusion:
            parts.append(self._generate_conclusion(doc.conclusion))

        # Sources
        if doc.sources:
            parts.append(self._generate_sources(doc.sources))

        parts.append('</div>')  # Close content

        # Footer
        parts.append(self._generate_footer(doc.metadata))

        content = "\n".join(parts)
        return get_html_template(doc.metadata.title, content)

    def _escape(self, text: str) -> str:
        """Escape HTML and convert markdown formatting."""
        if not text:
            return ""
        escaped = html.escape(text)
        # Convert **bold** to <strong>
        import re
        escaped = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', escaped)
        # Convert *italic* to <em>
        escaped = re.sub(r'\*(.+?)\*', r'<em>\1</em>', escaped)
        return escaped

    def _generate_cover(self, meta: Metadata) -> str:
        """Generate cover page HTML."""
        parts = ['<div class="cover">']

        if meta.phase:
            parts.append(f'    <div class="cover-phase">{self._escape(meta.phase)}</div>')

        parts.append(f'    <h1>{self._escape(meta.title)}</h1>')

        if meta.subtitle:
            parts.append(f'    <p class="cover-subtitle">{self._escape(meta.subtitle)}</p>')

        parts.append('    <div style="margin-top: auto;">')
        if meta.brand:
            parts.append(f'        <div class="cover-brand">{self._escape(meta.brand)}</div>')
        if meta.tagline:
            parts.append(f'        <p class="cover-tagline">{self._escape(meta.tagline)}</p>')
        parts.append('    </div>')

        if meta.date:
            parts.append(f'    <div class="cover-date">{self._escape(meta.date)}</div>')

        parts.append('</div>')
        return "\n".join(parts)

    def _generate_toc(self, sections: list[Section]) -> str:
        """Generate table of contents HTML."""
        parts = ['<div class="toc">', '    <h2>Sommaire</h2>', '    <ol>']

        for section in sections:
            parts.append(f'        <li><span>{self._escape(section.title)}</span></li>')

        parts.extend(['    </ol>', '</div>'])
        return "\n".join(parts)

    def _generate_section(self, section: Section, num: int) -> str:
        """Generate section HTML."""
        parts = ['<div class="section">']

        # Section header
        parts.append('    <div class="section-header">')
        parts.append(f'        <div class="section-num">{num:02d}</div>')
        parts.append(f'        <h2 class="section-title">{self._escape(section.title)}</h2>')
        parts.append('    </div>')

        # Section content
        for block in section.content:
            block_html = self._generate_block(block)
            if block_html:
                parts.append(block_html)

        parts.append('</div>')
        return "\n".join(parts)

    def _generate_block(self, block: dict) -> str:
        """Generate HTML for a content block."""
        block_type = block.get("type", "")

        if block_type == "paragraph":
            return f'    <p>{self._escape(block.get("text", ""))}</p>'

        elif block_type == "heading":
            level = block.get("level", 3)
            text = self._escape(block.get("text", ""))
            if level == 3:
                return f'    <h3 class="subsection-title">{text}</h3>'
            elif level == 4:
                return f'    <h4>{text}</h4>'
            else:
                return f'    <h{level}>{text}</h{level}>'

        elif block_type == "callout":
            return self._generate_callout(block)

        elif block_type == "list":
            return self._generate_list(block)

        elif block_type == "table":
            return self._generate_table(block)

        elif block_type == "quote":
            return f'    <div class="quote">{self._escape(block.get("text", ""))}</div>'

        elif block_type == "timeline":
            return self._generate_timeline(block)

        elif block_type == "stats":
            return self._generate_stats(block)

        elif block_type == "cards":
            return self._generate_cards(block)

        elif block_type == "two-col":
            return self._generate_two_col(block)

        return ""

    def _generate_callout(self, block: dict) -> str:
        """Generate callout/note HTML."""
        variant = block.get("variant", "note")
        title = block.get("title")
        content = block.get("content", "")

        variant_class = f" {variant}" if variant != "note" else ""

        parts = [f'    <div class="note{variant_class}">']
        if title:
            parts.append(f'        <div class="note-title">{self._escape(title)}</div>')
        parts.append(f'        <p>{self._escape(content)}</p>')
        parts.append('    </div>')

        return "\n".join(parts)

    def _generate_list(self, block: dict) -> str:
        """Generate list HTML."""
        style = block.get("style", "bullet")
        items = block.get("items", [])

        if style == "checklist":
            parts = ['    <ul class="checklist">']
            for item in items:
                text = item.get("text", "") if isinstance(item, dict) else str(item)
                checked = item.get("checked", "true") if isinstance(item, dict) else "true"
                cross_class = ' class="cross"' if checked == "cross" else ""
                parts.append(f'        <li{cross_class}>{self._escape(text)}</li>')
            parts.append('    </ul>')
        elif style == "numbered":
            parts = ['    <ol>']
            for item in items:
                text = item.get("text", "") if isinstance(item, dict) else str(item)
                parts.append(f'        <li>{self._escape(text)}</li>')
            parts.append('    </ol>')
        else:  # bullet
            parts = ['    <ul>']
            for item in items:
                text = item.get("text", "") if isinstance(item, dict) else str(item)
                parts.append(f'        <li>{self._escape(text)}</li>')
            parts.append('    </ul>')

        return "\n".join(parts)

    def _generate_table(self, block: dict) -> str:
        """Generate table HTML."""
        headers = block.get("headers", [])
        rows = block.get("rows", [])

        parts = ['    <table>', '        <thead>', '            <tr>']

        for header in headers:
            parts.append(f'                <th>{self._escape(header)}</th>')

        parts.extend(['            </tr>', '        </thead>', '        <tbody>'])

        for row in rows:
            parts.append('            <tr>')
            for cell in row:
                parts.append(f'                <td>{self._escape(cell)}</td>')
            parts.append('            </tr>')

        parts.extend(['        </tbody>', '    </table>'])
        return "\n".join(parts)

    def _generate_timeline(self, block: dict) -> str:
        """Generate timeline HTML."""
        items = block.get("items", [])
        parts = ['    <div class="timeline">']

        for item in items:
            title = item.get("title", "")
            description = item.get("description", "")
            parts.append('        <div class="timeline-item">')
            parts.append(f'            <div class="timeline-title">{self._escape(title)}</div>')
            parts.append(f'            <p>{self._escape(description)}</p>')
            parts.append('        </div>')

        parts.append('    </div>')
        return "\n".join(parts)

    def _generate_stats(self, block: dict) -> str:
        """Generate stats HTML."""
        items = block.get("items", [])
        parts = ['    <div class="stats">']

        for item in items:
            value = item.get("value", "")
            label = item.get("label", "")
            parts.append('        <div class="stat">')
            parts.append(f'            <div class="stat-value">{self._escape(value)}</div>')
            parts.append(f'            <div class="stat-label">{self._escape(label)}</div>')
            parts.append('        </div>')

        parts.append('    </div>')
        return "\n".join(parts)

    def _generate_cards(self, block: dict) -> str:
        """Generate cards HTML."""
        items = block.get("items", [])
        parts = ['    <div class="cards">']

        for item in items:
            title = item.get("title", "")
            content = item.get("content", "")
            parts.append('        <div class="card">')
            parts.append(f'            <div class="card-title">{self._escape(title)}</div>')
            parts.append(f'            <p>{self._escape(content)}</p>')
            parts.append('        </div>')

        parts.append('    </div>')
        return "\n".join(parts)

    def _generate_two_col(self, block: dict) -> str:
        """Generate two-column layout HTML."""
        left = block.get("left", {})
        right = block.get("right", {})

        parts = ['    <div class="two-col">']

        # Left column
        parts.append('        <div class="col">')
        if left.get("title"):
            parts.append(f'            <div class="col-title">{self._escape(left["title"])}</div>')
        for content_block in left.get("content", []):
            inner_html = self._generate_block(content_block)
            if inner_html:
                parts.append(inner_html)
        parts.append('        </div>')

        # Right column
        parts.append('        <div class="col">')
        if right.get("title"):
            parts.append(f'            <div class="col-title">{self._escape(right["title"])}</div>')
        for content_block in right.get("content", []):
            inner_html = self._generate_block(content_block)
            if inner_html:
                parts.append(inner_html)
        parts.append('        </div>')

        parts.append('    </div>')
        return "\n".join(parts)

    def _generate_conclusion(self, conclusion: ConclusionSection) -> str:
        """Generate conclusion HTML."""
        parts = ['<div class="conclusion">']

        parts.append(f'    <h2>{self._escape(conclusion.title)}</h2>')

        if conclusion.summary:
            parts.append(f'    <p>{self._escape(conclusion.summary)}</p>')

        for section in conclusion.sections:
            if isinstance(section, dict):
                title = section.get("title", "")
                items = section.get("items", [])
                parts.append(f'    <h3>{self._escape(title)}</h3>')
                parts.append('    <ul>')
                for item in items:
                    parts.append(f'        <li>{self._escape(item)}</li>')
                parts.append('    </ul>')

        parts.append('</div>')
        return "\n".join(parts)

    def _generate_sources(self, sources: list[Source]) -> str:
        """Generate sources section HTML."""
        parts = ['<div class="sources">', '    <h2>Sources</h2>']

        for source in sources:
            parts.append('    <div class="source">')
            parts.append(f'        <strong>{self._escape(source.title)}</strong>')
            if source.url:
                parts.append(f'        <div class="source-url">{self._escape(source.url)}</div>')
            if source.meta:
                parts.append(f'        <div class="source-meta">{self._escape(source.meta)}</div>')
            parts.append('    </div>')

        parts.append('</div>')
        return "\n".join(parts)

    def _generate_footer(self, meta: Metadata) -> str:
        """Generate footer HTML."""
        parts = ['<div class="footer">']

        if meta.brand:
            parts.append(f'    <div class="footer-brand">{self._escape(meta.brand)}</div>')

        parts.append(f'    <p>{self._escape(meta.title)}</p>')

        if meta.date:
            parts.append(f'    <p>{self._escape(meta.date)}</p>')

        parts.append('</div>')
        return "\n".join(parts)


# Singleton instance
html_generator = HTMLGenerator()
