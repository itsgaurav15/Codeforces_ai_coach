# Architecture & Interview Notes — Codeforces AI Coach

This document exists to answer one question well: **"Walk me through this project."**
Everything below is written the way you'd explain it in an interview — what it does,
why it's built this way, and what you'd change with more time.

---

## 1. One-line pitch

An AI coaching system for competitive programmers: it pulls a user's Codeforces
history, computes topic-level strengths/weaknesses, and uses an LLM to generate a
personalized weekly practice plan — served over a REST API, a Streamlit dashboard,
and as MCP tools so it can be queried from an AI assistant directly.

## 2. Folder structure

```
backend/
  main.py                 FastAPI app entrypoint. Owns startup (table creation,
                           background sync scheduler) and global exception handling.
  config.py                Centralized settings, all read from env vars with sane
                            defaults (TRACKED_HANDLES, SYNC_INTERVAL_HOURS, GROQ_MODEL).
  database.py               SQLAlchemy engine/session factory. SQLite locally,
                             Postgres in production — driven by DATABASE_URL.
  exceptions.py              Custom exception hierarchy (HandleNotFoundError,
                              CodeforcesAPIError) so errors map to correct HTTP codes.
  schemas.py                 Pydantic response models — typed API contracts.
  models/                   SQLAlchemy ORM models: User, Submission, Problem, Contest.
  routes/user_routes.py      HTTP layer. Thin — each route just calls a service.
  services/                 All business logic. One file per concern:
                             codeforces_service   -> talks to the external Codeforces API
                             analytics             -> success rate, weak/strong topics
                             recommendation_service -> problem recommendations
                             planner_service        -> weekly practice plan
                             contest_service         -> contest trend analysis (reads DB)
                             contest_sync_service    -> syncs contest history (DB write)
                             submission_service      -> syncs submissions (DB write)
                             problem_service          -> syncs the global problem catalog
                             llm_service               -> Groq LLM call for the coaching summary
  graph/                    LangGraph orchestration for the composite /coach endpoint.
  prompts/                  LLM prompt template, kept separate from llm_service so the
                             prompt can change without touching API-call logic.

frontend/                  Streamlit dashboard. Talks to the backend over HTTP only —
                            no direct DB or business logic here.

mcp_server/                Exposes the same backend as tools an AI assistant can call.
                            Thin HTTP client — no duplicated business logic.

Dockerfile                 Containerizes the backend for cloud deployment.
create_tables.py           Manual/optional table creation (main.py now does this
                            automatically on startup — kept for scripting convenience).
```

## 3. Why this architecture

**Layered: routes → services → models.** This is the standard separation for a
FastAPI service, and it's the answer to "why isn't your business logic in the route
handler?" — routes stay a thin HTTP translation layer, services hold logic that's
testable independent of HTTP, models own persistence. Each service file has a single
responsibility (Single Responsibility Principle) — `contest_service` *reads* contest
data, `contest_sync_service` *writes* it; they're separate because read and write have
different failure modes and different callers.

**Why LangGraph for `/coach`, not just a function that calls services in order?**
Two reasons. First, state management — LangGraph's typed `CoachState` makes the data
flowing between steps explicit and inspectable, rather than a chain of function
arguments. Second, it's the natural place to add branching/retries later (e.g. skip
the recommendation step if the user has no weak topics, or retry the LLM call on
failure) without restructuring a plain function chain.

**Why a background scheduler instead of requiring manual sync calls?** Data
staleness is a real correctness bug: if the analytics/recommendation endpoints read
from a DB that's never refreshed, they silently return stale results. Auto-syncing on
an interval (and once on boot) makes correctness the default instead of something a
caller has to remember to do.

**Why Postgres in production but SQLite locally?** SQLite is zero-setup for local
dev — no separate service to run. But most cloud platforms (Render, Railway, Fly)
have ephemeral filesystems: a SQLite file written to disk is wiped on every
redeploy. Postgres persists. `database.py` picks between them based on whether
`DATABASE_URL` is set, so the same code runs in both environments unmodified.

## 4. Data flow — `/coach/{handle}` (the composite endpoint)

```
Client
  │  GET /coach/J_A_I_KUMAR
  ▼
FastAPI route (user_routes.py)
  │  graph.invoke({"handle": handle})
  ▼
LangGraph pipeline (graph/graph_builder.py)

  profile_node ──────────▶ Codeforces API (live)
       │
       ▼
  analytics_node ────────▶ Postgres/SQLite (reads Submission rows,
       │                    computes tag_statistics ONCE, derives
       │                    weak_topics + strong_topics from it)
       │
       │  weak_tags cached in state ─────────────┐
       ▼                                          │
  contest_node ──────────▶ Postgres/SQLite        │
       │                    (reads Contest rows)  │
       ▼                                          │
  recommendation_node ◀──────────────────────────┘
       │  (reuses cached weak_tags — no recompute)
       │  ────────▶ Postgres/SQLite (rating-range filtered query)
       ▼
  planner_node
       │  (reuses cached weak_tags + recommendations)
       ▼
  coach_summary_node ────▶ Groq LLM API
       │  (builds a prompt from all prior state, gets coaching text back)
       ▼
Response: { profile, analytics, contest_analysis, recommendations,
            practice_plan, summary }
```

