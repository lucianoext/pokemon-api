"""Pokemon management page for Pokemon API frontend."""

import json
from typing import Any

import streamlit as st
from utils.api_client import api_client
from utils.validators import FormValidators


def show_pokemon_page() -> None:
    """Show pokemon management page."""
    st.title("⚡ Pokemon Management")

    tab1, tab2, tab3 = st.tabs(["📋 List", "➕ Create", "📈 Analytics"])

    with tab1:
        show_pokemon_list()

    with tab2:
        show_create_pokemon_form()

    with tab3:
        show_pokemon_analytics()


def show_pokemon_list() -> None:
    """Show list of pokemon with management options."""
    st.subheader("📋 Pokemon List")

    search_term, type_filter = _get_list_filters()

    try:
        pokemon_list = _fetch_pokemon_data()
        if not pokemon_list:
            st.info("No pokemon registered.")
            return

        filtered_pokemon = _apply_pokemon_filters(
            pokemon_list, search_term, type_filter
        )

        if filtered_pokemon:
            show_pokemon_statistics(filtered_pokemon)
            _display_pokemon_cards(filtered_pokemon)
        else:
            st.warning("No pokemon found with the applied filters.")

    except Exception as e:
        st.error(f"Error loading pokemon: {str(e)}")


def _get_list_filters() -> tuple[str, str]:
    """Get search and filter inputs for pokemon list."""
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        search_term = st.text_input(
            "🔍 Search pokemon", placeholder="Search by name..."
        )

    with col2:
        type_filter = st.selectbox(
            "🔥 Filter by type",
            ["All"] + FormValidators.get_pokemon_types(),
        )

    with col3:
        if st.button("🔄 Refresh List"):
            st.rerun()

    return search_term, type_filter


def _fetch_pokemon_data() -> list[dict[str, Any]]:
    """Fetch pokemon data from API."""
    pokemon_response = api_client.get_pokemon(limit=1000)
    return pokemon_response if isinstance(pokemon_response, list) else []


def _apply_pokemon_filters(
    pokemon_list: list[dict[str, Any]], search_term: str, type_filter: str
) -> list[dict[str, Any]]:
    """Apply search and type filters to pokemon list."""
    filtered = pokemon_list

    if search_term:
        filtered = [p for p in filtered if search_term.lower() in p["name"].lower()]

    if type_filter != "All":
        filtered = [
            p
            for p in filtered
            if p.get("type_primary") == type_filter
            or p.get("type_secondary") == type_filter
        ]

    # Sort by name
    filtered.sort(key=lambda x: x["name"].lower())
    return filtered


def _display_pokemon_cards(pokemon_list: list[dict[str, Any]]) -> None:
    """Display pokemon cards."""
    for pokemon in pokemon_list:
        show_pokemon_card(pokemon)


def show_pokemon_statistics(pokemon_list: list[dict[str, Any]]) -> None:
    """Show statistics about pokemon."""
    col1, col2, col3, col4 = st.columns(4)

    levels = [p.get("level", 1) for p in pokemon_list]

    with col1:
        st.metric("Total Pokemon", len(pokemon_list))

    with col2:
        avg_level = sum(levels) / len(levels) if levels else 0
        st.metric("Average Level", f"{avg_level:.1f}")

    with col3:
        max_level = max(levels) if levels else 0
        st.metric("Highest Level", max_level)

    with col4:
        unique_types = _count_unique_types(pokemon_list)
        st.metric("Unique Types", unique_types)


def _count_unique_types(pokemon_list: list[dict[str, Any]]) -> int:
    """Count unique types in pokemon list."""
    types = set()
    for pokemon in pokemon_list:
        types.add(pokemon.get("type_primary", ""))
        if pokemon.get("type_secondary"):
            types.add(pokemon.get("type_secondary", ""))
    return len(types)


