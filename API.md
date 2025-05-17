# API Documentation

This document describes the request and response models for all endpoints in the Venture Insights MCP system. For each POST endpoint, a sample request JSON is provided.

---

## Finance Agent

### /finance/revenue-analysis
**Request Model:**
```python
class RevenueAnalysisRequest(BaseModel):
    company_name: str
    domain: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    granularity: Optional[str] = "year"  # year, quarter, or month
```
**Sample Request JSON:**
```json
{
  "company_name": "TechNova Inc.",
  "domain": "tecnova.com",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "granularity": "quarter"
}
```
**Response Model:**
```python
class RevenueAnalysisResponse(BaseModel):
    company_name: str
    currency: str
    revenue_timeseries: List[RevenueTimeSeriesPoint]
    total_revenue: Optional[float] = None
    last_updated: Optional[datetime] = None
```

---

### /finance/expense-analysis
**Request Model:**
```python
class ExpenseAnalysisRequest(BaseModel):
    company_name: str
    domain: Optional[str] = None
    year: Optional[int] = None
    category: Optional[str] = None
```
**Sample Request JSON:**
```json
{
  "company_name": "TechNova Inc.",
  "domain": "tecnova.com",
  "year": 2023,
  "category": "R&D"
}
```
**Response Model:**
```python
class ExpenseAnalysisResponse(BaseModel):
    company_name: str
    year: Optional[int] = None
    expenses: List[ExpenseCategoryBreakdown]
    expense_timeseries: List[ExpenseTimeSeriesPoint]
    total_expense: float
    currency: str
    last_updated: Optional[datetime] = None
```

---

### /finance/profit-margins
**Request Model:**
```python
class ProfitMarginsRequest(BaseModel):
    company_name: str
    domain: Optional[str] = None
    year: Optional[int] = None
```
**Sample Request JSON:**
```json
{
  "company_name": "TechNova Inc.",
  "domain": "tecnova.com",
  "year": 2023
}
```
**Response Model:**
```python
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
```

---

### /finance/valuation-estimation
**Request Model:**
```python
class ValuationEstimationRequest(BaseModel):
    company_name: str
    domain: Optional[str] = None
    as_of_date: Optional[date] = None
```
**Sample Request JSON:**
```json
{
  "company_name": "TechNova Inc.",
  "domain": "tecnova.com",
  "as_of_date": "2024-05-01"
}
```
**Response Model:**
```python
class ValuationEstimationResponse(BaseModel):
    company_name: str
    valuation: float
    currency: str
    as_of_date: Optional[date] = None
    valuation_timeseries: List[ValuationTimeSeriesPoint]
    sources: Optional[List[str]] = None
    confidence: Optional[float] = None
    last_updated: Optional[datetime] = None
```

---

### /finance/funding-history
**Request Model:**
```python
class FundingHistoryRequest(BaseModel):
    company_name: str
    domain: Optional[str] = None
```
**Sample Request JSON:**
```json
{
  "company_name": "TechNova Inc.",
  "domain": "tecnova.com"
}
```
**Response Model:**
```python
class FundingHistoryResponse(BaseModel):
    company_name: str
    funding_rounds: List[FundingRound]
    funding_cumulative_timeseries: List[FundingCumulativeTimeSeriesPoint]
    total_funding: float
    currency: str
    last_updated: Optional[datetime] = None
```

---

# (The rest of the agents and endpoints will follow the same format. This file will be continued to include all request/response models and sample POST request JSONs for each endpoint.) 