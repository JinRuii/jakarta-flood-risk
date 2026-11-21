"""Load the tidy panel and create leakage-aware temporal sequences."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


ID_COLUMNS = ["neighbourhood_id", "neighbourhood", "year"]
FEATURE_COLUMNS = [
    "elevation",
    "distance_to_river",
    "drainage_capacity",
    "pump_capacity",
    "building_area",
    "rainfall",
    "population_density",
    "vegetation_cover",
    "ndwi",
    "ndbi",
    "land_subsidence_index",
]
TARGET_COLUMN = "flood_risk_index"


@dataclass(frozen=True)
class SequenceDataset:
    """Model-ready temporal sequences and their target metadata."""

    features: np.ndarray
    targets: np.ndarray
    metadata: pd.DataFrame


def load_panel(path: str | Path) -> pd.DataFrame:
    """Load and validate the neighbourhood-year panel."""
    panel = pd.read_csv(path)
    required = set(ID_COLUMNS + FEATURE_COLUMNS + [TARGET_COLUMN])
    missing_columns = sorted(required.difference(panel.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if panel[list(required)].isna().any().any():
        missing = panel[list(required)].isna().sum()
        raise ValueError(f"Required data contain missing values: {missing[missing > 0].to_dict()}")

    if panel.duplicated(["neighbourhood_id", "year"]).any():
        raise ValueError("Each neighbourhood-year key must be unique")

    return panel.sort_values(["neighbourhood_id", "year"]).reset_index(drop=True)


def build_sequences(panel: pd.DataFrame, lookback: int = 3) -> SequenceDataset:
    """Use preceding years to predict the following year's FRI.

    The target year's predictors are never placed in its input sequence.
    """
    if lookback < 2:
        raise ValueError("lookback must be at least 2")

    sequences: list[np.ndarray] = []
    targets: list[float] = []
    records: list[dict[str, object]] = []

    for neighbourhood_id, group in panel.groupby("neighbourhood_id", sort=True):
        group = group.sort_values("year").reset_index(drop=True)
        years = group["year"].to_numpy()
        if not np.all(np.diff(years) == 1):
            raise ValueError(f"Non-consecutive years for neighbourhood {neighbourhood_id}")

        values = group[FEATURE_COLUMNS].to_numpy(dtype=np.float32)
        target_values = group[TARGET_COLUMN].to_numpy(dtype=np.float32)
        for target_index in range(lookback, len(group)):
            sequences.append(values[target_index - lookback : target_index])
            targets.append(float(target_values[target_index]))
            records.append(
                {
                    "neighbourhood_id": neighbourhood_id,
                    "neighbourhood": group.loc[target_index, "neighbourhood"],
                    "target_year": int(years[target_index]),
                }
            )

    if not sequences:
        raise ValueError("No sequences could be created from the supplied panel")

    return SequenceDataset(
        features=np.stack(sequences),
        targets=np.asarray(targets, dtype=np.float32),
        metadata=pd.DataFrame.from_records(records),
    )

