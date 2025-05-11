from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    email: str = Field(..., description="Email address of the user")
    first_name: str = Field(..., description="First Name")
    last_name: str = Field(..., description="Last Name")
    token: str = Field(..., description="JWT Token")