import requests
from extensions.climate_risk import calculate_climate_risk

GEOCODE_API = "https://nominatim.openstreetmap.org/search"
WEATHER_API = "https://api.open-meteo.com/v1/forecast"
AQI_API = "https://air-quality-api.open-meteo.com/v1/air-quality"


def get_coordinates(city):
    params = {"q": city + ", India", "format": "json", "limit": 1}
    res = requests.get(GEOCODE_API, params=params, headers={"User-Agent": "city-compare"})
    data = res.json()
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


def build_city_profile(city):
    lat, lon = get_coordinates(city)
    weather = get_weather(lat, lon)
    aqi = get_aqi(lat, lon)

    current = weather["current"]
    daily = weather["daily"]

    weather_data = {
        "temp": round(current["temperature_2m"], 1),
        "humidity": current["relative_humidity_2m"],
        "windspeed": round(current["wind_speed_10m"], 1),
        "rain_chance": daily["precipitation_probability_max"][0]
    }

    forecast = [{"rain": daily["precipitation_probability_max"][i]} for i in range(7)]

    # Climate Risk Engine
    risk = calculate_climate_risk(city, weather_data, aqi, forecast)

    # ✅ Correct key from your engine
    risk_score = round(risk["total"], 1)

    return {
        "city": city,
        "temp": weather_data["temp"],
        "rain": weather_data["rain_chance"],
        "wind": weather_data["windspeed"],
        "aqi": aqi,
        "risk": f"{risk_score}"
    }


def compare_cities(city1, city2):
    return {
        "city1": build_city_profile(city1),
        "city2": build_city_profile(city2)
    }