def show_pokemon_card(pokemon: dict[str, Any]) -> None:
    """Show individual pokemon card with management options."""
    level = pokemon.get("level", 1)
    type_display = _get_type_display(pokemon)

    with st.expander(
        f"⚡ {pokemon['name']} (Level {level}) - {type_display}", expanded=False
    ):
        col1, col2 = st.columns([2, 1])

        with col1:
            _show_pokemon_info(pokemon, type_display)

        with col2:
            _show_pokemon_actions(pokemon)

        _handle_pokemon_forms(pokemon)


def _get_type_display(pokemon: dict[str, Any]) -> str:
    """Get formatted type display string."""
    pokemon_type = pokemon.get("type_primary", "unknown")
    secondary_type = pokemon.get("type_secondary")

    if secondary_type:
        return f"{pokemon_type}/{secondary_type}"
    return str(pokemon_type)


def _show_pokemon_info(pokemon: dict[str, Any], type_display: str) -> None:
    """Show pokemon information."""
    pokemon_id = pokemon["id"]
    nature = pokemon.get("nature", "unknown")

    st.write(f"**ID:** {pokemon_id}")
    st.write(f"**Type:** {type_display}")
    st.write(f"**Nature:** {nature}")

    attacks = _parse_attacks(pokemon.get("attacks", []))
    _display_attacks(attacks)


def _parse_attacks(attacks: Any) -> list[str]:
    """Parse attacks from various formats."""
    if isinstance(attacks, str):
        try:
            parsed = json.loads(attacks)
            return list(parsed) if isinstance(parsed, list) else []
        except (json.JSONDecodeError, TypeError):
            return []
    return list(attacks) if isinstance(attacks, list) else []


def _display_attacks(attacks: list[str]) -> None:
    """Display pokemon attacks."""
    if attacks:
        st.write("**Attacks:**")
        for i, attack in enumerate(attacks, 1):
            st.write(f"  {i}. {attack}")
    else:
        st.write("**Attacks:** None learned")


def _show_pokemon_actions(pokemon: dict[str, Any]) -> None:
    """Show pokemon action buttons."""
    pokemon_id = pokemon["id"]

    st.write("**Actions:**")

    col_edit, col_delete = st.columns(2)

    with col_edit:
        if st.button(
            "✏️ Edit",
            key=f"edit_pokemon_{pokemon_id}",
            use_container_width=True,
        ):
            st.session_state[f"editing_pokemon_{pokemon_id}"] = True
            st.rerun()

    with col_delete:
        if st.button(
            "🗑️ Delete",
            key=f"delete_pokemon_{pokemon_id}",
            type="secondary",
            use_container_width=True,
        ):
            _handle_pokemon_deletion(pokemon_id)

    col_level, col_attack = st.columns(2)

    with col_level:
        if st.button(
            "📈 Level Up",
            key=f"levelup_{pokemon_id}",
            use_container_width=True,
        ):
            _handle_level_up(pokemon_id, pokemon["name"])

    with col_attack:
        if st.button(
            "⚔️ Learn Attack",
            key=f"attack_{pokemon_id}",
            use_container_width=True,
        ):
            st.session_state[f"learning_attack_{pokemon_id}"] = True
            st.rerun()


def _handle_pokemon_forms(pokemon: dict[str, Any]) -> None:
    """Handle pokemon editing and attack learning forms."""
    pokemon_id = pokemon["id"]

    if st.session_state.get(f"editing_pokemon_{pokemon_id}", False):
        show_edit_pokemon_form(pokemon)

    if st.session_state.get(f"learning_attack_{pokemon_id}", False):
        show_learn_attack_form(pokemon)


def _handle_pokemon_deletion(pokemon_id: int) -> None:
    """Handle pokemon deletion with confirmation."""
    confirm_key = f"confirm_delete_pokemon_{pokemon_id}"

    if st.session_state.get(confirm_key, False):
        try:
            api_client.delete_pokemon(pokemon_id)
            st.success("Pokemon deleted successfully!")
            st.session_state[confirm_key] = False
            st.rerun()
        except Exception as e:
            st.error(f"Error deleting pokemon: {str(e)}")
    else:
        st.session_state[confirm_key] = True
        st.warning("Click delete again to confirm")


