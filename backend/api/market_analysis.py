from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from backend.services.market_analysis import MarketAnalysisService
from backend.models.requests.market_analysis import (
    MarketTrendsRequest,
    CompetitiveAnalysisRequest,
    GrowthProjectionsRequest,
    RegionalTrendsRequest,
)
from backend.models.response.market_analysis import (
    MarketTrendsResponse,
    CompetitiveAnalysisResponse,
    GrowthProjectionsResponse,
    RegionalTrendsResponse,
)

market_analysis_router = APIRouter(prefix="/market-analysis", tags=["market-analysis"])


@cbv(market_analysis_router)
class MarketAnalysisCBV:
    market_analysis_service: MarketAnalysisService = Depends(MarketAnalysisService)

    @market_analysis_router.post("/market-trends", response_model=MarketTrendsResponse)
    async def get_market_trends(self, req: MarketTrendsRequest):
        return await self.market_analysis_service.get_market_trends()

    @market_analysis_router.post(
        "/competitive-analysis", response_model=CompetitiveAnalysisResponse
    )
    async def get_competitive_analysis(self, req: CompetitiveAnalysisRequest):
        return await self.market_analysis_service.get_competitive_analysis()

    @market_analysis_router.post(
        "/growth-projections", response_model=GrowthProjectionsResponse
    )
    async def get_growth_projections(self, req: GrowthProjectionsRequest):
        return await self.market_analysis_service.get_growth_projections()

    @market_analysis_router.post(
        "/regional-trends", response_model=RegionalTrendsResponse
    )
    async def get_regional_trends(self, req: RegionalTrendsRequest):
        return await self.market_analysis_service.get_regional_trends()
