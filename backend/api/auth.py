from fastapi import APIRouter
from fastapi.params import Depends
from fastapi_utils.cbv import cbv
from starlette import status

from backend.dependencies import get_auth_service_settings
from backend.models.requests.auth import SignUpRequest, LoginRequest
from backend.services.auth import AuthService

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@cbv(auth_router)
class AuthorizationApi:
    auth_service: AuthService = Depends(get_auth_service_settings)

    @auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
    def signup(self, signup_request: SignUpRequest):
        return self.auth_service.signup(signup_request)

    @auth_router.post("/login", status_code=status.HTTP_200_OK)
    def login(self, login_request: LoginRequest):
        return self.auth_service.login(login_request)
