from datetime import datetime

from pydantic import HttpUrl, BaseModel


class NewsItem(BaseModel):
    id: str
    title: str
    content: str
    source: list[HttpUrl]
    publishedAt: datetime
    category: str
    image: HttpUrl