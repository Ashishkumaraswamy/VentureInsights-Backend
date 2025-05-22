from backend.agents.document_processing import DocumentProcessingEngine
from backend.agents.vector_store import VectorStore
from backend.models.base.users import User
from backend.services.auth import AuthService
from backend.services.companies import CompaniesService
from backend.services.news import NewsService
from backend.services.chat import ChatService
from backend.services.files import FilesService
from backend.settings import get_app_settings, AppSettings
from fastapi import Request, Depends
from backend.services.finance import FinanceService
from backend.services.market_analysis import MarketAnalysisService
from backend.services.linkedin_team import LinkedInTeamService
from backend.services.customer_sentiment import CustomerSentimentService
from backend.utils.llm import get_model
from backend.services.knowledge import KnowledgeBaseService
from backend.services.partnership_network import PartnershipNetworkService
from backend.services.regulatory_compliance import RegulatoryComplianceService
from backend.services.risk_analysis import RiskAnalysisService
from backend.services.research import ResearchService


def get_user(request: Request):
    if "user" in request.scope:
        return request.scope["user"]

    return None

def get_knowledge_base_service(app_settings: AppSettings = Depends(get_app_settings)):
    return KnowledgeBaseService(
        app_settings.db_config,
        app_settings.vector_store_config,
    )

def get_news_service(app_settings: AppSettings = Depends(get_app_settings)):
    return NewsService(
        app_settings.db_config, app_settings.llm_config, app_settings.sonar_config
    )


def get_auth_service_settings(
    app_settings: AppSettings = Depends(get_app_settings),
):
    return AuthService(app_settings.db_config, app_settings.jwt_config)


def get_company_service(app_settings: AppSettings = Depends(get_app_settings)):
    return CompaniesService(app_settings.db_config)


def get_chat_service(app_settings: AppSettings = Depends(get_app_settings)):
    return ChatService(app_settings.db_config)


def get_document_processing_engine(
    app_settings: AppSettings = Depends(get_app_settings),
):
    return DocumentProcessingEngine(
        get_model(app_settings.llm_config), app_settings.storage_config
    )


def get_vector_store(app_settings: AppSettings = Depends(get_app_settings)):
    return VectorStore(app_settings.db_config, app_settings.vector_store_config)


def get_files_service(
    doc_engine=Depends(get_document_processing_engine),
    vector_store=Depends(get_vector_store),
    app_settings: AppSettings = Depends(get_app_settings),
):
    return FilesService(
        doc_engine=doc_engine,
        vector_store=vector_store,
        mongo_config=app_settings.db_config,
    )


def get_finance_service(app_settings: AppSettings = Depends(get_app_settings), knowledge_base_service=Depends(get_knowledge_base_service)):
    return FinanceService(app_settings.llm_config, app_settings.sonar_config, knowledge_base_service)


def get_market_analysis_service(app_settings: AppSettings = Depends(get_app_settings)):
    return MarketAnalysisService(app_settings.llm_config, app_settings.sonar_config)


def get_linkedin_team_service(app_settings: AppSettings = Depends(get_app_settings), ):
    return LinkedInTeamService(app_settings.llm_config, app_settings.sonar_config, )


def get_customer_sentiment_service(
    app_settings: AppSettings = Depends(get_app_settings),
):
    return CustomerSentimentService(app_settings.llm_config, app_settings.sonar_config)


def get_partnership_network_service():
    return PartnershipNetworkService()

def get_regulatory_compliance_service():
    return RegulatoryComplianceService()

def get_risk_analysis_service():
    return RiskAnalysisService()

def get_research_service(
    finance_service=Depends(get_finance_service),
    linkedin_team_service=Depends(get_linkedin_team_service),
    market_analysis_service=Depends(get_market_analysis_service),
    partnership_network_service=Depends(get_partnership_network_service),
    customer_sentiment_service=Depends(get_customer_sentiment_service),
    regulatory_compliance_service=Depends(get_regulatory_compliance_service),
    risk_analysis_service=Depends(get_risk_analysis_service),
):
    return ResearchService(
        finance_service=finance_service,
        linkedin_team_service=linkedin_team_service,
        market_analysis_service=market_analysis_service,
        partnership_network_service=partnership_network_service,
        customer_sentiment_service=customer_sentiment_service,
        regulatory_compliance_service=regulatory_compliance_service,
        risk_analysis_service=risk_analysis_service,
    )


class CommonDeps:
    user: User = Depends(get_user)
