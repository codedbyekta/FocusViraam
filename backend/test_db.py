from sqlalchemy import text
from database import engine

try:
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT
                    fs.id,
                    fs.user_id,
                    EXTRACT(HOUR FROM fs.start_time) AS hour,
                    EXTRACT(DOW FROM fs.start_time) AS day_of_week,
                    t.category,
                    t.priority,
                    fs.focus_score
                FROM focus_sessions fs
                JOIN tasks t
                    ON fs.task_id = t.id
                ORDER BY fs.id
            """)
        )

        print("ML TRAINING DATA")
        print("-" * 100)

        for row in result:
            print(row)

except Exception as e:
    print("Database error!")
    print(e)