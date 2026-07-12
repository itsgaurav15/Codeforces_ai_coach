from backend.services.analytics import (weak_topics,get_user_rating)
from backend.services.recommendation_service import recommend_problems

def generate_practice_plan(handle, weak_tags=None, recommendations=None):

       # Allow callers (e.g. the LangGraph pipeline) to pass already-computed
       # weak topics / recommendations instead of recomputing them here.
       rating=get_user_rating(handle)

       if weak_tags is None:
              weak=weak_topics(handle)
              weak_tags=[x['tag'] for x in weak]

       if recommendations is None:
              recommendations=recommend_problems(handle, weak_tags)

       plan={
              "current_rating":rating,
              "target_rating":rating+200
       }

       days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

       # Precompute each problem's tags as a set once, rather than
       # rebuilding it on every (day, problem) pair in the loop below.
       problems_with_tag_sets = [
              (problem, set(problem['tags']))
              for problem in recommendations
       ]

       for i in range(min(len(weak_tags),5)):
              topic=weak_tags[i]
              topic_problems=[]
              for problem, problem_tag_set in problems_with_tag_sets:
                     if topic in problem_tag_set:
                            topic_problems.append(
                                   {
                                          "name":problem["name"],
                                          "rating":problem["rating"]
                                   }
                            )
                     if len(topic_problems)==2:
                            break
              plan[days[i]]={
                     "topic":topic,
                     "problems":topic_problems
              }
       plan["saturday"]={
               "task":"virtual contest"
        }
       plan["sunday"]={"task":"upsolve contest problems"}
       return plan