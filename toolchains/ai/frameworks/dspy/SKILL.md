---
name: dspy-framework
description: DSPy declarative framework for automatic prompt optimization treating prompts as code with systematic evaluation and compilers. Use when optimizing prompts systematically, building production LLM systems, implementing RAG/classification tasks, or requiring version-controlled reproducible prompts.
---

# DSPy Framework

---
progressive_disclosure:
  entry_point:
    summary: "Declarative framework for automatic prompt optimization treating prompts as code"
    when_to_use:
      - "When optimizing prompts systematically with evaluation data"
      - "When building production LLM systems requiring accuracy improvements"
      - "When implementing RAG, classification, or structured extraction tasks"
      - "When version-controlled, reproducible prompts are needed"
    quick_start:
      - "pip install dspy-ai"
      - "Define signature: class QA(dspy.Signature): question = dspy.InputField(); answer = dspy.OutputField()"
      - "Create module: qa = dspy.ChainOfThought(QA)"
      - "Optimize: optimizer.compile(qa, trainset=examples)"
  token_estimate:
    entry: 75
    full: 5500
---

## Core Philosophy

DSPy (Declarative Self-improving Python) shifts focus from **manual prompt engineering** to **programming language models**. Treat prompts as code with:
- **Declarative signatures** defining inputs/outputs
- **Automatic optimization** via compilers
- **Version control** and systematic testing
- **Reproducible results** across model changes

**Key Principle**: Don't write prompts manually—define task specifications and let DSPy optimize them.

## Core Concepts

### Signatures: Defining Task Interfaces

Signatures specify what your LM module should do (inputs → outputs) without saying how.

**Basic Signature**:
```python
import dspy

# Inline signature (quick)
qa_module = dspy.ChainOfThought("question -> answer")

# Class-based signature (recommended for production)
class QuestionAnswer(dspy.Signature):
    """Answer questions with short factual answers."""

    question = dspy.InputField()
    answer = dspy.OutputField(desc="often between 1 and 5 words")

# Use signature
qa = dspy.ChainOfThought(QuestionAnswer)
response = qa(question="What is the capital of France?")
print(response.answer)  # "Paris"
```

**Advanced Signatures with Type Hints**:
```python
from typing import List

class DocumentSummary(dspy.Signature):
    """Generate concise document summaries."""

    document: str = dspy.InputField(desc="Full text to summarize")
    key_points: List[str] = dspy.OutputField(desc="3-5 bullet points")
    summary: str = dspy.OutputField(desc="2-3 sentence summary")
    sentiment: str = dspy.OutputField(desc="positive, negative, or neutral")

# Type hints provide strong typing and validation
summarizer = dspy.ChainOfThought(DocumentSummary)
result = summarizer(document="Long document text...")
```

**Field Descriptions**:
- Short, descriptive phrases (not full sentences)
- Examples: `desc="often between 1 and 5 words"`, `desc="JSON format"`
- Used by optimizers to improve prompt quality

### Modules: Building Blocks

Modules are DSPy's reasoning patterns—replacements for manual prompt engineering.

**ChainOfThought (CoT)**:
```python
# Zero-shot reasoning
class Reasoning(dspy.Signature):
    """Solve complex problems step by step."""
    problem = dspy.InputField()
    solution = dspy.OutputField()

cot = dspy.ChainOfThought(Reasoning)
result = cot(problem="Roger has 5 tennis balls. He buys 2 cans of 3 balls each. How many total?")
print(result.solution)  # Includes reasoning steps automatically
print(result.rationale)  # Access the chain-of-thought reasoning
```

**Retrieve Module (RAG)**:
```python
class RAGSignature(dspy.Signature):
    """Answer questions using retrieved context."""
    question = dspy.InputField()
    context = dspy.InputField(desc="relevant passages")
    answer = dspy.OutputField(desc="answer based on context")

# Combine retrieval + reasoning
retriever = dspy.Retrieve(k=3)  # Retrieve top 3 passages
rag = dspy.ChainOfThought(RAGSignature)

# Use in pipeline
question = "What is quantum entanglement?"
context = retriever(question).passages
answer = rag(question=question, context=context)
```

**ReAct (Reasoning + Acting)**:
```python
class ResearchTask(dspy.Signature):
    """Research a topic using tools."""
    topic = dspy.InputField()
    findings = dspy.OutputField()

# ReAct interleaves reasoning with tool calls
react = dspy.ReAct(ResearchTask, tools=[web_search, calculator])
result = react(topic="Apple stock price change last month")
# Automatically uses tools when needed
```

**ProgramOfThought**:
```python
# Generate and execute Python code
class MathProblem(dspy.Signature):
    """Solve math problems by writing Python code."""
    problem = dspy.InputField()
    code = dspy.OutputField(desc="Python code to solve problem")
    result = dspy.OutputField(desc="final numerical answer")

pot = dspy.ProgramOfThought(MathProblem)
answer = pot(problem="Calculate compound interest on $1000 at 5% for 10 years")
```

