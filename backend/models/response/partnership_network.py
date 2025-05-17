from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


# --- Partner List ---
class PartnerItem(BaseModel):
    name: str
    domain: Optional[str] = None
    partnership_type: Optional[str] = None
    since: Optional[date] = None
    sources: Optional[List[str]] = None


class PartnerListResponse(BaseModel):
    company_name: str
    partners: List[PartnerItem]
    summary: Optional[str] = None
    sources: Optional[List[str]] = None
    last_updated: Optional[datetime] = None


# --- Strategic Alliances ---
class AllianceImpactItem(BaseModel):
    partner: str
    impact_area: str
    impact_score: float
    description: Optional[str] = None
    sources: Optional[List[str]] = None


class StrategicAlliancesResponse(BaseModel):
    company_name: str
    alliances: List[AllianceImpactItem]
    summary: Optional[str] = None
    sources: Optional[List[str]] = None
    last_updated: Optional[datetime] = None


# --- Network Strength ---
class NetworkMetricItem(BaseModel):
    metric: str
    value: float
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None


class NetworkStrengthResponse(BaseModel):
    company_name: str
    network_metrics: List[NetworkMetricItem]
    summary: Optional[str] = None
    sources: Optional[List[str]] = None
    last_updated: Optional[datetime] = None


# --- Partnership Trends ---
class PartnershipTrendTimeSeriesPoint(BaseModel):
    period_start: date
    period_end: date
    new_partnerships: int
    ended_partnerships: int
    net_growth: int
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None


class PartnershipTrendsResponse(BaseModel):
    company_name: str
    partnership_trends_timeseries: List[PartnershipTrendTimeSeriesPoint]
    summary: Optional[str] = None
    sources: Optional[List[str]] = None
    last_updated: Optional[datetime] = None
