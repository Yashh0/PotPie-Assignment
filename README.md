
# 🧠 PotPie AI — Autonomous Code Review Agent

PotPie AI is a fully asynchronous, autonomous code review backend that analyzes GitHub pull request diffs using LLM agents and returns structured, developer-friendly feedback. It uses a FastAPI backend, Celery task queue, and Groq LLMs to scale intelligent code analysis. Built with production-grade architecture and a clean HTML dashboard.

---

## 🔍 Overview

**Use Case:**  
Automate code reviews for pull requests using LLMs — ideal for teams wanting fast, consistent, AI-powered feedback on new code.

**How it works:**  
1. You submit a GitHub PR URL.  
2. PotPie fetches diffs and metadata.  
3. An LLM agent (via Groq API) reviews the code.  
4. Results are processed async with Celery and stored in PostgreSQL.  
5. You view the results via a REST API or HTML dashboard.

---

## 🚀 Key Features

- ✅ LLM-powered static code review agent (Groq API)
- 🧵 Asynchronous task processing with Celery + Redis
- 🔄 Real-time status tracking of review jobs
- 💾 PostgreSQL for persistent result storage
- 📡 FastAPI-based REST API endpoints
- 🧑‍💻 Minimal frontend dashboard (HTML/CSS/JS)
- 🐳 Fully containerized (Docker & Compose)

---

## 🧠 Architecture Diagram

```txt
[GitHub PR] → [FastAPI] → [Celery Task] → [LLM Agent via Groq] → [Store in PostgreSQL] → [Serve via API/UI]
```

---

## 🧱 Tech Stack

- **Backend:** FastAPI, Python 3.11+, Celery, SQLAlchemy, Pydantic, httpx
- **Async Queue:** Redis
- **Database:** PostgreSQL
- **AI:** Groq LLM API
- **Frontend:** HTML/CSS/JS dashboard
- **Deployment:** Docker + Docker Compose
- **Testing:** pytest

---

## 📦 Getting Started

### 1. Clone & Configure

```bash
git clone https://github.com/your-username/potpie-ai.git
cd potpie-ai
cp .env.example .env  # Add your GitHub token & Groq API key
```

### 2. Launch with Docker

```bash
docker-compose up --build
```

This will spin up:
- Redis (for task queue)
- PostgreSQL (for persistence)
- FastAPI backend
- Celery worker

### 3. Run the Frontend Dashboard

```bash
cd frontend
python3 -m http.server
```

Then open: [http://localhost:8000/index.html](http://localhost:8000/index.html)

---

## 🧪 API Reference

### `POST /analyze-pr`

Trigger a code review.

```json
{
  "repo_url": "https://github.com/user/repo",
  "pr_number": 123,
  "github_token": "ghp_..."
}
```

Response:

```json
{ "task_id": "abc123", "status": "pending" }
```

---

### `GET /status/{task_id}`

Check the current task status.

```json
{ "task_id": "abc123", "status": "SUCCESS" }
```

---

### `GET /results/{task_id}`

Fetch full analysis result.

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
      "total_issues": 1,
      "critical_issues": 1
    }
  }
}
```

---

## 🖥️ Frontend Dashboard

- Launch jobs, check progress, and view results visually
- Accessible via `index.html`
- Designed for both devs and non-technical users

---

## 🧠 Design Decisions

| Component      | Reason |
|----------------|--------|
| **Celery**     | Enables scalable async processing of LLM jobs |
| **FastAPI**    | Lightweight, async-friendly, fast REST API framework |
| **Groq API**   | Ultra-low-latency LLM for quick reviews |
| **PostgreSQL** | Structured, persistent result storage |
| **Docker**     | Easy to ship and deploy across systems |
| **Simple UI**  | Reduces complexity and helps demo the agent easily |

---

## 🚧 Future Work

- ✅ GitHub webhook integration (auto-trigger on PR)
- ⚙️ Result caching for repeated analysis
- 🌐 Multi-language code support
- 🔐 API authentication + rate limiting
- ☁️ Live cloud deployment (Railway, Render)
- 📈 Admin analytics & usage stats

---

## 🧪 Running Tests

```bash
pytest
```

Test suite lives in `tests/`, including endpoint tests.

---

## 🔐 Example `.env` File

```
GITHUB_TOKEN=ghp_...
REDIS_URL=redis://redis:6379/0
POSTGRES_URL=postgresql://postgres:postgres@localhost:5432/potpie
GROQ_API_KEY=your_groq_api_key
```

---

## 🚀 Deployment

- Push to GitHub and deploy with Docker anywhere
- Update frontend API URLs if deploying remotely

---

## 👤 Author

**Yash Trivedi**
