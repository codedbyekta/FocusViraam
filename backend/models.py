from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey
from database import Base


class FocusSession(Base):
    __tablename__ = "focus_sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration_minutes = Column(Integer)
    focus_score = Column(Float)
    completed_task = Column(Boolean)
    created_at = Column(DateTime)
    planned_duration = Column(Integer)
    interruptions = Column(Integer, default=0)
    self_rating = Column(Integer)