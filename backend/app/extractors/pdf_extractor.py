"""PDF text extraction using PyMuPDF."""

import fitz  # PyMuPDF
from typing import Optional
from pathlib import Path


class PDFExtractor:
    """Extract text content from PDF files."""

    def __init__(self):
        self.supported_extensions = [".pdf"]

    def extract(self, file_path: str | Path) -> str:
        """
        Extract text from a PDF file.

        Args:
            file_path: Path to the PDF file.

        Returns:
            Extracted text content.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If file is not a valid PDF.
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_path.suffix.lower() not in self.supported_extensions:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")

        return self._extract_text(file_path)

    def extract_from_bytes(self, content: bytes, filename: str = "document.pdf") -> str:
        """
        Extract text from PDF bytes.

        Args:
            content: PDF file content as bytes.
            filename: Original filename (for error messages).

        Returns:
            Extracted text content.
        """
        try:
            doc = fitz.open(stream=content, filetype="pdf")
            return self._process_document(doc)
        except Exception as e:
            raise ValueError(f"Failed to parse PDF '{filename}': {e}")

    def _extract_text(self, file_path: Path) -> str:
        """Extract text from a PDF file path."""
        try:
            doc = fitz.open(file_path)
            return self._process_document(doc)
        except Exception as e:
            raise ValueError(f"Failed to parse PDF '{file_path}': {e}")

    def _process_document(self, doc: fitz.Document) -> str:
        """Process a PyMuPDF document and extract text."""
        text_parts = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")

            if text.strip():
                text_parts.append(f"--- Page {page_num + 1} ---\n{text}")

        doc.close()

        return "\n\n".join(text_parts)

    def get_metadata(self, file_path: str | Path) -> dict:
        """
        Extract metadata from a PDF file.

        Args:
            file_path: Path to the PDF file.

        Returns:
            Dictionary with metadata (title, author, etc.).
        """
        file_path = Path(file_path)
        doc = fitz.open(file_path)
        metadata = doc.metadata or {}
        doc.close()

        return {
            "title": metadata.get("title", ""),
            "author": metadata.get("author", ""),
            "subject": metadata.get("subject", ""),
            "creator": metadata.get("creator", ""),
            "producer": metadata.get("producer", ""),
            "creation_date": metadata.get("creationDate", ""),
            "modification_date": metadata.get("modDate", ""),
            "page_count": doc.page_count if hasattr(doc, "page_count") else 0,
        }


# Singleton instance
pdf_extractor = PDFExtractor()