**Custom Modules**:
```python
class MultiStepRAG(dspy.Module):
    """Custom module combining retrieval and reasoning."""

    def __init__(self, num_passages=3):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        # Retrieve relevant passages
        context = self.retrieve(question).passages

        # Generate answer with context
        prediction = self.generate(context=context, question=question)

        # Return with metadata
        return dspy.Prediction(
            answer=prediction.answer,
            context=context,
            rationale=prediction.rationale
        )

# Use custom module
rag = MultiStepRAG(num_passages=5)
optimized_rag = optimizer.compile(rag, trainset=examples)
```

## Optimizers: Automatic Prompt Improvement

Optimizers compile your high-level program into optimized prompts or fine-tuned weights.

### BootstrapFewShot

**Best For**: Small datasets (10-50 examples), quick optimization
**Optimizes**: Few-shot examples only

```python
from dspy.teleprompt import BootstrapFewShot

# Define metric function
def accuracy_metric(example, prediction, trace=None):
    """Evaluate prediction correctness."""
    return example.answer.lower() == prediction.answer.lower()

# Configure optimizer
optimizer = BootstrapFewShot(
    metric=accuracy_metric,
    max_bootstrapped_demos=4,    # Max examples to bootstrap
    max_labeled_demos=16,         # Max labeled examples to consider
    max_rounds=1,                 # Bootstrapping rounds
    max_errors=10                 # Stop after N errors
)

# Training examples
trainset = [
    dspy.Example(question="What is 2+2?", answer="4").with_inputs("question"),
    dspy.Example(question="Capital of France?", answer="Paris").with_inputs("question"),
    # ... more examples
]

# Compile program
qa_module = dspy.ChainOfThought("question -> answer")
optimized_qa = optimizer.compile(
    student=qa_module,
    trainset=trainset
)

# Save optimized program
optimized_qa.save("qa_optimized.json")
```

**How It Works**:
1. Uses your program to generate outputs on training data
2. Filters successful traces using your metric
3. Selects representative examples as demonstrations
4. Returns optimized program with best few-shot examples

### BootstrapFewShotWithRandomSearch

**Best For**: Medium datasets (50-300 examples), better exploration
**Optimizes**: Few-shot examples with candidate exploration

```python
from dspy.teleprompt import BootstrapFewShotWithRandomSearch

config = dict(
    max_bootstrapped_demos=4,
    max_labeled_demos=4,
    num_candidate_programs=10,   # Explore 10 candidate programs
    num_threads=4                # Parallel optimization
)

optimizer = BootstrapFewShotWithRandomSearch(
    metric=accuracy_metric,
    **config
)

optimized_program = optimizer.compile(
    qa_module,
    trainset=training_examples,
    valset=validation_examples  # Optional validation set
)

# Compare candidates
print(f"Best program score: {optimizer.best_score}")
```

**Advantage**: Explores multiple candidate programs in parallel, selecting best performer via random search.

### MIPROv2 (State-of-the-Art 2025)

**Best For**: Large datasets (300+ examples), production systems
**Optimizes**: Instructions AND few-shot examples jointly via Bayesian optimization

```python
import dspy
from dspy.teleprompt import MIPROv2

# Initialize language model
lm = dspy.LM('openai/gpt-4o-mini', api_key='YOUR_API_KEY')
dspy.configure(lm=lm)

# Define comprehensive metric
def quality_metric(example, prediction, trace=None):
    """Multi-dimensional quality scoring."""
    correct = example.answer.lower() in prediction.answer.lower()
    reasonable_length = 10 < len(prediction.answer) < 200
    has_reasoning = hasattr(prediction, 'rationale') and len(prediction.rationale) > 20

    # Weighted composite score
    score = (
        correct * 1.0 +
        reasonable_length * 0.2 +
        has_reasoning * 0.3
    )
    return score / 1.5  # Normalize to [0, 1]

# Initialize MIPROv2 with auto-configuration
teleprompter = MIPROv2(
    metric=quality_metric,
    auto="medium",  # Options: "light", "medium", "heavy"
    num_candidates=10,  # Number of instruction candidates to explore
    init_temperature=1.0  # Temperature for instruction generation
)

# Optimize program
optimized_program = teleprompter.compile(
    dspy.ChainOfThought("question -> answer"),
    trainset=training_examples,
    num_trials=100,  # Bayesian optimization trials
    max_bootstrapped_demos=4,
    max_labeled_demos=8
)

# Save for production
optimized_program.save("production_qa_model.json")
```

**MIPROv2 Auto-Configuration Modes**:
- **`light`**: Fast optimization, ~20 trials, best for iteration (15-30 min)
- **`medium`**: Balanced optimization, ~50 trials, recommended default (30-60 min)
- **`heavy`**: Exhaustive search, ~100+ trials, highest quality (1-3 hours)

**How MIPROv2 Works**:
1. **Bootstrap Candidates**: Generates few-shot example candidates from training data
2. **Propose Instructions**: Creates instruction variations grounded in task dynamics
3. **Bayesian Optimization**: Uses surrogate model to find optimal instruction + example combinations
4. **Joint Optimization**: Optimizes both components together (not separately) for synergy

**Performance Gains** (2025 Study):
- Prompt Evaluation: +38.5% accuracy (46.2% → 64.0%)
- Guardrail Enforcement: +16.9% accuracy (72.1% → 84.3%)
- Code Generation: +21.9% accuracy (58.4% → 71.2%)
- Hallucination Detection: +20.8% accuracy (65.8% → 79.5%)
- Agent Routing: +18.5% accuracy (69.3% → 82.1%)

