from backend.settings import MongoConnectionDetails
from backend.models.response.companies import (
    CompanyBaseInfo,
)
from backend.utils.cache_decorator import cacheable
from backend.database.mongo import MongoDBConnector
from backend.models.response.research import (
    ResearchResponse,
)
import json
import os
from typing import Optional


class CompaniesService:
    def __init__(self, mongo_config: MongoConnectionDetails):
        self.mongo_config = mongo_config
        self.mongo_db = MongoDBConnector(mongo_config)
        # cache_service will be injected by the dependency injection system

    async def get_company_analysis(self, company_name: str) -> ResearchResponse:
        """
        Retrieve company analysis data from MongoDB.

        Args:
            company_name (str): Name of the company to retrieve research for

        Returns:
            ResearchResponse: The research data for the company
        """
        try:
            # Query MongoDB for the research data
            collection_name = "company_info"
            print(f">>> Querying collection: {collection_name}")

            # Get the document from MongoDB
            document = self.mongo_db.query(
                collection_name, {"company_name": company_name}
            )

            if not document:
                print(f">>> No research data found for {company_name}")
                return ResearchResponse(company_name=company_name)
            document = document[0]
            # Convert MongoDB document to ResearchResponse
            print(f">>> Found research data for {company_name}")
            print(document)

            # Create the research response from the document
            # discard the _id field
            document = {k: v for k, v in document.items() if k != "_id"}
            research_response = ResearchResponse(**document)

            return research_response

        except Exception as e:
            print(f">>> ERROR retrieving research data: {str(e)}")
            # Return empty ResearchResponse with just the company name
            return ResearchResponse(company_name=company_name)

    @cacheable()
    async def get_companies(self, limit: int = None) -> list[CompanyBaseInfo]:
        mock_companies = [
            {
                "name": "DataGenie",
                "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQS7QDxSkojyltJTl6vIloCWUDzmtohbDsWCg&s",
                "founder": "Ashish Verma",
                "headquarters": "San Francisco, CA, USA",
                "founding_date": "2020-01-01T00:00:00",
                "members_count": 10,
            },
            {
                "name": "Meta",
                "logo": "https://m.economictimes.com/thumb/msid-111856636,width-1200,height-900,resizemode-4,imgsize-155652/a-microsoft-logo.jpg",
                "founder": "Mark Zuckerberg",
                "headquarters": "Menlo Park, CA, USA",
                "founding_date": "2015-01-01T00:00:00",
                "members_count": 50,
            },
            {
                "name": "CypherD",
                "logo": "https://play-lh.googleusercontent.com/-dmoFW03JcyJihlNoguKe5mZBGSigpDGVlZKkJi6EhDLnzvUJQMIUhw3l6TrCW6CksE",
                "founder": "John Doe",
                "headquarters": "New York, NY, USA",
                "founding_date": "2015-01-01T00:00:00",
                "members_count": 50,
            },
            {
                "name": "PayPal",
                "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZ0ffI8EqxD3ClancA6PDjV_Blp1dZuZv_HVb6KkSXn1Z3i9fAdz4i1WBmun75iVpQU38&usqp=CAU",
                "founder": "Elon Musk, Peter Thiel, Max Levchin",
                "headquarters": "San Jose, CA, USA",
                "founding_date": "2015-01-01T00:00:00",
                "members_count": 50,
            },
        ]
        return [CompanyBaseInfo(**company) for company in mock_companies]

    async def get_featured_companies(
        self, limit: Optional[int] = None, page: int = 1
    ) -> dict:
        """
        Get featured companies for display on the homepage or featured section

        Args:
            limit: Optional number of companies to return
            page: Page number for pagination

        Returns:
            Dictionary with companies, total count, page number and limit
        """
        # Load sample data from JSON file
        json_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "data", "sample_card.json"
        )

        with open(json_path, "r") as f:
            companies_data = json.load(f)

        # Apply pagination if limit is provided
        total = len(companies_data)

        if limit:
            # Calculate start and end indices for pagination
            start_idx = (page - 1) * limit
            end_idx = start_idx + limit

            # Slice the data
            paginated_data = companies_data[start_idx:end_idx]
        else:
            paginated_data = companies_data
            limit = total

        return {
            "companies": paginated_data,
            "total": total,
            "page": page,
            "limit": limit,
        }
