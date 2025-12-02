---
name: session-compression
description: AI session compression techniques for managing multi-turn conversations efficiently through summarization, embedding-based retrieval, and intelligent context management.
progressive_disclosure:
  entry_point:
    - summary
    - when_to_use
    - quick_start
  full_content:
    - all
---

# AI Session Compression Techniques

## Summary

**Compress long AI conversations to fit context windows while preserving critical information.**

Session compression enables production AI applications to manage multi-turn conversations efficiently by reducing token usage by 70-95% through summarization, embedding-based retrieval, and intelligent context management. Achieve 3-20x compression ratios with minimal performance degradation.

**Key Benefits:**
- **Cost Reduction:** 80-90% token cost savings through hierarchical memory
- **Performance:** 2x faster responses with compressed context
- **Scalability:** Handle conversations exceeding 1M tokens
- **Quality:** Preserve critical information with <2% accuracy loss

## When to Use

**Use session compression when:**
- Multi-turn conversations approach context window limits (>50% capacity)
- Long-running chat sessions (customer support, tutoring, code assistants)
- Token costs become significant (high-volume applications)
- Response latency increases due to large context
- Managing conversation history across multiple sessions

**Don't use when:**
- Short conversations (<10 turns) fitting easily in context
- Every detail must be preserved verbatim (legal, compliance)
- Single-turn or stateless interactions
- Context window usage is <30%

**Ideal scenarios:**
- Chatbots with 50+ turn conversations
- AI code assistants tracking long development sessions
- Customer support with multi-session ticket history
- Educational tutors with student progress tracking
- Multi-day collaborative AI workflows

## Quick Start

### Basic Setup with LangChain

```python
from langchain.memory import ConversationSummaryBufferMemory
from langchain_anthropic import ChatAnthropic
from anthropic import Anthropic

# Initialize Claude client
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    api_key="your-api-key"
)

# Setup memory with automatic summarization
memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=2000,  # Summarize when exceeding this
    return_messages=True
)

# Add conversation turns
memory.save_context(
    {"input": "What's session compression?"},
    {"output": "Session compression reduces conversation token usage..."}
)

# Retrieve compressed context
context = memory.load_memory_variables({})
```

### Progressive Compression Pattern

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

class ProgressiveCompressor:
    def __init__(self, thresholds=[0.70, 0.85, 0.95]):
        self.thresholds = thresholds
        self.messages = []
        self.max_tokens = 200000  # Claude context window

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

        # Check if compression needed
        current_usage = self._estimate_tokens()
        usage_ratio = current_usage / self.max_tokens

        if usage_ratio >= self.thresholds[0]:
            self._compress(level=self._get_compression_level(usage_ratio))

    def _estimate_tokens(self):
        return sum(len(m["content"]) // 4 for m in self.messages)

    def _get_compression_level(self, ratio):
        for i, threshold in enumerate(self.thresholds):
            if ratio < threshold:
                return i
        return len(self.thresholds)

    def _compress(self, level: int):
        """Apply compression based on severity level."""
        if level == 1:  # 70% threshold: Light compression
            self._remove_redundant_messages()
        elif level == 2:  # 85% threshold: Medium compression
            self._summarize_old_messages(keep_recent=10)
        else:  # 95% threshold: Aggressive compression
            self._summarize_old_messages(keep_recent=5)

    def _remove_redundant_messages(self):
        """Remove duplicate or low-value messages."""
        # Implementation: Use semantic deduplication
        pass

    def _summarize_old_messages(self, keep_recent: int):
        """Summarize older messages, keep recent ones verbatim."""
        if len(self.messages) <= keep_recent:
            return

        # Messages to summarize
        to_summarize = self.messages[:-keep_recent]
        recent = self.messages[-keep_recent:]

        # Generate summary
        conversation_text = "\n\n".join([
            f"{m['role'].upper()}: {m['content']}"
            for m in to_summarize
        ])

        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": f"Summarize this conversation:\n\n{conversation_text}"
            }]
        )

        # Replace old messages with summary
        summary = {
            "role": "system",
            "content": f"[Summary]\n{response.content[0].text}"
        }
        self.messages = [summary] + recent

# Usage
compressor = ProgressiveCompressor()

for i in range(100):
    compressor.add_message("user", f"Message {i}")
    compressor.add_message("assistant", f"Response {i}")
```

### Using Anthropic Prompt Caching (90% Cost Reduction)

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

# Build context with cache control
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Long conversation context here...",
                "cache_control": {"type": "ephemeral"}  # Cache this
            }
        ]
    },
    {
        "role": "assistant",
        "content": "Previous response..."
    },
    {
        "role": "user",
        "content": "New question"  # Not cached, changes frequently
    }
]

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=messages
)

# Cache hit reduces costs by 90% for cached content
```

---

## Core Concepts

### Context Windows and Token Limits

**Context window:** Maximum tokens an LLM can process in a single request (input + output).

**Current limits (2025):**
- Claude 3.5 Sonnet: 200K tokens (~150K words, ~600 pages)
- GPT-4 Turbo: 128K tokens (~96K words, ~384 pages)
- Gemini 1.5 Pro: 2M tokens (~1.5M words, ~6000 pages)

**Token estimation:**
- English: ~4 characters per token
- Code: ~3 characters per token
- Rule of thumb: 1 token ≈ 0.75 words

**Why compression matters:**
- **Cost:** Claude Sonnet costs $3/$15 per 1M input/output tokens
- **Latency:** Larger contexts increase processing time
- **Quality:** Excessive context can dilute attention on relevant information

### Compression Ratios

**Compression ratio = Original tokens / Compressed tokens**

**Industry benchmarks:**
- Extractive summarization: 2-3x
- Abstractive summarization: 5-10x
- Hierarchical summarization: 20x+
- LLMLingua (prompt compression): 20x with 1.5% accuracy loss
- KVzip (KV cache compression): 3-4x with 2x speed improvement

**Target ratios by use case:**
- Customer support: 5-7x (preserve details)
- General chat: 8-12x (balance quality/efficiency)
- Code assistants: 3-5x (preserve technical accuracy)
- Long documents: 15-20x (extract key insights)

### Progressive Compression Thresholds

**Industry standard pattern:**

