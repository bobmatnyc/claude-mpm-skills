# AI/MCP Development

**Version:** 1.0.0
**Category:** AI
**Deployment Mode:** flat (recommended)

## Bundle Purpose

Complete AI development stack for building LLM-powered applications with Claude, featuring MCP integration, prompt engineering, multi-agent orchestration, and automatic prompt optimization. Optimized for production AI applications.

## Included Skills

- **mcp** (toolchains/ai/protocols/mcp) - Model Context Protocol for tool integration
- **anthropic-sdk** (toolchains/ai/sdks/anthropic) - Claude Messages API and streaming
- **langchain** (toolchains/ai/frameworks/langchain) - LCEL, RAG, agents, memory
- **dspy** (toolchains/ai/frameworks/dspy) - Automatic prompt optimization
- **langgraph** (toolchains/ai/frameworks/langgraph) - Stateful multi-agent orchestration
- **session-compression** (toolchains/ai/techniques/session-compression) - Context window management

## Use Cases

**When to Deploy This Bundle:**
- Building Claude-powered applications
- Creating MCP servers and tools
- Multi-agent AI workflows
- RAG (Retrieval-Augmented Generation) systems
- Production LLM applications with context management
- Prompt engineering and optimization projects

**What You Get:**
- MCP server development patterns
- Claude Messages API integration
- LangChain LCEL chains and agents
- DSPy prompt optimization techniques
- LangGraph state machines for agent orchestration
- Context compression strategies

## Deployment

```bash
# Recommended: Flat deployment to .claude/
./deploy.sh --flat ~/.claude/

# Validate before deploying
./deploy.sh --validate
```

## Skill Compatibility Matrix

| Skill | Standalone | Bundle-Enhanced | Required Dependencies |
|-------|------------|-----------------|----------------------|
| mcp | ✅ Yes | 🚀 Enhanced | None |
| anthropic-sdk | ✅ Yes | 🚀 Enhanced | None |
| langchain | ✅ Yes | 🚀 Enhanced | Anthropic SDK (recommended) |
| dspy | ✅ Yes | 🚀 Enhanced | LLM provider (Anthropic/OpenAI) |
| langgraph | ✅ Yes | 🚀 Enhanced | LangChain (required) |
| session-compression | ✅ Yes | 🚀 Enhanced | None (technique) |

**Bundle Synergies:**
- MCP + Anthropic SDK: Custom tools with Claude integration
- LangChain + Anthropic SDK: Claude-powered chains
- LangGraph + LangChain: Multi-agent orchestration
- DSPy + LangChain: Optimized prompts in chains
- Session Compression + any LLM: Long conversation support

**Framework Selection:**
- **Anthropic SDK**: Direct Claude API access (lowest latency)
- **LangChain**: Quick prototyping, ecosystem integrations
- **LangGraph**: Multi-step agents with state management
- **DSPy**: When prompt quality is critical

## Integration Example

```python
# MCP + Anthropic SDK
from anthropic import Anthropic
import mcp

# Create MCP tool
@mcp.tool()
def search_docs(query: str) -> str:
    """Search documentation database"""
    return search_db(query)

# Use tool with Claude
client = Anthropic()
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    tools=[search_docs],
    messages=[{"role": "user", "content": "Find API docs"}]
)

# LangGraph multi-agent
from langgraph.graph import StateGraph

workflow = StateGraph()
workflow.add_node("research", research_agent)
workflow.add_node("write", writing_agent)
workflow.add_edge("research", "write")

app = workflow.compile()
result = app.invoke({"topic": "AI development"})

# DSPy prompt optimization
import dspy

class RAGPipeline(dspy.Module):
    def __init__(self):
        self.retrieve = dspy.Retrieve(k=3)
        self.generate = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = self.retrieve(question).passages
        return self.generate(context=context, question=question)

# Optimize prompts automatically
optimizer = dspy.MIPROv2()
optimized_rag = optimizer.compile(RAGPipeline(), trainset=examples)
```

## Version History

- **1.0.0** (2025-11-30): Initial release with 6 AI development skills
