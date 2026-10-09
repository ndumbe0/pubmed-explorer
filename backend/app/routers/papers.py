from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal

router = APIRouter(prefix="/api/papers", tags=["papers"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{paper_id}")
def get_paper(paper_id: int, db: Session = Depends(get_db)):
    row = db.execute(text("SELECT id, title, journal, year, doi, abstract, authors, keyword FROM pubmed_papers WHERE id = :id"), {"id": paper_id}).fetchone()
    if not row:
        raise HTTPException(404, "Paper not found")
    return {
        "id": row[0],
        "title": row[1],
        "journal": row[2],
        "year": row[3],
        "doi": row[4],
        "abstract": row[5],
        "authors": row[6],
        "keyword": row[7]
    }
