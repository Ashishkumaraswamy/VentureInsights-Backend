from fastapi import APIRouter
from fastapi.params import Depends
from fastapi_utils.cbv import cbv
from starlette import status

from backend.dependencies import get_auth_service_settings
from backend.models.requests.auth import (
    SignUpRequest,
    LoginRequest,
    FounderSignupRequest,
)
from backend.services.auth import AuthService
from backend.utils.logger import get_logger

auth_router = APIRouter(prefix="/auth", tags=["auth"])

LOG = get_logger("Auth API")


@cbv(auth_router)
class AuthorizationApi:
    auth_service: AuthService = Depends(get_auth_service_settings)

    @auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
    async def signup(self, signup_request: SignUpRequest):
        return await self.auth_service.signup(signup_request)

    @auth_router.post("/login", status_code=status.HTTP_200_OK)
    async def login(self, login_request: LoginRequest):
        return await self.auth_service.login(login_request)

    @auth_router.post("/founder-signup", status_code=status.HTTP_201_CREATED)
    async def founder_signup(self, founder_signup_request: FounderSignupRequest):
        LOG.info(f"request{founder_signup_request}")
        return await self.auth_service.founder_signup(founder_signup_request)
