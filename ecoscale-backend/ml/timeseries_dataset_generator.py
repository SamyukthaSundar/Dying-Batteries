"""
Historical Traffic Dataset Generator for Time-Series Forecasting
------------------------------------------------------------------
Generates 30 days of hourly traffic data with realistic patterns:
- Peak hours: 8 AM - 8 PM (80-100% of daily peak)
- Off-peak hours: 8 PM - 8 AM (20-40% of daily peak)
- Weekday vs weekend variation
- Random noise for realism
"""

import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta


def generate_historical_traffic_dataset(days=30, base_rps=500, seed=42):
    """
    Generate realistic hourly traffic for the past N days.
    
    Args:
        days: Number of days to generate (default 30)
        base_rps: Base traffic level (requests/sec)
        seed: Random seed for reproducibility
    
    Returns:
        DataFrame with columns: timestamp, hour, day_of_week, traffic
    """
    
    np.random.seed(seed)
    
    data = []
    start_date = datetime.now() - timedelta(days=days)
    
    for day_offset in range(days):
        current_date = start_date + timedelta(days=day_offset)
        day_of_week = current_date.weekday()  # 0=Monday, 6=Sunday
        is_weekend = day_of_week >= 5
        
        # Weekend traffic is 40% of weekday on average
        weekday_multiplier = 0.6 if is_weekend else 1.0
        
        for hour in range(24):
            # Realistic traffic pattern across 24h
            if 8 <= hour <= 20:  # 8 AM - 8 PM: Peak business hours
                base_pattern = 0.7 + 0.3 * np.sin((hour - 8) / 12 * np.pi)
            elif 6 <= hour < 8:  # 6-8 AM: Morning ramp-up
                base_pattern = 0.2 + (hour - 6) * 0.25
            elif 20 <= hour < 22:  # 8-10 PM: Evening ramp-down
                base_pattern = 0.5 - (hour - 20) * 0.15
            else:  # 10 PM - 6 AM: Night minimum
                base_pattern = 0.15
            
            # Add some random variation (±15%)
            noise = np.random.normal(1.0, 0.15)
            noise = np.clip(noise, 0.7, 1.3)  # Keep within bounds
            
            traffic = int(base_rps * base_pattern * weekday_multiplier * noise)
            traffic = max(10, traffic)  # Never go to zero
            
            data.append({
                "timestamp": current_date.strftime("%Y-%m-%d") + f" {hour:02d}:00",
                "hour": hour,
                "day_of_week": day_of_week,
                "is_weekend": 1 if is_weekend else 0,
                "traffic": traffic,
            })
    
    df = pd.DataFrame(data)
    return df


def save_dataset():
    """Generate and save the historical traffic dataset."""
    
    data_folder = "data"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    
    # Generate dataset
    df = generate_historical_traffic_dataset(days=30, base_rps=500)
    
    # Save to CSV
    output_path = os.path.join(data_folder, "historical_traffic_24h.csv")
    df.to_csv(output_path, index=False)
    
    print(f"✅ Historical traffic dataset saved at: {output_path}")
    print(f"   Generated {len(df)} hours of data ({len(df) // 24} days)")
    print(f"\nDataset preview:")
    print(df.head(24))  # Show first day (24 hours)
    print(f"\nStatistics:")
    print(f"  Min traffic: {df['traffic'].min()} RPS")
    print(f"  Max traffic: {df['traffic'].max()} RPS")
    print(f"  Mean traffic: {df['traffic'].mean():.0f} RPS")


if __name__ == "__main__":
    save_dataset()

