from agno.agent import Agent
from agno.tools.mcp import MCPTools
from backend.settings import LLMConfig
from backend.utils.llm import get_model
from backend.settings import MongoConnectionDetails
import asyncio
from typing import List, Optional, Union

from backend.models.requests.chat import SendMessageRequest, CreateThreadRequest
from backend.models.response.chat import (
    ChatThread,
    ChatThreadWithMessages,
    MessageResponse,
)
from backend.utils.logger import get_logger
from agno.storage.mongodb import MongoDbStorage
from agno.run.response import RunResponse
import uuid
from backend.models.base.chat import MessageMetadata, AgnoMessage
from fastapi.responses import StreamingResponse
import json
from typing import AsyncGenerator

LOG = get_logger("Chat Service")


class ChatService:
    def __init__(
        self, llm_config: LLMConfig, db_config: MongoConnectionDetails, mcp_url: str
    ):
        self.llm_config = llm_config
        self.db_config = db_config
        self.mcp_url = mcp_url
        self.storage_agent = MongoDbStorage(
            collection_name="chat_agent",
            db_name=db_config.dbname,
            db_url=db_config.get_connection_string(),
        )

    @staticmethod
    def system_agent_prompt():
        return "You are a helpful AI assistant that uses Venture Insights tools to analyze companies and markets."

    @staticmethod
    def system_prompt():
        return (
            "Guidelines for using these tools:"
            "1. Always use company_name for company-specific analyses"
            "2. Include domain, region, or industry parameters when they would help narrow the analysis"
            "3. When analyzing trends over time, provide start_date and end_date parameters"
            "4. For specific categories or products, include those parameters when available"
            "5. Begin your analysis by identifying which tool will provide the most relevant information"
            "6. Use multiple tools when necessary to provide comprehensive insights"
        )

    async def process_query(
        self,
        user_message: str,
        thread_id: str,
        user_id: str,
        stream: bool = False,
        markdown: bool = False,
    ) -> RunResponse:
        """Process a user query using the MCP tools."""

        async with MCPTools(
            url=self.mcp_url, transport="streamable-http", timeout_seconds=300
        ) as mcp_tools:
            agent = Agent(
                session_id=thread_id,
                user_id=user_id,
                model=get_model(self.llm_config),
                tools=[mcp_tools],
                markdown=markdown,
                description=self.system_agent_prompt(),
                instructions=self.system_prompt(),
                storage=self.storage_agent,
                add_history_to_messages=True,
                num_history_runs=3,
            )
            response = await agent.arun(user_message, stream=stream)
            return response

    async def run_interactive(
        self,
        user_message: str,
        thread_id: str,
        user_id: str,
        stream: bool = True,
        markdown: bool = False,
    ) -> None:
        """Run the agent with streamed response."""

        async with MCPTools(
            url=self.mcp_url, transport="streamable-http", timeout_seconds=300
        ) as mcp_tools:
            agent = Agent(
                session_id=thread_id,
                user_id=user_id,
                model=get_model(self.llm_config),
                tools=[mcp_tools],
                markdown=markdown,
                description=self.system_agent_prompt(),
                instructions=self.system_prompt(),
                storage=self.storage_agent,
                add_history_to_messages=True,
                num_history_runs=3,
            )
            await agent.aprint_response(user_message, stream=stream)

    async def get_threads(
        self, limit: int = 10, offset: int = 0, user_id: Optional[str] = None
    ) -> tuple[List[ChatThread], int]:
        pass

    async def create_thread(self, request: CreateThreadRequest) -> ChatThread:
        pass

    async def get_thread(self, thread_id: str) -> ChatThreadWithMessages:
        pass

    async def add_message(
        self, thread_id: str, message: SendMessageRequest, stream: bool
    ) -> Union[MessageResponse, StreamingResponse]:
        if not stream:
            # Non-streaming implementation (what you already have)
            agent_response = await self.process_query(
                user_message=message.content,
                thread_id=thread_id,
                user_id=message.user_id,
                stream=stream,
            )

            return MessageResponse(
                id=str(uuid.uuid4()),
                content=agent_response.content,
                sender="assistant",
                metadata=MessageMetadata(
                    tools=agent_response.tools,
                    formatted_tool_calls=agent_response.formatted_tool_calls,
                    citations=agent_response.citations,
                    messages=[
                        AgnoMessage(role=message.role, content=message.content)
                        for message in agent_response.messages
                    ],
                    model=agent_response.model,
                ),
                user_id=message.user_id,
                user_name=message.user_name,
            )
        else:

            async def response_generator() -> AsyncGenerator[str, None]:
                # Start the streaming process
                agent_response_stream = await self.process_query(
                    user_message=message.content,
                    thread_id=thread_id,
                    user_id=message.user_id,
                    stream=True,
                )

                # Initialize variables to collect information during streaming
                full_content = ""

                # Process the stream
                async for chunk in agent_response_stream:
                    # Accumulate the full content
                    if isinstance(chunk, str):
                        full_content += chunk
                        # Format each chunk as SSE data
                        yield f"data: {json.dumps({'content': chunk})}\n\n"
                    else:
                        # If chunk is an object with attributes
                        if hasattr(chunk, "content"):
                            if chunk.content:
                                full_content += chunk.content
                                yield f"data: {json.dumps({'content': chunk.content})}\n\n"

                # After streaming is complete, send the final message with complete metadata
                # Use whatever metadata we've collected or provide defaults
                final_message = MessageResponse(
                    id=str(uuid.uuid4()),
                    content=full_content,
                    sender="assistant",
                    user_id=message.user_id,
                    user_name=message.user_name,
                )

                yield f"data: {json.dumps(final_message.model_dump_json())}\n\n"
                yield "data: [DONE]\n\n"

            return StreamingResponse(
                response_generator(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Content-Type": "text/event-stream",
                },
            )


if __name__ == "__main__":
    from dotenv import load_dotenv
    from backend.settings import get_app_settings

    async def main():
        load_dotenv()

        app_settings = get_app_settings()

        agent = ChatService(
            llm_config=app_settings.llm_config,
            db_config=app_settings.db_config,
            mcp_url=app_settings.mcp_url,
        )

        await agent.run_interactive(
            user_message="What's the revenue analysis for Datagenie AI?",
            thread_id="test_thread_id_2",
            user_id="test_user_id_2",
            stream=True,
        )

    asyncio.run(main())
