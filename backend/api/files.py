from fastapi import APIRouter, Depends, Query, Path
from fastapi_utils.cbv import cbv
from typing import Optional

from backend.dependencies import get_files_service
from backend.models.requests.files import FileUploadInitiateRequest, FileUploadCompleteRequest
from backend.models.response.files import (
    FileUploadInitiateResponse,
    FileResponse,
    FileListResponse,
)
from backend.services.files import FilesService

files_router = APIRouter(prefix="/files", tags=["files"])


@cbv(files_router)
class FilesAPI:
    files_service: FilesService = Depends(get_files_service)

    @files_router.post("/upload/initiate", response_model=FileUploadInitiateResponse)
    async def initiate_upload(self, request: FileUploadInitiateRequest) -> FileUploadInitiateResponse:
        """Initiate a file upload process and get a temporary upload URL"""
        result = await self.files_service.initiate_upload(
            request.filename,
            request.content_type,
            request.size,
            request.thread_id
        )
        return FileUploadInitiateResponse(
            file_id=result["file_id"],
            upload_url=result["upload_url"],
            expires=result["expires"]
        )

    @files_router.post("/upload/complete", response_model=FileResponse)
    async def complete_upload(self, request: FileUploadCompleteRequest) -> FileResponse:
        """Complete a file upload process"""
        result = await self.files_service.complete_upload(
            request.file_id,
            request.thread_id
        )
        return FileResponse(**result)

    @files_router.get("/", response_model=FileListResponse)
    async def list_files(
        self,
        thread_id: Optional[str] = Query(None),
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0),
        status: Optional[str] = Query(None),
    ) -> FileListResponse:
        """List files with filtering and pagination"""
        result = await self.files_service.list_files(
            thread_id=thread_id,
            limit=limit,
            offset=offset,
            status=status
        )
        return FileListResponse(**result)

    @files_router.get("/{file_id}", response_model=FileResponse)
    async def get_file(self, file_id: str = Path(...)) -> FileResponse:
        """Get file details, status, and analysis if available"""
        result = await self.files_service.get_file(file_id)
        return FileResponse(**result) 