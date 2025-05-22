from pydantic import BaseModel
from typing import Optional

from backend.models.response.finance import (
    RevenueAnalysisResponse,
    ExpenseAnalysisResponse,
    ProfitMarginsResponse,
    ValuationEstimationResponse,
    FundingHistoryResponse,
)
from backend.models.response.linkedin_team import (
    TeamOverviewResponse,
    IndividualPerformanceResponse,
    OrgStructureResponse,
    TeamGrowthResponse,
)
from backend.models.response.market_analysis import (
    MarketTrendsResponse,
    CompetitiveAnalysisResponse,
    GrowthProjectionsResponse,
    RegionalTrendsResponse,
)
from backend.models.response.partnership_network import (
    PartnerListResponse,
    StrategicAlliancesResponse,
    NetworkStrengthResponse,
    PartnershipTrendsResponse,
)
from backend.models.response.regulatory_compliance import (
    ComplianceOverviewResponse,
    ViolationHistoryResponse,
    ComplianceRiskResponse,
    RegionalComplianceResponse,
)
from backend.models.response.customer_sentiment import (
    SentimentSummaryResponse,
    CustomerFeedbackResponse,
    BrandReputationResponse,
    SentimentComparisonResponse,
)
from backend.models.response.risk_analysis import (
    RegulatoryRisksResponse,
    MarketRisksResponse,
    OperationalRisksResponse,
    LegalRisksResponse,
)

class FinanceResponse(BaseModel):
    revenue: Optional[RevenueAnalysisResponse] = None
    expenses: Optional[ExpenseAnalysisResponse] = None
    margins: Optional[ProfitMarginsResponse] = None
    valuation: Optional[ValuationEstimationResponse] = None
    funding: Optional[FundingHistoryResponse] = None

class LinkedInTeamResponse(BaseModel):
    team_overview: Optional[TeamOverviewResponse] = None
    individual_performance: Optional[IndividualPerformanceResponse] = None
    org_structure: Optional[OrgStructureResponse] = None
    team_growth: Optional[TeamGrowthResponse] = None

class MarketAnalysisResponse(BaseModel):
    market_trends: Optional[MarketTrendsResponse] = None
    competitive_analysis: Optional[CompetitiveAnalysisResponse] = None
    growth_projections: Optional[GrowthProjectionsResponse] = None
    regional_trends: Optional[RegionalTrendsResponse] = None

class PartnershipNetworkResponse(BaseModel):
    partner_list: Optional[PartnerListResponse] = None
    strategic_alliances: Optional[StrategicAlliancesResponse] = None
    network_strength: Optional[NetworkStrengthResponse] = None
    partnership_trends: Optional[PartnershipTrendsResponse] = None

class RegulatoryComplianceResponse(BaseModel):
    compliance_overview: Optional[ComplianceOverviewResponse] = None
    violation_history: Optional[ViolationHistoryResponse] = None
    compliance_risk: Optional[ComplianceRiskResponse] = None
    regional_compliance: Optional[RegionalComplianceResponse] = None

class CustomerSentimentResponse(BaseModel):
    sentiment_summary: Optional[SentimentSummaryResponse] = None
    customer_feedback: Optional[CustomerFeedbackResponse] = None
    brand_reputation: Optional[BrandReputationResponse] = None
    sentiment_comparison: Optional[SentimentComparisonResponse] = None

class RiskAnalysisResponse(BaseModel):
    regulatory_risks: Optional[RegulatoryRisksResponse] = None
    market_risks: Optional[MarketRisksResponse] = None
    operational_risks: Optional[OperationalRisksResponse] = None
    legal_risks: Optional[LegalRisksResponse] = None

class ResearchResponse(BaseModel):
    company_name: str
    finance: Optional[FinanceResponse] = None
    linkedin_team: Optional[LinkedInTeamResponse] = None
    market_analysis: Optional[MarketAnalysisResponse] = None
    partnership_network: Optional[PartnershipNetworkResponse] = None
    regulatory_compliance: Optional[RegulatoryComplianceResponse] = None
    customer_sentiment: Optional[CustomerSentimentResponse] = None
    risk_analysis: Optional[RiskAnalysisResponse] = None
    
    