from datetime import datetime

from backend.models.response.companies import CompanyBaseInfo
from backend.settings import MongoConnectionDetails


class CompaniesService:
    async def get_company_analysis(self, company_id: str):
        from backend.models.response.companies import (
            CompanyAnalysisFullResponse,
            CompanyAnalysisCompanyInfo,
            CompanyAnalysis,
            DocumentProcessing,
            DocumentInfo,
            TeamAnalysis,
            TeamMember,
            MarketIntelligence,
            Competitor,
            CompetitiveLandscape,
            FinancialAnalysis,
            RiskAssessment,
            RiskItem,
        )

        # Mock data for demonstration
        return CompanyAnalysisFullResponse(
            company=CompanyAnalysisCompanyInfo(
                id=company_id,
                name="VentureInsights",
                description="A platform for venture analysis.",
                industry="Technology",
                foundingYear=2015,
                headquarters="San Francisco, CA",
                website="https://ventureinsights.com",
                logo="https://ventureinsights.com/logo.png",
            ),
            analysis=CompanyAnalysis(
                documentProcessing=DocumentProcessing(
                    summary="Key company documents have been analyzed.",
                    keyFindings=["Strong IP portfolio", "Recent funding round"],
                    documents=[
                        DocumentInfo(
                            id="doc1",
                            name="Pitch Deck",
                            type="pdf",
                            uploadDate="2023-01-01",
                            analysis="Highlights growth potential.",
                        )
                    ],
                ),
                teamAnalysis=TeamAnalysis(
                    founders=[
                        TeamMember(
                            name="Alice Smith",
                            role="CEO",
                            background="Serial entrepreneur",
                            linkedin="https://linkedin.com/in/alicesmith",
                        )
                    ],
                    keyTeamMembers=[
                        TeamMember(
                            name="Bob Lee",
                            role="CTO",
                            background="Ex-Google engineer",
                            linkedin="https://linkedin.com/in/boblee",
                        )
                    ],
                ),
                marketIntelligence=MarketIntelligence(
                    marketSize=100000000.0,
                    growthRate=12.5,
                    trends=["AI adoption", "Remote work"],
                    opportunities=["Untapped SME market"],
                ),
                competitiveLandscape=CompetitiveLandscape(
                    competitors=[
                        Competitor(
                            name="CompetitorX",
                            strength="Strong brand",
                            weakness="Limited product range",
                        )
                    ],
                    marketPosition="Emerging leader",
                ),
                financialAnalysis=FinancialAnalysis(
                    revenue=5000000.0,
                    funding=12000000.0,
                    valuation=50000000.0,
                    metrics={"EBITDA": "1M", "Burn Rate": "100K/mo"},
                ),
                riskAssessment=RiskAssessment(
                    risks=[
                        RiskItem(
                            category="Market",
                            description="High competition",
                            severity="Medium",
                            mitigation="Focus on niche segments",
                        )
                    ]
                ),
            ),
        )

    def __init__(self, mongo_config: MongoConnectionDetails):
        self.mongo_config = mongo_config

    async def get_companies(self, limit: int = None) -> list[CompanyBaseInfo]:
        return [
            CompanyBaseInfo(
                name="DataGenie", founding_date=datetime(2020, 1, 1), members_count=10
            ),
            CompanyBaseInfo(
                name="VentureInsights",
                founding_date=datetime(2015, 1, 1),
                members_count=50,
            ),
            CompanyBaseInfo(
                name="CypherD", founding_date=datetime(2015, 1, 1), members_count=50
            ),
            CompanyBaseInfo(
                name="Test", founding_date=datetime(2015, 1, 1), members_count=50
            ),
        ]
