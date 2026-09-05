import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

query = """
SELECT
    fs.id AS session_id,
    fs.user_id,
    EXTRACT(HOUR FROM fs.start_time) AS hour,
    EXTRACT(DOW FROM fs.start_time) AS day_of_week,
    t.category,
    t.priority,
    t.estimated_duration,
    fs.planned_duration,
    fs.focus_score
FROM focus_sessions fs
JOIN tasks t
    ON fs.task_id = t.id
WHERE fs.focus_score IS NOT NULL
ORDER BY fs.id
"""

df = pd.read_sql(query, engine)

df["hour"] = df["hour"].astype(int)
df["day_of_week"] = df["day_of_week"].astype(int)

df.to_csv("focus_training_data.csv", index=False)

print("Dataset created successfully!")
print("Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())