### KNN Few-Shot Selector

**Best For**: Dynamic example selection based on query similarity

```python
from dspy.teleprompt import KNNFewShot

# Requires embeddings for examples
knn_optimizer = KNNFewShot(
    k=3,  # Select 3 most similar examples
    trainset=training_examples
)

optimized_program = knn_optimizer.compile(qa_module)

# Automatically selects relevant examples at inference time
# Math query → retrieves math examples
# Geography query → retrieves geography examples
```

### SignatureOptimizer

**Best For**: Optimizing signature descriptions and field specifications

```python
from dspy.teleprompt import SignatureOptimizer

sig_optimizer = SignatureOptimizer(
    metric=accuracy_metric,
    breadth=10,  # Number of variations to generate
    depth=3      # Optimization iterations
)

optimized_signature = sig_optimizer.compile(
    initial_signature=QuestionAnswer,
    trainset=trainset
)

# Use optimized signature
qa = dspy.ChainOfThought(optimized_signature)
```

### Sequential Optimization Strategy

Combine optimizers for best results:

```python
# Step 1: Bootstrap few-shot examples (fast)
bootstrap = dspy.BootstrapFewShot(metric=accuracy_metric)
bootstrapped_program = bootstrap.compile(qa_module, trainset=train_examples)

# Step 2: Optimize instructions with MIPRO (comprehensive)
mipro = dspy.MIPROv2(metric=accuracy_metric, auto="medium")
final_program = mipro.compile(
    bootstrapped_program,
    trainset=train_examples,
    num_trials=50
)

# Step 3: Fine-tune signature descriptions
sig_optimizer = dspy.SignatureOptimizer(metric=accuracy_metric)
production_program = sig_optimizer.compile(final_program, trainset=train_examples)

# Save production model
production_program.save("production_optimized.json")
```

## Teleprompters: Compilation Pipelines

Teleprompters orchestrate the optimization process (legacy term for "optimizers").

**Custom Teleprompter**:
```python
class CustomTeleprompter:
    """Custom optimization pipeline."""

    def __init__(self, metric):
        self.metric = metric

    def compile(self, student, trainset, valset=None):
        # Stage 1: Bootstrap examples
        bootstrap = BootstrapFewShot(metric=self.metric)
        stage1 = bootstrap.compile(student, trainset=trainset)

        # Stage 2: Optimize instructions
        mipro = MIPROv2(metric=self.metric, auto="light")
        stage2 = mipro.compile(stage1, trainset=trainset)

        # Stage 3: Validate on held-out set
        if valset:
            score = self._evaluate(stage2, valset)
            print(f"Validation score: {score:.2%}")

        return stage2

    def _evaluate(self, program, dataset):
        correct = 0
        for example in dataset:
            prediction = program(**example.inputs())
            if self.metric(example, prediction):
                correct += 1
        return correct / len(dataset)

# Use custom teleprompter
custom_optimizer = CustomTeleprompter(metric=accuracy_metric)
optimized = custom_optimizer.compile(
    student=qa_module,
    trainset=train_examples,
    valset=val_examples
)
```

## Metrics and Evaluation

### Custom Metrics

**Binary Accuracy**:
```python
def exact_match(example, prediction, trace=None):
    """Exact match metric."""
    return example.answer.lower().strip() == prediction.answer.lower().strip()
```

**Fuzzy Matching**:
```python
from difflib import SequenceMatcher

def fuzzy_match(example, prediction, trace=None):
    """Fuzzy string matching."""
    similarity = SequenceMatcher(
        None,
        example.answer.lower(),
        prediction.answer.lower()
    ).ratio()
    return similarity > 0.8  # 80% similarity threshold
```

**Multi-Criteria**:
```python
def comprehensive_metric(example, prediction, trace=None):
    """Evaluate on multiple criteria."""
    # Correctness
    correct = example.answer.lower() in prediction.answer.lower()

    # Length appropriateness
    length_ok = 10 < len(prediction.answer) < 200

    # Has reasoning (if CoT)
    has_reasoning = (
        hasattr(prediction, 'rationale') and
        len(prediction.rationale) > 30
    )

    # Citation quality (if RAG)
    has_citations = (
        hasattr(prediction, 'context') and
        len(prediction.context) > 0
    )

    # Composite score
    score = sum([
        correct * 1.0,
        length_ok * 0.2,
        has_reasoning * 0.3,
        has_citations * 0.2
    ]) / 1.7

    return score
```

**LLM-as-Judge**:
```python
def llm_judge_metric(example, prediction, trace=None):
    """Use LLM to evaluate quality."""
    judge_prompt = f"""
    Question: {example.question}
    Expected Answer: {example.answer}
    Predicted Answer: {prediction.answer}

    Evaluate the predicted answer on a scale of 0-10 for:
    1. Correctness
    2. Completeness
    3. Clarity

    Return only a number 0-10.
    """

    judge_lm = dspy.LM('openai/gpt-4o-mini')
    response = judge_lm(judge_prompt)
    score = float(response.strip()) / 10.0

    return score > 0.7  # Pass if score > 7/10
```

