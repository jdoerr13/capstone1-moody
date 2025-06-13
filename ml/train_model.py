import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

# Load data
df = pd.read_csv("ml/extended_weather_mood_dataset.csv").dropna()


# Select features and target
X = df[['temperature_f', 'air_pressure_hpa']]
y = df['mood_score']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Save scaler for future use
os.makedirs("ml/models", exist_ok=True)
joblib.dump(scaler, "ml/models/scaler.pkl")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "ml/models/mood_model.pkl")

# Evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"✅ Model trained.")
print(f"📈 MSE: {mse:.3f}")
print(f"📊 R^2 Score: {r2:.3f}")