def _handle_level_up(pokemon_id: int, pokemon_name: str) -> None:
    """Handle pokemon level up."""
    try:
        api_client.level_up_pokemon(pokemon_id, 1)
        st.success(f"🎉 {pokemon_name} leveled up!")
        st.rerun()
    except Exception as e:
        st.error(f"Error leveling up pokemon: {str(e)}")


def show_create_pokemon_form() -> None:
    """Show form to create new pokemon."""
    st.subheader("➕ Create New Pokemon")

    with st.form("create_pokemon_form"):
        pokemon_data = _get_pokemon_form_inputs()
        attacks = _get_attacks_input()

        submitted = st.form_submit_button("Create Pokemon", type="primary")

        if submitted:
            _handle_create_pokemon_submission(pokemon_data, attacks)


def _get_pokemon_form_inputs() -> dict[str, Any]:
    """Get basic pokemon form inputs."""
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Name *", placeholder="Pikachu")
        type_primary = st.selectbox(
            "Primary Type *", FormValidators.get_pokemon_types()
        )
        nature = st.selectbox("Nature *", FormValidators.get_pokemon_natures())

    with col2:
        type_secondary = st.selectbox(
            "Secondary Type",
            ["None"] + FormValidators.get_pokemon_types(),
        )
        level = st.number_input("Level *", min_value=1, max_value=100, value=1)

    return {
        "name": name,
        "type_primary": type_primary,
        "type_secondary": type_secondary,
        "nature": nature,
        "level": level,
    }


def _get_attacks_input() -> list[str]:
    """Get attacks input from form."""
    st.subheader("Attacks (Optional)")
    col1, col2 = st.columns(2)

    with col1:
        attack1 = st.text_input("Attack 1", placeholder="Tackle")
        attack2 = st.text_input("Attack 2", placeholder="Growl")

    with col2:
        attack3 = st.text_input("Attack 3", placeholder="Thunder Shock")
        attack4 = st.text_input("Attack 4", placeholder="Quick Attack")

    return [attack1, attack2, attack3, attack4]


def _handle_create_pokemon_submission(
    pokemon_data: dict[str, Any], attacks: list[str]
) -> None:
    """Handle pokemon creation form submission."""
    if (
        not pokemon_data["name"]
        or not pokemon_data["type_primary"]
        or not pokemon_data["nature"]
    ):
        st.error("Please complete all required fields.")
        return

    try:
        filtered_attacks = [a.strip() for a in attacks if a.strip()]

        submission_data = {
            "name": pokemon_data["name"],
            "type_primary": pokemon_data["type_primary"],
            "type_secondary": pokemon_data["type_secondary"]
            if pokemon_data["type_secondary"] != "None"
            else None,
            "nature": pokemon_data["nature"],
            "level": pokemon_data["level"],
            "attacks": filtered_attacks,
        }

        with st.spinner("Creating pokemon..."):
            api_client.create_pokemon(submission_data)

        st.success(f"Pokemon '{pokemon_data['name']}' created successfully!")
        st.balloons()
        st.rerun()

    except Exception as e:
        st.error(f"Error creating pokemon: {str(e)}")


def show_edit_pokemon_form(pokemon: dict[str, Any]) -> None:
    """Show form to edit existing pokemon."""
    form_key = f"edit_pokemon_form_{pokemon['id']}"

    with st.form(form_key):
        st.subheader(f"Edit {pokemon['name']}")

        pokemon_data = _get_edit_form_inputs(pokemon)
        attacks = _get_edit_attacks_input(pokemon)

        col1, col2 = st.columns(2)

        with col1:
            submitted = st.form_submit_button("Update Pokemon", type="primary")

        with col2:
            cancelled = st.form_submit_button("Cancel")

        if cancelled:
            st.session_state[f"editing_pokemon_{pokemon['id']}"] = False
            st.rerun()

        if submitted:
            _handle_edit_pokemon_submission(pokemon["id"], pokemon_data, attacks)


