import streamlit as st
from api import get_coach
from components.profile import show_profile
from components.analytics import show_analytics
from components.contest import show_contest
from components.recommendations import show_recommendations

st.set_page_config(
    page_title="Codeforces AI Coach",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Codeforces AI Coach")
st.write("Analyze your Codeforces profile using AI.")

handle = st.text_input("Enter Codeforces Handle")

if st.button("Analyze"):

    if handle == "":
        st.warning("Please enter a handle.")

    else:

        with st.spinner("Analyzing..."):

            data = get_coach(handle)

        if data:

            profile = data["profile"]
            analytics = data["analytics"]
            contest=data['contest_analysis']
            recommendations = data["recommendations"]
            st.success("Analysis Complete!")

            # ---------------- Sidebar ----------------

            with st.sidebar:

                st.header("Navigation")

                st.success(profile["handle"])

                st.write(profile["rank"])

                st.write(f"Rating : {profile['rating']}")

                st.write("AI Coach Dashboard")

            # ---------------- Progress Bar ----------------

            progress = min(profile["rating"] / 3000, 1.0)

            st.progress(progress)

            st.caption(
                f"{profile['rating']} / 3000 Rating"
            )

            # ---------------- Profile ----------------

            show_profile(profile, analytics)

            show_analytics(analytics)

            show_contest(contest)
            show_recommendations(recommendations)
        else:

            st.error("Unable to fetch data.")