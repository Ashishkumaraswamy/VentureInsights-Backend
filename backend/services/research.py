from agno.models.message import UrlCitation
from backend.utils.cache_decorator import cacheable

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
    ExpenseAnalysisResponse,
    ExpenseCategoryBreakdown,
    ProfitMarginsResponse,
    ProfitMarginBreakdown,
    ValuationEstimationResponse,
    FundingHistoryResponse,
    FundingRound,
    ValuationTimeSeriesPoint,
)
from backend.models.response.linkedin_team import (
    TeamOverviewResponse,
    TeamRoleBreakdown,
    IndividualPerformanceResponse,
    IndividualPerformanceMetric,
    PreviousCompany,
    Education,
    OrgStructureResponse,
    OrgNode,
    TeamGrowthResponse,
    TeamGrowthTimeSeriesPoint, DepartmentAttrition, HiringTrend, Department, LeadershipTeamMember,
    HiringTrendSupportingData,
)
from backend.models.response.market_analysis import MarketTrendsResponse, MarketSize, CompetitiveAnalysisResponse, \
    GrowthProjectionsResponse, RegionalTrendsResponse, RegionalTrendPoint, CompetitorProfile, \
    GrowthProjectionTimeSeriesPoint
from backend.models.response.partnership_network import PartnerListResponse, PartnerItem, StrategicAlliancesResponse, \
    AllianceImpactItem, NetworkStrengthResponse, PartnershipTrendsResponse, PartnershipTrendTimeSeriesPoint, \
    NetworkMetricItem
