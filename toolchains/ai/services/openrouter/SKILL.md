---
name: openrouter
description: OpenRouter unified AI API - Access 200+ LLMs through single interface with intelligent routing, streaming, cost optimization, and model fallbacks
version: 1.0.0
category: ai-service
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Unified AI gateway: 200+ models (GPT-4, Claude, Llama, Gemini), single API, intelligent routing, streaming, cost optimization"
    when_to_use: "Multi-model AI apps, cost-optimized inference, model fallbacks, A/B testing, production LLM deployments, avoiding vendor lock-in"
    quick_start: "1. Get API key at openrouter.ai 2. POST to /api/v1/chat/completions 3. Set model param 4. Handle streaming responses"
context_limit: 4200
tags:
  - ai
  - llm
  - api
  - openai-compatible
  - streaming
  - cost-optimization
  - multi-model
requires_tools: []
---

# OpenRouter - Unified AI API Gateway

## Overview

OpenRouter provides a single API to access 200+ language models from OpenAI, Anthropic, Google, Meta, Mistral, and more. It offers intelligent routing, streaming, cost optimization, and standardized OpenAI-compatible interface.

**Key Features**:
- Access 200+ models through one API
- OpenAI-compatible interface (drop-in replacement)
- Intelligent model routing and fallbacks
- Real-time streaming responses
- Cost tracking and optimization
- Model performance analytics
- Function calling support
- Vision model support

**Pricing Model**:
- Pay-per-token (no subscriptions)
- Volume discounts available
- Free tier with credits
- Per-model pricing varies

**Installation**:
```bash
npm install openai  # Use OpenAI SDK
# or
pip install openai  # Python
```

## Quick Start

### 1. Get API Key

```bash
# Sign up at https://openrouter.ai/keys
export OPENROUTER_API_KEY="sk-or-v1-..."
```

### 2. Basic Chat Completion

```typescript
import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: 'https://openrouter.ai/api/v1',
  apiKey: process.env.OPENROUTER_API_KEY,
  defaultHeaders: {
    'HTTP-Referer': 'https://your-app.com',  // Optional
    'X-Title': 'Your App Name',              // Optional
  }
});

async function chat() {
  const completion = await client.chat.completions.create({
    model: 'anthropic/claude-3.5-sonnet',
    messages: [
      { role: 'user', content: 'Explain quantum computing in simple terms' }
    ],
  });

  console.log(completion.choices[0].message.content);
}
```

### 3. Streaming Response

```typescript
async function streamChat() {
  const stream = await client.chat.completions.create({
    model: 'openai/gpt-4-turbo',
    messages: [
      { role: 'user', content: 'Write a short story about AI' }
    ],
    stream: true,
  });

  for await (const chunk of stream) {
    const content = chunk.choices[0]?.delta?.content || '';
    process.stdout.write(content);
  }
}
```

## Model Selection Strategy

### Available Model Categories

**Flagship Models** (Highest Quality):
```typescript
const flagshipModels = {
  claude: 'anthropic/claude-3.5-sonnet',      // Best reasoning
  gpt4: 'openai/gpt-4-turbo',                 // Best general purpose
  gemini: 'google/gemini-pro-1.5',            // Best long context
  opus: 'anthropic/claude-3-opus',            // Best complex tasks
};
```

**Fast Models** (Low Latency):
```typescript
const fastModels = {
  claude: 'anthropic/claude-3-haiku',         // Fastest Claude
  gpt35: 'openai/gpt-3.5-turbo',             // Fast GPT
  gemini: 'google/gemini-flash-1.5',         // Fast Gemini
  llama: 'meta-llama/llama-3.1-8b-instruct', // Fast open source
};
```

**Cost-Optimized Models**:
```typescript
const budgetModels = {
  haiku: 'anthropic/claude-3-haiku',          // $0.25/$1.25 per 1M tokens
  gemini: 'google/gemini-flash-1.5',         // $0.075/$0.30 per 1M tokens
  llama: 'meta-llama/llama-3.1-8b-instruct', // $0.06/$0.06 per 1M tokens
  mixtral: 'mistralai/mixtral-8x7b-instruct', // $0.24/$0.24 per 1M tokens
};
```

**Specialized Models**:
```typescript
const specializedModels = {
  vision: 'openai/gpt-4-vision-preview',     // Image understanding
  code: 'anthropic/claude-3.5-sonnet',       // Code generation
  longContext: 'google/gemini-pro-1.5',      // 2M token context
  function: 'openai/gpt-4-turbo',            // Function calling
};
```

