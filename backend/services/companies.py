from datetime import datetime

from backend.models.response.companies import CompanyBaseInfo
from backend.settings import MongoConnectionDetails


class CompaniesService:

    def __init__(self, mongo_config: MongoConnectionDetails):
        self.mongo_config = mongo_config

    async def get_companies(self, limit: int = None) -> list[CompanyBaseInfo]:
        return [
            CompanyBaseInfo(
                name="DataGenie",
                founding_date=datetime(2020, 1, 1),
                members_count=10
            ),
            CompanyBaseInfo(
                name="VentureInsights",
                founding_date=datetime(2015, 1, 1),
                members_count=50
            ),
            CompanyBaseInfo(
                name="CypherD",
                founding_date=datetime(2015, 1, 1),
                members_count=50
            ),
            CompanyBaseInfo(
                name="Test",
                founding_date=datetime(2015, 1, 1),
                members_count=50
            ),
        ]
