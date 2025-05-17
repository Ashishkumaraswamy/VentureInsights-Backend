from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


class MarketTrendsRequest(BaseModel):
    industry: str = Field(...)
    region: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class CompetitiveAnalysisRequest(BaseModel):
    company_name: str = Field(...)
    domain: Optional[str] = None
    industry: Optional[str] = None
    region: Optional[str] = None


class GrowthProjectionsRequest(BaseModel):
    industry: str = Field(...)
    region: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class RegionalTrendsRequest(BaseModel):
    industry: str = Field(...)
    regions: Optional[List[str]] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
