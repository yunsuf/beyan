-- Postgres initialization for Beyan document processing
-- This script is idempotent and safe to run multiple times

-- Switch to the application database created by init-multiple-databases.sh
\connect beyan_documents

-- processed_documents: stores classification, extraction, validation results per file
CREATE TABLE IF NOT EXISTS processed_documents (
    id BIGSERIAL PRIMARY KEY,
    filename TEXT NOT NULL,
    classification JSONB,
    extraction JSONB,
    validation JSONB,
    status TEXT DEFAULT 'completed',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Optional indexes to speed up JSON queries
CREATE INDEX IF NOT EXISTS idx_processed_documents_created_at ON processed_documents (created_at);
CREATE INDEX IF NOT EXISTS idx_processed_documents_status ON processed_documents (status);
CREATE INDEX IF NOT EXISTS idx_processed_documents_classification_gin ON processed_documents USING GIN (classification);
CREATE INDEX IF NOT EXISTS idx_processed_documents_extraction_gin ON processed_documents USING GIN (extraction);
CREATE INDEX IF NOT EXISTS idx_processed_documents_validation_gin ON processed_documents USING GIN (validation);

-- HITL review support (optional, for Option E)
CREATE TABLE IF NOT EXISTS review_queue (
    id BIGSERIAL PRIMARY KEY,
    processed_document_id BIGINT REFERENCES processed_documents(id) ON DELETE CASCADE,
    confidence NUMERIC,
    reason TEXT,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS reviewer_corrections (
    id BIGSERIAL PRIMARY KEY,
    processed_document_id BIGINT REFERENCES processed_documents(id) ON DELETE CASCADE,
    reviewer TEXT,
    corrected_data JSONB NOT NULL,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
