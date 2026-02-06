"""Teams management page for Pokemon API frontend."""

from typing import Any

import pandas as pd
import streamlit as st
from utils.api_client import api_client
from utils.session_state import require_auth


def show_teams_page() -> None:
    """Show teams management page."""
    require_auth()

    st.title("🎯 Teams Management")

    tab1, tab2, tab3 = st.tabs(["📋 List", "➕ Manage", "🔄 Positions"])

    with tab1:
        show_teams_list()

    with tab2:
        show_team_management()

    with tab3:
        show_position_management()


def show_teams_list() -> None:
    """Show list of teams with management options."""
    st.subheader("📋 Teams List")

    search_term, size_filter = _get_teams_filters()

    try:
        teams = _fetch_teams_data()
        if not teams:
            st.info("No teams found.")
            return

        filtered_teams = _apply_teams_filters(teams, search_term, size_filter)

        if filtered_teams:
            show_teams_statistics(filtered_teams)
            _display_teams(filtered_teams)
        else:
            st.warning("No teams found with the applied filters.")

    except Exception as e:
        st.error(f"Error loading teams: {str(e)}")


def _get_teams_filters() -> tuple[str, str]:
    """Get filter inputs for teams list."""
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        search_term = st.text_input(
            "🔍 Search trainer", placeholder="Search by trainer name..."
        )

    with col2:
        size_filter = st.selectbox(
            "👥 Filter by team size",
            ["All", "1", "2", "3", "4", "5", "6"],
        )

    with col3:
        if st.button("🔄 Refresh List"):
            st.rerun()

    return search_term, size_filter


def _fetch_teams_data() -> list[dict[str, Any]]:
    """Fetch teams data from API."""
    teams_response = api_client.get_all_teams()
    return teams_response if isinstance(teams_response, list) else []


def _apply_teams_filters(
    teams: list[dict[str, Any]], search_term: str, size_filter: str
) -> list[dict[str, Any]]:
    """Apply search and size filters to teams list."""
    filtered_teams = teams

    if search_term:
        filtered_teams = [
            t
            for t in filtered_teams
            if search_term.lower() in t.get("trainer_name", "").lower()
        ]

    if size_filter != "All":
        filtered_teams = [
            t for t in filtered_teams if t.get("team_size") == int(size_filter)
        ]

    return filtered_teams


def _display_teams(teams: list[dict[str, Any]]) -> None:
    """Display team cards."""
    for team in teams:
        show_team_card(team)


