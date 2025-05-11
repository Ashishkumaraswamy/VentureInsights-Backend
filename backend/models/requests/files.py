from pydantic import BaseModel
from typing import Optional


class FileUploadInitiateRequest(BaseModel):
    filename: str
    content_type: str
    size: int
    thread_id: Optional[str] = None


class FileUploadCompleteRequest(BaseModel):
    file_id: str
    thread_id: Optional[str] = None 