import streamlit as st


def show_profile(profile, analytics):

    col1, col2 = st.columns([1,2])

    with col1:

        st.image(
            profile["titlePhoto"],
            width=170
        )

    with col2:

        st.subheader(profile["handle"])

        st.write(f"Rank : {profile['rank']}")

        st.write(f"Rating : {profile['rating']}")

        st.write(f"Maximum Rating : {profile['maxRating']}")

        st.write(f"Country : {profile.get('country','N/A')}")

        st.write(f"Organization : {profile.get('organization','N/A')}")

    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Current Rating",
        profile["rating"]
    )

    c2.metric(
        "Maximum Rating",
        profile["maxRating"]
    )

    c3.metric(
        "Success Rate",
        f"{analytics['overall_success_rate']}%"
    )

    st.progress(
        min(profile["rating"]/3000,1.0)
    )