import pandas as pd
from db import get_engine

engine = get_engine()

df = pd.read_sql("SELECT * FROM weather_history ORDER BY date DESC LIMIT 10", engine)
print(df)
