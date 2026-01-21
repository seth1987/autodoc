"""PDF generation service using WeasyPrint."""

from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import io


class PDFGenerator:
    """Service for converting HTML to PDF."""

    def __init__(self):
        self.font_config = FontConfiguration()

    def generate_pdf(self, html_content: str) -> bytes:
        """
        Convert HTML content to PDF.

        Args:
            html_content: Complete HTML document string.

        Returns:
            PDF file as bytes.
        """
        html = HTML(string=html_content)

        pdf_buffer = io.BytesIO()
        html.write_pdf(
            pdf_buffer,
            font_config=self.font_config
        )

        pdf_buffer.seek(0)
        return pdf_buffer.read()


# Singleton instance
pdf_generator = PDFGenerator()
