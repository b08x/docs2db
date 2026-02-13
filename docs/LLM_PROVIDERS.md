# External LLM Provider Configuration

Docs2DB uses OpenAI-compatible APIs and IBM WatsonX for contextual chunk generation. This guide details provider configuration.

## Quick Start

Key chunking parameters:
- `--skip-context`: Disables contextual generation (fastest; lower quality).
- `--context-model`: Model name or identifier.
- `--openai-url`: URL for OpenAI-compatible APIs (Ollama, OpenAI).
- `--watsonx-url`: URL for IBM WatsonX API (mutually exclusive with `--openai-url`).
- `--context-limit`: Overrides model context limit (in tokens) for map-reduce summarization.

**Configuration Methods:**

1. **CLI flags**: Highest priority; one-time override.
2. **Environment variables**: Session-specific.
3. **`.env` file**: Project defaults.
4. **Code defaults**: Fallback values.

All settings use uppercase environment variables:
- `LLM_SKIP_CONTEXT`
- `LLM_CONTEXT_MODEL`
- `LLM_OPENAI_URL`
- `LLM_WATSONX_URL`
- `LLM_CONTEXT_LIMIT_OVERRIDE`
- `WATSONX_API_KEY`
- `WATSONX_PROJECT_ID`

## Local (Ollama)

**Default configuration** (no flags needed):

```bash
uv run docs2db chunk
```

Defaults:
- Model: `qwen2.5:7b-instruct`
- URL: `http://localhost:11434` (Ollama default)

### Fast Local Models:

```bash
# 3B model (2–3x faster)
uv run docs2db chunk --context-model qwen2.5:3b-instruct

# 1.5B model (4–5x faster)
uv run docs2db chunk --context-model qwen2.5:1.5b-instruct

# Alternative fast models
uv run docs2db chunk --context-model llama3.2:3b-instruct
uv run docs2db chunk --context-model gemma2:2b-instruct

# Custom Ollama URL
uv run docs2db chunk --openai-url "http://localhost:11434" --context-model qwen2.5:7b-instruct
```

## WatsonX

WatsonX provides IBM Granite and other models. Authentication requires an API key and project ID.

### Setup:

1. Obtain your API key and project ID from IBM Cloud.
2. Set environment variables:
   ```bash
   export WATSONX_API_KEY="your-api-key"
   export WATSONX_PROJECT_ID="your-project-id"
   ```

3. Run chunking:
   ```bash
   uv run docs2db chunk \
     --watsonx-url "https://us-south.ml.cloud.ibm.com" \
     --context-model "ibm/granite-13b-chat-v2"
   ```

### Region URLs:
- US South: `https://us-south.ml.cloud.ibm.com/ml/v1`
- EU Germany: `https://eu-de.ml.cloud.ibm.com/ml/v1`
- Japan Tokyo: `https://jp-tok.ml.cloud.ibm.com/ml/v1`

## OpenAI

### Setup:

1. Get your API key from OpenAI.
2. Set the environment variable:
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

3. Run chunking:
   ```bash
   uv run docs2db chunk \
     --openai-url "https://api.openai.com" \
     --context-model "gpt-4o-mini"
   ```

## Map-Reduce Summarization

Docs2DB applies map-reduce summarization when documents exceed the model's context window.

### Process

1. **Detection**: Docs2DB estimates token counts before processing, applying a 70% safety margin.
2. **Map Phase**: The system splits the document into chunks that fit the context limit and summarizes each independently.
3. **Reduce Phase**: The system combines summaries. If the combined summary exceeds the limit, the process repeats recursively.
4. **Contextualization**: The final summary provides context for chunk-specific generation.

The system sizes each chunk to account for:
- Summarization prompts (~100 tokens).
- Requested responses (500 tokens).
- A safety buffer.

### Overriding Context Limits

Override built-in limits via CLI, environment variables, or `.env` files:

**CLI:**
```bash
uv run docs2db chunk --context-limit 65536
```

**Environment variable:**
```bash
export LLM_CONTEXT_LIMIT_OVERRIDE=65536
```

## Performance Considerations

Contextual chunking speed depends on:
1. **Model size**: Smaller models (1.5B–3B) are 2–5x faster than 7B+ models.
2. **Latency**: Local Ollama is fastest; external APIs add network overhead.
3. **Document size**: Larger documents may require summarization.
4. **Cost**: External APIs charge per token.

### Recommendations:

**Development/Testing:**
```bash
# Skip context generation
uv run docs2db chunk --skip-context
```

**Production (Speed Priority):**
```bash
# Use local small model
uv run docs2db chunk --context-model qwen2.5:3b-instruct
```

**Production (Quality Priority):**
```bash
# Use capable cloud model
uv run docs2db chunk \
  --openai-url "https://api.openai.com" \
  --context-model "gpt-4o-mini"
```

## Troubleshooting

### Connection Errors
- **Local**: Ensure Ollama is running (`ollama serve`).
- **External**: Check internet connection and firewalls.

### Authentication Errors
- Verify `OPENAI_API_KEY` or `WATSONX_API_KEY` settings.
- Ensure environment variables are exported.

### Model Errors
- Match model names to your provider's catalog.
- **Ollama**: Pull models first (`ollama pull qwen2.5:3b-instruct`).

### Performance Issues
- Use smaller models or `--skip-context`.
- Check provider rate limits.