**Why the "cached in state" detail matters:** early versions of this pipeline
recomputed `weak_topics` (and the underlying tag-statistics DB scan) up to 4 times
per request, and re-ran the problem-recommendation query twice. Computing once in
`analytics_node` and threading it through `CoachState` to `recommendation_node` and
`planner_node` turned ~8 redundant DB scans into 1. This is the single most valuable
optimization in the codebase, and a good example to walk through in an interview: it
shows you can *read* a call graph and *spot* where the same input produces the same
computation more than once.

## 5. Error handling

```
Service raises a specific exception:
  HandleNotFoundError("bad_handle")     ──▶  404 Not Found
  CodeforcesAPIError("upstream down")   ──▶  502 Bad Gateway

FastAPI @app.exception_handler catches these centrally in main.py —
individual routes don't need their own try/except.
```

This replaces the earlier behavior where an invalid Codeforces handle raised a bare
`Exception`, which FastAPI would turn into an undifferentiated `500 Internal Server
Error` — indistinguishable from an actual bug. The distinction matters: 404 means
"the client asked for something that doesn't exist" (their fault, don't retry), 502
means "our upstream failed" (maybe retry), 500 should mean "we have a bug." Collapsing
all three into 500 is a common junior mistake and a good thing to be able to name.

## 6. API surface

| Endpoint | Method | Response model | Purpose |
|---|---|---|---|
| `/profile/{handle}` | GET | `ProfileResponse` | Live Codeforces profile |
| `/analytics/{handle}` | GET | `AnalyticsResponse` | Success rate + weak/strong topics |
| `/recommendations/{handle}` | GET | — | Recommended problems |
| `/contest-analysis/{handle}` | GET | — | Contest history stats + trend |
| `/plan/{handle}` | GET | — | 7-day practice plan |
| `/coach/{handle}` | GET | — | Full pipeline incl. LLM summary |
| `/sync-*` | GET | — | Manual data refresh (also runs automatically) |
| `/health` | GET | — | Health check for the hosting platform |

`ProfileResponse`/`AnalyticsResponse` are wired with Pydantic `response_model=`
(the pattern extends cleanly to the rest — same 10-line schema, same one-line route
change).

## 7. Scalability — realistically

At **current scale** (a handful of tracked handles), the bottleneck is nonexistent —
this is comfortably fast.

At **100–1,000 users**, the two things that start to matter:
- The `Problem` table query in `recommend_problems` is already indexed on `rating`
  and filtered in SQL (not loaded into Python), so this scales fine.
- Concurrent scheduler runs syncing many handles sequentially would get slow — the
  fix is `asyncio.gather` over handles, or a task queue (Celery/RQ) if sync volume
  grows enough to need retries/backoff per handle.

At **10,000+ users**, you'd want: connection pooling tuned on the Postgres engine
(`pool_size`, `max_overflow`), the Groq LLM call moved off the request path entirely
(pre-generate summaries on a schedule rather than on-demand), and a cache layer
(Redis) in front of `/profile` and `/analytics` since Codeforces rate-limits.

I would **not** reach for microservices or a distributed job queue below that —
that's over-engineering for the actual load this system sees, and "I scaled it
appropriately for the problem instead of defaulting to distributed systems" is
itself a good interview answer.

## 8. Likely interview questions

**"Why FastAPI over Flask/Django?"** Async support out of the box, automatic
OpenAPI docs from type hints (no separate schema-writing step), and Pydantic
validation built in — all of which this project actually uses (see `/docs`,
`schemas.py`).

**"Why SQLAlchemy over raw SQL?"** Portability between SQLite (dev) and Postgres
(prod) without rewriting queries, and the ORM layer maps cleanly onto the four
domain entities (User, Submission, Problem, Contest) without needing anything
fancier like a full repository pattern — that would be over-engineering for four
simple tables.

**"Walk me through what happens when a request hits an invalid handle."** →
Point to §5 above.

**"What was the hardest bug/optimization here?"** → Point to §4's cached-state
optimization. It's real, it's measurable (8 DB scans → 1), and it demonstrates
reading a call graph rather than just writing new code.

**"What would you do differently with more time?"** → See §9 below — have this
ready, not improvised.

## 9. Possible future improvements

- Add `response_model=` schemas to the remaining endpoints (recommendations, plan,
  contest-analysis, coach) — same pattern as `profile`/`analytics`, just not done
  everywhere yet.
- Cache Codeforces API responses with a short TTL to reduce redundant live calls
  and avoid rate-limiting under load.
- Move the LLM coaching summary off the synchronous request path (pre-generate on
  the sync schedule) so `/coach` doesn't block on an external LLM call.
- Add a lightweight test suite (pytest) around the service layer — it's already
  structured to be unit-testable independent of FastAPI/HTTP.
- Add pagination to `/recommendations` if the candidate pool grows.
