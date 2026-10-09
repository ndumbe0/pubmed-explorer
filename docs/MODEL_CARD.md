# Model Card - PubMed Explorer

## Overview
PubMed Explorer uses machine learning models for:
- TF-IDF/semantic similar-paper recommendations
- Topic modeling/clustering of abstracts with topic explorer
- Classifier predicting topic/journal group from title+abstract
- Publication-trend analysis per keyword

## Training Approach
- Proper train/validation/test splits
- Cross-validation where applicable
- Baseline model to beat
- Metrics documented honestly
- Models saved under `models/` (large artifacts gitignored)

## Data
- Dataset: key_pubmed.csv
- Training performed on sampled subset sized for laptop compatibility
- Sample size configurable via scripts/train.py

## Limitations
- Training on sampled data for performance on consumer hardware
- Small sample sizes may affect model quality
