import requests
import pandas as pd
from datetime import datetime, timedelta
from database.db import get_engine

engine = get_engine()

# 100 Major Indian Cities with coordinates
CITIES = {
    # West Bengal
    "Kolkata": (22.5726, 88.3639),
    "Howrah": (22.5958, 88.2636),
    "Siliguri": (26.7271, 88.3953),
    "Durgapur": (23.5204, 87.3119),
    "Asansol": (23.6889, 86.9661),
    "Darjeeling": (27.0360, 88.2627),
    "Malda": (25.0108, 88.1411),
    "Kharagpur": (22.3460, 87.2319),

    # Delhi NCR
    "Delhi": (28.6139, 77.2090),
    "Noida": (28.5355, 77.3910),
    "Gurgaon": (28.4595, 77.0266),
    "Faridabad": (28.4089, 77.3178),
    "Ghaziabad": (28.6692, 77.4538),

    # Maharashtra
    "Mumbai": (19.0760, 72.8777),
    "Pune": (18.5204, 73.8567),
    "Nagpur": (21.1458, 79.0882),
    "Nashik": (19.9975, 73.7898),
    "Aurangabad": (19.8762, 75.3433),
    "Solapur": (17.6599, 75.9064),

    # Karnataka
    "Bangalore": (12.9716, 77.5946),
    "Mysore": (12.2958, 76.6394),
    "Mangalore": (12.9141, 74.8560),
    "Hubli": (15.3647, 75.1240),
    "Belgaum": (15.8497, 74.4977),

    # Tamil Nadu
    "Chennai": (13.0827, 80.2707),
    "Coimbatore": (11.0168, 76.9558),
    "Madurai": (9.9252, 78.1198),
    "Trichy": (10.7905, 78.7047),
    "Salem": (11.6643, 78.1460),
    "Erode": (11.3410, 77.7172),

    # Telangana
    "Hyderabad": (17.3850, 78.4867),
    "Warangal": (17.9689, 79.5941),
    "Nizamabad": (18.6725, 78.0941),

    # Andhra Pradesh
    "Visakhapatnam": (17.6868, 83.2185),
    "Vijayawada": (16.5062, 80.6480),
    "Guntur": (16.3067, 80.4365),
    "Nellore": (14.4426, 79.9865),
    "Kurnool": (15.8281, 78.0373),

    # Kerala
    "Thiruvananthapuram": (8.5241, 76.9366),
    "Kochi": (9.9312, 76.2673),
    "Kozhikode": (11.2588, 75.7804),
    "Thrissur": (10.5276, 76.2144),
    "Kannur": (11.8745, 75.3704),

    # Gujarat
    "Ahmedabad": (23.0225, 72.5714),
    "Surat": (21.1702, 72.8311),
    "Vadodara": (22.3072, 73.1812),
    "Rajkot": (22.3039, 70.8022),
    "Bhavnagar": (21.7645, 72.1519),

    # Rajasthan
    "Jaipur": (26.9124, 75.7873),
    "Jodhpur": (26.2389, 73.0243),
    "Udaipur": (24.5854, 73.7125),
    "Ajmer": (26.4499, 74.6399),
    "Kota": (25.2138, 75.8648),

    # Uttar Pradesh
    "Lucknow": (26.8467, 80.9462),
    "Kanpur": (26.4499, 80.3319),
    "Varanasi": (25.3176, 82.9739),
    "Prayagraj": (25.4358, 81.8463),
    "Agra": (27.1767, 78.0081),
    "Meerut": (28.9845, 77.7064),

    # Bihar
    "Patna": (25.5941, 85.1376),
    "Gaya": (24.7955, 85.0002),
    "Bhagalpur": (25.2425, 86.9842),

    # Madhya Pradesh
    "Bhopal": (23.2599, 77.4126),
    "Indore": (22.7196, 75.8577),
    "Jabalpur": (23.1815, 79.9864),
    "Gwalior": (26.2183, 78.1828),

    # Punjab & Haryana
    "Chandigarh": (30.7333, 76.7794),
    "Ludhiana": (30.9010, 75.8573),
    "Amritsar": (31.6340, 74.8723),
    "Ambala": (30.3782, 76.7767),

    # Himachal, J&K, Ladakh
    "Shimla": (31.1048, 77.1734),
    "Manali": (32.2396, 77.1887),
    "Dharamshala": (32.2190, 76.3234),
    "Srinagar": (34.0837, 74.7973),
    "Jammu": (32.7266, 74.8570),
    "Leh": (34.1526, 77.5771),

    # North East
    "Guwahati": (26.1445, 91.7362),
    "Shilong": (25.5788, 91.8933),
    "Agartala": (23.8315, 91.2868),
    "Imphal": (24.8170, 93.9368),
    "Aizawl": (23.7271, 92.7176),
    "Kohima": (25.6751, 94.1086),
    "Itanagar": (27.0844, 93.6053)
}


def download_city_weather(city, lat, lon, years=2):

    # Always take yesterday as the last available date
    end_date = datetime.today() - timedelta(days=1)

    # Go back N years from yesterday
    start_date = end_date - timedelta(days=365 * years)

    start = start_date.strftime("%Y-%m-%d")
    end = end_date.strftime("%Y-%m-%d")

    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={lat}"
        f"&longitude={lon}"
        f"&start_date={start}"
        f"&end_date={end}"
        "&daily=temperature_2m_mean,precipitation_sum"
        "&timezone=Asia%2FKolkata"
    )

    print(f"\n📥 Downloading {city} weather history...")
    print(f"📅 From {start} to {end}")


    response = requests.get(url, timeout=30)

    if response.status_code != 200:
        print("❌ API Error:", response.text)
        return

    data = response.json()

    if "daily" not in data:
        print("❌ Invalid API response for", city)
        return

    df = pd.DataFrame({
        "city": city,
        "date": data["daily"]["time"],
        "temp": data["daily"]["temperature_2m_mean"],
        "humidity": [None] * len(data["daily"]["time"]),
        "windspeed": [None] * len(data["daily"]["time"]),
        "pressure": [None] * len(data["daily"]["time"]),
        "rain": data["daily"]["precipitation_sum"]
    })

    df.to_sql("weather_history", engine, if_exists="append", index=False)

    print(f"✅ {city}: {len(df)} days stored")


if __name__ == "__main__":
    print("\n🚀 Downloading 2 years historical weather data for 100 Indian cities...\n")

    for city, coords in CITIES.items():
        download_city_weather(city, coords[0], coords[1], years=2)

    print("\n🎉 Weather history download completed successfully!")
