from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from backend.services.customer_sentiment import CustomerSentimentService
from backend.models.requests.customer_sentiment import (
    SentimentSummaryRequest,
    CustomerFeedbackRequest,
    BrandReputationRequest,
)
from backend.models.response.customer_sentiment import (
    SentimentSummaryResponse,
    CustomerFeedbackResponse,
    BrandReputationResponse,
)

customer_sentiment_router = APIRouter(
    prefix="/customer-sentiment", tags=["customer-sentiment"]
)


@cbv(customer_sentiment_router)
class CustomerSentimentCBV:
    customer_sentiment_service: CustomerSentimentService = Depends(
        CustomerSentimentService
    )

    @customer_sentiment_router.post(
        "/sentiment-summary", response_model=SentimentSummaryResponse
    )
    async def get_sentiment_summary(self, req: SentimentSummaryRequest):
        return await self.customer_sentiment_service.get_sentiment_summary(
            company_name=req.company_name,
            domain=req.domain,
            product=req.product,
            region=req.region,
            start_date=req.start_date,
            end_date=req.end_date
        )

    @customer_sentiment_router.post(
        "/customer-feedback", response_model=CustomerFeedbackResponse
    )
    async def get_customer_feedback(self, req: CustomerFeedbackRequest):
        return await self.customer_sentiment_service.get_customer_feedback(
            company_name=req.company_name,
            domain=req.domain,
            product=req.product,
            region=req.region,
            start_date=req.start_date,
            end_date=req.end_date
        )

    @customer_sentiment_router.post(
        "/brand-reputation", response_model=BrandReputationResponse
    )
    async def get_brand_reputation(self, req: BrandReputationRequest):
        return await self.customer_sentiment_service.get_brand_reputation(
            company_name=req.company_name,
            domain=req.domain,
            region=req.region,
            start_date=req.start_date,
            end_date=req.end_date
        )
