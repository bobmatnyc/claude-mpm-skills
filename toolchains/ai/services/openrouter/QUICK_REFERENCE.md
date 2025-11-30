# OpenRouter Quick Reference Card

## Setup (30 seconds)

```bash
# 1. Get API key
# Visit: https://openrouter.ai/keys

# 2. Install SDK
npm install openai

# 3. Set environment variable
export OPENROUTER_API_KEY="sk-or-v1-..."
```

## Basic Usage

```typescript
import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: 'https://openrouter.ai/api/v1',
  apiKey: process.env.OPENROUTER_API_KEY,
});

// Chat completion
const response = await client.chat.completions.create({
  model: 'anthropic/claude-3.5-sonnet',
  messages: [{ role: 'user', content: 'Hello!' }],
});
```

## Model Selection Cheat Sheet

| Use Case | Model | Cost (per 1M tokens) | Speed |
|----------|-------|---------------------|-------|
| **Best Quality** | `anthropic/claude-3.5-sonnet` | $3/$15 | Medium |
| **Best Speed** | `anthropic/claude-3-haiku` | $0.25/$1.25 | Fast |
| **Cheapest** | `google/gemini-flash-1.5` | $0.075/$0.30 | Fast |
| **Long Context** | `google/gemini-pro-1.5` | $1.25/$5 | Medium |
| **Vision** | `openai/gpt-4-vision-preview` | $10/$30 | Slow |
| **Code** | `anthropic/claude-3.5-sonnet` | $3/$15 | Medium |
| **General** | `openai/gpt-4-turbo` | $10/$30 | Medium |

## Common Patterns

### Streaming
```typescript
const stream = await client.chat.completions.create({
  model: 'openai/gpt-4-turbo',
  messages: [{ role: 'user', content: 'Tell me a story' }],
  stream: true,
});

for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content || '');
}
```

### Error Handling
```typescript
try {
  const response = await client.chat.completions.create({...});
} catch (error: any) {
  if (error.status === 429) {
    // Rate limit - retry with backoff
  } else if (error.status === 401) {
    // Invalid API key
  } else if (error.status >= 500) {
    // Server error - retry
  }
}
```

### Cost Estimation
```typescript
const pricing = {
  'anthropic/claude-3.5-sonnet': { input: 3.00, output: 15.00 },
  'anthropic/claude-3-haiku': { input: 0.25, output: 1.25 },
  'google/gemini-flash-1.5': { input: 0.075, output: 0.30 },
};

const cost = (tokens / 1_000_000) * pricing[model].input;
```

### Model Fallback
```typescript
const models = [
  'anthropic/claude-3.5-sonnet',
  'openai/gpt-4-turbo',
  'anthropic/claude-3-haiku',
];

for (const model of models) {
  try {
    return await client.chat.completions.create({ model, messages });
  } catch (error) {
    continue; // Try next model
  }
}
```

## Rate Limits

- Default: 60 requests/minute
- Enterprise: Custom limits
- Solution: Implement request queuing

```typescript
await new Promise(resolve => setTimeout(resolve, 1000)); // 1s delay
```

## Security

❌ **NEVER** expose API keys in frontend:
```typescript
// WRONG
const apiKey = 'sk-or-v1-...'; // Exposed!
```

✅ **Use server-side proxy**:
```typescript
// Backend endpoint
app.post('/api/chat', async (req, res) => {
  const completion = await client.chat.completions.create({
    model: req.body.model,
    messages: req.body.messages,
  });
  res.json(completion);
});
```

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 401 | Invalid API key | Check `OPENROUTER_API_KEY` |
| 429 | Rate limit | Implement exponential backoff |
| 404 | Model not found | Check model name spelling |
| 500 | Server error | Retry with backoff |

## Token Limits by Model

| Model | Max Tokens | Context Window |
|-------|-----------|----------------|
| Claude 3.5 Sonnet | 200K | 200K |
| GPT-4 Turbo | 128K | 128K |
| Gemini Pro 1.5 | 2M | 2M |
| Claude Haiku | 200K | 200K |

## Best Practices Checklist

- [ ] Store API keys in environment variables
- [ ] Implement error handling with retry logic
- [ ] Use streaming for user-facing applications
- [ ] Estimate costs before expensive requests
- [ ] Set token limits to control costs
- [ ] Implement rate limiting
- [ ] Use model fallbacks for reliability
- [ ] Log requests for debugging
- [ ] Cache common responses
- [ ] Monitor token usage

## Quick Links

- API Docs: https://openrouter.ai/docs
- Models: https://openrouter.ai/models
- Pricing: https://openrouter.ai/docs/pricing
- Status: https://status.openrouter.ai

---

**See SKILL.md for comprehensive guide with 14+ code examples**
