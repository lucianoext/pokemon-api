"""Authentication page for Pokemon API frontend."""

from typing import Any

import streamlit as st
from utils.api_client import api_client
from utils.session_state import login_user


def show_auth_page() -> None:
    """Show authentication page with login and register tabs."""
    st.title("🔐 Pokémon API - Authentication")

    st.markdown("""
    ### Welcome to the Pokemon Management System

    This application allows you to manage:
    - 👥 **Trainers** - Create and manage trainers
    - ⚡ **Pokémon** - Register and organize your collection
    - 🎯 **Teams** - Form battle teams
    - 🎒 **Items** - Manage objects and tools
    - 👜 **Backpacks** - Manage inventories
    - ⚔️ **Battles** - Simulate pokémon battles
    """)

    st.divider()

    tab1, tab2 = st.tabs(["🔑 Sign In", "📝 Sign Up"])

    with tab1:
        show_login_form()

    with tab2:
        show_register_form()


def show_login_form() -> None:
    """Show login form."""
    st.subheader("🔑 Sign In")

    with st.form("login_form"):
        username, password = _get_login_inputs()
        submitted = _get_login_submit_section()

        if submitted:
            _handle_login_submission(username, password)


def _get_login_inputs() -> tuple[str, str]:
    """Get login form inputs."""
    username = st.text_input(
        "👤 Username",
        placeholder="Enter your username",
        help="Use your username or email",
    )
    password = st.text_input(
        "🔒 Password", type="password", placeholder="Enter your password"
    )
    return username, password


def _get_login_submit_section() -> bool:
    """Get login submit section with buttons."""
    col1, col2 = st.columns([2, 1])

    with col1:
        submitted = st.form_submit_button(
            "🚀 Sign In", type="primary", use_container_width=True
        )

    with col2:
        st.checkbox("Remember me")

    return bool(submitted)


def _handle_login_submission(username: str, password: str) -> None:
    """Handle login form submission."""
    if not username or not password:
        st.error("❌ Please, complete all fields.")
        return

    try:
        with st.spinner("🔄 Verifying credentials..."):
            response = api_client.login(username, password)

        _process_successful_login(response)

    except Exception as e:
        _handle_login_error(e)


def _process_successful_login(response: dict[str, Any]) -> None:
    """Process successful login response."""
    access_token = response["tokens"]["access_token"]
    user_info = response["user"]

    login_user(access_token, user_info)
    st.success(f"✅ Welcome, {user_info['username']}!")

    _show_user_info_cards(user_info)
    st.balloons()
    st.rerun()


def _show_user_info_cards(user_info: dict[str, Any]) -> None:
    """Show user information cards after successful login."""
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(f"📧 Email: {user_info['email']}")

    with col2:
        user_type = "👑 Administrator" if user_info["is_superuser"] else "👤 User"
        st.info(f"Type: {user_type}")

    with col3:
        status = "🟢 Active" if user_info["is_active"] else "🔴 Inactive"
        st.info(f"Status: {status}")


def _handle_login_error(error: Exception) -> None:
    """Handle login errors with appropriate messages."""
    error_msg = str(error)

    if "Invalid credentials" in error_msg:
        st.error("❌ Invalid username or password.")
    elif "User account is inactive" in error_msg:
        st.error("❌ Your account is deactivated. Contact the administrator.")
    else:
        st.error(f"❌ Login error: {error_msg}")


def show_register_form() -> None:
    """Show registration form."""
    st.subheader("📝 Create New Account")
    st.info("💡 Create your account to start managing your Pokémon world")

    with st.form("register_form"):
        user_data = _get_registration_inputs()
        agree_terms = st.checkbox(
            "✅ I accept the terms and conditions of use",
            help="You must accept the terms to create an account",
        )

        submitted = st.form_submit_button(
            "🚀 Create My Account", type="primary", use_container_width=True
        )

        if submitted:
            _handle_registration_submission(user_data, agree_terms)


def _get_registration_inputs() -> dict[str, Any]:
    """Get all registration form inputs."""
    st.markdown("#### 👤 User Information")

    # User credentials
    user_data = _get_user_credentials()

    st.divider()

    # Trainer information
    trainer_data = _get_trainer_information()
    user_data.update(trainer_data)

    st.divider()

    return user_data


def _get_user_credentials() -> dict[str, str]:
    """Get user credentials input."""
    col1, col2 = st.columns(2)

    with col1:
        username = st.text_input(
            "👤 Username *",
            placeholder="Choose a unique username",
            help="Only letters, numbers and underscores. Minimum 3 characters.",
        )
        email = st.text_input(
            "📧 Email *",
            placeholder="your@email.com",
            help="We'll use this email for important notifications",
        )

    with col2:
        password = st.text_input(
            "🔒 Password *",
            type="password",
            placeholder="Minimum 6 characters",
            help="Use a secure password with letters, numbers and symbols",
        )
        confirm_password = st.text_input(
            "🔒 Confirm Password *",
            type="password",
            placeholder="Repeat your password",
        )

    return {
        "username": username,
        "email": email,
        "password": password,
        "confirm_password": confirm_password,
    }


