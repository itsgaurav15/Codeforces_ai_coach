import requests

from backend.database import SessionLocal
from backend.models.problem import Problem

BASE_URL = "https://codeforces.com/api"


def get_problemset():
    url = f"{BASE_URL}/problemset.problems"

    response = requests.get(url, timeout=15)

    data = response.json()

    return data["result"]["problems"]


def sync_problems():
    """Upserts the Codeforces problem catalog instead of wiping and
    rewriting it on every run.

    Old approach: DELETE every row, then INSERT ~10,000+ rows, every
    sync interval — even on runs where zero problems actually changed
    (which is most of them; new problems only appear a few times a week
    when a new contest is rated).

    New approach: load existing (contest_id, index) -> row into a dict
    with one query, then for each problem from the API either skip it
    (unchanged), update it (rating/tags/name changed), or insert it
    (genuinely new). Turns O(10,000) writes into O(problems that
    actually changed) on a typical run.
    """

    db = SessionLocal()
    try:
        existing = {
            (row.contest_id, row.problem_index): row
            for row in db.query(Problem).all()
        }

        problems = get_problemset()

        inserted = 0
        updated = 0
        unchanged = 0

        for p in problems:

            if "rating" not in p:
                continue

            key = (p.get("contestId"), p.get("index"))
            tags_str = ",".join(p.get("tags", []))
            name = p.get("name")
            rating = p["rating"]

            row = existing.get(key)

            if row is None:
                db.add(Problem(
                    contest_id=key[0],
                    problem_index=key[1],
                    name=name,
                    rating=rating,
                    tags=tags_str
                ))
                inserted += 1

            elif row.rating != rating or row.tags != tags_str or row.name != name:
                row.rating = rating
                row.tags = tags_str
                row.name = name
                updated += 1

            else:
                unchanged += 1

        db.commit()

        return {
            "inserted": inserted,
            "updated": updated,
            "unchanged": unchanged,
        }
    finally:
        db.close()
