# DarkGPT — Reverse Engineering Analysis

**Target:** https://www.wormgpt.co/
**Analysis date:** 2026-11-03
**Method:** Playwright DOM render + JS bundle static analysis (no authentication, no exploitation)

## 1. Architecture

| Layer | Detail |
|---|---|
| Frontend | React SPA built with Vite |
| Bundle | `/assets/index-CeWFP5bj.js` (~1.89 MB) |
| Styles | `/assets/index-CeysEIn6.css` |
| Service Worker | `/registerSW.js` |
| Anti-bot | Cloudflare Turnstile (`challenges.cloudflare.com/turnstile/v0/api.js?render=explicit`) |
| Backend API | `https://api.wormgpt.live/v1` (separate origin) |
| Theme | Dark by default, localStorage key `worm-theme`, red accent `#FF0000` |
| Fonts | Inter, Cairo, Cinzel, IBM Plex Sans, Literata, Outfit, Source Sans 3, Fira Code |
| Background | dot-grid (`--app-dot-grid`), `#0a0a0a` base |

## 2. Frontend Routes (client-side)
`/` · `/models` · `/pricing` · `/specs` · `/ads` · `/login` · `/signup` · `/dashboard` · `/chat` · `/account` · `/admin` · `/verify` · `/reset-password`

## 3. API Endpoints (extracted from bundle)

Base: `https://api.wormgpt.live/v1`

| Endpoint | Inferred purpose |
|---|---|
| `POST /v1/chat/completions` | OpenAI-compatible chat (core product) |
| `POST /api/chat-proxy` | Chat proxy/relay |
| `POST /api/web-proxy?url=` | Web fetch proxy (agent browsing) |
| `POST /api/get-file-url?fileKey=` | Presigned file download URL |
| `GET /api/my-files` | User file list |
| `POST /api/email-osint` | Email OSINT tool |
| `GET/POST /api/mystery-box` | Mystery box feature |
| `GET /api/advertisement` | Ads |
| `GET /api/partners` | Partners |
| `POST /api/auth/login?user=admin` | Admin login (hardcoded `user=admin` query) |
| `GET/POST /api/admin` | Admin panel |
| `GET/POST /api/admin/users` | Admin user management |
| `GET/POST /api/admin-2fa` | Admin 2FA |
| `POST /api/telegram-admin?action=` | Telegram admin actions |
| `POST /api/v1/cart/checkout?cart_id=102` | Cart checkout |

## 4. Product Surface

### Models (8)
1. WormGPT v6 — FLAGSHIP — Agentic, Deep Reasoning, Uncensored, Premium
2. WormGPT v6.1 — CODING FLAGSHIP — Full Source, Debugging, Architecture
3. WormGPT v5.2 Ultra — THINKING CORE — Zero Restrictions, Deep Reasoning
4. WormGPT v5.1 Uncensored — UNCENSORED — Function Calling, JSON Mode, Multi-turn
5. WormGPT Coder v5.1 — ELITE CODER — AST Parsing, Refactoring, Vulnerability Scan, Full-Stack
6. WormGPT v5.0 Ultra — SUPREME LATENCY — 78 tok/s, Real-time Chat, Agent Loop
7. WormGPT v4.1 — UNFILTERED CREATIVE — Roleplay, Custom Personas, Long Form
8. WormGPT v4 Classic — HIGH EFFICIENT — Text Extraction, High Speed, Baseline

### Pricing
| Plan | Price | Duration | Key perks |
|---|---|---|---|
| 1 Month | $50 | 1 month | Unlimited gens, Worm v5.2 Ultra, Web Search & File Analysis, 4 daily uploads, Full Platform Access |
| 3 Months | $110 | 3 months | + Priority Support, Zero Downtime Fallback (SELECTED default) |
| 1 Year | $175 | 1 year | Unlimited uploads, Priority Support, High Throughput Routing |
| VIP Lifetime | $260 | Lifetime | Faster Responses, File & Web Search, Unlimited Uploads, Agent Mode, VSCode Integration, Full Source Code Access |

Toggle: Pay-as-you-go / Subscription. Free trial credits included.

