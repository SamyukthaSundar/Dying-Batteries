"""
Dataset Generator for EcoScale ML Models
-----------------------------------------
Generates synthetic but realistic cloud workload data.

Creates:
1. workload_dataset.csv  -> for utilization prediction
2. optimization_dataset.csv -> for optimal CPU prediction
"""

import numpy as np
import pandas as pd
import os


# ==============================
# CONFIGURATION
# ==============================

RANDOM_SEED = 42
NUM_ROWS = 1000000
DATA_FOLDER = "data"

np.random.seed(RANDOM_SEED)


# ==============================
# UTILIZATION DATASET
# ==============================

def generate_workload_dataset(rows=NUM_ROWS):
    """
    Generate dataset for utilization prediction.

    Features:
        traffic (requests/sec)
        cpu (allocated cores)
        memory (GB)
    Target:
        utilization (0–1)
    """

    traffic = np.random.randint(100, 5000, rows)
    cpu = np.random.randint(1, 16, rows)
    memory = np.random.randint(2, 64, rows)

    # Simulated realistic utilization formula
    # Higher traffic + lower CPU → higher utilization
    base_utilization = traffic / (cpu * 1200)

    noise = np.random.normal(0, 0.05, rows)

    utilization = base_utilization + noise
    utilization = np.clip(utilization, 0.05, 0.95)

    df = pd.DataFrame({
        "traffic": traffic,
        "cpu": cpu,
        "memory": memory,
        "utilization": utilization
    })

    return df


# ==============================
# OPTIMIZATION DATASET
# ==============================

def generate_optimization_dataset(rows=NUM_ROWS):
    """
    Generate dataset for optimal CPU prediction.

    Features:
        traffic
        cpu
        memory
    Target:
        optimal_cpu (with realistic noise and variance)
    """

    traffic = np.random.randint(100, 5000, rows)
    cpu = np.random.randint(1, 16, rows)
    memory = np.random.randint(2, 64, rows)

    # Base optimal CPU estimation
    optimal_cpu = np.ceil(traffic / 1200).astype(float)

    # Add memory influence
    optimal_cpu += (memory / 64.0)

    # Add realistic variability:
    # 1. Different teams/environments make different choices
    # 2. Sometimes over-provision for safety (cost > performance)
    # 3. Sometimes under-provision for cost savings
    variability = np.random.normal(0, 0.3, rows)  # ±0.3 cores variability
    optimal_cpu += variability

    # Add interaction noise (not purely linear)
    interaction_noise = (traffic / 5000) * np.random.normal(0, 0.15, rows)
    optimal_cpu += interaction_noise

    # Clip to valid range
    optimal_cpu = np.clip(optimal_cpu, 1, 16)
    optimal_cpu = np.round(optimal_cpu, 1)  # Realistic fractional cores

    df = pd.DataFrame({
        "traffic": traffic,
        "cpu": cpu,
        "memory": memory,
        "optimal_cpu": optimal_cpu
    })

    return df


# ==============================
# SAVE DATASETS
# ==============================

def save_datasets():

    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    workload_df = generate_workload_dataset()
    optimization_df = generate_optimization_dataset()

    workload_path = os.path.join(DATA_FOLDER, "workload_dataset.csv")
    optimization_path = os.path.join(DATA_FOLDER, "optimization_dataset.csv")

    workload_df.to_csv(workload_path, index=False)
    optimization_df.to_csv(optimization_path, index=False)

    print("✅ Workload dataset saved at:", workload_path)
    print("✅ Optimization dataset saved at:", optimization_path)


# ==============================
# MAIN EXECUTION
# ==============================

if __name__ == "__main__":
    save_datasets()