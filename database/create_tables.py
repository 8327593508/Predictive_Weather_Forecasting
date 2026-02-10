from database.db import get_engine
from sqlalchemy import text

engine = get_engine()

with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS weather_history;"))

    conn.execute(text("""
        CREATE TABLE weather_history (
            id SERIAL PRIMARY KEY,
            city TEXT,
            date DATE,
            temp REAL,
            humidity REAL,
            windspeed REAL,
            pressure REAL,
            rain REAL
        );
    """))

    conn.commit()

print("✅ weather_history table recreated successfully with correct schema")
