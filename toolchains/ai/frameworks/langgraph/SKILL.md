---
name: langgraph
description: LangGraph framework for building stateful, multi-agent AI applications with cyclical workflows, human-in-the-loop patterns, and persistent checkpointing.
progressive_disclosure:
  entry_point:
    - summary
    - when_to_use
    - quick_start
  sections:
    - core_concepts
    - graph_construction
    - state_management
    - conditional_routing
    - multi_agent_patterns
    - human_in_loop
    - checkpointing_persistence
    - time_travel_debugging
    - streaming
    - tool_integration
    - error_handling
    - subgraphs_composition
    - map_reduce
    - production_deployment
    - langsmith_integration
    - real_world_examples
    - performance_optimization
    - comparison_simple_chains
    - migration_langchain
    - best_practices
estimated_tokens:
  entry: 80
  full: 5800
---

# LangGraph Workflows

## Summary

LangGraph is a framework for building **stateful, multi-agent applications** with LLMs. It implements state machines and directed graphs for orchestration, enabling complex workflows with persistent state management, human-in-the-loop support, and time-travel debugging.

**Key Innovation**: Transforms agent coordination from sequential chains into cyclic graphs with persistent state, conditional branching, and production-grade debugging capabilities.

## When to Use

✅ **Use LangGraph When**:
- Multi-agent coordination required
- Complex state management needs
- Human-in-the-loop workflows (approval gates, reviews)
- Need debugging/observability (time-travel, replay)
- Conditional branching based on outputs
- Building production agent systems
- State persistence across sessions

❌ **Don't Use LangGraph When**:
- Simple single-agent tasks
- No state persistence needed
- Prototyping/experimentation phase (use simple chains)
- Team lacks graph/state machine expertise
- Stateless request-response patterns

## Quick Start

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

# 1. Define state schema
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    current_step: str

# 2. Create graph
workflow = StateGraph(AgentState)

# 3. Add nodes (agents)
def researcher(state):
    return {"messages": ["Research complete"], "current_step": "research"}

def writer(state):
    return {"messages": ["Article written"], "current_step": "writing"}

workflow.add_node("researcher", researcher)
workflow.add_node("writer", writer)

# 4. Add edges (transitions)
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", END)

# 5. Set entry point and compile
workflow.set_entry_point("researcher")
app = workflow.compile()

# 6. Execute
result = app.invoke({"messages": [], "current_step": "start"})
print(result)
```

---

## Core Concepts

### StateGraph

The fundamental building block representing a directed graph of agents with shared state.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    """State schema shared across all nodes."""
    messages: list
    user_input: str
    final_output: str
    metadata: dict

# Create graph with state schema
workflow = StateGraph(AgentState)
```

**Key Properties**:
- **Nodes**: Agent functions that transform state
- **Edges**: Transitions between nodes (static or conditional)
- **State**: Shared data structure passed between nodes
- **Entry Point**: Starting node of execution
- **END**: Terminal node signaling completion

### Nodes

Nodes are functions that receive current state and return state updates.

```python
def research_agent(state: AgentState) -> dict:
    """Node function: receives state, returns updates."""
    query = state["user_input"]

    # Perform research (simplified)
    results = search_web(query)

    # Return state updates (partial state)
    return {
        "messages": state["messages"] + [f"Research: {results}"],
        "metadata": {"research_complete": True}
    }

# Add node to graph
workflow.add_node("researcher", research_agent)
```

**Node Behavior**:
- Receives **full state** as input
- Returns **partial state** (only fields to update)
- Can be sync or async functions
- Can invoke LLMs, call APIs, run computations

### Edges

Edges define transitions between nodes.

#### Static Edges

```python
# Direct transition: researcher → writer
workflow.add_edge("researcher", "writer")

# Transition to END
workflow.add_edge("writer", END)
```

#### Conditional Edges

```python
def should_continue(state: AgentState) -> str:
    """Routing function: decides next node based on state."""
    last_message = state["messages"][-1]

    if "APPROVED" in last_message:
        return END
    elif "NEEDS_REVISION" in last_message:
        return "writer"
    else:
        return "reviewer"

workflow.add_conditional_edges(
    "reviewer",  # Source node
    should_continue,  # Routing function
    {
        END: END,
        "writer": "writer",
        "reviewer": "reviewer"
    }
)
```

---

## Graph Construction

### Complete Workflow Example

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_anthropic import ChatAnthropic

# State schema with reducer
class ResearchState(TypedDict):
    topic: str
    research_notes: Annotated[list, operator.add]  # Reducer: appends to list
    draft: str
    revision_count: int
    approved: bool

# Initialize LLM
llm = ChatAnthropic(model="claude-sonnet-4")

# Node 1: Research
def research_node(state: ResearchState) -> dict:
    """Research the topic and gather information."""
    topic = state["topic"]

    prompt = f"Research key points about: {topic}"
    response = llm.invoke(prompt)

    return {
        "research_notes": [response.content]
    }

# Node 2: Write
def write_node(state: ResearchState) -> dict:
    """Write draft based on research."""
    notes = "\n".join(state["research_notes"])

    prompt = f"Write article based on:\n{notes}"
    response = llm.invoke(prompt)

    return {
        "draft": response.content,
        "revision_count": state.get("revision_count", 0)
    }

# Node 3: Review
def review_node(state: ResearchState) -> dict:
    """Review the draft and decide if approved."""
    draft = state["draft"]

    prompt = f"Review this draft. Reply APPROVED or NEEDS_REVISION:\n{draft}"
    response = llm.invoke(prompt)

    approved = "APPROVED" in response.content

    return {
        "approved": approved,
        "revision_count": state["revision_count"] + 1,
        "research_notes": [f"Review feedback: {response.content}"]
    }

# Routing logic
def should_continue_writing(state: ResearchState) -> str:
    """Decide next step after review."""
    if state["approved"]:
        return END
    elif state["revision_count"] >= 3:
        return END  # Max revisions reached
    else:
        return "writer"

# Build graph
workflow = StateGraph(ResearchState)

workflow.add_node("researcher", research_node)
workflow.add_node("writer", write_node)
workflow.add_node("reviewer", review_node)

# Static edges
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", "reviewer")

# Conditional edge from reviewer
workflow.add_conditional_edges(
    "reviewer",
    should_continue_writing,
    {
        END: END,
        "writer": "writer"
    }
)

workflow.set_entry_point("researcher")

# Compile
app = workflow.compile()

# Execute
result = app.invoke({
    "topic": "AI Safety",
    "research_notes": [],
    "draft": "",
    "revision_count": 0,
    "approved": False
})

