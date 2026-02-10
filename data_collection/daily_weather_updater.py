import requests
import pandas as pd
from datetime import datetime, timedelta
from database.db import get_engine

engine = get_engine()

# 100 Indian Cities (same list you used for history)
CITIES = {
    "Kolkata": (22.5726, 88.3639),
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Chennai": (13.0827, 80.2707),
    "Bangalore": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Pune": (18.5204, 73.8567),
    "Ahmedabad": (23.0225, 72.5714),
    "Jaipur": (26.9124, 75.7873),
    "Lucknow": (26.8467, 80.9462),
    "Patna": (25.5941, 85.1376),
    "Ranchi": (23.3441, 85.3096),
    "Guwahati": (26.1445, 91.7362),
    "Shillong": (25.5788, 91.8933),
    "Agartala": (23.8315, 91.2868),
    "Aizawl": (23.7271, 92.7176),
    "Imphal": (24.8170, 93.9368),
    "Kohima": (25.6751, 94.1086),
    "Itanagar": (27.0844, 93.6053),
    "Srinagar": (34.0837, 74.7973),
    "Jammu": (32.7266, 74.8570),
    "Leh": (34.1526, 77.5771)
}

def update_city_weather(city, lat, lon):
    # yesterday
    date = datetime.today() - timedelta(days=1)
    day = date.strftime("%Y-%m-%d")

    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={lat}"
        f"&longitude={lon}"
        f"&start_date={day}"
        f"&end_date={day}"
        "&daily=temperature_2m_mean,precipitation_sum"
        "&timezone=Asia%2FKolkata"
    )

    response = requests.get(url, timeout=30)
    data = response.json()

    if "daily" not in data:
        print(f"❌ No data for {city}")
        return

    df = pd.DataFrame({
        "city": city,
        "date": data["daily"]["time"],
        "temp": data["daily"]["temperature_2m_mean"],
        "humidity": [None],
        "windspeed": [None],
        "pressure": [None],
        "rain": data["daily"]["precipitation_sum"]
    })

    df.to_sql("weather_history", engine, if_exists="append", index=False)
    print(f"✅ {city} updated for {day}")


if __name__ == "__main__":
    print("🌦 Running Daily Weather Updater")

    for city, coords in CITIES.items():
        update_city_weather(city, coords[0], coords[1])

    print("🎉 Daily weather update completed")
