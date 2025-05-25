from datetime import datetime, timedelta

import jwt
import bcrypt

from backend.database.mongo import MongoDBConnector
from backend.models.base.exceptions import Status
from backend.models.requests.auth import (
    SignUpRequest,
    LoginRequest,
    FounderSignupRequest,
)
from backend.models.response.auth import UserResponse
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
            "user_type": signup_request.user_type,
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

    async def founder_signup(self, founder_signup_request: FounderSignupRequest):
        # Extract personal info
        personal_info = founder_signup_request.personal_info
        raw_password = personal_info.password.get_secret_value()
        hashed_password = bcrypt.hashpw(
            raw_password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        # Create the user record
        user_record = {
            "first_name": personal_info.first_name,
            "last_name": personal_info.last_name,
            "email": personal_info.email,
            "password": hashed_password,
            "user_type": "founder",
            "linkedin_url": personal_info.linkedin_url,
            "role": personal_info.role,
            "phone_number": personal_info.phone_number,
        }

        # Create the company record
        company_info = founder_signup_request.company_info
        funding_details = founder_signup_request.funding_details
        company_status = founder_signup_request.company_status

        company_record = {
            "founder_email": personal_info.email,
            "company_name": company_info.company_name,
            "industry": company_info.industry,
            "stage": company_info.stage,
            "city": company_info.city,
            "country": company_info.country,
            "funding_amount": funding_details.funding_amount,
            "funding_purpose": funding_details.funding_purpose,
            "timeline": funding_details.timeline,
            "is_incorporated": company_status.is_incorporated,
            "description": company_status.description,
        }

        if company_status.website_url:
            company_record["website_url"] = company_status.website_url

        # Add documents if they exist
        if founder_signup_request.documents:
            documents = founder_signup_request.documents
            company_record["documents"] = {}

            if documents.pitch_deck_file_url:
                company_record["documents"]["pitch_deck_file_url"] = (
                    documents.pitch_deck_file_url
                )

            if documents.business_plan_file_url:
                company_record["documents"]["business_plan_file_url"] = (
                    documents.business_plan_file_url
                )

            if documents.financial_model_file_url:
                company_record["documents"]["financial_model_file_url"] = (
                    documents.financial_model_file_url
                )

            if documents.product_demo_file_url:
                company_record["documents"]["product_demo_file_url"] = (
                    documents.product_demo_file_url
                )

        # Insert records to DB
        try:
            users_collection = await self.mongo_connector.aget_collection("users")
            companies_collection = await self.mongo_connector.aget_collection(
                "companies"
            )

            # Check if user already exists
            existing_user = await self.mongo_connector.aquery(
                "users", {"email": personal_info.email}
            )
            if existing_user:
                raise ServiceException(
                    status=Status.ALREADY_EXISTS,
                    message="User with this email already exists",
                )

            # Insert user and company data
            await users_collection.insert_one(user_record)
            await companies_collection.insert_one(company_record)

            return {
                "status": Status.SUCCESS,
                "message": "Founder and Company Created Successfully",
            }
        except ServiceException:
            raise
        except Exception as e:
            LOG.error(f"Failed to create founder due to {e}")
            raise ServiceException(
                status=Status.EXECUTION_ERROR,
                message=f"Failed to create founder due to {e}",
            )

    async def login(self, login_request: LoginRequest):
        user_details = await self.mongo_connector.aquery(
            "users", {"email": login_request.email}
        )
        user = user_details[0] if user_details else None

        if not user:
            raise ServiceException(Status.NOT_FOUND, message="User Not Found")

        raw_password = login_request.password.get_secret_value()
        hashed_password = user["password"]

        if bcrypt.checkpw(
            raw_password.encode("utf-8"), hashed_password.encode("utf-8")
        ):
            token = self.create_auth_token(user["email"])
            return UserResponse(
                email=user["email"],
                first_name=user["first_name"],
                last_name=user["last_name"],
                token=token,
                user_type=user["user_type"],
            )
        else:
            raise ServiceException(Status.UNAUTHORIZED, message="Invalid Password")