### Model Selection Logic

```typescript
interface ModelSelector {
  task: 'chat' | 'code' | 'vision' | 'function' | 'summary';
  priority: 'quality' | 'speed' | 'cost';
  maxCost?: number;  // Max cost per 1M tokens
  contextSize?: number;
}

function selectModel(criteria: ModelSelector): string {
  if (criteria.task === 'vision') {
    return 'openai/gpt-4-vision-preview';
  }

  if (criteria.task === 'code') {
    return criteria.priority === 'quality'
      ? 'anthropic/claude-3.5-sonnet'
      : 'meta-llama/llama-3.1-70b-instruct';
  }

  if (criteria.contextSize && criteria.contextSize > 100000) {
    return 'google/gemini-pro-1.5';  // 2M context
  }

  // Default selection by priority
  switch (criteria.priority) {
    case 'quality':
      return 'anthropic/claude-3.5-sonnet';
    case 'speed':
      return 'anthropic/claude-3-haiku';
    case 'cost':
      return criteria.maxCost && criteria.maxCost < 0.5
        ? 'google/gemini-flash-1.5'
        : 'anthropic/claude-3-haiku';
    default:
      return 'openai/gpt-4-turbo';
  }
}

// Usage
const model = selectModel({
  task: 'code',
  priority: 'quality',
});
```

## Streaming Implementation

### TypeScript Streaming with Error Handling

```typescript
async function robustStreamingChat(
  prompt: string,
  model: string = 'anthropic/claude-3.5-sonnet'
) {
  try {
    const stream = await client.chat.completions.create({
      model,
      messages: [{ role: 'user', content: prompt }],
      stream: true,
      max_tokens: 4000,
    });

    let fullResponse = '';

    for await (const chunk of stream) {
      const delta = chunk.choices[0]?.delta;

      if (delta?.content) {
        fullResponse += delta.content;
        process.stdout.write(delta.content);
      }

      // Handle function calls
      if (delta?.function_call) {
        console.log('\nFunction call:', delta.function_call);
      }

      // Check for finish reason
      if (chunk.choices[0]?.finish_reason) {
        console.log(`\n[Finished: ${chunk.choices[0].finish_reason}]`);
      }
    }

    return fullResponse;
  } catch (error) {
    if (error instanceof Error) {
      console.error('Streaming error:', error.message);
    }
    throw error;
  }
}
```

### Python Streaming

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

def stream_chat(prompt: str, model: str = "anthropic/claude-3.5-sonnet"):
    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    full_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            full_response += content
            print(content, end="", flush=True)

    print()  # New line
    return full_response
```

### React Streaming Component

```typescript
import { useState } from 'react';

function StreamingChat() {
  const [response, setResponse] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);

  async function handleSubmit(prompt: string) {
    setIsStreaming(true);
    setResponse('');

    try {
      const res = await fetch('https://openrouter.ai/api/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${process.env.OPENROUTER_API_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: 'anthropic/claude-3.5-sonnet',
          messages: [{ role: 'user', content: prompt }],
          stream: true,
        }),
      });

      const reader = res.body?.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader!.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n').filter(line => line.trim());

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') continue;

            try {
              const parsed = JSON.parse(data);
              const content = parsed.choices[0]?.delta?.content || '';
              setResponse(prev => prev + content);
            } catch (e) {
              // Skip invalid JSON
            }
          }
        }
      }
    } catch (error) {
      console.error('Streaming error:', error);
    } finally {
      setIsStreaming(false);
    }
  }

  return (
    <div>
      <textarea
        value={response}
        readOnly
        rows={20}
        cols={80}
        placeholder="Response will appear here..."
      />
      <button onClick={() => handleSubmit('Explain AI')}>
        {isStreaming ? 'Streaming...' : 'Send'}
      </button>
    </div>
  );
}
```

## Function Calling

### Basic Function Calling

```typescript
const tools = [
  {
    type: 'function',
    function: {
      name: 'get_weather',
      description: 'Get current weather for a location',
      parameters: {
        type: 'object',
        properties: {
          location: {
            type: 'string',
            description: 'City name, e.g. San Francisco',
          },
          unit: {
            type: 'string',
            enum: ['celsius', 'fahrenheit'],
          },
        },
        required: ['location'],
      },
    },
  },
];

