from datetime import datetime, date

def travel_weather_advisor(weather, aqi, risk_score, travel_date):
    temp = weather["temp"]
    rain = weather["rain_chance"]
    condition = weather["condition"]

    advice = []

    # Temperature advice
    if temp > 35:
        advice.append("🔥 Very hot weather. Carry sunscreen & stay hydrated.")
    elif temp < 10:
        advice.append("❄ Cold weather. Carry warm clothes.")
    else:
        advice.append("🌤 Pleasant temperature for travel.")

    # Rain advice
    if rain > 60:
        advice.append("🌧 High rain chance. Carry raincoat/umbrella.")
    elif rain > 30:
        advice.append("🌦 Possible rain showers.")
    else:
        advice.append("☀ Low rain probability.")

    # AQI advice
    if aqi > 200:
        advice.append("😷 Poor air quality. Mask recommended.")
    elif aqi > 100:
        advice.append("🌫 Moderate air pollution.")
    else:
        advice.append("✅ Good air quality.")

    # Risk advice
    if risk_score > 7:
        advice.append("⚠ High climate risk. Travel not recommended.")
    elif risk_score > 4:
        advice.append("⚠ Moderate climate risk. Plan carefully.")
    else:
        advice.append("✅ Low climate risk for travel.")

    return advice