def _get_edit_form_inputs(pokemon: dict[str, Any]) -> dict[str, Any]:
    """Get edit form inputs with current values."""
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Name", value=pokemon["name"])

        type_options = FormValidators.get_pokemon_types()
        primary_index = _get_option_index(
            type_options, pokemon.get("type_primary", "normal")
        )
        type_primary = st.selectbox("Primary Type", type_options, index=primary_index)

        nature_options = FormValidators.get_pokemon_natures()
        nature_index = _get_option_index(nature_options, pokemon.get("nature", "hardy"))
        nature = st.selectbox("Nature", nature_options, index=nature_index)

    with col2:
        secondary_options = ["None"] + FormValidators.get_pokemon_types()
        secondary_value = pokemon.get("type_secondary") or "None"
        secondary_index = _get_option_index(secondary_options, secondary_value)
        type_secondary = st.selectbox(
            "Secondary Type", secondary_options, index=secondary_index
        )

        level = st.number_input(
            "Level", min_value=1, max_value=100, value=pokemon.get("level", 1)
        )

    return {
        "name": name,
        "type_primary": type_primary,
        "type_secondary": type_secondary,
        "nature": nature,
        "level": level,
    }


def _get_option_index(options: list[str], value: str) -> int:
    """Get index of value in options list, return 0 if not found."""
    try:
        return options.index(value)
    except ValueError:
        return 0


def _get_edit_attacks_input(pokemon: dict[str, Any]) -> list[str]:
    """Get attacks input for edit form."""
    current_attacks = _parse_attacks(pokemon.get("attacks", []))

    # Ensure we have 4 attack slots
    while len(current_attacks) < 4:
        current_attacks.append("")

    st.subheader("Attacks")
    col1, col2 = st.columns(2)

    with col1:
        attack1 = st.text_input("Attack 1", value=current_attacks[0])
        attack2 = st.text_input("Attack 2", value=current_attacks[1])

    with col2:
        attack3 = st.text_input("Attack 3", value=current_attacks[2])
        attack4 = st.text_input("Attack 4", value=current_attacks[3])

    return [attack1, attack2, attack3, attack4]


def _handle_edit_pokemon_submission(
    pokemon_id: int, pokemon_data: dict[str, Any], attacks: list[str]
) -> None:
    """Handle pokemon edit form submission."""
    if (
        not pokemon_data["name"]
        or not pokemon_data["type_primary"]
        or not pokemon_data["nature"]
    ):
        st.error("Please complete all required fields.")
        return

    try:
        filtered_attacks = [a.strip() for a in attacks if a.strip()]

        submission_data = {
            "name": pokemon_data["name"],
            "type_primary": pokemon_data["type_primary"],
            "type_secondary": pokemon_data["type_secondary"]
            if pokemon_data["type_secondary"] != "None"
            else None,
            "nature": pokemon_data["nature"],
            "level": pokemon_data["level"],
            "attacks": filtered_attacks,
        }

        with st.spinner("Updating pokemon..."):
            api_client.update_pokemon(pokemon_id, submission_data)

        st.success("🎉 Pokemon updated successfully!")
        st.session_state[f"editing_pokemon_{pokemon_id}"] = False
        st.rerun()

    except Exception as e:
        st.error(f"Error updating pokemon: {str(e)}")


