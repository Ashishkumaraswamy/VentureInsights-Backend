from fastapi import APIRouter, Depends, Path, Query
from fastapi_utils.cbv import cbv

from backend.dependencies import get_chat_service, get_user
from backend.models.base.users import User
from backend.models.requests.chat import (
    CreateThreadRequest,
    UpdateThreadRequest,
    SendMessageRequest,
)
from backend.models.response.chat import (
    ChatThreadList,
    ChatThread,
    ChatThreadWithMessages,
    MessageResponse,
)
from backend.services.chat import ChatService
from backend.utils.logger import get_logger

chat_router = APIRouter(prefix="/chat", tags=["chat"])
LOG = get_logger()

@cbv(chat_router)
class ChatAPI:
    chat_service: ChatService = Depends(get_chat_service)
    user: User = Depends(get_user)

    @chat_router.get("/threads", response_model=ChatThreadList)
    async def get_threads(
        self, 
        limit: int = Query(10, ge=1, le=100), 
        offset: int = Query(0, ge=0),
        user_threads_only: bool = Query(False)
    ) -> ChatThreadList:
        """Get all chat threads with pagination"""
        user_id = self.user.email if user_threads_only and self.user else None
        threads, total = await self.chat_service.get_threads(limit, offset, user_id)
        return ChatThreadList(threads=threads, total=total)

    @chat_router.post("/threads", response_model=ChatThread)
    async def create_thread(self, request: CreateThreadRequest) -> ChatThread:
        """Create a new chat thread"""
        LOG.info(f'thread payload is {request}')
        
        # Add user info if not provided in request
        if not request.created_by and self.user:
            request.created_by = self.user.email
            
        return await self.chat_service.create_thread(request)

    @chat_router.get("/threads/{thread_id}", response_model=ChatThreadWithMessages)
    async def get_thread(self, thread_id: str = Path(...)) -> ChatThreadWithMessages:
        """Get a chat thread with all its messages"""
        return await self.chat_service.get_thread(thread_id)

    @chat_router.delete("/threads/{thread_id}")
    async def delete_thread(self, thread_id: str = Path(...)) -> dict:
        """Delete a chat thread"""
        success = await self.chat_service.delete_thread(thread_id)
        return {"success": success}

    @chat_router.patch("/threads/{thread_id}", response_model=ChatThread)
    async def update_thread(
        self, request: UpdateThreadRequest, thread_id: str = Path(...)
    ) -> ChatThread:
        """Update a chat thread title"""
        return await self.chat_service.update_thread(thread_id, request.title)

    @chat_router.post("/threads/{thread_id}/messages", response_model=MessageResponse)
    async def send_message(
        self, 
        request: SendMessageRequest, 
        thread_id: str = Path(...)
    ) -> MessageResponse:
        """
        Send a new message to a chat thread
        
        The backend will:
        1. Add the user message to the thread
        2. Generate an AI response using the full thread context
        3. Return the AI response
        """
        LOG.info(f'thread payload is {request}')
        
        # Add user info if not provided in request
        if not request.user_id and self.user:
            request.user_id = self.user.email
            request.user_name = f"{self.user.first_name} {self.user.last_name}".strip()

        return await self.chat_service.add_message(thread_id, request) 