---
status: draft
owner: @pm
id: story-hybrid-orchestrator
---

# Story: Hybrid Architecture — n8n ingestion + Python Orchestrator (/orchestrate)

## Story
As an Architect/PM, I want a hybrid path where n8n only handles ingestion and the Python service orchestrates multi-page extraction so that we get powerful, code-native control with simple external integration.

## Acceptance Criteria
- New endpoint `POST /orchestrate` processes PDFs (multi-page) and images (single-page) and returns `{ text_content, confidence, extracted_fields, metadata.pages }`.
- A minimal n8n workflow (`n8n/workflows/hybrid-agentic-workflow.json`) triggers `/orchestrate` and stores results in `processed_documents`.
- Artifacts are saved under `data/processed/<ts>__<filename>/`.
- When LangSmith env variables are enabled, traces are visible for an orchestrated run.

## Tasks / Subtasks (checkboxes)
- [ ] Add `/orchestrate` endpoint with header + line-items staged extraction
- [ ] Render PDFs into page images using PyMuPDF
- [ ] Compute confidence and summary server-side
- [ ] Save artifacts and ensure Postgres insertion path works via n8n workflow
- [ ] Document environment variables for LangSmith in `.env.example`
- [ ] Add `n8n/workflows/hybrid-agentic-workflow.json`
- [ ] Test with `/sample_docs` and verify DB row + saved artifacts

## Dev Notes
- See `services/kimi-vl/main.py` for orchestrator implementation
- Required packages: `langgraph`, `langsmith`, `PyMuPDF`

## Testing
1. Start services `docker-compose up -d`
2. Import `n8n/workflows/hybrid-agentic-workflow.json` and set Postgres credentials
3. Trigger webhook with a sample PDF
4. Verify success response, DB row, and saved artifacts

## File List (to be updated by dev)
- services/kimi-vl/main.py
- n8n/workflows/hybrid-agentic-workflow.json
- .env.example

## Change Log
- Initial draft created

## Agent Model Used
- @dev

## Debug Log References
- N/A
