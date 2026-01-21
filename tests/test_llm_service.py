"""Tests for LLM service."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock


class TestLLMService:
    """Tests for LLM service."""

    def test_llm_service_import(self):
        """Test that LLM service can be imported."""
        from backend.app.services.llm_service import llm_service
        assert llm_service is not None

    def test_parse_response_valid_json(self):
        """Test parsing valid JSON response."""
        from backend.app.services.llm_service import LLMService

        service = LLMService()

        valid_json = '''
        {
            "metadata": {"title": "Test Document"},
            "toc": true,
            "sections": [],
            "conclusion": null,
            "sources": []
        }
        '''

        result = service._parse_response(valid_json)
        assert result.metadata.title == "Test Document"
        assert result.toc is True

    def test_parse_response_with_code_blocks(self):
        """Test parsing JSON wrapped in code blocks."""
        from backend.app.services.llm_service import LLMService

        service = LLMService()

        wrapped_json = '''```json
        {
            "metadata": {"title": "Test"},
            "toc": true,
            "sections": [],
            "sources": []
        }
        ```'''

        result = service._parse_response(wrapped_json)
        assert result.metadata.title == "Test"

    def test_parse_response_invalid_json(self):
        """Test that invalid JSON raises error."""
        from backend.app.services.llm_service import LLMService

        service = LLMService()

        with pytest.raises(ValueError, match="Invalid JSON"):
            service._parse_response("not valid json")

    def test_parse_response_invalid_structure(self):
        """Test that invalid structure raises error."""
        from backend.app.services.llm_service import LLMService

        service = LLMService()

        # Valid JSON but missing required fields
        with pytest.raises(ValueError, match="Invalid document structure"):
            service._parse_response('{"foo": "bar"}')


class TestLLMConfig:
    """Tests for LLM configuration."""

    def test_llm_config_openai(self):
        """Test OpenAI config."""
        from backend.app.models import LLMConfig, LLMProvider

        config = LLMConfig(
            provider=LLMProvider.OPENAI,
            api_key="sk-test",
            model="gpt-4"
        )

        assert config.provider == LLMProvider.OPENAI
        assert config.api_key == "sk-test"
        assert config.model == "gpt-4"
        assert config.base_url is None

    def test_llm_config_custom(self):
        """Test custom provider config."""
        from backend.app.models import LLMConfig, LLMProvider

        config = LLMConfig(
            provider=LLMProvider.CUSTOM,
            api_key="none",
            model="local-model",
            base_url="http://localhost:1234"
        )

        assert config.provider == LLMProvider.CUSTOM
        assert config.base_url == "http://localhost:1234"
