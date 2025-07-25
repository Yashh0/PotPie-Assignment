# app/schemas.py
from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any

class PullRequestRequest(BaseModel):
    url: HttpUrl

class AnalyzePRRequest(BaseModel):
    repo_url: str
    pr_number: int
    github_token: Optional[str] = None

class Issue(BaseModel):
    type: str  # style|bug|performance|best_practice
    line: Optional[int]
    description: str
    suggestion: str

class FileIssues(BaseModel):
    name: str
    issues: List[Issue]

class ResultsSummary(BaseModel):
    total_files: int
    total_issues: int
    critical_issues: int

class AnalyzePRResponse(BaseModel):
    task_id: str
    status: str
    results: Optional[Dict[str, Any]] = None

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Any] = None
