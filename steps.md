E2E (fastest) with OpenRouter mode
What you get
A working end-to-end flow via n8n → Kimi-VL (openrouter) → OpenAI nodes → Postgres, archiving processed results.
Changes
Update 
services/kimi-vl/main.py
 (OpenRouterProcessor) to also return text_content (concise textual summary) and a computed confidence (e.g., based on extraction completeness) to satisfy current n8n assumptions.
Implement 
save_processed_file()
 to write {upload, output.json, metadata.json} to data/processed/.
Add config/postgres/init-tables.sql to create processed_documents and mount it in 
docker-compose.yml
 via /docker-entrypoint-initdb.d.
Verify .env values: OPENROUTER_API_KEY, PROCESSING_MODE=openrouter.
BMAD workflow
@sm Draft story: Align Kimi-VL output with n8n + persistence + DB schema
@qa *design (test strategy) → @dev Implement → @qa *review
Effort
~2–4 hours to implement + test with sample_docs/.

Acceptance Criteria
- Kimi-VL in openrouter mode returns `data.text_content` and `data.confidence`.
- `save_processed_file()` writes original upload and `output.json` + `metadata.json` under `data/processed/`.
- Postgres has `processed_documents` table created via `config/postgres/init-tables.sql`.
- n8n workflow executes successfully on a sample doc and returns a success response; one row is inserted into `processed_documents`.
Local-only stack (privacy-first, no external APIs)
What you get
Fully local path using PROCESSING_MODE=local, optionally introducing Ollama for classification/extraction/validation as per 
ai-docs/local-multi-agent-implementation.md
.
Changes
Switch to PROCESSING_MODE=local in .env.
Ensure 
LocalProcessor
 returns text_content and confidence (it already does), so the current n8n flow works immediately.
Implement 
save_processed_file()
.
Optionally extend 
docker-compose.yml
 to include Ollama and plug local LLMs per the local guide.
Add config/postgres/init-tables.sql for processed_documents.
BMAD workflow
@architect Define local-only architecture slice
@sm Draft story: local E2E MVP → @qa *risk and @qa *design → @dev → @qa *review
Effort
~2–6 hours (quicker if you skip Ollama for now and just use the LocalProcessor mock).

Acceptance Criteria
- `.env` sets `PROCESSING_MODE=local` and Kimi-VL returns `data.text_content` and `data.confidence`.
- `save_processed_file()` persists outputs to `data/processed/`.
- `processed_documents` table exists and receives an insert from a successful run.
Fix n8n workflow to match Kimi-VL’s OpenRouter shape (minimal API changes)
What you get
Keep Kimi-VL’s openrouter payload as is (with extracted_fields), adjust n8n to:
Classify using first-pass structured fields instead of data.text_content.
Remove confidence dependency or compute a score from extraction completeness in n8n.
Changes
Edit 
n8n/workflows/document-processing-pipeline.json
 nodes:
Classification prompt reads from {{$json.data.extracted_fields}} (or add a preliminary “summarize” step).
IF conditions compute confidence from e.g. presence of key fields.
Implement 
save_processed_file()
; add DB init SQL for processed_documents.
BMAD workflow
@pm Outline workflow alignment task
@dev Update n8n nodes → @qa *trace coverage on acceptance criteria
Effort
~2–3 hours if we keep changes constrained to n8n.

Acceptance Criteria
- Classification prompt reads from `{{$json.data.extracted_fields}}` (or a preceding summarize step) instead of `text_content`.
- Confidence gating computed from presence of key fields; execution path proceeds correctly for both high/low confidence.
- Full run inserts into `processed_documents` and returns a success response.
Observability + QA-first hardening (for long-term quality)
What you get
Prometheus metrics and better logs in Kimi-VL, quality gates with BMAD QA artifacts.
Changes
Add counters/histograms in 
services/kimi-vl/main.py
 (duration, errors, confidence).
Wire to prometheus/grafana already in 
docker-compose.yml
.
Create docs/qa/assessments/ and docs/qa/gates/ and start using @qa *risk, @qa *design, @qa *review, @qa *gate.
BMAD workflow
@qa *risk before dev, @qa *design test plan, @qa *review after changes, @qa *gate.
Effort
~2–4 hours for first pass dashboards + QA docs.

