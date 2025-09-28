"""
# Agent Loop workflow:
1 - initialization
2 - user input processing
3 - model processing
4 - response analysis & tool execution
5 - tool result processing
6 - recursive processing
7 - completion

State Management
-What State Is: State in Strands is a key-value storage system that persists data across agent interactions and tool executions. It's designed for maintaining context and information throughout the agent's lifecycle.

-Persisted by Default:
--Conversation History - All messages exchanged between user and agent are stored in agent.messages
--Tool Call History - Direct tool calls are recorded by default (unless record_direct_tool_call=False)
-User-Persisted (optional) - Key value pairs (JSON seriazable)

- State can be persisted across sessions (Session Management)
"""

from strands import Agent

# Create an agent
agent = Agent()

# Send a message and get a response
agent("Hello!")

# Access the conversation history
print(agent.messages)  # Shows all messages exchanged so far


from strands import Agent
from strands_tools import calculator

agent = Agent(tools=[calculator])

# Direct tool call with recording (default behavior)
agent.tool.calculator(expression="123 * 456")

# Direct tool call without recording
agent.tool.calculator(expression="765 / 987", record_direct_tool_call=False)

print(agent.messages)


## Agent State management
from strands import Agent
agent = Agent(
    state = {"user_preferences": {"theme": "dark"}, "session_count": 0})


# Access state values
theme = agent.state.get("user_preferences")
print(theme)  # {"theme": "dark"}

# Set new state values
agent.state.set("last_action", "login")
agent.state.set("session_count", 1)

# Get entire state
all_state = agent.state.get()
print(all_state)  # All state data as a dictionary

# Delete state values
agent.state.delete("last_action")


# Valid JSON-serializable values
agent.state.set("string_value", "hello")
agent.state.set("number_value", 42)
agent.state.set("boolean_value", True)
agent.state.set("list_value", [1, 2, 3])
agent.state.set("dict_value", {"nested": "data"})
agent.state.set("null_value", None)

# Invalid values will raise ValueError
try:
    agent.state.set("function", lambda x: x)  # Not JSON serializable
except ValueError as e:
    print(f"Error: {e}")


# Using State in Tools¶
# Agent state is particularly useful for maintaining information across tool executions:

from strands import Agent, tool

@tool
def track_user_action(action: str, agent: Agent):
    """Track user actions in agent state."""
    # Get current action count
    action_count = agent.state.get("action_count") or 0

    # Update state
    agent.state.set("action_count", action_count + 1)
    agent.state.set("last_action", action)

    return f"Action '{action}' recorded. Total actions: {action_count + 1}"

@tool
def get_user_stats(agent: Agent):
    """Get user statistics from agent state."""
    action_count = agent.state.get("action_count") or 0
    last_action = agent.state.get("last_action") or "none"

    return f"Actions performed: {action_count}, Last action: {last_action}"

# Create agent with tools
agent = Agent(tools=[track_user_action, get_user_stats])

# Use tools that modify and read state
agent("Track that I logged in")
result = agent("Track that I viewed my profile")
print(f"Actions taken: {agent.state.get('action_count')}")
print(f"Last action: {agent.state.get('last_action')}")

print(f"Entire state: {agent.state.get()}")

"""
Request State¶
Each agent interaction maintains a request state dictionary that persists throughout the event loop cycles and is not included in the agent's context:
Key Points:
- Event-driven - Called multiple times during agent processing (steps 1-7 in your workflow)
- Request-scoped state - The request_state dictionary persists only for the current request, not across requests
- Not in context - This state doesn't become part of the agent's conversation history or permanent state
- Monitoring/debugging - Useful for tracking internal events, logging, or temporary calculations

Difference from Agent State:
- Agent State: Permanent, persists across all interactions
- Request State: Temporary, only exists during one agent("message") call
- In your example, each time the agent processes events during the "Hi there!" request, the counter increments, showing how many internal events occurred. This is useful for debugging, monitoring performance, or maintaining temporary data during complex processing.
"""


from strands import Agent

def custom_callback_handler(**kwargs):
    # Access request state
    if "request_state" in kwargs:
        state = kwargs["request_state"]
        # Use or modify state as needed
        if "counter" not in state:
            state["counter"] = 0
        state["counter"] += 1
        print(f"Callback handler event count: {state['counter']}")

agent = Agent(callback_handler=custom_callback_handler)

result = agent("Hi there!")

print(result)

print(result.state)


