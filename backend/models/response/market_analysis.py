from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


# --- Market Trends ---
class MarketTrendTimeSeriesPoint(BaseModel):
    period_start: date
    period_end: date
    value: float
    metric: str
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None


class MarketTrendsResponse(BaseModel):
    industry: str
    region: Optional[str] = None
    trends_timeseries: List[MarketTrendTimeSeriesPoint]
    summary: Optional[str] = None
    sources: Optional[List[str]] = None
    last_updated: Optional[datetime] = None


# --- Competitive Analysis ---
class CompetitorProfile(BaseModel):
    name: str
    domain: Optional[str] = None
    market_share: Optional[float] = None
    revenue: Optional[float] = None
    growth_rate: Optional[float] = None
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None
    sources: Optional[List[str]] = None


class CompetitiveAnalysisResponse(BaseModel):
    company_name: str
    industry: Optional[str] = None
    region: Optional[str] = None
    top_competitors: List[CompetitorProfile]
    summary: Optional[str] = None
    sources: Optional[List[str]] = None
    last_updated: Optional[datetime] = None


# --- Growth Projections ---
class GrowthProjectionTimeSeriesPoint(BaseModel):
    period_start: date
    period_end: date
    projected_value: float
    metric: str
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None


class GrowthProjectionsResponse(BaseModel):
    industry: str
    region: Optional[str] = None
    projections_timeseries: List[GrowthProjectionTimeSeriesPoint]
    summary: Optional[str] = None
    sources: Optional[List[str]] = None
    last_updated: Optional[datetime] = None


# --- Regional Trends ---
class RegionalTrendPoint(BaseModel):
    region: str
    period_start: date
    period_end: date
    value: float
    metric: str
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None


class RegionalTrendsResponse(BaseModel):
    industry: str
    regional_trends: List[RegionalTrendPoint]
    summary: Optional[str] = None
    sources: Optional[List[str]] = None
    last_updated: Optional[datetime] = None
