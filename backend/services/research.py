from agno.agent import Agent
from backend.agents.output_parser import LLMOutputParserAgent
from backend.database.mongo import MongoDBConnector
from backend.models.base.exceptions import Status
from backend.services.knowledge import KnowledgeBaseService
from backend.settings import MongoConnectionDetails, LLMConfig
import asyncio
import time

from backend.services.finance import FinanceService
from backend.services.team import TeamService
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
    ResearchResponseWithSummary,
)
from backend.models.response.finance import (
    RevenueAnalysisResponse,
    ExpenseAnalysisResponse,
    ProfitMarginsResponse,
    ValuationEstimationResponse,
    FundingHistoryResponse,
)
from backend.models.response.team import (
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
from backend.utils.exceptions import ServiceException
from backend.utils.llm import get_model


# Common base system prompt for all section/field LLMs
def BASE_SYSTEM_PROMPT():
    return """
You are a research agent. Your job is to extract, synthesize, and update company research details using the knowledge base as your primary source of truth.

General Instructions:
- For the field you are responsible for, actively search for and extract the most relevant and up-to-date information from the knowledge base.
- If the knowledge base contains relevant information for your field, you MUST:
    - Replace all basic info for that field with the knowledge base data.
    - Remove all basic info and citations for that field.
    - Set the only source for that field to 'Knowledge Base'.
    - Give extremely low weight to the basic info—use it ONLY if the knowledge base is empty for that field.
- Only if the knowledge base does not have information for your field, use the basic info as a fallback.
- This is a mandatory, high-priority rule: always check the knowledge base first and use its data if available. Be explicit and exhaustive in your search for your field.
- Your output must be a single, valid JSON object that exactly matches the schema provided below. Do not include any explanations or text outside the JSON.
"""


# Field-specific system prompt templates
def FIELD_SYSTEM_PROMPT(field_name, schema):
    return f"""
{BASE_SYSTEM_PROMPT()}
You are responsible for the field: **{field_name}** in the response model **{schema.__name__}**.

Instructions for this field:
- Focus your search and extraction on information relevant to **{field_name}**.
- Highlight and use any knowledge base facts/documents that mention or relate to **{field_name}** or its subfields.
- If the knowledge base contains information for **{field_name}**, you MUST replace all basic info and citations for that field with the knowledge base data, and set the only source to 'Knowledge Base'.
- Only use the basic info if the knowledge base is empty for this field, and give it extremely low weight.

Below is the schema for your field:
```json
{schema.schema_json(indent=2)}
```
"""


class ResearchService:
    def __init__(
        self,
        finance_service: FinanceService,
        linkedin_team_service: TeamService,
        market_analysis_service: MarketAnalysisService,
        partnership_network_service: PartnershipNetworkService,
        customer_sentiment_service: CustomerSentimentService,
        regulatory_compliance_service: RegulatoryComplianceService,
        risk_analysis_service: RiskAnalysisService,
        knowledge_base_service: KnowledgeBaseService,
        db_config: MongoConnectionDetails,
        llm_config: LLMConfig,
    ):
        self.finance_service = finance_service
        self.linkedin_team_service = linkedin_team_service
        self.market_analysis_service = market_analysis_service
        self.partnership_network_service = partnership_network_service
        self.customer_sentiment_service = customer_sentiment_service
        self.regulatory_compliance_service = regulatory_compliance_service
        self.risk_analysis_service = risk_analysis_service
        self.knowledge_base = knowledge_base_service.get_knowledge_base()
        self.db_config = db_config
        self.mongo_connector = MongoDBConnector(db_config)
        self.llm_model = get_model(llm_config)
        self.llm_output_parser = LLMOutputParserAgent(self.llm_model)

    async def _llm_field(
        self, company: str, section_name, field_name, schema, knowledge, basic_info
    ):
        prompt = FIELD_SYSTEM_PROMPT(field_name, schema)
        agent = Agent(
            name=f"{section_name}_{field_name}Agent",
            model=self.llm_model,
            instructions=prompt,
            response_model=schema,
            knowledge=knowledge,
            search_knowledge=True,
            use_json_mode=True,
            show_tool_calls=True,
        )
        input_text = (
            f"Generate the {company} {field_name} field for the {section_name} section"
        )
        # LOG THE CONTEXT
        # print(f"\n--- LLM CONTEXT FOR {section_name.upper()} - {field_name.upper()} ---")
        # print("Prompt:\n", prompt)
        # print("Input Text:\n", input_text)
        # print("Knowledge (first 1000 chars):\n", str(knowledge)[:1000])
        # print("--- END CONTEXT ---\n")
        response = await agent.arun(input_text)
        return response.content

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
            self.mongo_connector.insert_records(
                f"research_{company_name.lower().replace(' ', '_')}", research_dict
            )
            print(f">>> SAVED research data for {company_name} to MongoDB")
        except Exception as e:
            print(f">>> ERROR saving to MongoDB: {str(e)}")

        return research_response

    async def get_deep_research(
        self, company_name: str, use_knowledge_base: bool = False
    ):
        get_basic_company_info = await self.mongo_connector.aquery(
            "company_info", {"company_name": company_name}
        )
        if not get_basic_company_info:
            raise ServiceException(
                status=Status.NOT_FOUND, message="Company not found."
            )
        basic_info = get_basic_company_info[0]

        # Finance fields
        finance_fields = [
            ("revenue", RevenueAnalysisResponse),
            ("expenses", ExpenseAnalysisResponse),
            ("margins", ProfitMarginsResponse),
            ("valuation", ValuationEstimationResponse),
            ("funding", FundingHistoryResponse),
        ]
        finance_tasks = [
            self._llm_field(
                company_name,
                "Finance",
                fname,
                fschema,
                self.knowledge_base,
                basic_info.get("finance", {}),
            )
            for fname, fschema in finance_fields
        ]
        # Team fields
        team_fields = [
            ("team_overview", TeamOverviewResponse),
            ("individual_performance", IndividualPerformanceResponse),
            ("org_structure", OrgStructureResponse),
            ("team_growth", TeamGrowthResponse),
        ]
        team_tasks = [
            self._llm_field(
                company_name,
                "Team",
                fname,
                fschema,
                self.knowledge_base,
                basic_info.get("linkedin_team", {}),
            )
            for fname, fschema in team_fields
        ]
        # Market Analysis fields
        market_fields = [
            ("market_trends", MarketTrendsResponse),
            ("competitive_analysis", CompetitiveAnalysisResponse),
            ("growth_projections", GrowthProjectionsResponse),
            ("regional_trends", RegionalTrendsResponse),
        ]
        market_tasks = [
            self._llm_field(
                company_name,
                "MarketAnalysis",
                fname,
                fschema,
                self.knowledge_base,
                basic_info.get("market_analysis", {}),
            )
            for fname, fschema in market_fields
        ]

        # Run all field LLMs sequentially (no parallel gather)
        finance_results = []
        for task in finance_tasks:
            finance_results.append(await task)
        team_results = []
        for task in team_tasks:
            team_results.append(await task)
        market_results = []
        for task in market_tasks:
            market_results.append(await task)

        # Assemble section responses
        finance_response = FinanceResponse(
            revenue=finance_results[0],
            expenses=finance_results[1],
            margins=finance_results[2],
            valuation=finance_results[3],
            funding=finance_results[4],
        )
        team_response = LinkedInTeamResponse(
            team_overview=team_results[0],
            individual_performance=team_results[1],
            org_structure=team_results[2],
            team_growth=team_results[3],
        )
        market_response = MarketAnalysisResponse(
            market_trends=market_results[0],
            competitive_analysis=market_results[1],
            growth_projections=market_results[2],
            regional_trends=market_results[3],
        )

        return ResearchResponse(
            company_name=company_name,
            finance=finance_response,
            linkedin_team=team_response,
            market_analysis=market_response,
        )


if __name__ == "__main__":
    print(ResearchResponseWithSummary.schema_json(indent=2))
