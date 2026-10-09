import re
import hashlib
from typing import Any, Optional
import json

def normalize_text(s: Any) -> str:
    if s is None: return ""
    t = str(s).strip().lower()
    t = re.sub(r'\s+', ' ', t)
    return t

def compute_hash(title: str, year: Any, journal: str, doi: str = "") -> str:
    if doi and str(doi).strip():
        return hashlib.sha256(str(doi).strip().lower().encode()).hexdigest()
    base = f"{normalize_text(title)}|{year or ''}|{normalize_text(journal)}"
    return hashlib.sha256(base.encode()).hexdigest()

def parse_authors(s: Any):
    if s is None or s == "": return []
    if isinstance(s, list): return [str(x).strip() for x in s]
    t = str(s).strip()
    try:
        if t.startswith('['): 
            arr = json.loads(t)
            return [str(x).strip() for x in arr if str(x).strip()]
    except: pass
    # simple split
    return [x.strip() for x in t.split(';') if x.strip()]

def parse_keywords(s: Any):
    return parse_authors(s)
