---
status: draft
owner: @pm
id: story-option-a
---

# Story: Option A — Align Kimi-VL OpenRouter output with n8n + persistence + DB schema

## Story
As a PM, I want a working end-to-end demo using OpenRouter mode so that stakeholders can see documents processed through n8n → Kimi-VL → OpenAI → Postgres with files persisted to disk.

## Acceptance Criteria
- Kimi-VL in `openrouter` mode returns `data.text_content` and `data.confidence` in the `/process` payload.
- `save_processed_file()` writes original upload + `output.json` + `metadata.json` to `data/processed/<ts>__<filename>/`.
- `processed_documents` table exists (created by `config/postgres/init-tables.sql`).
- The n8n workflow (`n8n/workflows/document-processing-pipeline.json`) executes successfully on a sample document and inserts one row into `processed_documents`.

## Tasks / Subtasks (checkboxes)
- [ ] Verify `.env` contains `PROCESSING_MODE=openrouter` and `OPENROUTER_API_KEY`
- [ ] Implement `OpenRouterProcessor` to return `text_content` and `confidence`
- [ ] Implement `save_processed_file()` to persist upload and JSONs
- [ ] Add `config/postgres/init-tables.sql` and confirm mounted in `docker-compose.yml`
- [ ] Start stack, import workflow, set OpenAI credentials in n8n
- [ ] Run test with `sample_docs/` and verify DB insert and saved artifacts

## Dev Notes
- See `services/kimi-vl/main.py` for implementation details.
- `/processed` is mounted from host `data/processed` in `docker-compose.yml`.
- Postgres initialization runs both `init-multiple-databases.sh` and `init-tables.sql`.

## Testing
1. Start services: `docker-compose up -d`
2. Import workflow into n8n, set OpenAI credential
3. Trigger webhook with a sample PDF
4. Confirm success response, saved files, and DB row

## File List (to be updated by dev)
- services/kimi-vl/main.py
- config/postgres/init-tables.sql
- n8n/workflows/document-processing-pipeline.json

## Change Log
- Initial draft created

## Agent Model Used
- @dev

## Debug Log References
- N/A
