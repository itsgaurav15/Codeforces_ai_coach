def build_coach_prompt(state):

    profile = state["profile"]
    analytics = state["analytics"]
    contest = state["contest_analysis"]
    plan = state["practice_plan"]
    recommendations = state["recommendations"]

    weak_topics = [
        topic["tag"]
        for topic in analytics.get("weak_topics", [])
    ]

    strong_topics = [
        topic["tag"]
        for topic in analytics.get("strong_topics", [])
    ]

    recs = "\n".join(
        [
            f"- {problem['name']} ({problem['rating']})"
            for problem in recommendations[:5]
        ]
    )

    prompt = f"""
You are an Expert Codeforces Coach.

Analyze the following student.

PROFILE

Handle:
{profile.get("handle")}

Current Rating:
{profile.get("rating")}

Maximum Rating:
{profile.get("maxRating")}

Country:
{profile.get("country")}

--------------------------------------------------

ANALYTICS

Overall Success Rate:
{analytics.get("overall_success_rate")}

Weak Topics:
{weak_topics}

Strong Topics:
{strong_topics}

--------------------------------------------------

CONTEST PERFORMANCE

Current Rating:
{contest.get("current_rating")}

Best Rating:
{contest.get("best_rating")}

Contest Trend:
{contest.get("trend")}

--------------------------------------------------

RECOMMENDED PROBLEMS

{recs}

--------------------------------------------------

PRACTICE PLAN

{plan}

--------------------------------------------------

Write a coaching report with the following sections.

1. Overall Assessment

2. Biggest Strengths

3. Biggest Weaknesses

4. Contest Performance Review

5. One Week Strategy

6. Motivation

Keep the report practical and personalized.
"""

    return prompt