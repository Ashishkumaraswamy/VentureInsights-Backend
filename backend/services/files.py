import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from backend.models.base.exceptions import NotFoundException


class FilesService:
    def __init__(self, db_config: Dict[str, Any]):
        self.db_config = db_config
        # Mock storage for files
        self.files = {}
        self.uploads = {}

    async def initiate_upload(
        self,
        filename: str,
        content_type: str,
        size: int,
        thread_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Initiate a file upload and return upload URL"""
        file_id = str(uuid.uuid4())
        expiry = datetime.now() + timedelta(minutes=15)

        # In a real implementation, this would generate a pre-signed URL for cloud storage
        upload_url = f"https://api.ventureinsights.com/v1/uploads/{file_id}"

        # Store upload details
        self.uploads[file_id] = {
            "filename": filename,
            "content_type": content_type,
            "size": size,
            "thread_id": thread_id,
            "status": "uploading",
            "created_at": datetime.now(),
        }

        return {"file_id": file_id, "upload_url": upload_url, "expires": expiry}

    async def complete_upload(
        self, file_id: str, thread_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Complete a file upload process"""
        if file_id not in self.uploads:
            raise NotFoundException(f"Upload with ID {file_id} not found")

        upload_info = self.uploads[file_id]

        # If thread_id is provided, update it
        if thread_id:
            upload_info["thread_id"] = thread_id

        # Create file record
        file_record = {
            "id": file_id,
            "name": upload_info["filename"],
            "type": upload_info["content_type"],
            "size": upload_info["size"],
            "status": "processing",
            "url": f"https://api.ventureinsights.com/v1/files/{file_id}",
            "created_at": upload_info["created_at"],
            "thread_id": upload_info["thread_id"],
            "processing_details": {
                "progress": 0,
                "estimated_time_remaining": 60,  # 60 seconds
            },
        }

        # Store file record
        self.files[file_id] = file_record

        # Return file info
        return file_record

    async def get_file(self, file_id: str) -> Dict[str, Any]:
        """Get file details and status"""
        if file_id not in self.files:
            raise NotFoundException(f"File with ID {file_id} not found")

        file_record = self.files[file_id]

        # In a real implementation, you would check the actual status
        # Mock the processing progress
        if file_record["status"] == "processing":
            progress = file_record["processing_details"]["progress"]
            # Simulate progress
            if progress < 100:
                file_record["processing_details"]["progress"] = min(100, progress + 20)
                file_record["processing_details"]["estimated_time_remaining"] = max(
                    0, 60 - progress
                )
            else:
                file_record["status"] = "ready"
                file_record["processing_details"] = {}

                # Add analysis data for ready files
                file_record["analysis"] = {
                    "summary": f"This is a summary of the file {file_record['name']}",
                    "keyPoints": ["Key point 1", "Key point 2", "Key point 3"],
                    "sentiment": "positive",
                    "extractedEntities": [
                        {
                            "type": "company",
                            "value": "Example Corp",
                            "confidence": 0.95,
                            "relevance": 0.9,
                            "context": "Example Corp reported strong Q2 earnings",
                        }
                    ],
                    "documentStructure": {
                        "sections": [
                            {
                                "title": "Executive Summary",
                                "content": "Summary content here",
                                "pageNumbers": [1, 2],
                            }
                        ],
                        "tables": [
                            {
                                "title": "Financial Results",
                                "data": [["Q1", "Q2", "Q3"], ["100", "200", "300"]],
                                "pageNumber": 3,
                            }
                        ],
                        "figures": [
                            {
                                "title": "Growth Chart",
                                "description": "Annual growth trend",
                                "pageNumber": 4,
                            }
                        ],
                    },
                }

        return file_record

    async def list_files(
        self,
        thread_id: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List files with filters and pagination"""
        files_list = list(self.files.values())

        # Apply filters
        if thread_id:
            files_list = [f for f in files_list if f.get("thread_id") == thread_id]

        if status:
            files_list = [f for f in files_list if f.get("status") == status]

        # Sort by created_at desc
        files_list.sort(key=lambda x: x["created_at"], reverse=True)

        # Apply pagination
        paginated_files = files_list[offset : offset + limit]

        # Simplify response for list view
        simplified_files = []
        for file in paginated_files:
            simplified = {k: v for k, v in file.items() if k != "analysis"}
            if "processing_details" in simplified and simplified["status"] == "ready":
                del simplified["processing_details"]
            simplified_files.append(simplified)

        return {"files": simplified_files, "total": len(files_list)}
