import streamlit as st


def show_backpacks_page() -> None:
    st.subheader("🎒 Backpacks Management")

    tab1, tab2 = st.tabs(["View Backpack", "Add Item"])

    with tab1:
        st.info("View backpack functionality - Under construction")

    with tab2:
        st.info("Add items to backpack functionality - Under construction")
