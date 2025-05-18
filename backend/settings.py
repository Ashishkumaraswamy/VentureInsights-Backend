import os
from functools import lru_cache
from typing import Optional

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MongoConnectionDetails(BaseModel):
    host: str = Field(..., description="Host name for the database")
    user: str = Field(..., description="Username to use for connecting")
    password: str = Field(..., description="Password to connect to the db")
    port: int = Field(..., description="Database port to use")
    dbname: str = Field(..., description="Database name")

    def get_connection_string(self):
        return f"mongodb+srv://{self.user}:{self.password}@{self.host}/"

    def __str__(self):
        return self.get_connection_string()


class LLMConfig(BaseModel):
    api_key: str = Field(..., description="API key for the LLM service")
    api_base: str = Field(..., description="Base URL for the LLM service")
    api_version: str = Field(..., description="API version for the LLM service")
    llm_deployment_name: str = Field(
        ..., description="LLM deployment name for the LLM service"
    )


class SonarConfig(BaseModel):
    base_url: str = Field(..., description="Perplexity base URL")
    api_key: str = Field(..., description="Sonar API Key")


class JWTConfig(BaseModel):
    secret_key: str = Field(..., description="Secret key for JWT")
    algorithm: str = Field(..., description="Algorithm for JWT")
    expire_after: int = Field(..., description="Validity for the JWT token in minutes")


class AppSettings(BaseSettings):
    db_config: MongoConnectionDetails = Field(
        ..., description="MongoDB connection details"
    )
    llm_config: LLMConfig = Field(..., description="LLM configuration details")
    sonar_config: SonarConfig = Field(..., description="Sonar configuration details")
    jwt_config: JWTConfig = Field(..., description="JWT configuration details")
    local_user_email: Optional[str] = Field(None, description="Local user mail id")
    local: bool = Field(False, description="Local mode")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        yaml_file="config.yaml",
        extra="ignore",
    )

    @classmethod
    def get_from_config(cls, config_path: str = "../config.yaml"):
        with open(config_path) as file:
            yaml_data = yaml.safe_load(file)
            return cls(**yaml_data)

    @classmethod
    def get_from_env(cls):
        return cls(
            db_config=MongoConnectionDetails(
                host=os.environ.get("DB__HOST"),
                dbname=os.environ.get("DB__DBNAME"),
                port=os.environ.get("DB__PORT"),
                user=os.environ.get("DB__USER"),
                password=os.environ.get("DB__PASSWORD"),
            ),
            llm_config=LLMConfig(
                api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
                api_base=os.environ.get("AZURE_OPENAI_API_BASE"),
                api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
                llm_deployment_name=os.environ.get("OPENAI_LLM_DEPLOYMENT_NAME"),
            ),
            sonar_config=SonarConfig(
                base_url=os.environ.get("SONAR_BASE_URL"),
                api_key=os.environ.get("SONAR_API_KEY"),
            ),
            jwt_config=JWTConfig(
                secret_key=os.environ.get("JWT_SECRET_KEY"),
                algorithm=os.environ.get("JWT_ALGORITHM"),
                expire_after=os.environ.get("JWT_TOKEN_EXPIRY_MINUTES"),
            ),
            local_user=os.environ.get("LOCAL_USER"),
            local=os.environ.get("LOCAL"),
        )


@lru_cache
def get_app_settings():
    return AppSettings.get_from_env()
