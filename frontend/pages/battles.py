"""Battle management page for Pokemon API frontend."""

import random
from typing import Any

import streamlit as st
from utils.api_client import api_client
from utils.session_state import require_auth

TYPE_EFFECTIVENESS = {
    "normal": {"fighting": 2.0},
    "fire": {
        "water": 0.5,
        "grass": 2.0,
        "fire": 0.5,
        "ice": 2.0,
        "bug": 2.0,
        "steel": 2.0,
        "ground": 0.5,
        "rock": 0.5,
        "dragon": 0.5,
    },
    "water": {
        "fire": 2.0,
        "water": 0.5,
        "grass": 0.5,
        "ground": 2.0,
        "rock": 2.0,
        "dragon": 0.5,
    },
    "electric": {
        "water": 2.0,
        "electric": 0.5,
        "grass": 0.5,
        "ground": 0.0,
        "flying": 2.0,
        "dragon": 0.5,
    },
    "grass": {
        "water": 2.0,
        "fire": 0.5,
        "grass": 0.5,
        "poison": 0.5,
        "ground": 2.0,
        "rock": 2.0,
        "bug": 0.5,
        "dragon": 0.5,
        "steel": 0.5,
        "flying": 0.5,
    },
    "ice": {
        "fire": 0.5,
        "water": 0.5,
        "grass": 2.0,
        "ice": 0.5,
        "ground": 2.0,
        "flying": 2.0,
        "dragon": 2.0,
        "steel": 0.5,
    },
    "fighting": {
        "normal": 2.0,
        "ice": 2.0,
        "poison": 0.5,
        "flying": 0.5,
        "psychic": 0.5,
        "bug": 0.5,
        "rock": 2.0,
        "ghost": 0.0,
        "dark": 2.0,
        "steel": 2.0,
    },
    "poison": {
        "grass": 2.0,
        "poison": 0.5,
        "ground": 0.5,
        "rock": 0.5,
        "ghost": 0.5,
        "steel": 0.0,
    },
    "ground": {
        "fire": 2.0,
        "electric": 2.0,
        "grass": 0.5,
        "poison": 2.0,
        "flying": 0.0,
        "bug": 0.5,
        "rock": 2.0,
        "steel": 2.0,
    },
    "flying": {
        "electric": 0.5,
        "grass": 2.0,
        "ice": 0.5,
        "fighting": 2.0,
        "bug": 2.0,
        "rock": 0.5,
        "steel": 0.5,
    },
    "psychic": {
        "fighting": 2.0,
        "poison": 2.0,
        "psychic": 0.5,
        "dark": 0.0,
        "steel": 0.5,
    },
    "bug": {
        "fire": 0.5,
        "grass": 2.0,
        "fighting": 0.5,
        "poison": 0.5,
        "flying": 0.5,
        "psychic": 2.0,
        "ghost": 0.5,
        "dark": 2.0,
        "steel": 0.5,
    },
    "rock": {
        "fire": 2.0,
        "ice": 2.0,
        "fighting": 0.5,
        "ground": 0.5,
        "flying": 2.0,
        "bug": 2.0,
        "steel": 0.5,
    },
    "ghost": {"normal": 0.0, "psychic": 2.0, "ghost": 2.0, "dark": 0.5},
    "dragon": {"dragon": 2.0, "steel": 0.5},
    "dark": {"fighting": 0.5, "psychic": 2.0, "ghost": 2.0, "dark": 0.5},
    "steel": {
        "fire": 0.5,
        "water": 0.5,
        "electric": 0.5,
        "ice": 2.0,
        "rock": 2.0,
        "steel": 0.5,
    },
    "fairy": {
        "fire": 0.5,
        "fighting": 2.0,
        "poison": 0.5,
        "dragon": 2.0,
        "dark": 2.0,
        "steel": 0.5,
    },
}


def show_battles_page() -> None:
    """Show battles management page."""
    require_auth()

    st.title("⚔️ Pokemon Battles")

    tab1, tab2, tab3 = st.tabs(
        ["🥊 Battle Arena", "📊 Battle Results", "🏆 Leaderboard"]
    )

    with tab1:
        show_battle_arena()

    with tab2:
        show_battle_history()

    with tab3:
        show_battle_leaderboard()


