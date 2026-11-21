import numpy as np
import pandas as pd

from jakarta_flood_risk.data import FEATURE_COLUMNS, build_sequences


def test_build_sequences_uses_only_preceding_years():
    rows = []
    for neighbourhood_id in (1, 2):
        for year in range(2016, 2025):
            row = {
                "neighbourhood_id": neighbourhood_id,
                "neighbourhood": f"N{neighbourhood_id}",
                "year": year,
                "flood_risk_index": float(year),
            }
            row.update({name: float(year) for name in FEATURE_COLUMNS})
            rows.append(row)

    result = build_sequences(pd.DataFrame(rows), lookback=3)

    assert result.features.shape == (12, 3, len(FEATURE_COLUMNS))
    assert result.targets.shape == (12,)
    assert result.metadata.iloc[0]["target_year"] == 2019
    np.testing.assert_array_equal(result.features[0, :, 0], [2016, 2017, 2018])
    assert result.targets[0] == 2019

