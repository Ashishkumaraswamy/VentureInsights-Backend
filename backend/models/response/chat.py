from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Literal, Union
from datetime import datetime
from backend.models.base.chat import ChatThreadBase, ChatMessageBase, MessageMetadata
from backend.models.response.finance import (
    RevenueAnalysisResponse,
    ExpenseAnalysisResponse,
    ProfitMarginsResponse,
)


class LastMessage(BaseModel):
    content: str
    sender: Literal["user", "assistant"]
    timestamp: datetime
    user_id: Optional[str] = None
    user_name: Optional[str] = None


class ChatThread(ChatThreadBase):
    message_count: int
    last_message: Optional[LastMessage] = None


class ChatThreadList(BaseModel):
    threads: List[ChatThread]
    total: int


class ChatThreadWithoutMessages(ChatThreadBase):
    pass


class ThreadSummary(ChatThreadBase):
    last_message: Optional[LastMessage] = None
    message_count: Optional[int] = 0


class ChatMessage(ChatMessageBase):
    metadata: Optional[MessageMetadata] = None


class MessageResponse(ChatMessageBase):
    metadata: Optional[MessageMetadata] = None


class ChatThreadWithMessages(ChatThreadBase):
    messages: list[MessageResponse]


AgentResponse = Union[
    RevenueAnalysisResponse, ExpenseAnalysisResponse, ProfitMarginsResponse
]


class AnalysisResponse(BaseModel):
    summary: str
    data: dict
    sources: List[str]


class AssistantMessageResponse(ChatMessageBase):
    metadata: MessageMetadata = MessageMetadata(references=[], analysis={})


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
