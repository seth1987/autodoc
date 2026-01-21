"""Conversion orchestration service."""

from typing import Optional
from ..models import LLMConfig, ConversionResponse
from ..extractors import get_extractor
from ..config import settings
from .llm_service import llm_service
from .html_generator import html_generator


class ConversionService:
    """Orchestrate document conversion: Extract → Analyze → Generate."""

    def __init__(self):
        self.chunking_threshold = settings.chunking_threshold

    async def convert(
        self,
        file_content: bytes,
        filename: str,
        llm_config: LLMConfig
    ) -> ConversionResponse:
        """
        Convert a document to HTML.

        Args:
            file_content: File content as bytes.
            filename: Original filename.
            llm_config: LLM configuration.

        Returns:
            ConversionResponse with HTML or error.
        """
        try:
            # Step 1: Extract text
            text = self._extract_text(file_content, filename)

            if not text.strip():
                return ConversionResponse(
                    success=False,
                    error="Le document ne contient pas de texte extractible."
                )

            # Step 2: Chunk if necessary
            chunks = self._chunk_text(text)

            # Step 3: Analyze with LLM
            if len(chunks) == 1:
                doc_structure = await llm_service.analyze_document(chunks[0], llm_config)
            else:
                doc_structure = await self._analyze_chunks(chunks, llm_config)

            # Step 4: Generate HTML
            html_content = html_generator.generate(doc_structure)

            # Generate output filename
            output_filename = self._generate_output_filename(filename)

            return ConversionResponse(
                success=True,
                html=html_content,
                filename=output_filename
            )

        except ValueError as e:
            return ConversionResponse(
                success=False,
                error=f"Erreur de validation: {str(e)}"
            )
        except Exception as e:
            return ConversionResponse(
                success=False,
                error=f"Erreur lors de la conversion: {str(e)}"
            )

    def _extract_text(self, content: bytes, filename: str) -> str:
        """Extract text from file content."""
        extractor = get_extractor(filename)
        return extractor.extract_from_bytes(content, filename)

    def _chunk_text(self, text: str) -> list[str]:
        """
        Split text into chunks if it exceeds the threshold.

        Simple chunking strategy: split by double newlines (paragraphs).
        """
        # Estimate tokens (rough: 1 token ≈ 4 chars)
        estimated_tokens = len(text) / 4

        if estimated_tokens <= self.chunking_threshold:
            return [text]

        # Split into paragraphs
        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = []
        current_size = 0

        for para in paragraphs:
            para_tokens = len(para) / 4

            if current_size + para_tokens > self.chunking_threshold:
                if current_chunk:
                    chunks.append("\n\n".join(current_chunk))
                current_chunk = [para]
                current_size = para_tokens
            else:
                current_chunk.append(para)
                current_size += para_tokens

        if current_chunk:
            chunks.append("\n\n".join(current_chunk))

        return chunks

    async def _analyze_chunks(
        self,
        chunks: list[str],
        llm_config: LLMConfig
    ):
        """
        Analyze multiple chunks and merge results.

        For simplicity, we analyze each chunk separately and merge sections.
        """
        from ..models import DocumentStructure, Metadata, Section

        all_sections = []
        metadata = None
        conclusion = None
        sources = []

        for i, chunk in enumerate(chunks):
            # Add context for non-first chunks
            if i > 0:
                chunk = f"[Suite du document - Partie {i+1}/{len(chunks)}]\n\n{chunk}"

            doc = await llm_service.analyze_document(chunk, llm_config)

            # Use metadata from first chunk
            if i == 0:
                metadata = doc.metadata

            # Collect sections
            all_sections.extend(doc.sections)

            # Use conclusion from last chunk
            if i == len(chunks) - 1 and doc.conclusion:
                conclusion = doc.conclusion

            # Collect sources
            sources.extend(doc.sources)

        # Merge into final structure
        return DocumentStructure(
            metadata=metadata or Metadata(title="Document"),
            toc=True,
            sections=all_sections,
            conclusion=conclusion,
            sources=sources
        )

    def _generate_output_filename(self, input_filename: str) -> str:
        """Generate output HTML filename."""
        # Remove extension and add .html
        if "." in input_filename:
            base_name = input_filename.rsplit(".", 1)[0]
        else:
            base_name = input_filename

        return f"{base_name}_converted.html"


# Singleton instance
conversion_service = ConversionService()