async function chatWithFunctions() {
  const completion = await client.chat.completions.create({
    model: 'openai/gpt-4-turbo',
    messages: [
      { role: 'user', content: 'What is the weather in Tokyo?' }
    ],
    tools,
    tool_choice: 'auto',
  });

  const message = completion.choices[0].message;

  if (message.tool_calls) {
    for (const toolCall of message.tool_calls) {
      console.log('Function:', toolCall.function.name);
      console.log('Arguments:', toolCall.function.arguments);

      // Execute function
      const args = JSON.parse(toolCall.function.arguments);
      const result = await getWeather(args.location, args.unit);

      // Send result back
      const followUp = await client.chat.completions.create({
        model: 'openai/gpt-4-turbo',
        messages: [
          { role: 'user', content: 'What is the weather in Tokyo?' },
          message,
          {
            role: 'tool',
            tool_call_id: toolCall.id,
            content: JSON.stringify(result),
          },
        ],
        tools,
      });

      console.log(followUp.choices[0].message.content);
    }
  }
}
```

### Multi-Step Function Calling

```typescript
async function multiStepFunctionCall(userQuery: string) {
  const messages = [{ role: 'user', content: userQuery }];
  let iterationCount = 0;
  const maxIterations = 5;

  while (iterationCount < maxIterations) {
    const completion = await client.chat.completions.create({
      model: 'openai/gpt-4-turbo',
      messages,
      tools,
      tool_choice: 'auto',
    });

    const message = completion.choices[0].message;
    messages.push(message);

    if (!message.tool_calls) {
      // No more function calls, return final response
      return message.content;
    }

    // Execute all function calls
    for (const toolCall of message.tool_calls) {
      const functionName = toolCall.function.name;
      const args = JSON.parse(toolCall.function.arguments);

      // Execute function (implement your function registry)
      const result = await executeFunctionCall(functionName, args);

      messages.push({
        role: 'tool',
        tool_call_id: toolCall.id,
        content: JSON.stringify(result),
      });
    }

    iterationCount++;
  }

  throw new Error('Max iterations reached');
}
```

## Cost Optimization

### Token Counting and Cost Estimation

```typescript
import { encoding_for_model } from 'tiktoken';

interface CostEstimate {
  promptTokens: number;
  completionTokens: number;
  promptCost: number;
  completionCost: number;
  totalCost: number;
}

const modelPricing = {
  'anthropic/claude-3.5-sonnet': { input: 3.00, output: 15.00 },  // per 1M tokens
  'anthropic/claude-3-haiku': { input: 0.25, output: 1.25 },
  'openai/gpt-4-turbo': { input: 10.00, output: 30.00 },
  'openai/gpt-3.5-turbo': { input: 0.50, output: 1.50 },
  'google/gemini-flash-1.5': { input: 0.075, output: 0.30 },
};

function estimateCost(
  prompt: string,
  expectedCompletion: number,
  model: string
): CostEstimate {
  const encoder = encoding_for_model('gpt-4');  // Approximation
  const promptTokens = encoder.encode(prompt).length;
  const completionTokens = expectedCompletion;

  const pricing = modelPricing[model] || { input: 0, output: 0 };

  const promptCost = (promptTokens / 1_000_000) * pricing.input;
  const completionCost = (completionTokens / 1_000_000) * pricing.output;

  return {
    promptTokens,
    completionTokens,
    promptCost,
    completionCost,
    totalCost: promptCost + completionCost,
  };
}

// Usage
const estimate = estimateCost(
  'Explain quantum computing',
  500,  // Expected response tokens
  'anthropic/claude-3.5-sonnet'
);

