import os
import sys
import threading
import time
from datetime import datetime
from typing import Any

import streamlit as st

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pages.auth import show_auth_page
from pages.backpacks import show_backpacks_page
from pages.dashboard import show_dashboard
from pages.items import show_items_page
from pages.pokemon import show_pokemon_page
from pages.teams import show_teams_page
from pages.trainers import show_trainers_page
from utils.api_client import api_client
from utils.session_state import init_session_state, is_authenticated, logout_user


def main() -> None:
    """Main application entry point."""
    st.set_page_config(
        page_title="Pokémon Management System",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items={
            "Get Help": "https://github.com/lucianoext/pokemon-api",
            "Report a bug": "https://github.com/lucianoext/pokemon-api/issues",
            "About": """
            # Pokémon Management System
           Pokémon management site with JWT authentication.

            **Features:**
            - 🔐 Secure Authentication
            - 👥 Trainers management
            - ⚡ Pokémon register
            - 🎯 Team formation
            - 🎒 Inventory system

            Developed with FastAPI + Streamlit
            """,
        },
    )

    init_session_state()
    inject_custom_css()
    check_api_connectivity()

    if is_authenticated():
        show_authenticated_app()
    else:
        show_auth_page()


def inject_custom_css() -> None:
    """Inject custom CSS styles."""
    st.markdown(
        """
    <style>
        /* Hide Streamlit menu and footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Sidebar */
        .css-1d391kg {
            background: linear-gradient(180deg, #1f4e79 0%, #2e6da4 100%);
        }

        /* Custom buttons */
        .stButton > button {
            border-radius: 10px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }

        /* Metrics */
        .css-1xarl3l {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
        }

        /* Cards */
        .css-12w0qpk {
            border-radius: 10px;
            border: 1px solid #e1e5e9;
            padding: 1rem;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }

        .stTabs [data-baseweb="tab"] {
            height: 50px;
            padding-left: 20px;
            padding-right: 20px;
            border-radius: 10px 10px 0px 0px;
            background: #e03800;
        }

        .stTabs [aria-selected="true"] {
            background: #007bff;
            color: white;
        }

        /* Sidebar */
        .css-1lcbmhc {
            padding-top: 2rem;
        }

        /* Alerts */
        .stAlert {
            border-radius: 10px;
            border: none;
        }

        /* Forms */
        .stTextInput > div > div > input {
            border-radius: 8px;
        }

        .stSelectbox > div > div > select {
            border-radius: 8px;
        }

        /* Animations */
        .element-container {
            transition: all 0.3s ease;
        }

        /* Dataframes */
        .dataframe {
            border-radius: 10px;
            overflow: hidden;
        }

        /* Expanders */
        .streamlit-expanderHeader {
            border-radius: 8px;
            background: #f8f9fa;
        }

        /* Buttons Icons */
        .nav-button {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 12px 16px;
            margin: 4px 0;
            border-radius: 8px;
            border: none;
            background: transparent;
            width: 100%;
            text-align: left;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .nav-button:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateX(4px);
        }

        .nav-button.active {
            background: rgba(255, 255, 255, 0.2);
            font-weight: 600;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )


def check_api_connectivity() -> None:
    """Check API connectivity and show status."""
    if "api_status_checked" not in st.session_state:
        try:
            health_status = api_client.health_check()
            if health_status.get("status") == "healthy":
                st.session_state.api_status = "connected"
                st.session_state.api_message = "✅ Connected to the API"
            else:
                st.session_state.api_status = "error"
                st.session_state.api_message = "❌ API not available"
        except Exception as e:
            st.session_state.api_status = "error"
            st.session_state.api_message = f"❌ Error {str(e)}"

        st.session_state.api_status_checked = True

    if st.session_state.get("api_status") == "error":
        with st.sidebar:
            st.error(st.session_state.api_message)
            if st.button("🔄 Retry Connection"):
                del st.session_state.api_status_checked
                st.rerun()


def show_authenticated_app() -> None:
    """Show the main authenticated application."""
    show_sidebar_navigation()

    current_page = st.session_state.get("current_page", "dashboard")

    if current_page == "dashboard":
        show_dashboard()
    elif current_page == "trainers":
        show_trainers_page()
    elif current_page == "pokemon":
        show_pokemon_page()
    elif current_page == "teams":
        show_teams_page()
    elif current_page == "items":
        show_items_page()
    elif current_page == "backpacks":
        show_backpacks_page()
    else:
        show_dashboard()


def show_sidebar_navigation() -> None:
    """Show sidebar navigation and user information."""
    with st.sidebar:
        _show_user_info()
        st.markdown("---")
        _show_navigation_menu()
        st.markdown("---")
        _show_system_status()
        _show_quick_stats()
        st.markdown("---")
        _show_sidebar_actions()


def _show_user_info() -> None:
    """Show current user information in sidebar."""
    user_info = st.session_state.get("user_info", {})

    st.markdown("### 👤 Current User")

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**{user_info.get('username', 'User')}**")
        user_type = "👑 Admin" if user_info.get("is_superuser") else "👤 User"
        st.caption(user_type)

    with col2:
        if st.button("🚪", help="Log out", key="logout_btn"):
            logout_user()
            st.rerun()


def _show_navigation_menu() -> None:
    """Show navigation menu in sidebar."""
    st.markdown("### 🧭 Navigation")

    current_page = st.session_state.get("current_page", "dashboard")

    pages = {
        "dashboard": {
            "icon": "🏠",
            "title": "Dashboard",
            "desc": "General overview",
        },
        "trainers": {"icon": "👥", "title": "Trainers", "desc": "Manage trainers"},
        "pokemon": {"icon": "⚡", "title": "Pokémon", "desc": "Pokémon management"},
        "teams": {"icon": "🎯", "title": "Teams", "desc": "Form teams"},
        "items": {"icon": "🎒", "title": "Items", "desc": "Available objects"},
        "backpacks": {"icon": "👜", "title": "Backpacks", "desc": "Inventories"},
    }

    for page_key, page_info in pages.items():
        is_current = current_page == page_key

        if st.button(
            f"{page_info['icon']} {page_info['title']}",
            help=page_info["desc"],
            key=f"nav_{page_key}",
            use_container_width=True,
            type="primary" if is_current else "secondary",
        ):
            if not is_current:
                st.session_state.current_page = page_key
                st.rerun()


def _show_system_status() -> None:
    """Show system status in sidebar."""
    st.markdown("### ℹ️ System Status")

    api_status = st.session_state.get("api_status", "unknown")
    if api_status == "connected":
        st.success("API: Connected")
    else:
        st.error("API: Disconnected")


def _show_sidebar_actions() -> None:
    """Show action buttons in sidebar."""
    st.markdown("### ⚙️ Actions")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄", help="Refresh", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    with col2:
        if st.button("ℹ️", help="About", use_container_width=True):
            show_about_modal()

    if st.button("🔑 Change Password", use_container_width=True):
        show_change_password_modal()


def _show_quick_stats() -> None:
    """Show quick statistics in sidebar."""
    try:

        @st.cache_data(ttl=300)
        def get_cached_stats() -> dict[str, Any]:
            stats_data: dict[str, Any] = api_client.get_dashboard_stats()
            return stats_data

        stats = get_cached_stats()

        if not stats.get("error"):
            st.metric("👥 Trainers", stats.get("trainers_count", 0))
            st.metric("⚡ Pokémon", stats.get("pokemon_count", 0))
            st.metric("🎒 Items", stats.get("items_count", 0))

            if stats.get("average_level"):
                st.metric("📊 Average Level", f"{stats['average_level']:.1f}")

    except Exception as e:
        st.caption(f"Stats: Error ({str(e)[:20]}...)")


def show_about_modal() -> None:
    """Show about system modal."""
    with st.expander("ℹ️ About System", expanded=True):
        st.markdown("""
        ### 🌟 Pokémon Management System

        **Version:** 1.0.0
        **Developed with:**
        - 🚀 FastAPI (Backend)
        - 🎨 Streamlit (Frontend)
        - 🔐 JWT Authentication
        - 🗃️ SQLite/PostgreSQL

        **Main Features:**
        - ✅ JWT Authentication
        - ✅ CRUD for all entities
        - ✅ Dashboard with real-time stats
        - ✅ Responsive and intuitive interface
        - ✅ Pokemon management
        - ✅ Inventory system

        **Managed Entities:**
        - 👥 Trainers
        - ⚡ Pokémon
        - 🎯 Teams
        - 🎒 Items
        - 👜 Backpacks
        """)


def show_change_password_modal() -> None:
    """Show change password modal."""
    with st.expander("🔑 Change Password", expanded=True):
        with st.form("change_password_sidebar"):
            st.markdown("#### Update Password")

            current_password = st.text_input(
                "Current Password", type="password", placeholder="Current password"
            )

            new_password = st.text_input(
                "New Password", type="password", placeholder="Min 6 characters"
            )

            confirm_password = st.text_input(
                "Confirm New Password",
                type="password",
                placeholder="Repeat new password",
            )

            submitted = st.form_submit_button("🔒 Change Password", type="primary")

            if submitted:
                _handle_password_change(
                    current_password, new_password, confirm_password
                )


def _handle_password_change(
    current_password: str, new_password: str, confirm_password: str
) -> None:
    """Handle password change logic."""
    if not current_password or not new_password:
        st.error("Complete all fields")
        return

    if new_password != confirm_password:
        st.error("Passwords don't match")
        return

    if len(new_password) < 6:
        st.error("New password should have at least 6 characters")
        return

    try:
        with st.spinner("Changing password..."):
            api_client.change_password(current_password, new_password)
        st.success("✅ Password successfully updated")

    except Exception as e:
        error_msg = str(e)
        if "Current password is incorrect" in error_msg:
            st.error("❌ Current password is incorrect")
        else:
            st.error(f"❌ Error: {error_msg}")


def show_error_page(error_message: str) -> None:
    """Show error page with retry options."""
    st.error("🚨 Application Error")

    st.markdown(f"""
    ### Error Details:
    ```
    {error_message}
    ```
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔄 Retry"):
            st.rerun()

    with col2:
        if st.button("🏠 Home"):
            st.session_state.current_page = "dashboard"
            st.rerun()

    with col3:
        if st.button("🚪 Log Out"):
            logout_user()
            st.rerun()


def show_loading_spinner(message: str = "Loading...") -> Any:
    """Show loading spinner with custom message."""
    return st.spinner(f"🔄 {message}")


def show_success_message(message: str, duration: int = 3) -> None:
    """Show success message that auto-hides after duration."""
    success_placeholder = st.empty()
    success_placeholder.success(f"✅ {message}")

    def hide_message() -> None:
        time.sleep(duration)
        success_placeholder.empty()

    threading.Thread(target=hide_message, daemon=True).start()


def format_datetime(dt_string: str) -> str:
    """Format datetime string for display."""
    try:
        dt = datetime.fromisoformat(dt_string.replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y %H:%M")
    except (ValueError, TypeError, AttributeError):
        return dt_string


if __name__ == "__main__":
    main()
