# app/workers/tasks.py
from app.code_review.review_agent import run_review
from app.workers.celery_worker import celery_app
import uuid
from app.models.review_model import ReviewResult
from app.db import SessionLocal


@celery_app.task(bind=True)
def analyze_pr_task(self, repo_url: str, pr_number: int, github_token: str = None):
    import asyncio
    try:
        results = asyncio.run(run_review(repo_url, pr_number, github_token))
        return {"results": results}
    except Exception as e:
        import traceback
        # Do not call self.update_state; let Celery handle the error
        raise Exception(f"{str(e)}\n{traceback.format_exc()}")

