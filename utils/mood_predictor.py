import joblib
import numpy as np
import os

# Load the trained model and scaler from ml/models
MODEL_PATH = "ml/models/mood_model.pkl"
SCALER_PATH = "ml/models/scaler.pkl"

if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
    raise FileNotFoundError("Trained model or scaler not found. Run train_model.py first.")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

def predict_mood_score(temperature_f, air_pressure_hpa):
    features = np.array([[temperature_f, air_pressure_hpa]])
    features_scaled = scaler.transform(features)
    predicted_score = model.predict(features_scaled)[0]
    return round(predicted_score, 2)

def interpret_mood_score(score, temperature_f=None, air_pressure_hpa=None):
    if score is None:
        return "No prediction available."

    interpretation = ""

    # Core mood score interpretation
    if score < 3.5:
        interpretation += (
            "🟥 Very Low Mood Score.\n"
            "These conditions are often linked with the lowest mood states — typically due to cold, low pressure, or overcast skies. "
            "Try to prioritize warmth, rest, and gentle pacing."
        )
    elif 3.5 <= score < 4.5:
        interpretation += (
            "🟧 Low Mood Score.\n"
            "Reduced motivation or emotional dullness may occur today. Movement, sunlight, or fresh air might help rebalance you."
        )
    elif 4.5 <= score < 5.3:
        interpretation += (
            "🟨 Neutral Mood Score.\n"
            "Conditions suggest an emotionally steady day — not especially uplifting or draining. Your inner world may play a stronger role."
        )
    elif 5.3 <= score < 6.2:
        interpretation += (
            "🟩 Moderately Positive Mood Score.\n"
            "You might notice improved mood, mental clarity, or light optimism. Great for getting small wins or connecting with others."
        )
    elif 6.2 <= score < 7.2:
        interpretation += (
            "🟩 Strong Positive Mood Score.\n"
            "Expect elevated mood and focus. Many in your dataset reported energy, clarity, and social ease on days like today."
        )
    else:
        interpretation += (
            "🟦 Very High Mood Score.\n"
            "Today's weather is highly aligned with peak mood states — often warm, bright, and stable. A great day to lean into creativity or connection."
        )

    # Add-on logic for extreme temperature and pressure
    if temperature_f is not None:
        if temperature_f < 40:
            interpretation += "\n🌡️ Cold Stress Alert: Sub-40°F temperatures can reduce energy and comfort — layer up and stay warm."
        elif temperature_f > 85:
            interpretation += "\n🌞 Heat Stress Alert: Temps above 85°F may tax your mood and energy — hydration and shade matter."

    if air_pressure_hpa is not None:
        if air_pressure_hpa < 1000:
            interpretation += "\n🌪️ Low Pressure Zone: Atmospheric dips like this can trigger fatigue or mental fog in some people."
        elif air_pressure_hpa > 1035:
            interpretation += "\n🌀 High Pressure Bonus: Elevated pressure today may promote calm, clear-headed vibes."

    return interpretation

# def predict_mood_from_weather(weather_text, temperature):
#     """
#     Simple rule-based mood prediction based on weather conditions and temperature.
#     Returns a string like 'Good', 'Neutral', or 'Bad'.
#     """
#     if not weather_text or temperature is None:
#         return "Unknown"

#     weather_text = weather_text.lower()

#     if "sunny" in weather_text or "clear" in weather_text:
#         if 60 <= temperature <= 80:
#             return "Good"
#         elif temperature < 60:
#             return "Neutral"
#         else:
#             return "Neutral"
#     elif "rain" in weather_text or "snow" in weather_text or "storm" in weather_text:
#         return "Bad"
#     elif "cloud" in weather_text or "overcast" in weather_text:
#         return "Neutral"
#     else:
#         return "Unknown"