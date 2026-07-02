import streamlit as st


def show_recommendations(recommendations):

    st.header("💡 Recommended Problems")

    st.divider()

    for problem in recommendations:

        with st.container(border=True):

            st.subheader(problem["name"])

            st.write(f"⭐ **Rating:** {problem['rating']}")

            tags = " • ".join(problem["tags"])

            st.write(f"🏷️ {tags}")

            url = (
                f"https://codeforces.com/problemset/problem/"
                f"{problem['contest_id']}/"
                f"{problem['index']}"
            )

            st.link_button(
                "🔗 Open Problem",
                url
            )