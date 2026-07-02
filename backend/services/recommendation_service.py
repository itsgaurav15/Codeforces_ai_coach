from backend.database import SessionLocal
from backend.models.submission import Submission
from backend.services.analytics import weak_topics
from backend.services.analytics import get_user_rating
from backend.models.problem import Problem

def get_solved_problems(handle):

    db = SessionLocal()

    solved = (
        db.query(Submission)
        .filter(
            Submission.handle == handle,
            Submission.verdict == "OK"
        )
        .all()
    )

    db.close()

    return {
        s.problem_name
        for s in solved
    }


def recommend_problems(handle):

    db = SessionLocal()

    weak = weak_topics(handle)

    weak_tags = [
        item["tag"]
        for item in weak
    ]

    rating = get_user_rating(handle)

    solved = get_solved_problems(handle)

    recommendations = []

    problems = db.query(Problem).all()

    for problem in problems:

        if len(recommendations) >= 10:
            break

        if problem.name in solved:
            continue

        if problem.rating is None:
            continue

        if abs(problem.rating - rating) > 200:
            continue

        tags = problem.tags.split(",")

        if any(tag in weak_tags for tag in tags):

            recommendations.append({

    "contest_id": problem.contest_id,

    "index": problem.problem_index,

    "name": problem.name,

    "rating": problem.rating,

    "tags": problem.tags.split(",")

})

    db.close()

    return recommendations