```
Context Usage    Action                     Technique
─────────────────────────────────────────────────────────
0-70%           No compression             Store verbatim
70-85%          Light compression          Remove redundancy
85-95%          Medium compression         Summarize old messages
95-100%         Aggressive compression     Hierarchical + RAG
```

**Implementation guidelines:**
- **70% threshold:** Remove duplicate/redundant messages, semantic deduplication
- **85% threshold:** Summarize messages older than 20 turns, keep recent 10-15
- **95% threshold:** Multi-level hierarchical summarization + vector store archival
- **Emergency (100%):** Drop least important messages, aggressive summarization

---

## Compression Techniques

### 1. Summarization Techniques

#### 1.1 Extractive Summarization

**Selects key sentences/phrases without modification.**

**Pros:** No hallucination, fast, deterministic
**Cons:** Limited compression (2-3x), may feel disjointed
**Best for:** Legal/compliance, short-term compression

```python
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def extractive_compress(messages: list, compression_ratio: float = 0.3):
    """Extract most important messages using TF-IDF scoring."""
    texts = [msg['content'] for msg in messages]

    # Calculate TF-IDF scores
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    scores = np.array(tfidf_matrix.sum(axis=1)).flatten()

    # Select top messages
    n_keep = max(1, int(len(messages) * compression_ratio))
    top_indices = sorted(np.argsort(scores)[-n_keep:])

    return [messages[i] for i in top_indices]
```

#### 1.2 Abstractive Summarization

**Uses LLMs to semantically condense conversation history.**

**Pros:** Higher compression (5-10x), coherent, synthesizes information
**Cons:** Risk of hallucination, higher cost, less deterministic
**Best for:** General chat, customer support, multi-session continuity

```python
from anthropic import Anthropic

def abstractive_compress(messages: list, client: Anthropic):
    """Generate semantic summary using Claude."""
    conversation_text = "\n\n".join([
        f"{msg['role'].upper()}: {msg['content']}"
        for msg in messages
    ])

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"""Summarize this conversation, preserving:
1. Key decisions made
2. Important context and facts
3. Unresolved questions
4. Action items

Conversation:
{conversation_text}

Summary (aim for 1/5 the original length):"""
        }]
    )

    return {
        "role": "assistant",
        "content": f"[Summary]\n{response.content[0].text}"
    }
```

#### 1.3 Hierarchical Summarization (Multi-Level)

**Creates summaries of summaries in a tree structure.**

**Pros:** Extreme compression (20x+), handles 1M+ token conversations
**Cons:** Complex implementation, multiple LLM calls, information loss accumulates
**Best for:** Long-running conversations, multi-session applications

**Architecture:**
```
Level 0 (Raw):    [Msg1][Msg2][Msg3][Msg4][Msg5][Msg6][Msg7][Msg8]
Level 1 (Chunk):  [Summary1-2]  [Summary3-4]  [Summary5-6]  [Summary7-8]
Level 2 (Group):  [Summary1-4]              [Summary5-8]
Level 3 (Session): [Overall Session Summary]
```

```python
from anthropic import Anthropic
from typing import List, Dict

class HierarchicalMemory:
    def __init__(self, client: Anthropic, chunk_size: int = 10):
        self.client = client
        self.chunk_size = chunk_size
        self.levels: List[List[Dict]] = [[]]  # Level 0 = raw messages

    def add_message(self, message: Dict):
        """Add message and trigger summarization if needed."""
        self.levels[0].append(message)

        if len(self.levels[0]) >= self.chunk_size * 2:
            self._summarize_level(0)

    def _summarize_level(self, level: int):
        """Summarize a level into the next higher level."""
        messages = self.levels[level]

        # Ensure next level exists
        while len(self.levels) <= level + 1:
            self.levels.append([])

        # Summarize first chunk
        chunk = messages[:self.chunk_size]
        summary = self._generate_summary(chunk, level)

        # Move to next level
        self.levels[level + 1].append(summary)
        self.levels[level] = messages[self.chunk_size:]

        # Recursively check if next level needs summarization
        if len(self.levels[level + 1]) >= self.chunk_size * 2:
            self._summarize_level(level + 1)

    def _generate_summary(self, messages: List[Dict], level: int) -> Dict:
        """Generate summary for a chunk."""
        conversation_text = "\n\n".join([
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in messages
        ])

        response = self.client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=300,
            messages=[{
                "role": "user",
                "content": f"Summarize this Level {level} conversation chunk:\n\n{conversation_text}"
            }]
        )

        return {
            "role": "system",
            "content": f"[L{level+1} Summary] {response.content[0].text}",
            "level": level + 1
        }

    def get_context(self, max_tokens: int = 4000) -> List[Dict]:
        """Retrieve context within token budget."""
        context = []
        token_count = 0

        # Prioritize recent raw messages
        for msg in reversed(self.levels[0]):
            msg_tokens = len(msg['content']) // 4
            if token_count + msg_tokens > max_tokens * 0.6:
                break
            context.insert(0, msg)
            token_count += msg_tokens

        # Add summaries from higher levels
        for level in range(1, len(self.levels)):
            for summary in self.levels[level]:
                summary_tokens = len(summary['content']) // 4
                if token_count + summary_tokens > max_tokens:
                    break
                context.insert(0, summary)
                token_count += summary_tokens

        return context
```

**Academic reference:** "Recursively Summarizing Enables Long-Term Dialogue Memory in Large Language Models" (arXiv:2308.15022)

#### 1.4 Rolling Summarization (Continuous)

**Continuously compresses conversation with sliding window.**

**Pros:** Low latency, predictable token usage, simple
**Cons:** Early details over-compressed, no information recovery
**Best for:** Real-time chat, streaming conversations

