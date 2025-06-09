
def predict_mood_from_weather(weather_text, temperature_f):
    weather_text = weather_text.lower()

    if "sunny" in weather_text or "clear" in weather_text:
        return "Happy"
    elif "cloud" in weather_text:
        return "Calm"
    elif "rain" in weather_text or "storm" in weather_text:
        return "Low energy"
    elif "snow" in weather_text:
        return "Cozy"
    elif temperature_f > 90:
        return "Irritable"
    elif temperature_f < 40:
        return "Low energy"
    else:
        return "Neutral"