### Evaluation Pipeline

```python
class Evaluator:
    """Comprehensive evaluation system."""

    def __init__(self, program, metrics):
        self.program = program
        self.metrics = metrics

    def evaluate(self, dataset, verbose=True):
        """Evaluate program on dataset."""
        results = {name: [] for name in self.metrics.keys()}

        for example in dataset:
            prediction = self.program(**example.inputs())

            for metric_name, metric_fn in self.metrics.items():
                score = metric_fn(example, prediction)
                results[metric_name].append(score)

        # Aggregate results
        aggregated = {
            name: sum(scores) / len(scores)
            for name, scores in results.items()
        }

        if verbose:
            print("\nEvaluation Results:")
            print("=" * 50)
            for name, score in aggregated.items():
                print(f"{name:20s}: {score:.2%}")

        return aggregated

# Use evaluator
evaluator = Evaluator(
    program=optimized_qa,
    metrics={
        "accuracy": exact_match,
        "fuzzy_match": fuzzy_match,
        "quality": comprehensive_metric
    }
)

scores = evaluator.evaluate(test_dataset)
```

## Language Model Configuration

### Supported Providers

**OpenAI**:
```python
import dspy

lm = dspy.LM('openai/gpt-4o', api_key='YOUR_API_KEY')
dspy.configure(lm=lm)

# With custom settings
lm = dspy.LM(
    'openai/gpt-4o-mini',
    api_key='YOUR_API_KEY',
    temperature=0.7,
    max_tokens=1024
)
```

**Anthropic Claude**:
```python
lm = dspy.LM(
    'anthropic/claude-3-5-sonnet-20241022',
    api_key='YOUR_ANTHROPIC_KEY',
    max_tokens=4096
)
dspy.configure(lm=lm)

# Claude Opus for complex reasoning
lm_opus = dspy.LM('anthropic/claude-3-opus-20240229', api_key=key)
```

**Local Models (Ollama)**:
```python
# Requires Ollama running locally
lm = dspy.LM('ollama/llama3.1:70b', api_base='http://localhost:11434')
dspy.configure(lm=lm)

# Mixtral
lm = dspy.LM('ollama/mixtral:8x7b')
```

**Multiple Models**:
```python
# Use different models for different stages
strong_lm = dspy.LM('openai/gpt-4o')
fast_lm = dspy.LM('openai/gpt-4o-mini')

# Configure per module
class HybridPipeline(dspy.Module):
    def __init__(self):
        super().__init__()
        # Fast model for retrieval
        self.retrieve = dspy.Retrieve(k=5)

        # Strong model for reasoning
        with dspy.context(lm=strong_lm):
            self.reason = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = self.retrieve(question).passages
        return self.reason(context=context, question=question)
```

### Model Selection Strategy

```python
def select_model(task_complexity, budget):
    """Select appropriate model based on task and budget."""
    models = {
        "simple": [
            ("openai/gpt-4o-mini", 0.15),  # (model, cost per 1M tokens)
            ("anthropic/claude-3-haiku-20240307", 0.25),
        ],
        "medium": [
            ("openai/gpt-4o", 2.50),
            ("anthropic/claude-3-5-sonnet-20241022", 3.00),
        ],
        "complex": [
            ("anthropic/claude-3-opus-20240229", 15.00),
            ("openai/o1-preview", 15.00),
        ]
    }

    candidates = models[task_complexity]
    affordable = [m for m, cost in candidates if cost <= budget]

    return affordable[0] if affordable else candidates[0][0]

# Use in optimization
task = "complex"
model = select_model(task, budget=10.0)
lm = dspy.LM(model)
dspy.configure(lm=lm)
```

## Program Composition

### Chaining Modules

```python
class MultiStepPipeline(dspy.Module):
    """Chain multiple reasoning steps."""

    def __init__(self):
        super().__init__()
        self.step1 = dspy.ChainOfThought("question -> subtasks")
        self.step2 = dspy.ChainOfThought("subtask -> solution")
        self.step3 = dspy.ChainOfThought("solutions -> final_answer")

    def forward(self, question):
        # Break down question
        decomposition = self.step1(question=question)

        # Solve each subtask
        solutions = []
        for subtask in decomposition.subtasks.split('\n'):
            if subtask.strip():
                sol = self.step2(subtask=subtask)
                solutions.append(sol.solution)

        # Synthesize final answer
        combined = '\n'.join(solutions)
        final = self.step3(solutions=combined)

        return dspy.Prediction(
            answer=final.final_answer,
            subtasks=decomposition.subtasks,
            solutions=solutions
        )

# Optimize entire pipeline
pipeline = MultiStepPipeline()
optimizer = MIPROv2(metric=quality_metric, auto="medium")
optimized_pipeline = optimizer.compile(pipeline, trainset=examples)
```

### Conditional Branching