def show_battle_arena() -> None:
    """Show battle arena interface."""
    st.subheader("🥊 Battle Arena")
    st.write("Select two teams to battle against each other!")

    try:
        teams = _get_available_teams()
        if len(teams) < 2:
            st.warning("You need at least 2 teams with Pokemon to battle!")
            return

        team1, team2 = _show_team_selection(teams)

        if team1 and team2 and team1["trainer_id"] != team2["trainer_id"]:
            _show_battle_preview(team1, team2)

            if st.button("🚀 Start Battle!", type="primary", use_container_width=True):
                _execute_battle(team1, team2)

    except Exception as e:
        st.error(f"Error loading battle arena: {str(e)}")


def _get_available_teams() -> list[dict[str, Any]]:
    """Get teams that have at least one Pokemon."""
    all_teams = api_client.get_all_teams()
    return [team for team in all_teams if team.get("team_size", 0) > 0]


def _show_team_selection(
    teams: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    """Show team selection interface."""
    col1, col2 = st.columns(2)

    with col1:
        st.write("### 🔴 Team 1")
        team1 = st.selectbox(
            "Select first team:",
            options=teams,
            format_func=lambda x: f"{x['trainer_name']}'s Team ({x['team_size']} Pokemon)",
            key="team1_select",
        )
        if team1:
            _show_team_preview(team1, "🔴")

    with col2:
        st.write("### 🔵 Team 2")
        available_teams = [
            t
            for t in teams
            if t["trainer_id"] != (team1["trainer_id"] if team1 else None)
        ]
        team2 = st.selectbox(
            "Select second team:",
            options=available_teams,
            format_func=lambda x: f"{x['trainer_name']}'s Team ({x['team_size']} Pokemon)",
            key="team2_select",
        )
        if team2:
            _show_team_preview(team2, "🔵")

    return team1, team2


def _show_team_preview(team: dict[str, Any], color_emoji: str) -> None:
    """Show a preview of the selected team."""
    members = team.get("members", [])
    total_strength = sum(member.get("pokemon_level", 1) for member in members)

    with st.container():
        st.write(f"**Trainer:** {team['trainer_name']}")
        st.write(f"**Team Size:** {len(members)} Pokemon")
        st.write(f"**Total Strength:** {total_strength}")

        if members:
            st.write("**Team Members:**")
            for member in sorted(members, key=lambda x: x.get("position", 1)):
                st.write(
                    f"{color_emoji} {member.get('pokemon_name')} (Lvl {member.get('pokemon_level')})"
                )


def _show_battle_preview(team1: dict[str, Any], team2: dict[str, Any]) -> None:
    """Show battle preview with calculations."""
    st.write("---")
    st.write("### ⚔️ Battle Preview")

    col1, col2, col3 = st.columns([2, 1, 2])

    team1_stats = _calculate_team_stats(team1)
    team2_stats = _calculate_team_stats(team2)

    with col1:
        st.write(f"**🔴 {team1['trainer_name']}'s Team**")
        st.write(f"Base Strength: {team1_stats['base_strength']}")
        st.write(f"Type Advantage: {team1_stats['type_advantage']:.2f}x")
        st.write(f"Final Strength: {team1_stats['final_strength']:.1f}")

    with col2:
        st.write("**VS**")
        if team1_stats["final_strength"] > team2_stats["final_strength"]:
            st.write("🔴 **Advantage**")
        elif team2_stats["final_strength"] > team1_stats["final_strength"]:
            st.write("🔵 **Advantage**")
        else:
            st.write("⚖️ **Even Match**")

    with col3:
        st.write(f"**🔵 {team2['trainer_name']}'s Team**")
        st.write(f"Base Strength: {team2_stats['base_strength']}")
        st.write(f"Type Advantage: {team2_stats['type_advantage']:.2f}x")
        st.write(f"Final Strength: {team2_stats['final_strength']:.1f}")


def _calculate_team_stats(team: dict[str, Any]) -> dict[str, Any]:
    """Calculate team statistics including type advantages."""
    members = team.get("members", [])
    base_strength = sum(member.get("pokemon_level", 1) for member in members)

    types = set()
    for member in members:
        pokemon_type = member.get("pokemon_type", "normal").lower()
        types.add(pokemon_type)

    diversity_bonus = 1.0 + (len(types) * 0.05)

    battle_factor = random.uniform(0.9, 1.1)  # nosec B311

    final_strength = base_strength * diversity_bonus * battle_factor

    return {
        "base_strength": base_strength,
        "type_advantage": diversity_bonus * battle_factor,
        "final_strength": final_strength,
        "types": list(types),
    }


def _execute_battle(team1: dict[str, Any], team2: dict[str, Any]) -> None:
    """Execute the battle and show results."""
    with st.spinner("⚔️ Battle in progress..."):
        import time

        time.sleep(2)

        team1_stats = _calculate_team_stats(team1)
        team2_stats = _calculate_team_stats(team2)

        if team1_stats["final_strength"] > team2_stats["final_strength"]:
            winner = team1
            winner_stats = team1_stats
            loser = team2
            loser_stats = team2_stats
        else:
            winner = team2
            winner_stats = team2_stats
            loser = team1
            loser_stats = team1_stats

        _show_battle_results(winner, winner_stats, loser, loser_stats)

        _save_battle_result(team1, team2, winner, team1_stats, team2_stats)


def _show_battle_results(
    winner: dict[str, Any],
    winner_stats: dict[str, Any],
    loser: dict[str, Any],
    loser_stats: dict[str, Any],
) -> None:
    """Show detailed battle results."""
    st.success("⚔️ Battle Complete!")

    st.balloons()
    st.write("## 🏆 Battle Results")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.write(f"### 🎉 {winner['trainer_name']} Wins!")
        st.write(f"**Winning Team Strength:** {winner_stats['final_strength']:.1f}")
        st.write(f"**Defeated Team Strength:** {loser_stats['final_strength']:.1f}")

        strength_diff = winner_stats["final_strength"] - loser_stats["final_strength"]
        st.write(f"**Victory Margin:** {strength_diff:.1f}")

    st.write("---")
    st.write("### 📊 Detailed Battle Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**🏆 {winner['trainer_name']}'s Team**")
        st.write(f"• Base Strength: {winner_stats['base_strength']}")
        st.write(f"• Battle Multiplier: {winner_stats['type_advantage']:.2f}x")
        st.write(f"• Final Strength: {winner_stats['final_strength']:.1f}")
        st.write(f"• Types: {', '.join(winner_stats['types'])}")

    with col2:
        st.write(f"**💀 {loser['trainer_name']}'s Team**")
        st.write(f"• Base Strength: {loser_stats['base_strength']}")
        st.write(f"• Battle Multiplier: {loser_stats['type_advantage']:.2f}x")
        st.write(f"• Final Strength: {loser_stats['final_strength']:.1f}")
        st.write(f"• Types: {', '.join(loser_stats['types'])}")


def _save_battle_result(
    team1: dict[str, Any],
    team2: dict[str, Any],
    winner: dict[str, Any],
    team1_stats: dict[str, Any],
    team2_stats: dict[str, Any],
) -> None:
    """Save battle result to session state (could be extended to save to database)."""
    if "battle_history" not in st.session_state:
        st.session_state.battle_history = []

    from datetime import datetime

    battle_record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "team1": {
            "trainer_name": team1["trainer_name"],
            "team_size": team1["team_size"],
            "final_strength": team1_stats["final_strength"],
        },
        "team2": {
            "trainer_name": team2["trainer_name"],
            "team_size": team2["team_size"],
            "final_strength": team2_stats["final_strength"],
        },
        "winner": winner["trainer_name"],
        "margin": abs(team1_stats["final_strength"] - team2_stats["final_strength"]),
    }

    st.session_state.battle_history.insert(0, battle_record)

    if len(st.session_state.battle_history) > 50:
        st.session_state.battle_history = st.session_state.battle_history[:50]


