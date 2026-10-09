from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from app.database import SessionLocal

router = APIRouter(prefix="/api/facets", tags=["facets"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    total = db.query(func.count()).select_from(text("pubmed_papers")).scalar()
    years = db.execute(text("SELECT year, count(*) as c FROM pubmed_papers WHERE year IS NOT NULL GROUP BY year ORDER BY year DESC LIMIT 20")).fetchall()
    journals = db.execute(text("SELECT journal, count(*) as c FROM pubmed_papers WHERE journal IS NOT NULL AND journal != '' GROUP BY journal ORDER BY c DESC LIMIT 10")).fetchall()
    return {
        "total": total,
        "years": [{"year": r[0], "count": r[1]} for r in years],
        "journals": [{"journal": r[0], "count": r[1]} for r in journals]
    }