def show_teams_statistics(teams: list[dict[str, Any]]) -> None:
    """Show statistics about teams."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Teams", len(teams))

    with col2:
        team_sizes = [t.get("team_size", 0) for t in teams]
        avg_size = sum(team_sizes) / len(team_sizes) if team_sizes else 0
        st.metric("Average Team Size", f"{avg_size:.1f}")

    with col3:
        full_teams = sum(1 for t in teams if t.get("team_size", 0) == 6)
        st.metric("Full Teams (6/6)", full_teams)

    with col4:
        avg_level = _calculate_average_team_level(teams)
        st.metric("Avg Pokémon Level", f"{avg_level:.1f}")


def _calculate_average_team_level(teams: list[dict[str, Any]]) -> float:
    """Calculate average level across all team members."""
    all_levels = []
    for team in teams:
        members = team.get("members", [])
        for member in members:
            all_levels.append(member.get("pokemon_level", 1))

    return sum(all_levels) / len(all_levels) if all_levels else 0


def show_team_card(team: dict[str, Any]) -> None:
    """Show individual team card with management options."""
    trainer_name = team.get("trainer_name", "Unknown")
    team_size = team.get("team_size", 0)
    members = team.get("members", [])

    with st.expander(f"🎯 {trainer_name}'s Team ({team_size}/6)", expanded=False):
        if not members:
            st.info("This team has no Pokémon.")
            return

        col1, col2 = st.columns([3, 1])

        with col1:
            _show_team_roster(members)

        with col2:
            _show_team_actions(team, members)


def _show_team_roster(members: list[dict[str, Any]]) -> None:
    """Show team roster table."""
    st.write("**Team Roster:**")

    # Sort members by position
    sorted_members = sorted(members, key=lambda x: x.get("position", 1))

    # Create table data
    team_data = []
    for member in sorted_members:
        team_data.append(
            {
                "Position": member.get("position", 1),
                "Pokémon": member.get("pokemon_name", "Unknown"),
                "Type": member.get("pokemon_type", "unknown"),
                "Level": member.get("pokemon_level", 1),
                "Status": "Active" if member.get("is_active", True) else "Inactive",
            }
        )

    if team_data:
        df = pd.DataFrame(team_data)
        st.dataframe(
            df,
            use_container_width=True,
            column_config={
                "Position": st.column_config.NumberColumn("Pos", format="%d"),
                "Pokémon": "Name",
                "Type": "Type",
                "Level": st.column_config.NumberColumn("Lvl", format="%d"),
                "Status": "Status",
            },
            hide_index=True,
        )


def _show_team_actions(team: dict[str, Any], members: list[dict[str, Any]]) -> None:
    """Show team action buttons."""
    st.write("**Actions:**")

    trainer_id = team.get("trainer_id")
    trainer_name = team.get("trainer_name", "Unknown")

    if trainer_id:
        if st.button(
            "✏️ Manage Team",
            key=f"manage_team_{trainer_id}",
            use_container_width=True,
        ):
            st.session_state["selected_trainer_for_management"] = trainer_id
            st.session_state["selected_trainer_name"] = trainer_name
            st.rerun()

        if st.button(
            "🔄 Positions",
            key=f"positions_team_{trainer_id}",
            use_container_width=True,
        ):
            st.session_state["selected_trainer_for_positions"] = trainer_id
            st.session_state["selected_trainer_name"] = trainer_name
            st.rerun()

    # Team strength indicator
    total_levels = sum(member.get("pokemon_level", 1) for member in members)
    st.metric("Team Strength", total_levels)


def show_team_management() -> None:
    """Show team management interface."""
    st.subheader("➕ Team Management")

    try:
        trainers = api_client.get_trainers(limit=1000)
        if not trainers:
            st.info("No trainers available.")
            return

        selected_trainer_id = st.session_state.get("selected_trainer_for_management")
        selected_trainer_name = st.session_state.get("selected_trainer_name")

        if selected_trainer_id and selected_trainer_name:
            _show_selected_trainer_management(
                selected_trainer_id, selected_trainer_name
            )
        else:
            _show_trainer_selection_for_management(trainers)

    except Exception as e:
        st.error(f"Error loading trainers: {str(e)}")


def _show_selected_trainer_management(trainer_id: int, trainer_name: str) -> None:
    """Show management for selected trainer."""
    st.info(f"Managing team for: **{trainer_name}**")

    if st.button("🔙 Back to Trainer Selection"):
        st.session_state.pop("selected_trainer_for_management", None)
        st.session_state.pop("selected_trainer_name", None)
        st.rerun()

    show_trainer_team_management(trainer_id)


def _show_trainer_selection_for_management(trainers: list[dict[str, Any]]) -> None:
    """Show trainer selection interface for management."""
    trainer = st.selectbox(
        "Select trainer to manage:",
        options=trainers,
        format_func=lambda x: f"{x['name']} (ID: {x['id']}) - {x['region']}",
    )

    if trainer and st.button("Manage This Trainer's Team", type="primary"):
        st.session_state["selected_trainer_for_management"] = trainer["id"]
        st.session_state["selected_trainer_name"] = trainer["name"]
        st.rerun()


def show_trainer_team_management(trainer_id: int) -> None:
    """Show management interface for a specific trainer's team."""
    try:
        team = api_client.get_trainer_team(trainer_id)
        current_members = team.get("members", [])

        col1, col2 = st.columns(2)

        with col1:
            _show_add_pokemon_section(trainer_id, current_members)

        with col2:
            _show_current_team_section(trainer_id, current_members)

    except Exception as e:
        st.error(f"Error loading team: {str(e)}")


def _show_add_pokemon_section(
    trainer_id: int, current_members: list[dict[str, Any]]
) -> None:
    """Show section for adding Pokemon to team."""
    st.write("### Add Pokémon to Team")

    if len(current_members) >= 6:
        st.warning("Team is full (6/6 Pokémon)")
        return

    all_pokemon = api_client.get_pokemon(limit=1000)
    current_pokemon_ids = [m.get("pokemon_id") for m in current_members]
    available_pokemon = [p for p in all_pokemon if p["id"] not in current_pokemon_ids]

    if not available_pokemon:
        st.info("No available Pokémon to add to team.")
        return

    _show_add_pokemon_form(trainer_id, available_pokemon, current_members)


