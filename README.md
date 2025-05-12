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
- **Persistence**: Chat history is stored in MongoDB for persistent storage

## Database Structure
The chat system uses MongoDB to store chat data in two collections:
- **venture_chat_threads**: Stores thread metadata including title, creation time, and last message
- **venture_chat_history**: Stores individual chat messages with references to their threads

## Development
The conversation history is now stored in MongoDB, which is the same database used for authentication.