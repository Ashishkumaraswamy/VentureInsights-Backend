# Venture Insights Backend

## Chat API Architecture

The chat system implements a thread-based conversation architecture with the following features:

### Thread Creation
- Frontend: `POST /chat/threads` with title
- Backend: Creates thread, returns thread ID

### Sending Messages
- Frontend: `POST /chat/threads/{threadId}/messages` with just the message content
- Backend:
  - Retrieves existing thread context using threadId
  - Processes the new message with full conversation history
  - Generates an AI response
  - Saves both the user message and AI response
  - Returns the AI response

### Viewing Thread History
- Frontend: `GET /chat/threads/{threadId}`
- Backend: Returns thread with all messages in chronological order

### Benefits
- **Clean Separation of Concerns**:
  - Frontend: UI, user interaction
  - Backend: Data persistence, context management, AI response generation
- **Simplified API Contract**: Frontend only needs to send the new message content
- **Context Management**: Backend maintains the full conversation history
- **Persistence**: Currently using in-memory storage, will be migrated to database

## Development
Currently, the conversation history is stored in memory. In a future update, this will be migrated to a database for persistent storage.