Acceptance Criteria
- Kimi-VL exposes Prometheus metrics (e.g., processing duration histogram, error counter, confidence histogram).
- Grafana dashboard shows live metrics after a test run (`docker-compose --profile monitoring up -d`).
- QA artifacts exist under `docs/qa/` with risk assessment, test design, and a gate checklist.
HITL review UX (human-in-the-loop) via n8n forms
What you get
A usable human-review lane: the existing “Human Review Form” node is in the workflow, we’ll finish the round-trip to store reviewer corrections and reprocess.
Changes
Add an endpoint (or an n8n subflow) to accept corrected JSON and update DB.
Persist review queue entries in Postgres.
BMAD workflow
@pm Define HITL acceptance criteria
@dev Implement feedback handling → @qa *nfr for usability/reliability checks
Effort
~3–6 hours depending on how rich the review loop is.

Acceptance Criteria
- Human Review Form persists corrections to Postgres (review queue/corrections table) and triggers reprocessing.
- Final corrected result is stored; `processed_documents.status` reflects `completed`.

---
### **Implement Advanced Agentic Extractor (Multi-Page & Granular Control)**

*   **What you get:** A highly accurate and robust extraction pipeline that correctly processes multi-page documents by using n8n as an orchestrator. The Python service becomes a "toolkit" of specialized functions, giving us granular control over the extraction process.
*   **Changes:**
    1.  **`requirements.txt`:** Add the `PyMuPDF` library to handle splitting PDFs into images.
    2.  **`services/kimi-vl/main.py`:** Refactor the service into a "toolkit" of granular endpoints that the n8n coordinator can call.
        *   `/split_pdf`: Takes a PDF, returns a list of page image identifiers.
        *   `/extract_header`: Takes a page image, extracts only header/footer fields (e.g., invoice number, totals).
        *   `/extract_line_items`: Takes a page image, finds the table, and extracts all line items from it. This endpoint will contain the granular row-by-row logic.
    3.  **`n8n/workflows/`:** Create a new `advanced-agentic-workflow.json`. This workflow will act as the coordinator:
        *   It receives the file and calls `/split_pdf`.
        *   It calls `/extract_header` on the first page.
        *   It loops through all pages, calling `/extract_line_items` on each.
        *   It uses n8n's data nodes to merge the header data and all the line item arrays into a single, final JSON object.
*   **BMAD Workflow:** `@architect Design multi-page agentic workflow -> @sm Draft stories for toolkit endpoints and n8n orchestration -> @dev Implement -> @qa *design complex multi-page test cases`
*   **Effort:** `~8-12 hours`
*   **Acceptance Criteria:**
    - `/split_pdf` returns page identifiers for multi-page PDFs; downstream steps consume them.
    - `/extract_header` extracts header/footer fields deterministically for first page.
    - `/extract_line_items` aggregates row data across pages; final merged JSON matches schema and totals reconcile.
---
### Hybrid Architecture (n8n ingestion + LangGraph Orchestrator + LangSmith)

What you get
- n8n stays simple: only ingestion + single HTTP call
- Python service handles staged multi-page extraction at `/orchestrate`
- Optional LangSmith tracing for deep observability

Changes
- Add orchestration endpoint in `services/kimi-vl/main.py`: `POST /orchestrate`
- Add PyMuPDF rendering for multi-page PDFs and staged prompts for header/line-items
- Add `langgraph`, `langsmith`, and `PyMuPDF` to `services/kimi-vl/requirements.txt`
- Add `n8n/workflows/hybrid-agentic-workflow.json` (Webhook → HTTP `/orchestrate` → Postgres → Respond)
- Extend `.env.example` with optional LangSmith variables

Acceptance Criteria
- Triggering `hybrid-agentic-workflow.json` with a sample PDF returns success
- `/orchestrate` responds with `{ text_content, confidence, extracted_fields, metadata.pages }`
- Artifacts saved under `data/processed/…` and a row inserted into `processed_documents`
- When LangSmith env is enabled, traces appear for orchestrated runs

BMAD workflow
- @architect Define hybrid architecture slice and data contracts
- @sm Draft story for hybrid workflow and orchestrator endpoint
- @dev Implement orchestrator, update requirements, add hybrid workflow
- @qa *design hybrid test cases, verify DB and artifacts

Effort
- ~4–8 hours initial implementation + testing