from backend.models.response.regulatory_compliance import (
    ComplianceOverviewResponse,
    RegulationItem,
    ViolationHistoryResponse,
    ViolationItem,
    ComplianceRiskResponse,
    ComplianceRiskItem,
    RegionalComplianceResponse,
    RegionalComplianceItem,
)
from backend.models.response.customer_sentiment import (
    SentimentSummaryResponse,
    SentimentBreakdown,
    SentimentTimeSeriesPoint,
    CustomerFeedbackResponse,
    CustomerFeedbackItem,
    BrandReputationResponse,
    SentimentComparisonResponse,
    CompanySentimentData,
    BrandReputationTimeSeriesPoint,
)
from backend.models.response.risk_analysis import RegulatoryRisksResponse, MarketRisksResponse, OperationalRisksResponse, LegalRisksResponse, RegulatoryRiskItem, MarketRiskItem, OperationalRiskItem, LegalRiskItem


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

    @cacheable()
    async def get_research(self, company_name: str, use_knowledge_base: bool = False):
        # Mock data for demonstration
        sample_citations = [
            UrlCitation(url="https://example.com/citation1", title="Sample Citation 1"),
            UrlCitation(url="https://example.com/citation2", title="Sample Citation 2"),
        ]
        now = datetime.now().isoformat()
        now_dt = datetime.now()
        # Finance
        finance_response = FinanceResponse(
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
                last_updated=now,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html",
                plot_url="https://charts.netlify.app/revenue.html",
            ),
            expenses=ExpenseAnalysisResponse(
                company_name=company_name,
                expenses=[
                    ExpenseCategoryBreakdown(
                        category="R&D",
                        value=200000.0,
                        currency="USD",
                        sources=["https://finance.example.com/expenses"],
                        confidence=0.8,
                    ),
                    ExpenseCategoryBreakdown(
                        category="Marketing",
                        value=150000.0,
                        currency="USD",
                        sources=["https://finance.example.com/expenses"],
                        confidence=0.7,
                    ),
                ],
                total_expense=350000.0,
                last_updated=now,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html",
                plot_url="https://charts.netlify.app/expenses.html",
            ),
            margins=ProfitMarginsResponse(
                company_name=company_name,
                margins=[
                    ProfitMarginBreakdown(
                        margin_type="Gross",
                        value=0.6,
                        currency="USD",
                        sources=["https://finance.example.com/margins"],
                        confidence=0.85,
                    ),
                    ProfitMarginBreakdown(
                        margin_type="Net",
                        value=0.2,
                        currency="USD",
                        sources=["https://finance.example.com/margins"],
                        confidence=0.8,
                    ),
                ],
                last_updated=now,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html",
                plot_url="https://charts.netlify.app/margins.html",
            ),
            valuation=ValuationEstimationResponse(
                company_name=company_name,
                last_valuation=5000000.0,
                valuation_timeseries=[
                    ValuationTimeSeriesPoint(date="2023-01-01", value=4000000.0, currency="USD", sources=["https://finance.example.com/valuation"], confidence=0.9),
                    ValuationTimeSeriesPoint(date="2023-12-31", value=5000000.0, currency="USD", sources=["https://finance.example.com/valuation"], confidence=0.95),
                ],
                last_updated=now,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html",
                plot_url="https://charts.netlify.app/valuation.html",
            ),
            funding=FundingHistoryResponse(
                company_name=company_name,
                funding_rounds=[
                    FundingRound(
                        round_type="Seed",
                        value=500000.0,
                        currency="USD",
                        date="2021-06-01",
                        lead_investors=["VC Firm A"],
                        sources=["https://finance.example.com/funding"],
                        confidence=0.9,
                    ),
                    FundingRound(
                        round_type="Series A",
                        value=2000000.0,
                        currency="USD",
                        date="2022-08-15",
                        lead_investors=["VC Firm B"],
                        sources=["https://finance.example.com/funding"],
                        confidence=0.95,
                    ),
                ],
                total_funding=2500000.0,
                last_updated=now,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html",
                plot_url="https://charts.netlify.app/funding.html",
            ),
        )
        # LinkedIn Team
        linkedin_team_response = LinkedInTeamResponse(
            team_overview=TeamOverviewResponse(
                company_name=company_name,
                company_description="A leading tech company.",
                total_employees=200,
                roles_breakdown=[
                    TeamRoleBreakdown(role="Engineer", count=100, percentage=50.0, sources=[1], confidence=0.9),
                    TeamRoleBreakdown(role="Product", count=50, percentage=25.0, sources=[1], confidence=0.8),
                    TeamRoleBreakdown(role="Sales", count=50, percentage=25.0, sources=[1], confidence=0.7),
                ],
                locations=["San Francisco", "New York"],
                key_hiring_areas=["AI", "Cloud"],
                growth_rate=0.15,
                sources=["https://linkedin.com/company/example"],
                last_updated=now,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html",
                plot_url="https://charts.netlify.app/team_overview.html",
            ),
            individual_performance=IndividualPerformanceResponse(
                company_name=company_name,
                individual_name="Jane Doe",
                title="CTO",
                image_url="https://linkedin.com/jane.jpg",
                tenure_years=3.5,
                performance_metrics=[
                    IndividualPerformanceMetric(metric="Leadership", value=9.5, sources=[1], confidence=0.95),
                    IndividualPerformanceMetric(metric="Technical Skill", value=9.0, sources=[1], confidence=0.9),
                ],
                previous_companies=[PreviousCompany(name="BigTech", title="Engineer", duration="2 years", dates="2018-2020")],
                key_strengths=["Leadership", "AI Expertise"],
                development_areas=["Public Speaking"],
                education=[Education(institution="MIT", degree="PhD", field_of_study="CS", dates="2010-2015")],
                sources=["https://linkedin.com/jane"],
                last_updated=now,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html",
                plot_url="https://charts.netlify.app/individual_performance.html",
            ),
            org_structure=OrgStructureResponse(
                company_name=company_name,
                org_chart=[
                    OrgNode(name="Alice Smith", title="CEO", department="Executive", linkedin_url="https://linkedin.com/alice", direct_reports=["Bob Jones", "Carol Lee"]),
                    OrgNode(name="Bob Jones", title="CTO", department="Engineering", linkedin_url="https://linkedin.com/bob", reports_to="Alice Smith"),
                    OrgNode(name="Carol Lee", title="CFO", department="Finance", linkedin_url="https://linkedin.com/carol", reports_to="Alice Smith"),
                ],
                ceo="Alice Smith",
                departments=[
                    Department(name="Engineering", head="Bob Jones", employee_count=100),
                    Department(name="Finance", head="Carol Lee", employee_count=30),
                ],
                leadership_team=[
                    LeadershipTeamMember(name="Alice Smith", title="CEO", linkedin_url="https://linkedin.com/alice", department="Executive"),
                    LeadershipTeamMember(name="Bob Jones", title="CTO", linkedin_url="https://linkedin.com/bob", department="Engineering"),
                ],
                sources=["https://linkedin.com/orgstructure"],
                last_updated=now,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html",
                plot_url="https://charts.netlify.app/org_structure.html",
            ),
            team_growth=TeamGrowthResponse(
                company_name=company_name,
                team_growth_timeseries=[
                    TeamGrowthTimeSeriesPoint(period_start="2022-01-01", period_end="2022-12-31", hires=60, attrition=10, net_growth=50, growth_rate=0.25, sources=[1], confidence=0.9)
                ],
                total_hires=60,
                total_attrition=10,
                net_growth=50,
                growth_rate_annualized=0.25,
                key_hiring_areas=["AI", "Cloud"],
                attrition_by_department=[DepartmentAttrition(department="Engineering", attrition_count=5, attrition_rate=0.05)],
                hiring_trends=[HiringTrend(trend="Upward", description="Hiring increased in 2022", supporting_data=HiringTrendSupportingData(percentage=20.0, count=12, year_over_year_change=0.2, previous_value=48, current_value=60, description="12 more hires than last year"))],
                sources=["https://linkedin.com/teamgrowth"],
                last_updated=now,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html",
                plot_url="https://charts.netlify.app/team_growth.html",
            ),
        )
        # Market Analysis
        market_analysis_response = MarketAnalysisResponse(
            market_trends=MarketTrendsResponse(
                market_size=[MarketSize(percentage=40.0, industry="Cloud Computing", sources=["https://market.example.com"], confidence=0.8)],
                summary="Cloud market is growing rapidly.",
                last_updated=now,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html",
                plot_url="https://charts.netlify.app/market_trends.html",
            ),
            competitive_analysis=CompetitiveAnalysisResponse(
                top_competitors=[
                    CompetitorProfile(
                        company_name="CompetitorA",
                        industry="Cloud Computing",
                        market_share=0.3,
                        revenue=500000.0,
                        growth_rate=0.12,
                        strengths=["Brand"],
                        weaknesses=["Innovation"],
                        differentiating_factors=["Customer Service"],
                        sources=["https://market.example.com/competitors"],
                        confidence=0.8,
                    )
                ],
                summary="CompetitorA leads in brand.",
                last_updated=now,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html",
                plot_url="https://charts.netlify.app/competitive_analysis.html",
            ),
            growth_projections=GrowthProjectionsResponse(
                projections_timeseries=[
                    GrowthProjectionTimeSeriesPoint(
                        period_start="2023-01-01",
                        period_end="2023-12-31",
                        projected_value=1200000.0,
                        metric="revenue",
                        sources=["https://market.example.com/projections"],
                        confidence=0.9,
                    )
                ],
                summary="Projected growth to $1.2M revenue.",
                sources=["https://market.example.com/projections"],
                last_updated=now,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html",
                plot_url="https://charts.netlify.app/growth_projections.html",
            ),
            regional_trends=RegionalTrendsResponse(
                regional_trends=[
                    RegionalTrendPoint(
                        industry="Cloud Computing",
                        region="US",
                        period_start="2023-01-01",
                        period_end="2023-12-31",
                        value=700000.0,
                        metric="revenue",
                        sources=["https://market.example.com/region"],
                        confidence=0.85,
                    )
                ],
                summary="US region leads.",
                last_updated=now,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html",
                plot_url="https://charts.netlify.app/regional_trends.html",
            ),
        )
        # Partnership Network
        partnership_network_response = PartnershipNetworkResponse(
            partner_list=PartnerListResponse(
                company_name=company_name,
                partners=[PartnerItem(name="PartnerX", domain="partnerx.com", partnership_type="Technology", since=now_dt.date(), sources=["https://partners.example.com"])],
                summary="Strong partnership with PartnerX.",
                sources=["https://partners.example.com"],
                last_updated=now_dt,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html",
                plot_url="https://charts.netlify.app/partner_list.html",
            ),
            strategic_alliances=StrategicAlliancesResponse(
                company_name=company_name,
                alliances=[AllianceImpactItem(partner="PartnerY", impact_area="AI", impact_score=0.95, description="AI partnership", sources=["https://partners.example.com/alliances"])],
                summary="High impact alliance with PartnerY.",
                sources=["https://partners.example.com/alliances"],
                last_updated=now_dt,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html",
                plot_url="https://charts.netlify.app/strategic_alliances.html",
            ),
            network_strength=NetworkStrengthResponse(
                company_name=company_name,
                network_metrics=[NetworkMetricItem(metric="Connections", value=120, sources=["https://partners.example.com/network"], confidence=0.9)],
                summary="Strong network strength.",
                sources=["https://partners.example.com/network"],
                last_updated=now_dt,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html",
                plot_url="https://charts.netlify.app/network_strength.html",
            ),
            partnership_trends=PartnershipTrendsResponse(
                company_name=company_name,
                partnership_trends_timeseries=[
                    PartnershipTrendTimeSeriesPoint(period_start=now_dt.date(), period_end=now_dt.date(), new_partnerships=3, ended_partnerships=1, net_growth=2, sources=["https://partners.example.com/trends"], confidence=0.8)
                ],
                summary="2 net new partnerships in 2022.",
                sources=["https://partners.example.com/trends"],
                last_updated=now_dt,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html",
                plot_url="https://charts.netlify.app/partnership_trends.html",
            ),
        )
        # Regulatory Compliance
        regulatory_compliance_response = RegulatoryComplianceResponse(
            compliance_overview=ComplianceOverviewResponse(
                company_name=company_name,
                industry="Technology",
                region="Global",
                regulations=[RegulationItem(regulation="GDPR", description="EU data privacy regulation.", applicable=True, sources=["https://gdpr.eu/"])],
                summary="Compliant with GDPR.",
                sources=["https://gdpr.eu/"],
                last_updated=now_dt,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html",
            ),
            violation_history=ViolationHistoryResponse(
                company_name=company_name,
                industry="Technology",
                region="Global",
                violations=[ViolationItem(violation="Late Notification", regulation="GDPR", date=now_dt.date(), severity="High", description="Late data breach notification.", sources=["https://gdpr.eu/violations"], resolved=True)],
                summary="One GDPR violation in 2022.",
                sources=["https://gdpr.eu/violations"],
                last_updated=now_dt,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html",
            ),
            compliance_risk=ComplianceRiskResponse(
                company_name=company_name,
                industry="Technology",
                region="Global",
                risks=[ComplianceRiskItem(risk="GDPR Non-compliance", severity="High", description="Potential non-compliance with EU data privacy laws.", sources=["https://gdpr.eu/risks"], confidence=0.85)],
                summary="Key risk is GDPR non-compliance.",
                sources=["https://gdpr.eu/risks"],
                last_updated=now_dt,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html",
            ),
            regional_compliance=RegionalComplianceResponse(
                company_name=company_name,
                industry="Technology",
                regional_compliance=[RegionalComplianceItem(region="EU", regulations=[RegulationItem(regulation="GDPR", description="EU data privacy regulation.", applicable=True, sources=["https://gdpr.eu/"])], compliance_score=0.95, sources=["https://gdpr.eu/regional"])],
                summary="High compliance in EU region.",
                sources=["https://gdpr.eu/regional"],
                last_updated=now_dt,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html",
            ),
        )
        # Customer Sentiment
        customer_sentiment_response = CustomerSentimentResponse(
            sentiment_summary=SentimentSummaryResponse(
                company_name=company_name,
                product="Main Product",
                region="Global",
                sentiment_score=0.85,
                sentiment_breakdown=SentimentBreakdown(positive=80, negative=10, neutral=10),
                sentiment_timeseries=[SentimentTimeSeriesPoint(period_start="2023-01-01", period_end="2023-12-31", positive=80, negative=10, neutral=10, sentiment_score=0.85, sources=["https://reviews.example.com"], confidence=0.9)],
                summary="Mostly positive sentiment.",
                sources=["https://reviews.example.com"],
                last_updated=now,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html",
            ),
            customer_feedback=CustomerFeedbackResponse(
                company_name=company_name,
                product="Main Product",
                region="Global",
                feedback_items=[CustomerFeedbackItem(date="2023-06-01", customer="John Doe", feedback="Great product!", sentiment="positive", sources=["https://reviews.example.com/feedback"], confidence=0.95)],
                summary="Positive feedback dominates.",
                sources=["https://reviews.example.com/feedback"],
                last_updated=now,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html",
            ),
            brand_reputation=BrandReputationResponse(
                company_name=company_name,
                region="Global",
                reputation_score=0.9,
                reputation_timeseries=[BrandReputationTimeSeriesPoint(period_start="2023-01-01", period_end="2023-12-31", reputation_score=0.9, sources=["https://reviews.example.com/brand"], confidence=0.95)],
                summary="Excellent brand reputation.",
                sources=["https://reviews.example.com/brand"],
                last_updated=now,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html"
            ),
            sentiment_comparison=SentimentComparisonResponse(
                company_name=company_name,
                product="Main Product",
                region="Global",
                competitors=["Datgenie", "CompetitorB"],
                target_sentiment=CompanySentimentData(company=company_name, sentiment_score=8.5, strengths=["Brand", "Innovation"], weaknesses=["Pricing"]),
                competitor_sentiments=[
                    CompanySentimentData(company="Datgenie", sentiment_score=7.2, strengths=["Speed"], weaknesses=["Support"]),
                    CompanySentimentData(company="CompetitorB", sentiment_score=6.8, strengths=["Reach"], weaknesses=["UX"]),
                ],
                summary="Company leads in sentiment over competitors.",
                confidence=0.92,
                last_updated=now,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html",
            ),
        )
        # Risk Analysis
        risk_analysis_response = RiskAnalysisResponse(
            regulatory_risks=RegulatoryRisksResponse(
                company_name=company_name,
                industry="Technology",
                region="Global",
                risks=[RegulatoryRiskItem(risk="GDPR Non-compliance", severity="High", description="Potential non-compliance with EU data privacy laws.", sources=["https://gdpr.eu/"], confidence=0.85)],
                summary="Key regulatory risk is GDPR.",
                sources=["https://gdpr.eu/"],
                last_updated=now_dt,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html"
            ),
            market_risks=MarketRisksResponse(
                company_name=company_name,
                industry="Technology",
                region="Global",
                risks=[MarketRiskItem(risk="Market Downturn", severity="Medium", description="Potential for reduced demand.", sources=["https://market.example.com/risks"], confidence=0.7)],
                summary="Market downturn is a risk.",
                sources=["https://market.example.com/risks"],
                last_updated=now_dt,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html"
            ),
            operational_risks=OperationalRisksResponse(
                company_name=company_name,
                industry="Technology",
                region="Global",
                risks=[OperationalRiskItem(risk="Supply Chain", severity="Low", description="Delays in hardware supply.", sources=["https://ops.example.com/risks"], confidence=0.6)],
                summary="Supply chain delays possible.",
                sources=["https://ops.example.com/risks"],
                last_updated=now_dt,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html"
            ),
            legal_risks=LegalRisksResponse(
                company_name=company_name,
                industry="Technology",
                region="Global",
                risks=[LegalRiskItem(risk="Patent Infringement", severity="High", description="Risk of IP litigation.", sources=["https://legal.example.com/risks"], confidence=0.8, case_number="2023-XYZ-001", date_filed=now_dt.date())],
                summary="Patent litigation is a risk.",
                sources=["https://legal.example.com/risks"],
                last_updated=now_dt,
                citations=sample_citations,
                iframe_url="https://68317e9733cca04367007675--golden-dolphin-728ed5.netlify.app/charts/08da6f5e-dfb6-4667-8547-6229e8551d74.html"
            ),
        )
        return ResearchResponse(
            company_name=company_name,
            finance=finance_response,
            linkedin_team=linkedin_team_response,
            market_analysis=market_analysis_response,
            partnership_network=partnership_network_response,
            regulatory_compliance=regulatory_compliance_response,
            customer_sentiment=customer_sentiment_response,
            risk_analysis=risk_analysis_response,
        )
