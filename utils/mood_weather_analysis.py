import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_weather_mood_insights(csv_path='static/data/weather_mood_dataset.csv'):
    # Load and clean dataset
    df = pd.read_csv(csv_path).dropna()

    # Convert date if needed
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])

    # Variables to plot
    variables = ['avg_temp_f', 'humidity', 'wind_speed', 'pressure']
    plots = []

    # Ensure plot directory exists
    os.makedirs('static/plots', exist_ok=True)

    for var in variables:
        if var in df.columns:
            plt.figure(figsize=(10, 5))
            plt.scatter(df[var], df['mood_score'], alpha=0.6)
            plt.title(f'{var.replace("_", " ").title()} vs Mood Score')
            plt.xlabel(var.replace("_", " ").title())
            plt.ylabel('Mood Score')
            plt.grid(True)
            plot_path = f'static/plots/{var}_vs_mood.png'
            plt.savefig(plot_path)
            plt.close()
            plots.append(plot_path)

    return plots
