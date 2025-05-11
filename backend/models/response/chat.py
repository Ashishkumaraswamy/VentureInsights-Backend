from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime
from backend.models.base.chat import ChatThreadBase, ChatMessageBase, Attachment, Reference, MessageMetadata


class LastMessage(BaseModel):
    content: str
    sender: Literal["user", "assistant"]
    timestamp: datetime


class ChatThread(ChatThreadBase):
    message_count: int
    last_message: Optional[LastMessage] = None


class ChatThreadList(BaseModel):
    threads: List[ChatThread]
    total: int


class ChatThreadWithoutMessages(ChatThreadBase):
    pass


class ChatMessage(ChatMessageBase):
    metadata: Optional[MessageMetadata] = None


class ChatThreadWithMessages(ChatThreadBase):
    messages: List[ChatMessage]


class MessageResponse(ChatMessageBase):
    metadata: Optional[MessageMetadata] = None


class AnalysisResponse(BaseModel):
    summary: str
    confidence: float
    sources: List[Dict[str, str]]


class AssistantMessageResponse(ChatMessageBase):
    metadata: MessageMetadata = MessageMetadata(
        references=[],
        analysis={}
    )


class FileUploadInitiateResponse(BaseModel):
    file_id: str
    upload_url: str
    expires: datetime


class FileUploadCompleteResponse(BaseModel):
    id: str
    name: str
    type: str
    size: int
    status: Literal["processing", "ready", "error"]
    url: str
    created_at: datetime
    thread_id: Optional[str] = None
    processing_details: Dict[str, Any] 