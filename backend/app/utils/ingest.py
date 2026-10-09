from pathlib import Path
from typing import Dict, Optional
import pandas as pd
import json
import csv
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.pubmed import PubmedPaper
from app.utils.parsers import compute_hash, parse_authors, parse_keywords, normalize_text

CHECKPOINT_FILE = Path(__file__).parent.parent.parent.parent / "data" / "ingest_checkpoint.json"

class IngestState:
    def __init__(self):
        self.processed = 0
        self.added = 0
        self.skipped = 0
        self.failed = 0
        self.batch = 0

def load_checkpoint():
    if CHECKPOINT_FILE.exists():
        with open(CHECKPOINT_FILE) as f:
            return json.load(f)
    return {"offset": 0, "added": 0, "skipped": 0, "processed": 0, "total": 0}

def save_checkpoint(data):
    CHECKPOINT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump(data, f)

def ingest_full_streaming(db: Session, file_path: str, resume: bool = True, test_limit: Optional[int] = None) -> Dict:
    path = Path(file_path)
    if not path.exists(): raise FileNotFoundError(file_path)
    cp = load_checkpoint() if resume else {"offset": 0, "added": 0, "skipped": 0, "processed": 0}
    offset = cp.get("offset", 0)
    added = cp.get("added", 0)
    skipped = cp.get("skipped", 0)
    processed = cp.get("processed", 0)
    
    # get total lines approx
    try:
        with open(path, encoding='utf-8', errors='replace') as f:
            total_lines = sum(1 for _ in f)
    except:
        total_lines = offset + 1000000
    
    # build existing doi/hash set for dedup - but for full ingest on fresh db it's fine; for resume, load minimal
    existing_doi = set()
    existing_hash = set()
    if resume and offset > 0:  # load to avoid dup on resume
        for r in db.query(PubmedPaper.doi, PubmedPaper.content_hash).yield_per(10000):
            if r[0]: existing_doi.add(str(r[0]).strip().lower())
            if r[1]: existing_hash.add(r[1])
    
    with open(path, encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        # skip lines if needed
        for _ in range(offset):
            try:
                next(reader)
            except StopIteration:
                break
        batch = []
        for i, row in enumerate(reader):
            if test_limit and processed >= test_limit: break
            processed += 1
            try:
                title = str(row.get('title') or '').strip()
                doi = str(row.get('doi') or '').strip()
                abstract = str(row.get('abstract') or '').strip()
                journal = str(row.get('journal') or '').strip()
                date = str(row.get('date') or '').strip()
                authors = row.get('authors') or ''
                year = row.get('year')
                try:
                    year_int = int(float(year)) if year and str(year).strip() not in ('', 'nan', 'NaN') else None
                except:
                    year_int = None
                keyword = row.get('keyword') or ''
                ch = compute_hash(title, year_int or year, journal, doi)
                if doi and doi.lower() in existing_doi:
                    skipped += 1
                elif ch in existing_hash:
                    skipped += 1
                    if doi: existing_doi.add(doi.lower())
                    existing_hash.add(ch)
                else:
                    obj = PubmedPaper(
                        title=title,
                        doi=doi,
                        abstract=abstract,
                        journal=journal,
                        date=date,
                        published_date=date,
                        authors=json.dumps(parse_authors(authors)),
                        year=year_int,
                        keyword=json.dumps(parse_keywords(keyword)),
                        source_file=path.name,
                        content_hash=ch
                    )
                    batch.append(obj)
                    existing_hash.add(ch)
                    if doi: existing_doi.add(doi.lower())
                    added += 1
                    if len(batch) >= 5000:
                        db.bulk_save_objects(batch)
                        db.commit()
                        batch = []
                        save_checkpoint({"offset": offset + processed, "added": added, "skipped": skipped, "processed": processed, "total": total_lines})
            except Exception as e:
                # one bad row never crashes
                pass
        if batch:
            db.bulk_save_objects(batch)
            db.commit()
        save_checkpoint({"offset": offset + processed, "added": added, "skipped": skipped, "processed": processed, "total": total_lines})
    # build FTS after load if requested
    return {"rows_read": processed, "rows_added": added, "rows_skipped": skipped, "rows_failed": 0, "total_lines": total_lines, "offset": offset + processed}
