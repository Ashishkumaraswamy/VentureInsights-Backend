from agno.agent import Agent
from agno.tools.mcp import MCPTools
from backend.settings import LLMConfig
from backend.utils.llm import get_model
from mcp import StdioServerParameters
import asyncio


class VentureInsightsAgent:
    def __init__(self, llm_config: LLMConfig, server_params: StdioServerParameters):
        self.llm_config = llm_config
        self.server_params = server_params

    @staticmethod
    def system_prompt():
        return (
            "You are a helpful AI assistant that uses Venture Insights tools to analyze companies and markets."
            "Guidelines for using these tools:"
            "1. Always use company_name for company-specific analyses"
            "2. Include domain, region, or industry parameters when they would help narrow the analysis"
            "3. When analyzing trends over time, provide start_date and end_date parameters"
            "4. For specific categories or products, include those parameters when available"
            "5. Begin your analysis by identifying which tool will provide the most relevant information"
            "6. Use multiple tools when necessary to provide comprehensive insights"
        )

    async def process_query(self, user_message: str) -> str:
        """Process a user query using the MCP tools."""
        async with MCPTools(
            server_params=self.server_params, timeout_seconds=300
        ) as mcp_tools:
            agent = Agent(
                model=get_model(self.llm_config),
                tools=[mcp_tools],
                markdown=True,
                instructions=self.system_prompt(),
            )
            response = await agent.arun(user_message, stream=False)
            return response

    async def run_interactive(self, user_message: str) -> None:
        """Run the agent with streamed response."""
        async with MCPTools(
            server_params=self.server_params, timeout_seconds=300
        ) as mcp_tools:
            agent = Agent(
                model=get_model(self.llm_config),
                tools=[mcp_tools],
                markdown=True,
                instructions=self.system_prompt(),
            )
            await agent.aprint_response(user_message, stream=True)


if __name__ == "__main__":
    from dotenv import load_dotenv
    from backend.settings import get_app_settings

    async def main():
        load_dotenv()

        app_settings = get_app_settings()

        server_params = StdioServerParameters(
            command="/Users/mathanamathav/Library/Caches/pypoetry/virtualenvs/backend-MOHDKJyA-py3.11/bin/python",
            args=[
                "/Users/mathanamathav/PersonalProjects/hackathon/VentureInsights-Backend/mcp_server.py"
            ],
        )

        agent = VentureInsightsAgent(
            llm_config=app_settings.llm_config, server_params=server_params
        )

        # Example usage
        await agent.run_interactive(
            "What is the valuation estimation for Datagenie AI Start up also Known as code z?"
        )

    asyncio.run(main())
