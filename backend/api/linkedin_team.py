from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from backend.services.linkedin_team import LinkedInTeamService
from backend.models.requests.linkedin_team import (
    TeamOverviewRequest,
    IndividualPerformanceRequest,
    OrgStructureRequest,
    TeamGrowthRequest,
)
from backend.models.response.linkedin_team import (
    TeamOverviewResponse,
    IndividualPerformanceResponse,
    OrgStructureResponse,
    TeamGrowthResponse,
)

linkedin_team_router = APIRouter(prefix="/linkedin-team", tags=["linkedin-team"])


@cbv(linkedin_team_router)
class LinkedInTeamCBV:
    linkedin_team_service: LinkedInTeamService = Depends(LinkedInTeamService)

    @linkedin_team_router.post("/team-overview", response_model=TeamOverviewResponse)
    async def get_team_overview(self, req: TeamOverviewRequest):
        return await self.linkedin_team_service.get_team_overview()

    @linkedin_team_router.post(
        "/individual-performance", response_model=IndividualPerformanceResponse
    )
    async def get_individual_performance(self, req: IndividualPerformanceRequest):
        return await self.linkedin_team_service.get_individual_performance()

    @linkedin_team_router.post("/org-structure", response_model=OrgStructureResponse)
    async def get_org_structure(self, req: OrgStructureRequest):
        return await self.linkedin_team_service.get_org_structure()

    @linkedin_team_router.post("/team-growth", response_model=TeamGrowthResponse)
    async def get_team_growth(self, req: TeamGrowthRequest):
        return await self.linkedin_team_service.get_team_growth()