def show_learn_attack_form(pokemon: dict[str, Any]) -> None:
    """Show form to teach new attack to pokemon."""
    form_key = f"learn_attack_form_{pokemon['id']}"

    with st.form(form_key):
        st.subheader(f"Teach Attack to {pokemon['name']}")

        current_attacks = _parse_attacks(pokemon.get("attacks", []))
        new_attack, replace_attack = _get_learn_attack_inputs(current_attacks)

        col1, col2 = st.columns(2)

        with col1:
            submitted = st.form_submit_button("Learn Attack", type="primary")

        with col2:
            cancelled = st.form_submit_button("Cancel")

        if cancelled:
            st.session_state[f"learning_attack_{pokemon['id']}"] = False
            st.rerun()

        if submitted:
            _handle_learn_attack_submission(pokemon, new_attack, replace_attack)


def _get_learn_attack_inputs(current_attacks: list[str]) -> tuple[str, str | None]:
    """Get inputs for learning new attack."""
    new_attack = st.text_input(
        "New Attack *",
        placeholder="Enter attack name...",
        help="Name of the attack to learn",
    )

    replace_attack = None
    if len(current_attacks) >= 4:
        st.warning("Pokemon already knows 4 attacks. Select one to replace:")
        replace_option = st.selectbox(
            "Replace Attack:", current_attacks + ["None (don't learn)"]
        )

        if replace_option != "None (don't learn)":
            replace_attack = replace_option

    if current_attacks:
        st.write("**Current Attacks:**")
        for i, attack in enumerate(current_attacks, 1):
            st.write(f"  {i}. {attack}")

    return new_attack, replace_attack


def _handle_learn_attack_submission(
    pokemon: dict[str, Any], new_attack: str, replace_attack: str | None
) -> None:
    """Handle learn attack form submission."""
    if not new_attack.strip():
        st.error("Please enter an attack name.")
        return

    try:
        with st.spinner(f"Teaching {new_attack} to {pokemon['name']}..."):
            api_client.learn_attack(pokemon["id"], new_attack.strip(), replace_attack)

        st.success(f"🎉 {pokemon['name']} learned {new_attack}!")
        st.session_state[f"learning_attack_{pokemon['id']}"] = False
        st.rerun()

    except Exception as e:
        st.error(f"Error teaching attack: {str(e)}")


def show_pokemon_analytics() -> None:
    """Show pokemon analytics and insights."""
    st.subheader("📈 Pokemon Analytics")

    try:
        pokemon_list = api_client.get_pokemon(limit=1000)

        if not pokemon_list:
            st.info("No pokemon data available for analysis.")
            return

        _show_analytics_sections(pokemon_list)

    except Exception as e:
        st.error(f"Error loading analytics: {str(e)}")


def _show_analytics_sections(pokemon_list: list[dict[str, Any]]) -> None:
    """Show all analytics sections."""
    show_detailed_statistics(pokemon_list)

    st.subheader("🏷️ Type Distribution")
    show_type_distribution(pokemon_list)

    st.subheader("📊 Level Distribution")
    show_level_distribution(pokemon_list)

    st.subheader("🎭 Nature Distribution")
    show_nature_distribution(pokemon_list)

    st.subheader("⚔️ Attack Analysis")
    show_attack_analysis(pokemon_list)


def show_detailed_statistics(pokemon_list: list[dict[str, Any]]) -> None:
    """Show detailed pokemon statistics."""
    col1, col2, col3, col4 = st.columns(4)

    total_pokemon = len(pokemon_list)
    levels = [p.get("level", 1) for p in pokemon_list]

    with col1:
        st.metric("Total Pokemon", total_pokemon)

    with col2:
        avg_level = sum(levels) / len(levels) if levels else 0
        st.metric("Average Level", f"{avg_level:.1f}")

    with col3:
        max_level = max(levels) if levels else 0
        highest_pokemon = next(
            (p for p in pokemon_list if p.get("level") == max_level), None
        )
        st.metric(
            "Highest Level",
            f"{max_level}"
            + (f" ({highest_pokemon['name']})" if highest_pokemon else ""),
        )

    with col4:
        pokemon_with_attacks = sum(
            1
            for p in pokemon_list
            if p.get("attacks") and len(p.get("attacks", [])) > 0
        )
        st.metric("Pokemon with Attacks", pokemon_with_attacks)


