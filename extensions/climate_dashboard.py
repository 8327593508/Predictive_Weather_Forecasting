import requests
from datetime import datetime
import statistics

WEATHER_API = "https://archive-api.open-meteo.com/v1/archive"
GEOCODE_API = "https://nominatim.openstreetmap.org/search"



def get_coordinates(city):
    params = {
        "q": city + ", India",
        "format": "json",
        "limit": 1
    }

    res = requests.get(GEOCODE_API, params=params, headers={"User-Agent": "climate-dashboard"})
    data = res.json()

    # ✅ SAFETY CHECK
    if not data:
        raise ValueError(f"City not found: {city}")

    return float(data[0]["lat"]), float(data[0]["lon"])



def get_climate_history(lat, lon):
    today = datetime.now().strftime("%Y-%m-%d")

    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": "2022-01-01",
        "end_date": today,
        "daily": [
            "temperature_2m_max",
            "precipitation_sum"
        ],
        "timezone": "auto"
    }

    res = requests.get(WEATHER_API, params=params)
    return res.json()


def build_climate_dashboard(city):
    lat, lon = get_coordinates(city)
    history = get_climate_history(lat, lon)

    temps = history["daily"]["temperature_2m_max"]
    rain = history["daily"]["precipitation_sum"]
    dates = history["daily"]["time"]

    monthly_temp = {}
    monthly_rain = {}

    for i, date in enumerate(dates):
        month = date[:7]
        monthly_temp.setdefault(month, []).append(temps[i])
        monthly_rain.setdefault(month, []).append(rain[i])

    months = sorted(monthly_temp.keys())

    avg_temp = [round(statistics.mean(monthly_temp[m]), 1) for m in months]
    total_rain = [round(sum(monthly_rain[m]), 1) for m in months]

    # Seasonal breakdown
    seasons = {
        "Winter": [],
        "Summer": [],
        "Monsoon": [],
        "Post-Monsoon": []
    }

    for i, m in enumerate(months):
        month_no = int(m.split("-")[1])

        if month_no in [12, 1, 2]:
            seasons["Winter"].append(avg_temp[i])
        elif month_no in [3, 4, 5]:
            seasons["Summer"].append(avg_temp[i])
        elif month_no in [6, 7, 8, 9]:
            seasons["Monsoon"].append(avg_temp[i])
        else:
            seasons["Post-Monsoon"].append(avg_temp[i])

    seasonal_avg = {
        k: round(statistics.mean(v), 1) if v else 0
        for k, v in seasons.items()
    }

    # Climate volatility
    temp_volatility = round(statistics.stdev(avg_temp[-12:]), 2) if len(avg_temp) >= 12 else 0
    rain_volatility = round(statistics.stdev(total_rain[-12:]), 2) if len(total_rain) >= 12 else 0

    # Extreme rainfall detection
    extreme_rain = [r for r in total_rain if r > (statistics.mean(total_rain) * 1.5)]

    return {
        "city": city,
        "months": months[-12:],
        "avg_temp": avg_temp[-12:],
        "total_rain": total_rain[-12:],
        "seasonal_temp": seasonal_avg,
        "temp_volatility": temp_volatility,
        "rain_volatility": rain_volatility,
        "extreme_rain_count": len(extreme_rain)
    }
