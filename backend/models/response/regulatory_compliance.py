from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


# --- Compliance Overview ---
class RegulationItem(BaseModel):
    regulation: str
    description: Optional[str] = None
    applicable: bool
    sources: Optional[List[str]] = None


class ComplianceOverviewResponse(BaseModel):
    company_name: str
    industry: Optional[str] = None
    region: Optional[str] = None
    regulations: List[RegulationItem]
    summary: Optional[str] = None
    sources: Optional[List[str]] = None
    last_updated: Optional[datetime] = None


# --- Violation History ---
class ViolationItem(BaseModel):
    violation: str
    regulation: str
    date: date
    severity: str
    description: Optional[str] = None
    sources: Optional[List[str]] = None
    resolved: Optional[bool] = None


class ViolationHistoryResponse(BaseModel):
    company_name: str
    industry: Optional[str] = None
    region: Optional[str] = None
    violations: List[ViolationItem]
    summary: Optional[str] = None
    sources: Optional[List[str]] = None
    last_updated: Optional[datetime] = None


# --- Compliance Risk ---
class ComplianceRiskItem(BaseModel):
    risk: str
    severity: str
    description: Optional[str] = None
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None


class ComplianceRiskResponse(BaseModel):
    company_name: str
    industry: Optional[str] = None
    region: Optional[str] = None
    risks: List[ComplianceRiskItem]
    summary: Optional[str] = None
    sources: Optional[List[str]] = None
    last_updated: Optional[datetime] = None


# --- Regional Compliance ---
class RegionalComplianceItem(BaseModel):
    region: str
    regulations: List[RegulationItem]
    compliance_score: Optional[float] = None
    sources: Optional[List[str]] = None


class RegionalComplianceResponse(BaseModel):
    company_name: str
    industry: Optional[str] = None
    regional_compliance: List[RegionalComplianceItem]
    summary: Optional[str] = None
    sources: Optional[List[str]] = None
    last_updated: Optional[datetime] = None
