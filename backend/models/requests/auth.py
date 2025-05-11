from pydantic import BaseModel, Field, SecretStr


class SignUpRequest(BaseModel):
    first_name: str = Field(..., description="First name of the user")
    last_name: str = Field(..., description="Last name of the user")
    email: str = Field(..., description="Email address of the user")
    password: SecretStr = Field(..., description="Password of the user")


class LoginRequest(BaseModel):
    email: str = Field(..., description="Email address of the user")
    password: SecretStr = Field(..., description="Password of the user")
