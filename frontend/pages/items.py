import streamlit as st


def show_items_page() -> None:
    st.subheader("🎒 Items Management")

    tab1, tab2 = st.tabs(["View Items", "Create Item"])

    with tab1:
        st.info("View items functionality - Under construction")

    with tab2:
        st.info("Create items functionality - Under construction")
