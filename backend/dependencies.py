from backend.models.base.users import User
from backend.services.auth import AuthService
from backend.settings import get_app_settings, AppSettings
from fastapi import Request, Depends


async def get_user(request: Request):
    if "user" in request.scope:
        return request.scope["user"]

    return None


def get_auth_service_settings(
    app_settings: AppSettings = Depends(get_app_settings),
):
    return AuthService(app_settings.db_config)


class CommonDeps:
    user: User = Depends(get_user)