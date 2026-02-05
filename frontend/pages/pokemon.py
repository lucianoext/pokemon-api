import streamlit as st


def show_pokemon_page() -> None:
    st.subheader("⚡ Pokémon Management")

    tab1, tab2 = st.tabs(["View Pokémon", "Create Pokémon"])

    with tab1:
        st.info("View Pokémon functionality - Under construction")
        try:
            st.warning("Pokémon endpoint not available yet")

        except Exception as e:
            st.error(f"Error loading Pokémon: {str(e)}")

    with tab2:
        show_create_pokemon_form()


def show_create_pokemon_form() -> None:
    with st.form("create_pokemon_form"):
        name = st.text_input("Pokémon Name")
        type_primary = st.selectbox(
            "Primary Type",
            [
                "normal",
                "fire",
                "water",
                "electric",
                "grass",
                "ice",
                "fighting",
                "poison",
                "ground",
                "flying",
                "psychic",
                "bug",
                "rock",
                "ghost",
                "dragon",
                "dark",
                "steel",
                "fairy",
            ],
        )
        type_secondary = st.selectbox(
            "Secondary Type (optional)",
            [
                "None",
                "normal",
                "fire",
                "water",
                "electric",
                "grass",
                "ice",
                "fighting",
                "poison",
                "ground",
                "flying",
                "psychic",
                "bug",
                "rock",
                "ghost",
                "dragon",
                "dark",
                "steel",
                "fairy",
            ],
        )
        nature = st.selectbox(
            "Nature",
            [
                "hardy",
                "lonely",
                "brave",
                "adamant",
                "naughty",
                "bold",
                "docile",
                "relaxed",
                "impish",
                "lax",
                "timid",
                "hasty",
                "serious",
                "jolly",
                "naive",
                "modest",
                "mild",
                "quiet",
                "bashful",
                "rash",
                "calm",
                "gentle",
                "sassy",
                "careful",
                "quirky",
            ],
        )
        level = st.number_input("Level", min_value=1, max_value=100, value=1)
        attacks = st.text_area("Attacks (JSON)", placeholder='["tackle", "growl"]')

        if st.form_submit_button("Create Pokémon", type="primary"):
            if name and type_primary and nature:
                try:
                    pokemon_data = {
                        "name": name,
                        "type_primary": type_primary,
                        "type_secondary": type_secondary
                        if type_secondary != "None"
                        else None,
                        "nature": nature,
                        "level": level,
                        "attacks": attacks or "[]",
                    }

                    st.warning("Create Pokémon functionality - Under construction")
                    st.json(pokemon_data)

                except Exception as e:
                    st.error(f"Error creating Pokémon: {str(e)}")
            else:
                st.error("Please, complete all required fields.")