print(f"Final draft: {result['draft']}")
print(f"Revisions: {result['revision_count']}")
```

---

## State Management

### State Schema with TypedDict

```python
from typing import TypedDict, Annotated, Literal
import operator

class WorkflowState(TypedDict):
    # Simple fields (replaced on update)
    user_id: str
    request_id: str
    status: Literal["pending", "processing", "complete", "failed"]

    # List with reducer (appends instead of replacing)
    messages: Annotated[list, operator.add]

    # Dict with custom reducer
    metadata: Annotated[dict, lambda x, y: {**x, **y}]

    # Optional fields
    error: str | None
    result: dict | None
```

### State Reducers

Reducers control how state updates are merged.

```python
import operator
from typing import Annotated

# Built-in reducers
Annotated[list, operator.add]  # Append to list
Annotated[set, operator.or_]   # Union of sets
Annotated[int, operator.add]   # Sum integers

# Custom reducer
def merge_dicts(existing: dict, update: dict) -> dict:
    """Deep merge dictionaries."""
    result = existing.copy()
    for key, value in update.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result

class State(TypedDict):
    config: Annotated[dict, merge_dicts]
```

### State Updates

Nodes return **partial state** - only fields to update:

```python
def node_function(state: State) -> dict:
    """Return only fields that should be updated."""
    return {
        "messages": ["New message"],  # Will be appended
        "status": "processing"  # Will be replaced
    }
    # Other fields remain unchanged
```

---

## Conditional Routing

### Basic Routing Function

```python
def route_based_on_score(state: State) -> str:
    """Route to different nodes based on state."""
    score = state["quality_score"]

    if score >= 0.9:
        return "publish"
    elif score >= 0.6:
        return "review"
    else:
        return "revise"

workflow.add_conditional_edges(
    "evaluator",
    route_based_on_score,
    {
        "publish": "publisher",
        "review": "reviewer",
        "revise": "reviser"
    }
)
```

### Dynamic Routing with LLM

```python
from langchain_anthropic import ChatAnthropic

def llm_router(state: State) -> str:
    """Use LLM to decide next step."""
    llm = ChatAnthropic(model="claude-sonnet-4")

    prompt = f"""
    Current state: {state['current_step']}
    User request: {state['user_input']}

    Which agent should handle this next?
    Options: researcher, coder, writer, FINISH

    Return only one word.
    """

    response = llm.invoke(prompt)
    next_agent = response.content.strip().lower()

    if next_agent == "finish":
        return END
    else:
        return next_agent

workflow.add_conditional_edges(
    "supervisor",
    llm_router,
    {
        "researcher": "researcher",
        "coder": "coder",
        "writer": "writer",
        END: END
    }
)
```

### Multi-Condition Routing

```python
def complex_router(state: State) -> str:
    """Route based on multiple conditions."""
    # Check multiple conditions
    has_errors = bool(state.get("errors"))
    is_approved = state.get("approved", False)
    iteration_count = state.get("iterations", 0)

    # Priority-based routing
    if has_errors:
        return "error_handler"
    elif is_approved:
        return END
    elif iteration_count >= 5:
        return "escalation"
    else:
        return "processor"

workflow.add_conditional_edges(
    "validator",
    complex_router,
    {
        "error_handler": "error_handler",
        "processor": "processor",
        "escalation": "escalation",
        END: END
    }
)
```

---

## Multi-Agent Patterns

### Supervisor Pattern

One supervisor coordinates multiple specialized agents.

```python
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from typing import TypedDict, Literal

class SupervisorState(TypedDict):
    task: str
    agent_history: list
    result: dict
    next_agent: str

# Specialized agents
class ResearchAgent:
    def __init__(self):
        self.llm = ChatAnthropic(model="claude-sonnet-4")

    def run(self, state: SupervisorState) -> dict:
        response = self.llm.invoke(f"Research: {state['task']}")
        return {
            "agent_history": [f"Research: {response.content}"],
            "result": {"research": response.content}
        }

class CodingAgent:
    def __init__(self):
        self.llm = ChatAnthropic(model="claude-sonnet-4")

    def run(self, state: SupervisorState) -> dict:
        response = self.llm.invoke(f"Code: {state['task']}")
        return {
            "agent_history": [f"Code: {response.content}"],
            "result": {"code": response.content}
        }

class SupervisorAgent:
    def __init__(self):
        self.llm = ChatAnthropic(model="claude-sonnet-4")

    def route(self, state: SupervisorState) -> dict:
        """Decide which agent to use next."""
        history = "\n".join(state.get("agent_history", []))

        prompt = f"""
        Task: {state['task']}
        Progress: {history}

        Which agent should handle the next step?
        Options: researcher, coder, FINISH

        Return only one word.
        """

        response = self.llm.invoke(prompt)
        next_agent = response.content.strip().lower()

        return {"next_agent": next_agent}

# Build supervisor workflow
def create_supervisor_workflow():
    workflow = StateGraph(SupervisorState)

    # Initialize agents
    research_agent = ResearchAgent()
    coding_agent = CodingAgent()
    supervisor = SupervisorAgent()

    # Add nodes
    workflow.add_node("supervisor", supervisor.route)
    workflow.add_node("researcher", research_agent.run)
    workflow.add_node("coder", coding_agent.run)

    # Conditional routing from supervisor
    def route_from_supervisor(state: SupervisorState) -> str:
        next_agent = state.get("next_agent", "FINISH")
        if next_agent == "finish":
            return END
        return next_agent

    workflow.add_conditional_edges(
        "supervisor",
        route_from_supervisor,
        {
            "researcher": "researcher",
            "coder": "coder",
            END: END
        }
    )

    # Loop back to supervisor after each agent
    workflow.add_edge("researcher", "supervisor")
    workflow.add_edge("coder", "supervisor")

    workflow.set_entry_point("supervisor")

    return workflow.compile()

# Execute
app = create_supervisor_workflow()
result = app.invoke({
    "task": "Build a REST API for user management",
    "agent_history": [],
    "result": {},
    "next_agent": ""
})
```

### Hierarchical Multi-Agent

Nested supervisor pattern with sub-teams.

```python
class TeamState(TypedDict):
    task: str
    team_results: dict

def create_backend_team():
    """Sub-graph for backend development."""
    workflow = StateGraph(TeamState)

    workflow.add_node("api_designer", design_api)
    workflow.add_node("database_designer", design_db)
    workflow.add_node("implementer", implement_backend)

    workflow.add_edge("api_designer", "database_designer")
    workflow.add_edge("database_designer", "implementer")
    workflow.add_edge("implementer", END)

    workflow.set_entry_point("api_designer")

    return workflow.compile()

