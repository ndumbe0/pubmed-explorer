# Deployment Guide - PubMed Explorer

## Local Development
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8003

# Frontend
cd frontend
npm install
npm run dev
```

## Demo Mode
For free deployment (Hugging Face Spaces, Render), use the committed sample data (data/samples/). Full dataset is too large for free tiers.

## GitHub Pages (Frontend)
The frontend can be deployed to GitHub Pages via the included workflow. Update API base URL for production.

## Docker
```bash
docker compose up --build
```
