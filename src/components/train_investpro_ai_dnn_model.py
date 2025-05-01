import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os


def generate_fake_candles(n):
    candles = []
    np.random.seed(42)
    for _ in range(n):
        open_price = np.random.uniform(29000, 31000)
        close_price = open_price + np.random.uniform(-200, 200)
        high_price = max(open_price, close_price) + np.random.uniform(0, 100)
        low_price = min(open_price, close_price) - np.random.uniform(0, 100)
        volume = np.random.uniform(1000, 5000)
        candles.append([open_price, close_price, high_price, low_price, volume])
    return pd.DataFrame(candles, columns=["open", "close", "high", "low", "volume"])


def add_features(df):
    df["body_size"] = np.abs(df["close"] - df["open"])
    df["range"] = df["high"] - df["low"]
    df["ema_12"] = df["close"].ewm(span=12, adjust=False).mean()
    df["ema_26"] = df["close"].ewm(span=26, adjust=False).mean()
    df["macd"] = df["ema_12"] - df["ema_26"]

    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))

    return df.dropna()


def add_labels(df):
    df["future_close"] = df["close"].shift(-1)
    df["label"] = np.where(df["future_close"] > df["close"], 1, 0)
    return df.dropna()


def train_dnn(output_dir="."):
    print("🚀 Starting training...")

    df = generate_fake_candles(5000)
    df = add_features(df)
    df = add_labels(df)

    features = [
        "close",
        "open",
        "high",
        "low",
        "volume",
        "body_size",
        "range",
        "ema_12",
        "ema_26",
        "rsi",
        "macd",
    ]
    X = df[features]
    y = df["label"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Dense(
                64, activation="relu", input_shape=(X_train.shape[1],)
            ),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dense(1, activation="sigmoid"),
        ]
    )

    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    history = model.fit(
        X_train, y_train, epochs=30, batch_size=32, validation_split=0.1, verbose=0
    )

    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"✅ DNN Model Accuracy: {accuracy * 100:.2f}%")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    model.save(os.path.join(output_dir, "investpro_ai_dnn_model.h5"))
    joblib.dump(scaler, os.path.join(output_dir, "investpro_scaler.pkl"))

    print(f"✅ Model and scaler saved in {output_dir}")


