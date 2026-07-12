"""Custom exception hierarchy for the Codeforces AI Coach.

Using specific exception types (instead of raising bare `Exception`)
lets the FastAPI layer translate failures into the correct HTTP status
codes, and gives calling code the ability to catch specific failure
modes instead of a catch-all `except Exception`.
"""


class CoachError(Exception):
    """Base class for all application-specific errors."""


class HandleNotFoundError(CoachError):
    """Raised when a Codeforces handle does not exist."""

    def __init__(self, handle: str):
        self.handle = handle
        super().__init__(f"Codeforces handle '{handle}' was not found.")


class CodeforcesAPIError(CoachError):
    """Raised when the Codeforces API is unreachable or returns an
    unexpected/error response that isn't a simple 'handle not found'."""
