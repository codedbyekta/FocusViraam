from fastapi import FastAPI
from pydantic import BaseModel

from recommendation import recommend_best_time

app = FastAPI(title="FocusViraam API")


class RecommendationRequest(BaseModel):
    user_id: int
    day_of_week: int
    category: str
    priority: str
    estimated_duration: int


@app.get("/")
def root():
    return {"message": "FocusViraam API is running"}


@app.post("/recommendation")
def get_recommendation(request: RecommendationRequest):
    return recommend_best_time(
        request.user_id,
        request.day_of_week,
        request.category,
        request.priority,
        request.estimated_duration
    )