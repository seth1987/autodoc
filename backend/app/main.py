"""FastAPI application for AutoDoc."""

import json
import base64
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, Response

from .config import settings
from .models import LLMConfig, LLMProvider, OutputFormat, ConversionResponse, HealthResponse
from .services.converter import conversion_service
from .services.pdf_generator import pdf_generator


# Create FastAPI app
app = FastAPI(
    title="AutoDoc API",
    description="Convert PDF/DOCX documents to professional HTML reports",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=JSONResponse)
async def root():
    """Root endpoint with API info."""
    return {
        "name": settings.app_name,
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "convert": "/convert",
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", version="1.0.0")


@app.post("/convert", response_model=ConversionResponse)
async def convert_document(
    file: UploadFile = File(...),
    llm_config: str = Form(...),
    output_format: str = Form("html"),
):
    """
    Convert a document to HTML or PDF.

    Args:
        file: Uploaded PDF or DOCX file.
        llm_config: JSON string with LLM configuration.
        output_format: Output format ('html' or 'pdf').

    Returns:
        ConversionResponse with HTML/PDF content or error.
    """
    # Validate output format
    try:
        fmt = OutputFormat(output_format.lower())
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Format de sortie invalide. Utilisez 'html' ou 'pdf'."
        )

    # Validate file type
    allowed_extensions = settings.allowed_extensions.split(",")
    file_ext = file.filename.lower().split(".")[-1] if file.filename else ""

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Type de fichier non supporté. Extensions autorisées: {', '.join(allowed_extensions)}"
        )

    # Validate file size
    content = await file.read()
    max_size_bytes = settings.max_file_size_mb * 1024 * 1024

    if len(content) > max_size_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"Fichier trop volumineux. Taille max: {settings.max_file_size_mb}MB"
        )

    # Parse LLM config
    try:
        config_data = json.loads(llm_config)
        config = LLMConfig(**config_data)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Configuration LLM invalide (JSON mal formé)"
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Configuration LLM invalide: {str(e)}"
        )

    # Validate API key is provided (except for custom provider where it's optional)
    if config.provider != LLMProvider.CUSTOM:
        if not config.api_key or config.api_key == "" or config.api_key == "none":
            raise HTTPException(
                status_code=400,
                detail="Clé API requise"
            )

    # Validate custom provider has base_url
    if config.provider == LLMProvider.CUSTOM and not config.base_url:
        raise HTTPException(
            status_code=400,
            detail="URL de base requise pour le provider custom"
        )

    # Convert document to HTML
    result = await conversion_service.convert(
        file_content=content,
        filename=file.filename or "document",
        llm_config=config
    )

    # If PDF requested and HTML conversion succeeded, generate PDF
    if fmt == OutputFormat.PDF and result.success and result.html:
        try:
            pdf_bytes = pdf_generator.generate_pdf(result.html)
            pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
            result.pdf_base64 = pdf_base64
            result.format = "pdf"
            result.filename = result.filename.replace('.html', '.pdf') if result.filename else "document.pdf"
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de la génération du PDF: {str(e)}"
            )

    return result


@app.post("/convert/download")
async def convert_and_download(
    file: UploadFile = File(...),
    llm_config: str = Form(...),
):
    """
    Convert a document and return HTML as downloadable file.

    Same as /convert but returns the HTML directly for download.
    """
    # Use the same logic as convert_document
    allowed_extensions = settings.allowed_extensions.split(",")
    file_ext = file.filename.lower().split(".")[-1] if file.filename else ""

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Type de fichier non supporté. Extensions autorisées: {', '.join(allowed_extensions)}"
        )

    content = await file.read()
    max_size_bytes = settings.max_file_size_mb * 1024 * 1024

    if len(content) > max_size_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"Fichier trop volumineux. Taille max: {settings.max_file_size_mb}MB"
        )

    try:
        config_data = json.loads(llm_config)
        config = LLMConfig(**config_data)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Configuration LLM invalide: {str(e)}"
        )

    if not config.api_key:
        raise HTTPException(status_code=400, detail="Clé API requise")

    if config.provider == LLMProvider.CUSTOM and not config.base_url:
        raise HTTPException(status_code=400, detail="URL de base requise pour provider custom")

    result = await conversion_service.convert(
        file_content=content,
        filename=file.filename or "document",
        llm_config=config
    )

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    # Return HTML as response
    return HTMLResponse(
        content=result.html,
        headers={
            "Content-Disposition": f"attachment; filename={result.filename}"
        }
    )


# Run with: uvicorn backend.app.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