def show_type_distribution(pokemon_list: list[dict[str, Any]]) -> None:
    """Show type distribution analysis."""
    type_counts: dict[str, int] = {}
    dual_types = 0

    for pokemon in pokemon_list:
        primary_type = pokemon.get("type_primary", "unknown")
        type_counts[primary_type] = type_counts.get(primary_type, 0) + 1

        secondary_type = pokemon.get("type_secondary")
        if secondary_type:
            type_counts[secondary_type] = type_counts.get(secondary_type, 0) + 1
            dual_types += 1

    if type_counts:
        sorted_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Most Common Types:**")
            for i, (type_name, count) in enumerate(sorted_types[:10], 1):
                st.write(f"{i}. **{type_name.title()}:** {count} pokemon")

        with col2:
            single_types = len(pokemon_list) - dual_types
            st.write("**Type Combinations:**")
            st.write(f"Single-type: {single_types}")
            st.write(f"Dual-type: {dual_types}")


def show_level_distribution(pokemon_list: list[dict[str, Any]]) -> None:
    """Show level distribution analysis."""
    levels = [p.get("level", 1) for p in pokemon_list]

    if levels:
        level_ranges = {
            "1-10": sum(1 for level in levels if 1 <= level <= 10),
            "11-25": sum(1 for level in levels if 11 <= level <= 25),
            "26-50": sum(1 for level in levels if 26 <= level <= 50),
            "51-75": sum(1 for level in levels if 51 <= level <= 75),
            "76-100": sum(1 for level in levels if 76 <= level <= 100),
        }

        cols = st.columns(5)
        for i, (range_name, count) in enumerate(level_ranges.items()):
            with cols[i]:
                st.metric(f"Level {range_name}", count)


def show_nature_distribution(pokemon_list: list[dict[str, Any]]) -> None:
    """Show nature distribution analysis."""
    nature_counts: dict[str, int] = {}

    for pokemon in pokemon_list:
        nature = pokemon.get("nature", "unknown")
        nature_counts[nature] = nature_counts.get(nature, 0) + 1

    if nature_counts:
        sorted_natures = sorted(nature_counts.items(), key=lambda x: x[1], reverse=True)

        st.write("**Most Common Natures:**")
        for i, (nature_name, count) in enumerate(sorted_natures[:10], 1):
            st.write(f"{i}. **{nature_name.title()}:** {count} pokemon")


def show_attack_analysis(pokemon_list: list[dict[str, Any]]) -> None:
    """Show attack analysis."""
    attack_counts: dict[str, int] = {}
    pokemon_attack_counts: dict[int, int] = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}

    for pokemon in pokemon_list:
        attacks = _parse_attacks(pokemon.get("attacks", []))
        attack_count = len(attacks) if attacks else 0
        pokemon_attack_counts[attack_count] = (
            pokemon_attack_counts.get(attack_count, 0) + 1
        )

        if attacks:
            for attack in attacks:
                attack_counts[attack] = attack_counts.get(attack, 0) + 1

    _display_attack_statistics(pokemon_attack_counts, attack_counts)


def _display_attack_statistics(
    pokemon_attack_counts: dict[int, int], attack_counts: dict[str, int]
) -> None:
    """Display attack statistics."""
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Pokemon by Attack Count:**")
        for count, num_pokemon in pokemon_attack_counts.items():
            if num_pokemon > 0:
                st.write(f"{count} attacks: {num_pokemon} pokemon")

    with col2:
        if attack_counts:
            st.write("**Most Popular Attacks:**")
            sorted_attacks = sorted(
                attack_counts.items(), key=lambda x: x[1], reverse=True
            )
            for i, (attack_name, count) in enumerate(sorted_attacks[:10], 1):
                st.write(f"{i}. **{attack_name}:** {count} pokemon")
        else:
            st.write("**Most Popular Attacks:**")
            st.write("No attacks recorded yet.")
