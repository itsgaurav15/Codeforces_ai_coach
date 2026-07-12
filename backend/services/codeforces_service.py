import logging

import requests

from backend.exceptions import HandleNotFoundError, CodeforcesAPIError

BASE_URL = "https://codeforces.com/api"

logger = logging.getLogger(__name__)


def get_user_info(handle: str):
    url = f"{BASE_URL}/user.info?handles={handle}"

    response = requests.get(url, timeout=10)
    data = response.json()

    if data["status"] != "OK":
        # Codeforces returns status != OK for both "handle doesn't exist"
        # and other failures; the comment field reliably contains
        # "not found" for the former.
        if "not found" in data.get("comment", "").lower():
            raise HandleNotFoundError(handle)
        raise CodeforcesAPIError(data.get("comment", "Unknown Codeforces API error"))

    return data["result"][0]


def get_submissions(handle, count=None):
    url = f"{BASE_URL}/user.status?handle={handle}"

    if count is not None:
        # Ask Codeforces to only send back the most recent `count`
        # submissions instead of the user's entire history.
        url += f"&from=1&count={count}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    logger.debug("Status Code: %s", response.status_code)
    logger.debug("URL: %s", response.url)

    data = response.json()

    if data.get("status") != "OK":
        raise CodeforcesAPIError(data.get("comment", "Unable to fetch submissions"))

    return data["result"]


def get_contest_history(handle):
    """Fetches a handle's rating-change history, i.e. one entry per
    contest they've participated in (contest name, rank, rating before/
    after). Despite the Codeforces endpoint being named `user.rating`,
    this is what we use to build both rating history and contest
    history — they're the same data."""

    url = f"{BASE_URL}/user.rating?handle={handle}"

    response = requests.get(url, timeout=10)
    data = response.json()

    if data["status"] != "OK":
        if "not found" in data.get("comment", "").lower():
            raise HandleNotFoundError(handle)
        raise CodeforcesAPIError(data.get("comment", "Unable to fetch contest history"))

    return data["result"]
