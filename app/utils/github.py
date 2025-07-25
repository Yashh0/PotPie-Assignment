# app/utils/github.py

import httpx
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def build_pr_diff_url(repo_url: str, pr_number: int) -> str:
    # repo_url: https://github.com/user/repo
    # returns: https://github.com/user/repo/pull/{pr_number}.diff
    return f"{repo_url}/pull/{pr_number}.diff"

def build_pr_metadata_url(repo_url: str, pr_number: int) -> str:
    # repo_url: https://github.com/user/repo
    # returns: https://api.github.com/repos/user/repo/pulls/{pr_number}
    parts = repo_url.rstrip('/').split('/')
    user, repo = parts[-2], parts[-1]
    return f"https://api.github.com/repos/{user}/{repo}/pulls/{pr_number}"

def get_headers(github_token: str = None, accept: str = "application/vnd.github.v3.diff"):
    token = github_token or GITHUB_TOKEN
    headers = {"Accept": accept}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

async def fetch_pr_diff(pr_url: str, github_token: str = None) -> str:
    async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
        response = await client.get(pr_url, headers=get_headers(github_token, "application/vnd.github.v3.diff"))
        response.raise_for_status()
        return response.text

async def fetch_pr_metadata(api_url: str, github_token: str = None) -> dict:
    async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
        response = await client.get(api_url, headers=get_headers(github_token, "application/vnd.github+json"))
        response.raise_for_status()
        return response.json()