from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class CreateThreadRequest(BaseModel):
    title: Optional[str] = None


class UpdateThreadRequest(BaseModel):
    title: str


class AttachmentRequest(BaseModel):
    id: str


class MessageContext(BaseModel):
    company_id: Optional[str] = None


class SendMessageRequest(BaseModel):
    content: str
    attachments: Optional[List[AttachmentRequest]] = None 