```python
from anthropic import Anthropic

class RollingMemory:
    def __init__(self, client: Anthropic, window_size: int = 10, compress_threshold: int = 15):
        self.client = client
        self.window_size = window_size
        self.compress_threshold = compress_threshold
        self.rolling_summary = None
        self.recent_messages = []

    def add_message(self, message: dict):
        self.recent_messages.append(message)

        if len(self.recent_messages) >= self.compress_threshold:
            self._compress()

    def _compress(self):
        """Compress older messages into rolling summary."""
        messages_to_compress = self.recent_messages[:-self.window_size]

        parts = []
        if self.rolling_summary:
            parts.append(f"Existing summary:\n{self.rolling_summary}")

        parts.append("\nNew messages:\n" + "\n\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in messages_to_compress
        ]))

        response = self.client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=400,
            messages=[{
                "role": "user",
                "content": "\n".join(parts) + "\n\nUpdate the summary:"
            }]
        )

        self.rolling_summary = response.content[0].text
        self.recent_messages = self.recent_messages[-self.window_size:]

    def get_context(self):
        context = []
        if self.rolling_summary:
            context.append({
                "role": "system",
                "content": f"[Summary]\n{self.rolling_summary}"
            })
        context.extend(self.recent_messages)
        return context
```

### 2. Embedding-Based Approaches

#### 2.1 RAG (Retrieval-Augmented Generation)

**Store full conversation in vector database, retrieve only relevant chunks.**

**Pros:** Extremely scalable, no information loss, high relevance
**Cons:** Requires vector DB infrastructure, retrieval latency
**Best for:** Knowledge bases, customer support with large history

```python
from anthropic import Anthropic
from openai import OpenAI
import chromadb

class RAGMemory:
    def __init__(self, anthropic_client: Anthropic, openai_client: OpenAI):
        self.anthropic = anthropic_client
        self.openai = openai_client

        # Initialize vector store
        self.chroma = chromadb.Client()
        self.collection = self.chroma.create_collection(
            name="conversation",
            metadata={"hnsw:space": "cosine"}
        )

        self.recent_messages = []
        self.recent_window = 5
        self.message_counter = 0

    def add_message(self, message: dict):
        """Add to recent memory and vector store."""
        self.recent_messages.append(message)

        if len(self.recent_messages) > self.recent_window:
            old_msg = self.recent_messages.pop(0)
            self._store_in_vectordb(old_msg)

    def _store_in_vectordb(self, message: dict):
        """Archive to vector database."""
        # Generate embedding
        response = self.openai.embeddings.create(
            model="text-embedding-3-small",
            input=message['content']
        )

        self.collection.add(
            embeddings=[response.data[0].embedding],
            documents=[message['content']],
            metadatas=[{"role": message['role']}],
            ids=[f"msg_{self.message_counter}"]
        )
        self.message_counter += 1

    def retrieve_context(self, query: str, max_tokens: int = 4000):
        """Retrieve relevant context using RAG."""
        context = []
        token_count = 0

        # 1. Recent messages (short-term memory)
        for msg in self.recent_messages:
            context.append(msg)
            token_count += len(msg['content']) // 4

        # 2. Retrieve relevant historical context
        if token_count < max_tokens:
            query_embedding = self.openai.embeddings.create(
                model="text-embedding-3-small",
                input=query
            )

            n_results = min(10, (max_tokens - token_count) // 100)
            results = self.collection.query(
                query_embeddings=[query_embedding.data[0].embedding],
                n_results=n_results
            )

            for i, doc in enumerate(results['documents'][0]):
                if token_count + len(doc) // 4 > max_tokens:
                    break

                metadata = results['metadatas'][0][i]
                context.insert(0, {
                    "role": metadata['role'],
                    "content": f"[Retrieved] {doc}"
                })
                token_count += len(doc) // 4

        return context
```

**Vector database options:**
- **ChromaDB:** Embedded, easy local development
- **Pinecone:** Managed, 50ms p95 latency
- **Weaviate:** Open-source, hybrid search
- **Qdrant:** High performance, payload filtering

#### 2.2 Vector Search and Clustering

**Group similar messages into clusters, represent with centroids.**

**Pros:** Reduces redundancy, identifies themes, multi-topic handling
**Cons:** Requires sufficient data, may lose nuances
**Best for:** Multi-topic conversations, meeting summaries

```python
from sklearn.cluster import KMeans
from openai import OpenAI
import numpy as np

class ClusteredMemory:
    def __init__(self, openai_client: OpenAI, n_clusters: int = 5):
        self.client = openai_client
        self.n_clusters = n_clusters
        self.messages = []
        self.embeddings = []

    def add_messages(self, messages: list):
        for msg in messages:
            self.messages.append(msg)

            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=msg['content']
            )
            self.embeddings.append(response.data[0].embedding)

    def compress_by_clustering(self):
        """Cluster messages and return representatives."""
        if len(self.messages) < self.n_clusters:
            return self.messages

        embeddings_array = np.array(self.embeddings)
        kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)
        labels = kmeans.fit_predict(embeddings_array)

        # Select message closest to each centroid
        compressed = []
        for cluster_id in range(self.n_clusters):
            cluster_indices = np.where(labels == cluster_id)[0]
            centroid = kmeans.cluster_centers_[cluster_id]
            cluster_embeddings = embeddings_array[cluster_indices]
            distances = np.linalg.norm(cluster_embeddings - centroid, axis=1)
            closest_idx = cluster_indices[np.argmin(distances)]

            compressed.append({
                **self.messages[closest_idx],
                "cluster_id": int(cluster_id),
                "cluster_size": len(cluster_indices)
            })

        return compressed
```

#### 2.3 Semantic Deduplication

**Remove semantically similar messages that convey redundant information.**

**Pros:** Reduces redundancy without losing unique content
**Cons:** Requires threshold tuning, O(n²) complexity
**Best for:** FAQ systems, repetitive conversations

```python
from openai import OpenAI
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class SemanticDeduplicator:
    def __init__(self, openai_client: OpenAI, similarity_threshold: float = 0.85):
        self.client = openai_client
        self.threshold = similarity_threshold

    def deduplicate(self, messages: list):
        """Remove semantically similar messages."""
        if len(messages) <= 1:
            return messages

        # Generate embeddings
        embeddings = []
        for msg in messages:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=msg['content']
            )
            embeddings.append(response.data[0].embedding)

        embeddings_array = np.array(embeddings)
        similarity_matrix = cosine_similarity(embeddings_array)

        # Mark unique messages
        keep_indices = []
        for i in range(len(messages)):
            is_unique = True
            for j in keep_indices:
                if similarity_matrix[i][j] > self.threshold:
                    is_unique = False
                    break

            if is_unique:
                keep_indices.append(i)

        return [messages[i] for i in keep_indices]
```