console.log(`Estimated cost: $${estimate.totalCost.toFixed(4)}`);
```

### Dynamic Model Selection by Budget

```typescript
async function budgetOptimizedChat(
  prompt: string,
  maxCostPerRequest: number = 0.01  // $0.01 max
) {
  // Estimate with expensive model
  const expensiveEstimate = estimateCost(
    prompt,
    1000,
    'anthropic/claude-3.5-sonnet'
  );

  let selectedModel = 'anthropic/claude-3.5-sonnet';

  if (expensiveEstimate.totalCost > maxCostPerRequest) {
    // Try cheaper models
    const cheapEstimate = estimateCost(
      prompt,
      1000,
      'anthropic/claude-3-haiku'
    );

    if (cheapEstimate.totalCost > maxCostPerRequest) {
      selectedModel = 'google/gemini-flash-1.5';
    } else {
      selectedModel = 'anthropic/claude-3-haiku';
    }
  }

  console.log(`Selected model: ${selectedModel}`);

  const completion = await client.chat.completions.create({
    model: selectedModel,
    messages: [{ role: 'user', content: prompt }],
  });

  return completion.choices[0].message.content;
}
```

### Batching for Cost Reduction

```typescript
async function batchProcess(prompts: string[], model: string) {
  // Process multiple prompts in parallel with rate limiting
  const concurrency = 5;
  const results = [];

  for (let i = 0; i < prompts.length; i += concurrency) {
    const batch = prompts.slice(i, i + concurrency);

    const batchResults = await Promise.all(
      batch.map(prompt =>
        client.chat.completions.create({
          model,
          messages: [{ role: 'user', content: prompt }],
          max_tokens: 500,  // Limit tokens to control cost
        })
      )
    );

    results.push(...batchResults);

    // Rate limiting delay
    if (i + concurrency < prompts.length) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }

  return results;
}
```

## Model Fallback and Retry Strategy

### Automatic Fallback

```typescript
const modelFallbackChain = [
  'anthropic/claude-3.5-sonnet',
  'openai/gpt-4-turbo',
  'anthropic/claude-3-haiku',
  'google/gemini-flash-1.5',
];

async function chatWithFallback(
  prompt: string,
  maxRetries: number = 3
): Promise<string> {
  for (const model of modelFallbackChain) {
    try {
      console.log(`Trying model: ${model}`);

      const completion = await client.chat.completions.create({
        model,
        messages: [{ role: 'user', content: prompt }],
        max_tokens: 2000,
      });

      return completion.choices[0].message.content || '';
    } catch (error) {
      console.warn(`Model ${model} failed:`, error);

      // Continue to next model
      if (model === modelFallbackChain[modelFallbackChain.length - 1]) {
        throw new Error('All models failed');
      }
    }
  }

  throw new Error('No models available');
}
```

### Exponential Backoff for Rate Limits

```typescript
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxRetries: number = 5
): Promise<T> {
  let lastError: Error;

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;

      // Check if rate limit error
      if (error.status === 429) {
        const delay = Math.pow(2, i) * 1000;  // Exponential backoff
        console.log(`Rate limited. Retrying in ${delay}ms...`);
        await new Promise(resolve => setTimeout(resolve, delay));
      } else {
        throw error;  // Non-retryable error
      }
    }
  }

  throw lastError!;
}

// Usage
const result = await retryWithBackoff(() =>
  client.chat.completions.create({
    model: 'anthropic/claude-3.5-sonnet',
    messages: [{ role: 'user', content: 'Hello' }],
  })
);
```

## Prompt Engineering Best Practices

### System Prompts for Consistency

```typescript
const systemPrompts = {
  concise: 'You are a helpful assistant. Be concise and direct.',
  detailed: 'You are a knowledgeable expert. Provide comprehensive answers with examples.',
  code: 'You are an expert programmer. Provide clean, well-commented code with explanations.',
  creative: 'You are a creative writing assistant. Be imaginative and engaging.',
};

async function chatWithPersonality(
  prompt: string,
  personality: keyof typeof systemPrompts
) {
  const completion = await client.chat.completions.create({
    model: 'anthropic/claude-3.5-sonnet',
    messages: [
      { role: 'system', content: systemPrompts[personality] },
      { role: 'user', content: prompt },
    ],
  });

  return completion.choices[0].message.content;
}
```

### Few-Shot Prompting

```typescript
async function fewShotClassification(text: string) {
  const completion = await client.chat.completions.create({
    model: 'openai/gpt-4-turbo',
    messages: [
      {
        role: 'system',
        content: 'Classify text sentiment as positive, negative, or neutral.',
      },
      { role: 'user', content: 'I love this product!' },
      { role: 'assistant', content: 'positive' },
      { role: 'user', content: 'This is terrible.' },
      { role: 'assistant', content: 'negative' },
      { role: 'user', content: 'It works fine.' },
      { role: 'assistant', content: 'neutral' },
      { role: 'user', content: text },
    ],
  });

  return completion.choices[0].message.content;
}
```

### Chain of Thought Prompting

```typescript
async function reasoningTask(problem: string) {
  const completion = await client.chat.completions.create({
    model: 'anthropic/claude-3.5-sonnet',
    messages: [
      {
        role: 'user',
        content: `${problem}\n\nLet's solve this step by step:\n1.`,
      },
    ],
    max_tokens: 3000,
  });

  return completion.choices[0].message.content;
}
```

## Rate Limits and Throttling

### Rate Limit Handler

```typescript
class RateLimitedClient {
  private requestQueue: Array<() => Promise<any>> = [];
  private processing = false;
  private requestsPerMinute = 60;
  private requestInterval = 60000 / this.requestsPerMinute;