def create_frontend_team():
    """Sub-graph for frontend development."""
    workflow = StateGraph(TeamState)

    workflow.add_node("ui_designer", design_ui)
    workflow.add_node("component_builder", build_components)
    workflow.add_node("integrator", integrate_frontend)

    workflow.add_edge("ui_designer", "component_builder")
    workflow.add_edge("component_builder", "integrator")
    workflow.add_edge("integrator", END)

    workflow.set_entry_point("ui_designer")

    return workflow.compile()

# Top-level coordinator
def create_project_workflow():
    workflow = StateGraph(TeamState)

    # Add team sub-graphs as nodes
    backend_team = create_backend_team()
    frontend_team = create_frontend_team()

    workflow.add_node("backend_team", backend_team)
    workflow.add_node("frontend_team", frontend_team)
    workflow.add_node("integrator", integrate_teams)

    # Parallel execution of teams
    workflow.add_edge("backend_team", "integrator")
    workflow.add_edge("frontend_team", "integrator")
    workflow.add_edge("integrator", END)

    workflow.set_entry_point("backend_team")

    return workflow.compile()
```

### Swarm Pattern (2025)

Dynamic agent hand-offs with collaborative decision-making.

```python
from typing import Literal

class SwarmState(TypedDict):
    task: str
    messages: list
    current_agent: str
    handoff_reason: str

def create_swarm():
    """Agents can dynamically hand off to each other."""

    def research_agent(state: SwarmState) -> dict:
        llm = ChatAnthropic(model="claude-sonnet-4")

        # Perform research
        response = llm.invoke(f"Research: {state['task']}")

        # Decide if handoff needed
        needs_code = "implementation" in response.content.lower()

        if needs_code:
            return {
                "messages": [response.content],
                "current_agent": "coder",
                "handoff_reason": "Need implementation"
            }
        else:
            return {
                "messages": [response.content],
                "current_agent": "writer",
                "handoff_reason": "Ready for documentation"
            }

    def coding_agent(state: SwarmState) -> dict:
        llm = ChatAnthropic(model="claude-sonnet-4")

        response = llm.invoke(f"Implement: {state['task']}")

        return {
            "messages": [response.content],
            "current_agent": "tester",
            "handoff_reason": "Code complete, needs testing"
        }

    def tester_agent(state: SwarmState) -> dict:
        # Test the code
        tests_pass = True  # Simplified

        if tests_pass:
            return {
                "messages": ["Tests passed"],
                "current_agent": "DONE",
                "handoff_reason": "All tests passing"
            }
        else:
            return {
                "messages": ["Tests failed"],
                "current_agent": "coder",
                "handoff_reason": "Fix failing tests"
            }

    # Build graph
    workflow = StateGraph(SwarmState)

    workflow.add_node("researcher", research_agent)
    workflow.add_node("coder", coding_agent)
    workflow.add_node("tester", tester_agent)

    # Dynamic routing based on current_agent
    def route_swarm(state: SwarmState) -> str:
        next_agent = state.get("current_agent", "DONE")
        if next_agent == "DONE":
            return END
        return next_agent

    workflow.add_conditional_edges(
        "researcher",
        route_swarm,
        {"coder": "coder", "writer": "writer"}
    )

    workflow.add_conditional_edges(
        "coder",
        route_swarm,
        {"tester": "tester"}
    )

    workflow.add_conditional_edges(
        "tester",
        route_swarm,
        {"coder": "coder", END: END}
    )

    workflow.set_entry_point("researcher")

    return workflow.compile()
```

---

## Human-in-the-Loop

### Interrupt for Approval

```python
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, END

# Enable checkpointing for interrupts
memory = SqliteSaver.from_conn_string(":memory:")

def create_approval_workflow():
    workflow = StateGraph(dict)

    workflow.add_node("draft", create_draft)
    workflow.add_node("approve", human_approval)  # Interrupt point
    workflow.add_node("publish", publish_content)

    workflow.add_edge("draft", "approve")
    workflow.add_edge("approve", "publish")
    workflow.add_edge("publish", END)

    workflow.set_entry_point("draft")

    # Compile with interrupt before "approve"
    return workflow.compile(
        checkpointer=memory,
        interrupt_before=["approve"]  # Pause here
    )

# Usage
app = create_approval_workflow()
config = {"configurable": {"thread_id": "1"}}

# Step 1: Run until interrupt
for event in app.stream({"content": "Draft article..."}, config):
    print(event)
    # Workflow pauses at "approve" node

# Human reviews draft
print("Draft ready for review. Approve? (y/n)")
approval = input()

# Step 2: Resume with approval decision
if approval == "y":
    # Continue execution
    result = app.invoke(None, config)  # Resume from checkpoint
    print("Published:", result)
else:
    # Optionally update state and retry
    app.update_state(config, {"needs_revision": True})
    result = app.invoke(None, config)
```

### Interactive Approval Gates

```python
class ApprovalState(TypedDict):
    draft: str
    approved: bool
    feedback: str

def approval_node(state: ApprovalState) -> dict:
    """This node requires human interaction."""
    # This is where workflow pauses
    # Human provides input through update_state
    return state  # No automatic changes

def create_interactive_workflow():
    workflow = StateGraph(ApprovalState)

    workflow.add_node("writer", write_draft)
    workflow.add_node("approval_gate", approval_node)
    workflow.add_node("reviser", revise_draft)
    workflow.add_node("publisher", publish_final)

    workflow.add_edge("writer", "approval_gate")

    # Route based on approval
    def route_after_approval(state: ApprovalState) -> str:
        if state.get("approved"):
            return "publisher"
        else:
            return "reviser"

    workflow.add_conditional_edges(
        "approval_gate",
        route_after_approval,
        {"publisher": "publisher", "reviser": "reviser"}
    )

    workflow.add_edge("reviser", "approval_gate")  # Loop back
    workflow.add_edge("publisher", END)

    workflow.set_entry_point("writer")

    memory = SqliteSaver.from_conn_string("approvals.db")
    return workflow.compile(
        checkpointer=memory,
        interrupt_before=["approval_gate"]
    )

# Execute with human intervention
app = create_interactive_workflow()
config = {"configurable": {"thread_id": "article_123"}}

# Step 1: Generate draft (pauses at approval_gate)
for event in app.stream({"draft": "", "approved": False, "feedback": ""}, config):
    print(event)

# Step 2: Human reviews and provides feedback
current_state = app.get_state(config)
print(f"Review this draft: {current_state.values['draft']}")

