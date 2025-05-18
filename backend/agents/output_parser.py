from typing import Type

from agno.models.azure import AzureOpenAI
from pydantic import BaseModel
from agno.agent import Agent


class LLMOutputParserAgent:
    """
    Agent that takes a string (LLM output) and a response model class, and uses an LLM to convert the string into a valid instance of the response model.
    """

    def __init__(self, model: AzureOpenAI):
        self.model = model

    def parse(self, content: str, response_model: Type[BaseModel]) -> BaseModel:
        """
        Given a string and a response model class, use the LLM to convert the string into the response model structure.
        """
        agent = Agent(
            model=self.model,
            instructions="""
            You are a strict output parser.

                1.Your task is to convert the given content into a valid instance of the specified Pydantic model. You must:
                2.Parse the content strictly according to the provided model schema.
                3.Ensure all required fields are correctly extracted and typed.
                4. Return only the parsed result as a JSON object, which should be directly convertible into an instance of the Pydantic model.
                
                Do not include any explanations, formatting, or text outside the JSON object.
            """,
            response_model=response_model,
        )
        response = agent.run(f"Parse this content: {content}")
        return response.content
