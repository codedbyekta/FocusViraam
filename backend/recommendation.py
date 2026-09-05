import pandas as pd
import joblib
from sqlalchemy import text

from database import engine

model = joblib.load("focus_model.pkl")


def format_hour(hour):
    if hour == 0:
        return "12 AM"
    if hour < 12:
        return f"{hour} AM"
    if hour == 12:
        return "12 PM"
    return f"{hour - 12} PM"


def recommend_best_time(
    user_id,
    day_of_week,
    category,
    priority,
    estimated_duration
):

    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT COUNT(*) AS session_count,
                       AVG(focus_score) AS average_focus
                FROM focus_sessions
                WHERE user_id = :user_id
                  AND focus_score IS NOT NULL
            """),
            {"user_id": user_id}
        ).fetchone()

    session_count = result.session_count

    if session_count < 10:

        with engine.connect() as connection:
            result = connection.execute(
                text("""
                    SELECT
                        EXTRACT(HOUR FROM start_time) AS hour,
                        AVG(focus_score) AS avg_focus
                    FROM focus_sessions
                    WHERE focus_score IS NOT NULL
                    GROUP BY EXTRACT(HOUR FROM start_time)
                    ORDER BY avg_focus DESC
                    LIMIT 1
                """)
            ).fetchone()

        hour = int(result.hour)
        score = float(result.avg_focus)

        return {
            "recommendation_type": "global_average",
            "recommended_hour": hour,
            "recommended_time": format_hour(hour),
            "predicted_focus_score": round(score, 2),
            "session_count": session_count,
            "reason": "Not enough personal session data yet. Recommendation is based on historical data across users."
        }

    elif session_count < 30:

        with engine.connect() as connection:
            result = connection.execute(
                text("""
                    SELECT
                        EXTRACT(HOUR FROM start_time) AS hour,
                        AVG(focus_score) AS avg_focus
                    FROM focus_sessions
                    WHERE user_id = :user_id
                      AND focus_score IS NOT NULL
                    GROUP BY EXTRACT(HOUR FROM start_time)
                    ORDER BY avg_focus DESC
                    LIMIT 1
                """),
                {"user_id": user_id}
            ).fetchone()

        hour = int(result.hour)
        score = float(result.avg_focus)

        return {
            "recommendation_type": "user_average",
            "recommended_hour": hour,
            "recommended_time": format_hour(hour),
            "predicted_focus_score": round(score, 2),
            "session_count": session_count,
            "reason": "Based on your previous sessions, this has been your most productive time."
        }

    else:

        hours = list(range(9, 22))

        data = pd.DataFrame([
            {
                "user_id": user_id,
                "hour": hour,
                "day_of_week": day_of_week,
                "category": category,
                "priority": priority,
                "estimated_duration": estimated_duration
            }
            for hour in hours
        ])

        predictions = model.predict(data)

        best_index = predictions.argmax()

        best_hour = hours[best_index]
        best_score = float(predictions[best_index])
        average_prediction = float(predictions.mean())

        if best_score - average_prediction >= 15:
            strength = "high"
        elif best_score - average_prediction >= 7:
            strength = "medium"
        else:
            strength = "low"

        return {
            "recommendation_type": "personalized_ml",
            "recommended_hour": best_hour,
            "recommended_time": format_hour(best_hour),
            "predicted_focus_score": round(best_score, 2),
            "session_count": session_count,
            "recommendation_strength": strength,
            "reason": "Based on your historical behavior and the personalized ML model, this time is predicted to give you the highest focus."
        }