### 3. Token-Efficient Strategies

#### 3.1 Message Prioritization

**Assign importance scores and retain only high-priority content.**

**Pros:** Retains most important information, flexible criteria
**Cons:** Scoring is heuristic-based, may break flow
**Best for:** Mixed-importance conversations, filtering noise

```python
import re

class MessagePrioritizer:
    def score_message(self, msg: dict, index: int, total: int) -> float:
        """Calculate composite importance score."""
        scores = []

        # Length score (longer = more info)
        scores.append(min(len(msg['content']) / 500, 1.0))

        # Question score
        if msg['role'] == 'user':
            scores.append(min(msg['content'].count('?') * 0.5, 1.0))

        # Entity score (capitalized words)
        entities = len(re.findall(r'\b[A-Z][a-z]+', msg['content']))
        scores.append(min(entities / 10, 1.0))

        # Recency score (linear decay)
        scores.append(index / max(total - 1, 1))

        # Role score
        scores.append(0.6 if msg['role'] == 'user' else 0.4)

        return sum(scores) / len(scores)

    def prioritize(self, messages: list, target_count: int):
        """Select top N messages by priority."""
        scored = [
            (msg, self.score_message(msg, i, len(messages)), i)
            for i, msg in enumerate(messages)
        ]

        scored.sort(key=lambda x: x[1], reverse=True)
        top_messages = scored[:target_count]
        top_messages.sort(key=lambda x: x[2])  # Restore chronological order

        return [msg for msg, score, idx in top_messages]
```

#### 3.2 Delta Compression

**Store only changes between consecutive messages.**

**Pros:** Highly efficient for incremental changes
**Cons:** Reconstruction overhead, not suitable for all content
**Best for:** Code assistants with incremental edits

```python
import difflib

class DeltaCompressor:
    def __init__(self):
        self.base_messages = []
        self.deltas = []

    def add_message(self, message: dict):
        if not self.base_messages:
            self.base_messages.append(message)
            return

        # Find most similar previous message
        last_msg = self.base_messages[-1]

        if last_msg['role'] == message['role']:
            # Calculate delta
            diff = list(difflib.unified_diff(
                last_msg['content'].splitlines(),
                message['content'].splitlines(),
                lineterm=''
            ))

            if len('\n'.join(diff)) < len(message['content']) * 0.7:
                # Store as delta if compression achieved
                self.deltas.append({
                    'base_index': len(self.base_messages) - 1,
                    'delta': diff,
                    'role': message['role']
                })
                return

        # Store as new base message
        self.base_messages.append(message)

    def reconstruct(self):
        """Reconstruct full conversation from bases + deltas."""
        messages = self.base_messages.copy()

        for delta_info in self.deltas:
            base_content = messages[delta_info['base_index']]['content']
            # Apply diff to reconstruct (simplified)
            reconstructed = base_content  # Full implementation would apply diff
            messages.append({
                'role': delta_info['role'],
                'content': reconstructed
            })

        return messages
```

### 4. LangChain Memory Types

#### 4.1 ConversationSummaryMemory

**Automatically summarizes conversation as it progresses.**

```python
from langchain.memory import ConversationSummaryMemory
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")

memory = ConversationSummaryMemory(llm=llm)

# Add conversation
memory.save_context(
    {"input": "Hi, I'm working on a Python project"},
    {"output": "Great! How can I help with your Python project?"}
)

# Get summary
summary = memory.load_memory_variables({})
print(summary['history'])
```

**Pros:** Automatic summarization, simple API
**Cons:** Every turn triggers LLM call
**Best for:** Medium conversations (20-50 turns)

#### 4.2 ConversationSummaryBufferMemory

**Hybrid: Recent messages verbatim, older summarized.**

```python
from langchain.memory import ConversationSummaryBufferMemory
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-3-5-haiku-20241022")

memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=2000,  # Summarize when exceeding
    return_messages=True
)

# Add conversation
for i in range(50):
    memory.save_context(
        {"input": f"Question {i}"},
        {"output": f"Answer {i}"}
    )

# Automatically keeps recent messages + summary of old
context = memory.load_memory_variables({})
```

**Pros:** Best balance of detail and compression
**Cons:** Requires token limit tuning
**Best for:** Most production applications

#### 4.3 ConversationTokenBufferMemory

**Maintains fixed token budget, drops oldest when exceeded.**

```python
from langchain.memory import ConversationTokenBufferMemory
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")

memory = ConversationTokenBufferMemory(
    llm=llm,
    max_token_limit=2000
)

# Simple FIFO when token limit exceeded
```

**Pros:** Predictable token usage, simple
**Cons:** Loses old information completely
**Best for:** Real-time chat with strict limits

#### 4.4 VectorStoreRetrieverMemory

**Stores all messages in vector database, retrieves relevant ones.**

```python
from langchain.memory import VectorStoreRetrieverMemory
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
vectorstore = Chroma(embedding_function=embeddings)

memory = VectorStoreRetrieverMemory(
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5})
)

# Automatically retrieves most relevant context
```

**Pros:** Infinite conversation length, semantic retrieval
**Cons:** Requires vector DB, retrieval overhead
**Best for:** Long-running conversations, knowledge bases

### 5. Anthropic-Specific Patterns

#### 5.1 Prompt Caching (90% Cost Reduction)

**Cache static context to reduce token costs.**

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

# Long conversation context
conversation_history = [
    {"role": "user", "content": "Message 1"},
    {"role": "assistant", "content": "Response 1"},
    # ... many more messages
]

# Mark context for caching
messages = []
for i, msg in enumerate(conversation_history[:-1]):
    content = msg['content']

    # Add cache control to last context message
    if i == len(conversation_history) - 2:
        messages.append({
            "role": msg['role'],
            "content": [
                {
                    "type": "text",
                    "text": content,
                    "cache_control": {"type": "ephemeral"}
                }
            ]
        })
    else:
        messages.append(msg)

# Add new user message (not cached)
messages.append(conversation_history[-1])

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=messages
)

