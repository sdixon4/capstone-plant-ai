# simulate_data.py

# Simulation duration and frequency

hours = 72
interval_minutes = 5

# Total number of samples

num_samples = int((hours * 60) / interval_minutes)
print("Total data points:", num_samples)

from datetime import datetime, timedelta

# Create list of timestamps starting from now
start_time = datetime.now()
timestamps = [start_time + timedelta(minutes=i * interval_minutes) for i in range(num_samples)]

# Print the first 5 timestamps to check
for t in timestamps[:5]:
    print(t)


import numpy as np

# Temperature signal generator
def simulate_temperature(i):
    # Smooth daily fluctuation
    base = 23 + 5 * np.sin(i / 50)

    # Inject heat stress between i=500–600
    if 500 < i < 600:
        return base + 10 + np.random.normal(0, 0.5)

    # Normal operation with noise
    return base + np.random.normal(0, 0.2)

# Generate temperature values
temps = [simulate_temperature(i) for i in range(num_samples)]

# Print the first 5 temperatures
print("\nSample temperatures:")
for t in temps[:5]:
    print(f"{t:.2f} °C")

# Moisture signal generator
def simulate_moisture(i):
    base = 60 + 10 * np.sin(i / 80)
    if 1000 < i < 1100:  # Dry-out period
        return base - 25 + np.random.normal(0, 1.0)
    return base + np.random.normal(0, 0.5)

# CO₂ signal generator
def simulate_co2(i):
    return 400 + 20 * np.sin(i / 70) + np.random.normal(0, 5)

# Light signal generator (on/off cycle)
def simulate_light(i):
    cycle = (i % 288)  # 288 = 24 hrs @ 5-min intervals
    if cycle < 60:
        return 0  # Lights off
    return 500 + 100 * np.sin((cycle - 60) / 50)

moisture = [simulate_moisture(i) for i in range(num_samples)]
co2 = [simulate_co2(i) for i in range(num_samples)]
light = [simulate_light(i) for i in range(num_samples)]

# Print samples
print("\nSample moisture (%):", [f"{m:.1f}" for m in moisture[:5]])
print("Sample CO2 (ppm):", [f"{c:.0f}" for c in co2[:5]])
print("Sample light (lux):", [f"{l:.0f}" for l in light[:5]])

import pandas as pd

# Build dataset row-by-row
data = []
for i in range(num_samples):
    row = {
        "timestamp": timestamps[i],
        "temp_C": round(temps[i], 2),
        "moisture_pct": round(moisture[i], 1),
        "co2_ppm": round(co2[i], 0),
        "light_lux": round(light[i], 0),
    }
    data.append(row)

# Convert to DataFrame
df = pd.DataFrame(data)

# Print the first few rows
print("\nPreview of combined data:")
print(df.head())

# Define fallback logic
def check_fallback(temp, moisture):
    return temp > 35 and moisture < 40

# Apply fallback flag
df["fallback_active"] = df.apply(
    lambda row: check_fallback(row["temp_C"], row["moisture_pct"]),
    axis=1
)

# Preview fallback rows only
print("\nFallback-triggered rows:")
print(df[df["fallback_active"]].head())

# Save as CSV
df.to_csv("simulated_sensor_data.csv", index=False)
print("\nData saved to simulated_sensor_data.csv ✅")

