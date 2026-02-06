"""Dashboard page for Pokemon API frontend."""

from typing import Any

import streamlit as st
from utils.api_client import api_client
from utils.session_state import get_current_user, logout_user
from utils.validators import FormValidators

from pages.backpacks import show_backpacks_page
from pages.items import show_items_page
from pages.pokemon import show_pokemon_page
from pages.teams import show_teams_page


def show_dashboard() -> None:
    """Show main dashboard with navigation."""
    user_info = get_current_user()

    col1, col2 = st.columns([3, 1])

    with col1:
        st.title(f"🏠 Dashboard - Welcome {user_info['username']}")

    with col2:
        if st.button("Logout", type="secondary"):
            logout_user()
            st.rerun()

    st.sidebar.title("Navigation")

    page = st.sidebar.selectbox(
        "Select a page:",
        ["Dashboard", "Trainers", "Pokemon", "Teams", "Items", "Backpacks"],
    )

    if page == "Dashboard":
        show_main_dashboard()
    elif page == "Trainers":
        show_trainers_page()
    elif page == "Pokemon":
        show_pokemon_page()
    elif page == "Teams":
        show_teams_page()
    elif page == "Items":
        show_items_page()
    elif page == "Backpacks":
        show_backpacks_page()


def show_main_dashboard() -> None:
    """Show main dashboard overview."""
    st.subheader("📊 Overview")

    try:
        trainers = api_client.get_trainers()

        pokemon: list[dict[str, Any]] = []
        items: list[dict[str, Any]] = []
        teams: list[dict[str, Any]] = []
        backpacks: list[dict[str, Any]] = []

        try:
            pokemon = api_client.get_pokemon()
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"Warning: Could not load pokemon data: {e}")

        try:
            items = api_client.get_items()
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"Warning: Could not load items data: {e}")

        try:
            teams = api_client.get_teams()
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"Warning: Could not load teams data: {e}")

        try:
            backpacks = api_client.get_backpacks()
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"Warning: Could not load backpacks data: {e}")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Trainers", len(trainers))

        with col2:
            st.metric("Pokemon", len(pokemon))

        with col3:
            st.metric("Items", len(items))

        with col4:
            st.metric("Team Entries", len(teams))

        with col5:
            total_backpack_items = sum(bp.get("quantity", 0) for bp in backpacks)
            st.metric("Items in Backpacks", total_backpack_items)

        st.subheader("📈 Quick Stats")

        col1, col2 = st.columns(2)

        with col1:
            show_trainers_summary(trainers, teams)

        with col2:
            show_pokemon_summary(pokemon)

    except Exception as e:  # pylint: disable=broad-exception-caught
        st.error(f"Error loading dashboard data: {str(e)}")


def show_trainers_summary(
    trainers: list[dict[str, Any]], teams: list[dict[str, Any]]
) -> None:
    """Show summary of trainers."""
    st.write("**Trainers Summary**")

    if trainers:
        for trainer in trainers[:5]:
            team_count = len(
                [t for t in teams if t.get("trainer_id") == trainer.get("id")]
            )
            st.write(
                f"• {trainer['name']} ({trainer['region']}) - {team_count} Pokemon in team"
            )

        if len(trainers) > 5:
            st.write(f"... and {len(trainers) - 5} more trainers")
    else:
        st.info("No trainers yet. Create your first trainer!")


def show_pokemon_summary(pokemon: list[dict[str, Any]]) -> None:
    """Show summary of pokemon."""
    st.write("**Pokemon Summary**")

    if pokemon:
        type_counts: dict[str, int] = {}
        for poke in pokemon:
            poke_type = poke.get("type_primary", "unknown")
            type_counts[poke_type] = type_counts.get(poke_type, 0) + 1

        sorted_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
        for poke_type, count in sorted_types[:5]:
            st.write(f"• {poke_type.title()}: {count} Pokemon")

        levels = [p.get("level", 1) for p in pokemon]
        if levels:
            avg_level = sum(levels) / len(levels)
            max_level = max(levels)
            st.write(f"• Average Level: {avg_level:.1f}")
            st.write(f"• Highest Level: {max_level}")
    else:
        st.info("No Pokemon yet. Start catching some!")


def show_trainers_page() -> None:
    """Show trainers management page."""
    st.subheader("👨‍🎓 Trainers Management")

    tab1, tab2 = st.tabs(["View Trainers", "Create Trainer"])

    with tab1:
        show_trainers_list()

    with tab2:
        show_create_trainer_form()


def show_trainers_list() -> None:
    """Show list of trainers."""
    try:
        trainers = api_client.get_trainers()

        if trainers:
            search_term = st.text_input(
                "🔍 Search Trainers", placeholder="Enter trainer name or region..."
            )

            if search_term:
                trainers = [
                    t
                    for t in trainers
                    if search_term.lower() in t["name"].lower()
                    or search_term.lower() in t["region"].lower()
                ]

            if trainers:
                for trainer in trainers:
                    show_trainer_card(trainer)
            else:
                st.info("No trainers found matching your search.")
        else:
            st.info("No trainers registered yet.")

    except Exception as e:  # pylint: disable=broad-exception-caught
        st.error(f"Error loading trainers: {str(e)}")


