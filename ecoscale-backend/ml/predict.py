"""
Prediction Interface
--------------------
Loads trained models and provides clean prediction functions.
"""

import joblib
import os


BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
UTIL_MODEL_PATH = os.path.join(BASE_DIR, "models", "utilization_model.pkl")
OPT_MODEL_PATH = os.path.join(BASE_DIR, "models", "optimization_model.pkl")


if not os.path.exists(UTIL_MODEL_PATH):
    raise FileNotFoundError(f"Utilization model not found at {UTIL_MODEL_PATH}. Train it first.")

if not os.path.exists(OPT_MODEL_PATH):
    raise FileNotFoundError(f"Optimization model not found at {OPT_MODEL_PATH}. Train it first.")


util_model = joblib.load(UTIL_MODEL_PATH)
opt_model = joblib.load(OPT_MODEL_PATH)


def predict_utilization(traffic: int, cpu: int, memory: int) -> float:

    prediction = util_model.predict([[traffic, cpu, memory]])[0]

    return max(0.05, min(prediction, 0.95))


def predict_optimal_cpu(traffic: int, cpu: int, memory: int) -> int:

    prediction = opt_model.predict([[traffic, cpu, memory]])[0]

    return max(1, int(round(prediction)))
