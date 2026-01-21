"""Pydantic models for AutoDoc."""

from pydantic import BaseModel, Field
from typing import Optional, Literal
from enum import Enum


# === LLM Configuration ===

class LLMProvider(str, Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    CUSTOM = "custom"


class OutputFormat(str, Enum):
    """Supported output formats."""
    HTML = "html"
    PDF = "pdf"


class LLMConfig(BaseModel):
    """LLM configuration from client."""
    provider: LLMProvider
    api_key: str
    model: str = "gpt-4"
    base_url: Optional[str] = None  # For custom providers (LM Studio, Ollama)


# === Document Structure (LLM Response) ===

class Metadata(BaseModel):
    """Document metadata."""
    title: str
    subtitle: Optional[str] = None
    phase: Optional[str] = None
    brand: Optional[str] = None
    tagline: Optional[str] = None
    date: Optional[str] = None


class CalloutVariant(str, Enum):
    """Types of callout boxes."""
    NOTE = "note"
    SUCCESS = "success"
    WARNING = "warning"
    ALERT = "alert"
    INFO = "info"


class ListStyle(str, Enum):
    """Types of lists."""
    BULLET = "bullet"
    NUMBERED = "numbered"
    CHECKLIST = "checklist"


class ListItem(BaseModel):
    """Item in a list."""
    text: str
    checked: Optional[Literal["true", "false", "cross"]] = None


class TimelineItem(BaseModel):
    """Item in a timeline."""
    title: str
    description: str


class StatItem(BaseModel):
    """Item in stats block."""
    value: str
    label: str


class CardItem(BaseModel):
    """Item in cards grid."""
    title: str
    content: str


class TableData(BaseModel):
    """Table structure."""
    headers: list[str]
    rows: list[list[str]]


# === Content Blocks ===

class ParagraphBlock(BaseModel):
    """Paragraph content block."""
    type: Literal["paragraph"] = "paragraph"
    text: str


class CalloutBlock(BaseModel):
    """Callout/note content block."""
    type: Literal["callout"] = "callout"
    variant: CalloutVariant
    title: Optional[str] = None
    content: str


class ListBlock(BaseModel):
    """List content block."""
    type: Literal["list"] = "list"
    style: ListStyle
    items: list[ListItem]


class TableBlock(BaseModel):
    """Table content block."""
    type: Literal["table"] = "table"
    headers: list[str]
    rows: list[list[str]]


class QuoteBlock(BaseModel):
    """Quote content block."""
    type: Literal["quote"] = "quote"
    text: str


class TimelineBlock(BaseModel):
    """Timeline content block."""
    type: Literal["timeline"] = "timeline"
    items: list[TimelineItem]


class StatsBlock(BaseModel):
    """Stats content block."""
    type: Literal["stats"] = "stats"
    items: list[StatItem]


class CardsBlock(BaseModel):
    """Cards grid content block."""
    type: Literal["cards"] = "cards"
    items: list[CardItem]


class TwoColContent(BaseModel):
    """Content for a column."""
    title: str
    content: list[dict]  # Simplified: list of content blocks


class TwoColBlock(BaseModel):
    """Two-column layout content block."""
    type: Literal["two-col"] = "two-col"
    left: TwoColContent
    right: TwoColContent


class HeadingBlock(BaseModel):
    """Heading content block."""
    type: Literal["heading"] = "heading"
    level: int = Field(ge=1, le=4)
    text: str


# Union type for all content blocks
ContentBlock = (
    ParagraphBlock
    | CalloutBlock
    | ListBlock
    | TableBlock
    | QuoteBlock
    | TimelineBlock
    | StatsBlock
    | CardsBlock
    | TwoColBlock
    | HeadingBlock
)


# === Document Sections ===

class Section(BaseModel):
    """Document section."""
    type: Literal["section"] = "section"
    title: str
    content: list[dict]  # List of content blocks (parsed dynamically)


class ConclusionSection(BaseModel):
    """Conclusion section with subsections."""
    title: str
    summary: Optional[str] = None
    sections: list[dict] = []  # {title: str, items: list[str]}


class Source(BaseModel):
    """Source/reference entry."""
    title: str
    url: Optional[str] = None
    meta: Optional[str] = None


# === Full Document Structure ===

class DocumentStructure(BaseModel):
    """Complete document structure returned by LLM."""
    metadata: Metadata
    toc: bool = True
    sections: list[Section]
    conclusion: Optional[ConclusionSection] = None
    sources: list[Source] = []


# === API Request/Response ===

class ConversionRequest(BaseModel):
    """Request to convert a document."""
    llm_config: LLMConfig


class ConversionResponse(BaseModel):
    """Response with converted document."""
    success: bool
    html: Optional[str] = None
    pdf_base64: Optional[str] = None
    error: Optional[str] = None
    filename: Optional[str] = None
    format: str = "html"


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str = "1.0.0"
