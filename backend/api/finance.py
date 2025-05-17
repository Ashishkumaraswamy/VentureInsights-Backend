from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from backend.dependencies import get_finance_service
from backend.services.finance import FinanceService
from backend.models.requests.finance import (
    RevenueAnalysisRequest,
    ExpenseAnalysisRequest,
    ProfitMarginsRequest,
    ValuationEstimationRequest,
    FundingHistoryRequest,
)
from backend.models.response.finance import (
    RevenueAnalysisResponse,
    ExpenseAnalysisResponse,
    ProfitMarginsResponse,
    ValuationEstimationResponse,
    FundingHistoryResponse,
)

finance_router = APIRouter(prefix="/finance", tags=["finance"])


@cbv(finance_router)
class FinanceCBV:
    finance_service: FinanceService = Depends(get_finance_service)

    @finance_router.post("/revenue-analysis", response_model=RevenueAnalysisResponse)
    async def get_finance(self, req: RevenueAnalysisRequest):
        return await self.finance_service.get_revenue_analysis()

    @finance_router.post("/expense-analysis", response_model=ExpenseAnalysisResponse)
    async def get_expense_analysis(self, req: ExpenseAnalysisRequest):
        return await self.finance_service.get_expense_analysis()

    @finance_router.post("/profit-margins", response_model=ProfitMarginsResponse)
    async def get_profit_margins(self, req: ProfitMarginsRequest):
        return await self.finance_service.get_profit_margins()

    @finance_router.post(
        "/valuation-estimation", response_model=ValuationEstimationResponse
    )
    async def get_valuation_estimation(self, req: ValuationEstimationRequest):
        return await self.finance_service.get_valuation_estimation()

    @finance_router.post("/funding-history", response_model=FundingHistoryResponse)
    async def get_funding_history(self, req: FundingHistoryRequest):
        return await self.finance_service.get_funding_history()
