from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


# --- Regulatory Risks ---
class RegulatoryRiskItem(BaseModel):
    risk: str
    severity: str
    description: Optional[str] = None
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None


class RegulatoryRisksResponse(BaseModel):
    company_name: str
    industry: Optional[str] = None
    region: Optional[str] = None
    risks: List[RegulatoryRiskItem]
    summary: Optional[str] = None
    sources: Optional[List[str]] = None
    last_updated: Optional[datetime] = None


# --- Market Risks ---
class MarketRiskItem(BaseModel):
    risk: str
    severity: str
    description: Optional[str] = None
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None


class MarketRisksResponse(BaseModel):
    company_name: str
    industry: Optional[str] = None
    region: Optional[str] = None
    risks: List[MarketRiskItem]
    summary: Optional[str] = None
    sources: Optional[List[str]] = None
    last_updated: Optional[datetime] = None


# --- Operational Risks ---
class OperationalRiskItem(BaseModel):
    risk: str
    severity: str
    description: Optional[str] = None
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None


class OperationalRisksResponse(BaseModel):
    company_name: str
    industry: Optional[str] = None
    region: Optional[str] = None
    risks: List[OperationalRiskItem]
    summary: Optional[str] = None
    sources: Optional[List[str]] = None
    last_updated: Optional[datetime] = None


# --- Legal Risks ---
class LegalRiskItem(BaseModel):
    risk: str
    severity: str
    description: Optional[str] = None
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None
    case_number: Optional[str] = None
    date_filed: Optional[date] = None


class LegalRisksResponse(BaseModel):
    company_name: str
    industry: Optional[str] = None
    region: Optional[str] = None
    risks: List[LegalRiskItem]
    summary: Optional[str] = None
    sources: Optional[List[str]] = None
    last_updated: Optional[datetime] = None