# Subsequent calls with same cached context cost 90% less
```

**Cache TTL:** 5 minutes
**Savings:** 90% cost reduction for cached tokens
**Limits:** Max 4 cache breakpoints per request
**Best practices:**
- Cache conversation history, not current query
- Update cache when context changes significantly
- Combine with summarization for maximum efficiency

#### 5.2 Extended Thinking for Compression Planning

**Use extended thinking to plan optimal compression strategy.**

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

response = client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000
    },
    messages=[{
        "role": "user",
        "content": f"""Analyze this conversation and recommend compression:

{conversation_text}

Current token count: {current_tokens}
Target: {target_tokens}
Required compression: {compression_ratio}x

Recommend optimal strategy."""
    }]
)

# Access thinking process
thinking_content = [
    block for block in response.content
    if block.type == "thinking"
]

# Get compression recommendation
recommendation = response.content[-1].text
```

---

## Production Patterns

### Checkpointing and Persistence

**Save compression state for recovery and resume.**

```python
import json
import pickle
from pathlib import Path

class PersistentMemory:
    def __init__(self, checkpoint_dir: str = "./checkpoints"):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(exist_ok=True)
        self.memory = []
        self.summary = None

    def save_checkpoint(self, session_id: str):
        """Save current memory state."""
        checkpoint = {
            'messages': self.memory,
            'summary': self.summary,
            'timestamp': time.time()
        }

        checkpoint_file = self.checkpoint_dir / f"{session_id}.json"
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint, f, indent=2)

    def load_checkpoint(self, session_id: str):
        """Load memory state from checkpoint."""
        checkpoint_file = self.checkpoint_dir / f"{session_id}.json"

        if checkpoint_file.exists():
            with open(checkpoint_file, 'r') as f:
                checkpoint = json.load(f)

            self.memory = checkpoint['messages']
            self.summary = checkpoint.get('summary')
            return True

        return False

    def auto_checkpoint(self, session_id: str, interval: int = 10):
        """Automatically save every N messages."""
        if len(self.memory) % interval == 0:
            self.save_checkpoint(session_id)
```

### Resume Workflows

**Continue conversations across sessions.**

```python
from anthropic import Anthropic
import json

class ResumableConversation:
    def __init__(self, client: Anthropic, session_id: str):
        self.client = client
        self.session_id = session_id
        self.memory = self._load_or_create()

    def _load_or_create(self):
        """Load existing session or create new."""
        try:
            with open(f'sessions/{self.session_id}.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'messages': [],
                'summary': None,
                'created_at': time.time()
            }

    def add_turn(self, user_message: str):
        """Add user message and get response."""
        # Add user message
        self.memory['messages'].append({
            'role': 'user',
            'content': user_message
        })

        # Build context (with compression)
        context = self._build_context()

        # Get response
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=context + [{
                'role': 'user',
                'content': user_message
            }]
        )

        # Save response
        assistant_message = response.content[0].text
        self.memory['messages'].append({
            'role': 'assistant',
            'content': assistant_message
        })

        # Compress if needed
        if len(self.memory['messages']) > 20:
            self._compress()

        # Save state
        self._save()

        return assistant_message

    def _build_context(self):
        """Build context with compression."""
        context = []

        # Add summary if exists
        if self.memory['summary']:
            context.append({
                'role': 'system',
                'content': f"[Previous conversation summary]\n{self.memory['summary']}"
            })

        # Add recent messages
        context.extend(self.memory['messages'][-10:])

        return context

    def _compress(self):
        """Compress older messages."""
        if len(self.memory['messages']) < 15:
            return

        # Messages to summarize
        to_summarize = self.memory['messages'][:-10]

        # Generate summary
        conversation_text = "\n\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in to_summarize
        ])

        response = self.client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=500,
            messages=[{
                'role': 'user',
                'content': f"Summarize this conversation:\n\n{conversation_text}"
            }]
        )

        # Update memory
        self.memory['summary'] = response.content[0].text
        self.memory['messages'] = self.memory['messages'][-10:]

    def _save(self):
        """Save session to disk."""
        with open(f'sessions/{self.session_id}.json', 'w') as f:
            json.dump(self.memory, f, indent=2)

# Usage
client = Anthropic(api_key="your-api-key")
conversation = ResumableConversation(client, session_id="user123_session1")

# Continue across multiple sessions
response1 = conversation.add_turn("What's Python?")
# ... later session
response2 = conversation.add_turn("Show me an example")  # Remembers context
```

### Hybrid Approaches (Best Practice)

**Combine multiple techniques for optimal results.**

