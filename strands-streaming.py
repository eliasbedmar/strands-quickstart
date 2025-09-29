"""

Streaming in Strands SDK

 - Enables - real-time streaming, monitor/process events as they ocurr during agent execution.
 - Responsive UI, real-time monitoring, custom output formatting.

2 options:
- Async Iterators (pull) - asynchronous applications (non-blocking), need to control processing timing, FastAPI, aiohttp, Djanjo Channels
- Callback handlers (push) - synchronous applications (blocking until all events processed), simpler event handling/automatic event processing, custom-event processing

Usage:
- Async Iterators: agent.stream_async() + async for event (iteration in Python)
- Callback Handler: Agent(callback_handler=function()) + agent() (standard agent call)

Event Types:
- Lifecycle events
- Text Generation events
- Tool events
- Reasoning events

"""

# ASYNC ITERATOR PATTERN

import asyncio
from strands import Agent
from strands_tools import calculator

# Create agent with event loop tracker
agent = Agent(
    tools=[calculator],
    callback_handler=None
)

# This will show the full event lifecycle in the console
async def run_streaming():
    async for event in agent.stream_async("What is the capital of France and what is 42+7?"):
        # Track event loop lifecycle
        if event.get("init_event_loop", False):
            print("🔄 Event loop initialized")
        elif event.get("start_event_loop", False):
            print("▶️ Event loop cycle starting")
        elif "message" in event:
            print(f"📬 New message created: {event['message']['role']}")
        elif event.get("complete", False):
            print("✅ Cycle completed")
        elif event.get("force_stop", False):
            print(f"🛑 Event loop force-stopped: {event.get('force_stop_reason', 'unknown reason')}")

        # Track tool usage
        if "current_tool_use" in event and event["current_tool_use"].get("name"):
            tool_name = event["current_tool_use"]["name"]
            print(f"🔧 Using tool: {tool_name}")

        # Show only a snippet of text to keep output clean
        if "data" in event:
            # Only show first 20 chars of each chunk for demo purposes
            data_snippet = event["data"][:20] + ("..." if len(event["data"]) > 20 else "")
            print(f"📟 Text: {data_snippet}")

# Run the async function
asyncio.run(run_streaming())


# CALLBACK HANDLER PATTERN

from strands import Agent
from strands_tools import calculator

def event_loop_tracker(**kwargs):
    # Track event loop lifecycle
    if kwargs.get("init_event_loop", False):
        print("🔄 Event loop initialized")
    elif kwargs.get("start_event_loop", False):
        print("▶️ Event loop cycle starting")
    elif "message" in kwargs:
        print(f"📬 New message created: {kwargs['message']['role']}")
    elif kwargs.get("complete", False):
        print("✅ Cycle completed")
    elif kwargs.get("force_stop", False):
        print(f"🛑 Event loop force-stopped: {kwargs.get('force_stop_reason', 'unknown reason')}")

    # Track tool usage
    if "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
        tool_name = kwargs["current_tool_use"]["name"]
        print(f"🔧 Using tool: {tool_name}")

    # Show only a snippet of text to keep output clean
    if "data" in kwargs:
        # Only show first 20 chars of each chunk for demo purposes
        data_snippet = kwargs["data"][:20] + ("..." if len(kwargs["data"]) > 20 else "")
        print(f"📟 Text: {data_snippet}")

# Create agent with event loop tracker
agent = Agent(
    tools=[calculator],
    callback_handler=event_loop_tracker
)

# This will show the full event lifecycle in the console
agent("What is the capital of France and what is 42+7?")