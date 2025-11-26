# Models - ML Artifacts & Embeddings

Machine learning artifacts for semantic search, embeddings, and advanced AI features.

## Purpose

This directory will contain:
- Character/zone embeddings for semantic similarity
- Trained models for photo classification
- Vector indices for fast search
- Synthetic data generation tools

## Status

**🔄 Placeholder - Future Development**

Currently, GLUTCHDEXMALL uses:
- Rule-based systems (v4 Cloud logic)
- Structured schemas (spynt, mallOS)
- Manual classification (v5 CRD workflow)

Future ML enhancements may include:
- Vision models fine-tuned on Eastland photos
- Character behavior prediction from spine data
- Automated CRD classification
- Zone similarity clustering

## Planned Structure

```
models/
├── embeddings/
│   ├── zone_embeddings.npy
│   ├── character_embeddings.npy
│   └── photo_embeddings.npy
│
├── classifiers/
│   ├── photo_primary_class.pkl
│   ├── feature_extractor.pkl
│   └── stereo_pair_matcher.pkl
│
├── generators/
│   ├── character_spine_gen.pkl
│   ├── crowd_behavior_gen.pkl
│   └── zone_population_gen.pkl
│
└── indices/
    ├── photo_search.faiss
    ├── character_search.faiss
    └── zone_search.faiss
```

## Integration

When implemented, models will:
- Accelerate `pipelines/photo_processing/`
- Enhance `ai/spynt/` character generation
- Power semantic search in `v6-nextgen/src/`

## Principles

Even with ML:
1. **Reconstruction > Hallucination** - Train on evidence, not synthetic data
2. **Metrology First** - Models must respect escalator calibration
3. **Explainable** - Black box outputs must be validated against CRD
4. **Optional** - Core systems must work without models

---

*Models augment, they don't replace, human reconstruction.*