  async enqueue<T>(request: () => Promise<T>): Promise<T> {
    return new Promise((resolve, reject) => {
      this.requestQueue.push(async () => {
        try {
          const result = await request();
          resolve(result);
        } catch (error) {
          reject(error);
        }
      });

      this.processQueue();
    });
  }

  private async processQueue() {
    if (this.processing || this.requestQueue.length === 0) return;

    this.processing = true;

    while (this.requestQueue.length > 0) {
      const request = this.requestQueue.shift()!;
      await request();
      await new Promise(resolve => setTimeout(resolve, this.requestInterval));
    }

    this.processing = false;
  }
}

// Usage
const rateLimitedClient = new RateLimitedClient();

const result = await rateLimitedClient.enqueue(() =>
  client.chat.completions.create({
    model: 'anthropic/claude-3.5-sonnet',
    messages: [{ role: 'user', content: 'Hello' }],
  })
);
```

## Vision Models

### Image Understanding

```typescript
async function analyzeImage(imageUrl: string, question: string) {
  const completion = await client.chat.completions.create({
    model: 'openai/gpt-4-vision-preview',
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: question },
          { type: 'image_url', image_url: { url: imageUrl } },
        ],
      },
    ],
    max_tokens: 1000,
  });

  return completion.choices[0].message.content;
}

// Usage
const result = await analyzeImage(
  'https://example.com/image.jpg',
  'What objects are in this image?'
);
```

### Multi-Image Analysis

```typescript
async function compareImages(imageUrls: string[]) {
  const completion = await client.chat.completions.create({
    model: 'openai/gpt-4-vision-preview',
    messages: [
      {
        role: 'user',
        content: [
          { type: 'text', text: 'Compare these images and describe the differences:' },
          ...imageUrls.map(url => ({
            type: 'image_url' as const,
            image_url: { url },
          })),
        ],
      },
    ],
  });

  return completion.choices[0].message.content;
}
```

## Error Handling and Monitoring

### Comprehensive Error Handler

```typescript
interface ErrorResponse {
  error: {
    message: string;
    type: string;
    code: string;
  };
}

