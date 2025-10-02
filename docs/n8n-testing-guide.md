# n8n End-to-End Testing Guide — Option A (OpenRouter)

This guide walks you through testing the full pipeline with the existing workflow `n8n/workflows/document-processing-pipeline.json`.

## 1) Prerequisites
- `.env` file present (copy from `.env.example`)
- Set:
  - `OPENROUTER_API_KEY=...`
  - `PROCESSING_MODE=openrouter`
- Docker & Docker Compose installed

## 2) Start Services
```bash
# from repo root
cp -n .env.example .env  # if not created yet
# edit .env to set OPENROUTER_API_KEY and PROCESSING_MODE

docker-compose up -d
```
Check status:
```bash
docker-compose ps
```

## 3) Import Workflow in n8n
1. Open n8n UI: http://localhost:5678 (default user: `admin`, pass: `beyan_admin` unless changed in `.env`)
2. Import `n8n/workflows/document-processing-pipeline.json`
3. Ensure OpenAI credentials are configured in n8n (Credentials → “OpenAI API”).

## 4) Test a Document
Two options to trigger the webhook:
- Use n8n Execute Workflow and attach a file to the webhook node (binary property `file`)
- Or POST via curl/Postman to the webhook endpoint:

Webhook URL structure (default):
```
http://localhost:5678/webhook/process-document
```

Example curl:
```bash
curl -X POST \
  -F "file=@sample_docs/2640316788_Commercial Invoice_1.pdf" \
  http://localhost:5678/webhook/process-document
```

## 5) Expected Results
- n8n execution completes
- Response contains success message with key details
- Kimi-VL container logs show a `/process` request with `openrouter` mode
- Files appear under `data/processed/<timestamp>__<filename_without_ext>/`:
  - original uploaded file
  - `output.json` (the service `data` payload)
  - `metadata.json`
- Postgres contains one new row in `processed_documents`

Optional check inside Postgres container:
```bash
docker exec -it beyan-postgres psql -U ${POSTGRES_USER:-n8n} -d beyan_documents -c "SELECT id, filename, status, created_at FROM processed_documents ORDER BY id DESC LIMIT 5;"
```

## 6) Troubleshooting
- 401/403 from n8n
  - Verify n8n basic auth and webhook URL
- 500 from Kimi-VL
  - Check `OPENROUTER_API_KEY`
  - Inspect Kimi-VL logs: `docker-compose logs -f kimi-vl`
- No DB row inserted
  - Ensure Postgres node in n8n points to `beyan_documents` and table `processed_documents`
- Files not saved
  - Confirm `data/processed/` exists and is mounted (see `docker-compose.yml`)

## 7) Next Steps
- Measure and monitor with `--profile monitoring`
- Iterate to Option B/C/D/E/F as defined in `steps.md` and `docs/prd.md`

---

# n8n Hybrid Orchestration Testing — `/orchestrate`

This section tests the hybrid workflow `n8n/workflows/hybrid-agentic-workflow.json` that calls the Python orchestrator endpoint.

## 1) Prerequisites
- Same as Option A plus the following are recommended:
  - Ensure `services/kimi-vl/requirements.txt` includes `PyMuPDF`, `langgraph`, `langsmith`
  - Rebuild Kimi-VL: `docker-compose build kimi-vl` then `docker-compose up -d`

## 2) Import Hybrid Workflow
1. Open n8n UI: http://localhost:5678
2. Import `n8n/workflows/hybrid-agentic-workflow.json`
3. Ensure Postgres credentials are configured in n8n

## 3) Trigger Hybrid Webhook
Webhook URL structure (default):
```
http://localhost:5678/webhook/hybrid-orchestrate
```

Example curl:
```bash
curl -X POST \
  -F "file=@sample_docs/2640316788_Commercial Invoice_1.pdf" \
  http://localhost:5678/webhook/hybrid-orchestrate
```

## 4) Expected Results
- Response indicates success and includes confidence and page count
- Files appear under `data/processed/<timestamp>__<filename_without_ext>/`
- Postgres contains one new row in `processed_documents`

## 5) Optional: LangSmith Tracing
Enable in `.env`:
```
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=...
LANGCHAIN_PROJECT=beyan
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```
Rebuild and restart Kimi-VL to apply environment changes.
