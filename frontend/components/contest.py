import streamlit as st


def show_contest(contest):

    st.header("📈 Contest Performance")

    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Current Rating",
        contest["current_rating"]
    )

    c2.metric(
        "Best Rating",
        contest["best_rating"]
    )

    trend = contest["trend"]

    icon = "📈" if trend == "Improving" else (
        "📉" if trend == "Declining" else "➡️"
    )

    c3.metric(
        "Trend",
        f"{icon} {trend}"
    )

    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Largest Gain",
        f"+{contest['largest_gain']}"
    )

    c2.metric(
        "Largest Loss",
        contest["largest_loss"]
    )

    c3.metric(
        "Average Gain",
        round(contest["average_gain"], 2)
    )

    st.divider()

    c1, c2 = st.columns(2)

    c1.metric(
        "Contests Participated",
        contest["contests_participated"]
    )

    c2.metric(
        "Latest Rank",
        contest["latest_rank"]
    )

    st.divider()

    st.subheader("🏆 Latest Contest")

    st.info(contest["last_contest"])