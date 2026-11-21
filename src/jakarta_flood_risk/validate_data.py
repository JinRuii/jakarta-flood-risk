"""Run structural checks on the repository's processed CSV files."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from .data import load_panel


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    data_dir = args.root / "data" / "processed"
    panel = load_panel(data_dir / "jakarta_neighbourhood_panel_2016_2024.csv")
    forecast = pd.read_csv(data_dir / "jakarta_fri_forecast_2025_2045.csv")

    if len(panel) != 2_349 or panel["neighbourhood_id"].nunique() != 261:
        raise ValueError("Panel must contain 261 neighbourhoods and 2,349 rows")
    if set(panel["year"]) != set(range(2016, 2025)):
        raise ValueError("Panel years must span 2016–2024")
    if forecast.isna().any().any():
        raise ValueError("Forecast table contains missing values")
    if forecast.duplicated(["neighbourhood", "year"]).any():
        raise ValueError("Forecast neighbourhood-year keys must be unique")
    if len(forecast) != 5_481 or forecast["neighbourhood"].nunique() != 261:
        raise ValueError("Forecast must contain 261 neighbourhoods and 5,481 rows")
    if set(forecast["year"]) != set(range(2025, 2046)):
        raise ValueError("Forecast years must span 2025–2045")

    print("Data validation passed: 261 neighbourhoods, 2016–2024 panel, 2025–2045 forecast.")


if __name__ == "__main__":
    main()

