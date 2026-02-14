"""
Prediction Interface
--------------------
Loads trained models and provides clean prediction functions.
"""

import joblib
import os


UTIL_MODEL_PATH = "models/utilization_model.pkl"
OPT_MODEL_PATH = "models/optimization_model.pkl"


if not os.path.exists(UTIL_MODEL_PATH):
    raise FileNotFoundError("Utilization model not found. Train it first.")

if not os.path.exists(OPT_MODEL_PATH):
    raise FileNotFoundError("Optimization model not found. Train it first.")


util_model = joblib.load(UTIL_MODEL_PATH)
opt_model = joblib.load(OPT_MODEL_PATH)


def predict_utilization(traffic: int, cpu: int, memory: int) -> float:

    prediction = util_model.predict([[traffic, cpu, memory]])[0]

    return max(0.05, min(prediction, 0.95))


def predict_optimal_cpu(traffic: int, cpu: int, memory: int) -> int:

    prediction = opt_model.predict([[traffic, cpu, memory]])[0]

    return max(1, int(round(prediction)))
