from backend.settings import LLMConfig
from phi.model.azure import AzureOpenAIChat

def get_model(llm_config: LLMConfig):
    return AzureOpenAIChat(
        id="gpt-4o",
        api_key=llm_config.api_key,
        azure_endpoint=llm_config.api_base,
        azure_deployment=llm_config.llm_deployment_name
    )