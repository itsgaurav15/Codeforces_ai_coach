from backend.database import SessionLocal
from backend.models.submission import Submission
from backend.services.codeforces_service import get_submissions


def sync_submissions(handle):
    db = SessionLocal()
    try:
        # Ask Codeforces for at most 500 submissions directly, instead of
        # fetching the user's entire history and truncating client-side.
        submissions = get_submissions(handle, count=500)

        db.query(Submission)\
          .filter(Submission.handle == handle)\
          .delete()

        for sub in submissions[:500]:
            problem = sub.get("problem", {})

            db_sub = Submission(
                handle=handle,
                contest_id=problem.get("contestId"),
                problem_name=problem.get("name"),
                problem_index=problem.get("index"),
                verdict=sub.get("verdict"),
                rating=problem.get("rating"),
                tags=",".join(problem.get("tags", [])),
                programming_language=sub.get("programmingLanguage")
            )

            db.add(db_sub)

        db.commit()

        return {
            "saved": min(500, len(submissions))
        }
    finally:
        db.close()