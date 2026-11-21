"""Train and evaluate the reference CNN-LSTM model."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

import numpy as np
import pandas as pd

from .data import FEATURE_COLUMNS, build_sequences, load_panel
from .model import build_cnn_lstm


def _metrics(actual: np.ndarray, predicted: np.ndarray) -> dict[str, float]:
    residual = actual - predicted
    mse = float(np.mean(residual**2))
    return {
        "mae": float(np.mean(np.abs(residual))),
        "mse": mse,
        "rmse": float(np.sqrt(mse)),
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("outputs/reference_run"))
    parser.add_argument("--lookback", type=int, default=3)
    parser.add_argument("--epochs", type=int, default=200)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    random.seed(args.seed)
    np.random.seed(args.seed)

    import tensorflow as tf

    tf.keras.utils.set_random_seed(args.seed)
    try:
        tf.config.experimental.enable_op_determinism()
    except Exception:
        pass

    dataset = build_sequences(load_panel(args.data), lookback=args.lookback)
    years = dataset.metadata["target_year"].to_numpy()
    split_masks = {
        "train": years <= 2022,
        "validation": years == 2023,
        "test": years == 2024,
    }
    if any(not mask.any() for mask in split_masks.values()):
        raise ValueError("Expected training years through 2022, validation 2023, and test 2024")

    train_x = dataset.features[split_masks["train"]]
    feature_mean = train_x.mean(axis=(0, 1), keepdims=True)
    feature_std = train_x.std(axis=(0, 1), keepdims=True)
    feature_std[feature_std == 0] = 1.0

    train_y = dataset.targets[split_masks["train"]]
    target_mean = float(train_y.mean())
    target_std = float(train_y.std()) or 1.0

    scaled_x = (dataset.features - feature_mean) / feature_std
    scaled_y = (dataset.targets - target_mean) / target_std

    model = build_cnn_lstm((args.lookback, len(FEATURE_COLUMNS)))
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss", patience=15, restore_best_weights=True
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss", factor=0.5, patience=7, min_lr=1e-6
        ),
    ]
    history = model.fit(
        scaled_x[split_masks["train"]],
        scaled_y[split_masks["train"]],
        validation_data=(
            scaled_x[split_masks["validation"]],
            scaled_y[split_masks["validation"]],
        ),
        epochs=args.epochs,
        batch_size=args.batch_size,
        callbacks=callbacks,
        verbose=2,
        shuffle=True,
    )

    args.output.mkdir(parents=True, exist_ok=True)
    model.save(args.output / "reference_cnn_lstm.keras")
    np.savez(
        args.output / "scalers.npz",
        feature_mean=feature_mean,
        feature_std=feature_std,
        target_mean=target_mean,
        target_std=target_std,
    )
    pd.DataFrame(history.history).to_csv(args.output / "training_history.csv", index=False)

    results: dict[str, dict[str, float]] = {}
    for name, mask in split_masks.items():
        scaled_prediction = model.predict(scaled_x[mask], verbose=0).reshape(-1)
        prediction = scaled_prediction * target_std + target_mean
        results[name] = _metrics(dataset.targets[mask], prediction)

    (args.output / "metrics.json").write_text(
        json.dumps(results, indent=2) + "\n", encoding="utf-8"
    )
    run_metadata = {
        "data": str(args.data),
        "lookback": args.lookback,
        "seed": args.seed,
        "features": FEATURE_COLUMNS,
        "split": {"train": "target year <= 2022", "validation": 2023, "test": 2024},
    }
    (args.output / "run_metadata.json").write_text(
        json.dumps(run_metadata, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