def _show_add_pokemon_form(
    trainer_id: int,
    available_pokemon: list[dict[str, Any]],
    current_members: list[dict[str, Any]],
) -> None:
    """Show form to add Pokemon to team."""
    with st.form(f"add_pokemon_form_{trainer_id}"):
        selected_pokemon = st.selectbox(
            "Select Pokémon:",
            options=available_pokemon,
            format_func=lambda x: f"{x['name']} (Level {x.get('level', 1)}) - {x.get('type_primary', 'unknown')}",
        )

        # Get available positions
        occupied_positions = [m.get("position") for m in current_members]
        available_positions = [i for i in range(1, 7) if i not in occupied_positions]
        position = st.selectbox("Position:", available_positions)

        if st.form_submit_button("Add to Team", type="primary"):
            _handle_add_pokemon_to_team(trainer_id, selected_pokemon, position)


def _handle_add_pokemon_to_team(
    trainer_id: int, selected_pokemon: dict[str, Any], position: int
) -> None:
    """Handle adding Pokemon to team."""
    try:
        team_data = {
            "trainer_id": trainer_id,
            "pokemon_id": selected_pokemon["id"],
            "position": position,
        }

        with st.spinner("Adding Pokémon to team..."):
            api_client.add_pokemon_to_team(team_data)

        st.success(f"Added {selected_pokemon['name']} to team!")
        st.rerun()

    except Exception as e:
        st.error(f"Error adding Pokémon: {str(e)}")


def _show_current_team_section(
    trainer_id: int, current_members: list[dict[str, Any]]
) -> None:
    """Show current team section."""
    st.write("### Current Team")

    if not current_members:
        st.info("Team is empty.")
        return

    for member in sorted(current_members, key=lambda x: x.get("position", 1)):
        _show_team_member(trainer_id, member)


def _show_team_member(trainer_id: int, member: dict[str, Any]) -> None:
    """Show individual team member with remove option."""
    with st.container():
        col_info, col_action = st.columns([3, 1])

        with col_info:
            st.write(
                f"**Position {member.get('position')}:** "
                f"{member.get('pokemon_name')} "
                f"(Level {member.get('pokemon_level')}) - "
                f"{member.get('pokemon_type')}"
            )

        with col_action:
            if st.button(
                "🗑️",
                key=f"remove_{trainer_id}_{member.get('pokemon_id')}",
                help="Remove from team",
                use_container_width=True,
            ):
                _handle_remove_pokemon_from_team(trainer_id, member)


def _handle_remove_pokemon_from_team(trainer_id: int, member: dict[str, Any]) -> None:
    """Handle removing Pokemon from team."""
    try:
        with st.spinner("Removing Pokémon..."):
            api_client.remove_pokemon_from_team(trainer_id, member.get("pokemon_id"))

        st.success(f"Removed {member.get('pokemon_name')} from team!")
        st.rerun()

    except Exception as e:
        st.error(f"Error removing Pokémon: {str(e)}")


def show_position_management() -> None:
    """Show position management interface."""
    st.subheader("🔄 Position Management")

    try:
        trainers = api_client.get_trainers(limit=1000)
        if not trainers:
            st.info("No trainers available.")
            return

        selected_trainer_id = st.session_state.get("selected_trainer_for_positions")
        selected_trainer_name = st.session_state.get("selected_trainer_name")

        if selected_trainer_id and selected_trainer_name:
            _show_selected_trainer_positions(selected_trainer_id, selected_trainer_name)
        else:
            _show_trainer_selection_for_positions(trainers)

    except Exception as e:
        st.error(f"Error loading trainers: {str(e)}")


def _show_selected_trainer_positions(trainer_id: int, trainer_name: str) -> None:
    """Show position management for selected trainer."""
    st.info(f"Managing positions for: **{trainer_name}**")

    if st.button("🔙 Back to Trainer Selection"):
        st.session_state.pop("selected_trainer_for_positions", None)
        st.session_state.pop("selected_trainer_name", None)
        st.rerun()

    show_trainer_position_management(trainer_id)


def _show_trainer_selection_for_positions(trainers: list[dict[str, Any]]) -> None:
    """Show trainer selection for position management."""
    trainer = st.selectbox(
        "Select trainer to manage positions:",
        options=trainers,
        format_func=lambda x: f"{x['name']} (ID: {x['id']}) - {x['region']}",
        key="position_trainer_select",
    )

    if trainer and st.button("Manage Positions", type="primary"):
        st.session_state["selected_trainer_for_positions"] = trainer["id"]
        st.session_state["selected_trainer_name"] = trainer["name"]
        st.rerun()


