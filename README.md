# 🧠 PotPie AI – Autonomous Code Review Agent

PotPie is an async, autonomous code review backend that fetches GitHub pull request diffs, analyzes them using an LLM-powered agent (Groq API), and returns structured feedback via a FastAPI REST API. Results are processed asynchronously with Celery and stored in PostgreSQL. The system is fully dockerized and includes a modern frontend dashboard.

---

## 🚀 Features

- Async code analysis using Celery & Redis
- PR diff & metadata fetched via GitHub API
- LLM-powered review agent (Groq API)
- FastAPI-based REST API
- Results stored in PostgreSQL
- Dockerized deployment
- Modern frontend dashboard (HTML/JS)

---

## 🧱 Tech Stack

- Python 3.11+
- FastAPI
- Celery + Redis
- PostgreSQL
- Docker + Docker Compose
- GitHub API
- Groq API (LLM)
- SQLAlchemy, httpx, pydantic
- pytest
- HTML/CSS/JS frontend

---

## 📦 Setup

### 1. Clone & Environment Setup

```sh
git clone <your-repo-url>
cd PotPie
cp .env.example .env  # Fill in your GitHub token, Groq API key, etc.
```

### 2. Run with Docker

```sh
docker-compose up --build
```

This will start:
- Redis
- Postgres
- FastAPI app (backend)
- Celery worker

### 3. Run Frontend Dashboard

Open `frontend/index.html` in your browser, or run:
```sh
cd frontend
python3 -m http.server
```
Then visit `http://localhost:8000/index.html` in your browser.

---

## 🧪 API Usage

### POST `/analyze-pr`
Trigger async analysis.

**Body:**
```json
{
  "repo_url": "https://github.com/user/repo",
  "pr_number": 123,
  "github_token": "ghp_..."
}
```
**Response:**
```json
{
  "task_id": "abc123",
  "status": "pending"
}
```

### GET `/status/{task_id}`
Poll task status.

**Response:**
```json
{
  "task_id": "abc123",
  "status": "SUCCESS",
  "result": { ... }
}
```

### GET `/results/{task_id}`
Fetch final review result from DB.

**Response:**
```json
{
  "task_id": "abc123",
  "status": "completed",
  "results": {
    "files": [
      {
        "name": "main.py",
        "issues": [
          {
            "type": "style",
            "line": 15,
            "description": "Line too long",
            "suggestion": "Break line into multiple lines"
          },
          {
            "type": "bug",
            "line": 23,
            "description": "Potential null pointer",
            "suggestion": "Add null check"
          }
        ]
      }
    ],
    "summary": {
      "total_files": 1,
      "total_issues": 2,
      "critical_issues": 1
    }
  }
}
```

---

### Example cURL Commands

**Analyze a PR**
```sh
curl -X POST http://localhost:8000/analyze-pr \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/google/adk-python", "pr_number": 2167, "github_token": "ghp_your_token_here"}'
```

**Check Task Status**
```sh
curl http://localhost:8000/status/<task_id>
```

**Get Analysis Results**
```sh
curl http://localhost:8000/results/<task_id>
```
---
## 🖥️ Frontend Dashboard

- Modern HTML/CSS/JS dashboard in `frontend/index.html`
- Start new analysis, check status, view results
- Task history and summary stats

---

## 🛠️ Design Decisions

- **Async processing:** Celery for scalable, non-blocking code analysis
- **LLM agent:** Groq API for code review intelligence
- **Database:** PostgreSQL for persistent results
- **Docker:** Easy local and cloud deployment
- **Frontend:** Simple, beautiful dashboard for non-technical users

---

## 🚧 Future Improvements

- Add GitHub webhook support for automatic PR analysis
- Structured logging (see `structlog` in requirements)
- Result caching for repeated PRs
- Multi-language support
- Rate limiting and authentication
- Live deployment (Railway, Render, etc.)

---

## 📝 Test Instructions

- Run tests with pytest:
```sh
pytest
```
- See `tests/test_routes.py` for example API tests

---

## 📄 Example Environment File

Create `.env.example`:
```
GITHUB_TOKEN=ghp_...
REDIS_URL=redis://redis:6379/0
POSTGRES_URL=postgresql://postgres:postgres@localhost:5432/potpie
GROQ_API_KEY=your_groq_api_key
```

---

## 📤 Deployment

- Push to GitHub and deploy with Docker or cloud platforms
- Update API URLs in frontend if deploying remotely

---
