"""LLM service for document analysis - Multi-provider support."""

import httpx
import json
from typing import Optional
from ..models import LLMConfig, LLMProvider, DocumentStructure
from ..config import settings


# System prompt for document analysis
ANALYSIS_PROMPT = """Tu es un analyseur de documents expert. Analyse le texte suivant et retourne une structure JSON représentant le document.

**Format de sortie STRICT** :
```json
{
  "metadata": {
    "title": "string",
    "subtitle": "string | null",
    "phase": "string | null",
    "brand": "string | null",
    "tagline": "string | null",
    "date": "string | null"
  },
  "toc": true,
  "sections": [
    {
      "type": "section",
      "title": "string",
      "content": [
        { "type": "paragraph", "text": "string" },
        { "type": "callout", "variant": "note|success|warning|alert|info", "title": "string | null", "content": "string" },
        { "type": "list", "style": "bullet|numbered|checklist", "items": [{ "text": "string", "checked": "true|false|cross" }] },
        { "type": "table", "headers": ["string"], "rows": [["string"]] },
        { "type": "quote", "text": "string" },
        { "type": "timeline", "items": [{ "title": "string", "description": "string" }] },
        { "type": "stats", "items": [{ "value": "string", "label": "string" }] },
        { "type": "cards", "items": [{ "title": "string", "content": "string" }] },
        { "type": "two-col", "left": { "title": "string", "content": [...] }, "right": { "title": "string", "content": [...] } },
        { "type": "heading", "level": 3, "text": "string" }
      ]
    }
  ],
  "conclusion": {
    "title": "string",
    "summary": "string",
    "sections": [
      { "title": "string", "items": ["string"] }
    ]
  },
  "sources": [
    { "title": "string", "url": "string | null", "meta": "string | null" }
  ]
}
```

**Règles d'analyse** :
1. Détecte les métadonnées depuis le début du document (titre principal, sous-titres, dates, auteur/marque)
2. Identifie la hiérarchie : H1 = sections principales, H2 = sous-sections, H3/H4 = sous-sous-sections
3. Détecte les callouts via le contexte sémantique :
   - "Important", "À noter", "Note" → note
   - "Point fort", "Validé", "✓", "Avantage" → success
   - "Attention", "Vigilance", "À surveiller" → warning
   - "Danger", "Critique", "Alerte", "⚠️", "✗" → alert
   - "Info", "Contexte", "Pour information" → info
4. Numérote les sections automatiquement (01, 02, 03...)
5. Préserve le formatage inline avec **gras** et *italique*
6. Détecte les listes à puces vs numérotées vs checklists (✓/✗)
7. Identifie les tableaux et préserve leur structure
8. Repère les citations (guillemets, retrait, style différent)
9. Détecte les chronologies/timelines (étapes séquentielles, phases)
10. Identifie les blocs de statistiques (chiffres clés mis en avant)
11. Regroupe la conclusion (généralement en fin de document)
12. Extrait les sources/références si présentes

Retourne UNIQUEMENT le JSON valide, sans commentaires ni explications."""


class LLMService:
    """Service for calling LLM APIs."""

    def __init__(self):
        self.timeout = settings.llm_timeout_seconds

    async def analyze_document(
        self,
        text: str,
        config: LLMConfig
    ) -> DocumentStructure:
        """
        Analyze document text using the configured LLM.

        Args:
            text: Extracted document text.
            config: LLM configuration (provider, api_key, model).

        Returns:
            Parsed DocumentStructure.

        Raises:
            ValueError: If LLM response is invalid.
            httpx.HTTPError: If API call fails.
        """
        if config.provider == LLMProvider.OPENAI:
            response = await self._call_openai(text, config)
        elif config.provider == LLMProvider.ANTHROPIC:
            response = await self._call_anthropic(text, config)
        elif config.provider == LLMProvider.CUSTOM:
            response = await self._call_custom(text, config)
        else:
            raise ValueError(f"Unsupported provider: {config.provider}")

        return self._parse_response(response)

    async def _call_openai(self, text: str, config: LLMConfig) -> str:
        """Call OpenAI API."""
        url = "https://api.openai.com/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": config.model,
            "messages": [
                {"role": "system", "content": ANALYSIS_PROMPT},
                {"role": "user", "content": f"Document à analyser :\n---\n{text}\n---"},
            ],
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()

        data = response.json()
        return data["choices"][0]["message"]["content"]

    async def _call_anthropic(self, text: str, config: LLMConfig) -> str:
        """Call Anthropic API."""
        url = "https://api.anthropic.com/v1/messages"

        headers = {
            "x-api-key": config.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        payload = {
            "model": config.model,
            "max_tokens": 8192,
            "system": ANALYSIS_PROMPT,
            "messages": [
                {"role": "user", "content": f"Document à analyser :\n---\n{text}\n---"},
            ],
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()

        data = response.json()
        return data["content"][0]["text"]

    async def _call_custom(self, text: str, config: LLMConfig) -> str:
        """Call custom OpenAI-compatible API (LM Studio, Ollama, etc.)."""
        if not config.base_url:
            raise ValueError("base_url is required for custom provider")

        url = f"{config.base_url.rstrip('/')}/v1/chat/completions"

        headers = {
            "Content-Type": "application/json",
        }

        # Add API key if provided (some local servers don't need it)
        if config.api_key and config.api_key != "none":
            headers["Authorization"] = f"Bearer {config.api_key}"

        payload = {
            "model": config.model,
            "messages": [
                {"role": "system", "content": ANALYSIS_PROMPT},
                {"role": "user", "content": f"Document à analyser :\n---\n{text}\n---"},
            ],
            "temperature": 0.1,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()

        data = response.json()
        return data["choices"][0]["message"]["content"]

    def _parse_response(self, response: str) -> DocumentStructure:
        """Parse LLM response into DocumentStructure."""
        # Clean response (remove markdown code blocks if present)
        cleaned = response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response from LLM: {e}")

        # Validate with Pydantic
        try:
            return DocumentStructure(**data)
        except Exception as e:
            raise ValueError(f"Invalid document structure from LLM: {e}")


# Singleton instance
llm_service = LLMService()
