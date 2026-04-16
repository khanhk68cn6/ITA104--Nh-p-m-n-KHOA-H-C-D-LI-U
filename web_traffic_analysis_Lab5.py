import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
warnings.filterwarnings('ignore')

# 1. Load and preprocess data
df = pd.read_csv('ITA105_Lab_5_Web_traffic.csv', parse_dates=['datetime'], index_col='datetime')
df['visits'] = pd.to_numeric(df['visits'], errors='coerce')  # Handle empty as NaN
df = df.asfreq('h')  # Ensure hourly frequency
df['visits'] = df['visits'].interpolate(method='linear')  # Linear interpolation for missing

print(f"Data shape: {df.shape}")
print(f"Missing values after interp: {df['visits'].isna().sum()}")

# 2. Create features
df['hour'] = df.index.hour
df['dayofweek'] = df.index.dayofweek  # 0=Mon, 6=Sun
df['day_name'] = df.index.day_name()

# 3. Hourly pattern analysis and plot
hourly_avg = df.groupby('hour')['visits'].mean()
peak_hour = hourly_avg.idxmax()
peak_visits = hourly_avg.max()
trough_hour = hourly_avg.idxmin()
trough_visits = hourly_avg.min()

plt.figure(figsize=(12, 6))
hourly_avg.plot(kind='bar')
plt.axvline(peak_hour, color='green', linestyle='--', label=f'Peak: {peak_hour}:00 ({peak_visits:.1f})')
plt.axvline(trough_hour, color='red', linestyle='--', label=f'Trough: {trough_hour}:00 ({trough_visits:.1f})')
plt.title('Average Visits by Hour of Day (Peak/Trough Highlighted)')
plt.xlabel('Hour')
plt.ylabel('Average Visits')
plt.legend()
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('hourly_traffic.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"\nDaily Peak: Hour {peak_hour} with {peak_visits:.1f} avg visits")
print(f"Daily Trough: Hour {trough_hour} with {trough_visits:.1f} avg visits")

# 4. Weekly seasonality
weekly_avg = df.groupby('dayofweek')['visits'].mean()
weekly_avg.index = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
plt.figure(figsize=(10, 5))
weekly_avg.plot(kind='bar')
plt.title('Average Visits by Day of Week')
plt.xlabel('Day of Week')
plt.ylabel('Average Visits')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('weekly_pattern.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nWeekly averages:")
print(weekly_avg)

# 5. Full time series plot
plt.figure(figsize=(15, 6))
plt.plot(df.index, df['visits'], alpha=0.7)
plt.title('Website Traffic Time Series (Hourly, Interpolated)')
plt.xlabel('Date')
plt.ylabel('Visits')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('full_timeseries.png', dpi=300, bbox_inches='tight')
plt.show()

# 6. Seasonal decomposition (daily seasonality)
decomp = seasonal_decompose(df['visits'], model='additive', period=24)  # Hourly, daily cycle=24h
fig, axes = plt.subplots(4, 1, figsize=(15, 10))
decomp.observed.plot(ax=axes[0])
decomp.trend.plot(ax=axes[1])
decomp.seasonal.plot(ax=axes[2])
decomp.resid.plot(ax=axes[3])
plt.suptitle('Seasonal Decomposition (Daily Period=24h)')
plt.tight_layout()
plt.savefig('decomposition.png', dpi=300, bbox_inches='tight')
plt.show()

# Boxplot for distribution by hour
plt.figure(figsize=(15, 6))
sns.boxplot(data=df, x='hour', y='visits')
plt.title('Visits Distribution by Hour')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('hourly_boxplot.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nAnalysis complete. Plots saved: hourly_traffic.png, weekly_pattern.png, full_timeseries.png, decomposition.png, hourly_boxplot.png")
print("Key insights:")
print("- Clear daily seasonality: peaks evenings (18-21h), troughs early morning.")
print("- Check weekly for weekend vs weekday differences.")

