from backend.models.base.users import User
from backend.services.auth import AuthService
from backend.services.companies import CompaniesService
from backend.services.news import NewsService
from backend.settings import get_app_settings, AppSettings
from fastapi import Request, Depends


def get_user(request: Request):
    if "user" in request.scope:
        return request.scope["user"]

    return None

def get_news_service(
    app_settings: AppSettings = Depends(get_app_settings)):
    return NewsService(app_settings.db_config)

def get_auth_service_settings(
    app_settings: AppSettings = Depends(get_app_settings),
):
    return AuthService(app_settings.db_config, app_settings.jwt_config)

def get_company_service(
    app_settings: AppSettings = Depends(get_app_settings)
):
    return CompaniesService(app_settings.db_config)


class CommonDeps:
    user: User = Depends(get_user)