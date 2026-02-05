from typing import Any

import pandas as pd
import plotly.express as px
import streamlit as st
from utils.api_client import api_client
from utils.session_state import get_current_user, logout_user, require_auth


def show_dashboard() -> None:
    require_auth()

    user = get_current_user()

    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        st.title(f"🏠 Dashboard - Welcome {user['username']}")

    with col2:
        if st.button("🔄 Refresh"):
            st.rerun()

    with col3:
        if st.button("🚪 Log Out"):
            logout_user()
            st.rerun()

    st.divider()

    show_user_info()

    show_stats()

    show_quick_actions()


def show_user_info() -> None:
    st.subheader("👤 My Profile")

    user = get_current_user()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Username", user["username"])
        st.metric("Email", user["email"])

    with col2:
        st.metric("Status", "🟢 Active" if user["is_active"] else "🔴 Inactive")
        st.metric("Type", "👑 Administrator" if user["is_superuser"] else "👤 User")

    with col3:
        if st.button("🔑 Change Password"):
            show_change_password_form()


def show_change_password_form() -> None:
    with st.expander("🔑 Change Password", expanded=True):
        with st.form("change_password_form"):
            current_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_new_password = st.text_input(
                "Confirm New Password", type="password"
            )

            if st.form_submit_button("Change Password"):
                if not current_password or not new_password:
                    st.error("Complete all fields.")
                    return

                if new_password != confirm_new_password:
                    st.error("New passwords don't match.")
                    return

                if len(new_password) < 6:
                    st.error("New password must have at least 6 characters.")
                    return

                try:
                    api_client.change_password(current_password, new_password)
                    st.success("Password changed successfully.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")


def show_stats() -> None:
    st.subheader("📊 Statistics")

    try:
        trainers_response = api_client.get_trainers(limit=1000)
        pokemon_response = api_client.get_pokemon(limit=1000)

        trainers: list[dict[str, Any]] = (
            trainers_response if isinstance(trainers_response, list) else []
        )
        pokemon: list[dict[str, Any]] = (
            pokemon_response if isinstance(pokemon_response, list) else []
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("👥 Trainers", len(trainers))

        with col2:
            st.metric("⚡ Pokémon", len(pokemon))

        with col3:
            total_teams = sum(trainer.get("team_size", 0) for trainer in trainers)
            st.metric("🎯 Pokémon in Teams", total_teams)

        with col4:
            if pokemon:
                avg_level = sum(p.get("level", 1) for p in pokemon) / len(pokemon)
                st.metric("📈 Average Level", f"{avg_level:.1f}")

        if trainers:
            show_trainer_charts(trainers)

        if pokemon:
            show_pokemon_charts(pokemon)

    except Exception as e:
        st.error(f"Error loading statistics: {str(e)}")


def show_trainer_charts(trainers: list[dict[str, Any]]) -> None:
    col1, col2 = st.columns(2)

    with col1:
        regions = [trainer.get("region", "Unknown") for trainer in trainers]
        region_df = pd.DataFrame({"Region": regions})
        region_counts = region_df["Region"].value_counts()

        fig = px.pie(
            values=region_counts.values,
            names=region_counts.index,
            title="Trainers by Region",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        genders = [trainer.get("gender", "Unknown") for trainer in trainers]
        gender_df = pd.DataFrame({"Gender": genders})
        gender_counts = gender_df["Gender"].value_counts()

        fig = px.bar(
            x=gender_counts.index,
            y=gender_counts.values,
            title="Trainers by Gender",
        )
        st.plotly_chart(fig, use_container_width=True)


def show_pokemon_charts(pokemon: list[dict[str, Any]]) -> None:
    col1, col2 = st.columns(2)

    with col1:
        types = [p.get("type_primary", "Unknown") for p in pokemon]
        type_df = pd.DataFrame({"Type": types})
        type_counts = type_df["Type"].value_counts().head(10)

        fig = px.bar(
            x=type_counts.values,
            y=type_counts.index,
            orientation="h",
            title="Top 10 Pokémon Types",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        levels = [p.get("level", 1) for p in pokemon]

        fig = px.histogram(x=levels, nbins=20, title="Level Distribution")
        st.plotly_chart(fig, use_container_width=True)


def show_quick_actions() -> None:
    st.subheader("⚡ Quick Actions")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("👥 Manage Trainers", use_container_width=True):
            st.session_state.current_page = "trainers"
            st.rerun()

    with col2:
        if st.button("⚡ Manage Pokémon", use_container_width=True):
            st.session_state.current_page = "pokemon"
            st.rerun()

    with col3:
        if st.button("🎯 Manage Teams", use_container_width=True):
            st.session_state.current_page = "teams"
            st.rerun()

    with col4:
        if st.button("🎒 Manage Items", use_container_width=True):
            st.session_state.current_page = "items"
            st.rerun()