# Human decides
app.update_state(config, {
    "approved": False,
    "feedback": "Add more examples in section 2"
})

# Step 3: Resume (goes to reviser due to approved=False)
result = app.invoke(None, config)
```

---

## Checkpointing and Persistence

### MemorySaver (In-Memory)

```python
from langgraph.checkpoint.memory import MemorySaver

# In-memory checkpointing (lost on restart)
memory = MemorySaver()

app = workflow.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "conversation_1"}}

# State automatically saved at each step
result = app.invoke(initial_state, config)
```

### SQLite Persistence

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Persistent checkpointing with SQLite
checkpointer = SqliteSaver.from_conn_string("./workflow_state.db")

app = workflow.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "user_session_456"}}

# State persists across restarts
result = app.invoke(initial_state, config)

# Later: Resume from same thread
result2 = app.invoke(None, config)  # Continues from last state
```

### PostgreSQL for Production

```python
from langgraph.checkpoint.postgres import PostgresSaver

# Production-grade persistence
checkpointer = PostgresSaver.from_conn_string(
    "postgresql://user:pass@localhost/langgraph_db"
)

app = workflow.compile(checkpointer=checkpointer)

# Supports concurrent workflows with isolation
config1 = {"configurable": {"thread_id": "user_1"}}
config2 = {"configurable": {"thread_id": "user_2"}}

# Each thread maintains independent state
result1 = app.invoke(state1, config1)
result2 = app.invoke(state2, config2)
```

### Redis for Distributed Systems

```python
from langgraph.checkpoint.redis import RedisSaver

# Distributed checkpointing
checkpointer = RedisSaver.from_conn_string(
    "redis://localhost:6379",
    ttl=3600  # 1 hour TTL
)

app = workflow.compile(checkpointer=checkpointer)

# Supports horizontal scaling
# Multiple workers can process different threads
```

---

## Time-Travel Debugging

### View State History

```python
from langgraph.checkpoint.sqlite import SqliteSaver

checkpointer = SqliteSaver.from_conn_string("workflow.db")
app = workflow.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "debug_session"}}

# Run workflow
result = app.invoke(initial_state, config)

# Retrieve full history
history = app.get_state_history(config)

for i, state_snapshot in enumerate(history):
    print(f"Step {i}:")
    print(f"  Node: {state_snapshot.next}")
    print(f"  State: {state_snapshot.values}")
    print(f"  Metadata: {state_snapshot.metadata}")
    print()
```

### Replay from Checkpoint

```python
# Get state at specific step
history = list(app.get_state_history(config))
checkpoint_3 = history[3]  # Get state at step 3

# Replay from that checkpoint
config_replay = {
    "configurable": {
        "thread_id": "debug_session",
        "checkpoint_id": checkpoint_3.config["configurable"]["checkpoint_id"]
    }
}

# Resume from step 3
result = app.invoke(None, config_replay)
```

### Rewind and Modify

```python
# Rewind to step 5
history = list(app.get_state_history(config))
step_5 = history[5]

# Update state at that point
app.update_state(
    config,
    {"messages": ["Modified message"]},
    as_node="researcher"  # Apply update as if from this node
)

# Continue execution with modified state
result = app.invoke(None, config)
```

### Debug Workflow

```python
def debug_workflow():
    """Debug workflow step-by-step."""
    checkpointer = SqliteSaver.from_conn_string("debug.db")
    app = workflow.compile(checkpointer=checkpointer)

    config = {"configurable": {"thread_id": "debug"}}

    # Execute step-by-step
    state = initial_state
    for step in range(10):  # Max 10 steps
        print(f"\n=== Step {step} ===")

        # Get current state
        current = app.get_state(config)
        print(f"Current state: {current.values}")
        print(f"Next node: {current.next}")

        if not current.next:
            print("Workflow complete")
            break

        # Execute one step
        for event in app.stream(None, config):
            print(f"Event: {event}")

        # Pause for inspection
        input("Press Enter to continue...")

    # View full history
    print("\n=== Full History ===")
    for i, snapshot in enumerate(app.get_state_history(config)):
        print(f"Step {i}: {snapshot.next} -> {snapshot.values}")

debug_workflow()
```

---

## Streaming

### Token Streaming

```python
from langchain_anthropic import ChatAnthropic

def streaming_node(state: dict) -> dict:
    """Node that streams LLM output."""
    llm = ChatAnthropic(model="claude-sonnet-4")

    # Use streaming
    response = ""
    for chunk in llm.stream(state["prompt"]):
        content = chunk.content
        print(content, end="", flush=True)
        response += content

    return {"response": response}

# Stream events from workflow
for event in app.stream(initial_state):
    print(event)
```

### Event Streaming

```python
# Stream all events (node execution, state updates)
for event in app.stream(initial_state, stream_mode="updates"):
    node_name = event.keys()[0]
    state_update = event[node_name]
    print(f"Node '{node_name}' updated state: {state_update}")
```

### Custom Streaming

```python
from typing import AsyncGenerator

async def streaming_workflow(input_data: dict) -> AsyncGenerator:
    """Stream workflow progress in real-time."""
    config = {"configurable": {"thread_id": "stream"}}

    async for event in app.astream(input_data, config):
        # Stream each state update
        yield {
            "type": "state_update",
            "data": event
        }

    # Stream final result
    final_state = app.get_state(config)
    yield {
        "type": "complete",
        "data": final_state.values
    }

# Usage in FastAPI
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app_api = FastAPI()

@app_api.post("/workflow/stream")
async def stream_workflow(input: dict):
    return StreamingResponse(
        streaming_workflow(input),
        media_type="text/event-stream"
    )
```

---

## Tool Integration

### LangChain Tools

```python
from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import AgentExecutor, create_react_agent

# Define tools
search = DuckDuckGoSearchRun()

tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Search the web for information"
    )
]

def agent_with_tools(state: dict) -> dict:
    """Node that uses LangChain tools."""
    from langchain_anthropic import ChatAnthropic

    llm = ChatAnthropic(model="claude-sonnet-4")

    # Create agent with tools
    agent = create_react_agent(llm, tools, prompt_template)
    agent_executor = AgentExecutor(agent=agent, tools=tools)

    # Execute with tools
    result = agent_executor.invoke({"input": state["query"]})

    return {"result": result["output"]}

# Add to graph
workflow.add_node("agent_with_tools", agent_with_tools)
```

### Custom Tools

