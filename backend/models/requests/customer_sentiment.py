from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class SentimentSummaryRequest(BaseModel):
    company_name: str = Field(...)
    domain: Optional[str] = None
    product: Optional[str] = None
    region: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class CustomerFeedbackRequest(BaseModel):
    company_name: str = Field(...)
    domain: Optional[str] = None
    product: Optional[str] = None
    region: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class BrandReputationRequest(BaseModel):
    company_name: str = Field(...)
    domain: Optional[str] = None
    region: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
