import requests

from backend.database import SessionLocal
from backend.models.problem import Problem

BASE_URL = "https://codeforces.com/api"


def get_problemset():
    url = f"{BASE_URL}/problemset.problems"

    response = requests.get(url)

    data = response.json()

    return data["result"]["problems"]


def sync_problems():

    db = SessionLocal()

    # Remove old records
    db.query(Problem).delete()
    db.commit()

    problems = get_problemset()

    count = 0

    for p in problems:

        if "rating" not in p:
            continue

        problem = Problem(
            contest_id=p.get("contestId"),
            problem_index=p.get("index"),
            name=p.get("name"),
            rating=p.get("rating"),
            tags=",".join(p.get("tags", []))
        )

        db.add(problem)
        count += 1

    db.commit()
    db.close()

    return {"saved": count}