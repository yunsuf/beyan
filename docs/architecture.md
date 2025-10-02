# Architecture — Beyan Document Digitization System

Version: 0.1
Owner: BMAD @architect
Date: 2025-09-14

## 1. High-Level Overview
Beyan supports two orchestration styles:

- Classic: n8n-centric flow with Kimi-VL `/process` and OpenAI nodes in n8n
- Hybrid (recommended): n8n handles ingestion only; Kimi-VL exposes `/orchestrate` that runs a staged, multi-page extraction inside Python using LangGraph-style composition. LangSmith can be enabled for observability.

```
Classic:
Upload → n8n Webhook → Kimi-VL (/process) → OpenAI Classification → Extraction → Validation → Decision (STP vs HITL) → Postgres (processed_documents) → Respond/Notify

Hybrid:
Upload → n8n Webhook → Kimi-VL (/orchestrate) → staged header + line items extraction → merge → confidence/summary → Postgres → Respond/Notify
```

## 2. Components
- Kimi-VL Service (`services/kimi-vl/`)
  - FastAPI service exposing `/process` and `/health`
  - Hybrid endpoint: `/orchestrate` (staged, multi-page extraction)
  - Modes: `local` (mock) or `openrouter` (calls OpenRouter chat completions)
  - Persists processed results to host via `/processed` volume
  - Optional LangSmith observability via environment
- n8n (`n8n/`)
  - Workflow: `workflows/document-processing-pipeline.json`
  - Hybrid workflow: `workflows/hybrid-agentic-workflow.json` (single HTTP call → `/orchestrate`)
  - Nodes: Webhook → HTTP Request (Kimi-VL) → IF (confidence) → OpenAI Classification → OpenAI Extraction → OpenAI Validation → IF (validation) → Postgres → Respond
- Database (`config/postgres/`)
  - `init-multiple-databases.sh` creates `beyan_documents`
  - `init-tables.sql` creates `processed_documents` and optional review tables
- Docker Compose (`docker-compose.yml`)
  - Services: n8n, postgres, redis, kimi-vl, optional nginx, prometheus, grafana

## 3. Data Contracts
- Kimi-VL `/process` (classic) and `/orchestrate` (hybrid) responses
  - `data.text_content` (string) — concise summary for downstream classification
  - `data.confidence` (0.0–1.0) — computed coverage score
  - `data.extracted_fields` (object) — structured extraction payload
  - `data.metadata` (object) — processing details

- n8n → Postgres insert into `processed_documents`:
  - `filename` TEXT
  - `classification` JSONB
  - `extraction` JSONB
  - `validation` JSONB
  - `status` TEXT
  - `created_at` TIMESTAMPTZ

## 4. Persistence Layout
Host-mounted directories (see `docker-compose.yml`):
- `data/uploads/` → mounted at `/uploads`
- `data/processed/` → mounted at `/processed`
- `data/models/` → mounted at `/models`

Kimi-VL saves:
- Original file content
- `output.json` (service `data` payload)
- `metadata.json` (filename, timestamp, mode)

## 5. Observability (Optional)
- Prometheus scrape config and Grafana dashboards
- Kimi-VL to emit metrics: processing duration, errors, confidence distribution
- For hybrid, enable LangSmith tracing via `.env` keys (see `.env.example`)

## 6. HITL (Future Option)
- n8n Form node for human review
- Tables: `review_queue`, `reviewer_corrections`
- Reprocessing with corrected data

## 7. Security Notes
- Auth on n8n (`N8N_BASIC_AUTH_*`)
- Use SSL (Nginx) in production profiles
- Never commit secrets; use `.env`

## 8. Roadmap Links
- See `docs/prd.md` for options A–F and acceptance criteria
- See `docs/n8n-testing-guide.md` for end-to-end test steps
