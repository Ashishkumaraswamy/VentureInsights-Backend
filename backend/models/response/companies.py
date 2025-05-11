from datetime import datetime

from pydantic import BaseModel, Field


class CompanyBaseInfo(BaseModel):
    name: str = Field(..., description="Name of the company")
    logo: str = Field(..., description="URL to the company logo image")
    founder: str = Field(..., description="Name of the founder")
    headquarters: str = Field(..., description="Headquarters location")
    founding_date: datetime = Field(..., description="Founding Date of the company")
    members_count: int = Field(..., description="Number of members in the company")


class DocumentInfo(BaseModel):
    id: str
    name: str
    type: str
    uploadDate: str
    analysis: str


class DocumentProcessing(BaseModel):
    summary: str
    keyFindings: list[str]
    documents: list[DocumentInfo]


class TeamMember(BaseModel):
    name: str
    role: str
    background: str
    linkedin: str


class TeamAnalysis(BaseModel):
    founders: list[TeamMember]
    keyTeamMembers: list[TeamMember]


class MarketIntelligence(BaseModel):
    marketSize: float
    growthRate: float
    trends: list[str]
    opportunities: list[str]


class Competitor(BaseModel):
    name: str
    strength: str
    weakness: str


class CompetitiveLandscape(BaseModel):
    competitors: list[Competitor]
    marketPosition: str


class FinancialAnalysis(BaseModel):
    revenue: float
    funding: float
    valuation: float
    metrics: dict[str, str]


class RiskItem(BaseModel):
    category: str
    description: str
    severity: str
    mitigation: str


class RiskAssessment(BaseModel):
    risks: list[RiskItem]


class CompanyAnalysisCompanyInfo(BaseModel):
    name: str = Field(..., description="Name of the company")
    description: str = Field(..., description="Short description of the company")
    industry: str = Field(..., description="Industry sector of the company")
    foundingYear: int = Field(..., description="Year the company was founded")
    headquarters: str = Field(..., description="Headquarters location")
    website: str = Field(..., description="Company website URL")
    logo: str = Field(..., description="URL to the company logo image")


class CompanyAnalysis(BaseModel):
    documentProcessing: DocumentProcessing = Field(
        ..., description="Analysis and summary of company documents"
    )
    teamAnalysis: TeamAnalysis = Field(
        ..., description="Analysis of founders and key team members"
    )
    marketIntelligence: MarketIntelligence = Field(
        ..., description="Market size, growth, trends, and opportunities"
    )
    competitiveLandscape: CompetitiveLandscape = Field(
        ..., description="Competitors and market position analysis"
    )
    financialAnalysis: FinancialAnalysis = Field(
        ..., description="Financial metrics, revenue, funding, and valuation"
    )
    riskAssessment: RiskAssessment = Field(
        ..., description="Identified risks and mitigation strategies"
    )


class CompanyAnalysisFullResponse(BaseModel):
    company: CompanyAnalysisCompanyInfo = Field(
        ..., description="Basic information about the company"
    )
    analysis: CompanyAnalysis = Field(
        ..., description="Detailed analysis of the company"
    )
