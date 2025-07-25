# app/code_review/review_agent.py

from app.utils.github import fetch_pr_diff, fetch_pr_metadata, build_pr_diff_url, build_pr_metadata_url
from app.services.analyzer import split_diff_by_file
from app.agents.agent import review_code_chunk
from app.models.schema import FileIssues, Issue, ResultsSummary
from typing import List, Dict
import asyncio


async def run_review(repo_url: str, pr_number: int, github_token: str = None) -> dict:
    """
    Orchestrates the full code review process asynchronously for Celery:
    - Fetches PR metadata & diff
    - Splits diff into files
    - Sends each file to LLM for review
    - Returns results in required format
    """
    pr_diff_url = build_pr_diff_url(repo_url, pr_number)
    pr_metadata_url = build_pr_metadata_url(repo_url, pr_number)
    metadata, raw_diff = await asyncio.gather(
        fetch_pr_metadata(pr_metadata_url, github_token),
        fetch_pr_diff(pr_diff_url, github_token)
    )
    file_chunks = split_diff_by_file(raw_diff)

    files = []
    total_issues = 0
    critical_issues = 0
    for chunk in file_chunks:
        filename = chunk["filename"]
        diff = chunk["diff"]
        issues_list = await review_code_chunk(filename, diff)  # returns list of dicts
        # Convert dicts to Issue models
        issues = [Issue(**issue) for issue in issues_list if isinstance(issue, dict)]
        total_issues += len(issues)
        critical_issues += sum(1 for i in issues if i.type == "bug")
        files.append(FileIssues(name=filename, issues=issues))

    summary = ResultsSummary(
        total_files=len(files),
        total_issues=total_issues,
        critical_issues=critical_issues
    )
    return {
        "files": [f.dict() for f in files],
        "summary": summary.dict()
    }
