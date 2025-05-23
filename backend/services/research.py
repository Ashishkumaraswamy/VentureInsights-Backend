from agno.models.message import UrlCitation

from backend.services.finance import FinanceService
from backend.services.linkedin_team import LinkedInTeamService
from backend.services.market_analysis import MarketAnalysisService
from backend.services.partnership_network import PartnershipNetworkService
from backend.services.customer_sentiment import CustomerSentimentService
from backend.services.regulatory_compliance import RegulatoryComplianceService
from backend.services.risk_analysis import RiskAnalysisService
from backend.models.response.research import (
    ResearchResponse,
    FinanceResponse,
    LinkedInTeamResponse,
    MarketAnalysisResponse,
    PartnershipNetworkResponse,
    RegulatoryComplianceResponse,
    CustomerSentimentResponse,
    RiskAnalysisResponse,
)
from datetime import datetime
from backend.models.response.finance import (
    RevenueAnalysisResponse,
    RevenueTimeSeriesPoint,
)
from backend.models.response.linkedin_team import (
    TeamOverviewResponse,
    TeamRoleBreakdown,
)
from backend.models.response.market_analysis import MarketTrendsResponse, MarketSize
from backend.models.response.partnership_network import PartnerListResponse, PartnerItem
from backend.models.response.regulatory_compliance import (
    ComplianceOverviewResponse,
    RegulationItem,
)
from backend.models.response.customer_sentiment import (
    SentimentSummaryResponse,
    SentimentBreakdown,
    SentimentTimeSeriesPoint,
)
from backend.models.response.risk_analysis import RegulatoryRisksResponse


class ResearchService:
    def __init__(
        self,
        finance_service: FinanceService,
        linkedin_team_service: LinkedInTeamService,
        market_analysis_service: MarketAnalysisService,
        partnership_network_service: PartnershipNetworkService,
        customer_sentiment_service: CustomerSentimentService,
        regulatory_compliance_service: RegulatoryComplianceService,
        risk_analysis_service: RiskAnalysisService,
    ):
        self.finance_service = finance_service
        self.linkedin_team_service = linkedin_team_service
        self.market_analysis_service = market_analysis_service
        self.partnership_network_service = partnership_network_service
        self.customer_sentiment_service = customer_sentiment_service
        self.regulatory_compliance_service = regulatory_compliance_service
        self.risk_analysis_service = risk_analysis_service

    async def get_research(self, company_name: str, use_knowledge_base: bool = False):
        # Mock data for demonstration
        sample_citations = [
            UrlCitation(url="https://example.com/citation1", title="Sample Citation 1"),
            UrlCitation(url="https://example.com/citation2", title="Sample Citation 2"),
        ]
        return ResearchResponse(
            company_name=company_name,
            finance=FinanceResponse(
                revenue=RevenueAnalysisResponse(
                    company_name=company_name,
                    revenue_timeseries=[
                        RevenueTimeSeriesPoint(
                            currency="USD",
                            period_start="2023-01-01",
                            period_end="2023-12-31",
                            value=1000000.0,
                            sources=["https://finance.example.com"],
                            confidence=0.9,
                        )
                    ],
                    total_revenue=1000000.0,
                    last_updated=datetime.now().isoformat(),
                    citations=sample_citations,
                ),
                expenses=None,
                margins=None,
                valuation=None,
                funding=None,
            ),
            linkedin_team=LinkedInTeamResponse(
                team_overview=TeamOverviewResponse(
                    company_name=company_name,
                    company_description="A leading tech company.",
                    total_employees=200,
                    roles_breakdown=[
                        TeamRoleBreakdown(role="Engineer", count=100, percentage=50.0)
                    ],
                    locations=["San Francisco", "New York"],
                    key_hiring_areas=["AI", "Cloud"],
                    growth_rate=0.15,
                    sources=["https://linkedin.com/company/example"],
                    last_updated=datetime.now().isoformat(),
                ),
                individual_performance=None,
                org_structure=None,
                team_growth=None,
            ),
            market_analysis=MarketAnalysisResponse(
                market_trends=MarketTrendsResponse(
                    market_size=[
                        MarketSize(
                            percentage=40.0,
                            industry="Cloud Computing",
                            sources=["https://market.example.com"],
                            confidence=0.8,
                        )
                    ],
                    summary="Cloud market is growing rapidly.",
                    last_updated=datetime.now().isoformat(),
                    citations=sample_citations,
                ),
                competitive_analysis=None,
                growth_projections=None,
                regional_trends=None,
            ),
            partnership_network=PartnershipNetworkResponse(
                partner_list=PartnerListResponse(
                    company_name=company_name,
                    partners=[
                        PartnerItem(
                            name="PartnerX",
                            domain="partnerx.com",
                            partnership_type="Technology",
                            since=datetime(2022, 1, 1).date(),
                            sources=["https://partners.example.com"],
                        )
                    ],
                    summary="Strong partnership with PartnerX.",
                    sources=["https://partners.example.com"],
                    last_updated=datetime.now(),
                ),
                strategic_alliances=None,
                network_strength=None,
                partnership_trends=None,
            ),
            regulatory_compliance=RegulatoryComplianceResponse(
                compliance_overview=ComplianceOverviewResponse(
                    company_name=company_name,
                    industry="Technology",
                    region="Global",
                    regulations=[
                        RegulationItem(
                            regulation="GDPR",
                            description="EU data privacy regulation.",
                            applicable=True,
                            sources=["https://gdpr.eu/"],
                        )
                    ],
                    summary="Compliant with GDPR.",
                    sources=["https://gdpr.eu/"],
                    last_updated=datetime.now(),
                    citations=sample_citations,
                ),
                violation_history=None,
                compliance_risk=None,
                regional_compliance=None,
            ),
            customer_sentiment=CustomerSentimentResponse(
                sentiment_summary=SentimentSummaryResponse(
                    company_name=company_name,
                    product="Main Product",
                    region="Global",
                    sentiment_score=0.85,
                    sentiment_breakdown=SentimentBreakdown(
                        positive=80, negative=10, neutral=10
                    ),
                    sentiment_timeseries=[
                        SentimentTimeSeriesPoint(
                            period_start="2023-01-01",
                            period_end="2023-12-31",
                            positive=80,
                            negative=10,
                            neutral=10,
                            sentiment_score=0.85,
                            sources=["https://reviews.example.com"],
                            confidence=0.9,
                        )
                    ],
                    summary="Mostly positive sentiment.",
                    sources=["https://reviews.example.com"],
                    last_updated=datetime.now().isoformat(),
                    citations=sample_citations,
                ),
                customer_feedback=None,
                brand_reputation=None,
                sentiment_comparison=None,
            ),
            risk_analysis=RiskAnalysisResponse(
                regulatory_risks=RegulatoryRisksResponse(
                    company_name=company_name,
                    industry="Technology",
                    region="Global",
                    risks=[
                        {
                            "risk": "GDPR Non-compliance",
                            "severity": "High",
                            "description": "Potential non-compliance with EU data privacy laws.",
                            "sources": ["https://gdpr.eu/"],
                            "confidence": 0.85,
                        }
                    ],
                    summary="Key regulatory risk is GDPR.",
                    sources=["https://gdpr.eu/"],
                    last_updated=datetime.now().isoformat(),
                    citations=sample_citations,
                ),
                market_risks=None,
                operational_risks=None,
                legal_risks=None,
            ),
        )
