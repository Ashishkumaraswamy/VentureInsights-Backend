from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


# --- Revenue Analysis ---
class RevenueTimeSeriesPoint(BaseModel):
    period_start: date
    period_end: date
    value: float
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None


class RevenueAnalysisResponse(BaseModel):
    company_name: str
    currency: str
    revenue_timeseries: List[RevenueTimeSeriesPoint]
    total_revenue: Optional[float] = None
    last_updated: Optional[datetime] = None


# --- Expense Analysis ---
class ExpenseTimeSeriesPoint(BaseModel):
    period_start: date
    period_end: date
    category: str
    value: float
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None


class ExpenseCategoryBreakdown(BaseModel):
    category: str
    amount: float
    currency: str
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None


class ExpenseAnalysisResponse(BaseModel):
    company_name: str
    year: Optional[int] = None
    expenses: List[ExpenseCategoryBreakdown]
    expense_timeseries: List[ExpenseTimeSeriesPoint]
    total_expense: float
    currency: str
    last_updated: Optional[datetime] = None


# --- Profit Margins ---
class ProfitMarginTimeSeriesPoint(BaseModel):
    period_start: date
    period_end: date
    gross_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    net_margin: Optional[float] = None
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None


class ProfitMarginsResponse(BaseModel):
    company_name: str
    year: Optional[int] = None
    gross_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    net_margin: Optional[float] = None
    margin_timeseries: List[ProfitMarginTimeSeriesPoint]
    currency: str
    sources: Optional[List[str]] = None
    last_updated: Optional[datetime] = None


# --- Valuation Estimation ---
class ValuationTimeSeriesPoint(BaseModel):
    as_of_date: date
    valuation: float
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None


class ValuationEstimationResponse(BaseModel):
    company_name: str
    valuation: float
    currency: str
    as_of_date: Optional[date] = None
    valuation_timeseries: List[ValuationTimeSeriesPoint]
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None
    last_updated: Optional[datetime] = None


# --- Funding History ---
class FundingRound(BaseModel):
    round_type: str
    amount: float
    currency: str
    date: Optional[date] = None
    lead_investors: Optional[List[str]] = None
    sources: Optional[List[str]] = None


class FundingCumulativeTimeSeriesPoint(BaseModel):
    date: date
    cumulative_amount: float
    sources: Optional[List[str]] = None


class FundingHistoryResponse(BaseModel):
    company_name: str
    funding_rounds: List[FundingRound]
    funding_cumulative_timeseries: List[FundingCumulativeTimeSeriesPoint]
    total_funding: float
    currency: str
    last_updated: Optional[datetime] = None