```python
class AdaptivePipeline(dspy.Module):
    """Adapt reasoning based on query type."""

    def __init__(self):
        super().__init__()
        self.classifier = dspy.ChainOfThought("question -> category")
        self.math_solver = dspy.ProgramOfThought("problem -> solution")
        self.fact_qa = dspy.ChainOfThought("question -> answer")
        self.creative = dspy.ChainOfThought("prompt -> response")

    def forward(self, question):
        # Classify query type
        category = self.classifier(question=question).category.lower()

        # Route to appropriate module
        if "math" in category or "calculation" in category:
            return self.math_solver(problem=question)
        elif "creative" in category or "story" in category:
            return self.creative(prompt=question)
        else:
            return self.fact_qa(question=question)

# Optimize each branch independently
adaptive = AdaptivePipeline()
optimized_adaptive = optimizer.compile(adaptive, trainset=diverse_examples)
```

## Production Deployment

### Saving and Loading Models

```python
# Save optimized program
optimized_program.save("models/qa_v1.0.0.json")

# Load in production
production_qa = dspy.ChainOfThought("question -> answer")
production_qa.load("models/qa_v1.0.0.json")

# Use loaded model
response = production_qa(question="What is quantum computing?")
```

### Version Control

```python
import json
from datetime import datetime

class ModelRegistry:
    """Version control for DSPy models."""

    def __init__(self, registry_path="models/registry.json"):
        self.registry_path = registry_path
        self.registry = self._load_registry()

    def register(self, name, version, model_path, metadata=None):
        """Register a model version."""
        model_id = f"{name}:v{version}"

        self.registry[model_id] = {
            "name": name,
            "version": version,
            "path": model_path,
            "created_at": datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }

        self._save_registry()
        return model_id

    def get_model(self, name, version="latest"):
        """Load model by name and version."""
        if version == "latest":
            versions = [
                v for k, v in self.registry.items()
                if v["name"] == name
            ]
            if not versions:
                raise ValueError(f"No versions found for {name}")

            latest = max(versions, key=lambda x: x["created_at"])
            model_path = latest["path"]
        else:
            model_id = f"{name}:v{version}"
            model_path = self.registry[model_id]["path"]

        # Load model
        module = dspy.ChainOfThought("question -> answer")
        module.load(model_path)
        return module

    def _load_registry(self):
        try:
            with open(self.registry_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_registry(self):
        with open(self.registry_path, 'w') as f:
            json.dump(self.registry, f, indent=2)

# Use registry
registry = ModelRegistry()

# Register new version
registry.register(
    name="qa_assistant",
    version="1.0.0",
    model_path="models/qa_v1.0.0.json",
    metadata={
        "accuracy": 0.87,
        "optimizer": "MIPROv2",
        "training_examples": 500
    }
)

# Load for production
qa = registry.get_model("qa_assistant", version="latest")
```

### Monitoring and Logging

```python
import logging
from datetime import datetime

class DSPyMonitor:
    """Monitor DSPy program execution."""

    def __init__(self, program, log_file="logs/dspy.log"):
        self.program = program
        self.logger = self._setup_logger(log_file)
        self.metrics = []

    def __call__(self, **kwargs):
        """Wrap program execution with monitoring."""
        start_time = datetime.utcnow()

        try:
            # Execute program
            result = self.program(**kwargs)

            # Log success
            duration = (datetime.utcnow() - start_time).total_seconds()
            self._log_execution(
                status="success",
                inputs=kwargs,
                outputs=result,
                duration=duration
            )

            return result

        except Exception as e:
            # Log error
            duration = (datetime.utcnow() - start_time).total_seconds()
            self._log_execution(
                status="error",
                inputs=kwargs,
                error=str(e),
                duration=duration
            )
            raise

    def _log_execution(self, status, inputs, duration, outputs=None, error=None):
        """Log execution details."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "status": status,
            "inputs": inputs,
            "duration_seconds": duration
        }

        if outputs:
            log_entry["outputs"] = str(outputs)
        if error:
            log_entry["error"] = error

        self.logger.info(json.dumps(log_entry))
        self.metrics.append(log_entry)

    def _setup_logger(self, log_file):
        """Setup logging."""
        logger = logging.getLogger("dspy_monitor")
        logger.setLevel(logging.INFO)

        handler = logging.FileHandler(log_file)
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(message)s')
        )
        logger.addHandler(handler)

        return logger

    def get_stats(self):
        """Get execution statistics."""
        if not self.metrics:
            return {}

        successes = [m for m in self.metrics if m["status"] == "success"]
        errors = [m for m in self.metrics if m["status"] == "error"]

        return {
            "total_calls": len(self.metrics),
            "success_rate": len(successes) / len(self.metrics),
            "error_rate": len(errors) / len(self.metrics),
            "avg_duration": sum(m["duration_seconds"] for m in self.metrics) / len(self.metrics),
            "errors": [m["error"] for m in errors]
        }

# Use monitor
monitored_qa = DSPyMonitor(optimized_qa)
result = monitored_qa(question="What is AI?")

# Check stats
stats = monitored_qa.get_stats()
print(f"Success rate: {stats['success_rate']:.2%}")
```

## Integration with LangSmith

Evaluate DSPy programs using LangSmith:

