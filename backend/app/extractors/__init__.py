"""Document extractors for PDF and DOCX files."""

from .pdf_extractor import PDFExtractor, pdf_extractor
from .docx_extractor import DOCXExtractor, docx_extractor

__all__ = [
    "PDFExtractor",
    "pdf_extractor",
    "DOCXExtractor",
    "docx_extractor",
]


def get_extractor(filename: str):
    """
    Get the appropriate extractor based on file extension.

    Args:
        filename: Name of the file.

    Returns:
        Extractor instance (PDFExtractor or DOCXExtractor).

    Raises:
        ValueError: If file type is not supported.
    """
    filename_lower = filename.lower()

    if filename_lower.endswith(".pdf"):
        return pdf_extractor
    elif filename_lower.endswith(".docx"):
        return docx_extractor
    else:
        raise ValueError(f"Unsupported file type: {filename}")