def show_trainer_position_management(trainer_id: int) -> None:
    """Show position management for a specific trainer."""
    try:
        team = api_client.get_trainer_team(trainer_id)
        members = team.get("members", [])

        if not members:
            st.info("This trainer has no Pokémon in their team.")
            return

        st.write("### Current Team Positions")
        _show_position_controls(trainer_id, members)

        st.write("### Team Overview")
        _show_team_overview(members)

    except Exception as e:
        st.error(f"Error loading team positions: {str(e)}")


def _show_position_controls(trainer_id: int, members: list[dict[str, Any]]) -> None:
    """Show position control interfaces."""
    sorted_members = sorted(members, key=lambda x: x.get("position", 1))

    for member in sorted_members:
        with st.container():
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.write(
                    f"**{member.get('pokemon_name')}** "
                    f"(Level {member.get('pokemon_level')}) - "
                    f"{member.get('pokemon_type')}"
                )

            with col2:
                st.write(f"Position: **{member.get('position')}**")

            with col3:
                _show_position_selector(trainer_id, member)


def _show_position_selector(trainer_id: int, member: dict[str, Any]) -> None:
    """Show position selector for a team member."""
    new_position = st.selectbox(
        "New Position:",
        options=list(range(1, 7)),
        index=member.get("position", 1) - 1,
        key=f"pos_{trainer_id}_{member.get('pokemon_id')}",
    )

    if new_position != member.get("position"):
        if st.button(
            "Update",
            key=f"update_pos_{trainer_id}_{member.get('pokemon_id')}",
            use_container_width=True,
        ):
            _handle_position_update(trainer_id, member, new_position)


def _handle_position_update(
    trainer_id: int, member: dict[str, Any], new_position: int
) -> None:
    """Handle position update for team member."""
    try:
        with st.spinner("Updating position..."):
            api_client.update_pokemon_position(
                trainer_id,
                member.get("pokemon_id"),
                new_position,
            )

        st.success(f"Updated {member.get('pokemon_name')}'s position!")
        st.rerun()

    except Exception as e:
        st.error(f"Error updating position: {str(e)}")


def _show_team_overview(members: list[dict[str, Any]]) -> None:
    """Show team overview grid."""
    positions_grid = [""] * 6

    for member in members:
        pos = member.get("position", 1) - 1
        if 0 <= pos < 6:
            positions_grid[pos] = (
                f"{member.get('pokemon_name')} (Lvl {member.get('pokemon_level')})"
            )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("**Position 1:**", positions_grid[0] or "Empty")
        st.write("**Position 2:**", positions_grid[1] or "Empty")

    with col2:
        st.write("**Position 3:**", positions_grid[2] or "Empty")
        st.write("**Position 4:**", positions_grid[3] or "Empty")

    with col3:
        st.write("**Position 5:**", positions_grid[4] or "Empty")
        st.write("**Position 6:**", positions_grid[5] or "Empty")


def show_team_details(team: dict[str, Any]) -> None:
    """Show detailed information about a team."""
    trainer_name = team.get("trainer_name", "Unknown")
    members = team.get("members", [])

    with st.expander(f"👁️ Details of {trainer_name}'s Team", expanded=True):
        _show_team_metrics(team, members)

        if members:
            _show_team_members_details(members)


def _show_team_metrics(team: dict[str, Any], members: list[dict[str, Any]]) -> None:
    """Show team metrics."""
    trainer_name = team.get("trainer_name", "Unknown")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Trainer", trainer_name)
        st.metric("Team Size", team.get("team_size", 0))

    with col2:
        total_levels = sum(member.get("pokemon_level", 1) for member in members)
        st.metric("Total Levels", total_levels)

        avg_level = total_levels / len(members) if members else 0
        st.metric("Average Level", f"{avg_level:.1f}")

    with col3:
        # Type distribution
        types = [member.get("pokemon_type", "unknown") for member in members]
        unique_types = len(set(types))
        st.metric("Unique Types", unique_types)

        active_members = sum(1 for member in members if member.get("is_active", True))
        st.metric("Active Members", active_members)


def _show_team_members_details(members: list[dict[str, Any]]) -> None:
    """Show detailed team members list."""
    st.subheader("🎯 Team Members")
    sorted_members = sorted(members, key=lambda x: x.get("position", 1))

    for member in sorted_members:
        status_emoji = "✅" if member.get("is_active", True) else "❌"
        st.write(
            f"{status_emoji} **Position {member.get('position')}:** "
            f"{member.get('pokemon_name')} "
            f"(Level {member.get('pokemon_level')}) - "
            f"{member.get('pokemon_type')}"
        )