```python
import os
from langsmith import Client
from langsmith.evaluation import evaluate

# Setup
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-key"

client = Client()

# Wrap DSPy program for LangSmith
def dspy_wrapper(inputs: dict) -> dict:
    """Wrapper for LangSmith evaluation."""
    question = inputs["question"]
    result = optimized_qa(question=question)
    return {"answer": result.answer}

# Define evaluator
def dspy_evaluator(run, example):
    """Evaluate DSPy output."""
    predicted = run.outputs["answer"]
    expected = example.outputs["answer"]

    return {
        "key": "correctness",
        "score": 1.0 if expected.lower() in predicted.lower() else 0.0
    }

# Create dataset
dataset = client.create_dataset(
    dataset_name="dspy_qa_eval",
    description="DSPy QA evaluation dataset"
)

# Add examples
for example in test_examples:
    client.create_example(
        dataset_id=dataset.id,
        inputs={"question": example.question},
        outputs={"answer": example.answer}
    )

# Run evaluation
results = evaluate(
    dspy_wrapper,
    data="dspy_qa_eval",
    evaluators=[dspy_evaluator],
    experiment_prefix="dspy_v1.0"
)

print(f"Average correctness: {results['results']['correctness']:.2%}")
```

## Real-World Examples

### RAG Pipeline

```python
class ProductionRAG(dspy.Module):
    """Production-ready RAG system."""

    def __init__(self, k=5):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=k)

        # Multi-stage reasoning
        self.rerank = dspy.ChainOfThought(
            "question, passages -> relevant_passages"
        )
        self.generate = dspy.ChainOfThought(
            "question, context -> answer, citations"
        )

    def forward(self, question):
        # Retrieve candidate passages
        candidates = self.retrieve(question).passages

        # Rerank for relevance
        reranked = self.rerank(
            question=question,
            passages="\n---\n".join(candidates)
        )

        # Generate answer with citations
        result = self.generate(
            question=question,
            context=reranked.relevant_passages
        )

        return dspy.Prediction(
            answer=result.answer,
            citations=result.citations,
            passages=candidates
        )

# Optimize RAG pipeline
rag = ProductionRAG(k=10)

def rag_metric(example, prediction, trace=None):
    """Evaluate RAG quality."""
    answer_correct = example.answer.lower() in prediction.answer.lower()
    has_citations = len(prediction.citations) > 0
    return answer_correct and has_citations

optimizer = MIPROv2(metric=rag_metric, auto="heavy")
optimized_rag = optimizer.compile(rag, trainset=rag_examples)
optimized_rag.save("models/rag_production.json")
```

### Classification

```python
class SentimentClassifier(dspy.Module):
    """Multi-class sentiment classification."""

    def __init__(self, classes):
        super().__init__()
        self.classes = classes

        class ClassificationSig(dspy.Signature):
            text = dspy.InputField()
            reasoning = dspy.OutputField(desc="step-by-step reasoning")
            sentiment = dspy.OutputField(desc=f"one of: {', '.join(classes)}")
            confidence = dspy.OutputField(desc="confidence score 0-1")

        self.classify = dspy.ChainOfThought(ClassificationSig)

    def forward(self, text):
        result = self.classify(text=text)

        # Validate output
        if result.sentiment not in self.classes:
            result.sentiment = "neutral"  # Fallback

        return result

# Train classifier
classes = ["positive", "negative", "neutral"]
classifier = SentimentClassifier(classes)

def classification_metric(example, prediction, trace=None):
    return example.sentiment == prediction.sentiment

optimizer = BootstrapFewShot(metric=classification_metric)
optimized_classifier = optimizer.compile(
    classifier,
    trainset=sentiment_examples
)

# Use in production
result = optimized_classifier(text="This product is amazing!")
print(f"Sentiment: {result.sentiment} ({result.confidence})")
```

### Summarization

```python
class DocumentSummarizer(dspy.Module):
    """Hierarchical document summarization."""

    def __init__(self):
        super().__init__()

        # Chunk-level summaries
        self.chunk_summary = dspy.ChainOfThought(
            "chunk -> summary"
        )

        # Document-level synthesis
        self.final_summary = dspy.ChainOfThought(
            "chunk_summaries -> final_summary, key_points"
        )

    def forward(self, document, chunk_size=1000):
        # Split document into chunks
        chunks = self._chunk_document(document, chunk_size)

        # Summarize each chunk
        chunk_summaries = []
        for chunk in chunks:
            summary = self.chunk_summary(chunk=chunk)
            chunk_summaries.append(summary.summary)

        # Synthesize final summary
        combined = "\n---\n".join(chunk_summaries)
        final = self.final_summary(chunk_summaries=combined)

        return dspy.Prediction(
            summary=final.final_summary,
            key_points=final.key_points.split('\n'),
            chunk_count=len(chunks)
        )

    def _chunk_document(self, document, chunk_size):
        """Split document into chunks."""
        words = document.split()
        chunks = []

        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)

        return chunks

# Optimize summarizer
summarizer = DocumentSummarizer()

def summary_metric(example, prediction, trace=None):
    # Check key points coverage
    key_points_present = sum(
        1 for kp in example.key_points
        if kp.lower() in prediction.summary.lower()
    )
    coverage = key_points_present / len(example.key_points)

    # Check length appropriateness
    length_ok = 100 < len(prediction.summary) < 500

    return coverage > 0.7 and length_ok

optimizer = MIPROv2(metric=summary_metric, auto="medium")
optimized_summarizer = optimizer.compile(summarizer, trainset=summary_examples)
```

