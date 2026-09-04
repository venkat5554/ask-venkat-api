# Ask Venkat API

API-only Cloudflare Worker for the Ask Venkat portfolio assistant.

## Responsibilities

- `POST /api/chat` — retrieve relevant portfolio context and answer with Groq.
- `POST /api/admin/ingest` — embed and upsert `src/knowledge.py` into Cloudflare Vectorize.
- `GET /health` — health check.

The public chat UI lives in the separate portfolio repository.

## Cloudflare resources

Create/attach:

1. Workers AI binding named `AI`.
2. Vectorize index named `ask-venkat-knowledge` using dimensions compatible with `@cf/baai/bge-base-en-v1.5`.
3. Secret `GROQ_API_KEY`.
4. Secret `INGEST_SECRET`.

## Allowed portfolio origins

Edit `wrangler.jsonc` before production deployment:

```json
"ALLOWED_ORIGINS": "https://yourdomain.com,https://www.yourdomain.com"
```

Use your real portfolio origin(s). Do not include URL paths.

## Secrets

Set secrets with Wrangler rather than committing them:

```bash
npx wrangler secret put GROQ_API_KEY
npx wrangler secret put INGEST_SECRET
```

## Development

```bash
npm install
npm run dev
```

## Deploy

```bash
npm run deploy
```

After the first deployment (and whenever `src/knowledge.py` changes), call `/api/admin/ingest` with the `X-Ingest-Secret` header so the Vectorize index is refreshed.

## Custom domain

A clean production setup is:

- Portfolio: `https://yourdomain.com`
- Worker API: `https://api.yourdomain.com`

Then set the portfolio's `assets/js/ask-ai-config.js` to the API hostname.
