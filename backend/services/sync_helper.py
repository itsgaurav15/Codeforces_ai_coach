"""Lazy sync-on-demand.

Ensures a handle has at least some local data before analytics/
recommendations/etc. try to read from the DB, instead of requiring every
handle to be pre-registered in TRACKED_HANDLES (which only controls the
periodic background refresh) or manually synced via /sync-* first.

Only syncs if the handle has zero rows — an existing handle relies on the
background scheduler (or a manual /sync-* call) to stay fresh. This keeps
a first-time lookup for a brand-new handle fast-ish (one sync) without
silently re-syncing on every single request.
"""

from backend.database import SessionLocal
from backend.models.contest import Contest
from backend.models.submission import Submission
from backend.services.contest_sync_service import sync_contests
from backend.services.submission_service import sync_submissions


def ensure_handle_synced(handle: str):
    db = SessionLocal()
    try:
        has_submissions = (
            db.query(Submission.id)
            .filter(Submission.handle == handle)
            .first()
            is not None
        )
        has_contests = (
            db.query(Contest.id)
            .filter(Contest.handle == handle)
            .first()
            is not None
        )
    finally:
        db.close()

    # Note: sync_submissions only pulls a handle's 500 most recent
    # submissions (see submission_service.py). For handles with very
    # long histories (e.g. top competitive programmers), this means
    # analytics reflect recent activity only, not their entire career.
    if not has_submissions:
        sync_submissions(handle)

    if not has_contests:
        sync_contests(handle)
