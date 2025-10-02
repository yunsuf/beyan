#!/usr/bin/env bash
set -euo pipefail

BASE_URL=${BASE_URL:-http://localhost:8001}
N8N_WEBHOOK=${N8N_WEBHOOK:-http://localhost:5678/webhook/hybrid-orchestrate}
SMALL_DOC="sample_docs/2640316788_Commercial Invoice_1.pdf"
BIG_DOC="sample_docs/2640316788_Packing List_1.pdf"

echo "==> Hitting /health"
curl -sS "${BASE_URL}/health" | jq . || true

run_doc() {
  local path="$1"
  local label="$2"
  echo "\n==> Orchestrate: ${label} (${path})"
  curl -sS -X POST -F "file=@${path}" "${BASE_URL}/orchestrate" | jq . || true
}

run_webhook() {
  local path="$1"
  local label="$2"
  echo "\n==> n8n Hybrid Webhook: ${label} (${path})"
  curl -sS -X POST -F "file=@${path}" "${N8N_WEBHOOK}" | sed -e 's/^/  /'
}

run_doc "${SMALL_DOC}" "Small Invoice"
run_doc "${BIG_DOC}" "Bigger Doc"

# Give a moment for n8n to insert rows if webhook is used
sleep 1

# Optional: query last 5 DB rows for router decisions
if docker ps --format '{{.Names}}' | grep -q '^beyan-postgres$'; then
  echo "\n==> Last 5 processed_documents (id, filename, created_at):"
  docker exec -e PGPASSWORD=${POSTGRES_PASSWORD:-n8n_password} -it beyan-postgres \
    psql -U ${POSTGRES_USER:-n8n} -d beyan_documents -c \
    "SELECT id, filename, status, created_at, jsonb_pretty(validation) AS router FROM processed_documents ORDER BY id DESC LIMIT 5;" || true
fi
