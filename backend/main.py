import logging
from contextlib import asynccontextmanager
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.config import TRACKED_HANDLES, SYNC_INTERVAL_HOURS
from backend.database import engine
from backend.exceptions import HandleNotFoundError, CodeforcesAPIError
from backend.models.base import Base
from backend.routes.user_routes import router as user_router
from backend.services.contest_sync_service import sync_contests
from backend.services.problem_service import sync_problems
from backend.services.submission_service import sync_submissions

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def scheduled_sync():
    """Refreshes the problem catalog plus contests/submissions for every
    tracked handle. Runs automatically on a schedule so no one has to call
    the /sync-* endpoints by hand."""

    try:
        sync_problems()
    except Exception:
        logger.exception("sync_problems failed")

    for handle in TRACKED_HANDLES:
        try:
            sync_contests(handle)
            sync_submissions(handle)
        except Exception:
            logger.exception("sync failed for handle %s", handle)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables automatically on startup (idempotent — no-ops if they
    # already exist), so a fresh deploy never needs a manual migration step.
    Base.metadata.create_all(bind=engine)

    scheduler.add_job(
        scheduled_sync,
        "interval",
        hours=SYNC_INTERVAL_HOURS,
        next_run_time=datetime.now(),  # also run once immediately on boot
        id="scheduled_sync",
        replace_existing=True,
    )
    scheduler.start()

    yield

    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)


# Centralized exception handling: application code raises specific
# exceptions (backend/exceptions.py) and this is the single place that
# maps them to HTTP status codes, instead of every route needing its own
# try/except.
@app.exception_handler(HandleNotFoundError)
async def handle_not_found(request: Request, exc: HandleNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"error": str(exc)},
    )


@app.exception_handler(CodeforcesAPIError)
async def codeforces_api_error(request: Request, exc: CodeforcesAPIError):
    return JSONResponse(
        status_code=502,  # Bad Gateway: our upstream (Codeforces) failed
        content={"error": str(exc)},
    )


@app.get("/health")
def health():
    """Lightweight endpoint for the cloud platform's health checks."""
    return {"status": "ok"}
