from collections import defaultdict

from backend.database import SessionLocal
from backend.models.user import User
from backend.models.submission import Submission


def overall_success_rate(handle):
    db = SessionLocal()

    submissions = (
        db.query(Submission)
        .filter(Submission.handle == handle)
        .all()
    )

    total = len(submissions)

    if total == 0:
        db.close()
        return 0

    solved = sum(
        1
        for sub in submissions
        if sub.verdict == "OK"
    )

    db.close()

    return round(
        solved * 100 / total,
        2
    )

def get_user_rating(handle):
    db = SessionLocal()

    user = (
        db.query(User)
        .filter(User.handle == handle)
        .first()
    )

    db.close()

    if not user:
        return 1200

    return user.rating

def tag_statistics(handle):
    db = SessionLocal()

    submissions = (
        db.query(Submission)
        .filter(Submission.handle == handle)
        .all()
    )

    tag_total = defaultdict(int)
    tag_ok = defaultdict(int)

    for sub in submissions:

        if not sub.tags:
            continue

        tags = sub.tags.split(",")

        for tag in tags:

            tag_total[tag] += 1

            if sub.verdict == "OK":
                tag_ok[tag] += 1

    db.close()

    stats = {}

    for tag in tag_total:

        stats[tag] = round(
            tag_ok[tag] * 100 / tag_total[tag],
            2
        )

    return stats


def weak_topics(handle):

    stats = tag_statistics(handle)

    weak = []

    for tag, success_rate in stats.items():

        if success_rate < 50:

            weak.append(
                {
                    "tag": tag,
                    "success_rate": success_rate
                }
            )

    weak.sort(
        key=lambda x: x["success_rate"]
    )

    return weak[:5]


def strong_topics(handle):

    stats = tag_statistics(handle)

    strong = []

    for tag, success_rate in stats.items():

        if success_rate >= 80:

            strong.append(
                {
                    "tag": tag,
                    "success_rate": success_rate
                }
            )

    strong.sort(
        key=lambda x: -x["success_rate"]
    )

    return strong[:5]


def analytics_report(handle):

    return {

        "overall_success_rate":
            overall_success_rate(handle),

        "weak_topics":
            weak_topics(handle),

        "strong_topics":
            strong_topics(handle)
    }