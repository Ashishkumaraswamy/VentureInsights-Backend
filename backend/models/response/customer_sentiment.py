from pydantic import BaseModel
from typing import Optional, List
from .base import CitationResponse


# --- Sentiment Summary ---
class SentimentTimeSeriesPoint(BaseModel):
    period_start: str  # ISO format date string (YYYY-MM-DD)
    period_end: str  # ISO format date string (YYYY-MM-DD)
    positive: int
    negative: int
    neutral: int
    sentiment_score: float
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None


class SentimentBreakdown(BaseModel):
    positive: int
    negative: int
    neutral: int


class SentimentSummaryResponse(CitationResponse):
    company_name: str
    product: Optional[str] = None
    region: Optional[str] = None
    sentiment_score: float
    sentiment_breakdown: SentimentBreakdown
    sentiment_timeseries: List[SentimentTimeSeriesPoint]
    summary: Optional[str] = None
    sources: Optional[List[str]] = None
    last_updated: Optional[str] = None  # ISO format datetime string

    class Config:
        arbitrary_types_allowed = True


# --- Customer Feedback ---
class CustomerFeedbackItem(BaseModel):
    date: str  # ISO format date string (YYYY-MM-DD)
    customer: Optional[str] = None
    feedback: str
    sentiment: str
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None


class CustomerFeedbackResponse(CitationResponse):
    company_name: str
    product: Optional[str] = None
    region: Optional[str] = None
    feedback_items: List[CustomerFeedbackItem]
    summary: Optional[str] = None
    sources: Optional[List[str]] = None
    last_updated: Optional[str] = None  # ISO format datetime string

    class Config:
        arbitrary_types_allowed = True


# --- Brand Reputation ---
class BrandReputationTimeSeriesPoint(BaseModel):
    period_start: str  # ISO format date string (YYYY-MM-DD)
    period_end: str  # ISO format date string (YYYY-MM-DD)
    reputation_score: float
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None


class BrandReputationResponse(CitationResponse):
    company_name: str
    region: Optional[str] = None
    reputation_score: float
    reputation_timeseries: List[BrandReputationTimeSeriesPoint]
    summary: Optional[str] = None
    sources: Optional[List[str]] = None
    last_updated: Optional[str] = None  # ISO format datetime string

    class Config:
        arbitrary_types_allowed = True


# --- Sentiment Comparison ---
class CompanySentimentData(BaseModel):
    company: str
    sentiment_score: float
    strengths: List[str]
    weaknesses: List[str]


class SentimentComparisonResponse(CitationResponse):
    company_name: str
    product: Optional[str] = None
    region: Optional[str] = None
    competitors: List[str]
    target_sentiment: CompanySentimentData
    competitor_sentiments: List[CompanySentimentData]
    summary: Optional[str] = None
    confidence: float
    last_updated: str  # ISO format datetime string

    class Config:
        arbitrary_types_allowed = True
