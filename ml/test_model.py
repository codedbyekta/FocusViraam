import pandas as pd
import joblib

model = joblib.load("focus_model.pkl")

test_data = pd.DataFrame([
    {
        "user_id": 4,
        "hour": 9,
        "day_of_week": 1,
        "category": "Coding",
        "priority": "high"
    },
    {
        "user_id": 4,
        "hour": 15,
        "day_of_week": 1,
        "category": "Study",
        "priority": "high"
    }
])

predictions = model.predict(test_data)

for i, prediction in enumerate(predictions):
    print(f"Test {i + 1}: Predicted Focus Score = {prediction:.2f}")