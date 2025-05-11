from fastapi import APIRouter
from fastapi.params import Depends
from fastapi_utils.cbv import cbv

from backend.dependencies import get_news_service
from backend.models.response.news import NewsItem
from backend.services.news import NewsService

news_router = APIRouter(prefix="/news", tags=["news"])

@cbv(news_router)
class NewsAPI:
    news_service: NewsService = Depends(get_news_service)

    @news_router.get("/trending", response_model=list[NewsItem])
    async def get_trending_news(self, limit: int = 10) -> list[NewsItem]:
        return await self.news_service.get_news(limit)