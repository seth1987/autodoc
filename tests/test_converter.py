"""Tests for conversion service."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock


class TestConversionService:
    """Tests for conversion service."""

    def test_conversion_service_import(self):
        """Test that conversion service can be imported."""
        from backend.app.services.converter import conversion_service
        assert conversion_service is not None

    def test_chunk_text_small_document(self):
        """Test that small documents are not chunked."""
        from backend.app.services.converter import ConversionService

        service = ConversionService()
        service.chunking_threshold = 6000

        small_text = "This is a small document." * 10  # ~260 chars = ~65 tokens
        chunks = service._chunk_text(small_text)

        assert len(chunks) == 1
        assert chunks[0] == small_text

    def test_chunk_text_large_document(self):
        """Test that large documents are chunked."""
        from backend.app.services.converter import ConversionService

        service = ConversionService()
        service.chunking_threshold = 100  # Low threshold for testing

        # Create text with multiple paragraphs
        paragraphs = ["Paragraph " + str(i) + " " * 100 for i in range(20)]
        large_text = "\n\n".join(paragraphs)

        chunks = service._chunk_text(large_text)

        assert len(chunks) > 1

    def test_generate_output_filename(self):
        """Test output filename generation."""
        from backend.app.services.converter import ConversionService

        service = ConversionService()

        assert service._generate_output_filename("document.pdf") == "document_converted.html"
        assert service._generate_output_filename("report.docx") == "report_converted.html"
        assert service._generate_output_filename("file") == "file_converted.html"


class TestHTMLGenerator:
    """Tests for HTML generator."""

    def test_html_generator_import(self):
        """Test that HTML generator can be imported."""
        from backend.app.services.html_generator import html_generator
        assert html_generator is not None

    def test_escape_html(self):
        """Test HTML escaping."""
        from backend.app.services.html_generator import HTMLGenerator

        generator = HTMLGenerator()

        assert "&lt;" in generator._escape("<script>")
        assert "&gt;" in generator._escape("</script>")
        assert "&amp;" in generator._escape("&")

    def test_escape_markdown_bold(self):
        """Test markdown bold conversion."""
        from backend.app.services.html_generator import HTMLGenerator

        generator = HTMLGenerator()

        result = generator._escape("This is **bold** text")
        assert "<strong>bold</strong>" in result

    def test_escape_markdown_italic(self):
        """Test markdown italic conversion."""
        from backend.app.services.html_generator import HTMLGenerator

        generator = HTMLGenerator()

        result = generator._escape("This is *italic* text")
        assert "<em>italic</em>" in result

    def test_generate_cover(self):
        """Test cover page generation."""
        from backend.app.services.html_generator import HTMLGenerator
        from backend.app.models import Metadata

        generator = HTMLGenerator()
        meta = Metadata(
            title="Test Title",
            subtitle="Test Subtitle",
            phase="Phase 1",
            brand="Test Brand",
            tagline="Test Tagline",
            date="January 2026"
        )

        html = generator._generate_cover(meta)

        assert "Test Title" in html
        assert "Test Subtitle" in html
        assert "Phase 1" in html
        assert 'class="cover"' in html

    def test_generate_callout(self):
        """Test callout generation."""
        from backend.app.services.html_generator import HTMLGenerator

        generator = HTMLGenerator()

        block = {
            "type": "callout",
            "variant": "success",
            "title": "Success Title",
            "content": "Success content"
        }

        html = generator._generate_callout(block)

        assert 'class="note success"' in html
        assert "Success Title" in html
        assert "Success content" in html

    def test_generate_table(self):
        """Test table generation."""
        from backend.app.services.html_generator import HTMLGenerator

        generator = HTMLGenerator()

        block = {
            "type": "table",
            "headers": ["Col1", "Col2"],
            "rows": [["A", "B"], ["C", "D"]]
        }

        html = generator._generate_table(block)

        assert "<table>" in html
        assert "<th>Col1</th>" in html
        assert "<td>A</td>" in html


class TestDocumentStructure:
    """Tests for document structure models."""

    def test_document_structure_minimal(self):
        """Test minimal document structure."""
        from backend.app.models import DocumentStructure, Metadata

        doc = DocumentStructure(
            metadata=Metadata(title="Test"),
            sections=[]
        )

        assert doc.metadata.title == "Test"
        assert doc.toc is True
        assert doc.sections == []
        assert doc.conclusion is None
        assert doc.sources == []

    def test_document_structure_full(self):
        """Test full document structure."""
        from backend.app.models import DocumentStructure, Metadata, Section, Source

        doc = DocumentStructure(
            metadata=Metadata(
                title="Full Test",
                subtitle="Subtitle",
                phase="Phase 1",
                brand="Brand",
                tagline="Tagline",
                date="2026"
            ),
            toc=True,
            sections=[
                Section(title="Section 1", content=[])
            ],
            sources=[
                Source(title="Source 1", url="https://example.com")
            ]
        )

        assert doc.metadata.title == "Full Test"
        assert len(doc.sections) == 1
        assert len(doc.sources) == 1
