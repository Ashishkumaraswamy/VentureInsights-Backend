import uuid
from datetime import datetime
from typing import List, Optional

from backend.database.mongo import MongoDBConnector
from backend.models.base.chat import MessageMetadata, Reference
from backend.models.base.exceptions import NotFoundException
from backend.models.requests.chat import SendMessageRequest, CreateThreadRequest
from backend.models.response.chat import (
    ChatThread,
    ChatThreadWithMessages,
    ChatMessage,
    MessageResponse,
    AssistantMessageResponse,
)
from backend.settings import MongoConnectionDetails
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

    Using MongoDB collections:
    - venture_chat_threads: Stores thread metadata
    - venture_chat_history: Stores individual messages
    """

    # Collection names
    THREADS_COLLECTION = "venture_chat_threads"
    MESSAGES_COLLECTION = "venture_chat_history"

    def __init__(self, db_config: MongoConnectionDetails):
        self.db_config = db_config
        self.mongo_connector = MongoDBConnector(db_config)

        # Create indexes for efficient querying
        self._create_indexes()

    def _create_indexes(self):
        """Create necessary indexes for chat collections"""
        from backend.database.mongo import MongoIndexSpec

        # Thread indexes
        thread_indexes = [
            MongoIndexSpec(keys=[("updated_at", -1)], name="updated_at_desc"),
            MongoIndexSpec(keys=[("created_by", 1)], name="created_by"),
        ]

        # Message indexes
        message_indexes = [
            MongoIndexSpec(keys=[("thread_id", 1)], name="thread_id"),
            MongoIndexSpec(
                keys=[("thread_id", 1), ("timestamp", 1)], name="thread_id_timestamp"
            ),
            MongoIndexSpec(keys=[("user_id", 1)], name="user_id"),
        ]

        # Create indexes
        self.mongo_connector.create_indexes(self.THREADS_COLLECTION, thread_indexes)
        self.mongo_connector.create_indexes(self.MESSAGES_COLLECTION, message_indexes)

    async def get_threads(
        self, limit: int = 10, offset: int = 0, user_id: Optional[str] = None
    ) -> tuple[List[ChatThread], int]:
        """Get a list of chat threads with pagination"""
        # Prepare query - optionally filter by user_id
        query = {}
        if user_id:
            query["created_by"] = user_id

        # Get total count first
        total_threads = len(self.mongo_connector.query(self.THREADS_COLLECTION, query))

        # Get paginated threads sorted by updated_at desc
        pipeline = [
            {"$match": query},
            {"$sort": {"updated_at": -1}},
            {"$skip": offset},
            {"$limit": limit},
        ]

        thread_docs = await self.mongo_connector.aaggregate(
            self.THREADS_COLLECTION, pipeline
        )

        # Convert MongoDB docs to ChatThread objects
        threads = []
        for doc in thread_docs:
            threads.append(
                ChatThread(
                    id=str(doc["_id"]),
                    title=doc["title"],
                    created_at=doc["created_at"],
                    updated_at=doc["updated_at"],
                    message_count=doc["message_count"],
                    last_message=doc.get("last_message"),
                    created_by=doc.get("created_by"),
                )
            )

        return threads, total_threads

    async def create_thread(self, request: CreateThreadRequest) -> ChatThread:
        """Create a new chat thread"""
        thread_id = str(uuid.uuid4())
        now = datetime.now()

        # Generate default title if not provided
        title = request.title
        if not title:
            title = f"Chat {now.strftime('%Y-%m-%d %H:%M')}"

        thread = ChatThread(
            id=thread_id,
            title=title,
            created_at=now,
            updated_at=now,
            message_count=0,
            last_message=None,
            created_by=request.created_by,
        )

        # Convert to dict for MongoDB
        thread_dict = thread.model_dump()
        thread_dict["_id"] = thread_id  # Use the thread_id as MongoDB _id

        # Insert thread into MongoDB
        collection = await self.mongo_connector.aget_collection(self.THREADS_COLLECTION)
        await collection.insert_one(thread_dict)

        return thread

    async def get_thread(self, thread_id: str) -> ChatThreadWithMessages:
        """Get a chat thread with all its messages"""
        # Get the thread
        thread_docs = await self.mongo_connector.aquery(
            self.THREADS_COLLECTION, {"_id": thread_id}
        )

        if not thread_docs:
            raise NotFoundException(f"Thread with ID {thread_id} not found")

        thread_doc = thread_docs[0]

        # Get the messages for this thread
        message_docs = await self.mongo_connector.aquery(
            self.MESSAGES_COLLECTION, {"thread_id": thread_id}
        )

        # Sort messages by timestamp
        message_docs.sort(key=lambda x: x["timestamp"])

        # Convert MongoDB docs to ChatMessage objects
        messages = []
        for doc in message_docs:
            messages.append(
                ChatMessage(
                    id=str(doc["_id"]),
                    content=doc["content"],
                    sender=doc["sender"],
                    timestamp=doc["timestamp"],
                    metadata=doc.get("metadata"),
                    user_id=doc.get("user_id"),
                    user_name=doc.get("user_name"),
                )
            )

        return ChatThreadWithMessages(
            id=thread_doc["_id"],
            title=thread_doc["title"],
            created_at=thread_doc["created_at"],
            updated_at=thread_doc["updated_at"],
            messages=messages,
            created_by=thread_doc.get("created_by"),
        )

    async def delete_thread(self, thread_id: str) -> bool:
        """Delete a chat thread and all its messages"""
        # Check if thread exists
        thread_docs = await self.mongo_connector.aquery(
            self.THREADS_COLLECTION, {"_id": thread_id}
        )

        if not thread_docs:
            raise NotFoundException(f"Thread with ID {thread_id} not found")

        # Delete thread from MongoDB
        thread_collection = await self.mongo_connector.aget_collection(
            self.THREADS_COLLECTION
        )
        await thread_collection.delete_one({"_id": thread_id})

        # Delete all messages for this thread
        message_collection = await self.mongo_connector.aget_collection(
            self.MESSAGES_COLLECTION
        )
        await message_collection.delete_many({"thread_id": thread_id})

        return True

    async def update_thread(self, thread_id: str, title: str) -> ChatThread:
        """Update a chat thread's title"""
        # Check if thread exists
        thread_docs = await self.mongo_connector.aquery(
            self.THREADS_COLLECTION, {"_id": thread_id}
        )

        if not thread_docs:
            raise NotFoundException(f"Thread with ID {thread_id} not found")

        thread_doc = thread_docs[0]
        now = datetime.now()

        # Update thread in MongoDB
        thread_collection = await self.mongo_connector.aget_collection(
            self.THREADS_COLLECTION
        )
        await thread_collection.update_one(
            {"_id": thread_id}, {"$set": {"title": title, "updated_at": now}}
        )

        # Return updated thread
        return ChatThread(
            id=thread_id,
            title=title,
            created_at=thread_doc["created_at"],
            updated_at=now,
            message_count=thread_doc["message_count"],
            last_message=thread_doc.get("last_message"),
            created_by=thread_doc.get("created_by"),
        )

    async def add_message(
        self, thread_id: str, message: SendMessageRequest
    ) -> MessageResponse:
        """Add a new message to a thread and generate an AI response"""
        # Check if thread exists
        thread_docs = await self.mongo_connector.aquery(
            self.THREADS_COLLECTION, {"_id": thread_id}
        )

        if not thread_docs:
            raise NotFoundException(f"Thread with ID {thread_id} not found")

        # thread_doc = thread_docs[0]
        now = datetime.now()

        # Create user message
        message_id = str(uuid.uuid4())

        # Create metadata if attachments exist
        metadata = None
        if message.attachments:
            # In a real implementation, you would look up attachment details
            metadata = MessageMetadata(
                attachments=[
                    {
                        "id": att.id,
                        "name": f"Attachment {i + 1}",
                        "type": "application/pdf",
                        "size": 1024 * 1024,  # 1MB
                        "url": f"https://example.com/files/{att.id}",
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
            metadata=metadata,
            user_id=message.user_id,
            user_name=message.user_name,
        )

        # Convert to dict for MongoDB
        user_message_dict = chat_message.model_dump()
        user_message_dict["_id"] = message_id
        user_message_dict["thread_id"] = thread_id

        # Insert user message to MongoDB
        message_collection = await self.mongo_connector.aget_collection(
            self.MESSAGES_COLLECTION
        )
        await message_collection.insert_one(user_message_dict)

        # Update thread metadata
        thread_collection = await self.mongo_connector.aget_collection(
            self.THREADS_COLLECTION
        )

        # Create last_message data
        last_message = {
            "content": message.content,
            "sender": "user",
            "timestamp": now,
            "user_id": message.user_id,
            "user_name": message.user_name,
        }

        # Update thread in MongoDB
        await thread_collection.update_one(
            {"_id": thread_id},
            {
                "$inc": {"message_count": 1},
                "$set": {"updated_at": now, "last_message": last_message},
            },
        )

        # Get thread conversation history to provide context for the AI
        message_docs = await self.mongo_connector.aquery(
            self.MESSAGES_COLLECTION, {"thread_id": thread_id}
        )
        message_docs.sort(key=lambda x: x["timestamp"])

        # In a real implementation, this would use the full conversation history
        # to generate a contextually appropriate response using an AI model

        # For now, we'll create a simple mock response that acknowledges the conversation context
        response_content = (
            f"This is an AI-generated response to your message: '{message.content}'."
        )

        if len(message_docs) > 1:
            response_content += (
                f" I see our conversation has {len(message_docs)} messages so far."
            )

        if message.user_name:
            response_content = f"Hello {message.user_name}, " + response_content

        # Create AI response
        response_id = str(uuid.uuid4())

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
                        url="https://example.com/docs/sample",
                    )
                ],
                analysis={
                    "summary": "This is a summary of the AI analysis.",
                    "confidence": 0.95,
                    "sources": [
                        {
                            "type": "web",
                            "title": "Example Source",
                            "url": "https://example.com/source",
                        }
                    ],
                },
            ),
        )

        # Convert to dict for MongoDB
        assistant_message_dict = response.model_dump()
        assistant_message_dict["_id"] = response_id
        assistant_message_dict["thread_id"] = thread_id

        # Insert AI response to MongoDB
        await message_collection.insert_one(assistant_message_dict)

        # Update thread metadata again after AI response
        last_message = {
            "content": response.content,
            "sender": "assistant",
            "timestamp": now,
        }

        # Update thread in MongoDB
        await thread_collection.update_one(
            {"_id": thread_id},
            {
                "$inc": {"message_count": 1},
                "$set": {"updated_at": now, "last_message": last_message},
            },
        )

        return MessageResponse(
            id=response.id,
            content=response.content,
            sender=response.sender,
            timestamp=now,
            metadata=response.metadata,
        )
