from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


# --- Team Overview ---
class TeamRoleBreakdown(BaseModel):
    role: str
    count: int
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None


class TeamOverviewResponse(BaseModel):
    company_name: str
    total_employees: int
    roles_breakdown: List[TeamRoleBreakdown]
    locations: Optional[List[str]] = None
    sources: Optional[List[str]] = None
    last_updated: Optional[datetime] = None


# --- Individual Performance ---
class IndividualPerformanceMetric(BaseModel):
    metric: str
    value: float
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None


class IndividualPerformanceResponse(BaseModel):
    company_name: str
    individual_name: str
    title: Optional[str] = None
    tenure_years: Optional[float] = None
    performance_metrics: List[IndividualPerformanceMetric]
    sources: Optional[List[str]] = None
    last_updated: Optional[datetime] = None


# --- Org Structure ---
class OrgNode(BaseModel):
    name: str
    title: str
    reports_to: Optional[str] = None
    direct_reports: Optional[List[str]] = None
    sources: Optional[List[str]] = None


class OrgStructureResponse(BaseModel):
    company_name: str
    org_chart: List[OrgNode]
    sources: Optional[List[str]] = None
    last_updated: Optional[datetime] = None


# --- Team Growth ---
class TeamGrowthTimeSeriesPoint(BaseModel):
    period_start: date
    period_end: date
    hires: int
    attrition: int
    net_growth: int
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None


class TeamGrowthResponse(BaseModel):
    company_name: str
    team_growth_timeseries: List[TeamGrowthTimeSeriesPoint]
    total_hires: int
    total_attrition: int
    net_growth: int
    sources: Optional[List[str]] = None
    last_updated: Optional[datetime] = None
