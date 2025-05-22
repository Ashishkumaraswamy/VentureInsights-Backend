from typing import Dict, Any
import os
from backend.models.base.exceptions import NotFoundException
from backend.agents.document_processing import DocumentProcessingEngine
from backend.agents.vector_store import VectorStore
from backend.models.response.files import CompanyDocumentsResponse
from backend.settings import MongoConnectionDetails
from backend.database.mongo import MongoDBConnector


class FilesService:
    def __init__(
        self,
        doc_engine: DocumentProcessingEngine,
        vector_store: VectorStore,
        mongo_config: MongoConnectionDetails,
    ):
        self.doc_engine = doc_engine
        self.vector_store = vector_store
        self.mongo_config = mongo_config
        self.mongo_connector = MongoDBConnector(mongo_config)

    async def upload_file(self, file, company_name: str) -> Dict[str, Any]:
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())
        # cloud_url = self.doc_engine.upload_to_cloudinary(temp_path)
        cloud_url = ""
        documents = self.doc_engine.extract_text(temp_path, file.filename, company_name)
        await self.vector_store.add_documents(documents)
        os.remove(temp_path)
        # Add the public URL to the company_docs collection
        self.mongo_connector.update_records(
            "company_docs",
            {"company_name": company_name},
            {"$addToSet": {"document_urls": cloud_url}},
        )
        return {"cloud_url": cloud_url}

    async def get_company_docs(self, company_name: str) -> CompanyDocumentsResponse:
        company_docs_collection = self.mongo_connector.db["company_docs"]
        doc = company_docs_collection.find_one({"company_name": company_name})
        if not doc:
            raise NotFoundException("Company not found")
        return CompanyDocumentsResponse(
            company_name=company_name, document_urls=doc.get("document_urls", [])
        )

    async def download_file(self, cloud_url: str) -> str:
        temp_path = "/tmp/downloaded_file"
        self.doc_engine.download_from_cloudinary(cloud_url, temp_path)
        return temp_path
