from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime


class ChatThreadBase(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime


class ChatMessageBase(BaseModel):
    id: str
    content: str
    sender: Literal["user", "assistant", "tool"]
    timestamp: datetime


class Attachment(BaseModel):
    id: str
    name: Optional[str] = None
    type: Optional[str] = None
    size: Optional[int] = None
    url: Optional[str] = None


class Reference(BaseModel):
    title: str
    url: str


class AssociatedDocument(BaseModel):
    id: str
    name: str
    insights: List[str]
    confidence: float
    extracted_data: Dict[str, Any]


class MessageMetadata(BaseModel):
    attachments: Optional[List[Attachment]] = None
    references: Optional[List[Reference]] = None
    associated_documents: Optional[List[AssociatedDocument]] = None
    analysis: Optional[Dict[str, Any]] = None 