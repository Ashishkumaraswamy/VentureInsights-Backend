from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from backend.dependencies import get_company_service
from backend.models.response.companies import (
    CompanyBaseInfo,
    CompanyAnalysisFullResponse,
)
from backend.services.companies import CompaniesService

companies_router = APIRouter(prefix="/companies", tags=["companies"])


@cbv(companies_router)
class CompaniesAPI:
    company_service: CompaniesService = Depends(get_company_service)

    @companies_router.get("/search", response_model=list[CompanyBaseInfo])
    async def get_companies_list(self, limit: int = None) -> list[CompanyBaseInfo]:
        return await self.company_service.get_companies(limit)

    @companies_router.get(
        "/{companyName}/analysis", response_model=CompanyAnalysisFullResponse
    )
    async def get_company_analysis(self, companyName: str):
        return await self.company_service.get_company_analysis(companyName)
