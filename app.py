from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime
import os
from datetime import datetime, date
from extensions.travel_advisor import travel_weather_advisor
from extensions.climate_risk import calculate_climate_risk
from extensions.city_compare import compare_cities
from extensions.climate_dashboard import build_climate_dashboard
from extensions.chatbot import weather_chatbot_engine





app = Flask(__name__)

# -----------------------------
# APIs
# -----------------------------
GEOCODE_API = "https://nominatim.openstreetmap.org/search"
WEATHER_API = "https://api.open-meteo.com/v1/forecast"
AQI_API = "https://air-quality-api.open-meteo.com/v1/air-quality"


# -----------------------------
# Helpers
# -----------------------------
def get_coordinates(place):
    params = {
        "q": place + ", India",
        "format": "json",
        "limit": 1
    }
    res = requests.get(GEOCODE_API, params=params, headers={"User-Agent": "weather-app"})
    data = res.json()
    return float(data[0]["lat"]), float(data[0]["lon"])


def get_weather(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "pressure_msl"],
        "daily": ["temperature_2m_max", "precipitation_probability_max", "sunrise", "sunset"],
        "timezone": "auto"
    }
    res = requests.get(WEATHER_API, params=params)
    return res.json()


def get_forecast(lat, lon):
    weather = get_weather(lat, lon)
    daily = weather["daily"]

    forecast = []
    for i in range(7):
        forecast.append({
            "day": f"Day +{i+1}",
            "temp": round(daily["temperature_2m_max"][i], 1),
            "rain": daily["precipitation_probability_max"][i]
        })

    return forecast



def get_aqi(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "us_aqi"
    }
    res = requests.get(AQI_API, params=params)
    data = res.json()
    return int(data["hourly"]["us_aqi"][0])


# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search")
def search():
    try:
        place = request.args.get("place")

        lat, lon = get_coordinates(place)
        weather = get_weather(lat, lon)
        aqi = get_aqi(lat, lon)

        current = weather["current"]
        daily = weather["daily"]

        # Current KPIs
        current_data = {
            "temp": round(current["temperature_2m"], 1),
            "humidity": current["relative_humidity_2m"],
            "windspeed": round(current["wind_speed_10m"], 1),
            "pressure": round(current["pressure_msl"], 1),
            "rain_chance": daily["precipitation_probability_max"][0],
            "sunrise": daily["sunrise"][0].split("T")[1],
            "sunset": daily["sunset"][0].split("T")[1]
        }

        # 7 day forecast
        forecast = []
        for i in range(7):
            forecast.append({
                "day": f"Day +{i+1}",
                "temp": round(daily["temperature_2m_max"][i], 1),
                "rain": daily["precipitation_probability_max"][i]
            })

        return jsonify({
            "place": place,
            "lat": lat,
            "lon": lon,
            "current": current_data,
            "forecast": forecast,
            "aqi": aqi,
            "alerts": []  # future expansion
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/climate-risk")
def climate_risk_page():
    return render_template("climate_risk.html")

@app.route("/travel-advisor")
def travel_advisor_page():
    return render_template("travel_advisor.html")

@app.route("/compare")
def compare_page():
    return render_template("city_compare.html")

@app.route("/climate-dashboard")
def climate_dashboard_page():
    return render_template("climate_dashboard.html")

@app.route("/chatbot")
def chatbot_page():
    return render_template("chatbot.html")


@app.route("/api/climate-risk")
def climate_risk_api():
    city = request.args.get("city")

    lat, lon = get_coordinates(city)
    weather = get_weather(lat, lon)
    aqi = get_aqi(lat, lon)

    current = weather["current"]
    daily = weather["daily"]

    weather_data = {
        "temp": round(current["temperature_2m"], 1),
        "humidity": current["relative_humidity_2m"],
        "rain_chance": daily["precipitation_probability_max"][0]
    }

    forecast = []
    for i in range(7):
        forecast.append({
            "rain": daily["precipitation_probability_max"][i]
        })

    risk = calculate_climate_risk(city, weather_data, aqi, forecast)

    return jsonify(risk)

@app.route("/api/travel-advisor")
def travel_advisor_api():

    from_city = request.args.get("from")
    to_city = request.args.get("to")
    travel_date = request.args.get("date")

    if not from_city or not to_city or not travel_date:
        return jsonify({"error": "Missing travel details"}), 400

    travel_date = datetime.strptime(travel_date, "%Y-%m-%d").date()

    # Get destination coordinates
    lat, lon = get_coordinates(to_city)

    # Fetch weather
    weather_data = get_weather(lat, lon)
    current = weather_data["current"]
    daily = weather_data["daily"]

    # Build forecast
    forecast = []
    for i in range(7):
        forecast.append({
            "day": f"Day +{i+1}",
            "temp": round(daily["temperature_2m_max"][i], 1),
            "rain": daily["precipitation_probability_max"][i]
        })

    # AQI
    aqi = get_aqi(lat, lon)

    # Destination weather for risk engine
    destination_weather = {
        "temp": round(current["temperature_2m"], 1),
        "humidity": current["relative_humidity_2m"],
        "rain_chance": daily["precipitation_probability_max"][0]
    }

    # Climate risk engine
    climate_risk = calculate_climate_risk(to_city, destination_weather, aqi, forecast)

    # ✅ Extract numeric score safely
    if "score" in climate_risk:
        risk_score = climate_risk["score"]
    elif "total_risk" in climate_risk:
        risk_score = climate_risk["total_risk"]
    elif "risk_score" in climate_risk:
        risk_score = climate_risk["risk_score"]
    else:
        # fallback: sum all numeric values
        risk_score = round(sum(v for v in climate_risk.values() if isinstance(v, (int, float)))/len(climate_risk),1)

    # Travel classification
    if risk_score >= 6:
        status = "High Risk"
        recommendation = "Avoid travel. Unsafe climate conditions."
        color = "red"
    elif risk_score >= 4:
        status = "Moderate Risk"
        recommendation = "Travel with caution. Weather disruptions possible."
        color = "orange"
    else:
        status = "Low Risk"
        recommendation = "Safe for travel."
        color = "green"

    return jsonify({
        "from": from_city,
        "to": to_city,
        "date": travel_date.strftime("%Y-%m-%d"),
        "travel_risk": {
            "score": round(risk_score, 2),
            "status": status,
            "recommendation": recommendation,
            "color": color,
            "factors": climate_risk
        },
        "destination_weather": {
            "temp": destination_weather["temp"],
            "rain_chance": destination_weather["rain_chance"],
            "windspeed": round(current["wind_speed_10m"], 1)
        },
        "aqi": aqi,
        "forecast": forecast
    })

@app.route("/api/compare-cities")
def compare_cities_api():
    city1 = request.args.get("city1")
    city2 = request.args.get("city2")

    if not city1 or not city2:
        return jsonify({"error": "Both cities required"}), 400

    result = compare_cities(city1, city2)
    return jsonify(result)

@app.route("/api/climate-dashboard")
def climate_dashboard_api():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "City required"}), 400

    data = build_climate_dashboard(city)
    return jsonify(data)

@app.route("/api/chatbot", methods=["POST"])
def chatbot_api():
    data = request.json
    message = data.get("message")

    if not message:
        return jsonify({"reply": "Please type a message."})

    reply = weather_chatbot_engine(message)

    return jsonify({"reply": reply})


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
