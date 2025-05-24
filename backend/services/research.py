import asyncio
import time
from backend.database.mongo import MongoDBConnector
from backend.settings import MongoConnectionDetails

from backend.services.finance import FinanceService
from backend.services.linkedin_team import LinkedInTeamService
from backend.services.market_analysis import MarketAnalysisService
from backend.models.response.research import (
    ResearchResponse,
    FinanceResponse,
    LinkedInTeamResponse,
    MarketAnalysisResponse,
)


class ResearchService:
    def __init__(
        self,
        db_config: MongoConnectionDetails,
        finance_service: FinanceService,
        linkedin_team_service: LinkedInTeamService,
        market_analysis_service: MarketAnalysisService,
    ):
        self.mongo_db = MongoDBConnector(db_config)
        self.finance_service = finance_service
        self.linkedin_team_service = linkedin_team_service
        self.market_analysis_service = market_analysis_service

    async def get_research(self, company_name: str, use_knowledge_base: bool = False):
        """
        Get comprehensive research data for a company by calling multiple service agents in parallel.

        Args:
            company_name (str): Name of the company to research
            use_knowledge_base (bool): Whether to use the knowledge base

        Returns:
            ResearchResponse: Comprehensive research data about the company
        """

        # Create task groups with clearer tracking
        async def tracked_task(name, coro):
            print(f">>> STARTING: {name} at {time.time()}")
            try:
                result = await coro
                print(f">>> COMPLETED: {name} at {time.time()}")
                return result
            except Exception as e:
                print(f">>> ERROR: {name} failed with {str(e)}")
                return e

        # Create finance tasks
        finance_revenue = tracked_task(
            "finance_revenue",
            self.finance_service.get_revenue_analysis(
                company_name, use_knowledge_base=use_knowledge_base
            ),
        )

        finance_expenses = tracked_task(
            "finance_expenses",
            self.finance_service.get_expense_analysis(
                company_name, use_knowledge_base=use_knowledge_base
            ),
        )

        finance_margins = tracked_task(
            "finance_margins",
            self.finance_service.get_profit_margins(
                company_name, use_knowledge_base=use_knowledge_base
            ),
        )

        finance_valuation = tracked_task(
            "finance_valuation",
            self.finance_service.get_valuation_estimation(
                company_name, use_knowledge_base=use_knowledge_base
            ),
        )

        finance_funding = tracked_task(
            "finance_funding",
            self.finance_service.get_funding_history(
                company_name, use_knowledge_base=use_knowledge_base
            ),
        )

        # Create LinkedIn team tasks
        linkedin_team_overview = tracked_task(
            "linkedin_team_overview",
            self.linkedin_team_service.get_team_overview(company_name),
        )

        linkedin_individual = tracked_task(
            "linkedin_individual",
            self.linkedin_team_service.get_individual_performance(
                company_name, use_knowledge_base=use_knowledge_base
            ),
        )

        linkedin_org_structure = tracked_task(
            "linkedin_org_structure",
            self.linkedin_team_service.get_org_structure(
                company_name, use_knowledge_base=use_knowledge_base
            ),
        )

        linkedin_team_growth = tracked_task(
            "linkedin_team_growth",
            self.linkedin_team_service.get_team_growth(
                company_name, use_knowledge_base=use_knowledge_base
            ),
        )

        # Create market analysis tasks
        market_trends = tracked_task(
            "market_trends",
            self.market_analysis_service.get_market_trends(
                company_name, use_knowledge_base=use_knowledge_base
            ),
        )

        market_competitive = tracked_task(
            "market_competitive",
            self.market_analysis_service.get_competitive_analysis(
                company_name, use_knowledge_base=use_knowledge_base
            ),
        )

        market_growth = tracked_task(
            "market_growth",
            self.market_analysis_service.get_growth_projections(
                company_name, use_knowledge_base=use_knowledge_base
            ),
        )

        market_regional = tracked_task(
            "market_regional",
            self.market_analysis_service.get_regional_trends(
                company_name, use_knowledge_base=use_knowledge_base
            ),
        )

        # Run a small batch of concurrent tasks first (4 at a time)
        print(f">>> STARTING BATCH 1 at {time.time()}")
        finance_results_part1 = await asyncio.gather(
            finance_revenue, finance_expenses, finance_margins, finance_valuation
        )

        print(f">>> STARTING BATCH 2 at {time.time()}")
        # Run the next batch
        finance_results_part2 = await asyncio.gather(
            finance_funding,
            linkedin_team_overview,
            linkedin_individual,
            linkedin_org_structure,
        )

        print(f">>> STARTING BATCH 3 at {time.time()}")
        # Run the final batch
        remaining_results = await asyncio.gather(
            linkedin_team_growth,
            market_trends,
            market_competitive,
            market_growth,
            market_regional,
        )

        # Combine results
        revenue, expenses, margins, valuation = finance_results_part1
        funding, team_overview, individual_performance, org_structure = (
            finance_results_part2
        )
        (
            team_growth,
            market_trends_result,
            competitive_analysis,
            growth_projections,
            regional_trends,
        ) = remaining_results

        # Process finance results
        finance_response = FinanceResponse(
            revenue=revenue if not isinstance(revenue, Exception) else None,
            expenses=expenses if not isinstance(expenses, Exception) else None,
            margins=margins if not isinstance(margins, Exception) else None,
            valuation=valuation if not isinstance(valuation, Exception) else None,
            funding=funding if not isinstance(funding, Exception) else None,
        )

        # Process LinkedIn team results
        linkedin_response = LinkedInTeamResponse(
            team_overview=team_overview
            if not isinstance(team_overview, Exception)
            else None,
            individual_performance=individual_performance
            if not isinstance(individual_performance, Exception)
            else None,
            org_structure=org_structure
            if not isinstance(org_structure, Exception)
            else None,
            team_growth=team_growth if not isinstance(team_growth, Exception) else None,
        )

        # Process market analysis results
        market_response = MarketAnalysisResponse(
            market_trends=market_trends_result
            if not isinstance(market_trends_result, Exception)
            else None,
            competitive_analysis=competitive_analysis
            if not isinstance(competitive_analysis, Exception)
            else None,
            growth_projections=growth_projections
            if not isinstance(growth_projections, Exception)
            else None,
            regional_trends=regional_trends
            if not isinstance(regional_trends, Exception)
            else None,
        )

        # Combine all responses
        research_response = ResearchResponse(
            company_name=company_name,
            finance=finance_response,
            linkedin_team=linkedin_response,
            market_analysis=market_response,
        )

        # Save to MongoDB - save research to a collection named after the company
        try:
            research_dict = research_response.dict()
            self.mongo_db.insert_one(
                f"research_{company_name.lower().replace(' ', '_')}", research_dict
            )
            print(f">>> SAVED research data for {company_name} to MongoDB")
        except Exception as e:
            print(f">>> ERROR saving to MongoDB: {str(e)}")

        return research_response
