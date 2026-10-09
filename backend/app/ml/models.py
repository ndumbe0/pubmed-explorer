"""
ML utilities for pubmed-explorer
"""
import pickle
from pathlib import Path
from typing import Dict, Any

MODELS_DIR = Path(__file__).parent.parent.parent / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

def save_model(model: Any, name: str):
    path = MODELS_DIR / f"{name}.pkl"
    with open(path, 'wb') as f:
        pickle.dump(model, f)
    return str(path)

def load_model(name: str):
    path = MODELS_DIR / f"{name}.pkl"
    if not path.exists():
        raise FileNotFoundError(path)
    with open(path, 'rb') as f:
        return pickle.load(f)
