#!/usr/bin/env python3
"""
Train ML models for pubmed-explorer
"""
import argparse
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

def main():
    parser = argparse.ArgumentParser(description="Train PubMed ML models")
    parser.add_argument("--sample-size", type=int, default=10000, help="Sample size for training")
    args = parser.parse_args()
    print(f"Training with sample size: {args.sample_size}")
    # Placeholder - to be implemented

if __name__ == "__main__":
    main()
