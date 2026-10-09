# Architecture - PubMed Explorer

## Overview
PubMed Explorer is a full-stack data application for exploring PubMed articles with search, facets, and ML capabilities.

## Tech Stack
- Backend: FastAPI + SQLAlchemy + SQLite
- Frontend: React + Vite + TypeScript + Tailwind CSS + Recharts
- ML: scikit-learn, sentence-transformers (as size allows)
- Search: SQLite FTS5

## Data Flow
1. CSV/XLSX data ingested via CLI or API (streaming, chunked)
2. Data stored in SQLite with deduplication
3. FTS5 index built for full-text search
4. API provides search, facets, details, export
5. Frontend visualizes data with Recharts

## Mermaid Diagram
```mermaid
graph LR
    A[CSV Data] --> B[Streaming Ingest]
    B --> C[SQLite DB]
    C --> D[FTS5 Index]
    D --> E[FastAPI Backend]
    E --> F[React Frontend]
```
