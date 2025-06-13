# Step 2: Visualization
# This file is used for exploratory data analysis (EDA) and confirms which features are worth training on.

import matplotlib
matplotlib.use('Agg')  # 🔧 Use non-GUI backend for servers

import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np

# def generate_weather_mood_insights(use_extended=True):
#     csv_path = "ml/extended_weather_mood_dataset.csv" if use_extended else "ml/weather_mood_dataset.csv"
#     df = pd.read_csv(csv_path).dropna()
def generate_weather_mood_insights(csv_path='ml/extended_weather_mood_dataset.csv'):
    # Load and clean dataset
    df = pd.read_csv(csv_path)
    print("\n[DEBUG] Initial DataFrame columns:", df.columns.tolist())

    # Drop rows with missing mood_score or plotting variables
    variables = ['temperature_f', 'humidity', 'wind_speed_mph', 'air_pressure_hpa']
    required_columns = ['mood_score'] + variables
    df = df.dropna(subset=required_columns)
    print("[DEBUG] Sample data used for plots:\n", df[required_columns].head())

    # Convert date if needed
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])

    plots = []

    # Ensure plot directory exists
    os.makedirs('static/plots', exist_ok=True)

    for weather_metric in variables:
        if weather_metric in df.columns:
            x = df[weather_metric]
            y = df['mood_score']

            plt.figure(figsize=(10, 5))
            plt.scatter(x, y, alpha=0.6, label='Data')

            if weather_metric in ['air_pressure_hpa', 'temperature_f']:
                slope, intercept = np.polyfit(x, y, 1)
                regression_line = slope * x + intercept
                plt.plot(x, regression_line, color='red', label='Trend Line')
                print(f"[DEBUG] {weather_metric} regression slope: {slope:.4f}, intercept: {intercept:.4f}")

            plt.title(f'{weather_metric.replace("_", " ").title()} vs Mood Score')
            plt.xlabel(weather_metric.replace("_", " ").title())
            plt.ylabel('Mood Score')
            plt.grid(True)
            plt.legend()

            plot_filename = f'{weather_metric}_vs_mood.png'
            plot_path = os.path.join('static/plots', plot_filename)
            plt.savefig(plot_path)
            plt.close()

            print(f"[DEBUG] Saved plot to: {plot_path}")
            plots.append(plot_path)


    return plots