```python
from anthropic import Anthropic
from openai import OpenAI
import chromadb

class HybridMemorySystem:
    """
    Combines:
    - Rolling summarization (short-term compression)
    - RAG retrieval (long-term memory)
    - Prompt caching (cost optimization)
    - Progressive compression (adaptive behavior)
    """

    def __init__(self, anthropic_client: Anthropic, openai_client: OpenAI):
        self.anthropic = anthropic_client
        self.openai = openai_client

        # Recent messages (verbatim)
        self.recent_messages = []
        self.recent_window = 10

        # Rolling summary
        self.rolling_summary = None

        # Vector store (long-term)
        self.chroma = chromadb.Client()
        self.collection = self.chroma.create_collection(name="memory")
        self.message_counter = 0

        # Compression thresholds
        self.thresholds = {
            'light': 0.70,    # Start basic compression
            'medium': 0.85,   # Aggressive summarization
            'heavy': 0.95     # Emergency measures
        }

    def add_message(self, message: dict):
        """Add message with intelligent compression."""
        self.recent_messages.append(message)

        # Check compression needs
        usage_ratio = self._estimate_usage()

        if usage_ratio >= self.thresholds['heavy']:
            self._emergency_compress()
        elif usage_ratio >= self.thresholds['medium']:
            self._medium_compress()
        elif usage_ratio >= self.thresholds['light']:
            self._light_compress()

    def _light_compress(self):
        """Remove redundancy, archive to vector store."""
        if len(self.recent_messages) > self.recent_window * 1.5:
            # Archive oldest to vector store
            to_archive = self.recent_messages[:5]
            for msg in to_archive:
                self._archive_to_vectorstore(msg)

            self.recent_messages = self.recent_messages[5:]

    def _medium_compress(self):
        """Generate rolling summary, aggressive archival."""
        if len(self.recent_messages) > self.recent_window:
            # Summarize older messages
            to_summarize = self.recent_messages[:-self.recent_window]

            summary_text = "\n\n".join([
                f"{msg['role']}: {msg['content']}"
                for msg in to_summarize
            ])

            if self.rolling_summary:
                summary_text = f"Existing: {self.rolling_summary}\n\nNew: {summary_text}"

            response = self.anthropic.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=400,
                messages=[{
                    'role': 'user',
                    'content': f"Update summary:\n{summary_text}"
                }]
            )

            self.rolling_summary = response.content[0].text

            # Archive all summarized messages
            for msg in to_summarize:
                self._archive_to_vectorstore(msg)

            self.recent_messages = self.recent_messages[-self.recent_window:]

    def _emergency_compress(self):
        """Extreme compression for near-limit situations."""
        # Keep only 5 most recent messages
        to_archive = self.recent_messages[:-5]
        for msg in to_archive:
            self._archive_to_vectorstore(msg)

        self.recent_messages = self.recent_messages[-5:]

        # Compress summary further if needed
        if self.rolling_summary and len(self.rolling_summary) > 1000:
            response = self.anthropic.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=200,
                messages=[{
                    'role': 'user',
                    'content': f"Create ultra-concise summary:\n{self.rolling_summary}"
                }]
            )
            self.rolling_summary = response.content[0].text

    def _archive_to_vectorstore(self, message: dict):
        """Store in vector database for retrieval."""
        embedding_response = self.openai.embeddings.create(
            model="text-embedding-3-small",
            input=message['content']
        )

        self.collection.add(
            embeddings=[embedding_response.data[0].embedding],
            documents=[message['content']],
            metadatas=[{'role': message['role']}],
            ids=[f"msg_{self.message_counter}"]
        )
        self.message_counter += 1

    def get_context(self, current_query: str, max_tokens: int = 8000):
        """Build optimal context for current query."""
        context = []
        token_count = 0

        # 1. Add rolling summary (if exists)
        if self.rolling_summary:
            summary_msg = {
                'role': 'system',
                'content': [
                    {
                        'type': 'text',
                        'text': f"[Conversation Summary]\n{self.rolling_summary}",
                        'cache_control': {'type': 'ephemeral'}  # Cache it
                    }
                ]
            }
            context.append(summary_msg)
            token_count += len(self.rolling_summary) // 4

        # 2. Retrieve relevant historical context (RAG)
        if token_count < max_tokens * 0.3:
            query_embedding = self.openai.embeddings.create(
                model="text-embedding-3-small",
                input=current_query
            )

            results = self.collection.query(
                query_embeddings=[query_embedding.data[0].embedding],
                n_results=5
            )

            for i, doc in enumerate(results['documents'][0]):
                if token_count + len(doc) // 4 > max_tokens * 0.3:
                    break

                metadata = results['metadatas'][0][i]
                context.append({
                    'role': metadata['role'],
                    'content': f"[Retrieved] {doc}"
                })
                token_count += len(doc) // 4

        # 3. Add recent messages verbatim
        for msg in self.recent_messages:
            if token_count + len(msg['content']) // 4 > max_tokens * 0.8:
                break
            context.append(msg)
            token_count += len(msg['content']) // 4

        return context

    def _estimate_usage(self):
        """Estimate current context window usage."""
        total_tokens = 0

        if self.rolling_summary:
            total_tokens += len(self.rolling_summary) // 4

        for msg in self.recent_messages:
            total_tokens += len(msg['content']) // 4

        return total_tokens / 200000  # Claude Sonnet context window

# Usage
anthropic_client = Anthropic(api_key="your-anthropic-key")
openai_client = OpenAI(api_key="your-openai-key")

memory = HybridMemorySystem(anthropic_client, openai_client)

# Add messages over time
for i in range(1000):
    memory.add_message({
        'role': 'user' if i % 2 == 0 else 'assistant',
        'content': f"Message {i} with some content..."
    })

# Retrieve optimized context
current_query = "What did we discuss about pricing?"
context = memory.get_context(current_query)

# Use with Claude
response = anthropic_client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=context + [{
        'role': 'user',
        'content': current_query
    }]
)
```

---

## Performance Benchmarks

### Compression Efficiency

| Technique | Compression Ratio | Quality Loss | Latency | Cost Impact |
|-----------|------------------|--------------|---------|-------------|
| Extractive | 2-3x | <1% | <10ms | None |
| Abstractive | 5-10x | 2-5% | 1-2s | +$0.001/turn |
| Hierarchical | 20x+ | 5-8% | 2-5s | +$0.003/turn |
| LLMLingua | 20x | 1.5% | 500ms | None |
| RAG | Variable | <1% | 100-300ms | +$0.0005/turn |
| Prompt Caching | N/A | 0% | 0ms | -90% |

### Token Savings by Use Case

**Customer Support (50-turn conversation):**
- No compression: ~8,000 tokens/request
- Rolling summary: ~2,000 tokens/request (75% reduction)
- Hybrid (RAG + summary): ~1,500 tokens/request (81% reduction)

**Code Assistant (100-turn session):**
- No compression: ~25,000 tokens/request
- Hierarchical: ~5,000 tokens/request (80% reduction)
- Hybrid + caching: ~1,000 tokens/request effective (96% cost reduction)

**Educational Tutor (multi-session):**
- No compression: Would exceed context window
- RAG + summarization: ~3,000 tokens/request
- Infinite session length enabled

### Cost Analysis

**Example: Claude Sonnet pricing ($3 input, $15 output per 1M tokens)**

**1,000 conversations, 50 turns each:**
- **No compression:**
  - Avg 8K tokens/request × 50K requests = 400M tokens
  - Cost: $1,200

- **With rolling summarization:**
  - Avg 2K tokens/request × 50K requests = 100M tokens
  - Summarization overhead: +10M tokens
  - Cost: $330 (72% savings)

- **With hybrid system + caching:**
  - First turn: 2K tokens (no cache)
  - Subsequent: 200 tokens effective (90% cache hit)
  - Total: ~15M tokens effective
  - Cost: $45 (96% savings)

---

## Tool Recommendations

### Memory Management Tools

#### Mem0 (Recommended for Production)

**Best for:** Hybrid memory systems with minimal code