```python
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

class CalculatorInput(BaseModel):
    expression: str = Field(description="Mathematical expression to evaluate")

def calculate(expression: str) -> str:
    """Evaluate mathematical expression."""
    try:
        result = eval(expression)  # Simplified
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {e}"

calculator_tool = StructuredTool.from_function(
    func=calculate,
    name="Calculator",
    description="Evaluate mathematical expressions",
    args_schema=CalculatorInput
)

tools = [calculator_tool]

def tool_using_node(state: dict) -> dict:
    """Use custom tools."""
    result = calculator_tool.invoke({"expression": state["math_problem"]})
    return {"solution": result}
```

### Anthropic Tool Use

```python
from anthropic import Anthropic
import json

def node_with_anthropic_tools(state: dict) -> dict:
    """Use Anthropic's tool use feature."""
    client = Anthropic()

    # Define tools
    tools = [
        {
            "name": "get_weather",
            "description": "Get weather for a location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        }
    ]

    # First call: Request tool use
    response = client.messages.create(
        model="claude-sonnet-4",
        max_tokens=1024,
        tools=tools,
        messages=[{"role": "user", "content": state["query"]}]
    )

    # Execute tool if requested
    if response.stop_reason == "tool_use":
        tool_use = next(
            block for block in response.content
            if block.type == "tool_use"
        )

        # Execute tool
        tool_result = execute_tool(tool_use.name, tool_use.input)

        # Second call: Provide tool result
        final_response = client.messages.create(
            model="claude-sonnet-4",
            max_tokens=1024,
            tools=tools,
            messages=[
                {"role": "user", "content": state["query"]},
                {"role": "assistant", "content": response.content},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_use.id,
                            "content": str(tool_result)
                        }
                    ]
                }
            ]
        )

        return {"response": final_response.content[0].text}

    return {"response": response.content[0].text}
```

---

## Error Handling

### Try-Catch in Nodes

```python
def robust_node(state: dict) -> dict:
    """Node with error handling."""
    try:
        # Main logic
        result = risky_operation(state["input"])

        return {
            "result": result,
            "error": None,
            "status": "success"
        }

    except ValueError as e:
        # Handle specific error
        return {
            "error": f"Validation error: {e}",
            "status": "validation_failed"
        }

    except Exception as e:
        # Handle unexpected errors
        return {
            "error": f"Unexpected error: {e}",
            "status": "failed"
        }

# Route based on error status
def error_router(state: dict) -> str:
    status = state.get("status")

    if status == "success":
        return "next_step"
    elif status == "validation_failed":
        return "validator"
    else:
        return "error_handler"

workflow.add_conditional_edges(
    "robust_node",
    error_router,
    {
        "next_step": "next_step",
        "validator": "validator",
        "error_handler": "error_handler"
    }
)
```

### Retry Logic

```python
from typing import TypedDict

class RetryState(TypedDict):
    input: str
    result: str
    error: str | None
    retry_count: int
    max_retries: int

def node_with_retry(state: RetryState) -> dict:
    """Node that can be retried on failure."""
    try:
        result = unstable_operation(state["input"])

        return {
            "result": result,
            "error": None,
            "retry_count": 0
        }

    except Exception as e:
        return {
            "error": str(e),
            "retry_count": state.get("retry_count", 0) + 1
        }

def should_retry(state: RetryState) -> str:
    """Decide whether to retry or fail."""
    if state.get("error") is None:
        return "success"

    retry_count = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 3)

    if retry_count < max_retries:
        return "retry"
    else:
        return "failed"

# Build retry loop
workflow.add_node("operation", node_with_retry)
workflow.add_node("success_handler", handle_success)
workflow.add_node("failure_handler", handle_failure)

workflow.add_conditional_edges(
    "operation",
    should_retry,
    {
        "success": "success_handler",
        "retry": "operation",  # Loop back
        "failed": "failure_handler"
    }
)
```

### Fallback Strategies

```python
def node_with_fallback(state: dict) -> dict:
    """Try primary method, fall back to secondary."""
    # Try primary LLM
    try:
        result = primary_llm(state["prompt"])
        return {
            "result": result,
            "method": "primary"
        }
    except Exception as e_primary:
        # Fallback to secondary LLM
        try:
            result = secondary_llm(state["prompt"])
            return {
                "result": result,
                "method": "fallback",
                "primary_error": str(e_primary)
            }
        except Exception as e_secondary:
            # Both failed
            return {
                "error": f"Both methods failed: {e_primary}, {e_secondary}",
                "method": "failed"
            }
```

---

## Subgraphs and Composition

### Subgraphs as Nodes

```python
def create_subgraph():
    """Create reusable subgraph."""
    subgraph = StateGraph(dict)

    subgraph.add_node("step1", step1_func)
    subgraph.add_node("step2", step2_func)

    subgraph.add_edge("step1", "step2")
    subgraph.add_edge("step2", END)

    subgraph.set_entry_point("step1")

    return subgraph.compile()

# Use subgraph in main graph
def create_main_graph():
    workflow = StateGraph(dict)

    # Add subgraph as a node
    subgraph_compiled = create_subgraph()
    workflow.add_node("subgraph", subgraph_compiled)

    workflow.add_node("before", before_func)
    workflow.add_node("after", after_func)

    workflow.add_edge("before", "subgraph")
    workflow.add_edge("subgraph", "after")
    workflow.add_edge("after", END)

    workflow.set_entry_point("before")

    return workflow.compile()
```

### Parallel Subgraphs

```python
from langgraph.graph import StateGraph, END

def create_parallel_workflow():
    """Execute multiple subgraphs in parallel."""

    # Create subgraphs
    backend_graph = create_backend_subgraph()
    frontend_graph = create_frontend_subgraph()
    database_graph = create_database_subgraph()

    # Main graph
    workflow = StateGraph(dict)

    # Add subgraphs as parallel nodes
    workflow.add_node("backend", backend_graph)
    workflow.add_node("frontend", frontend_graph)
    workflow.add_node("database", database_graph)

    # Merge results
    workflow.add_node("merge", merge_results)

    # All subgraphs lead to merge
    workflow.add_edge("backend", "merge")
    workflow.add_edge("frontend", "merge")
    workflow.add_edge("database", "merge")

    workflow.add_edge("merge", END)

    # Set all as entry points (parallel execution)
    workflow.set_entry_point("backend")
    workflow.set_entry_point("frontend")
    workflow.set_entry_point("database")

    return workflow.compile()
```

---

## Map-Reduce Patterns

### Map-Reduce with LangGraph

