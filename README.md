# Decision Model Playground Web

A local web playground for interacting with Ollama decision models (e.g. `clef-flash`, `clef`, `nimble`, `tev1`). Test prompts, inspect the exact JSON request payload, and see structured answers with probabilities and confidence scores.

## Quick Start

1. Make sure Ollama v0.35.0+ is running with the desired model:
   ```bash
   ollama serve
   ollama pull clef-flash
   ```

2. Serve the static files from this directory:
   ```bash
   cd decision-model-playground-web
   python3 -m http.server 8080
   ```

3. Open **http://localhost:8080** in your browser.

> No build step, no dependencies — just a single HTML file.

## Features

- **Request builder** — edit model, state (context text), and decision questions
- **Question types** — `noul` (yes/no probability), `choice` (select from options), `score` (ranked levels)
- **Live Request JSON preview** — see the exact payload sent to Ollama's `/v1/systemone` endpoint
- **cURL export** — copy the equivalent curl command for any request
- **Structured answer display** — answers rendered with probability bars, confidence scores, and highlight colors
- **Raw JSON view** — toggle between formatted answers and raw JSON response
- **Image support** — upload files or paste URLs (Clef models only); sent as base64 in the `images` field
- **Model selector** — fetches available models from your Ollama instance on load
- **Dark theme** — optimized for long sessions

## Ollama Decision API

The app communicates with Ollama via the decision API at `http://localhost:11434/v1/systemone`.

### Request Format

```json
{
  "model": "clef-flash",
  "state": "The input text or JSON object for context",
  "images": ["<base64-encoded>"],
  "questions": {
    "refund": {
      "type": "noul",
      "instructions": "Is the customer requesting a refund?",
      "criteria": { "false": "No refund", "true": "Refund requested" }
    },
    "urgency": {
      "type": "score",
      "instructions": "How urgent is this?",
      "criteria": ["Routine", "Soon", "Immediate"]
    }
  }
}
```

### Response Format

```json
{
  "model": "clef-flash",
  "answers": {
    "refund": {
      "type": "noul",
      "noul": 0.959,
      "confidence": 0.92
    },
    "urgency": {
      "type": "score",
      "score": 1.2,
      "probabilities": [0.1, 0.64, 0.26],
      "confidence": 0.78
    }
  },
  "usage": { "input_tokens": 174, "output_tokens": 1 }
}
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Enter` | Send request |

## License

MIT
