# Codeforces AI Coach

An AI-powered coaching system for competitive programmers on Codeforces. It pulls your
profile, contest history, and submissions, analyzes strengths/weaknesses by topic, and
uses an LLM (via Groq) to generate personalized practice plans and recommendations —
all orchestrated through a LangGraph pipeline and exposed both as a REST API and as
an MCP server so it can be queried directly from Claude.

## How it works

```
Codeforces API ──▶ FastAPI backend ──▶ Postgres/SQLite
                        │
                        ├── LangGraph pipeline (profile → analytics → contest →
                        │    recommendation → planner → LLM summary)
                        │
                        └── Background scheduler (auto-syncs every N hours)

MCP server ──▶ calls the FastAPI backend over HTTP ──▶ exposed as tools to Claude
```

## Project structure

```
backend/
  main.py                 FastAPI app, startup table creation, auto-sync scheduler
  config.py                TRACKED_HANDLES, SYNC_INTERVAL_HOURS, GROQ_MODEL
  database.py               SQLAlchemy engine (SQLite locally, Postgres in production)
  models/                  SQLAlchemy models: User, Submission, Problem, Contest
  routes/user_routes.py     REST endpoints
  services/                 Business logic (Codeforces API calls, analytics, recommendations,
                             practice planning, sync jobs)
  graph/                    LangGraph pipeline (nodes, state, graph builder)
  prompts/                  LLM prompt templates

mcp_server/
  server.py                 FastMCP server exposing tools (get_profile, get_analytics, etc.)
  tools.py                  Thin HTTP client calling the FastAPI backend
  config.py                 FASTAPI_URL (points at local or deployed backend)

frontend/                   Frontend client (see its own files for details)

Dockerfile                  Container build for the FastAPI backend
create_tables.py            One-off manual table creation (not needed — main.py does this on startup)
```

## REST API

| Endpoint | Description |
|---|---|
| `GET /profile/{handle}` | Live Codeforces profile |
| `GET /analytics/{handle}` | Success rate + weak/strong topics |
| `GET /recommendations/{handle}` | Recommended problems based on weak topics |
| `GET /contest-analysis/{handle}` | Contest history stats and trend |
| `GET /plan/{handle}` | 7-day practice plan |
| `GET /coach/{handle}` | Runs the full LangGraph pipeline incl. LLM summary |
| `GET /sync-problems` | Manually refresh the problem catalog |
| `GET /sync-contests/{handle}` | Manually refresh a handle's contest history |
| `GET /sync-submissions/{handle}` | Manually refresh a handle's submissions |
| `GET /health` | Health check |

Manual `/sync-*` calls are optional — the backend auto-syncs `TRACKED_HANDLES` on a
schedule (default: every 6 hours, plus once on startup).

## Local development

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# create a .env file with:
# GROQ_API_KEY=your_key_here

uvicorn backend.main:app --reload
```

Tables are created automatically on startup. No manual migration step needed.

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///coach.db` | Set to a Postgres URL in production |
| `GROQ_API_KEY` | — | Required for LLM coaching summaries |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | Groq model used for coaching summaries |
| `SYNC_INTERVAL_HOURS` | `6` | How often the background sync job runs |

## Deployment

The backend is containerized (`Dockerfile`) and deploys cleanly to any Docker-based
host (Render, Railway, Fly.io, etc.):

1. Provision a managed Postgres instance and copy its connection URL.
2. Create a web service from this repo — the platform will detect the `Dockerfile`.
3. Set `DATABASE_URL`, `GROQ_API_KEY`, and `TRACKED_HANDLES` as environment variables.
4. Deploy. Tables are created and the first sync runs automatically on boot.
5. Update `mcp_server`'s `FASTAPI_URL` environment variable to point at the deployed
   URL so the MCP server (and Claude) talk to the live backend instead of localhost.

## MCP server

```bash
cd mcp_server
pip install -r requirements.txt
python server.py
```

Exposes these tools to Claude: `get_profile`, `get_analytics`, `get_recommendations`,
`get_contest_analysis`, `get_practice_plan`, `get_coach`.
