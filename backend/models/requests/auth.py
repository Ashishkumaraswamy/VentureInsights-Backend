from pydantic import BaseModel, Field, SecretStr
from typing import Optional


class SignUpRequest(BaseModel):
    first_name: str = Field(..., description="First name of the user")
    last_name: str = Field(..., description="Last name of the user")
    email: str = Field(..., description="Email address of the user")
    password: SecretStr = Field(..., description="Password of the user")
    user_type: str = Field(..., description="Type of user: 'vc' or 'founder'")


class LoginRequest(BaseModel):
    email: str = Field(..., description="Email address of the user")
    password: SecretStr = Field(..., description="Password of the user")


class PersonalInfo(BaseModel):
    first_name: str = Field(..., description="First name of the founder")
    last_name: str = Field(..., description="Last name of the founder")
    email: str = Field(..., description="Email address of the founder")
    password: SecretStr = Field(..., description="Password of the founder")
    linkedin_url: str = Field(..., description="LinkedIn profile URL of the founder")
    role: str = Field(..., description="Role of the founder in the company")
    phone_number: str = Field(..., description="Phone number of the founder")


class CompanyInfo(BaseModel):
    company_name: str = Field(..., description="Name of the company")
    industry: str = Field(..., description="Industry of the company")
    stage: str = Field(..., description="Funding stage of the company")
    city: str = Field(..., description="City where the company is based")
    country: str = Field(..., description="Country where the company is based")


class FundingDetails(BaseModel):
    funding_amount: str = Field(..., description="Amount of funding requested")
    funding_purpose: str = Field(..., description="Purpose of the funding")
    timeline: str = Field(..., description="Timeline for the funding")


class CompanyStatus(BaseModel):
    is_incorporated: bool = Field(
        ..., description="Whether the company is incorporated"
    )
    website_url: Optional[str] = Field(None, description="URL of the company website")
    description: str = Field(..., description="Description of the company")


class Documents(BaseModel):
    pitch_deck_file_id: Optional[str] = Field(
        None, description="File ID of the pitch deck"
    )
    business_plan_file_id: Optional[str] = Field(
        None, description="File ID of the business plan"
    )
    financial_model_file_id: Optional[str] = Field(
        None, description="File ID of the financial model"
    )
    product_demo_file_id: Optional[str] = Field(
        None, description="File ID of the product demo"
    )


class FounderSignupRequest(BaseModel):
    personal_info: PersonalInfo
    company_info: CompanyInfo
    funding_details: FundingDetails
    company_status: CompanyStatus
    documents: Optional[Documents] = Field(None, description="Document file IDs")
