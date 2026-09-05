import pandas as pd
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score


df = pd.read_csv("focus_training_data.csv")

X = df[
    ["user_id", "hour", "day_of_week", "category", "priority", "estimated_duration"]
]

y = df["focus_score"]


categorical_features = ["category", "priority"]
numeric_features = ["user_id", "hour", "day_of_week", "estimated_duration"]


preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", "passthrough", numeric_features)
    ]
)


model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)


pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", model)
])


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


pipeline.fit(X_train, y_train)


predictions = pipeline.predict(X_test)


mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)


print("Model Evaluation")
print("----------------")
print(f"MAE: {mae:.2f}")
print(f"R2 Score: {r2:.2f}")


pipeline.fit(X, y)

joblib.dump(pipeline, "focus_model.pkl")

print("\nFinal model trained on full dataset.")
print("Model saved as focus_model.pkl")