def show_battle_history() -> None:
    """Show battle history and results."""
    st.subheader("📊 Battle Results")

    if "battle_history" not in st.session_state or not st.session_state.battle_history:
        st.info(
            "No battles have been fought yet! Go to the Battle Arena to start fighting."
        )
        return

    st.write(f"**Total Battles:** {len(st.session_state.battle_history)}")

    st.write("### 🕒 Recent Battles")

    for i, battle in enumerate(st.session_state.battle_history[:10]):
        with st.expander(f"Battle #{i + 1} - {battle['timestamp']}", expanded=i == 0):
            col1, col2, col3 = st.columns([2, 1, 2])

            with col1:
                st.write(f"**{battle['team1']['trainer_name']}'s Team**")
                st.write(f"Team Size: {battle['team1']['team_size']}")
                st.write(f"Strength: {battle['team1']['final_strength']:.1f}")

            with col2:
                st.write("**VS**")
                if battle["winner"] == battle["team1"]["trainer_name"]:
                    st.write("🏆 ← **WINNER**")
                else:
                    st.write("**WINNER** → 🏆")

            with col3:
                st.write(f"**{battle['team2']['trainer_name']}'s Team**")
                st.write(f"Team Size: {battle['team2']['team_size']}")
                st.write(f"Strength: {battle['team2']['final_strength']:.1f}")

            st.write(f"**Victory Margin:** {battle['margin']:.1f}")

    st.write("---")
    if st.button("🗑️ Clear Battle History", type="secondary"):
        st.session_state.battle_history = []
        st.success("Battle history cleared!")
        st.rerun()


