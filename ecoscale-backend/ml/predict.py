"""
Prediction Interface
--------------------
Loads trained models and provides:
- Utilization prediction
- Optimal CPU prediction
- Explainable AI (SHAP-based explanation)
"""

import joblib
import os
import pandas as pd
import shap

# ==========================
# MODEL PATHS
# ==========================

BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
UTIL_MODEL_PATH = os.path.join(BASE_DIR, "models", "utilization_model.pkl")
OPT_MODEL_PATH = os.path.join(BASE_DIR, "models", "optimization_model.pkl")

# ==========================
# LOAD MODELS
# ==========================

if not os.path.exists(UTIL_MODEL_PATH):
    raise FileNotFoundError(f"Utilization model not found at {UTIL_MODEL_PATH}. Train it first.")

if not os.path.exists(OPT_MODEL_PATH):
    raise FileNotFoundError(f"Optimization model not found at {OPT_MODEL_PATH}. Train it first.")

util_model = joblib.load(UTIL_MODEL_PATH)
opt_model = joblib.load(OPT_MODEL_PATH)

# ==========================
# PREDICTION FUNCTIONS
# ==========================

def predict_utilization(traffic: int, cpu: int, memory: int) -> float:
    """
    Predict CPU utilization (returns value between 0.05 and 0.95).
    """
    prediction = util_model.predict([[traffic, cpu, memory]])[0]
    return max(0.05, min(float(prediction), 0.95))


def predict_optimal_cpu(traffic: int, cpu: int, memory: int) -> int:
    """
    Predict optimal CPU allocation.
    """
    prediction = opt_model.predict([[traffic, cpu, memory]])[0]
    return max(1, int(round(prediction)))

# ==========================
# EXPLAINABLE AI SECTION
# ==========================

def explain_utilization(traffic: int, cpu: int, memory: int) -> dict:
    """
    Returns SHAP explanation for a single utilization prediction.
    Output format:
    {
        "traffic": shap_value,
        "cpu": shap_value,
        "memory": shap_value
    }
    """

    # Create input DataFrame
    X = pd.DataFrame([{
        "traffic": traffic,
        "cpu": cpu,
        "memory": memory
    }])

    # SHAP explainer for tree-based models
    explainer = shap.TreeExplainer(util_model)
    shap_values = explainer.shap_values(X)

    feature_names = ["traffic", "cpu", "memory"]

    explanation = {}
    for i, feature in enumerate(feature_names):
        explanation[feature] = float(shap_values[0][i])

    return explanation


def get_feature_importance() -> dict:
    """
    Returns global feature importance from RandomForest model.
    """
    if not hasattr(util_model, "feature_importances_"):
        return {}

    importances = util_model.feature_importances_
    feature_names = ["traffic", "cpu", "memory"]

    return dict(zip(feature_names, [float(i) for i in importances]))


def explain_optimal_cpu(traffic: int, cpu: int, memory: int) -> dict:
    """
    Returns SHAP explanation for optimal CPU prediction.
    Output format:
    {
        "traffic": shap_value,
        "cpu": shap_value,
        "memory": shap_value
    }
    """
    # Create input DataFrame
    X = pd.DataFrame([{
        "traffic": traffic,
        "cpu": cpu,
        "memory": memory
    }])

    # SHAP explainer for tree-based models
    explainer = shap.TreeExplainer(opt_model)
    shap_values = explainer.shap_values(X)

    feature_names = ["traffic", "cpu", "memory"]

    explanation = {}
    for i, feature in enumerate(feature_names):
        explanation[feature] = float(shap_values[0][i])

    return explanation

