import streamlit as st
from utils.api_client import api_client
from utils.session_state import login_user


def show_auth_page() -> None:
    st.title("🔐 Pokémon API - Authentication")

    st.markdown("""
    ### Welcome to the Pokemon Management System

    This application allows you to manage:
    - 👥 **Trainers** - Create and manage trainers
    - ⚡ **Pokémon** - Register and organize your collection
    - 🎯 **Teams** - Form battle teams
    - 🎒 **Items** - Manage objects and tools
    - 👜 **Backpacks** - Manage inventories
    """)

    st.divider()

    tab1, tab2 = st.tabs(["🔑 Sign In", "📝 Sign Up"])

    with tab1:
        show_login_form()

    with tab2:
        show_register_form()


def show_login_form() -> None:
    """Login form"""
    st.subheader("🔑 Sign In")

    with st.expander("ℹ️ Test Accounts"):
        st.write("""
        **Demo accounts:**
        - User: `demo_user` / Password: `demo123`
        - Admin: `admin` / Password: `admin123`
        """)

    with st.form("login_form"):
        username = st.text_input(
            "👤 Username",
            placeholder="Enter your username",
            help="Use your username or email",
        )
        password = st.text_input(
            "🔒 Password", type="password", placeholder="Enter your password"
        )

        col1, col2 = st.columns([2, 1])

        with col1:
            submitted = st.form_submit_button(
                "🚀 Sign In", type="primary", use_container_width=True
            )

        with col2:
            st.checkbox("Remember me")

        if submitted:
            if not username or not password:
                st.error("❌ Please, complete all fields.")
                return

            try:
                with st.spinner("🔄 Verifying credentials..."):
                    response = api_client.login(username, password)

                access_token = response["tokens"]["access_token"]
                user_info = response["user"]

                login_user(access_token, user_info)

                st.success(f"✅ Welcome, {user_info['username']}!")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.info(f"📧 Email: {user_info['email']}")
                with col2:
                    user_type = (
                        "👑 Administrator" if user_info["is_superuser"] else "👤 User"
                    )
                    st.info(f"Type: {user_type}")
                with col3:
                    status = "🟢 Active" if user_info["is_active"] else "🔴 Inactive"
                    st.info(f"Status: {status}")

                st.balloons()

                st.rerun()

            except Exception as e:
                error_msg = str(e)
                if "Invalid credentials" in error_msg:
                    st.error("❌ Invalid username or password.")
                elif "User account is inactive" in error_msg:
                    st.error(
                        "❌ Your account is deactivated. Contact the administrator."
                    )
                else:
                    st.error(f"❌ Login error: {error_msg}")


def show_register_form() -> None:
    st.subheader("📝 Create New Account")

    st.info("💡 Create your account to start managing your Pokémon world")

    with st.form("register_form"):
        st.markdown("#### 👤 User Information")
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

        st.divider()

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
                format_func=lambda x: {
                    "": "Select...",
                    "male": "🚹 Male",
                    "female": "🚺 Female",
                    "other": "⚧️ Other",
                }.get(x, x),
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
                format_func=lambda x: {
                    "": "Select...",
                    "kanto": "🏔️ Kanto",
                    "johto": "🌸 Johto",
                    "hoenn": "🌊 Hoenn",
                    "sinnoh": "❄️ Sinnoh",
                    "unova": "🏙️ Unova",
                    "kalos": "🗼 Kalos",
                    "alola": "🏝️ Alola",
                    "galar": "🏰 Galar",
                }.get(x, x),
            )

        st.divider()

        agree_terms = st.checkbox(
            "✅ I accept the terms and conditions of use",
            help="You must accept the terms to create an account",
        )

        submitted = st.form_submit_button(
            "🚀 Create My Account", type="primary", use_container_width=True
        )

        if submitted:
            errors = []

            if not username or not email or not password:
                errors.append("❌ Complete all required fields (marked with *)")

            if len(username) < 3:
                errors.append("❌ Username must have at least 3 characters")

            if len(password) < 6:
                errors.append("❌ Password must have at least 6 characters")

            if password != confirm_password:
                errors.append("❌ Passwords don't match")

            if "@" not in email or "." not in email:
                errors.append("❌ Enter a valid email")

            if not agree_terms:
                errors.append("❌ You must accept the terms and conditions")

            if errors:
                for error in errors:
                    st.error(error)
                return

            try:
                with st.spinner("🔄 Creating your account..."):
                    user_data = {
                        "username": username.strip(),
                        "email": email.strip().lower(),
                        "password": password,
                    }

                    if trainer_name:
                        user_data["trainer_name"] = trainer_name.strip()
                    if trainer_gender:
                        user_data["trainer_gender"] = trainer_gender
                    if trainer_region:
                        user_data["trainer_region"] = trainer_region

                    response = api_client.register(user_data)

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

            except Exception as e:
                error_msg = str(e)
                if "Username already exists" in error_msg:
                    st.error("❌ This username is already in use. Try another one.")
                elif "Email already exists" in error_msg:
                    st.error(
                        "❌ This email is already registered. Do you already have an account?"
                    )
                else:
                    st.error(f"❌ Account creation error: {error_msg}")
