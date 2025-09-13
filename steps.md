
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