```python
from mem0 import MemoryClient

client = MemoryClient(api_key="your-mem0-key")

# Automatically handles compression, summarization, RAG
memory = client.create_memory(
    user_id="user123",
    messages=[
        {"role": "user", "content": "I'm working on a Python project"},
        {"role": "assistant", "content": "Great! What kind of project?"}
    ]
)

# Retrieve relevant context
context = client.get_memory(
    user_id="user123",
    query="What programming language am I using?"
)
```

**Features:**
- Automatic hierarchical summarization
- Built-in RAG retrieval
- Multi-user session management
- Analytics dashboard

**Pricing:** $0.40/1K memory operations

#### Zep

**Best for:** Low-latency production deployments**

```python
from zep_python import ZepClient

client = ZepClient(api_key="your-zep-key")

# Add to session
client.memory.add_memory(
    session_id="session123",
    messages=[
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ]
)

# Auto-summarized retrieval
memory = client.memory.get_memory(session_id="session123")
```

**Features:**
- <100ms retrieval latency
- Automatic fact extraction
- Entity recognition
- Session management

**Pricing:** Open-source (self-hosted) or $0.50/1K operations (cloud)

#### ChromaDB

**Best for:** Self-hosted vector storage**

```python
import chromadb

client = chromadb.Client()
collection = client.create_collection("conversations")

# Store embeddings
collection.add(
    documents=["Message content"],
    embeddings=[[0.1, 0.2, ...]],
    ids=["msg1"]
)

# Retrieve
results = collection.query(
    query_embeddings=[[0.1, 0.2, ...]],
    n_results=5
)
```

**Features:**
- Fully open-source
- Embedded or client-server
- Fast local development

**Pricing:** Free (self-hosted)

#### LangChain

**Best for:** Rapid prototyping and experimentation**

```python
from langchain.memory import ConversationSummaryBufferMemory
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=2000)
```

**Features:**
- Multiple memory types
- Framework integration
- Extensive documentation

**Pricing:** Free (uses your LLM API costs)

### Compression Libraries

#### LLMLingua

**Best for:** Extreme compression with minimal quality loss**

```python
from llmlingua import PromptCompressor

compressor = PromptCompressor()

compressed = compressor.compress_prompt(
    context="Long conversation history...",
    instruction="Current user query",
    target_token=500
)

# Achieves 20x compression with 1.5% accuracy loss
```

**Features:**
- 20x compression ratios
- <2% quality degradation
- Fast inference (<500ms)

**Pricing:** Free (open-source)

---

## Use Cases and Patterns

### Chatbot (Customer Support)

**Requirements:**
- Multi-turn conversations (50-100 turns)
- Preserve customer context
- Fast response times
- Cost-efficient

**Recommended approach:**
- ConversationSummaryBufferMemory (LangChain)
- 70% threshold: Semantic deduplication
- 85% threshold: Rolling summarization
- Prompt caching for frequent patterns

**Implementation:**

```python
from langchain.memory import ConversationSummaryBufferMemory
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-3-5-haiku-20241022")

memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=2000,
    return_messages=True
)

# Add customer conversation
for turn in customer_conversation:
    memory.save_context(
        {"input": turn['customer_message']},
        {"output": turn['agent_response']}
    )

# Retrieve compressed context
context = memory.load_memory_variables({})
```

### Code Assistant

**Requirements:**
- Long development sessions (100+ turns)
- Preserve technical details
- Handle large code blocks
- Track incremental changes

**Recommended approach:**
- Hierarchical summarization for overall context
- RAG retrieval for specific code references
- Delta compression for iterative edits
- Prompt caching for system prompts

**Implementation:**

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

class CodeAssistantMemory:
    def __init__(self):
        self.hierarchy = HierarchicalMemory(client, chunk_size=15)
        self.rag = RAGMemory(anthropic_client=client, openai_client=openai_client)
        self.deltas = DeltaCompressor()

    def add_interaction(self, code_change: dict):
        # Store in hierarchy
        self.hierarchy.add_message({
            'role': 'user',
            'content': code_change['description']
        })

        # Store in RAG for retrieval
        self.rag.add_message(code_change)

        # Store as delta if incremental
        if code_change.get('is_incremental'):
            self.deltas.add_message(code_change)

    def get_context(self, current_query: str):
        # Combine hierarchical summary + RAG retrieval
        summary_context = self.hierarchy.get_context(max_tokens=2000)
        rag_context = self.rag.retrieve_context(current_query, max_tokens=2000)

        return summary_context + rag_context
```

### Educational Tutor

**Requirements:**
- Multi-session tracking
- Student progress persistence
- Personalized context retrieval
- Long-term knowledge retention

**Recommended approach:**
- VectorStoreRetrieverMemory for multi-session
- Fact extraction for student knowledge
- Progressive compression across sessions
- Resumable conversations

**Implementation:**

```python
from langchain.memory import VectorStoreRetrieverMemory
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

class TutorMemory:
    def __init__(self, student_id: str):
        self.student_id = student_id

        # Vector store for all sessions
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma(
            collection_name=f"student_{student_id}",
            embedding_function=embeddings
        )

        self.memory = VectorStoreRetrieverMemory(
            retriever=vectorstore.as_retriever(search_kwargs={"k": 10})
        )

    def add_lesson_content(self, lesson: dict):
        """Add lesson interaction to student memory."""
        self.memory.save_context(
            {"input": lesson['topic']},
            {"output": lesson['explanation']}
        )

    def get_student_context(self, current_topic: str):
        """Retrieve relevant past lessons for current topic."""
        return self.memory.load_memory_variables({
            "prompt": current_topic
        })
