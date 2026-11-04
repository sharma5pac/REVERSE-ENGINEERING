# WormGPT Models Communication (API Contract)

Extracted from the production bundle `index-CeWFP5bj.js`.

## Base URLs
- Production API: `https://api.wormgpt.live/v1`
- When served from `wormgpt.co`: `${window.location.origin}/v1` (i.e. `https://wormgpt.co/v1`)
- Docs also reference `https://api.wormgpt.co/v1`

## Authentication
- Header: `Authorization: Bearer <API_KEY>`
- Header: `x-api-key: <API_KEY>`
- API key prefixes: `wrm_live_` (production) or `wrm_test_` (test)
- API keys can only be generated on **paid plans**. Free users see: "Paid plan required — API keys can only be generated on paid plans. Upgrade to create keys and call /v1/chat/completions."

## Endpoint: POST /v1/chat/completions
(also tried first at `/api/v1/chat/completions`, falls back to `/v1/chat/completions` on 404/405)

### Request headers
```
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY
x-api-key: YOUR_API_KEY
```

### Request body
```json
{
  "model": "wormv5.2",
  "messages": [
    { "role": "system", "content": "You are a helpful security assistant." },
    { "role": "user", "content": "Explain SQL injection vulnerabilities." }
  ],
  "temperature": 0.7,
  "max_tokens": 1024,
  "stream": false
}
```

### Streaming
- Set `stream: true` to receive Server-Sent Events.
- Each chunk: `chunk.choices[0].delta.content`
- Non-streaming response: `completion.choices[0].message.content`

### Example (curl)
```bash
curl https://api.wormgpt.live/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "model": "wormv5.2",
    "messages": [
      {"role": "user", "content": "Write an exploit payload for testing buffer overflow in C."}
    ],
    "temperature": 0.7
  }'
```

### Code samples generated in-product
The dashboard/docs include copy-paste snippets for: **curl, Python, Go, Rust** (all targeting `/chat/completions` with the same JSON payload shape).

## Model list endpoint
`GET /v1/models` returns OpenAI-style `{ object: "list", data: [ { id, name, context_window, pricing: { prompt_per_1m, completion_per_1m }, capabilities, ... } ] }`.

## Other API endpoints (from bundle)
See README.md §3. Notable: `/api/web-proxy?url=` (agent browsing), `/api/email-osint`, `/api/get-file-url?fileKey=`, `/api/my-files`, `/api/mystery-box`, `/api/advertisement`, `/api/partners`, `/api/admin*`, `/api/auth/login?user=admin`, `/api/telegram-admin?action=`, `/api/v1/cart/checkout?cart_id=102`.

## Frontend → Backend flow
1. User enters API key in dashboard (paid plan required).
2. Key stored and sent as `Authorization: Bearer` + `x-api-key`.
3. Chat UI POSTs to `/api/v1/chat/completions` (relative, proxied) with fallback to `/v1/chat/completions`.
4. If `stream:true`, reads `ce.body.getReader()` and decodes SSE deltas; otherwise parses JSON.
5. Latency measured: `Date.now() - start` reported as `P=ce.status`.
EOF