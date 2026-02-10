import requests
import re

GEOCODE_API = "https://nominatim.openstreetmap.org/search"
WEATHER_API = "https://api.open-meteo.com/v1/forecast"
AQI_API = "https://air-quality-api.open-meteo.com/v1/air-quality"


# -----------------------------
# Helpers
# -----------------------------
def get_coordinates(city):
    city = city.replace("?", "").replace(".", "").strip()

    params = {"q": city + ", India", "format": "json", "limit": 1}
    res = requests.get(GEOCODE_API, params=params, headers={"User-Agent": "chatbot"})
    data = res.json()

    if not data:
        return None, None

    return float(data[0]["lat"]), float(data[0]["lon"])


def get_weather(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"],
        "daily": ["precipitation_probability_max"],
        "timezone": "auto"
    }
    res = requests.get(WEATHER_API, params=params)
    return res.json()


def get_aqi(lat, lon):
    params = {"latitude": lat, "longitude": lon, "hourly": "us_aqi"}
    res = requests.get(AQI_API, params=params)
    data = res.json()
    return int(data["hourly"]["us_aqi"][0])


# -----------------------------
# AI Chatbot Engine
# -----------------------------
def weather_chatbot_engine(message, weather_data=None, climate_risk=None, aqi=None):
    msg = message.lower()

    # Extract city name from sentence
    city_match = re.search(r"in ([a-zA-Z ]+)", msg)
    city = city_match.group(1).strip() if city_match else None

    # Weather intent
    if "weather" in msg or "temperature" in msg:
        if not city:
            return "Please mention a city. Example: What's the weather in Delhi?"

        lat, lon = get_coordinates(city)

        if lat is None:
            return f"❌ Sorry, I couldn't find weather data for '{city.title()}'. Please check spelling."

        weather = get_weather(lat, lon)
        current = weather["current"]
        daily = weather["daily"]

        temp = round(current["temperature_2m"], 1)
        humidity = current["relative_humidity_2m"]
        wind = round(current["wind_speed_10m"], 1)
        rain = daily["precipitation_probability_max"][0]

        return (
            f"🌍 Weather in {city.title()}:\n"
            f"🌡 Temperature: {temp}°C\n"
            f"💧 Humidity: {humidity}%\n"
            f"🌬 Wind: {wind} km/h\n"
            f"🌧 Rain Chance: {rain}%"
        )

    # Pollution intent
    if "pollution" in msg or "aqi" in msg or "air quality" in msg:
        if not city:
            return "Please mention a city. Example: How is air pollution in Mumbai?"

        lat, lon = get_coordinates(city)

        if lat is None:
            return f"❌ Sorry, I couldn't find AQI data for '{city.title()}'."

        aqi = get_aqi(lat, lon)

        if aqi > 200:
            status = "Very Poor 😷"
        elif aqi > 100:
            status = "Moderate 🌫"
        else:
            status = "Good ✅"

        return f"🌫 Air Quality in {city.title()}: AQI {aqi} ({status})"

    # Travel intent
    if "safe" in msg or "travel" in msg:
        return "✈ For travel advice, please use the Smart Travel Advisor section on the website."

    # Default help
    return (
        "Hello! 🌍 I'm your AI Climate Assistant.\n\n"
        "Try asking:\n"
        "• What's the weather in Delhi?\n"
        "• How is pollution in Mumbai?\n"
        "• Is Chennai safe to travel?\n"
    )
