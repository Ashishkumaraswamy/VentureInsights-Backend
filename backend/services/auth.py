from starlette import status

from backend.models.base.exceptions import Status
from backend.models.requests.auth import SignUpRequest, LoginRequest
from backend.settings import MongoConnectionDetails


class AuthService:
    def __init__(self, mongo_config: MongoConnectionDetails):
        self.mongo_config = mongo_config

    def signup(self, signup_request:SignUpRequest):
        return {
            "status": Status.SUCCESS,
            "message": "User Created Successfully"
        }

    def login(self, login_request: LoginRequest):
        return {
            "status": Status.SUCCESS,
            "message": "User Logged In Successfully",
            "token": "asadbasdbaadsba"
        }