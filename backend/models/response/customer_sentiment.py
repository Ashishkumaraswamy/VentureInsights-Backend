from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


# --- Sentiment Summary ---
class SentimentTimeSeriesPoint(BaseModel):
    period_start: date
    period_end: date
    positive: int
    negative: int
    neutral: int
    sentiment_score: float
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None


class SentimentSummaryResponse(BaseModel):
    company_name: str
    product: Optional[str] = None
    region: Optional[str] = None
    sentiment_score: float
    sentiment_breakdown: dict
    sentiment_timeseries: List[SentimentTimeSeriesPoint]
    summary: Optional[str] = None
    sources: Optional[List[str]] = None
    last_updated: Optional[datetime] = None


# --- Customer Feedback ---
class CustomerFeedbackItem(BaseModel):
    date: date
    customer: Optional[str] = None
    feedback: str
    sentiment: str
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None


class CustomerFeedbackResponse(BaseModel):
    company_name: str
    product: Optional[str] = None
    region: Optional[str] = None
    feedback_items: List[CustomerFeedbackItem]
    summary: Optional[str] = None
    sources: Optional[List[str]] = None
    last_updated: Optional[datetime] = None


# --- Brand Reputation ---
class BrandReputationTimeSeriesPoint(BaseModel):
    period_start: date
    period_end: date
    reputation_score: float
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None


class BrandReputationResponse(BaseModel):
    company_name: str
    region: Optional[str] = None
    reputation_score: float
    reputation_timeseries: List[BrandReputationTimeSeriesPoint]
    summary: Optional[str] = None
    sources: Optional[List[str]] = None
    last_updated: Optional[datetime] = None
