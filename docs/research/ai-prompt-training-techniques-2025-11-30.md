# AI Prompt Training and Optimization Techniques - 2025 Research

**Research Date**: 2025-11-30
**Research Focus**: Methods for training, optimizing, and improving prompts programmatically
**Target Audience**: AI/ML engineers, prompt engineers, LLM application developers

---

## Executive Summary

This research document provides a comprehensive analysis of prompt training and optimization techniques as of 2025. The landscape has matured significantly with three primary approaches:

1. **DSPy Framework**: Automated prompt optimization treating prompts as code with declarative programming
2. **LangGraph Workflows**: Stateful multi-agent orchestration with graph-based prompt coordination
3. **Traditional Patterns**: Manual prompt engineering patterns (CoT, ToT, ReAct) with evaluation frameworks

**Key Finding**: The industry is moving from manual prompt engineering toward programmatic optimization, with DSPy leading automated optimization and LangGraph dominating complex multi-agent systems.

**Production Adoption**: Companies including JetBlue, Databricks, Walmart, VMware, Replit, Sephora, and Moody's use DSPy in production as of 2025.

---

## Table of Contents

1. [DSPy Framework](#1-dspy-framework)
2. [Prompt Engineering Patterns](#2-prompt-engineering-patterns)
3. [LangGraph Workflows](#3-langgraph-workflows)
4. [Simpler Approaches Without LangGraph](#4-simpler-approaches-without-langgraph)
5. [Evaluation Frameworks](#5-evaluation-frameworks)
6. [Production Patterns](#6-production-patterns)
7. [Comparison Matrix](#7-comparison-matrix)
8. [Use Case Recommendations](#8-use-case-recommendations)
9. [Tool Recommendations](#9-tool-recommendations)

---

## 1. DSPy Framework

### Overview

DSPy (Declarative Self-improving Python) is a framework for **programming—not prompting—language models**. It shifts focus from manual prompt engineering to declarative natural-language modules that can be automatically optimized.

**Core Philosophy**: Treat prompts as code with version control, automated testing, and systematic optimization.

### Key Features

#### Declarative Programming Model
```python
import dspy

# Define signature (input → output)
class QA(dspy.Signature):
    """Answer questions with short factual answers."""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="often between 1 and 5 words")

# Create module
qa_module = dspy.ChainOfThought(QA)

# Use module
response = qa_module(question="What is the capital of France?")
print(response.answer)  # "Paris"
```

#### Automatic Prompt Optimization

DSPy provides **optimizers** that compile high-level code into optimized prompts or weight updates:

- **BootstrapFewShot**: Optimizes few-shot examples
- **COPRO**: Optimizes instruction prompts
- **MIPRO/MIPROv2**: Optimizes both instructions and examples jointly
- **KNN**: K-nearest neighbors example selection

### DSPy Optimizers Deep Dive

#### BootstrapFewShot

**Best For**: Small datasets (10-50 examples)
**Optimizes**: Few-shot examples only

```python
from dspy.teleprompt import BootstrapFewShot

# Define metric
def accuracy_metric(example, prediction, trace=None):
    return example.answer.lower() == prediction.answer.lower()

# Configure optimizer
fewshot_optimizer = BootstrapFewShot(
    metric=accuracy_metric,
    max_bootstrapped_demos=4,      # Max examples to bootstrap
    max_labeled_demos=16,           # Max labeled examples to use
    max_rounds=1,                   # Bootstrapping rounds
    max_errors=10                   # Max errors before stopping
)

# Compile program
optimized_program = fewshot_optimizer.compile(
    student=qa_module,
    trainset=training_examples
)
```

**How It Works**:
1. Uses your program to generate outputs on training data
2. Filters successful traces (based on metric)
3. Selects representative examples as few-shot demonstrations
4. Compiles optimized program with best examples

#### BootstrapFewShotWithRandomSearch

**Best For**: Medium datasets (50-300 examples)
**Optimizes**: Few-shot examples with candidate exploration

```python
from dspy.teleprompt import BootstrapFewShotWithRandomSearch

config = dict(
    max_bootstrapped_demos=4,
    max_labeled_demos=4,
    num_candidate_programs=10,    # Number of candidates to explore
    num_threads=4                 # Parallel threads
)

teleprompter = BootstrapFewShotWithRandomSearch(
    metric=accuracy_metric,
    **config
)

optimized_program = teleprompter.compile(
    qa_module,
    trainset=training_examples
)
```

**Advantage**: Explores multiple candidate programs in parallel, selecting the best performer.

#### MIPROv2 (State-of-the-Art as of 2025)

**Best For**: Large datasets (300+ examples)
**Optimizes**: Instructions AND few-shot examples jointly
**Method**: Bayesian Optimization

```python
import dspy
from dspy.teleprompt import MIPROv2

# Initialize LM
lm = dspy.LM('openai/gpt-4o-mini', api_key='YOUR_API_KEY')
dspy.configure(lm=lm)

# Define metric
def custom_metric(example, prediction, trace=None):
    # Custom scoring logic
    return prediction.score > 0.8

# Initialize MIPROv2 with auto-configuration
teleprompter = MIPROv2(
    metric=custom_metric,
    auto="medium",  # Options: light, medium, heavy
    # auto="medium" automatically sets hyperparameters
)

# Optimize program
optimized_program = teleprompter.compile(
    dspy.ChainOfThought("question -> answer"),
    trainset=training_examples,
)

# Save optimized program
optimized_program.save("optimized_qa_model.json")
```

**MIPROv2 Auto-Configuration Modes** (2025 Update):
- **light**: Fast optimization, fewer iterations, lower compute
- **medium**: Balanced optimization (recommended default)
- **heavy**: Exhaustive optimization, highest quality, most compute

**How MIPROv2 Works**:
1. **Bootstrap Few-Shot Candidates**: Generates example candidates from training data
2. **Propose Instructions**: Creates instruction variations grounded in task dynamics
3. **Bayesian Optimization**: Finds optimal combination of instructions + examples
4. **Joint Optimization**: Optimizes both components together (not separately)

### Sequential Optimization Strategy

For best results, combine optimizers:

```python
# Step 1: Bootstrap few-shot examples
bootstrap = dspy.BootstrapFewShot(metric=accuracy_metric)
bootstrapped_program = bootstrap.compile(qa_module, trainset=examples)

# Step 2: Optimize instructions with MIPRO
mipro = dspy.MIPROv2(metric=accuracy_metric, auto="light")
final_program = mipro.compile(bootstrapped_program, trainset=examples)

# Step 3: Save final optimized program
final_program.save("production_model.json")
```

### Real-World Performance (2025 Study)

A 2025 study applied DSPy to five use cases:

| Use Case | Baseline Accuracy | DSPy Optimized | Improvement |
|----------|------------------|----------------|-------------|
| Prompt Evaluation | 46.2% | 64.0% | +38.5% |
| Guardrail Enforcement | 72.1% | 84.3% | +16.9% |
| Code Generation | 58.4% | 71.2% | +21.9% |
| Hallucination Detection | 65.8% | 79.5% | +20.8% |
| Agent Routing | 69.3% | 82.1% | +18.5% |

**Source**: "Is It Time To Treat Prompts As Code? A Multi-Use Case Study For Prompt Optimization Using DSPy" (arXiv:2507.03620, 2025)

### When to Use DSPy

✅ **Use DSPy When**:
- You have structured input/output requirements
- You have evaluation datasets (even small ones)
- You need systematic prompt improvement
- You want version-controlled, reproducible prompts
- You're building production systems requiring optimization

❌ **Don't Use DSPy When**:
- You have zero training examples
- Task requires extreme creativity/open-endedness
- You need immediate results without setup
- Your task changes frequently (no stable evaluation)

---

## 2. Prompt Engineering Patterns

### Chain-of-Thought (CoT)

**Purpose**: Enable complex reasoning through intermediate steps

**Technique**: Encourage the model to "think step by step"

#### Zero-Shot CoT

```python
prompt = """
Question: Roger has 5 tennis balls. He buys 2 more cans of tennis balls.
Each can has 3 tennis balls. How many tennis balls does he have now?

Let's think step by step.
"""

response = llm(prompt)
# Output:
# 1. Roger starts with 5 tennis balls
# 2. He buys 2 cans, each with 3 balls
# 3. 2 cans × 3 balls = 6 balls
# 4. 5 + 6 = 11 balls
# Answer: 11 tennis balls
```

**Key Phrase**: "Let's think step by step" triggers step-by-step reasoning

#### Few-Shot CoT

```python
prompt = """
Q: There are 15 trees in the grove. Grove workers will plant trees in the grove today.
After they are done, there will be 21 trees. How many did they plant today?

A: There are 15 trees originally. Then there were 21 trees after some more were planted.
So there must have been 21 - 15 = 6. The answer is 6.

Q: If there are 3 cars in the parking lot and 2 more cars arrive,
how many cars are in the parking lot?

A: There are originally 3 cars. 2 more arrive. 3 + 2 = 5. The answer is 5.

Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls.
Each can has 3 tennis balls. How many tennis balls does he have now?

A:
"""
```

**When to Use CoT**:
- Math problems
- Logical reasoning
- Multi-step tasks
- Debugging code
- Complex analysis

### Tree-of-Thoughts (ToT)

**Purpose**: Explore multiple reasoning paths like a search tree

**Technique**: Generate multiple thought branches, evaluate them, and select the best path

#### ToT Implementation Pattern

```python
import anthropic

def tree_of_thoughts(problem, num_branches=3, depth=3):
    """
    Implement Tree of Thoughts reasoning.

    Args:
        problem: The problem to solve
        num_branches: Number of thought branches per node
        depth: Maximum tree depth

    Returns:
        Best solution found
    """
    client = anthropic.Anthropic()

    def generate_thoughts(current_state, remaining_depth):
        if remaining_depth == 0:
            return current_state

        # Generate multiple next thoughts
        prompt = f"""
        Current reasoning: {current_state}

        Generate {num_branches} different next steps to solve: {problem}

        Format as:
        1. [thought 1]
        2. [thought 2]
        3. [thought 3]
        """

        response = client.messages.create(
            model="claude-sonnet-4",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        thoughts = parse_thoughts(response.content[0].text)

        # Evaluate each thought
        evaluated_thoughts = []
        for thought in thoughts:
            evaluation_prompt = f"""
            Problem: {problem}
            Current reasoning: {current_state}
            Proposed next step: {thought}

            Rate this step from 0-10 for:
            1. Correctness
            2. Progress toward solution
            3. Logical soundness

            Return only a number 0-10.
            """

            eval_response = client.messages.create(
                model="claude-sonnet-4",
                max_tokens=10,
                messages=[{"role": "user", "content": evaluation_prompt}]
            )

            score = float(eval_response.content[0].text.strip())
            evaluated_thoughts.append((thought, score))

        # Select best thought and recurse
        best_thought = max(evaluated_thoughts, key=lambda x: x[1])[0]
        new_state = f"{current_state}\n{best_thought}"

        return generate_thoughts(new_state, remaining_depth - 1)

    # Start with empty state
    final_solution = generate_thoughts("", depth)
    return final_solution

# Example usage
solution = tree_of_thoughts(
    problem="Design a database schema for a multi-tenant SaaS application",
    num_branches=3,
    depth=3
)
```

**When to Use ToT**:
- Strategic planning
- Creative problem solving
- Architecture design
- Game playing (chess, puzzles)
- Research planning

**Cost Consideration**: ToT makes multiple LLM calls per step, increasing costs significantly.

### ReAct (Reasoning + Acting)

**Purpose**: Combine reasoning with external tool usage

**Technique**: Interleave thought, action, and observation steps

#### ReAct Pattern

```python
def react_agent(question, tools, max_steps=10):
    """
    Implement ReAct pattern: Reasoning + Acting.

    Args:
        question: User question
        tools: Dictionary of available tools
        max_steps: Maximum reasoning steps
    """
    client = anthropic.Anthropic()

    history = []

    for step in range(max_steps):
        # Reasoning step
        prompt = f"""
        Question: {question}

        Previous steps:
        {format_history(history)}

        Think about what to do next. You can:
        1. Use a tool (search, calculate, code_execute)
        2. Provide final answer

        Format:
        Thought: [your reasoning]
        Action: [tool_name: tool_input] OR Answer: [final answer]
        """

        response = client.messages.create(
            model="claude-sonnet-4",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.content[0].text
        thought, action = parse_react_response(text)

        history.append({"thought": thought, "action": action})

        # Check if final answer
        if action.startswith("Answer:"):
            return action.replace("Answer:", "").strip()

        # Execute action
        tool_name, tool_input = parse_action(action)
        observation = tools[tool_name](tool_input)

        history.append({"observation": observation})

    return "Failed to find answer within step limit"

# Example tools
tools = {
    "search": lambda query: web_search(query),
    "calculate": lambda expr: eval(expr),
    "code_execute": lambda code: execute_python(code)
}

# Example usage
answer = react_agent(
    question="What is the current stock price of Apple and how has it changed in the last month?",
    tools=tools
)
```

**ReAct Trace Example**:
```
Thought: I need to find Apple's current stock price
Action: search: Apple stock price today

Observation: Apple (AAPL) is trading at $178.52

Thought: Now I need historical data for the last month
Action: search: Apple stock price 30 days ago

Observation: Apple was trading at $165.23 on [date]

Thought: I can now calculate the change
Action: calculate: ((178.52 - 165.23) / 165.23) * 100

Observation: 8.04

Thought: I have all the information needed
Action: Answer: Apple (AAPL) is currently trading at $178.52, up 8.04% from $165.23 a month ago.
```

**When to Use ReAct**:
- Information retrieval tasks
- Tasks requiring calculations
- Code execution workflows
- Research and analysis
- Real-time data needs

### Self-Consistency

**Purpose**: Generate multiple reasoning paths and select the most consistent answer

**Technique**: Sample multiple CoT responses and use majority voting

```python
def self_consistency(question, num_samples=5):
    """
    Implement self-consistency with CoT.
    """
    client = anthropic.Anthropic()

    answers = []

    for i in range(num_samples):
        prompt = f"""
        Question: {question}

        Let's think step by step.
        """

        response = client.messages.create(
            model="claude-sonnet-4",
            max_tokens=1024,
            temperature=0.7,  # Higher temperature for diversity
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract final answer
        answer = extract_final_answer(response.content[0].text)
        answers.append(answer)

    # Majority vote
    from collections import Counter
    most_common = Counter(answers).most_common(1)[0][0]

    return most_common

# Example
answer = self_consistency(
    "If a train travels 120 miles in 2 hours, then 180 miles in 3 hours, what is its average speed?",
    num_samples=5
)
```

**When to Use Self-Consistency**:
- High-stakes decisions
- Math/logic problems with discrete answers
- Classification tasks
- When accuracy is more important than latency/cost

### Comparison of Patterns

| Pattern | Complexity | Cost | Best For | Latency |
|---------|-----------|------|----------|---------|
| **CoT** | Low | Low | Reasoning, math | Low |
| **ToT** | High | Very High | Strategic planning | Very High |
| **ReAct** | Medium | Medium | Tool use, research | Medium |
| **Self-Consistency** | Medium | High | High-accuracy tasks | High |

### Hybrid Patterns (2025 Best Practices)

**CoT + ReAct**:
```python
# Combine reasoning with tool use
prompt = """
Question: {question}

You have access to: search, calculator, code_executor

Think step by step AND use tools when needed.

Format:
Thought: [reasoning]
Action: [tool if needed]
Observation: [result]
... (repeat)
Answer: [final answer]
"""
```

**ToT + ReAct**:
- Use ToT for strategic planning
- Use ReAct for execution of each branch
- Best for complex planning + execution tasks

---

## 3. LangGraph Workflows

### Overview

**LangGraph** is a framework for building **stateful, multi-agent applications** with LLMs. It implements state machines and directed graphs for orchestration.

**Key Innovation**: Persistent state management across agent interactions with time-travel debugging and human-in-the-loop support.

### Core Architecture

#### StateGraph

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

# Define state
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    current_agent: str
    intermediate_results: dict

# Create graph
workflow = StateGraph(AgentState)

# Add nodes (agents)
workflow.add_node("researcher", research_agent)
workflow.add_node("writer", writing_agent)
workflow.add_node("reviewer", review_agent)

# Add edges (transitions)
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", "reviewer")

# Conditional routing
def should_continue(state):
    last_message = state["messages"][-1]
    if "APPROVED" in last_message:
        return END
    else:
        return "writer"

workflow.add_conditional_edges(
    "reviewer",
    should_continue,
    {
        END: END,
        "writer": "writer"
    }
)

# Set entry point
workflow.set_entry_point("researcher")

# Compile
app = workflow.compile()
```

#### Running the Workflow

```python
# Execute workflow
result = app.invoke({
    "messages": ["Research and write an article about AI safety"],
    "current_agent": "researcher",
    "intermediate_results": {}
})

# Stream intermediate results
for output in app.stream({
    "messages": ["Research and write an article about AI safety"]
}):
    print(output)
```

### Multi-Agent Patterns

#### Supervisor Pattern

**Architecture**: One supervisor coordinates multiple specialized agents

```python
from langgraph.graph import StateGraph
from langchain_anthropic import ChatAnthropic

# Define agents
class ResearchAgent:
    def __init__(self):
        self.llm = ChatAnthropic(model="claude-sonnet-4")

    def run(self, state):
        # Research logic
        prompt = f"Research: {state['task']}"
        response = self.llm.invoke(prompt)
        return {"research_results": response.content}

class CodingAgent:
    def __init__(self):
        self.llm = ChatAnthropic(model="claude-sonnet-4")

    def run(self, state):
        # Coding logic
        prompt = f"Code: {state['task']}"
        response = self.llm.invoke(prompt)
        return {"code": response.content}

class SupervisorAgent:
    def __init__(self):
        self.llm = ChatAnthropic(model="claude-sonnet-4")

    def route(self, state):
        """Decide which agent to use next."""
        prompt = f"""
        Task: {state['task']}
        Progress: {state.get('progress', [])}

        Which agent should handle the next step?
        Options: researcher, coder, FINISH

        Return only one word.
        """
        response = self.llm.invoke(prompt)
        return response.content.strip().lower()

# Build workflow
def create_supervisor_workflow():
    workflow = StateGraph(dict)

    # Add agents
    research_agent = ResearchAgent()
    coding_agent = CodingAgent()
    supervisor = SupervisorAgent()

    workflow.add_node("supervisor", supervisor.route)
    workflow.add_node("researcher", research_agent.run)
    workflow.add_node("coder", coding_agent.run)

    # Conditional routing from supervisor
    def route_based_on_supervisor(state):
        decision = state.get("next_agent", "FINISH")
        if decision == "researcher":
            return "researcher"
        elif decision == "coder":
            return "coder"
        else:
            return END

    workflow.add_conditional_edges(
        "supervisor",
        route_based_on_supervisor
    )

    # Loop back to supervisor
    workflow.add_edge("researcher", "supervisor")
    workflow.add_edge("coder", "supervisor")

    workflow.set_entry_point("supervisor")

    return workflow.compile()
```

#### Swarm Pattern (2025 Update)

**LangGraph Multi-Agent Swarm** orchestrates agents with dynamic hand-offs.

```python
from langgraph_swarm import Swarm, Agent

# Define specialized agents
research_agent = Agent(
    name="Researcher",
    instructions="Research topics thoroughly using available tools",
    tools=[web_search, database_query]
)

analysis_agent = Agent(
    name="Analyst",
    instructions="Analyze data and provide insights",
    tools=[data_analyzer, visualization]
)

writing_agent = Agent(
    name="Writer",
    instructions="Write clear, concise content",
    tools=[grammar_checker, style_guide]
)

# Create swarm
swarm = Swarm(
    agents=[research_agent, analysis_agent, writing_agent],
    initial_agent=research_agent
)

# Agents can hand off to each other
def research_with_handoff(state):
    # Research agent can transfer to analyst
    if state["needs_analysis"]:
        return {"transfer_to": "Analyst"}
    return {"status": "complete"}

# Run swarm
result = swarm.run(
    task="Research AI trends and create analysis report",
    max_handoffs=10
)
```

### Human-in-the-Loop

**Critical Feature**: Pause workflow for human approval

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Enable checkpointing
memory = SqliteSaver.from_conn_string(":memory:")

workflow = StateGraph(AgentState)
# ... add nodes ...

# Compile with checkpointer
app = workflow.compile(checkpointer=memory)

# Run with interrupt
config = {"configurable": {"thread_id": "1"}}

# Step 1: Run until interrupt
for event in app.stream({"messages": ["Write blog post"]}, config):
    print(event)
    # Workflow pauses at designated checkpoint

# Human reviews and approves
# Step 2: Resume from checkpoint
result = app.invoke(None, config)  # Resume from last checkpoint
```

### State Persistence & Time-Travel Debugging

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Persistent storage
checkpointer = SqliteSaver.from_conn_string("./workflow_state.db")

app = workflow.compile(checkpointer=checkpointer)

# Run workflow
config = {"configurable": {"thread_id": "thread_1"}}
result = app.invoke(initial_state, config)

# Later: Retrieve history
history = app.get_state_history(config)

for state in history:
    print(f"Step {state.step}: {state.values}")

# Rewind to specific step
app.update_state(config, {"step": 3})  # Go back to step 3
```

### When to Use LangGraph

✅ **Use LangGraph When**:
- Multi-agent coordination required
- Complex state management needs
- Human-in-the-loop workflows
- Need debugging/observability
- Conditional branching based on outputs
- Building production agent systems

❌ **Don't Use LangGraph When**:
- Simple single-agent tasks
- No state persistence needed
- Prototyping/experimentation phase
- Team lacks graph/state machine expertise

---

## 4. Simpler Approaches Without LangGraph

For teams wanting optimization without framework complexity:

### Template-Based Optimization

**Approach**: Use Jinja2 templates with versioning

```python
from jinja2 import Template
import json

# Define template
PROMPT_TEMPLATE = """
You are a {{ role }}.

Task: {{ task }}

{% if examples %}
Examples:
{% for example in examples %}
Input: {{ example.input }}
Output: {{ example.output }}
{% endfor %}
{% endif %}

{% if constraints %}
Constraints:
{% for constraint in constraints %}
- {{ constraint }}
{% endfor %}
{% endif %}

Now process:
Input: {{ user_input }}
Output:
"""

# Version control for templates
class PromptRegistry:
    def __init__(self):
        self.templates = {}

    def register(self, name, version, template_str):
        key = f"{name}_v{version}"
        self.templates[key] = Template(template_str)

    def get(self, name, version):
        key = f"{name}_v{version}"
        return self.templates[key]

    def render(self, name, version, **kwargs):
        template = self.get(name, version)
        return template.render(**kwargs)

# Usage
registry = PromptRegistry()

registry.register("qa", 1, PROMPT_TEMPLATE)

prompt = registry.render(
    "qa",
    version=1,
    role="helpful AI assistant",
    task="Answer the question accurately",
    examples=[
        {"input": "What is 2+2?", "output": "4"},
        {"input": "What is the capital of France?", "output": "Paris"}
    ],
    constraints=["Be concise", "Use simple language"],
    user_input="What is the capital of Germany?"
)
```

### A/B Testing Framework

**Approach**: Test prompt variations systematically

```python
import random
from dataclasses import dataclass
from typing import List, Callable

@dataclass
class PromptVariant:
    name: str
    template: str
    weight: float = 1.0  # For weighted sampling

@dataclass
class ABTestResult:
    variant_name: str
    success_rate: float
    avg_latency: float
    total_samples: int

class PromptABTester:
    def __init__(self, variants: List[PromptVariant], metric_fn: Callable):
        self.variants = variants
        self.metric_fn = metric_fn
        self.results = {v.name: [] for v in variants}

    def select_variant(self) -> PromptVariant:
        """Select variant based on weights."""
        total_weight = sum(v.weight for v in self.variants)
        r = random.uniform(0, total_weight)

        cumulative = 0
        for variant in self.variants:
            cumulative += variant.weight
            if r <= cumulative:
                return variant

        return self.variants[-1]

    def run_test(self, test_cases: List[dict], num_iterations: int = 100):
        """Run A/B test across variants."""
        import time

        for _ in range(num_iterations):
            for test_case in test_cases:
                variant = self.select_variant()

                # Execute prompt
                start_time = time.time()
                prompt = variant.template.format(**test_case)
                result = self.execute_llm(prompt)
                latency = time.time() - start_time

                # Evaluate
                score = self.metric_fn(test_case, result)

                self.results[variant.name].append({
                    "score": score,
                    "latency": latency
                })

    def get_results(self) -> List[ABTestResult]:
        """Analyze results."""
        results = []

        for variant_name, scores in self.results.items():
            if not scores:
                continue

            success_rate = sum(s["score"] for s in scores) / len(scores)
            avg_latency = sum(s["latency"] for s in scores) / len(scores)

            results.append(ABTestResult(
                variant_name=variant_name,
                success_rate=success_rate,
                avg_latency=avg_latency,
                total_samples=len(scores)
            ))

        return sorted(results, key=lambda x: x.success_rate, reverse=True)

    def execute_llm(self, prompt: str):
        # Replace with actual LLM call
        import anthropic
        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-sonnet-4",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

# Example usage
variants = [
    PromptVariant(
        name="concise",
        template="Answer briefly: {question}",
        weight=0.5
    ),
    PromptVariant(
        name="detailed",
        template="Provide a detailed answer with examples: {question}",
        weight=0.3
    ),
    PromptVariant(
        name="step_by_step",
        template="Answer step by step:\n{question}",
        weight=0.2
    )
]

def accuracy_metric(test_case, result):
    # Custom metric
    return 1.0 if test_case["expected"] in result else 0.0

tester = PromptABTester(variants, accuracy_metric)

test_cases = [
    {"question": "What is 2+2?", "expected": "4"},
    {"question": "Capital of France?", "expected": "Paris"}
]

tester.run_test(test_cases, num_iterations=50)

for result in tester.get_results():
    print(f"{result.variant_name}: {result.success_rate:.2%} success, {result.avg_latency:.3f}s latency")
```

### Gradient-Free Optimization

**Approach**: Use evolutionary algorithms or grid search

```python
from typing import List, Dict, Callable
import random

class PromptEvolution:
    """Evolutionary optimization for prompts."""

    def __init__(
        self,
        base_prompt: str,
        mutations: List[Callable[[str], str]],
        fitness_fn: Callable[[str], float],
        population_size: int = 10,
        generations: int = 20
    ):
        self.base_prompt = base_prompt
        self.mutations = mutations
        self.fitness_fn = fitness_fn
        self.population_size = population_size
        self.generations = generations

    def mutate(self, prompt: str) -> str:
        """Apply random mutation."""
        mutation = random.choice(self.mutations)
        return mutation(prompt)

    def evolve(self) -> str:
        """Run evolutionary optimization."""
        # Initialize population
        population = [self.base_prompt]
        for _ in range(self.population_size - 1):
            population.append(self.mutate(self.base_prompt))

        for generation in range(self.generations):
            # Evaluate fitness
            scored = [(p, self.fitness_fn(p)) for p in population]
            scored.sort(key=lambda x: x[1], reverse=True)

            print(f"Generation {generation}: Best fitness = {scored[0][1]:.3f}")

            # Select top performers
            survivors = [p for p, _ in scored[:self.population_size // 2]]

            # Generate new population
            population = survivors[:]
            while len(population) < self.population_size:
                parent = random.choice(survivors)
                child = self.mutate(parent)
                population.append(child)

        # Return best prompt
        final_scored = [(p, self.fitness_fn(p)) for p in population]
        best_prompt = max(final_scored, key=lambda x: x[1])[0]

        return best_prompt

# Define mutations
def add_context(prompt: str) -> str:
    contexts = [
        "You are an expert assistant.",
        "You are a helpful AI.",
        "You are a knowledgeable guide."
    ]
    return f"{random.choice(contexts)}\n\n{prompt}"

def add_constraint(prompt: str) -> str:
    constraints = [
        "Be concise.",
        "Use simple language.",
        "Provide examples."
    ]
    return f"{prompt}\n\n{random.choice(constraints)}"

def add_format_instruction(prompt: str) -> str:
    formats = [
        "Format your answer as a list.",
        "Use markdown formatting.",
        "Structure your response clearly."
    ]
    return f"{prompt}\n\n{random.choice(formats)}"

# Fitness function
def evaluate_prompt_quality(prompt: str) -> float:
    """Evaluate prompt quality (replace with real evaluation)."""
    # Example: run on test set and measure accuracy
    test_cases = [...]  # Your test cases
    correct = 0

    for case in test_cases:
        result = llm(prompt.format(**case))
        if is_correct(result, case["expected"]):
            correct += 1

    return correct / len(test_cases)

# Run evolution
optimizer = PromptEvolution(
    base_prompt="Answer the question: {question}",
    mutations=[add_context, add_constraint, add_format_instruction],
    fitness_fn=evaluate_prompt_quality,
    population_size=10,
    generations=15
)

best_prompt = optimizer.evolve()
print(f"Optimized prompt:\n{best_prompt}")
```

### Few-Shot Learning with Embeddings

**Approach**: Select best examples using semantic similarity

```python
import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer

class SemanticFewShotSelector:
    """Select few-shot examples using embeddings."""

    def __init__(self, examples: List[Dict], model_name: str = "all-MiniLM-L6-v2"):
        self.examples = examples
        self.model = SentenceTransformer(model_name)

        # Precompute embeddings
        texts = [ex["input"] for ex in examples]
        self.embeddings = self.model.encode(texts)

    def select_examples(self, query: str, k: int = 3) -> List[Dict]:
        """Select k most similar examples."""
        # Embed query
        query_embedding = self.model.encode([query])[0]

        # Compute similarities
        similarities = np.dot(self.embeddings, query_embedding)

        # Get top k
        top_k_indices = np.argsort(similarities)[-k:][::-1]

        return [self.examples[i] for i in top_k_indices]

    def build_prompt(self, query: str, k: int = 3) -> str:
        """Build prompt with selected examples."""
        selected = self.select_examples(query, k)

        prompt = "Examples:\n\n"
        for ex in selected:
            prompt += f"Input: {ex['input']}\nOutput: {ex['output']}\n\n"

        prompt += f"Now process:\nInput: {query}\nOutput:"

        return prompt

# Usage
examples = [
    {"input": "What is 2+2?", "output": "4"},
    {"input": "What is 5*3?", "output": "15"},
    {"input": "What is the capital of France?", "output": "Paris"},
    {"input": "Who wrote Hamlet?", "output": "William Shakespeare"},
    # ... hundreds more examples
]

selector = SemanticFewShotSelector(examples)

# Automatically selects most relevant examples
prompt = selector.build_prompt("What is 7*8?", k=3)
# Will select the math examples, not the geography/literature ones
```

### Prompt Versioning (Git-Based)

**Approach**: Store prompts in Git with semantic versioning

```yaml
# prompts/qa_prompt/v1.0.0.yaml
version: "1.0.0"
name: "qa_prompt"
description: "Basic QA prompt"
template: |
  Answer the question:
  Q: {question}
  A:

# prompts/qa_prompt/v1.1.0.yaml
version: "1.1.0"
name: "qa_prompt"
description: "QA prompt with few-shot examples"
template: |
  Examples:
  Q: What is 2+2?
  A: 4

  Q: What is the capital of France?
  A: Paris

  Now answer:
  Q: {question}
  A:
```

```python
import yaml
from pathlib import Path
from packaging import version as version_parser

class PromptVersionManager:
    """Manage prompt versions using semantic versioning."""

    def __init__(self, prompts_dir: str = "./prompts"):
        self.prompts_dir = Path(prompts_dir)

    def list_versions(self, prompt_name: str) -> List[str]:
        """List all versions of a prompt."""
        prompt_dir = self.prompts_dir / prompt_name
        versions = []

        for yaml_file in prompt_dir.glob("v*.yaml"):
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
                versions.append(data["version"])

        # Sort by semantic version
        versions.sort(key=lambda v: version_parser.parse(v))
        return versions

    def get_prompt(self, prompt_name: str, version: str = "latest") -> str:
        """Get specific version of prompt."""
        if version == "latest":
            versions = self.list_versions(prompt_name)
            version = versions[-1] if versions else None

        if not version:
            raise ValueError(f"No versions found for {prompt_name}")

        yaml_file = self.prompts_dir / prompt_name / f"v{version}.yaml"

        with open(yaml_file) as f:
            data = yaml.safe_load(f)
            return data["template"]

    def rollback(self, prompt_name: str) -> str:
        """Rollback to previous version."""
        versions = self.list_versions(prompt_name)
        if len(versions) < 2:
            raise ValueError("No previous version to rollback to")

        previous_version = versions[-2]
        return self.get_prompt(prompt_name, previous_version)

# Usage
manager = PromptVersionManager()

# Get latest version
prompt = manager.get_prompt("qa_prompt", "latest")

# Get specific version
prompt_v1 = manager.get_prompt("qa_prompt", "1.0.0")

# Rollback if new version has issues
previous = manager.rollback("qa_prompt")
```

---

## 5. Evaluation Frameworks

### LangSmith

**Purpose**: Tracing, debugging, and evaluation for LangChain/LangGraph applications

#### Key Features

1. **Automatic Tracing**: Captures all LLM calls with inputs/outputs
2. **Dataset Management**: Build test sets for evaluation
3. **Evaluators**: Off-the-shelf and custom scoring functions
4. **Version Comparison**: Compare prompt/model versions
5. **Production Monitoring**: Real-time quality tracking

#### Basic Usage

```python
import os
from langsmith import Client
from langsmith.evaluation import evaluate

# Initialize client
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"

client = Client()

# Create dataset
examples = [
    {
        "inputs": {"question": "What is 2+2?"},
        "outputs": {"answer": "4"}
    },
    {
        "inputs": {"question": "Capital of France?"},
        "outputs": {"answer": "Paris"}
    }
]

dataset = client.create_dataset(
    dataset_name="qa_test_set",
    description="Test questions for QA system"
)

for example in examples:
    client.create_example(
        dataset_id=dataset.id,
        inputs=example["inputs"],
        outputs=example["outputs"]
    )

# Define your LLM function
def qa_function(inputs: dict) -> dict:
    from langchain_anthropic import ChatAnthropic

    llm = ChatAnthropic(model="claude-sonnet-4")
    response = llm.invoke(inputs["question"])

    return {"answer": response.content}

# Define evaluator
def correctness_evaluator(run, example):
    """Check if answer matches expected."""
    predicted = run.outputs["answer"]
    expected = example.outputs["answer"]

    return {
        "key": "correctness",
        "score": 1.0 if expected.lower() in predicted.lower() else 0.0
    }

# Run evaluation
results = evaluate(
    qa_function,
    data="qa_test_set",
    evaluators=[correctness_evaluator],
    experiment_prefix="qa_v1"
)

print(f"Average correctness: {results['results']['correctness']:.2%}")
```

#### LLM-as-Judge Evaluator

```python
from langsmith.evaluation import LangChainStringEvaluator

# Use LLM to evaluate quality
quality_evaluator = LangChainStringEvaluator(
    "qa",
    config={
        "criteria": {
            "accuracy": "Is the answer factually correct?",
            "completeness": "Does the answer fully address the question?",
            "clarity": "Is the answer clear and easy to understand?"
        }
    },
    prepare_data=lambda run, example: {
        "prediction": run.outputs["answer"],
        "reference": example.outputs["answer"],
        "input": example.inputs["question"]
    }
)

results = evaluate(
    qa_function,
    data="qa_test_set",
    evaluators=[quality_evaluator]
)
```

#### Version Comparison

```python
# Evaluate multiple prompt versions
def qa_v1(inputs):
    # Version 1 implementation
    pass

def qa_v2(inputs):
    # Version 2 implementation with improvements
    pass

# Compare
results_v1 = evaluate(qa_v1, data="qa_test_set", experiment_prefix="v1")
results_v2 = evaluate(qa_v2, data="qa_test_set", experiment_prefix="v2")

# View comparison in LangSmith UI
```

### Weights & Biases (W&B Weave)

**Purpose**: Experiment tracking, logging, and evaluation for LLM applications

#### Key Features

1. **Automatic Logging**: Tracks all inputs, outputs, tokens, costs
2. **Trace Visualization**: See execution flow
3. **Version Control**: Automatic versioning of code, datasets, scorers
4. **Evaluations**: Compare experiments side-by-side
5. **Cost Tracking**: Monitor token usage and costs

#### Basic Usage

```python
import weave
from anthropic import Anthropic

# Initialize Weave
weave.init("my-project")

# Weave automatically tracks this function
@weave.op()
def qa_pipeline(question: str) -> str:
    client = Anthropic()

    response = client.messages.create(
        model="claude-sonnet-4",
        max_tokens=1024,
        messages=[{"role": "user", "content": question}]
    )

    return response.content[0].text

# Calls are automatically logged
result = qa_pipeline("What is the capital of France?")

# View traces in W&B dashboard
```

#### Evaluation with Weave

```python
import weave

# Define evaluation dataset
dataset = [
    {"question": "What is 2+2?", "expected": "4"},
    {"question": "Capital of France?", "expected": "Paris"}
]

# Define scorer
@weave.op()
def accuracy_score(expected: str, model_output: str) -> dict:
    correct = expected.lower() in model_output.lower()
    return {"correct": correct}

# Run evaluation
evaluation = weave.Evaluation(
    dataset=dataset,
    scorers=[accuracy_score]
)

results = evaluation.evaluate(qa_pipeline)

# Results automatically tracked in W&B
print(f"Accuracy: {results['accuracy_score']['correct']}")
```

#### Multi-Dimensional Scoring

```python
@weave.op()
def quality_scorer(expected: str, model_output: str) -> dict:
    """Score across multiple dimensions."""
    return {
        "accuracy": 1.0 if expected in model_output else 0.0,
        "length": len(model_output),
        "has_explanation": 1.0 if len(model_output) > 20 else 0.0
    }

evaluation = weave.Evaluation(
    dataset=dataset,
    scorers=[quality_scorer]
)

results = evaluation.evaluate(qa_pipeline)

# View breakdown in W&B dashboard
```

### Other Evaluation Platforms (2025)

#### Helicone

**Focus**: Open-source monitoring and prompt versioning

```python
from helicone import Helicone

client = Helicone(api_key="your-key")

# Automatic prompt versioning
response = client.chat.completions.create(
    model="claude-sonnet-4",
    messages=[{"role": "user", "content": "Hello"}],
    helicone_properties={
        "Prompt-Id": "greeting_prompt",
        "Prompt-Version": "v2.1"
    }
)

# Track in Helicone dashboard
```

#### Promptfoo (Open Source)

**Focus**: Testing and CI/CD integration

```yaml
# promptfooconfig.yaml
description: "QA System Tests"

prompts:
  - "Answer: {{question}}"
  - "Provide a brief answer: {{question}}"

providers:
  - anthropic:claude-sonnet-4

tests:
  - vars:
      question: "What is 2+2?"
    assert:
      - type: contains
        value: "4"

  - vars:
      question: "Capital of France?"
    assert:
      - type: contains-any
        value: ["Paris", "paris"]
      - type: cost
        threshold: 0.01  # Max cost per call
```

```bash
# Run tests
promptfoo eval

# View results
promptfoo view

# CI/CD integration
promptfoo eval --output junit.xml
```

#### Braintrust

**Focus**: Production observability with environment management

```python
from braintrust import Eval, current_experiment

def qa_task(input):
    # Your QA logic
    return {"answer": llm_call(input["question"])}

Eval(
    "QA System",
    data=lambda: [
        {"input": {"question": "What is 2+2?"}, "expected": "4"},
    ],
    task=qa_task,
    scores=[
        lambda output, expected: {
            "accuracy": 1 if expected in output["answer"] else 0
        }
    ]
)
```

### Comparison of Evaluation Tools

| Tool | Open Source | Tracing | Versioning | CI/CD | Cost Tracking | Best For |
|------|-------------|---------|------------|-------|---------------|----------|
| **LangSmith** | No | ✅ Excellent | ✅ Yes | ⚠️ Limited | ✅ Yes | LangChain apps |
| **W&B Weave** | No | ✅ Excellent | ✅ Automatic | ✅ Yes | ✅ Yes | ML teams, experiments |
| **Helicone** | Yes | ✅ Yes | ✅ Excellent | ✅ Yes | ✅ Yes | Prompt versioning |
| **Promptfoo** | Yes | ⚠️ Basic | ⚠️ Manual | ✅ Excellent | ⚠️ Basic | Testing, CI/CD |
| **Braintrust** | No | ✅ Yes | ✅ Environment-based | ✅ Yes | ✅ Yes | Production monitoring |

---

## 6. Production Patterns

### Prompt Registry Pattern

**Goal**: Centralized prompt management with versioning

```python
from typing import Dict, Optional
from datetime import datetime
import hashlib

class PromptRegistry:
    """Production-grade prompt registry."""

    def __init__(self, storage_backend):
        self.storage = storage_backend
        self.cache = {}

    def register(
        self,
        name: str,
        template: str,
        version: str,
        metadata: Optional[Dict] = None
    ):
        """Register a new prompt version."""
        prompt_id = f"{name}:{version}"

        prompt_data = {
            "id": prompt_id,
            "name": name,
            "version": version,
            "template": template,
            "metadata": metadata or {},
            "created_at": datetime.utcnow().isoformat(),
            "hash": hashlib.sha256(template.encode()).hexdigest()
        }

        self.storage.save(prompt_id, prompt_data)
        self.cache[prompt_id] = prompt_data

    def get(self, name: str, version: str = "latest") -> str:
        """Retrieve prompt template."""
        if version == "latest":
            version = self.storage.get_latest_version(name)

        prompt_id = f"{name}:{version}"

        # Check cache
        if prompt_id in self.cache:
            return self.cache[prompt_id]["template"]

        # Load from storage
        prompt_data = self.storage.load(prompt_id)
        self.cache[prompt_id] = prompt_data

        return prompt_data["template"]

    def rollback(self, name: str) -> str:
        """Rollback to previous version."""
        versions = self.storage.list_versions(name)
        if len(versions) < 2:
            raise ValueError("No previous version available")

        previous_version = versions[-2]
        return self.get(name, previous_version)

# Storage backend example (Redis)
class RedisPromptStorage:
    def __init__(self, redis_client):
        self.redis = redis_client

    def save(self, prompt_id: str, data: dict):
        self.redis.set(f"prompt:{prompt_id}", json.dumps(data))

        # Track versions
        name = data["name"]
        self.redis.zadd(
            f"versions:{name}",
            {data["version"]: datetime.fromisoformat(data["created_at"]).timestamp()}
        )

    def load(self, prompt_id: str) -> dict:
        data = self.redis.get(f"prompt:{prompt_id}")
        return json.loads(data)

    def get_latest_version(self, name: str) -> str:
        versions = self.redis.zrange(f"versions:{name}", -1, -1)
        return versions[0].decode() if versions else None

    def list_versions(self, name: str) -> list:
        versions = self.redis.zrange(f"versions:{name}", 0, -1)
        return [v.decode() for v in versions]

# Usage
import redis

redis_client = redis.Redis(host="localhost", port=6379)
storage = RedisPromptStorage(redis_client)
registry = PromptRegistry(storage)

# Register prompts
registry.register(
    name="qa_prompt",
    version="1.0.0",
    template="Answer: {question}",
    metadata={"author": "team@company.com", "tested": True}
)

# Use in production
prompt_template = registry.get("qa_prompt", "latest")
```

### Monitoring & Observability

**Goal**: Track quality, cost, and latency in production

```python
from dataclasses import dataclass
from typing import Optional
import time

@dataclass
class LLMMetrics:
    prompt_id: str
    prompt_version: str
    model: str
    latency_ms: float
    tokens_input: int
    tokens_output: int
    cost_usd: float
    success: bool
    error: Optional[str] = None

class LLMMonitor:
    """Monitor LLM calls in production."""

    def __init__(self, metrics_backend):
        self.metrics = metrics_backend

    def track_call(
        self,
        prompt_id: str,
        prompt_version: str,
        model: str,
        input_text: str,
        output_text: str,
        latency_ms: float,
        success: bool,
        error: Optional[str] = None
    ):
        """Track individual LLM call."""
        # Calculate tokens (simplified)
        tokens_input = len(input_text.split())
        tokens_output = len(output_text.split())

        # Calculate cost (example rates)
        cost_per_token = {
            "claude-sonnet-4": {"input": 0.003/1000, "output": 0.015/1000},
            "gpt-4": {"input": 0.03/1000, "output": 0.06/1000}
        }

        rates = cost_per_token.get(model, {"input": 0, "output": 0})
        cost_usd = (tokens_input * rates["input"] +
                   tokens_output * rates["output"])

        metrics = LLMMetrics(
            prompt_id=prompt_id,
            prompt_version=prompt_version,
            model=model,
            latency_ms=latency_ms,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            cost_usd=cost_usd,
            success=success,
            error=error
        )

        self.metrics.record(metrics)

        # Check alerts
        self._check_alerts(metrics)

    def _check_alerts(self, metrics: LLMMetrics):
        """Check if metrics exceed thresholds."""
        # Latency alert
        if metrics.latency_ms > 5000:  # 5 seconds
            self.metrics.alert(
                f"High latency: {metrics.latency_ms}ms for {metrics.prompt_id}"
            )

        # Cost alert
        if metrics.cost_usd > 0.10:  # $0.10 per call
            self.metrics.alert(
                f"High cost: ${metrics.cost_usd} for {metrics.prompt_id}"
            )

        # Error alert
        if not metrics.success:
            self.metrics.alert(
                f"LLM call failed: {metrics.error}"
            )

# Metrics backend (Prometheus example)
from prometheus_client import Counter, Histogram, Gauge

class PrometheusMetrics:
    def __init__(self):
        self.call_count = Counter(
            "llm_calls_total",
            "Total LLM calls",
            ["prompt_id", "model", "success"]
        )

        self.latency = Histogram(
            "llm_latency_ms",
            "LLM call latency",
            ["prompt_id", "model"]
        )

        self.cost = Counter(
            "llm_cost_usd",
            "LLM cost in USD",
            ["prompt_id", "model"]
        )

        self.tokens = Counter(
            "llm_tokens_total",
            "Total tokens used",
            ["prompt_id", "model", "direction"]
        )

    def record(self, metrics: LLMMetrics):
        self.call_count.labels(
            prompt_id=metrics.prompt_id,
            model=metrics.model,
            success=str(metrics.success)
        ).inc()

        self.latency.labels(
            prompt_id=metrics.prompt_id,
            model=metrics.model
        ).observe(metrics.latency_ms)

        self.cost.labels(
            prompt_id=metrics.prompt_id,
            model=metrics.model
        ).inc(metrics.cost_usd)

        self.tokens.labels(
            prompt_id=metrics.prompt_id,
            model=metrics.model,
            direction="input"
        ).inc(metrics.tokens_input)

        self.tokens.labels(
            prompt_id=metrics.prompt_id,
            model=metrics.model,
            direction="output"
        ).inc(metrics.tokens_output)

    def alert(self, message: str):
        # Send to alerting system (PagerDuty, Slack, etc.)
        print(f"ALERT: {message}")
```

### Rollback Strategy

**Goal**: Quickly revert to previous version on issues

```python
class PromptDeploymentManager:
    """Manage prompt deployments with rollback capability."""

    def __init__(self, registry: PromptRegistry, monitor: LLMMonitor):
        self.registry = registry
        self.monitor = monitor
        self.active_versions = {}  # name -> version

    def deploy(self, name: str, version: str, canary_percentage: float = 0.1):
        """Deploy new prompt version with canary."""
        import random

        # Store previous version
        previous = self.active_versions.get(name)

        # Gradual rollout
        def get_version(name: str) -> str:
            if random.random() < canary_percentage:
                return version
            else:
                return previous if previous else version

        # Monitor canary
        canary_metrics = self._monitor_canary(name, version, duration_minutes=10)

        # Decide: continue or rollback
        if self._is_healthy(canary_metrics):
            # Full deployment
            self.active_versions[name] = version
            print(f"Successfully deployed {name}:{version}")
        else:
            # Rollback
            print(f"Canary failed for {name}:{version}, rolling back to {previous}")
            self.rollback(name)

    def rollback(self, name: str):
        """Rollback to previous version."""
        previous_version = self.registry.rollback(name)
        self.active_versions[name] = previous_version
        print(f"Rolled back {name} to {previous_version}")

    def _monitor_canary(self, name: str, version: str, duration_minutes: int):
        """Monitor canary deployment."""
        # Collect metrics for canary period
        # In production, this would query metrics backend
        return {
            "error_rate": 0.02,
            "avg_latency_ms": 850,
            "p95_latency_ms": 1500,
            "avg_cost_usd": 0.015
        }

    def _is_healthy(self, metrics: dict) -> bool:
        """Check if metrics are within acceptable thresholds."""
        return (
            metrics["error_rate"] < 0.05 and
            metrics["p95_latency_ms"] < 2000 and
            metrics["avg_cost_usd"] < 0.05
        )

# Usage
manager = PromptDeploymentManager(registry, monitor)

# Deploy with canary
manager.deploy("qa_prompt", "2.0.0", canary_percentage=0.1)
```

### Cost Optimization

**Goal**: Reduce LLM costs without sacrificing quality

```python
class CostOptimizer:
    """Optimize LLM costs."""

    def __init__(self):
        self.cache = {}  # Semantic cache

    def optimize_prompt(self, prompt: str) -> str:
        """Reduce prompt length while maintaining quality."""
        # Remove unnecessary whitespace
        optimized = " ".join(prompt.split())

        # Abbreviate common phrases
        replacements = {
            "Please provide": "Provide",
            "I would like you to": "Please",
            "Can you please": "Please",
        }

        for old, new in replacements.items():
            optimized = optimized.replace(old, new)

        return optimized

    def semantic_cache(self, query: str, llm_fn, threshold: float = 0.95):
        """Cache similar queries to avoid repeated LLM calls."""
        from sentence_transformers import SentenceTransformer, util

        model = SentenceTransformer('all-MiniLM-L6-v2')
        query_embedding = model.encode(query)

        # Check cache for similar queries
        for cached_query, cached_result in self.cache.items():
            cached_embedding = model.encode(cached_query)
            similarity = util.cos_sim(query_embedding, cached_embedding).item()

            if similarity > threshold:
                print(f"Cache hit! Similarity: {similarity:.3f}")
                return cached_result

        # Cache miss: call LLM
        result = llm_fn(query)
        self.cache[query] = result

        return result

    def use_cheaper_model(self, task_complexity: str):
        """Select model based on task complexity."""
        models = {
            "simple": "claude-haiku",      # Cheapest
            "medium": "claude-sonnet",     # Balanced
            "complex": "claude-opus"       # Most capable
        }

        return models.get(task_complexity, "claude-sonnet")

    def batch_requests(self, queries: list, batch_size: int = 10):
        """Batch multiple queries into single request."""
        batched_prompt = "Answer each question:\n\n"

        for i, query in enumerate(queries[:batch_size], 1):
            batched_prompt += f"{i}. {query}\n"

        # Single LLM call instead of N calls
        return batched_prompt

# Usage
optimizer = CostOptimizer()

# Optimize prompt
original = "Please provide a detailed answer to the following question: What is AI?"
optimized = optimizer.optimize_prompt(original)

# Use semantic cache
def expensive_llm_call(query):
    # Actual LLM call
    pass

result = optimizer.semantic_cache("What is machine learning?", expensive_llm_call)
# Next similar query uses cache instead of calling LLM again
```

### Latency Optimization

**Goal**: Reduce response time

```python
import asyncio
from typing import List

class LatencyOptimizer:
    """Optimize LLM latency."""

    async def parallel_calls(self, prompts: List[str]):
        """Execute multiple LLM calls in parallel."""
        tasks = [self._async_llm_call(p) for p in prompts]
        results = await asyncio.gather(*tasks)
        return results

    async def _async_llm_call(self, prompt: str):
        """Async LLM call."""
        from anthropic import AsyncAnthropic

        client = AsyncAnthropic()
        response = await client.messages.create(
            model="claude-sonnet-4",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text

    def streaming_response(self, prompt: str):
        """Use streaming for faster time-to-first-token."""
        from anthropic import Anthropic

        client = Anthropic()

        with client.messages.stream(
            model="claude-sonnet-4",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            for text in stream.text_stream:
                yield text  # Stream tokens as they arrive

    def reduce_max_tokens(self, task_type: str):
        """Set appropriate max_tokens based on task."""
        max_tokens_map = {
            "classification": 10,
            "short_answer": 50,
            "summary": 200,
            "essay": 2000
        }

        return max_tokens_map.get(task_type, 1024)

# Usage
optimizer = LatencyOptimizer()

# Parallel execution
prompts = ["Question 1?", "Question 2?", "Question 3?"]
results = asyncio.run(optimizer.parallel_calls(prompts))

# Streaming
for chunk in optimizer.streaming_response("Write a short story"):
    print(chunk, end="", flush=True)
```

---

## 7. Comparison Matrix

### Approach Comparison

| Approach | Automation | Complexity | Setup Time | Best For | Learning Curve |
|----------|-----------|------------|------------|----------|----------------|
| **DSPy** | ✅ High | Medium | Medium | Structured tasks, optimization | Medium |
| **LangGraph** | ⚠️ Medium | High | High | Multi-agent, complex workflows | High |
| **Manual Patterns (CoT/ToT/ReAct)** | ❌ None | Low | Low | Prototyping, exploration | Low |
| **Template + A/B Testing** | ⚠️ Medium | Low | Low | Simple production systems | Low |
| **Gradient-Free Optimization** | ✅ High | Medium | Medium | When DSPy not applicable | Medium |

### Feature Comparison

| Feature | DSPy | LangGraph | Manual | Template-Based |
|---------|------|-----------|--------|----------------|
| Automatic optimization | ✅ | ❌ | ❌ | ⚠️ (A/B testing) |
| Multi-agent support | ⚠️ (basic) | ✅ | ⚠️ (manual) | ❌ |
| State management | ❌ | ✅ | ❌ | ❌ |
| Version control | ✅ | ⚠️ | ❌ | ✅ |
| Human-in-the-loop | ❌ | ✅ | ✅ | ❌ |
| Production-ready | ✅ | ✅ | ⚠️ | ✅ |
| Debugging tools | ⚠️ | ✅ (excellent) | ❌ | ⚠️ |

### Cost Comparison (Approximate)

| Approach | Development Cost | Compute Cost | Maintenance Cost |
|----------|-----------------|--------------|------------------|
| **DSPy** | Medium (training time) | High (optimization runs) | Low (automated) |
| **LangGraph** | High (complex setup) | Medium | Medium |
| **Manual** | Low (quick start) | Low | High (manual tuning) |
| **Template + A/B** | Low | Medium (A/B testing) | Medium |

---

## 8. Use Case Recommendations

### When to Use DSPy

**Best For**:
- ✅ Structured input/output tasks (classification, extraction, QA)
- ✅ Tasks with clear evaluation metrics
- ✅ Production systems requiring optimization
- ✅ RAG (Retrieval-Augmented Generation) pipelines
- ✅ Code generation with test cases
- ✅ Teams with ML engineering expertise

**Examples**:
- Customer support ticket classification
- Information extraction from documents
- Question answering systems
- SQL query generation
- Code documentation generation

**Sample Decision Tree**:
```
Do you have evaluation data?
├─ No → Use Manual Patterns or Template-based
└─ Yes → Do you need multi-agent coordination?
    ├─ Yes → Use LangGraph
    └─ No → Do you need automatic optimization?
        ├─ Yes → Use DSPy
        └─ No → Use Template-based
```

### When to Use LangGraph

**Best For**:
- ✅ Multi-agent systems with coordination
- ✅ Complex workflows with branching logic
- ✅ Human-in-the-loop approval workflows
- ✅ Stateful conversations and planning
- ✅ Systems requiring debugging/observability
- ✅ Production agents with error recovery

**Examples**:
- Research assistants (research → analyze → write → review)
- Code review workflows (lint → test → review → approve)
- Multi-step data processing pipelines
- Customer service agents with escalation
- Planning and execution systems

### When to Use Manual Patterns

**Best For**:
- ✅ Rapid prototyping and experimentation
- ✅ Creative/open-ended tasks
- ✅ One-off analysis or research
- ✅ Teams without ML engineering
- ✅ Tasks without clear evaluation metrics
- ✅ Budget-constrained projects

**Examples**:
- Brainstorming and ideation
- Content generation
- Ad-hoc data analysis
- Personal assistants
- Educational tutoring

### When to Use Template-Based + A/B Testing

**Best For**:
- ✅ Simple production systems
- ✅ Well-understood tasks
- ✅ Version control requirements
- ✅ Gradual optimization over time
- ✅ Teams familiar with traditional software engineering

**Examples**:
- Email generation templates
- Product description generation
- Simple chatbots
- Notification systems
- Content summarization

### Hybrid Approaches

**DSPy + LangGraph**:
- Use DSPy to optimize individual agents
- Use LangGraph to coordinate optimized agents
- Best for: Complex multi-agent systems requiring both optimization and orchestration

**Manual Patterns + DSPy**:
- Prototype with manual patterns
- Migrate to DSPy for optimization
- Best for: Iterative development with eventual production deployment

---

## 9. Tool Recommendations

### Development Phase

| Phase | Recommended Tools | Why |
|-------|------------------|-----|
| **Prototyping** | Manual patterns, Anthropic Console, ChatGPT | Fast iteration, no setup |
| **Optimization** | DSPy, A/B testing frameworks | Systematic improvement |
| **Evaluation** | Promptfoo, custom scripts | Testing before production |
| **Production** | LangSmith, W&B Weave, Helicone | Monitoring and versioning |

### By Team Size

**Solo Developer / Small Team (1-5)**:
- **Development**: Manual patterns, DSPy for optimization
- **Evaluation**: Promptfoo (open source)
- **Production**: Helicone (open source) or PromptLayer
- **Rationale**: Low cost, simple setup, open source options

**Medium Team (5-20)**:
- **Development**: DSPy + LangGraph for complex systems
- **Evaluation**: LangSmith or W&B Weave
- **Production**: LangSmith + Prometheus
- **Rationale**: Balance of features and cost, team collaboration

**Enterprise (20+)**:
- **Development**: Full DSPy + LangGraph stack
- **Evaluation**: W&B Weave for ML teams, LangSmith for LLM-focused
- **Production**: Braintrust or custom observability platform
- **Rationale**: Enterprise features, compliance, custom integrations

### By Budget

**$0-100/month**:
- Helicone (open source)
- Promptfoo (open source)
- Manual patterns
- Self-hosted monitoring

**$100-1000/month**:
- LangSmith Starter
- W&B Weave
- PromptLayer Pro
- DSPy (free, but compute costs)

**$1000+/month**:
- LangSmith Enterprise
- W&B Weave Enterprise
- Braintrust
- Custom infrastructure

### Technology Stack Recommendations

#### Python-First Teams

**Stack**:
```
Development: DSPy + LangGraph
Evaluation: W&B Weave (ML-friendly)
Production: LangSmith
Infrastructure: Redis (caching), PostgreSQL (storage), Prometheus (metrics)
```

#### JavaScript/TypeScript Teams

**Stack**:
```
Development: LangChain.js + manual patterns
Evaluation: Promptfoo
Production: Helicone
Infrastructure: Node.js, Redis, PostgreSQL
```

#### Multi-Language Teams

**Stack**:
```
Development: REST API wrappers around DSPy/LangGraph
Evaluation: Promptfoo (language-agnostic YAML config)
Production: Helicone (supports all languages)
Infrastructure: API Gateway, Redis, unified monitoring
```

---

## Conclusion

### Key Takeaways

1. **The Industry is Maturing**: 2025 marks a shift from manual prompt engineering to programmatic optimization with frameworks like DSPy.

2. **Three Primary Approaches**:
   - **DSPy**: For automatic optimization with evaluation data
   - **LangGraph**: For complex multi-agent orchestration
   - **Manual/Template**: For prototyping and simple systems

3. **Evaluation is Critical**: Production systems require systematic evaluation, monitoring, and version control.

4. **Cost & Latency Matter**: Semantic caching, model selection, and batching can reduce costs by 40-60%.

5. **Production Readiness**: Companies like JetBlue, Databricks, and Walmart are already using DSPy in production.

### Future Trends (2025 and Beyond)

1. **Continued DSPy Adoption**: More companies moving from manual to automated optimization
2. **LLM-as-Judge**: Using LLMs to evaluate other LLMs becoming standard practice
3. **Multi-Modal Optimization**: Extending prompt optimization to vision, audio, video
4. **Federated Prompt Learning**: Privacy-preserving prompt optimization
5. **Prompt Compression**: Automatic reduction of prompt length without quality loss

### Getting Started Checklist

For teams starting prompt optimization:

- [ ] Choose initial approach (DSPy, LangGraph, or Manual)
- [ ] Set up evaluation dataset (start small, 10-50 examples)
- [ ] Implement basic monitoring (track cost, latency, errors)
- [ ] Establish version control for prompts
- [ ] Define success metrics aligned with business goals
- [ ] Create rollback strategy
- [ ] Set up CI/CD for prompt testing
- [ ] Plan gradual rollout (canary deployment)
- [ ] Document patterns and learnings
- [ ] Build team expertise through experimentation

---

## References

### Primary Sources

1. **DSPy Documentation**: https://dspy.ai/
2. **LangGraph Documentation**: https://www.langchain.com/langgraph
3. **LangSmith**: https://www.langchain.com/langsmith
4. **Weights & Biases Weave**: https://wandb.ai/site/weave/
5. **Promptfoo**: https://www.promptfoo.dev/

### Research Papers

1. "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines" - Stanford NLP
2. "Is It Time To Treat Prompts As Code? A Multi-Use Case Study For Prompt Optimization Using DSPy" (arXiv:2507.03620, 2025)
3. "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
4. "Tree of Thoughts: Deliberate Problem Solving with Large Language Models"
5. "ReAct: Synergizing Reasoning and Acting in Language Models"

### Additional Resources

- Prompt Engineering Guide: https://www.promptingguide.ai/
- DSPy GitHub Examples: https://github.com/stanfordnlp/dspy
- LangGraph Multi-Agent Examples: https://github.com/langchain-ai/langgraph
- Anthropic Prompt Engineering: https://docs.anthropic.com/claude/docs/prompt-engineering

---

**Document Version**: 1.0
**Last Updated**: 2025-11-30
**Maintained By**: Research Team
**Next Review**: 2026-01-30
