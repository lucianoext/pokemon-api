from typing import Any

import streamlit as st


def init_session_state() -> None:
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "access_token" not in st.session_state:
        st.session_state.access_token = None

    if "user_info" not in st.session_state:
        st.session_state.user_info = None

    if "current_page" not in st.session_state:
        st.session_state.current_page = "auth"


def login_user(token: str, user_info: dict[str, Any]) -> None:
    st.session_state.authenticated = True
    st.session_state.access_token = token
    st.session_state.user_info = user_info
    st.session_state.current_page = "dashboard"


def logout_user() -> None:
    st.session_state.authenticated = False
    st.session_state.access_token = None
    st.session_state.user_info = None
    st.session_state.current_page = "auth"


def is_authenticated() -> bool:
    return bool(st.session_state.get("authenticated", False))


def get_current_user() -> dict[str, Any] | None:
    user_info = st.session_state.get("user_info")
    return user_info if user_info is not None else None


def require_auth() -> None:
    if not is_authenticated():
        st.error("You must log in to access this page.")
        st.session_state.current_page = "auth"
        st.rerun()
