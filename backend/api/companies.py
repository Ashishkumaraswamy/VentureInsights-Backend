from fastapi import APIRouter, Depends, Query
from fastapi_utils.cbv import cbv

from backend.dependencies import get_company_service
from backend.models.response.companies import (
    CompanyBaseInfo,
    FeaturedCompaniesResponse,
)
from backend.models.response.research import ResearchResponse
from backend.services.companies import CompaniesService

companies_router = APIRouter(prefix="/companies", tags=["companies"])


@cbv(companies_router)
class CompaniesAPI:
    company_service: CompaniesService = Depends(get_company_service)

    @companies_router.get("/search", response_model=list[CompanyBaseInfo])
    async def get_companies_list(self, limit: int = None) -> list[CompanyBaseInfo]:
        return await self.company_service.get_companies(limit)

    @companies_router.get("/{companyName}/analysis", response_model=ResearchResponse)
    async def get_company_analysis(self, companyName: str):
        return await self.company_service.get_company_analysis(companyName)

    @companies_router.get("/featured", response_model=FeaturedCompaniesResponse)
    async def get_featured_companies(
        self,
        limit: int = Query(None, description="Number of companies to return"),
        page: int = Query(1, description="Page number for pagination"),
    ) -> FeaturedCompaniesResponse:
        """
        Get featured investment companies.

        This endpoint returns a list of featured companies for investment consideration.
        Optional authentication via Bearer token provides personalized results.
        """
        result = await self.company_service.get_featured_companies(limit, page)
        return result