def show_trainer_card(trainer: dict[str, Any]) -> None:
    """Show individual trainer card."""
    with st.expander(f"🎓 {trainer['name']} - {trainer['region']}"):
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            st.write(f"**ID:** {trainer['id']}")
            st.write(f"**Gender:** {trainer['gender']}")
            st.write(f"**Region:** {trainer['region']}")
            team_size = trainer.get("team_size", 0)
            st.write(f"**Team Size:** {team_size} Pokemon")

        with col2:
            if st.button("✏️ Edit", key=f"edit_trainer_{trainer['id']}"):
                st.session_state[f"editing_trainer_{trainer['id']}"] = True
                st.rerun()

        with col3:
            if st.button(
                "🗑️ Delete", key=f"delete_trainer_{trainer['id']}", type="secondary"
            ):
                handle_trainer_deletion(trainer["id"])

        if st.session_state.get(f"editing_trainer_{trainer['id']}", False):
            show_edit_trainer_form(trainer)


def handle_trainer_deletion(trainer_id: int) -> None:
    """Handle trainer deletion with confirmation."""
    confirm_key = f"confirm_delete_trainer_{trainer_id}"

    if st.session_state.get(confirm_key, False):
        try:
            api_client.delete_trainer(trainer_id)
            st.success("Trainer deleted successfully!")
            st.session_state[confirm_key] = False
            st.rerun()
        except Exception as e:  # pylint: disable=broad-exception-caught
            st.error(f"Error deleting trainer: {str(e)}")
    else:
        st.session_state[confirm_key] = True
        st.warning("Click delete again to confirm")


def show_create_trainer_form() -> None:
    """Show form to create new trainer."""
    with st.form("create_trainer_form"):
        st.subheader("Create New Trainer")

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Trainer Name*", placeholder="Enter trainer name")
            gender = st.selectbox("Gender*", FormValidators.get_trainer_genders())

        with col2:
            region = st.selectbox("Region*", FormValidators.get_trainer_regions())

        submitted = st.form_submit_button("Create Trainer", type="primary")

        if submitted:
            handle_create_trainer_submission(name, gender, region)


def handle_create_trainer_submission(name: str, gender: str, region: str) -> None:
    """Handle trainer creation form submission."""
    name_valid, name_error = FormValidators.validate_trainer_name(name)

    if not name_valid:
        st.error(f"Invalid name: {name_error}")
        return

    try:
        trainer_data = {"name": name, "gender": gender, "region": region}

        with st.spinner("Creating trainer..."):
            response = api_client.create_trainer(trainer_data)

        st.success(f"Trainer '{name}' created successfully!")
        st.json(response)

    except Exception as e:  # pylint: disable=broad-exception-caught
        st.error(f"Error creating trainer: {str(e)}")


def show_edit_trainer_form(trainer: dict[str, Any]) -> None:
    """Show form to edit existing trainer."""
    form_key = f"edit_trainer_form_{trainer['id']}"

    with st.form(form_key):
        st.subheader(f"Edit {trainer['name']}")

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Trainer Name*", value=trainer["name"])
            gender = st.selectbox(
                "Gender*",
                FormValidators.get_trainer_genders(),
                index=FormValidators.get_trainer_genders().index(trainer["gender"]),
            )

        with col2:
            region = st.selectbox(
                "Region*",
                FormValidators.get_trainer_regions(),
                index=FormValidators.get_trainer_regions().index(trainer["region"]),
            )

        col1, col2 = st.columns(2)

        with col1:
            submitted = st.form_submit_button("Update Trainer", type="primary")

        with col2:
            cancelled = st.form_submit_button("Cancel")

        if cancelled:
            st.session_state[f"editing_trainer_{trainer['id']}"] = False
            st.rerun()

        if submitted:
            handle_edit_trainer_submission(trainer["id"], name, gender, region)


def handle_edit_trainer_submission(
    trainer_id: int, name: str, gender: str, region: str
) -> None:
    """Handle trainer edit form submission."""
    name_valid, name_error = FormValidators.validate_trainer_name(name)

    if not name_valid:
        st.error(f"Invalid name: {name_error}")
        return

    try:
        trainer_data = {"name": name, "gender": gender, "region": region}

        with st.spinner("Updating trainer..."):
            api_client.update_trainer(trainer_id, trainer_data)

        st.success("Trainer updated successfully!")
        st.session_state[f"editing_trainer_{trainer_id}"] = False
        st.rerun()

    except Exception as e:  # pylint: disable=broad-exception-caught
        st.error(f"Error updating trainer: {str(e)}")
