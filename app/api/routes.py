# app/api/routes.py
from fastapi import APIRouter, HTTPException
from app.models.schema import AnalyzePRRequest, AnalyzePRResponse, TaskStatusResponse
from app.workers.tasks import analyze_pr_task
from celery.result import AsyncResult
from app.workers.tasks import celery_app

router = APIRouter()

@router.post("/analyze-pr", response_model=AnalyzePRResponse)
def analyze_pr(request: AnalyzePRRequest):
    task = analyze_pr_task.delay(request.repo_url, request.pr_number, request.github_token)
    return AnalyzePRResponse(task_id=task.id, status="pending")

@router.get("/status/{task_id}", response_model=TaskStatusResponse)
def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return TaskStatusResponse(task_id=task_id, status=result.state, result=result.result if result.state == "SUCCESS" else None)

@router.get("/results/{task_id}", response_model=AnalyzePRResponse)
def get_results(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    if result.state == "SUCCESS":
        if isinstance(result.result, dict) and "results" in result.result:
            return AnalyzePRResponse(task_id=task_id, status="completed", results=result.result["results"])
        else:
            raise HTTPException(status_code=500, detail="Malformed result from worker.")
    elif result.state == "FAILURE":
        raise HTTPException(status_code=500, detail=str(result.result))
    else:
        return AnalyzePRResponse(task_id=task_id, status=result.state)

from fastapi import APIRouter, HTTPException
from celery.result import AsyncResult
from app.workers.celery_worker import celery_app  # adjust import if needed

@router.get("/review/{task_id}")
async def get_review_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    if result.state == "PENDING":
        return {"status": "PENDING"}
    elif result.state == "FAILURE":
        return {"status": "FAILURE", "error": str(result.result)}
    elif result.state == "SUCCESS":
        return {"status": "SUCCESS", "result": result.result}
    else:
        return {"status": result.state}
