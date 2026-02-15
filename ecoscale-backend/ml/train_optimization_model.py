"""
Train Optimization Model
------------------------
Predicts optimal CPU allocation based on:
- traffic
- cpu
- memory
"""

import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


DATA_PATH = "data/optimization_dataset.csv"
MODEL_PATH = "models/optimization_model.pkl"


def train_optimization_model():

    df = pd.read_csv(DATA_PATH)
    # Remove exact duplicate rows to avoid data leakage between train/test
    dup_count = len(df) - len(df.drop_duplicates())
    if dup_count > 0:
        print(f"Found and removing {dup_count} duplicate rows from dataset (prevents leakage)")
        df = df.drop_duplicates()

    X = df[["traffic", "cpu", "memory"]]
    y = df["optimal_cpu"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print("Optimization Model Performance:")
    print("MSE:", round(mse, 4))
    print("R2 Score:", round(r2, 4))

    if not os.path.exists("models"):
        os.makedirs("models")

    joblib.dump(model, MODEL_PATH)

    print("✅ Optimization model saved at:", MODEL_PATH)


if __name__ == "__main__":
    train_optimization_model()


