# OpenRouter AI Service Skill

Comprehensive skill for using OpenRouter - a unified AI API gateway providing access to 200+ language models through a single, OpenAI-compatible interface.

## Overview

This skill covers:
- **Model Selection**: Choosing optimal models for quality, speed, or cost
- **Streaming Responses**: Real-time response handling in TypeScript, Python, and React
- **Function Calling**: Tool integration and multi-step reasoning
- **Cost Optimization**: Token estimation, budget management, and model fallbacks
- **Rate Limiting**: Request throttling and retry strategies
- **Prompt Engineering**: System prompts, few-shot learning, chain-of-thought
- **Vision Models**: Image understanding and multi-image analysis
- **Error Handling**: Comprehensive error recovery and monitoring

## Progressive Loading Model

### Entry Point (65-80 tokens)
- Quick summary of OpenRouter capabilities
- When to use (multi-model apps, cost optimization, vendor neutrality)
- Quick start steps

### Full Skill (~4,200 tokens)
Complete implementation guide including:
- Basic setup and authentication
- Model selection strategies (flagship, fast, budget, specialized)
- Streaming implementation (TypeScript, Python, React)
- Function calling patterns
- Cost estimation and optimization
- Rate limiting and retry logic
- Prompt engineering best practices
- Vision model usage
- Error handling and monitoring

## Key Features

### Model Categories Covered
1. **Flagship Models**: Claude 3.5 Sonnet, GPT-4 Turbo, Gemini Pro 1.5
2. **Fast Models**: Claude Haiku, GPT-3.5, Gemini Flash, Llama 3.1
3. **Budget Models**: Gemini Flash, Haiku, Mixtral, Llama 3.1
4. **Specialized**: Vision (GPT-4V), Code (Claude Sonnet), Long Context (Gemini Pro)

### Implementation Patterns
- OpenAI SDK compatibility (drop-in replacement)
- Real-time streaming with error recovery
- Function calling and tool integration
- Dynamic model selection based on cost/quality/speed
- Automatic fallback chains
- Exponential backoff for rate limits
- Request queuing and throttling

### Cost Optimization Strategies
- Token counting and cost estimation
- Budget-based model selection
- Batch processing with rate limiting
- Response caching
- Token limit enforcement

## Usage Examples

### Quick Start
```typescript
import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: 'https://openrouter.ai/api/v1',
  apiKey: process.env.OPENROUTER_API_KEY,
});

const completion = await client.chat.completions.create({
  model: 'anthropic/claude-3.5-sonnet',
  messages: [{ role: 'user', content: 'Hello!' }],
});
```

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

### Cost-Optimized Selection
```typescript
const model = selectModel({
  task: 'code',
  priority: 'cost',
  maxCost: 0.5,  // Max $0.50 per 1M tokens
});
// Returns: 'google/gemini-flash-1.5' or 'meta-llama/llama-3.1-8b-instruct'
```

## Best Practices Highlighted

1. **Never expose API keys in frontend code** - Use server-side proxies
2. **Always implement streaming** for user-facing applications
3. **Estimate costs before requests** to avoid budget overruns
4. **Use model fallbacks** for production reliability
5. **Implement exponential backoff** for rate limit handling
6. **Cache common responses** to reduce API costs
7. **Monitor token usage** and response times
8. **Validate inputs** before sending to API

## Common Pitfalls Covered

- API key exposure in client code
- Missing error handling in streaming
- Ignoring rate limits
- Not implementing fallback strategies
- Inefficient prompt design
- Missing token limits
- Poor cost estimation

## Related Skills

- **MCP Servers**: Model Context Protocol integration (when built)
- **TypeScript API Integration**: Type-safe client patterns
- **Python API Integration**: Python SDK usage

## Token Budget

- **Entry Point**: ~75 tokens (quick reference)
- **Full Content**: ~4,180 tokens (comprehensive guide)
- **Total**: Well within 4,500 token target

## File Structure

```
toolchains/ai/services/openrouter/
├── SKILL.md          # Main skill content with progressive loading
├── metadata.json     # Skill metadata and configuration
└── README.md        # This file - skill overview
```

## Version History

- **v1.0.0** (2025-11-30): Initial release with comprehensive OpenRouter coverage

## License

MIT License - Part of Claude MPM Skills repository
