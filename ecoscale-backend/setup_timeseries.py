"""
Complete Setup for Time-Series Forecasting
=====================================================
Run this script to generate datasets and train the model.

Steps:
1. Generate 30 days of historical hourly traffic data
2. Train Prophet model on the historical data
3. Ready to use in API!
"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))


def main():
    print("\n" + "=" * 70)
    print("EcoScale Time-Series Forecasting Setup")
    print("=" * 70 + "\n")
    
    # Step 1: Generate historical dataset
    print("[1/2] Generating historical traffic dataset...")
    print("-" * 70)
    try:
        from ml.timeseries_dataset_generator import generate_historical_traffic_dataset, save_dataset
        save_dataset()
    except Exception as e:
        print(f"❌ Error generating dataset: {e}")
        return False
    
    print("\n")
    
    # Step 2: Train time-series model
    print("[2/2] Training time-series forecast model...")
    print("-" * 70)
    try:
        from ml.train_timeseries_model import train_timeseries_model
        train_timeseries_model()
    except Exception as e:
        print(f"❌ Error training model: {e}")
        return False
    
    print("\n" + "=" * 70)
    print("✅ Setup Complete!")
    print("=" * 70)
    print("\nyou can now use the 24-hour traffic prediction in the API.")
    print("Start the API with: python main.py")
    print("\nAPI Endpoint: POST /api/predict")
    print("  Responses with 24-hour ML-predicted traffic patterns.\n")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

