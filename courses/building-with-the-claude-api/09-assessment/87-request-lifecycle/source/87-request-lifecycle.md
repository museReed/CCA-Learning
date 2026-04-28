# Request Lifecycle

> This is a synthesized lesson that consolidates the request lifecycle concepts covered across the course. It does not correspond to a specific video lecture.

## Overview

Every Claude interaction follows a five-step round trip:

1. **Request to server** — client app sends user input to your backend
2. **Request to Anthropic API** — your server forwards the request with API key authentication
3. **Model processing** — Claude tokenizes, embeds, contextualizes, and generates
4. **Response to server** — Anthropic returns structured response (message, usage, stop_reason)
5. **Response to client** — your server forwards the generated text to the UI

## Key Concepts

### Why You Need a Server Layer
- Never call the Anthropic API directly from client-side code
- API keys in client code create a serious security vulnerability
- Server layer enables rate limiting, observability, audit logging

### Four Required API Fields
- **API Key** — authenticates your request
- **Model** — which Claude model to use
- **Messages** — the conversation history
- **Max Tokens** — output length limit

### Internal Processing Stages
1. **Tokenization** — break text into tokens (words, sub-words, symbols)
2. **Embedding** — convert tokens to numerical meaning vectors
3. **Contextualization** — refine embeddings using surrounding context
4. **Generation** — predict next tokens using probability + controlled randomness

### Stop Reasons
- `end_turn` — natural completion
- `max_tokens` — hit the token limit
- `stop_sequence` — matched a predefined stop phrase
- `tool_use` — model wants to call a tool
