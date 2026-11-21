# Interpretable CNN–LSTM flood-risk modelling for Jakarta

This repository contains preprocessing notebooks and a cleaned reference implementation of a CNN–LSTM workflow for modelling Jakarta's Flood Risk Index (FRI). The study combines hydrological, infrastructure, built-environment, demographic, and ecological indicators for 261 neighbourhoods.

## Repository contents

```text
docs/              Data dictionary
notebooks/         Source-data preprocessing notebooks with outputs removed
src/               Reusable data validation and CNN–LSTM training code
tests/             Lightweight tests for sequence construction
```

The study datasets are excluded from this repository. The [data dictionary](docs/data_dictionary.md) documents the expected inputs.

## Installation

Python 3.10 or 3.11 is recommended.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

With a local copy of the study inputs, place the panel and forecast CSV files in `data/processed/` under your input directory and validate them:

```bash
python -m jakarta_flood_risk.validate_data --root /path/to/input-directory
```

Run the reference training workflow:

```bash
python -m jakarta_flood_risk.train \
  --data /path/to/input-directory/data/processed/jakarta_neighbourhood_panel_2016_2024.csv \
  --output outputs/reference_run
```

The training script uses three preceding years to predict the following year's FRI. Samples with target years through 2022 are used for training, 2023 for validation, and 2024 for testing. Feature and target scalers are fit only on the training split.

## Notebooks

The notebooks are retained as provenance for two upstream workflows:

1. joining socioeconomic data to neighbourhood boundaries;
2. deriving impervious-surface information with ENDISI from Sentinel-2 imagery.

Notebook outputs and execution counters were removed to reduce repository size. The ENDISI notebook accesses external satellite data and therefore requires network access and the services used in the original workflow.

## Citation

Use the project metadata in `CITATION.cff` when citing this repository.
