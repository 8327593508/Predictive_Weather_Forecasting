import datetime

# Flood-prone baseline risk map for 100+ Indian cities
FLOOD_BASELINE = {

    # West Bengal
    "kolkata": 8, "howrah": 7, "durgapur": 6, "asansol": 6,
    "siliguri": 8, "jalpaiguri": 8, "cooch behar": 7,

    # Assam & Northeast
    "guwahati": 9, "dibrugarh": 9, "silchar": 9, "tezpur": 8,
    "agartala": 8, "imphal": 7, "aizawl": 7, "kohima": 7,
    "itanagar": 8, "dimapur": 7, "shillong": 8,

    # Bihar
    "patna": 9, "gaya": 8, "bhagalpur": 9, "muzaffarpur": 9,
    "darbhanga": 9, "purnia": 9, "araria": 9,

    # Uttar Pradesh
    "lucknow": 6, "kanpur": 7, "prayagraj": 8,
    "varanasi": 8, "gorakhpur": 9, "bareilly": 7,
    "meerut": 7, "ghaziabad": 6, "noida": 6,

    # Odisha
    "bhubaneswar": 8, "cuttack": 9, "puri": 8,
    "balasore": 9, "berhampur": 8,

    # Andhra Pradesh
    "visakhapatnam": 8, "vijayawada": 7, "guntur": 7,
    "nellore": 8, "kakinada": 9,

    # Tamil Nadu
    "chennai": 8, "vellore": 6, "madurai": 6,
    "coimbatore": 5, "tirunelveli": 6,

    # Kerala
    "kochi": 8, "ernakulam": 8, "trivandrum": 7,
    "kollam": 7, "alappuzha": 9, "kottayam": 8,

    # Maharashtra
    "mumbai": 9, "thane": 8, "navi mumbai": 8,
    "pune": 6, "nagpur": 5, "nashik": 6,
    "aurangabad": 5, "kolhapur": 7, "sangli": 7,

    # Karnataka
    "bangalore": 5, "mysore": 5, "mangalore": 7,
    "udupi": 8, "hubli": 5, "belgaum": 6,

    # Telangana
    "hyderabad": 5, "warangal": 6, "nizamabad": 6,
    "karimnagar": 6,

    # Rajasthan
    "jaipur": 3, "jodhpur": 2, "udaipur": 4,
    "kota": 4, "ajmer": 3, "bikaner": 2,

    # Madhya Pradesh
    "bhopal": 5, "indore": 4, "jabalpur": 6,
    "gwalior": 5, "rewa": 6,

    # Gujarat
    "ahmedabad": 5, "surat": 7, "vadodara": 6,
    "rajkot": 5, "bhavnagar": 7, "jamnagar": 6,

    # Punjab & Haryana
    "chandigarh": 4, "ludhiana": 5, "amritsar": 5,
    "patiala": 5, "ambala": 5, "panipat": 5,
    "gurgaon": 4, "faridabad": 5,

    # Delhi NCR
    "delhi": 5, "new delhi": 5,

    # Jammu & Kashmir + Himalayas
    "srinagar": 7, "jammu": 6, "leh": 2, "kargil": 2,
    "shimla": 5, "manali": 6, "dharamshala": 7,
    "dehradun": 6, "haridwar": 7, "rishikesh": 7,

    # Jharkhand
    "ranchi": 6, "jamshedpur": 7, "dhanbad": 7,

    # Chhattisgarh
    "raipur": 6, "bilaspur": 7, "korba": 7
}


def calculate_climate_risk(city, weather, aqi, forecast):
    city_key = city.lower()

    temp = weather["temp"]
    rain_today = weather["rain_chance"]
    humidity = weather["humidity"]

    # Heatwave Risk
    heat_risk = min(10, round(temp / 4, 1))

    # 7-day rain average
    avg_rain = sum([d["rain"] for d in forecast]) / 7

    # Monsoon boost
    month = datetime.datetime.now().month
    monsoon_boost = 3 if month in [6, 7, 8, 9] else 0

    # City flood baseline
    base_flood = FLOOD_BASELINE.get(city_key, 4)

    # Flood Risk Model
    flood_risk = min(10, round(
        (base_flood * 0.6) +
        (avg_rain / 15) +
        (rain_today / 15) +
        monsoon_boost, 1)
    )

    # Pollution Risk
    pollution_risk = min(10, round(aqi / 30, 1))

    # Cyclone Risk (coastal sensitivity)
    cyclone_risk = 7 if city_key in ["chennai","kolkata","bhubaneswar","visakhapatnam","kochi","mumbai","surat"] else 3

    # Rainfall Variability
    rainfall_variability = min(10, round(avg_rain / 8, 1))

    # Total Risk
    total_risk = round(
        (heat_risk + flood_risk + pollution_risk + cyclone_risk + rainfall_variability) / 5, 1
    )

    return {
        "total": total_risk,
        "heatwave": heat_risk,
        "flood": flood_risk,
        "pollution": pollution_risk,
        "cyclone": cyclone_risk,
        "rainfall": rainfall_variability
    }
