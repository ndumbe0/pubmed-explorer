from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from pathlib import Path
from app.database import SessionLocal
from app.utils.ingest import ingest_full_streaming, load_checkpoint

router = APIRouter(prefix="/api/ingest", tags=["ingest"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/progress")
def progress():
    return load_checkpoint()

@router.post("/start")
def start_ingest(background_tasks: BackgroundTasks, file_path: str = Query(None), resume: bool = Query(True), db: Session = Depends(get_db)):
    if file_path is None:
        file_path = str(Path(__file__).parent.parent.parent.parent / "data" / "key_pubmed.csv")
    path = Path(file_path)
    if not path.exists():
        raise HTTPException(404, f"File not found: {file_path}")
    # Run in background
    background_tasks.add_task(ingest_full_streaming, db, str(path), resume)
    return {"status": "started", "file": str(path)}
