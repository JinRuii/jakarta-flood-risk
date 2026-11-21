"""CNN-LSTM model definition."""

from __future__ import annotations


def build_cnn_lstm(input_shape: tuple[int, int]):
    """Build a two-convolution, two-LSTM regression network."""
    try:
        import tensorflow as tf
    except ImportError as exc:  # pragma: no cover - depends on optional runtime
        raise RuntimeError("TensorFlow is required for model training") from exc

    inputs = tf.keras.Input(shape=input_shape, name="predictor_sequence")
    x = tf.keras.layers.Conv1D(64, 2, padding="same", activation="relu")(inputs)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Conv1D(64, 2, padding="same", activation="relu")(x)
    x = tf.keras.layers.Dropout(0.20)(x)
    x = tf.keras.layers.LSTM(64, return_sequences=True)(x)
    x = tf.keras.layers.Dropout(0.20)(x)
    x = tf.keras.layers.LSTM(32)(x)
    x = tf.keras.layers.Dense(32, activation="relu")(x)
    outputs = tf.keras.layers.Dense(1, name="scaled_fri")(x)

    model = tf.keras.Model(inputs=inputs, outputs=outputs, name="cnn_lstm_fri")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3, clipnorm=1.0),
        loss="mse",
        metrics=[tf.keras.metrics.RootMeanSquaredError(name="rmse")],
    )
    return model