### Question Answering

```python
class MultiHopQA(dspy.Module):
    """Multi-hop question answering."""

    def __init__(self):
        super().__init__()

        # Decompose complex questions
        self.decompose = dspy.ChainOfThought(
            "question -> subquestions"
        )

        # Answer subquestions with retrieval
        self.retrieve = dspy.Retrieve(k=3)
        self.answer_subq = dspy.ChainOfThought(
            "subquestion, context -> answer"
        )

        # Synthesize final answer
        self.synthesize = dspy.ChainOfThought(
            "question, subanswers -> final_answer, reasoning"
        )

    def forward(self, question):
        # Decompose into subquestions
        decomp = self.decompose(question=question)
        subquestions = [
            sq.strip()
            for sq in decomp.subquestions.split('\n')
            if sq.strip()
        ]

        # Answer each subquestion
        subanswers = []
        for subq in subquestions:
            context = self.retrieve(subq).passages
            answer = self.answer_subq(
                subquestion=subq,
                context="\n".join(context)
            )
            subanswers.append(answer.answer)

        # Synthesize final answer
        combined = "\n".join([
            f"Q: {sq}\nA: {sa}"
            for sq, sa in zip(subquestions, subanswers)
        ])

        final = self.synthesize(
            question=question,
            subanswers=combined
        )

        return dspy.Prediction(
            answer=final.final_answer,
            reasoning=final.reasoning,
            subquestions=subquestions,
            subanswers=subanswers
        )

# Optimize multi-hop QA
multihop_qa = MultiHopQA()

def multihop_metric(example, prediction, trace=None):
    # Check answer correctness
    correct = example.answer.lower() in prediction.answer.lower()

    # Check reasoning quality
    has_reasoning = len(prediction.reasoning) > 50

    # Check subquestion coverage
    has_subquestions = len(prediction.subquestions) >= 2

    return correct and has_reasoning and has_subquestions

optimizer = MIPROv2(metric=multihop_metric, auto="heavy")
optimized_multihop = optimizer.compile(multihop_qa, trainset=multihop_examples)
```

## Migration from Manual Prompting

### Before: Manual Prompting

```python
# Manual prompt engineering
PROMPT = """
You are a helpful assistant. Answer questions accurately and concisely.

Examples:
Q: What is 2+2?
A: 4

Q: Capital of France?
A: Paris

Q: {question}
A: """

def manual_qa(question):
    response = llm.invoke(PROMPT.format(question=question))
    return response
```

### After: DSPy

```python
# DSPy declarative approach
class QA(dspy.Signature):
    """Answer questions accurately and concisely."""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="short factual answer")

qa = dspy.ChainOfThought(QA)

# Optimize automatically
optimizer = MIPROv2(metric=accuracy_metric, auto="medium")
optimized_qa = optimizer.compile(qa, trainset=examples)

def dspy_qa(question):
    result = optimized_qa(question=question)
    return result.answer
```

**Benefits**:
- Systematic optimization vs. manual trial-and-error
- Version control and reproducibility
- Automatic adaptation to new models
- Performance gains: +18-38% accuracy

## Best Practices

### Data Preparation

```python
# Create high-quality training examples
def prepare_training_data(raw_data):
    """Convert raw data to DSPy examples."""
    examples = []

    for item in raw_data:
        example = dspy.Example(
            question=item["question"],
            answer=item["answer"],
            context=item.get("context", "")  # Optional fields
        ).with_inputs("question", "context")  # Mark input fields

        examples.append(example)

    return examples

# Split data properly
def train_val_test_split(examples, train=0.7, val=0.15, test=0.15):
    """Split data for optimization and evaluation."""
    import random
    random.shuffle(examples)

    n = len(examples)
    train_end = int(n * train)
    val_end = int(n * (train + val))

    return {
        "train": examples[:train_end],
        "val": examples[train_end:val_end],
        "test": examples[val_end:]
    }

# Use split data
data = train_val_test_split(all_examples)
optimized = optimizer.compile(
    program,
    trainset=data["train"],
    valset=data["val"]  # For hyperparameter tuning
)

# Final evaluation on held-out test set
evaluator = Evaluator(optimized, metrics={"accuracy": accuracy_metric})
test_results = evaluator.evaluate(data["test"])
```

### Metric Design

```python
# Design metrics aligned with business goals
def business_aligned_metric(example, prediction, trace=None):
    """Metric aligned with business KPIs."""

    # Core correctness (must have)
    correct = example.answer.lower() in prediction.answer.lower()
    if not correct:
        return 0.0

    # Business-specific criteria
    is_concise = len(prediction.answer) < 100  # User preference
    is_professional = not any(
        word in prediction.answer.lower()
        for word in ["um", "like", "maybe", "dunno"]
    )
    has_confidence = (
        hasattr(prediction, 'confidence') and
        float(prediction.confidence) > 0.7
    )

    # Weighted score
    score = (
        correct * 1.0 +
        is_concise * 0.2 +
        is_professional * 0.3 +
        has_confidence * 0.2
    ) / 1.7

    return score
```

### Error Handling

