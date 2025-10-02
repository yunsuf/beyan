## 11. Smart Router (OpenRouter Phase 1)

Goals
- Dynamically select the best OpenRouter model per subtask (header vs line items) using routing rules and a model portfolio.
- Keep n8n unchanged (single HTTP call), store router decisions to DB for audit.

Implementation
- Config files: `config/models.yml`, `config/routing.yml`.
- Router modules: `services/kimi-vl/router/{registry,policy,smart_router}.py` and `adapters/openrouter.py`.
- Orchestrator: `/orchestrate` consults router, calls adapter, falls back gracefully if not configured.
- DB: store `metadata.router` and also persist to Postgres `validation` column.

Acceptance Criteria
- For small invoices (<=3 pages), the router selects a mid-tier, low-cost vision model.
- For large/dense invoices (>10 pages or >50 items), the router selects a high-accuracy model.
- If `OPENROUTER_API_KEY` is missing, the flow completes via fallback and still logs router decisions.
- Router decisions appear in response payload and in `processed_documents.validation`.
# Product Requirements Document (PRD) — Beyan Document Digitization System

Version: 0.1
Owner: BMAD @pm
Date: 2025-09-14

## 1. Summary
Beyan automates processing of business documents (invoices, packing lists, certificates) using an agentic workflow orchestrated by n8n and powered by a Kimi-VL microservice and LLM agents. This PRD captures user value, scope boundaries, and acceptance criteria for our incremental options (A–F).

## 2. Goals & Non-Goals
- Goals
  - Turn documents into validated structured JSON with high accuracy
  - Provide a visual, observable orchestration with HITL capability
  - Enable privacy-first local mode and a fast E2E demo mode
- Non-Goals
  - Full ERP integration (out of scope for MVP)
  - Custom OCR training (use LLM/VLM first)

## 3. Users & Use Cases
- Back-office operators upload or forward documents
- System auto-classifies, extracts, validates, and stores results
- When low confidence, HITL reviewers correct and approve data

## 4. High-Level Flow
Upload → n8n Webhook → Kimi-VL → LLM agents (classify/extract/validate) → Decision (STP vs HITL) → Store in Postgres → Notify

## 5. MVP Scope (Option A)
- Kimi-VL in OpenRouter mode
- n8n workflow: classification, extraction, validation using OpenAI nodes
- Postgres persistence: `processed_documents`
- Files archived under `data/processed/`

### Acceptance Criteria (Option A)
- Kimi-VL returns `data.text_content` and `data.confidence` in OpenRouter mode
- `save_processed_file()` persists original + `output.json` + `metadata.json`
- `processed_documents` table exists and receives a row from a successful run
- n8n execution returns success on a sample document

## 6. Future Options (B–F)
- B: Local-only stack (privacy-first)
- C: n8n-only workflow alignment (no API change)
- D: Observability + QA hardening
- E: HITL review loop round-trip
- F: Advanced agentic extractor for multi-page, granular control

## 7. Recommended Path: Hybrid Architecture (n8n + LangGraph + LangSmith)
For the best balance of control and convenience, adopt a hybrid model:

- n8n for ingestion and triggering only (email/watch/webhook → single HTTP call)
- LangGraph-style orchestration within the Python service for multi-page, granular extraction
- LangSmith observability for tracing and debugging complex runs

Implementation Notes
- New endpoint: `POST /orchestrate` in `services/kimi-vl/main.py`
- Multi-page handling via PyMuPDF (render PDF pages to images)
- Staged prompts for header-only and line-item-only extraction, merged server-side
- Optional LangSmith tracing variables in `.env.example`

Acceptance Criteria (Hybrid)
- n8n hybrid workflow triggers a single HTTP step to `/orchestrate` with the file
- `/orchestrate` returns `{ text_content, confidence, extracted_fields, metadata }`
- Files saved in `data/processed/`; `processed_documents` receives an insert via simple Postgres node
- When LangSmith is enabled, traces appear for orchestrated runs

## 8. Success Metrics
- >80% straight-through processing (STP) for target document types
- >95% field-level accuracy after HITL corrections fed back
- <30s average end-to-end latency per document

## 9. Risks & Mitigations
- Model/API variability → implement fallbacks and clear error handling
- Document diversity → use schema-driven prompting and HITL loop
- Cost/latency → local mode and caching where applicable

## 10. Open Questions
- Which external systems to integrate post-MVP?
- Data retention and compliance specifics per environment
