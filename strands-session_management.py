"""
Session Management
- Persisting agent state and conversation history across multiple interactions
- Maintaining context & continuity with restarts or deployed in distributed environments
- Strands provides built-in session persistence capabilities that automatically capture and restore this information, allowing agents to seamlessly continue conversations where they left off.

Contains:
- Session ID (FileSessionManager object)
- Conversation history
- Agent state (key-value store)
- Other stateful information (like Conversation Manager)
"""

#Basic Usage
from strands import Agent
from strands.session.file_session_manager import FileSessionManager

# Create a session manager with a unique session ID
session_manager = FileSessionManager(session_id="test-session")

# Create an agent with the session manager
agent = Agent(session_manager=session_manager)

# Use the agent - all messages and state are automatically persisted
agent("Hello!")  # This conversation is persisted


"""Built-in Session Managers
1 - FileSessionManager (local filesystem)
2 - S3SessionManager (Distributed environments)
"""

"""
FileSessionManager
/<sessions_dir>/
└── session_<session_id>/
    ├── session.json                # Session metadata
    └── agents/
        └── agent_<agent_id>/
            ├── agent.json          # Agent metadata and state
            └── messages/
                ├── message_<message_id>.json
                └── message_<message_id>.json

"""

from strands import Agent
from strands.session.file_session_manager import FileSessionManager

# Create a session manager with a unique session ID
session_manager = FileSessionManager(
    session_id="user-123",
    # storage_dir="/path/to/sessions"  # Optional, defaults to a temp directory
)

# Create an agent with the session manager
agent = Agent(session_manager=session_manager)

# Use the agent normally - state and messages will be persisted automatically
agent("Hello, I'm a new user!")

"""
#S3 Session Manager (Distributed Environments)

<s3_key_prefix>/
└── session_<session_id>/
    ├── session.json                # Session metadata
    └── agents/
        └── agent_<agent_id>/
            ├── agent.json          # Agent metadata and state
            └── messages/
                ├── message_<message_id>.json
                └── message_<message_id>.json
"""



from strands import Agent
from strands.session.s3_session_manager import S3SessionManager
import boto3

# Optional: Create a custom boto3 session
boto_session = boto3.Session(region_name="us-west-2")

# Create a session manager that stores data in S3
session_manager = S3SessionManager(
    session_id="user-dev-1",
    bucket="strands-agents-test-bedelias",
    prefix="dev/",  # Optional key prefix
    boto_session=boto_session,  # Optional boto3 session
    region_name="us-west-2"  # Optional AWS region (if boto_session not provided)
)

# Create an agent with the session manager
agent = Agent(session_manager=session_manager)

# Use the agent normally - state and messages will be persisted to S3
agent("Tell me how many messages have been asked already? And where is your Session information stored?")


"""
How Session Management Works:

1 - Session Persistence Triggers: Agent initialization, Message Addition, Agent Invocation, Message Redaction
*Note - After initializing the agent, direct modifications to agent.messages will not be persisted. Utilize the Conversation Manager to help manage context of the agent in a way that can be persisted.

2 - Data Models: Session, SessionAgent, SessionMessage
- Session - top level container for session data (Namespace) - multiple Agents and interactions
- SessionAgent - Agent-specific data within session
- SessionMessage - Individual messages in the conversation

BEST PRACTICES:
1 - Use Unique session IDs, avoid data overlap
2 - Session cleanup (old/inactive sessions - e.g. TTL)
3 - Understand persistence triggers (changes to agent state/messages only persisted during specific events)

"""


"""
Custom Session Repositories

- Store session in bespoke storage backend 

"""
from typing import Optional
from strands import Agent
from strands.session.repository_session_manager import RepositorySessionManager
from strands.session.session_repository import SessionRepository
from strands.types.session import Session, SessionAgent, SessionMessage

class CustomSessionRepository(SessionRepository):
    """Custom session repository implementation."""

    def __init__(self):
        """Initialize with your custom storage backend."""
        # Initialize your storage backend (e.g., database connection)
        self.db = YourDatabaseClient()

    def create_session(self, session: Session) -> Session:
        """Create a new session."""
        self.db.sessions.insert(asdict(session))
        return session

    def read_session(self, session_id: str) -> Optional[Session]:
        """Read a session by ID."""
        data = self.db.sessions.find_one({"session_id": session_id})
        if data:
            return Session.from_dict(data)
        return None

    # Implement other required methods...
    # create_agent, read_agent, update_agent
    # create_message, read_message, update_message, list_messages

# Use your custom repository with RepositorySessionManager
custom_repo = CustomSessionRepository()
session_manager = RepositorySessionManager(
    session_id="user-789",
    session_repository=custom_repo
)

agent = Agent(session_manager=session_manager)