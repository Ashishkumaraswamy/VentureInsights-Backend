from datetime import datetime, timedelta

import jwt
import bcrypt
from backend.database.mongo import MongoDBConnector
from backend.models.base.exceptions import Status
from backend.models.requests.auth import SignUpRequest, LoginRequest
from backend.settings import MongoConnectionDetails, JWTConfig
from backend.utils.exceptions import ServiceException
from backend.utils.logger import get_logger

LOG = get_logger()


class AuthService:
    def __init__(self, mongo_config: MongoConnectionDetails, jwt_config: JWTConfig):
        self.mongo_config = mongo_config
        self.mongo_connector = MongoDBConnector(mongo_config)
        self.jwt_config = jwt_config

    def create_auth_token(self, email: str):
        expire = datetime.now() + timedelta(minutes=self.jwt_config.expire_after)
        payload = {"sub": email, "exp": expire}
        token = jwt.encode(
            payload, self.jwt_config.secret_key, algorithm=self.jwt_config.algorithm
        )
        return token

    async def signup(self, signup_request: SignUpRequest):
        raw_password = signup_request.password.get_secret_value()
        hashed_password = bcrypt.hashpw(
            raw_password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        # Store user details in DB (example dictionary shown here)
        user_record = {
            "first_name": signup_request.first_name,
            "last_name": signup_request.last_name,
            "email": signup_request.email,
            "password": hashed_password,
        }
        collection = await self.mongo_connector.aget_collection("users")
        try:
            await collection.insert_one(user_record)
            return {"status": Status.SUCCESS, "message": "User Created Successfully"}
        except Exception as e:
            LOG.error(f"Failed to create user due to {e}")
            raise ServiceException(
                status=Status.EXECUTION_ERROR,
                message=f"Failed to create user due to {e}",
            )

    async def login(self, login_request: LoginRequest):
        user_details = await self.mongo_connector.aquery(
            "users", {"email": login_request.email}
        )
        user = user_details[0] if user_details else None

        if not user:
            return {"status": Status.NOT_FOUND, "message": "User not found"}

        raw_password = login_request.password.get_secret_value()
        hashed_password = user["password"]

        if bcrypt.checkpw(
            raw_password.encode("utf-8"), hashed_password.encode("utf-8")
        ):
            token = self.create_auth_token(user["email"])
            return {
                "status": Status.SUCCESS,
                "message": "User Logged In Successfully",
                "token": token,
            }
        else:
            return {"status": Status.INVALID_PARAM, "message": "Invalid Password"}
