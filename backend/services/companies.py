from backend.settings import MongoConnectionDetails
from backend.models.response.companies import (
    CompanyBaseInfo,
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
from backend.utils.cache_decorator import cacheable
import json
import os
from typing import Optional


class CompaniesService:
    def __init__(self, mongo_config: MongoConnectionDetails):
        self.mongo_config = mongo_config
        # cache_service will be injected by the dependency injection system

    @cacheable()
    async def get_company_analysis(self, company_name: str):
        # Mock data for demonstration
        return CompanyAnalysisFullResponse(
            company=CompanyAnalysisCompanyInfo(
                name=company_name,
                description="A platform for venture analysis.",
                industry="Technology",
                foundingYear=2015,
                headquarters="San Francisco, CA",
                website="https://ventureinsights.com",
                logo="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Apple_logo_grey.svg/1010px-Apple_logo_grey.svg.png",
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

    @cacheable()
    async def get_companies(self, limit: int = None) -> list[CompanyBaseInfo]:
        mock_companies = [
            {
                "name": "DataGenie",
                "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQS7QDxSkojyltJTl6vIloCWUDzmtohbDsWCg&s",
                "founder": "Ashish Verma",
                "headquarters": "San Francisco, CA, USA",
                "founding_date": "2020-01-01T00:00:00",
                "members_count": 10,
            },
            {
                "name": "Meta",
                "logo": "https://m.economictimes.com/thumb/msid-111856636,width-1200,height-900,resizemode-4,imgsize-155652/a-microsoft-logo.jpg",
                "founder": "Mark Zuckerberg",
                "headquarters": "Menlo Park, CA, USA",
                "founding_date": "2015-01-01T00:00:00",
                "members_count": 50,
            },
            {
                "name": "CypherD",
                "logo": "https://play-lh.googleusercontent.com/-dmoFW03JcyJihlNoguKe5mZBGSigpDGVlZKkJi6EhDLnzvUJQMIUhw3l6TrCW6CksE",
                "founder": "John Doe",
                "headquarters": "New York, NY, USA",
                "founding_date": "2015-01-01T00:00:00",
                "members_count": 50,
            },
            {
                "name": "PayPal",
                "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZ0ffI8EqxD3ClancA6PDjV_Blp1dZuZv_HVb6KkSXn1Z3i9fAdz4i1WBmun75iVpQU38&usqp=CAU",
                "founder": "Elon Musk, Peter Thiel, Max Levchin",
                "headquarters": "San Jose, CA, USA",
                "founding_date": "2015-01-01T00:00:00",
                "members_count": 50,
            },
        ]
        return [CompanyBaseInfo(**company) for company in mock_companies]

    @cacheable()
    async def get_featured_companies(
        self, limit: Optional[int] = None, page: int = 1
    ) -> dict:
        """
        Get featured companies for display on the homepage or featured section

        Args:
            limit: Optional number of companies to return
            page: Page number for pagination

        Returns:
            Dictionary with companies, total count, page number and limit
        """
        # Load sample data from JSON file
        json_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "data", "sample_card.json"
        )

        with open(json_path, "r") as f:
            companies_data = json.load(f)

        # Apply pagination if limit is provided
        total = len(companies_data)

        if limit:
            # Calculate start and end indices for pagination
            start_idx = (page - 1) * limit
            end_idx = start_idx + limit

            # Slice the data
            paginated_data = companies_data[start_idx:end_idx]
        else:
            paginated_data = companies_data
            limit = total

        return {
            "companies": paginated_data,
            "total": total,
            "page": page,
            "limit": limit,
        }
