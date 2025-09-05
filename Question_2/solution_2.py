# Analyse Australian weather station temperatures across multiple CSVs.

import os
import glob
import pandas as pd
import numpy as np

# ---- Constants ----
# List of months in order
MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]

# Map each month to a season
MONTH_TO_SEASON = {
    "December":"Summer","January":"Summer","February":"Summer",
    "March":"Autumn","April":"Autumn","May":"Autumn",
    "June":"Winter","July":"Winter","August":"Winter",
    "September":"Spring","October":"Spring","November":"Spring"
}

# Define seasons in the order we want to display them
SEASONS = ["Summer","Autumn","Winter","Spring"]

# ---- Setup paths ----
# Current script folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Subfolder where CSV files are stored
TEMP_DIR = os.path.join(BASE_DIR, "temperatures")

# ---- Load CSV files ----
files = sorted(glob.glob(os.path.join(TEMP_DIR, "*.csv")))
if not files:
    raise FileNotFoundError("No CSV files found!")

data = []
for f in files:
    df = pd.read_csv(f)

    # Only keep columns that are actual months
    months_present = [c for c in df.columns if c.strip() in MONTHS]

    # Convert month columns to numbers (ignore bad values)
    for c in months_present:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # Reshape from wide (Jan, Feb, ...) to long format (Month, Temp)
    long_df = df.melt(
        id_vars=[c for c in df.columns if c not in MONTHS],
        value_vars=months_present,
        var_name="Month",
        value_name="Temperature"
    )

    # Clean up month names (remove spaces)
    long_df["Month"] = long_df["Month"].str.strip()
    data.append(long_df)

# Combine all station data together
all_long = pd.concat(data, ignore_index=True)

# Drop rows with no temperature value
all_long = all_long.dropna(subset=["Temperature"])

# Add a "Season" column based on month
all_long["Season"] = all_long["Month"].map(MONTH_TO_SEASON)

# ---- Seasonal averages ----
season_avg = all_long.groupby("Season")["Temperature"].mean()
with open(os.path.join(BASE_DIR, "average_temp.txt"), "w") as f:
    for season in SEASONS:
        f.write(f"{season}: {season_avg.get(season, np.nan):.1f}°C\n")

# ---- Station temperature ranges ----
station_stats = all_long.groupby("STATION_NAME")["Temperature"].agg(['max','min'])
station_stats['range'] = station_stats['max'] - station_stats['min']

# Find station(s) with the largest temperature range
max_range = station_stats['range'].max()
with open(os.path.join(BASE_DIR, "largest_temp_range_station.txt"), "w") as f:
    for name, row in station_stats[station_stats['range']==max_range].sort_index().iterrows():
        f.write(f"{name}: Range {row['range']:.1f}°C (Max: {row['max']:.1f}°C, Min: {row['min']:.1f}°C)\n")

# ---- Temperature stability (std dev) ----
stds = all_long.groupby("STATION_NAME")["Temperature"].std()
min_std, max_std = stds.min(), stds.max()

# Write most stable and most variable stations
with open(os.path.join(BASE_DIR, "temperature_stability_stations.txt"), "w") as f:
    for name, val in stds[stds==min_std].sort_index().items():
        f.write(f"Most Stable: {name}: StdDev {val:.1f}°C\n")
    for name, val in stds[stds==max_std].sort_index().items():
        f.write(f"Most Variable: {name}: StdDev {val:.1f}°C\n")

print("Analysis complete. Files created in:", BASE_DIR)
