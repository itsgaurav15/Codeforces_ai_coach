from backend.database import SessionLocal
from backend.models.contest import Contest
from backend.services.codeforces_service import get_contest_history


def sync_contests(handle):

    db = SessionLocal()

    contests = get_contest_history(handle)

    db.query(Contest).filter(
        Contest.handle == handle
    ).delete()

    db.commit()

    for contest in contests:

        row = Contest(

            handle=handle,

            contest_id=contest["contestId"],

            contest_name=contest["contestName"],

            rank=contest["rank"],

            old_rating=contest["oldRating"],

            new_rating=contest["newRating"],

            rating_change=contest["newRating"] -
                           contest["oldRating"],

            contest_time=contest["ratingUpdateTimeSeconds"]

        )

        db.add(row)

    db.commit()

    db.close()

    return {

        "saved": len(contests)

    }