async function robustCompletion(prompt: string) {
  try {
    const completion = await client.chat.completions.create({
      model: 'anthropic/claude-3.5-sonnet',
      messages: [{ role: 'user', content: prompt }],
    });

    return completion.choices[0].message.content;
  } catch (error: any) {
    // Rate limit errors
    if (error.status === 429) {
      console.error('Rate limit exceeded. Please wait.');
      throw new Error('RATE_LIMIT_EXCEEDED');
    }

    // Invalid API key
    if (error.status === 401) {
      console.error('Invalid API key');
      throw new Error('INVALID_API_KEY');
    }

    // Model not found
    if (error.status === 404) {
      console.error('Model not found');
      throw new Error('MODEL_NOT_FOUND');
    }

    // Server errors
    if (error.status >= 500) {
      console.error('OpenRouter server error');
      throw new Error('SERVER_ERROR');
    }

    // Unknown error
    console.error('Unknown error:', error);
    throw error;
  }
}
```

### Request/Response Logging

```typescript
class LoggingClient {
  async chat(prompt: string, model: string) {
    const startTime = Date.now();

    console.log('[Request]', {
      timestamp: new Date().toISOString(),
      model,
      promptLength: prompt.length,
    });

    try {
      const completion = await client.chat.completions.create({
        model,
        messages: [{ role: 'user', content: prompt }],
      });

      const duration = Date.now() - startTime;

      console.log('[Response]', {
        timestamp: new Date().toISOString(),
        duration,
        usage: completion.usage,
        finishReason: completion.choices[0].finish_reason,
      });

      return completion;
    } catch (error) {
      console.error('[Error]', {
        timestamp: new Date().toISOString(),
        duration: Date.now() - startTime,
        error,
      });
      throw error;
    }
  }
}
```

## Best Practices

1. **Model Selection**:
   - Use fast models (Haiku, Flash) for simple tasks
   - Use flagship models (Sonnet, GPT-4) for complex reasoning
   - Consider context size requirements
   - Test multiple models for your use case

2. **Cost Optimization**:
   - Estimate costs before requests
   - Use cheaper models when possible
   - Implement token limits
   - Cache common responses
   - Batch similar requests

3. **Streaming**:
   - Always use streaming for user-facing apps
   - Handle connection interruptions
   - Show progress indicators
   - Buffer partial responses

4. **Error Handling**:
   - Implement retry logic with exponential backoff
   - Use model fallbacks for reliability
   - Log all errors for debugging
   - Handle rate limits gracefully

5. **Prompt Engineering**:
   - Use system prompts for consistency
   - Implement few-shot learning for specific tasks
   - Use chain-of-thought for complex reasoning
   - Keep prompts concise to reduce costs

6. **Rate Limiting**:
   - Respect API rate limits
   - Implement request queuing
   - Use exponential backoff
   - Monitor usage metrics

7. **Security**:
   - Never expose API keys in client code
   - Use environment variables
   - Implement server-side proxies
   - Validate user inputs

8. **Monitoring**:
   - Track token usage
   - Monitor response times
   - Log errors and failures
   - Analyze model performance

## Common Pitfalls

❌ **Exposing API keys in frontend**:
```typescript
// WRONG - API key exposed
const client = new OpenAI({
  baseURL: 'https://openrouter.ai/api/v1',
  apiKey: 'sk-or-v1-...',  // Exposed!
});
```

✅ **Correct - Server-side proxy**:
```typescript
// Backend proxy
app.post('/api/chat', async (req, res) => {
  const { prompt } = req.body;

  const completion = await client.chat.completions.create({
    model: 'anthropic/claude-3.5-sonnet',
    messages: [{ role: 'user', content: prompt }],
  });

  res.json(completion);
});
```

❌ **Not handling streaming errors**:
```typescript
// WRONG - no error handling
for await (const chunk of stream) {
  console.log(chunk.choices[0].delta.content);
}
```

✅ **Correct - with error handling**:
```typescript
try {
  for await (const chunk of stream) {
    const content = chunk.choices[0]?.delta?.content || '';
    process.stdout.write(content);
  }
} catch (error) {
  console.error('Stream error:', error);
  // Implement retry or fallback
}
```

❌ **Ignoring rate limits**:
```typescript
// WRONG - no rate limiting
const promises = prompts.map(prompt => chat(prompt));
await Promise.all(promises);  // May hit rate limits
```

✅ **Correct - with rate limiting**:
```typescript
const results = [];
for (let i = 0; i < prompts.length; i += 5) {
  const batch = prompts.slice(i, i + 5);
  const batchResults = await Promise.all(batch.map(chat));
  results.push(...batchResults);
  await new Promise(r => setTimeout(r, 1000));  // Delay between batches
}
```

## Performance Optimization

### Caching Responses

```typescript
const responseCache = new Map<string, string>();

async function cachedChat(prompt: string, model: string) {
  const cacheKey = `${model}:${prompt}`;

  if (responseCache.has(cacheKey)) {
    console.log('Cache hit');
    return responseCache.get(cacheKey)!;
  }

  const completion = await client.chat.completions.create({
    model,
    messages: [{ role: 'user', content: prompt }],
  });

  const response = completion.choices[0].message.content || '';
  responseCache.set(cacheKey, response);

  return response;
}
```

### Parallel Processing

```typescript
async function parallelChat(prompts: string[], model: string) {
  const results = await Promise.all(
    prompts.map(prompt =>
      client.chat.completions.create({
        model,
        messages: [{ role: 'user', content: prompt }],
      })
    )
  );

  return results.map(r => r.choices[0].message.content);
}
```

## Resources

- **Documentation**: https://openrouter.ai/docs
- **API Reference**: https://openrouter.ai/docs/api-reference
- **Model List**: https://openrouter.ai/models
- **Pricing**: https://openrouter.ai/docs/pricing
- **Status Page**: https://status.openrouter.ai

## Related Skills

- **MCP Servers**: Integration with Model Context Protocol (when built)
- **TypeScript API Integration**: Type-safe OpenRouter clients
- **Python API Integration**: Python SDK usage patterns

## Summary

- **OpenRouter** provides unified access to 200+ LLMs
- **OpenAI-compatible** API for easy migration
- **Cost optimization** through model selection and token management
- **Streaming** for responsive user experiences
- **Function calling** for tool integration
- **Vision models** for image understanding
- **Fallback strategies** for reliability
- **Rate limiting** and error handling essential
- **Perfect for** multi-model apps, cost-sensitive deployments, avoiding vendor lock-in
