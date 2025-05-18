from agno.models.message import UrlCitation
from pydantic import BaseModel, Field


class CitationResponse(BaseModel):
    citations: list[UrlCitation] = Field(
        ..., description="List of citations for the response"
    )
