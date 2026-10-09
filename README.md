# PubMed Explorer

A full-stack data application for exploring PubMed articles with search, facets, ML insights, and data management.

[![CI](https://github.com/ndumbe0/pubmed-explorer/actions/workflows/ci.yml/badge.svg)](https://github.com/ndumbe0/pubmed-explorer/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Features
- Full-text search with FTS5
- Faceted browsing (years, journals, keywords)
- Streaming data ingestion (handles large CSV files)
- Bring-your-own data upload and analysis
- ML: similar paper recommendations, topic modeling, classification, trends
- Interactive dashboards with Recharts
- Dark/light mode support

## Tech Stack
- **Backend**: FastAPI, SQLAlchemy, SQLite, FTS5
- **Frontend**: React, Vite, TypeScript, Tailwind CSS, Recharts
- **ML**: scikit-learn, sentence-transformers (optional)
- **Testing**: pytest, Vitest

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+

### Local Development

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8003

# Frontend (in new terminal)
cd frontend
npm install
npm run dev
```

Or use PowerShell:
```powershell
.\run.ps1
```

## API Overview
- `GET /health` - Health check
- `GET /api/pubmed/search` - Full-text search
- `GET /api/facets/summary` - Facet summary
- `POST /api/upload` - Upload data files
- `POST /api/ingest/start` - Start ingestion
- `GET /api/ingest/progress` - Ingestion progress
- `GET /api/export/csv` - Export filtered results

## Documentation
- [Architecture](docs/ARCHITECTURE.md)
- [Model Card](docs/MODEL_CARD.md)
- [Deployment Guide](docs/DEPLOY.md)