def _get_trainer_information() -> dict[str, str]:
    """Get trainer information input."""
    st.markdown("#### ⚡ Trainer Information (Optional)")
    st.caption(
        "If you complete this information, your trainer profile will be automatically created"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        trainer_name = st.text_input(
            "🎯 Trainer Name",
            placeholder="Ash Ketchum",
            help="The name that will appear in your trainer profile",
        )

    with col2:
        trainer_gender = st.selectbox(
            "⚧️ Gender",
            ["", "male", "female", "other"],
            format_func=_format_gender_option,
        )

    with col3:
        trainer_region = st.selectbox(
            "🌍 Origin Region",
            [
                "",
                "kanto",
                "johto",
                "hoenn",
                "sinnoh",
                "unova",
                "kalos",
                "alola",
                "galar",
            ],
            format_func=_format_region_option,
        )

    return {
        "trainer_name": trainer_name,
        "trainer_gender": trainer_gender,
        "trainer_region": trainer_region,
    }


def _format_gender_option(option: str) -> str:
    """Format gender option for display."""
    gender_map = {
        "": "Select...",
        "male": "🚹 Male",
        "female": "🚺 Female",
        "other": "⚧️ Other",
    }
    return gender_map.get(option, option)


def _format_region_option(option: str) -> str:
    """Format region option for display."""
    region_map = {
        "": "Select...",
        "kanto": "🏔️ Kanto",
        "johto": "🌸 Johto",
        "hoenn": "🌊 Hoenn",
        "sinnoh": "❄️ Sinnoh",
        "unova": "🏙️ Unova",
        "kalos": "🗼 Kalos",
        "alola": "🏝️ Alola",
        "galar": "🏰 Galar",
    }
    return region_map.get(option, option)


def _handle_registration_submission(
    user_data: dict[str, Any], agree_terms: bool
) -> None:
    """Handle registration form submission."""
    validation_errors = _validate_registration_data(user_data, agree_terms)

    if validation_errors:
        for error in validation_errors:
            st.error(error)
        return

    try:
        _process_registration(user_data)
    except Exception as e:
        _handle_registration_error(e)


def _validate_registration_data(
    user_data: dict[str, Any], agree_terms: bool
) -> list[str]:
    """Validate registration data and return list of errors."""
    errors = []

    # Required field validation
    if not user_data["username"] or not user_data["email"] or not user_data["password"]:
        errors.append("❌ Complete all required fields (marked with *)")

    # Username validation
    if len(user_data["username"]) < 3:
        errors.append("❌ Username must have at least 3 characters")

    # Password validation
    if len(user_data["password"]) < 6:
        errors.append("❌ Password must have at least 6 characters")

    # Password confirmation
    if user_data["password"] != user_data["confirm_password"]:
        errors.append("❌ Passwords don't match")

    # Email validation
    if "@" not in user_data["email"] or "." not in user_data["email"]:
        errors.append("❌ Enter a valid email")

    # Terms acceptance
    if not agree_terms:
        errors.append("❌ You must accept the terms and conditions")

    return errors


def _process_registration(user_data: dict[str, Any]) -> None:
    """Process registration request."""
    with st.spinner("🔄 Creating your account..."):
        registration_data = _prepare_registration_data(user_data)
        response = api_client.register(registration_data)

    _show_registration_success(response)


def _prepare_registration_data(user_data: dict[str, Any]) -> dict[str, Any]:
    """Prepare registration data for API call."""
    registration_data = {
        "username": user_data["username"].strip(),
        "email": user_data["email"].strip().lower(),
        "password": user_data["password"],
    }

    # Add optional trainer information
    if user_data["trainer_name"]:
        registration_data["trainer_name"] = user_data["trainer_name"].strip()
    if user_data["trainer_gender"]:
        registration_data["trainer_gender"] = user_data["trainer_gender"]
    if user_data["trainer_region"]:
        registration_data["trainer_region"] = user_data["trainer_region"]

    return registration_data


def _show_registration_success(response: dict[str, Any]) -> None:
    """Show registration success message and user information."""
    st.success("🎉 Account created successfully!")

    with st.container():
        st.markdown("#### ✅ Your account has been created")
        col1, col2 = st.columns(2)

        with col1:
            st.info(f"👤 Username: {response['username']}")
            st.info(f"📧 Email: {response['email']}")

        with col2:
            st.info(f"🆔 ID: {response['id']}")
            created_date = response.get("created_at", "Now")
            st.info(f"📅 Created: {created_date}")

    st.markdown("---")
    st.success("🚀 Now you can sign in with your new account")
    st.info("💡 **Tip:** Switch to the '🔑 Sign In' tab to access")
    st.balloons()


def _handle_registration_error(error: Exception) -> None:
    """Handle registration errors with appropriate messages."""
    error_msg = str(error)

    if "Username already exists" in error_msg:
        st.error("❌ This username is already in use. Try another one.")
    elif "Email already exists" in error_msg:
        st.error("❌ This email is already registered. Do you already have an account?")
    else:
        st.error(f"❌ Account creation error: {error_msg}")