### Value propositions
- Security & Exploit Audits (pentesting, vuln discovery, exploit verification)
- Full-Stack Code Synthesis (production-ready codebases, AST analysis)
- Zero-Filter Freedom (no topic blocks)

### Stats / social proof
- 8 AI models · 100% uncensored · 80K+ active engineers · 99.9% uptime · 120,000+ users

## 5. Footer & Trust
- `© 2026 WORMGPT.LIVE. All rights reserved.`
- Official sites: wormgpt.live · wormgpt.co · wormgpt4.com · wormgpt4.net · llms.txt
- Support: Telegram
- MetaMask error suppression (crypto payments)

## 6. Security-relevant observations (defensive)
1. Admin login endpoint exposes `user=admin` as a query param in the client bundle — credential/role hint leakage.
2. Bundle ships example payload strings (`attacker-server.com`, `target-server.com`, `vulnerable-ecommerce.shop`, path-traversal & Spring4Shell-style templates) — these appear to be OSINT/exploit playbook fixtures shipped to the client. They are not live targets.
3. `http://internal-vulnerable-host.local`, `https://internal-mainframe.local` — internal hostnames leaked in bundle.
4. Crypto wallet (MetaMask) integration → payments likely crypto; no PCI scope but wallet phishing risk.
5. Cloudflare Turnstile gating signup.

## 7. Not captured (lazy-loaded / auth-gated)
- FAQ answers (collapsed)
- `/specs`, `/ads`, `/dashboard`, `/chat`, `/admin`, `/account` content (require auth or separate chunks)
- Full route/component tree
- Source maps (not exposed)

## 8. Files in this folder
- `README.md` — this document
- `rendered_homepage.txt` — full rendered DOM text
- `api_endpoints.txt` — extracted API paths
- `bundle.js` — production JS bundle (1.89 MB)
- `external_urls.txt` — extracted external URLs

## 9. /models route (OpenAI-compatible model list)

The `/models` route renders an OpenAI-style `/v1/models` JSON response. Per-1M-token pricing:

| Model ID | Name | Context | Prompt $/1M | Completion $/1M | Capabilities |
|---|---|---|---|---|---|
| wormv6.2 | Worm v6.2 | 128k | 0.4 | 1.6 | Chat, Code, Uncensored, Agentic, Full Source, Neural Core v6.2 |
| wormv6 | Worm v6 | 128k | 5.0 | 8.5 | Chat, Code, Uncensored, Agentic, Deep Reasoning, Neural Core v6 |
| wormv6.1 | Worm v6.1 | 128k | 0.4 | 1.6 | Chat, Code, Uncensored, Coding Flagship, Neural Core v6.1 |
| wormv5.2 | Worm v5.2 | 128k | 0.5 | 2.0 | Chat, Code, Uncensored, Deep Reasoning, Neural Core v5.2 |
| wormv5.1 | Worm v5.1 | 128k | 0.4 | 1.6 | Chat, Code, Uncensored, Function Calling, JSON Mode |
| wormv5.0 | Worm v5.0 | 32k | 0.3 | 1.2 | Low Latency, Fast Chat, JSON Output, High Throughput |
| wormv4.1 | Worm v4.1 | 32k | 0.3 | 1.2 | Creative Writing, Unfiltered Responses, Roleplay, Long Form |
| wormv4.0 | Worm v4.0 | 16k | 0.2 | 0.8 | High Efficiency, Text Processing, Summarization, Extraction |

Full JSON: `models_list.json`

## 10. /ads route (Partner With Us)

Self-serve ad marketplace: 50K–60K active users reach. Pricing: 1 Week $50, 1 Month $150, Lifetime $500. Manual review before going live. Submission form: product name, type (Tool/Software, Service, Course/Guide, Other), description, pricing, email/telegram, up to 2 images.

## 11. Files in this folder
- `README.md` — this document
- `rendered_homepage.txt` — full rendered DOM text of homepage
- `rendered_routes.txt` — rendered output of /specs, /models, /pricing, /ads
- `models_list.json` — OpenAI-style model list with per-token pricing
- `api_endpoints.txt` — extracted API paths
- `external_urls.txt` — extracted external URLs
- `bundle.js` — production JS bundle (1.89 MB)
