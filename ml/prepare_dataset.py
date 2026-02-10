import pandas as pd

def prepare_dataset():
    df = pd.read_csv("ml/weather_dataset.csv")

    # Convert date column
    df["date"] = pd.to_datetime(df["date"])

    # Create seasonal feature
    df["month"] = df["date"].dt.month

    # Select ML features
    df_ml = df[[
        "temp",
        "humidity",
        "windspeed",
        "pressure",
        "day_index",
        "month"
    ]].dropna()

    df_ml.to_csv("ml/final_training_data.csv", index=False)
    print("✅ Dataset prepared successfully")

if __name__ == "__main__":
    prepare_dataset()
