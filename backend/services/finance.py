from backend.settings import LLMConfig
from datetime import datetime


class FinanceService:
    def __init__(
        self,
        llm_config: LLMConfig,
    ):
        self.llm_config = llm_config

    async def get_revenue_analysis(self):
        return {
            "company_name": "TechNova Inc.",
            "currency": "USD",
            "revenue_timeseries": [
                {
                    "period_start": "2023-01-01",
                    "period_end": "2023-03-31",
                    "value": 1200000.0,
                    "sources": [
                        "https://crunchbase.com/tecnova",
                        "https://news.ycombinator.com/item?id=123456",
                    ],
                    "confidence": 0.9,
                },
                {
                    "period_start": "2023-04-01",
                    "period_end": "2023-06-30",
                    "value": 1350000.0,
                    "sources": ["https://crunchbase.com/tecnova"],
                    "confidence": 0.85,
                },
            ],
            "total_revenue": 2550000.0,
            "last_updated": datetime.now().isoformat(),
        }

    async def get_expense_analysis(self):
        return {
            "company_name": "TechNova Inc.",
            "year": 2023,
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

    async def get_profit_margins(self):
        return {
            "company_name": "TechNova Inc.",
            "year": 2023,
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

    async def get_valuation_estimation(self):
        return {
            "company_name": "TechNova Inc.",
            "valuation": 15000000.0,
            "currency": "USD",
            "as_of_date": "2024-05-01",
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

    async def get_funding_history(self):
        return {
            "company_name": "TechNova Inc.",
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