def show_battle_leaderboard() -> None:
    """Show battle leaderboard and statistics."""
    st.subheader("🏆 Battle Leaderboard")

    if "battle_history" not in st.session_state or not st.session_state.battle_history:
        st.info(
            "No battle data available yet! Fight some battles to see the leaderboard."
        )
        return

    trainer_stats = _calculate_trainer_battle_stats()

    if not trainer_stats:
        st.info("Not enough battle data to generate leaderboard.")
        return

    st.write("### 🥇 Top Trainers")

    sorted_trainers = sorted(
        trainer_stats.items(),
        key=lambda x: (x[1]["wins"], x[1]["win_rate"]),
        reverse=True,
    )

    for i, (trainer_name, stats) in enumerate(sorted_trainers[:10], 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."

        col1, col2, col3, col4, col5 = st.columns([1, 3, 1, 1, 2])

        with col1:
            st.write(medal)

        with col2:
            st.write(f"**{trainer_name}**")

        with col3:
            st.write(f"{stats['wins']}W")

        with col4:
            st.write(f"{stats['losses']}L")

        with col5:
            st.write(f"{stats['win_rate']:.1f}% ({stats['total_battles']} battles)")

    st.write("---")
    st.write("### 📈 Battle Statistics")

    col1, col2, col3, col4 = st.columns(4)

    total_battles = len(st.session_state.battle_history)
    total_trainers = len(trainer_stats)
    avg_battles_per_trainer = (
        total_battles / total_trainers if total_trainers > 0 else 0
    )

    with col1:
        st.metric("Total Battles", total_battles)

    with col2:
        st.metric("Active Trainers", total_trainers)

    with col3:
        st.metric("Avg Battles/Trainer", f"{avg_battles_per_trainer:.1f}")

    with col4:
        if st.session_state.battle_history:
            latest_battle = st.session_state.battle_history[0]
            st.metric("Latest Winner", latest_battle["winner"])


def _calculate_trainer_battle_stats() -> dict[str, dict[str, Any]]:
    """Calculate battle statistics for each trainer."""
    if "battle_history" not in st.session_state:
        return {}

    trainer_stats: dict[str, dict[str, Any]] = {}

    for battle in st.session_state.battle_history:
        for team_key in ["team1", "team2"]:
            trainer_name = battle[team_key]["trainer_name"]
            if trainer_name not in trainer_stats:
                trainer_stats[trainer_name] = {
                    "wins": 0,
                    "losses": 0,
                    "total_battles": 0,
                    "win_rate": 0.0,
                }

        winner = battle["winner"]
        team1_trainer = battle["team1"]["trainer_name"]
        team2_trainer = battle["team2"]["trainer_name"]

        if winner == team1_trainer:
            trainer_stats[team1_trainer]["wins"] += 1
            trainer_stats[team2_trainer]["losses"] += 1
        else:
            trainer_stats[team2_trainer]["wins"] += 1
            trainer_stats[team1_trainer]["losses"] += 1

        trainer_stats[team1_trainer]["total_battles"] += 1
        trainer_stats[team2_trainer]["total_battles"] += 1

    for trainer_name, stats in trainer_stats.items():
        if stats["total_battles"] > 0:
            stats["win_rate"] = (stats["wins"] / stats["total_battles"]) * 100

    return trainer_stats
