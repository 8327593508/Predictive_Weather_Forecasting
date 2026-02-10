import pandas as pd
import joblib

MODEL_PATH = "models/weather_model.pkl"
DATASET_PATH = "ml/final_training_data.csv"

def predict_city_weather(city, current_weather):
    df = pd.read_csv(DATASET_PATH)
    model = joblib.load(MODEL_PATH)

    last_day = df["day_index"].max()
    forecasts = []

    for i in range(1, 8):
        future_day = last_day + i

        X = [[
            future_day,
            current_weather["temp"],
            current_weather["humidity"],
            current_weather["windspeed"],
            current_weather["pressure"]
        ]]

        pred_temp = float(model.predict(X)[0])

        rain_prob = min(100, round(current_weather["humidity"] * 0.8, 1))

        forecasts.append({
            "day": f"Day +{i}",
            "temp": round(pred_temp, 2),
            "rain": rain_prob
        })

    return forecasts