```

---

## Best Practices

### 1. Choose the Right Technique for Your Use Case

- **Short conversations (<20 turns):** No compression needed
- **Medium conversations (20-50 turns):** ConversationSummaryBufferMemory
- **Long conversations (50-100 turns):** Hierarchical or rolling summarization
- **Very long (100+ turns):** Hybrid (RAG + summarization + caching)
- **Multi-session:** VectorStoreRetrieverMemory or Mem0

### 2. Implement Progressive Compression

Don't compress aggressively from the start. Use thresholds:
- 0-70%: Store verbatim
- 70-85%: Light compression (deduplication)
- 85-95%: Medium compression (summarization)
- 95-100%: Aggressive compression (hierarchical)

### 3. Combine Techniques

Single-technique approaches are suboptimal. Best production systems use:
- Rolling summarization (short-term)
- RAG retrieval (long-term)
- Prompt caching (cost optimization)
- Semantic deduplication (redundancy removal)

### 4. Monitor Quality Metrics

Track compression impact:
- Response relevance score
- Information retention rate
- User satisfaction metrics
- Token usage reduction

### 5. Use Prompt Caching Strategically

Cache stable content:
- Conversation summaries
- System prompts
- Knowledge base context
- User profiles

Don't cache frequently changing content:
- Current user query
- Real-time data
- Session-specific state

### 6. Implement Checkpointing

Save compression state for:
- Recovery from failures
- Multi-session continuity
- Analytics and debugging
- A/B testing different strategies

### 7. Tune Compression Parameters

Test and optimize:
- Summary token limits
- Compression thresholds
- Retrieval result counts
- Cache TTLs
- Chunk sizes for hierarchical

### 8. Handle Edge Cases

Plan for:
- Very long messages (split or compress individually)
- Code blocks (preserve formatting)
- Multi-language content
- Rapidly changing context

---

## Troubleshooting

### Problem: Summary loses critical information

**Solutions:**
- Lower compression ratio (less aggressive)
- Implement importance scoring to preserve key messages
- Use extractive summarization for critical sections
- Increase summary token budget

### Problem: Retrieval returns irrelevant context

**Solutions:**
- Improve embedding model quality
- Add metadata filtering (timestamps, topics)
- Adjust similarity threshold
- Use hybrid search (semantic + keyword)

### Problem: High latency from compression

**Solutions:**
- Compress asynchronously (background tasks)
- Use faster models for summarization (Haiku instead of Sonnet)
- Cache summaries more aggressively
- Reduce compression frequency

### Problem: Conversations still exceeding context window

**Solutions:**
- Implement hierarchical compression
- Archive to vector database more aggressively
- Use more aggressive compression ratios
- Consider switching to model with larger context window

### Problem: High costs despite compression

**Solutions:**
- Implement prompt caching
- Use cheaper models for summarization (Haiku)
- Batch summarization operations
- Reduce summarization frequency

### Problem: Lost conversation continuity

**Solutions:**
- Increase recent message window
- Include summary in every request
- Use more descriptive summaries
- Implement session resumption with context injection

---

## Advanced Topics

### Streaming Compression

**Compress in real-time as conversation progresses:**

```python
async def streaming_compress(messages: list):
    """Compress while streaming responses."""
    compressor = ProgressiveCompressor()

    async for message in conversation_stream:
        compressor.add_message(message)

        # Compression happens asynchronously
        if compressor.should_compress():
            asyncio.create_task(compressor.compress_async())

    return compressor.get_context()
```

### Multi-User Session Management

**Handle concurrent conversations with shared context:**

```python
class MultiUserMemory:
    def __init__(self):
        self.user_sessions = {}

    def get_or_create_session(self, user_id: str):
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = HybridMemorySystem(...)
        return self.user_sessions[user_id]

    def cleanup_inactive_sessions(self, timeout: int = 3600):
        """Remove sessions inactive for > timeout seconds."""
        current_time = time.time()
        inactive = [
            user_id for user_id, session in self.user_sessions.items()
            if current_time - session.last_activity > timeout
        ]

        for user_id in inactive:
            self._archive_session(user_id)
            del self.user_sessions[user_id]
```

### Custom Importance Scoring

**Train ML models to score message importance:**

```python
from transformers import pipeline

class MLImportanceScorer:
    def __init__(self):
        # Use pre-trained classifier or fine-tune on your data
        self.classifier = pipeline(
            "text-classification",
            model="your-importance-model"
        )

    def score(self, message: dict) -> float:
        """Score message importance (0-1)."""
        result = self.classifier(message['content'])
        return result[0]['score']
```

### Context Window Utilization Optimization

**Maximize information density within token budget:**

```python
def optimize_context_allocation(
    summary_tokens: int,
    recent_tokens: int,
    retrieval_tokens: int,
    max_tokens: int
):
    """
    Optimal allocation (empirically tested):
    - 20% summary
    - 50% recent messages
    - 30% retrieved context
    """
    return {
        'summary': int(max_tokens * 0.20),
        'recent': int(max_tokens * 0.50),
        'retrieval': int(max_tokens * 0.30)
    }
```

---

## Future Directions

### Emerging Techniques (2025+)

**1. Infinite Attention Mechanisms**
- Models with >10M token context windows (Gemini 1.5, future Claude)
- Reduces need for compression but doesn't eliminate cost concerns

**2. Learned Compression Models**
- Neural networks trained to compress conversation optimally
- Maintain semantic meaning while minimizing tokens
- Examples: LLMLingua v2, PromptCompressor

**3. Multimodal Session Compression**
- Compress conversations with images, audio, video
- Maintain cross-modal context relationships

**4. Federated Memory Systems**
- Distributed compression across multiple memory stores
- Privacy-preserving compression for sensitive conversations

**5. Adaptive Compression Strategies**
- RL-based systems that learn optimal compression per user/domain
- Dynamic threshold adjustment based on conversation importance

---

## References

### Academic Papers
- "Recursively Summarizing Enables Long-Term Dialogue Memory" (arXiv:2308.15022)
- "LLMLingua: Compressing Prompts for Accelerated Inference" (arXiv:2310.05736)
- "Lost in the Middle: How Language Models Use Long Contexts" (arXiv:2307.03172)

### Documentation
- [Anthropic Prompt Caching](https://docs.anthropic.com/claude/docs/prompt-caching)
- [LangChain Memory](https://python.langchain.com/docs/modules/memory/)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)

### Tools
- [Mem0](https://mem0.ai/) - Managed memory service
- [Zep](https://www.getzep.com/) - Fast memory layer
- [LLMLingua](https://github.com/microsoft/LLMLingua) - Prompt compression
- [ChromaDB](https://www.trychroma.com/) - Vector database

---

**Last Updated:** 2025-11-30
**Version:** 1.0.0
**License:** MIT
