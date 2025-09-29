"""
Amazon Bedrock

BedrockModel class
- Configuration Parameters: https://strandsagents.com/latest/documentation/docs/api-reference/models/#strands.models.bedrock.BedrockModel.BedrockConfig
- Can be updated at runtime (useful for tools that need to update config

Capabilities:
- Text generation
- Multi-Modal understanding (Image, Document, etc.)
- Tool/function calling
- Guardrail configurations
- System Prompt, Tool, and/or Message caching


Caching in Bedrock
-  uses Cache checkpoints,
- Metrics - AgentResult metrics & OTEL; min length required
- Tool caching - BedrockModel param cache_tools="default"
- System Prompt caching - BedrockModel param cache_prompt="default"
- Message caching - use cachePoint in Agent Messages array

Reasoning support
- Supported models only;
- Requires extra config parameter:
 additional_request_fields={
        "thinking": {
            "type": "enabled",
            "budget_tokens": 4096 # Minimum of 1,024
        }

Structured Output:
- For Tool Calling - specify schema for tool output - Agent.structured_output() translates required schema (JSON) to Bedrock's tool specification format
- Agent.structured_output() or Agent.structured_output_async()
- output_model = Pydantic BaseModel with schema for structured output

"""

from pydantic import BaseModel, Field
from strands import Agent
from strands.models import BedrockModel
from typing import List, Optional

class ProductAnalysis(BaseModel):
    """Analyze product information from text."""
    name: str = Field(description="Product name")
    category: str = Field(description="Product category")
    price: float = Field(description="Price in USD")
    features: List[str] = Field(description="Key product features")
    rating: Optional[float] = Field(description="Customer rating 1-5", ge=1, le=5)

bedrock_model = BedrockModel()

agent = Agent(model=bedrock_model)

result = agent.structured_output(
    ProductAnalysis,
    """
    Analyze this product: The UltraBook Pro is a premium laptop computer
    priced at $1,299. It features a 15-inch 4K display, 16GB RAM, 512GB SSD,
    and 12-hour battery life. Customer reviews average 4.5 stars.
    """
)

print(f"Product: {result.name}")
print(f"Category: {result.category}")
print(f"Price: ${result.price}")
print(f"Features: {result.features}")
print(f"Rating: {result.rating}")