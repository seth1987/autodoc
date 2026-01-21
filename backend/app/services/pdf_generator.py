"""PDF generation service using Playwright for perfect rendering."""

from playwright.sync_api import sync_playwright
from concurrent.futures import ThreadPoolExecutor
import asyncio


class PDFGenerator:
    """Service for converting HTML to PDF using headless browser."""

    def __init__(self):
        self._executor = ThreadPoolExecutor(max_workers=2)

    def _generate_pdf_sync(self, html_content: str) -> bytes:
        """
        Generate PDF synchronously using Playwright.

        Args:
            html_content: Complete HTML document string.

        Returns:
            PDF file as bytes.
        """
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()

            # Set content and wait for fonts to load
            page.set_content(html_content, wait_until='networkidle')

            # Generate PDF with print settings
            pdf_bytes = page.pdf(
                format='A4',
                print_background=True,
                margin={
                    'top': '20mm',
                    'bottom': '20mm',
                    'left': '15mm',
                    'right': '15mm'
                }
            )

            browser.close()

        return pdf_bytes

    async def generate_pdf_async(self, html_content: str) -> bytes:
        """
        Generate PDF asynchronously by running sync code in thread pool.

        Args:
            html_content: Complete HTML document string.

        Returns:
            PDF file as bytes.
        """
        loop = asyncio.get_event_loop()
        pdf_bytes = await loop.run_in_executor(
            self._executor,
            self._generate_pdf_sync,
            html_content
        )
        return pdf_bytes


# Singleton instance
pdf_generator = PDFGenerator()
