from backend.database import SessionLocal
from backend.models.contest import Contest


def rating_trend(contests):
    """
    Determines whether the user's rating is improving,
    declining or stable.
    """

    if len(contests) < 2:
        return "Not enough contests"

    first_rating = contests[0].new_rating
    last_rating = contests[-1].new_rating

    diff = last_rating - first_rating

    if diff >= 100:
        return "Improving"
    elif diff <= -100:
        return "Declining"
    else:
        return "Stable"


def contest_analysis(handle):

    db = SessionLocal()
    try:
        contests = (
            db.query(Contest)
            .filter(Contest.handle == handle)
            .order_by(Contest.contest_time.asc())
            .all()
        )
    finally:
        db.close()

    if not contests:
        return {
            "message": "No contests found"
        }

    gains = [contest.rating_change for contest in contests]

    current = contests[-1]

    return {

        "contests_participated": len(contests),

        "current_rating": current.new_rating,

        "best_rating": max(
            contest.new_rating
            for contest in contests
        ),

        "lowest_rating": min(
            contest.new_rating
            for contest in contests
        ),

        "largest_gain": max(gains),

        "largest_loss": min(gains),

        "average_gain": round(
            sum(gains) / len(gains),
            2
        ),

        "trend": rating_trend(contests),

        "latest_rank": current.rank,

        "last_contest": current.contest_name
    }