from fastmcp import FastMCP
from backend.services.finance import FinanceService
from backend.services.linkedin_team import LinkedInTeamService
from backend.services.market_analysis import MarketAnalysisService
from backend.services.risk_analysis import RiskAnalysisService
from backend.services.customer_sentiment import CustomerSentimentService
from backend.services.regulatory_compliance import RegulatoryComplianceService
from backend.services.partnership_network import PartnershipNetworkService
from backend.dependencies import get_finance_service

mcp = FastMCP("Venture Insights MCP Server")

# Instantiate services
finance_service = FinanceService(get_finance_service)
linkedin_team_service = LinkedInTeamService()
market_analysis_service = MarketAnalysisService()
risk_analysis_service = RiskAnalysisService()
customer_sentiment_service = CustomerSentimentService()
regulatory_compliance_service = RegulatoryComplianceService()
partnership_network_service = PartnershipNetworkService()


# --- Finance ---
@mcp.tool()
async def revenue_analysis(
    company_name: str,
    domain: str = None,
    start_date: str = None,
    end_date: str = None,
    granularity: str = "year",
):
    return await finance_service.get_revenue_analysis()


@mcp.tool()
async def expense_analysis(
    company_name: str, domain: str = None, year: int = None, category: str = None
):
    return await finance_service.get_expense_analysis()


@mcp.tool()
async def profit_margins(company_name: str, domain: str = None, year: int = None):
    return await finance_service.get_profit_margins()


@mcp.tool()
async def valuation_estimation(
    company_name: str, domain: str = None, as_of_date: str = None
):
    return await finance_service.get_valuation_estimation()


@mcp.tool()
async def funding_history(company_name: str, domain: str = None):
    return await finance_service.get_funding_history()


# --- LinkedIn Team ---
@mcp.tool()
async def team_overview(company_name: str, domain: str = None):
    return await linkedin_team_service.get_team_overview()


@mcp.tool()
async def individual_performance(
    company_name: str, domain: str = None, individual_name: str = None
):
    return await linkedin_team_service.get_individual_performance()


@mcp.tool()
async def org_structure(company_name: str, domain: str = None):
    return await linkedin_team_service.get_org_structure()


@mcp.tool()
async def team_growth(
    company_name: str, domain: str = None, start_date: str = None, end_date: str = None
):
    return await linkedin_team_service.get_team_growth()


# --- Market Analysis ---
@mcp.tool()
async def market_trends(
    industry: str, region: str = None, start_date: str = None, end_date: str = None
):
    return await market_analysis_service.get_market_trends()


@mcp.tool()
async def competitive_analysis(
    company_name: str, domain: str = None, industry: str = None, region: str = None
):
    return await market_analysis_service.get_competitive_analysis()


@mcp.tool()
async def growth_projections(
    industry: str, region: str = None, start_date: str = None, end_date: str = None
):
    return await market_analysis_service.get_growth_projections()


@mcp.tool()
async def regional_trends(
    industry: str, regions: list = None, start_date: str = None, end_date: str = None
):
    return await market_analysis_service.get_regional_trends()


# --- Risk Analysis ---
@mcp.tool()
async def regulatory_risks(
    company_name: str, domain: str = None, industry: str = None, region: str = None
):
    return await risk_analysis_service.get_regulatory_risks()


@mcp.tool()
async def market_risks(
    company_name: str, domain: str = None, industry: str = None, region: str = None
):
    return await risk_analysis_service.get_market_risks()


@mcp.tool()
async def operational_risks(
    company_name: str, domain: str = None, industry: str = None, region: str = None
):
    return await risk_analysis_service.get_operational_risks()


@mcp.tool()
async def legal_risks(
    company_name: str, domain: str = None, industry: str = None, region: str = None
):
    return await risk_analysis_service.get_legal_risks()


# --- Customer Sentiment ---
@mcp.tool()
async def sentiment_summary(
    company_name: str,
    domain: str = None,
    product: str = None,
    region: str = None,
    start_date: str = None,
    end_date: str = None,
):
    return await customer_sentiment_service.get_sentiment_summary()


@mcp.tool()
async def customer_feedback(
    company_name: str,
    domain: str = None,
    product: str = None,
    region: str = None,
    start_date: str = None,
    end_date: str = None,
):
    return await customer_sentiment_service.get_customer_feedback()


@mcp.tool()
async def brand_reputation(
    company_name: str,
    domain: str = None,
    region: str = None,
    start_date: str = None,
    end_date: str = None,
):
    return await customer_sentiment_service.get_brand_reputation()


# --- Regulatory Compliance ---
@mcp.tool()
async def compliance_overview(
    company_name: str, domain: str = None, industry: str = None, region: str = None
):
    return await regulatory_compliance_service.get_compliance_overview()


@mcp.tool()
async def violation_history(
    company_name: str,
    domain: str = None,
    industry: str = None,
    region: str = None,
    start_date: str = None,
    end_date: str = None,
):
    return await regulatory_compliance_service.get_violation_history()


@mcp.tool()
async def compliance_risk(
    company_name: str, domain: str = None, industry: str = None, region: str = None
):
    return await regulatory_compliance_service.get_compliance_risk()


@mcp.tool()
async def regional_compliance(
    company_name: str, domain: str = None, industry: str = None, regions: list = None
):
    return await regulatory_compliance_service.get_regional_compliance()


# --- Partnership Network ---
@mcp.tool()
async def partner_list(
    company_name: str, domain: str = None, industry: str = None, region: str = None
):
    return await partnership_network_service.get_partner_list()


@mcp.tool()
async def strategic_alliances(
    company_name: str, domain: str = None, industry: str = None, region: str = None
):
    return await partnership_network_service.get_strategic_alliances()


@mcp.tool()
async def network_strength(
    company_name: str, domain: str = None, industry: str = None, region: str = None
):
    return await partnership_network_service.get_network_strength()


@mcp.tool()
async def partnership_trends(
    company_name: str,
    domain: str = None,
    industry: str = None,
    region: str = None,
    start_date: str = None,
    end_date: str = None,
):
    return await partnership_network_service.get_partnership_trends()


@mcp.tool()
async def hi(name: str, age: int = None):
    return "Hi"


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=9000)
