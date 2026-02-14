"""
Train Time-Series Forecasting Model
------------------------------------
Trains a RandomForest model to predict hourly traffic multipliers (0.1 - 2.0)
based on time-of-day and day-of-week patterns.

Uses data from: timeseries_dataset_generator.py
Creates: models/timeseries_model.pkl
"""

import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import numpy as np


DATA_PATH = "data/historical_traffic_24h.csv"
MODEL_PATH = "models/timeseries_model.pkl"
BASE_TRAFFIC = 500  # Must match what timeseries_dataset_generator used


def train_timeseries_model():
    """Train forecasting model on historical traffic patterns."""
    
    # Load historical data from timeseries_dataset_generator
    if not os.path.exists(DATA_PATH):
        print(f"❌ Dataset not found at {DATA_PATH}")
        print("   Run: python ml/timeseries_dataset_generator.py")
        return
    
    df = pd.read_csv(DATA_PATH)
    
    print(f"Loaded {len(df)} hours of historical traffic data")
    print(f"Data columns: {list(df.columns)}\n")
    
    # Convert traffic values to multipliers (traffic / base_traffic)
    df["traffic_multiplier"] = df["traffic"] / BASE_TRAFFIC
    df["traffic_multiplier"] = np.clip(df["traffic_multiplier"], 0.1, 2.0)
    
    # Features: hour of day, day of week
    X = df[["hour", "day_of_week"]]
    # Target: traffic multiplier
    y = df["traffic_multiplier"]
    
    print(f"Training on {len(df)} samples...")
    print(f"Traffic multiplier range: {y.min():.3f} - {y.max():.3f}\n")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train RandomForest
    model = RandomForestRegressor(
        n_estimators=50,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    print("⏱️  Time-Series Model Performance:")
    print(f"   MSE: {mse:.4f}")
    print(f"   MAE: {mae:.4f}")
    print(f"   R² Score: {r2:.4f}\n")
    
    # Save model
    if not os.path.exists("models"):
        os.makedirs("models")
    
    joblib.dump(model, MODEL_PATH)
    print(f"✅ Time-series model saved at: {MODEL_PATH}")


if __name__ == "__main__":
    train_timeseries_model()

    