from typing import Any

import pandas as pd
import streamlit as st
from utils.api_client import api_client
from utils.session_state import require_auth


def show_trainers_page() -> None:
    require_auth()

    st.title("👥 Trainers Management")

    tab1, tab2, tab3 = st.tabs(["📋 List", "➕ Create", "✏️ Edit"])

    with tab1:
        show_trainers_list()

    with tab2:
        show_create_trainer_form()

    with tab3:
        show_edit_trainer_form()


def show_trainers_list() -> None:
    st.subheader("📋 Trainers List")

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        search_term = st.text_input(
            "🔍 Search trainer", placeholder="Search by name..."
        )

    with col2:
        region_filter = st.selectbox(
            "🌍 Filter by region",
            [
                "All",
                "kanto",
                "johto",
                "hoenn",
                "sinnoh",
                "unova",
                "kalos",
                "alola",
                "galar",
            ],
        )

    with col3:
        if st.button("🔄 Refresh List"):
            st.rerun()

    try:
        trainers_response = api_client.get_trainers(limit=1000)
        trainers: list[dict[str, Any]] = (
            trainers_response if isinstance(trainers_response, list) else []
        )

        if not trainers:
            st.info("No trainers registered.")
            return

        if search_term:
            trainers = [t for t in trainers if search_term.lower() in t["name"].lower()]

        if region_filter != "All":
            trainers = [t for t in trainers if t["region"] == region_filter]

        if trainers:
            display_data = []
            for trainer in trainers:
                pokemon_names = "No Pokémon"
                if trainer.get("pokemon_team") and len(trainer["pokemon_team"]) > 0:
                    names = [pokemon["name"] for pokemon in trainer["pokemon_team"]]
                    if len(names) <= 3:
                        pokemon_names = ", ".join(names)
                    else:
                        pokemon_names = (
                            ", ".join(names[:3]) + f" (+{len(names) - 3} more)"
                        )

                display_data.append(
                    {
                        "id": trainer["id"],
                        "name": trainer["name"],
                        "gender": trainer["gender"],
                        "region": trainer["region"],
                        "team_size": trainer.get("team_size", 0),
                        "pokemon_display": pokemon_names,
                    }
                )

            df = pd.DataFrame(display_data)

            st.dataframe(
                df,
                use_container_width=True,
                column_config={
                    "id": "ID",
                    "name": "Name",
                    "gender": "Gender",
                    "region": "Region",
                    "team_size": st.column_config.NumberColumn(
                        "Pokémon in Team",
                        help="Number of Pokémon in the team",
                        format="%d",
                    ),
                    "pokemon_display": st.column_config.TextColumn(
                        "Pokémon Team",
                        help="Names of Pokémon in the team",
                        width="large",
                    ),
                },
                hide_index=True,
            )

            st.info(f"📊 Showing {len(trainers)} trainers")

            selected_trainers = st.multiselect(
                "Select trainers for actions:",
                options=trainers,
                format_func=lambda x: f"{x['name']} (ID: {x['id']})",
            )

            if selected_trainers:
                col1, col2 = st.columns(2)

                with col1:
                    if st.button("👁️ View Details", type="primary"):
                        show_trainer_details(selected_trainers[0])

                with col2:
                    if st.button("🗑️ Delete Selected", type="secondary"):
                        delete_trainers(selected_trainers)

        else:
            st.warning("No trainers found with the applied filters.")

    except Exception as e:
        st.error(f"Error loading trainers: {str(e)}")


def show_create_trainer_form() -> None:
    st.subheader("➕ Create New Trainer")

    with st.form("create_trainer_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Name *", placeholder="Ash Ketchum")
            gender = st.selectbox("Gender *", ["male", "female", "other"])

        with col2:
            region = st.selectbox(
                "Region *",
                [
                    "kanto",
                    "johto",
                    "hoenn",
                    "sinnoh",
                    "unova",
                    "kalos",
                    "alola",
                    "galar",
                ],
            )

        submitted = st.form_submit_button("Create Trainer", type="primary")

        if submitted:
            if not name or not gender or not region:
                st.error("Please complete all required fields.")
                return

            try:
                trainer_data = {"name": name, "gender": gender, "region": region}

                with st.spinner("Creating trainer..."):
                    response = api_client.create_trainer(trainer_data)

                st.success(f"Trainer '{name}' created successfully!")
                st.balloons()

                st.json(response)

            except Exception as e:
                st.error(f"Error creating trainer: {str(e)}")


def show_edit_trainer_form() -> None:
    st.subheader("✏️ Edit Trainer")

    try:
        trainers_response = api_client.get_trainers(limit=1000)
        trainers: list[dict[str, Any]] = (
            trainers_response if isinstance(trainers_response, list) else []
        )

        if not trainers:
            st.info("No trainers to edit.")
            return

        selected_trainer = st.selectbox(
            "Select trainer to edit:",
            options=trainers,
            format_func=lambda x: f"{x['name']} (ID: {x['id']}, {x['region']})",
        )

        if selected_trainer:
            with st.form("edit_trainer_form"):
                col1, col2 = st.columns(2)

                with col1:
                    name = st.text_input("Name", value=selected_trainer["name"])
                    gender = st.selectbox(
                        "Gender",
                        ["male", "female", "other"],
                        index=["male", "female", "other"].index(
                            selected_trainer["gender"]
                        ),
                    )

                with col2:
                    regions = [
                        "kanto",
                        "johto",
                        "hoenn",
                        "sinnoh",
                        "unova",
                        "kalos",
                        "alola",
                        "galar",
                    ]
                    region = st.selectbox(
                        "Region",
                        regions,
                        index=regions.index(selected_trainer["region"]),
                    )

                submitted = st.form_submit_button("Update Trainer", type="primary")

                if submitted:
                    if not name or not gender or not region:
                        st.error("Please complete all fields.")
                        return

                    try:
                        trainer_data = {
                            "name": name,
                            "gender": gender,
                            "region": region,
                        }

                        with st.spinner("Updating trainer..."):
                            response = api_client.update_trainer(
                                selected_trainer["id"], trainer_data
                            )

                        st.success("Trainer updated successfully!")
                        st.json(response)

                    except Exception as e:
                        st.error(f"Error updating trainer: {str(e)}")

    except Exception as e:
        st.error(f"Error loading trainers: {str(e)}")


def show_trainer_details(trainer: dict[str, Any]) -> None:
    with st.expander(f"👁️ Details of {trainer['name']}", expanded=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("ID", trainer["id"])
            st.metric("Name", trainer["name"])

        with col2:
            st.metric("Gender", trainer["gender"])
            st.metric("Region", trainer["region"])

        with col3:
            st.metric("Pokémon in Team", trainer.get("team_size", 0))

        if trainer.get("pokemon_team"):
            st.subheader("🎯 Pokémon Team")
            for pokemon in trainer["pokemon_team"]:
                st.write(
                    f"⚡ {pokemon['name']} (Level {pokemon['level']}) - {pokemon['type_primary']}"
                )


def delete_trainers(trainers_to_delete: list[dict[str, Any]]) -> None:
    st.warning(f"Are you sure you want to delete {len(trainers_to_delete)} trainer(s)?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Yes, Delete", type="primary"):
            try:
                for trainer in trainers_to_delete:
                    api_client.delete_trainer(trainer["id"])

                st.success(
                    f"{len(trainers_to_delete)} trainer(s) deleted successfully!"
                )
                st.rerun()

            except Exception as e:
                st.error(f"Error deleting trainers: {str(e)}")

    with col2:
        if st.button("❌ Cancel"):
            st.rerun()
