import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor

DATASET_PATH = "ml/final_training_data.csv"
MODEL_PATH = "models/weather_model.pkl"

df = pd.read_csv(DATASET_PATH)

# Features & Target
X = df[["day_index", "temp", "humidity", "windspeed", "pressure"]]
y = df["temp"]

model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X, y)

joblib.dump(model, MODEL_PATH)

print("✅ Weather model trained and saved successfully")
