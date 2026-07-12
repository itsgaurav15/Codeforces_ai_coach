from backend.database import SessionLocal
from backend.models.submission import Submission
from backend.services.analytics import weak_topics
from backend.services.analytics import get_user_rating
from backend.models.problem import Problem

def get_solved_problems(handle):

    db = SessionLocal()
    try:
        solved = (
            db.query(Submission)
            .filter(
                Submission.handle == handle,
                Submission.verdict == "OK"
            )
            .all()
        )

        return {
            s.problem_name
            for s in solved
        }
    finally:
        db.close()


def recommend_problems(handle, weak_tags=None):

    # Allow callers (e.g. the LangGraph pipeline) to pass already-computed
    # weak topics instead of recomputing them here.
    if weak_tags is None:
        weak = weak_topics(handle)
        weak_tags = [item["tag"] for item in weak]

    # A set turns each membership check below from O(len(weak_tags)) into
    # O(1). weak_tags is only ~5 items so the difference is negligible
    # at this scale, but it's the correct default and costs nothing.
    weak_tag_set = set(weak_tags)

    rating = get_user_rating(handle)
    solved = get_solved_problems(handle)

    db = SessionLocal()
    try:
        # Filter by rating range at the DB level instead of pulling every
        # problem row into Python and filtering there.
        problems = (
            db.query(Problem)
            .filter(Problem.rating.isnot(None))
            .filter(Problem.rating.between(rating - 200, rating + 200))
            .all()
        )
    finally:
        db.close()

    recommendations = []

    for problem in problems:

        if len(recommendations) >= 10:
            break

        if problem.name in solved:
            continue

        tags = [tag for tag in problem.tags.split(",") if tag.strip()]

        if any(tag in weak_tag_set for tag in tags):

            recommendations.append({
                "contest_id": problem.contest_id,
                "index": problem.problem_index,
                "name": problem.name,
                "rating": problem.rating,
                "tags": tags
            })

    return recommendations