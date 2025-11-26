# Pipelines - Automation & Integration

GitHub Actions, Collab notebooks, and automation scripts for AI-native workflows.

## Purpose

Automation tooling for:
- Photo classification and CRD batch processing
- Schema validation (spynt, mallOS, canon)
- Testing and CI/CD
- Collaboration workflows (Jupyter, Collab)

## Structure

```
pipelines/
├── github_actions/
│   ├── validate_schemas.yml
│   ├── test_simulation.yml
│   └── build_docs.yml
│
├── photo_processing/
│   ├── batch_classify.py
│   ├── extract_exif.py
│   └── stereo_pair_detection.py
│
├── validation/
│   ├── validate_spynt.py
│   ├── validate_zones.py
│   └── check_measurements.py
│
├── collab_notebooks/
│   ├── CRD_Photo_Classification.ipynb
│   ├── Zone_Graph_Builder.ipynb
│   └── Character_Spine_Editor.ipynb
│
└── utilities/
    ├── import_from_v5.py
    ├── export_to_json.py
    └── sync_canon.py
```

## GitHub Actions

### Schema Validation
Runs on every PR:
- Validates all JSON schemas in `ai/spynt/`, `ai/mallOS/`, `v6-nextgen/canon/`
- Checks for required fields, type correctness
- Verifies cross-references (character IDs, zone IDs, etc.)

### Measurement Checks
Ensures metrology consistency:
- Escalator standards (8" step height, 30° incline)
- Civic-scale dimensions (no 35-foot masts!)
- CRD measurement confidence levels

### Documentation Build
Auto-generates:
- API docs from source
- Canon index from `v6-nextgen/canon/`
- Version matrix updates

## Photo Processing

### Batch Classification (CRD Workflow)
```python
python pipelines/photo_processing/batch_classify.py \
  --input v6-nextgen/assets/photos/raw/ \
  --output ai/classification_results.csv \
  --mode PRIMARY_CLASS
```

Classifies photos into:
- ATRIUM, CORRIDOR, FOOD_COURT, ANCHOR, EXTERIOR, etc.
- With FEATURE and ZONE annotations
- Outputs CRD-compatible CSV

### EXIF Extraction
```python
python pipelines/photo_processing/extract_exif.py \
  --input v6-nextgen/assets/photos/ \
  --output metadata.json
```

Extracts:
- Date taken (for timeline placement)
- Camera model (for perspective calibration)
- Geolocation (if available)

### Stereo Pair Detection
Identifies photos taken from similar angles for depth estimation:
```python
python pipelines/photo_processing/stereo_pair_detection.py \
  --threshold 0.85 \
  --output stereo_pairs.json
```

## Validation Scripts

### Spynt Validator
```python
python pipelines/validation/validate_spynt.py
```
Checks:
- Schema compliance
- Required fields present
- Valid era tags (1981, 1995, 2005, 2011)
- Referenced photo IDs exist

### Zone Validator
```python
python pipelines/validation/validate_zones.py
```
Checks:
- Zone graph connectivity
- Measurement references to v5 CRD
- Cooldown rule consistency

## Collab Notebooks

### CRD Photo Classification
Interactive notebook for:
- Viewing photos in batches
- Assigning PRIMARY_CLASS
- Extracting measurable FEATURES
- Building ZONE_GRAPH relationships

### Zone Graph Builder
Visual tool for:
- Mapping zone adjacencies
- Defining access points
- Setting population densities

### Character Spine Editor
GUI for creating/editing spynt schemas:
- Template-based character creation
- Relationship graph visualization
- Behavior weight tuning

## Usage

### Run All Validation
```bash
./pipelines/validate_all.sh
```

### Run Photo Batch Processing
```bash
./pipelines/process_photos.sh \
  --batch v6-nextgen/assets/photos/batch_2025_01/ \
  --output results/batch_2025_01.csv
```

---

*Automation enables reconstruction at scale.*
