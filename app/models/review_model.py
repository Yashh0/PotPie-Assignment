from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ReviewResult(Base):
    __tablename__ = "review_results"

    task_id = Column(String, primary_key=True, index=True)
    pr_url = Column(Text)
    result_summary = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
