"""Tests for document extractors."""

import pytest
from pathlib import Path


class TestPDFExtractor:
    """Tests for PDF extraction."""

    def test_pdf_extractor_import(self):
        """Test that PDF extractor can be imported."""
        from backend.app.extractors import pdf_extractor
        assert pdf_extractor is not None

    def test_pdf_extractor_supported_extensions(self):
        """Test supported extensions."""
        from backend.app.extractors import PDFExtractor
        extractor = PDFExtractor()
        assert ".pdf" in extractor.supported_extensions

    def test_pdf_extractor_invalid_extension(self):
        """Test that invalid extension raises error."""
        from backend.app.extractors import PDFExtractor
        extractor = PDFExtractor()

        with pytest.raises(ValueError, match="Unsupported file type"):
            extractor.extract("test.txt")

    def test_pdf_extractor_file_not_found(self):
        """Test that missing file raises error."""
        from backend.app.extractors import PDFExtractor
        extractor = PDFExtractor()

        with pytest.raises(FileNotFoundError):
            extractor.extract("nonexistent.pdf")


class TestDOCXExtractor:
    """Tests for DOCX extraction."""

    def test_docx_extractor_import(self):
        """Test that DOCX extractor can be imported."""
        from backend.app.extractors import docx_extractor
        assert docx_extractor is not None

    def test_docx_extractor_supported_extensions(self):
        """Test supported extensions."""
        from backend.app.extractors import DOCXExtractor
        extractor = DOCXExtractor()
        assert ".docx" in extractor.supported_extensions

    def test_docx_extractor_invalid_extension(self):
        """Test that invalid extension raises error."""
        from backend.app.extractors import DOCXExtractor
        extractor = DOCXExtractor()

        with pytest.raises(ValueError, match="Unsupported file type"):
            extractor.extract("test.pdf")


class TestGetExtractor:
    """Tests for get_extractor function."""

    def test_get_pdf_extractor(self):
        """Test getting PDF extractor."""
        from backend.app.extractors import get_extractor, PDFExtractor
        extractor = get_extractor("document.pdf")
        assert isinstance(extractor, PDFExtractor)

    def test_get_docx_extractor(self):
        """Test getting DOCX extractor."""
        from backend.app.extractors import get_extractor, DOCXExtractor
        extractor = get_extractor("document.docx")
        assert isinstance(extractor, DOCXExtractor)

    def test_get_extractor_unsupported(self):
        """Test that unsupported file raises error."""
        from backend.app.extractors import get_extractor

        with pytest.raises(ValueError, match="Unsupported file type"):
            get_extractor("document.txt")

    def test_get_extractor_case_insensitive(self):
        """Test case insensitivity."""
        from backend.app.extractors import get_extractor, PDFExtractor
        extractor = get_extractor("document.PDF")
        assert isinstance(extractor, PDFExtractor)
