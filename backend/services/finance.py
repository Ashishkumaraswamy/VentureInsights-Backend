from datetime import datetime, date
from typing import Optional

from agno.agent import Agent

from backend.agents.output_parser import LLMOutputParserAgent
from backend.settings import SonarConfig, LLMConfig
from backend.utils.llm import get_model, get_sonar_model
from backend.models.response.finance import RevenueAnalysisResponse


class FinanceService:
    def __init__(self, llm_config: LLMConfig, sonar_config: SonarConfig):
        self.llm_config = llm_config
        self.sonar_config = sonar_config
        self.llm_model = get_model(self.llm_config)
        self.sonar_model = get_sonar_model(self.sonar_config)
        self.llm_output_parser = LLMOutputParserAgent(self.llm_model)

    async def get_revenue_analysis(
        self,
        company_name: str,
        domain: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        granularity: str = "year",
    ):
        """
        Retrieve revenue analysis data for a company.
        Args:
            company_name (str): Name of the company (required)
            domain (str, optional): Domain of the company
            start_date (date, optional): Start date for analysis
            end_date (date, optional): End date for analysis
            granularity (str, optional): Granularity of data (year, quarter, or month)
        Returns:
            dict: Contains company name, currency, revenue timeseries, total revenue, and last updated timestamp.
        """

        # Compose a detailed prompt for the LLM to generate all required fields
        prompt = f"""
        You are a financial analyst. Generate a detailed revenue analysis for the following company:
        - Company Name: {company_name}
        - Domain: {domain or "N/A"}
        - Start Date: {start_date or "N/A"}
        - End Date: {end_date or "N/A"}
        - Granularity: {granularity}

        Please provide the following fields in your response:
        - company_name: The name of the company
        - currency: The currency used for revenue (e.g., USD)
        - revenue_timeseries: A list of objects, each with period_start, period_end, value, sources (list of strings), and confidence (float between 0 and 1)
        - total_revenue: The total revenue for the period
        - last_updated: The datetime of the latest data (ISO format)

        Be as realistic and detailed as possible. Use plausible numbers and sources. Output should be a detailed textual description of all these fields and their values.
        """
        revenue_agent = Agent(
            name="RevenueAgent",
            model=self.sonar_model,
            instructions=prompt,
        )

        # Use the LLM to generate the content
        content = revenue_agent.run(prompt)
        # Parse the LLM output into the response model
        response = self.llm_output_parser.parse(
            content.content, RevenueAnalysisResponse
        )
        if isinstance(response, RevenueAnalysisResponse):
            response.citations = content.citations.urls
        return response

    async def get_expense_analysis(
        self,
        company_name: str,
        domain: Optional[str] = None,
        year: Optional[int] = None,
        category: Optional[str] = None,
    ):
        """
        Retrieve expense analysis data for a company.
        Args:
            company_name (str): Name of the company (required)
            domain (str, optional): Domain of the company
            year (int, optional): Year for analysis
            category (str, optional): Expense category
        Returns:
            dict: Contains company name, year, expenses by category, expense timeseries, total expense, currency, and last updated timestamp.
        """
        return {
            "company_name": company_name,
            "year": year or 2023,
            "expenses": [
                {
                    "category": "R&D",
                    "amount": 500000.0,
                    "currency": "USD",
                    "sources": ["https://publicfilings.com/tecnova"],
                    "confidence": 0.8,
                },
                {
                    "category": "Marketing",
                    "amount": 300000.0,
                    "currency": "USD",
                    "sources": ["https://publicfilings.com/tecnova"],
                    "confidence": 0.7,
                },
            ],
            "expense_timeseries": [
                {
                    "period_start": "2023-01-01",
                    "period_end": "2023-03-31",
                    "category": "R&D",
                    "value": 120000.0,
                    "sources": ["https://publicfilings.com/tecnova"],
                    "confidence": 0.8,
                },
                {
                    "period_start": "2023-01-01",
                    "period_end": "2023-03-31",
                    "category": "Marketing",
                    "value": 80000.0,
                    "sources": ["https://publicfilings.com/tecnova"],
                    "confidence": 0.7,
                },
            ],
            "total_expense": 800000.0,
            "currency": "USD",
            "last_updated": datetime.now().isoformat(),
        }

    async def get_profit_margins(
        self,
        company_name: str,
        domain: Optional[str] = None,
        year: Optional[int] = None,
    ):
        """
        Retrieve profit margin data for a company.
        Args:
            company_name (str): Name of the company (required)
            domain (str, optional): Domain of the company
            year (int, optional): Year for analysis
        Returns:
            dict: Contains company name, year, gross/operating/net margins, margin timeseries, currency, sources, and last updated timestamp.
        """
        return {
            "company_name": company_name,
            "year": year or 2023,
            "gross_margin": 0.55,
            "operating_margin": 0.32,
            "net_margin": 0.21,
            "margin_timeseries": [
                {
                    "period_start": "2023-01-01",
                    "period_end": "2023-03-31",
                    "gross_margin": 0.53,
                    "operating_margin": 0.30,
                    "net_margin": 0.20,
                    "sources": ["https://finance.yahoo.com/tecnova"],
                    "confidence": 0.8,
                },
                {
                    "period_start": "2023-04-01",
                    "period_end": "2023-06-30",
                    "gross_margin": 0.57,
                    "operating_margin": 0.34,
                    "net_margin": 0.22,
                    "sources": ["https://finance.yahoo.com/tecnova"],
                    "confidence": 0.85,
                },
            ],
            "currency": "USD",
            "sources": ["https://finance.yahoo.com/tecnova"],
            "last_updated": datetime.now().isoformat(),
        }

    async def get_valuation_estimation(
        self,
        company_name: str,
        domain: Optional[str] = None,
        as_of_date: Optional[date] = None,
    ):
        """
        Retrieve valuation estimation data for a company.
        Args:
            company_name (str): Name of the company (required)
            domain (str, optional): Domain of the company
            as_of_date (date, optional): Date for valuation
        Returns:
            dict: Contains company name, valuation, currency, as-of date, valuation timeseries, sources, confidence, and last updated timestamp.
        """
        return {
            "company_name": company_name,
            "valuation": 15000000.0,
            "currency": "USD",
            "as_of_date": str(as_of_date) if as_of_date else "2024-05-01",
            "valuation_timeseries": [
                {
                    "as_of_date": "2023-06-01",
                    "valuation": 12000000.0,
                    "sources": ["https://techcrunch.com/tecnova-funding"],
                    "confidence": 0.7,
                },
                {
                    "as_of_date": "2024-05-01",
                    "valuation": 15000000.0,
                    "sources": [
                        "https://techcrunch.com/tecnova-funding",
                        "https://crunchbase.com/tecnova",
                    ],
                    "confidence": 0.8,
                },
            ],
            "sources": [
                "https://techcrunch.com/tecnova-funding",
                "https://crunchbase.com/tecnova",
            ],
            "confidence": 0.8,
            "last_updated": datetime.now().isoformat(),
        }

    async def get_funding_history(
        self, company_name: str, domain: Optional[str] = None
    ):
        """
        Retrieve funding history data for a company.
        Args:
            company_name (str): Name of the company (required)
            domain (str, optional): Domain of the company
        Returns:
            dict: Contains company name, funding rounds, cumulative funding timeseries, total funding, currency, and last updated timestamp.
        """
        return {
            "company_name": company_name,
            "funding_rounds": [
                {
                    "round_type": "Seed",
                    "amount": 2000000.0,
                    "currency": "USD",
                    "date": "2022-01-15",
                    "lead_investors": ["Alpha Ventures"],
                    "sources": ["https://crunchbase.com/tecnova"],
                },
                {
                    "round_type": "Series A",
                    "amount": 5000000.0,
                    "currency": "USD",
                    "date": "2023-03-10",
                    "lead_investors": ["Beta Capital", "Gamma Partners"],
                    "sources": ["https://techcrunch.com/tecnova-funding"],
                },
            ],
            "funding_cumulative_timeseries": [
                {
                    "date": "2022-01-15",
                    "cumulative_amount": 2000000.0,
                    "sources": ["https://crunchbase.com/tecnova"],
                },
                {
                    "date": "2023-03-10",
                    "cumulative_amount": 7000000.0,
                    "sources": ["https://techcrunch.com/tecnova-funding"],
                },
            ],
            "total_funding": 7000000.0,
            "currency": "USD",
            "last_updated": datetime.now().isoformat(),
        }
