from backend.settings import LLMConfig

# from phi.model.azure import AzureOpenAIChat
from agno.models.azure import AzureOpenAI


def get_model(llm_config: LLMConfig):
    return AzureOpenAI(
        id="gpt-4o",
        api_key=llm_config.api_key,
        azure_endpoint=llm_config.api_base,
        azure_deployment=llm_config.llm_deployment_name,
    )