```python
from typing import TypedDict, List

class MapReduceState(TypedDict):
    documents: List[str]
    summaries: List[str]
    final_summary: str

def map_node(state: MapReduceState) -> dict:
    """Map: Summarize each document."""
    llm = ChatAnthropic(model="claude-sonnet-4")

    summaries = []
    for doc in state["documents"]:
        summary = llm.invoke(f"Summarize: {doc}")
        summaries.append(summary.content)

    return {"summaries": summaries}

def reduce_node(state: MapReduceState) -> dict:
    """Reduce: Combine summaries into final summary."""
    llm = ChatAnthropic(model="claude-sonnet-4")

    combined = "\n".join(state["summaries"])
    final = llm.invoke(f"Combine these summaries:\n{combined}")

    return {"final_summary": final.content}

# Build map-reduce workflow
workflow = StateGraph(MapReduceState)

workflow.add_node("map", map_node)
workflow.add_node("reduce", reduce_node)

workflow.add_edge("map", "reduce")
workflow.add_edge("reduce", END)

workflow.set_entry_point("map")

app = workflow.compile()

# Execute
result = app.invoke({
    "documents": ["Doc 1...", "Doc 2...", "Doc 3..."],
    "summaries": [],
    "final_summary": ""
})
```

### Parallel Map with Batching

```python
import asyncio
from typing import List

async def parallel_map_node(state: dict) -> dict:
    """Map: Process documents in parallel."""
    llm = ChatAnthropic(model="claude-sonnet-4")

    async def summarize(doc: str) -> str:
        response = await llm.ainvoke(f"Summarize: {doc}")
        return response.content

    # Process all documents in parallel
    summaries = await asyncio.gather(
        *[summarize(doc) for doc in state["documents"]]
    )

    return {"summaries": list(summaries)}

# Use async workflow
app = workflow.compile()

# Execute with asyncio
result = asyncio.run(app.ainvoke({
    "documents": ["Doc 1", "Doc 2", "Doc 3"],
    "summaries": [],
    "final_summary": ""
}))
```

---

## Production Deployment

### LangGraph Cloud

```python
# Deploy to LangGraph Cloud (managed service)

# 1. Install LangGraph CLI
# pip install langgraph-cli

# 2. Create langgraph.json config
langgraph_config = {
    "dependencies": ["langchain", "langchain-anthropic"],
    "graphs": {
        "agent": "./graph.py:app"
    },
    "env": {
        "ANTHROPIC_API_KEY": "$ANTHROPIC_API_KEY"
    }
}

# 3. Deploy
# langgraph deploy

# 4. Use deployed graph via API
import requests

response = requests.post(
    "https://your-deployment.langraph.cloud/invoke",
    json={
        "input": {"messages": ["Hello"]},
        "config": {"thread_id": "user_123"}
    },
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)

result = response.json()
```

### Self-Hosted with FastAPI

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langgraph.checkpoint.postgres import PostgresSaver
import uvicorn

# Create FastAPI app
app_api = FastAPI()

# Initialize workflow
checkpointer = PostgresSaver.from_conn_string(
    "postgresql://user:pass@localhost/langgraph"
)
workflow_app = workflow.compile(checkpointer=checkpointer)

class WorkflowRequest(BaseModel):
    input: dict
    thread_id: str

class WorkflowResponse(BaseModel):
    output: dict
    thread_id: str