```python
class RobustModule(dspy.Module):
    """Module with error handling."""

    def __init__(self):
        super().__init__()
        self.qa = dspy.ChainOfThought("question -> answer")

    def forward(self, question, max_retries=3):
        """Forward with retry logic."""
        for attempt in range(max_retries):
            try:
                result = self.qa(question=question)

                # Validate output
                if self._validate_output(result):
                    return result
                else:
                    logging.warning(f"Invalid output on attempt {attempt + 1}")

            except Exception as e:
                logging.error(f"Error on attempt {attempt + 1}: {e}")

                if attempt == max_retries - 1:
                    raise

        # Fallback
        return dspy.Prediction(
            answer="I'm unable to answer that question.",
            confidence=0.0
        )

    def _validate_output(self, result):
        """Validate output quality."""
        return (
            hasattr(result, 'answer') and
            len(result.answer) > 0 and
            len(result.answer) < 1000
        )
```

### Caching for Efficiency

```python
from functools import lru_cache
import hashlib

class CachedModule(dspy.Module):
    """Module with semantic caching."""

    def __init__(self, base_module):
        super().__init__()
        self.base_module = base_module
        self.cache = {}

    def forward(self, question):
        # Check cache
        cache_key = self._get_cache_key(question)

        if cache_key in self.cache:
            logging.info("Cache hit")
            return self.cache[cache_key]

        # Cache miss: execute module
        result = self.base_module(question=question)
        self.cache[cache_key] = result

        return result

    def _get_cache_key(self, question):
        """Generate cache key."""
        return hashlib.md5(question.lower().encode()).hexdigest()

# Use cached module
base_qa = dspy.ChainOfThought("question -> answer")
cached_qa = CachedModule(base_qa)
```

## Troubleshooting

### Common Issues

**Low Optimization Performance**:
- Increase training data size (aim for 100+ examples)
- Use better quality metric (more specific)
- Try different optimizer (`auto="heavy"` for MIPROv2)
- Check for data leakage in metric

**Optimization Takes Too Long**:
- Use `auto="light"` instead of `"heavy"`
- Reduce `num_trials` for MIPROv2
- Use BootstrapFewShot instead of MIPROv2 for quick iteration
- Parallelize with `num_threads` parameter

**Inconsistent Results**:
- Set random seed: `dspy.configure(random_seed=42)`
- Increase temperature for diversity or decrease for consistency
- Use ensemble of multiple optimized programs
- Validate on larger test set

**Out of Memory**:
- Reduce batch size in optimization
- Use streaming for large datasets
- Clear cache periodically
- Use smaller model for bootstrapping

### Debugging Optimization

```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.INFO)

# Custom teleprompter with debugging
class DebugTeleprompter:
    def __init__(self, metric):
        self.metric = metric
        self.history = []

    def compile(self, student, trainset):
        print(f"\nStarting optimization with {len(trainset)} examples")

        # Bootstrap with debugging
        bootstrap = BootstrapFewShot(metric=self.metric)

        for i, example in enumerate(trainset):
            prediction = student(**example.inputs())
            score = self.metric(example, prediction)

            self.history.append({
                "example_idx": i,
                "score": score,
                "prediction": str(prediction)
            })

            print(f"Example {i}: score={score}")

        # Continue with optimization
        optimized = bootstrap.compile(student, trainset=trainset)

        print(f"\nOptimization complete")
        print(f"Average score: {sum(h['score'] for h in self.history) / len(self.history):.2f}")

        return optimized

# Use debug teleprompter
debug_optimizer = DebugTeleprompter(metric=accuracy_metric)
optimized = debug_optimizer.compile(qa_module, trainset=examples)
```

## Performance Benchmarks

Based on 2025 production studies:

| Use Case | Baseline | DSPy Optimized | Improvement | Optimizer Used |
|----------|----------|----------------|-------------|----------------|
| Prompt Evaluation | 46.2% | 64.0% | **+38.5%** | MIPROv2 |
| Guardrail Enforcement | 72.1% | 84.3% | **+16.9%** | MIPROv2 |
| Code Generation | 58.4% | 71.2% | **+21.9%** | MIPROv2 |
| Hallucination Detection | 65.8% | 79.5% | **+20.8%** | BootstrapFewShot |
| Agent Routing | 69.3% | 82.1% | **+18.5%** | MIPROv2 |
| RAG Accuracy | 54.0% | 68.5% | **+26.9%** | BootstrapFewShot + MIPRO |

**Production Adopters**: JetBlue, Databricks, Walmart, VMware, Replit, Sephora, Moody's

## Resources

- **Documentation**: https://dspy.ai/
- **GitHub**: https://github.com/stanfordnlp/dspy
- **Paper**: "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines"
- **2025 Study**: "Is It Time To Treat Prompts As Code?" (arXiv:2507.03620)
- **Community**: Discord, GitHub Discussions

## Related Skills

When using Dspy, these skills enhance your workflow:
- **langgraph**: LangGraph for multi-agent orchestration (use with DSPy-optimized prompts)
- **test-driven-development**: Testing DSPy modules and prompt optimizations
- **systematic-debugging**: Debugging DSPy compilation and optimization failures

[Full documentation available in these skills if deployed in your bundle]
