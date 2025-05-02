CREATE DATABASE actionsuggester;

\c actionsuggester

-- Create the api_querylog table
CREATE TABLE IF NOT EXISTS api_querylog (
    id BIGSERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    tone VARCHAR(100) NOT NULL,
    intent VARCHAR(100) NOT NULL,
    suggested_actions JSONB NOT NULL
);