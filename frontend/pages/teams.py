import streamlit as st


def show_teams_page() -> None:
    st.subheader("👥 Teams Management")

    tab1, tab2 = st.tabs(["View Teams", "Create Team"])

    with tab1:
        st.info("View teams functionality - Under construction")

    with tab2:
        st.info("Create teams functionality - Under construction")
