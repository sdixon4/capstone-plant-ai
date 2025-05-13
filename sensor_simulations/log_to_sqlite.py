import sqlite3
import pandas as pd
import zlib
from datetime import datetime

# Load fallback data (assumes df and fallback_log already generated)
df = pd.read_csv("simulated_sensor_data.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Load fallback reasons
def get_fallback_reason(temp, moisture, co2, light):
    reasons = []
    if temp > 35: reasons.append("high_temp")
    if moisture < 40: reasons.append("low_moisture")
    if pd.isna(moisture): reasons.append("moisture_dropout")
    if co2 > 800: reasons.append("co2_noise")
    return reasons

# Connect to SQLite
conn = sqlite3.connect("fallback_events.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS fallback_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    reasons TEXT,
    fallback_active INTEGER,
    crc TEXT
)
""")

# Insert fallback events with CRC
for _, row in df.iterrows():
    reasons = get_fallback_reason(row["temp_C"], row["moisture_pct"], row["co2_ppm"], row["light_lux"])
    if reasons:
        ts = row["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        reasons_str = ", ".join(reasons)
        fallback_flag = 1

        # Create CRC checksum of the message
        raw_string = f"{ts}:{reasons_str}:{fallback_flag}"
        crc = format(zlib.crc32(raw_string.encode()), '08x')

        cursor.execute("""
            INSERT INTO fallback_events (timestamp, reasons, fallback_active, crc)
            VALUES (?, ?, ?, ?)
        """, (ts, reasons_str, fallback_flag, crc))

# Commit and close
conn.commit()
conn.close()

print("✅ fallback_events.db created with CRC-protected entries.")

