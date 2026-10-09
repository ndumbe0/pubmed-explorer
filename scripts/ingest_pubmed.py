#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.database import SessionLocal, apply_pragmas
from app.utils.ingest import ingest_full_streaming

def main():
    parser = argparse.ArgumentParser(description="Ingest PubMed CSV")
    parser.add_argument("--file", default=str(Path(__file__).parent.parent / "data" / "key_pubmed.csv"))
    parser.add_argument("--resume", action="store_true", default=True)
    parser.add_argument("--no-resume", dest="resume", action="store_false")
    parser.add_argument("--test-limit", type=int, default=None)
    args = parser.parse_args()
    
    apply_pragmas()
    db = SessionLocal()
    try:
        res = ingest_full_streaming(db, args.file, resume=args.resume, test_limit=args.test_limit)
        print(res)
    finally:
        db.close()

if __name__ == "__main__":
    main()
