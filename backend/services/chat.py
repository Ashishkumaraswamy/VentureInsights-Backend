import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

from backend.models.base.chat import ChatMessageBase, MessageMetadata, Reference
from backend.models.base.exceptions import NotFoundException
from backend.models.requests.chat import SendMessageRequest
from backend.models.response.chat import (
    ChatThread,
    ChatThreadWithMessages,
    ChatMessage,
    MessageResponse,
    AssistantMessageResponse,
)
from backend.utils.logger import get_logger

LOG = get_logger()
class ChatService:
    """
    Service for managing chat threads and messages.
    
    The ChatService handles:
    1. Creating and managing chat threads
    2. Storing the complete conversation history in threads
    3. Processing user messages with full conversation context
    4. Generating AI responses based on the thread's conversation history
    
    Currently using in-memory storage (class variables) for threads and messages.
    This will be replaced with database storage in the future.
    """
    
    # Make these class variables instead of instance variables for persistence
    threads = {}
    messages = {}

    def __init__(self, db_config: Dict[str, Any]):
        self.db_config = db_config
        # Removed initialization of threads and messages from here

    async def get_threads(self, limit: int = 10, offset: int = 0) -> tuple[List[ChatThread], int]:
        """Get a list of chat threads with pagination"""
        thread_list = list(ChatService.threads.values())
        # Sort by updated_at desc
        thread_list.sort(key=lambda x: x.updated_at, reverse=True)
        
        # Apply pagination
        paginated_threads = thread_list[offset:offset + limit]
        
        return paginated_threads, len(thread_list)

    async def create_thread(self, title: Optional[str] = None) -> ChatThread:
        """Create a new chat thread"""
        thread_id = str(uuid.uuid4())
        now = datetime.now()
        
        # Generate default title if not provided
        if not title:
            title = f"Chat {now.strftime('%Y-%m-%d %H:%M')}"
            
        thread = ChatThread(
            id=thread_id,
            title=title,
            created_at=now,
            updated_at=now,
            message_count=0,
            last_message=None
        )
        
        ChatService.threads[thread_id] = thread
        ChatService.messages[thread_id] = []
        
        return thread

    async def get_thread(self, thread_id: str) -> ChatThreadWithMessages:
        """Get a chat thread with all its messages"""
        if thread_id not in ChatService.threads:
            raise NotFoundException(f"Thread with ID {thread_id} not found")
            
        thread = ChatService.threads[thread_id]
        messages = ChatService.messages.get(thread_id, [])
        
        return ChatThreadWithMessages(
            id=thread.id,
            title=thread.title,
            created_at=thread.created_at,
            updated_at=thread.updated_at,
            messages=messages
        )

    async def delete_thread(self, thread_id: str) -> bool:
        """Delete a chat thread and all its messages"""
        if thread_id not in ChatService.threads:
            raise NotFoundException(f"Thread with ID {thread_id} not found")
            
        del ChatService.threads[thread_id]
        if thread_id in ChatService.messages:
            del ChatService.messages[thread_id]
            
        return True

    async def update_thread(self, thread_id: str, title: str) -> ChatThread:
        """Update a chat thread's title"""
        if thread_id not in ChatService.threads:
            raise NotFoundException(f"Thread with ID {thread_id} not found")
            
        thread = ChatService.threads[thread_id]
        thread.title = title
        thread.updated_at = datetime.now()
        
        return thread

    async def add_message(self, thread_id: str, message: SendMessageRequest) -> MessageResponse:
        """Add a new message to a thread and generate an AI response"""
        if thread_id not in ChatService.threads:
            raise NotFoundException(f"Thread with ID {thread_id} not found")
            
        # Create user message
        message_id = str(uuid.uuid4())
        now = datetime.now()
        
        # Create metadata if attachments exist
        metadata = None
        if message.attachments:
            # In a real implementation, you would look up attachment details
            metadata = MessageMetadata(
                attachments=[
                    {
                        "id": att.id,
                        "name": f"Attachment {i+1}",
                        "type": "application/pdf",
                        "size": 1024 * 1024,  # 1MB
                        "url": f"https://example.com/files/{att.id}"
                    }
                    for i, att in enumerate(message.attachments)
                ]
            )
            
        # Create the user message
        chat_message = ChatMessage(
            id=message_id,
            content=message.content,
            sender="user",
            timestamp=now,
            metadata=metadata
        )
        
        # Add user message to thread
        ChatService.messages[thread_id].append(chat_message)
        
        # Update thread metadata
        thread = ChatService.threads[thread_id]
        thread.message_count += 1
        thread.updated_at = now
        thread.last_message = {
            "content": message.content,
            "sender": "user",
            "timestamp": now
        }
        
        # Generate AI response using the thread context
        response_id = str(uuid.uuid4())
        
        # Get thread conversation history to provide context for the AI
        conversation_history = ChatService.messages[thread_id]
        LOG.info(f'conversation_history:{conversation_history}')
        
        # In a real implementation, this would use the full conversation history
        # to generate a contextually appropriate response using an AI model
        
        # For now, we'll create a simple mock response that acknowledges the conversation context
        response_content = f"This is an AI-generated response to your message: '{message.content}'."
        
        if len(conversation_history) > 1:
            response_content += f" I see our conversation has {len(conversation_history)} messages so far."
        
        # Create response with metadata
        response = AssistantMessageResponse(
            id=response_id,
            content=response_content,
            sender="assistant",
            timestamp=now,
            metadata=MessageMetadata(
                references=[
                    Reference(
                        title="Sample Reference Document",
                        url="https://example.com/docs/sample"
                    )
                ],
                analysis={
                    "summary": "This is a summary of the AI analysis.",
                    "confidence": 0.95,
                    "sources": [
                        {
                            "type": "web",
                            "title": "Example Source",
                            "url": "https://example.com/source"
                        }
                    ]
                }
            )
        )
        
        # Add AI response to thread
        ChatService.messages[thread_id].append(ChatMessage(
            id=response.id,
            content=response.content,
            sender=response.sender,
            timestamp=response.timestamp,
            metadata=response.metadata
        ))
        
        # Update thread metadata again after AI response
        thread.message_count += 1
        thread.updated_at = now
        thread.last_message = {
            "content": response.content,
            "sender": "assistant",
            "timestamp": now
        }
        
        return MessageResponse(
            id=response.id,
            content=response.content,
            sender=response.sender,
            timestamp=now,
            metadata=response.metadata
        ) 