@app_api.post("/invoke", response_model=WorkflowResponse)
async def invoke_workflow(request: WorkflowRequest):
    """Invoke workflow synchronously."""
    try:
        config = {"configurable": {"thread_id": request.thread_id}}
        result = workflow_app.invoke(request.input, config)

        return WorkflowResponse(
            output=result,
            thread_id=request.thread_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app_api.post("/stream")
async def stream_workflow(request: WorkflowRequest):
    """Stream workflow execution."""
    from fastapi.responses import StreamingResponse

    config = {"configurable": {"thread_id": request.thread_id}}

    async def generate():
        async for event in workflow_app.astream(request.input, config):
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")

# Run server
if __name__ == "__main__":
    uvicorn.run(app_api, host="0.0.0.0", port=8000)
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app_api", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - POSTGRES_URL=postgresql://user:pass@db:5432/langgraph
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=langgraph
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

---

## LangSmith Integration

### Automatic Tracing

```python
import os
from langchain_anthropic import ChatAnthropic

# Enable LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-langsmith-key"
os.environ["LANGCHAIN_PROJECT"] = "my-langgraph-project"

# All LangGraph executions automatically traced
app = workflow.compile()

result = app.invoke(initial_state)
# View trace in LangSmith UI: https://smith.langchain.com
```

### Custom Metadata

```python
from langsmith import traceable

@traceable(
    run_type="chain",
    name="research_agent",
    metadata={"version": "1.0.0"}
)
def research_agent(state: dict) -> dict:
    """Node with custom LangSmith metadata."""
    # Function execution automatically traced
    return {"research": "results"}

workflow.add_node("researcher", research_agent)
```

### Evaluation with LangSmith

```python
from langsmith import Client
from langsmith.evaluation import evaluate

client = Client()

# Create test dataset
examples = [
    {
        "inputs": {"topic": "AI Safety"},
        "outputs": {"quality_score": 0.9}
    }
]

dataset = client.create_dataset("langgraph_tests")
for example in examples:
    client.create_example(
        dataset_id=dataset.id,
        inputs=example["inputs"],
        outputs=example["outputs"]
    )

# Evaluate workflow
def workflow_wrapper(inputs: dict) -> dict:
    result = app.invoke(inputs)
    return result

def quality_evaluator(run, example):
    """Custom evaluator."""
    score = calculate_quality(run.outputs)
    return {"key": "quality", "score": score}

results = evaluate(
    workflow_wrapper,
    data="langgraph_tests",
    evaluators=[quality_evaluator],
    experiment_prefix="langgraph_v1"
)

print(f"Average quality: {results['results']['quality']:.2f}")
```

---

## Real-World Examples

### Customer Support Agent

```python
from typing import TypedDict, Literal
from langchain_anthropic import ChatAnthropic

class SupportState(TypedDict):
    customer_query: str
    category: Literal["billing", "technical", "general"]
    priority: Literal["low", "medium", "high"]
    resolution: str
    escalated: bool

def categorize(state: SupportState) -> dict:
    """Categorize customer query."""
    llm = ChatAnthropic(model="claude-sonnet-4")

    prompt = f"""
    Categorize this support query:
    "{state['customer_query']}"

    Categories: billing, technical, general
    Priority: low, medium, high

    Return format: category|priority
    """

    response = llm.invoke(prompt)
    category, priority = response.content.strip().split("|")

    return {
        "category": category,
        "priority": priority
    }

def handle_billing(state: SupportState) -> dict:
    """Handle billing issues."""
    llm = ChatAnthropic(model="claude-sonnet-4")

    response = llm.invoke(f"Resolve billing issue: {state['customer_query']}")

    return {"resolution": response.content}

def handle_technical(state: SupportState) -> dict:
    """Handle technical issues."""
    llm = ChatAnthropic(model="claude-sonnet-4")

    response = llm.invoke(f"Resolve technical issue: {state['customer_query']}")

    return {"resolution": response.content}

def escalate(state: SupportState) -> dict:
    """Escalate to human agent."""
    return {
        "escalated": True,
        "resolution": "Escalated to senior support team"
    }

def route_by_category(state: SupportState) -> str:
    """Route based on category and priority."""
    if state["priority"] == "high":
        return "escalate"

    category = state["category"]
    if category == "billing":
        return "billing"
    elif category == "technical":
        return "technical"
    else:
        return "general"

# Build support workflow
workflow = StateGraph(SupportState)

workflow.add_node("categorize", categorize)
workflow.add_node("billing", handle_billing)
workflow.add_node("technical", handle_technical)
workflow.add_node("general", handle_technical)  # Reuse
workflow.add_node("escalate", escalate)

workflow.add_edge("categorize", "router")

workflow.add_conditional_edges(
    "categorize",
    route_by_category,
    {
        "billing": "billing",
        "technical": "technical",
        "general": "general",
        "escalate": "escalate"
    }
)

workflow.add_edge("billing", END)
workflow.add_edge("technical", END)
workflow.add_edge("general", END)
workflow.add_edge("escalate", END)

workflow.set_entry_point("categorize")

support_app = workflow.compile()

# Usage
result = support_app.invoke({
    "customer_query": "I was charged twice for my subscription",
    "category": "",
    "priority": "",
    "resolution": "",
    "escalated": False
})
```

### Research Assistant

```python
class ResearchState(TypedDict):
    topic: str
    research_notes: list
    outline: str
    draft: str
    final_article: str
    revision_count: int

def research(state: ResearchState) -> dict:
    """Gather information on topic."""
    # Use search tools
    results = search_web(state["topic"])

    return {
        "research_notes": [f"Research: {results}"]
    }

def create_outline(state: ResearchState) -> dict:
    """Create article outline."""
    llm = ChatAnthropic(model="claude-sonnet-4")

    notes = "\n".join(state["research_notes"])
    response = llm.invoke(f"Create outline for: {notes}")

    return {"outline": response.content}

def write_draft(state: ResearchState) -> dict:
    """Write article draft."""
    llm = ChatAnthropic(model="claude-sonnet-4")

    prompt = f"""
    Topic: {state['topic']}
    Outline: {state['outline']}
    Research: {state['research_notes']}

    Write comprehensive article.
    """

    response = llm.invoke(prompt)

    return {"draft": response.content}

def review_and_revise(state: ResearchState) -> dict:
    """Review draft quality."""
    llm = ChatAnthropic(model="claude-sonnet-4")

    response = llm.invoke(f"Review and improve:\n{state['draft']}")

    return {
        "final_article": response.content,
        "revision_count": state.get("revision_count", 0) + 1
    }

# Build research workflow
workflow = StateGraph(ResearchState)

workflow.add_node("research", research)
workflow.add_node("outline", create_outline)
workflow.add_node("write", write_draft)
workflow.add_node("review", review_and_revise)

workflow.add_edge("research", "outline")
workflow.add_edge("outline", "write")
workflow.add_edge("write", "review")

def check_quality(state: ResearchState) -> str:
    if state["revision_count"] >= 2:
        return END

    # Simple quality check
    if len(state.get("final_article", "")) > 1000:
        return END
    else:
        return "write"  # Revise

workflow.add_conditional_edges(
    "review",
    check_quality,
    {END: END, "write": "write"}
)

workflow.set_entry_point("research")

research_app = workflow.compile()
```

### Code Review Workflow

```python
class CodeReviewState(TypedDict):
    code: str
    language: str
    lint_results: list
    test_results: dict
    security_scan: dict
    review_comments: list
    approved: bool

def lint_code(state: CodeReviewState) -> dict:
    """Run linters on code."""
    # Run appropriate linter
    issues = run_linter(state["code"], state["language"])

    return {"lint_results": issues}

def run_tests(state: CodeReviewState) -> dict:
    """Execute test suite."""
    results = execute_tests(state["code"])

    return {"test_results": results}

def security_scan(state: CodeReviewState) -> dict:
    """Scan for security vulnerabilities."""
    scan_results = scan_for_vulnerabilities(state["code"])

    return {"security_scan": scan_results}

def ai_review(state: CodeReviewState) -> dict:
    """AI-powered code review."""
    llm = ChatAnthropic(model="claude-sonnet-4")

    prompt = f"""
    Review this {state['language']} code:

    {state['code']}

    Lint issues: {state['lint_results']}
    Test results: {state['test_results']}
    Security: {state['security_scan']}

    Provide review comments.
    """

    response = llm.invoke(prompt)

    return {"review_comments": [response.content]}

def approve_or_reject(state: CodeReviewState) -> dict:
    """Final approval decision."""
    # Auto-approve if all checks pass
    lint_ok = len(state["lint_results"]) == 0
    tests_ok = state["test_results"].get("passed", 0) == state["test_results"].get("total", 0)
    security_ok = len(state["security_scan"].get("vulnerabilities", [])) == 0

    approved = lint_ok and tests_ok and security_ok

    return {"approved": approved}

# Build code review workflow
workflow = StateGraph(CodeReviewState)

workflow.add_node("lint", lint_code)
workflow.add_node("test", run_tests)
workflow.add_node("security", security_scan)
workflow.add_node("ai_review", ai_review)
workflow.add_node("decision", approve_or_reject)

# Parallel execution of checks
workflow.add_edge("lint", "ai_review")
workflow.add_edge("test", "ai_review")
workflow.add_edge("security", "ai_review")
workflow.add_edge("ai_review", "decision")
workflow.add_edge("decision", END)

workflow.set_entry_point("lint")
workflow.set_entry_point("test")
workflow.set_entry_point("security")

code_review_app = workflow.compile()
```

---

## Performance Optimization

### Parallel Execution

```python
# Multiple nodes with same parent execute in parallel
workflow.add_edge("start", "task_a")
workflow.add_edge("start", "task_b")
workflow.add_edge("start", "task_c")

# task_a, task_b, task_c run concurrently
```

### Caching with Checkpointers

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Checkpoint results for reuse
checkpointer = SqliteSaver.from_conn_string("cache.db")

app = workflow.compile(checkpointer=checkpointer)

# Same thread_id reuses cached results
config = {"configurable": {"thread_id": "cached_session"}}

# First run: executes all nodes
result1 = app.invoke(input_data, config)

# Second run: uses cached state
result2 = app.invoke(None, config)  # Instant
```

### Batching

```python
def batch_processing_node(state: dict) -> dict:
    """Process items in batches."""
    items = state["items"]
    batch_size = 10

    results = []
    for i in range(0, len(items), batch_size):
        batch = items[i:i+batch_size]
        batch_result = process_batch(batch)
        results.extend(batch_result)

    return {"results": results}
```

### Async Execution

```python
from langgraph.graph import StateGraph
import asyncio

async def async_node(state: dict) -> dict:
    """Async node for I/O-bound operations."""
    results = await asyncio.gather(
        fetch_api_1(state["input"]),
        fetch_api_2(state["input"]),
        fetch_api_3(state["input"])
    )

    return {"results": results}

# Use async invoke
result = await app.ainvoke(input_data)
```

---

## Comparison with Simple Chains

### LangChain LCEL (Simple Chain)

```python
from langchain_core.runnables import RunnablePassthrough
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-sonnet-4")

# Simple linear chain
chain = (
    RunnablePassthrough()
    | llm
    | {"output": lambda x: x.content}
)

result = chain.invoke("Hello")
```

**Limitations**:
- ❌ No state persistence
- ❌ No conditional branching
- ❌ No cycles/loops
- ❌ No human-in-the-loop
- ❌ Limited debugging

### LangGraph (Cyclic Workflow)

```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(dict)

workflow.add_node("step1", step1_func)
workflow.add_node("step2", step2_func)

# Conditional loop
workflow.add_conditional_edges(
    "step2",
    should_continue,
    {"step1": "step1", END: END}
)

app = workflow.compile(checkpointer=memory)
```

**Advantages**:
- ✅ Persistent state across steps
- ✅ Conditional branching
- ✅ Cycles and loops
- ✅ Human-in-the-loop support
- ✅ Time-travel debugging
- ✅ Production-ready

---

## Migration from LangChain LCEL

### Before: LCEL Chain

```python
from langchain_core.runnables import RunnablePassthrough
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-sonnet-4")

chain = (
    {"input": RunnablePassthrough()}
    | llm
    | {"output": lambda x: x.content}
)

result = chain.invoke("Question")
```

### After: LangGraph

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class State(TypedDict):
    input: str
    output: str

def llm_node(state: State) -> dict:
    llm = ChatAnthropic(model="claude-sonnet-4")
    response = llm.invoke(state["input"])
    return {"output": response.content}

workflow = StateGraph(State)
workflow.add_node("llm", llm_node)
workflow.add_edge("llm", END)
workflow.set_entry_point("llm")

app = workflow.compile()

result = app.invoke({"input": "Question", "output": ""})
```

### Migration Checklist

- [ ] Identify stateful vs stateless operations
- [ ] Convert chain steps to graph nodes
- [ ] Define state schema (TypedDict)
- [ ] Add edges between nodes
- [ ] Implement conditional routing if needed
- [ ] Add checkpointing for state persistence
- [ ] Test with same inputs
- [ ] Verify output matches original chain

---

## Best Practices

### State Design

```python
# ✅ GOOD: Flat, explicit state
class GoodState(TypedDict):
    user_id: str
    messages: list
    current_step: str
    result: dict

# ❌ BAD: Nested, ambiguous state
class BadState(TypedDict):
    data: dict  # Too generic
    context: Any  # No type safety
```

### Node Granularity

```python
# ✅ GOOD: Single responsibility per node
def validate_input(state): ...
def process_data(state): ...
def format_output(state): ...

# ❌ BAD: Monolithic node
def do_everything(state): ...
```

### Error Handling

```python
# ✅ GOOD: Explicit error states
class State(TypedDict):
    result: dict | None
    error: str | None
    status: Literal["pending", "success", "failed"]

def robust_node(state):
    try:
        result = operation()
        return {"result": result, "status": "success"}
    except Exception as e:
        return {"error": str(e), "status": "failed"}

# ❌ BAD: Silent failures
def fragile_node(state):
    try:
        return operation()
    except:
        return {}  # Error lost
```

### Testing

```python
# Test individual nodes
def test_node():
    state = {"input": "test"}
    result = my_node(state)
    assert result["output"] == "expected"

# Test full workflow
def test_workflow():
    app = workflow.compile()
    result = app.invoke(initial_state)
    assert result["final_output"] == "expected"

# Test error paths
def test_error_handling():
    state = {"input": "invalid"}
    result = my_node(state)
    assert result["error"] is not None
```

### Monitoring

```python
import logging

logger = logging.getLogger(__name__)

def monitored_node(state: dict) -> dict:
    """Node with logging."""
    logger.info(f"Executing node with state: {state.keys()}")

    try:
        result = operation()
        logger.info("Node succeeded")
        return {"result": result}
    except Exception as e:
        logger.error(f"Node failed: {e}")
        raise
```

---

## Summary

LangGraph transforms agent development from linear chains into **cyclic, stateful workflows** with production-grade capabilities:

**Core Strengths**:
- 🔄 Cyclic workflows with loops and branches
- 💾 Persistent state across sessions
- 🕐 Time-travel debugging and replay
- 👤 Human-in-the-loop approval gates
- 🔧 Tool integration (LangChain, Anthropic, custom)
- 📊 LangSmith integration for tracing
- 🏭 Production deployment (cloud or self-hosted)

**When to Choose LangGraph**:
- Multi-agent coordination required
- Complex branching logic
- State persistence needed
- Human approvals in workflow
- Production systems with debugging needs

**Learning Path**:
1. Start with StateGraph basics
2. Add conditional routing
3. Implement checkpointing
4. Build multi-agent patterns
5. Deploy to production

**Production Checklist**:
- [ ] State schema with TypedDict
- [ ] Error handling in all nodes
- [ ] Checkpointing configured
- [ ] LangSmith tracing enabled
- [ ] Monitoring and logging
- [ ] Testing (unit + integration)
- [ ] Deployment strategy (cloud/self-hosted)

For simple request-response patterns, use LangChain LCEL. For complex stateful workflows, LangGraph is the industry-standard solution.

## Related Skills

When using Langgraph, these skills enhance your workflow:
- **dspy**: DSPy for LLM prompt optimization (complementary to LangGraph orchestration)
- **test-driven-development**: Testing LangGraph workflows and state machines
- **systematic-debugging**: Debugging multi-agent workflows and state transitions

[Full documentation available in these skills if deployed in your bundle]
