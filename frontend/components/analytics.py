import streamlit as st


def show_analytics(analytics):

    st.header("📊 Analytics Dashboard")

    st.metric(
        "Overall Success Rate",
        f"{analytics['overall_success_rate']}%"
    )

    st.divider()

    col1, col2 = st.columns(2)

    # ---------------- Weak Topics ----------------

    with col1:

        st.subheader("🔴 Weak Topics")

        for topic in analytics["weak_topics"]:

            c1, c2 = st.columns([3, 1])

            with c1:
                st.write(topic["tag"])

            with c2:
                st.write(f"{topic['success_rate']}%")

            st.progress(topic["success_rate"] / 100)

    # ---------------- Strong Topics ----------------

    with col2:

        st.subheader("🟢 Strong Topics")

        for topic in analytics["strong_topics"]:

            c1, c2 = st.columns([3, 1])

            with c1:
                st.write(topic["tag"])

            with c2:
                st.write(f"{topic['success_rate']}%")

            st.progress(topic["success_rate"] / 100)