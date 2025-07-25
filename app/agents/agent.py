# app/agents/agent.py

import os
import httpx
from typing import List, Dict

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

async def review_code_chunk(filename: str, diff: str) -> List[Dict]:
    """
    Sends a code diff chunk to Groq LLM and gets a structured review.
    """
    prompt = f"""
You are an autonomous code review agent. Analyze the following code diff for:
- Code style and formatting issues
- Potential bugs or errors
- Performance improvements
- Best practices

Return a list of issues in this JSON format:
[
  {{
    "type": "style|bug|performance|best_practice",
    "line": <int>,
    "description": <str>,
    "suggestion": <str>
  }}
]

Filename: {filename}
Diff:
{diff}
"""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a senior code reviewer."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        # Parse the LLM response
        content = result["choices"][0]["message"]["content"]
        try:
            import json
            issues = json.loads(content)
        except Exception:
            issues = []
        return issues
