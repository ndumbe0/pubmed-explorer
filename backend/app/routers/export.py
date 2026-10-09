from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal
import csv
import io
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/api/export", tags=["export"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/csv")
def export_csv(q: str = Query(None), db: Session = Depends(get_db)):
    def iter_csv():
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['id', 'title', 'journal', 'year', 'doi'])
        yield output.getvalue()
        output.seek(0); output.truncate(0)
        if q:
            q2 = q.replace("'", "''")
            rows = db.execute(text("SELECT rowid, title, journal, year, doi FROM pubmed_fts WHERE pubmed_fts MATCH :q"), {"q": q2})
        else:
            rows = db.execute(text("SELECT id, title, journal, year, doi FROM pubmed_papers LIMIT 1000"))
        for r in rows:
            writer.writerow([r[0], r[1], r[2], r[3], r[4]])
            yield output.getvalue()
            output.seek(0); output.truncate(0)
    return StreamingResponse(iter_csv(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=export.csv"})
