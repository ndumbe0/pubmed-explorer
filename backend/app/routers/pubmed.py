from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import text
from pathlib import Path
from typing import Optional
import json

from app.database import SessionLocal, apply_pragmas
from app.utils.ingest import ingest_full_streaming, load_checkpoint, save_checkpoint

router = APIRouter(prefix="/api/pubmed", tags=["pubmed"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.on_event("startup")
def startup():
    apply_pragmas()

@router.get("/status")
def status():
    cp = load_checkpoint()
    return cp

@router.post("/ingest/test")
def ingest_test(background_tasks: BackgroundTasks, limit: int = Query(10000), resume: bool = False, db: Session = Depends(get_db)):
    # run in foreground for test but controlled
    res = ingest_full_streaming(db, str(Path(__file__).parent.parent.parent.parent / "data" / "key_pubmed.csv"), resume=resume, test_limit=limit)
    return res

@router.post("/build-index")
def build_index(db: Session = Depends(get_db)):
    try:
        db.execute(text("CREATE VIRTUAL TABLE IF NOT EXISTS pubmed_fts USING fts5(title, abstract, keyword, authors, journal, content='pubmed_papers', content_rowid='id')"))
        db.execute(text("INSERT INTO pubmed_fts(pubmed_fts) VALUES('rebuild')"))
        db.execute(text("CREATE INDEX IF NOT EXISTS idx_pubmed_doi ON pubmed_papers(doi)"))
        db.execute(text("CREATE INDEX IF NOT EXISTS idx_pubmed_year ON pubmed_papers(year)"))
        db.execute(text("CREATE INDEX IF NOT EXISTS idx_pubmed_journal ON pubmed_papers(journal)"))
        db.commit()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(400, str(e))

@router.get("/search")
def search(q: str = Query(...), limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    q2 = q.replace("'", "''")
    try:
        rows = db.execute(text("SELECT rowid, title, journal, year, snippet(pubmed_fts, 0, '<b>', '</b>', '...', 10) as snip FROM pubmed_fts WHERE pubmed_fts MATCH :q ORDER BY rank LIMIT :lim OFFSET :off"), {"q": q2, "lim": limit, "off": offset}).fetchall()
        return [{"id": r[0], "title": r[1], "journal": r[2], "year": r[3], "snippet": r[4]} for r in rows]
    except Exception as e:
        raise HTTPException(400, str(e))
