
# Conversation Manager
# 3 key elements - apply_management, reduce_context, removed_messages_count
# Managing conversations - NullConversationManager, SlidingWindowConversationManager - default

# NullConversationManager

from strands import Agent
from strands.agent.conversation_manager import NullConversationManager

agent = Agent(
    conversation_manager=NullConversationManager()
)


# SlidingWindowConversationManager
from strands import Agent
from strands.agent.conversation_manager import SlidingWindowConversationManager

# Create a conversation manager with custom window size
# By default, SlidingWindowConversationManager is used even if not specified
conversation_manager = SlidingWindowConversationManager(
    window_size=10,  # Maximum number of message pairs to keep
)

# Use the conversation manager with your agent
agent = Agent(conversation_manager=conversation_manager)


# SummarizingConversationManager

from strands import Agent
from strands.agent.conversation_manager import SummarizingConversationManager

agent = Agent(
    conversation_manager=SummarizingConversationManager()
)



from strands import Agent
from strands.agent.conversation_manager import SummarizingConversationManager

# Custom system prompt for technical conversations
custom_system_prompt = """
You are summarizing a technical conversation. Create a concise bullet-point summary that:
- Focuses on code changes, architectural decisions, and technical solutions
- Preserves specific function names, file paths, and configuration details
- Omits conversational elements and focuses on actionable information
- Uses technical terminology appropriate for software development

Format as bullet points without conversational language.
"""

conversation_manager = SummarizingConversationManager(
    summarization_system_prompt=custom_system_prompt
)

agent = Agent(
    conversation_manager=conversation_manager
)


from strands import Agent
from strands.agent.conversation_manager import SummarizingConversationManager
from strands.models import AnthropicModel

# Create a cheaper, faster model for summarization tasks
summarization_model = AnthropicModel(
    model_id="claude-3-5-haiku-20241022",  # More cost-effective for summarization
    max_tokens=1000,
    params={"temperature": 0.1}  # Low temperature for consistent summaries
)
custom_summarization_agent = Agent(model=summarization_model)

conversation_manager = SummarizingConversationManager(
    summary_ratio=0.4,
    preserve_recent_messages=8,
    summarization_agent=custom_summarization_agent
)

agent = Agent(
    conversation_manager=conversation_manager
)