from collections import defaultdict

from backend.database import SessionLocal
from backend.models.user import User
from backend.models.submission import Submission


def overall_success_rate(handle):
    db = SessionLocal()
    try:
        submissions = (
            db.query(Submission)
            .filter(Submission.handle == handle)
            .all()
        )

        total = len(submissions)

        if total == 0:
            return 0

        solved = sum(
            1
            for sub in submissions
            if sub.verdict == "OK"
        )

        return round(
            solved * 100 / total,
            2
        )
    finally:
        db.close()

def get_user_rating(handle):
    db = SessionLocal()
    try:
        user = (
            db.query(User)
            .filter(User.handle == handle)
            .first()
        )

        if not user:
            return 1200

        return user.rating
    finally:
        db.close()

def tag_statistics(handle):
    db = SessionLocal()
    try:
        submissions = (
            db.query(Submission)
            .filter(Submission.handle == handle)
            .all()
        )
    finally:
        db.close()

    tag_total = defaultdict(int)
    tag_ok = defaultdict(int)

    for sub in submissions:

        if not sub.tags:
            continue

        tags = [tag for tag in sub.tags.split(",") if tag.strip()]

        for tag in tags:

            tag_total[tag] += 1

            if sub.verdict == "OK":
                tag_ok[tag] += 1

    stats = {}

    for tag in tag_total:

        stats[tag] = round(
            tag_ok[tag] * 100 / tag_total[tag],
            2
        )

    return stats


def weak_topics(handle, stats=None):

    if stats is None:
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


def strong_topics(handle, stats=None):

    if stats is None:
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

    # Compute tag stats once and reuse for both weak and strong topics,
    # instead of scanning all submissions twice.
    stats = tag_statistics(handle)

    return {

        "overall_success_rate":
            overall_success_rate(handle),

        "weak_topics":
            weak_topics(handle, stats),

        "strong_topics":
            strong_topics(handle, stats)
    }