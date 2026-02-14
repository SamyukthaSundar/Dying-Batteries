"""
Time-Series Traffic Prediction
-------------------------------
Loads trained RandomForest model and predicts 24-hour traffic patterns.
Takes a base RPS and multiplies by the learned hourly patterns.
"""

import joblib
import os
from datetime import datetime, timedelta
from typing import List, Dict


BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_PATH = os.path.join(BASE_DIR, "models", "timeseries_model.pkl")


# Load model if available (won't fail if not yet trained)
timeseries_model = None
if os.path.exists(MODEL_PATH):
    timeseries_model = joblib.load(MODEL_PATH)


def predict_24h_traffic(base_rps: int) -> List[int]:
    """
    Predict traffic for next 24 hours using ML model.
    
    Args:
        base_rps (int): Current traffic level (requests/sec)
    
    Returns:
        List[int]: Predicted traffic for hours 0-23
    """
    
    if timeseries_model is None:
        # Fallback if model not trained yet
        return _fallback_24h_traffic(base_rps)
    
    predictions = []
    now = datetime.now()
    
    for h in range(24):
        future_time = now + timedelta(hours=h)
        hour_of_day = future_time.hour
        day_of_week = future_time.weekday()
        
        # Predict traffic multiplier (0.1 - 2.0)
        multiplier = timeseries_model.predict([[hour_of_day, day_of_week]])[0]
        multiplier = max(0.1, min(multiplier, 2.0))  # Bound it
        
        # Scale by base RPS
        traffic = max(0, int(base_rps * multiplier))
        predictions.append(traffic)
    
    return predictions


def predict_with_confidence(base_rps: int) -> List[Dict]:
    """
    Predict 24-hour traffic with confidence intervals.
    
    Returns:
        List of {"traffic": int, "lower": int, "upper": int}
    """
    
    traffic_list = predict_24h_traffic(base_rps)
    
    # Simple ±15% confidence intervals
    return [
        {
            "traffic": t,
            "lower": int(t * 0.85),
            "upper": int(t * 1.15)
        }
        for t in traffic_list
    ]


def _fallback_24h_traffic(base_rps: int) -> List[int]:
    """Hardcoded pattern when model not available."""
    import math
    
    predictions = []
    for h in range(24):
        # Sine wave peaking at 2 PM (hour 14)
        peak_factor = math.sin(((h - 6) / 24) * math.pi * 2) * 0.5 + 0.5
        noise = math.sin(h * 7.3) * 0.1
        multiplier = 0.3 + peak_factor * 0.7 + noise
        multiplier = max(0.1, min(multiplier, 2.0))
        
        traffic = int(base_rps * multiplier)
        predictions.append(max(0, traffic))
    
    return predictions
    
    future_df = pd.DataFrame({
        "ds": future_dates,
        "hour": hours,
        "is_weekend": is_weekends,
    })
    
    forecast = forecast_model.predict(future_df)
    
    predictions = []
    historical_mean = 500
    scale_factor = base_rps / historical_mean if historical_mean > 0 else 1
    
    for idx, row in forecast.iterrows():
        pred = max(0, int(row["yhat"] * scale_factor))
        lower = max(0, int(row["yhat_lower"] * scale_factor))
        upper = max(0, int(row["yhat_upper"] * scale_factor))
        
        predictions.append({
            "traffic": max(10, pred),
            "lower": max(10, lower),
            "upper": max(10, upper),
        })
    
    return predictions

