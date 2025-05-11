from datetime import datetime

from pydantic import BaseModel, Field


class CompanyBaseInfo(BaseModel):
    name: str = Field(..., description="Name of the company")
    founding_date: datetime = Field(..., description="Founding Date of the company")
    members_count: int = Field(..., description="Number of members in the company")