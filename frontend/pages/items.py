"""Items management page for Pokemon API frontend."""

from typing import Any

import streamlit as st
from utils.api_client import api_client
from utils.validators import FormValidators


def show_items_page() -> None:
    """Show items management page."""
    st.subheader("🎒 Items Management")

    tab1, tab2 = st.tabs(["View Items", "Create Item"])

    with tab1:
        show_items_list()

    with tab2:
        show_create_item_form()


def show_items_list() -> None:
    """Show list of items with management options."""
    try:
        items_list = api_client.get_items()

        if items_list:
            # Search and filter options
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                search_term = st.text_input(
                    "🔍 Search Items", placeholder="Enter item name..."
                )

            with col2:
                type_filter = st.selectbox(
                    "Filter by Type", ["All"] + FormValidators.get_item_types()
                )

            with col3:
                sort_option = st.selectbox(
                    "Sort by", ["Name", "Price (Low-High)", "Price (High-Low)", "Type"]
                )

            # Filter and sort items
            filtered_items = filter_and_sort_items(
                items_list, search_term, type_filter, sort_option
            )

            if filtered_items:
                # Display statistics
                show_items_statistics(filtered_items)

                # Display items
                for item in filtered_items:
                    show_item_card(item)
            else:
                st.info("No items found matching your criteria.")
        else:
            st.info("No items registered yet.")

    except Exception as e:  # pylint: disable=broad-exception-caught
        st.error(f"Error loading items: {str(e)}")


def filter_and_sort_items(
    items_list: list[dict[str, Any]],
    search_term: str,
    type_filter: str,
    sort_option: str,
) -> list[dict[str, Any]]:
    """Filter and sort items list based on criteria."""
    filtered = items_list

    # Apply search filter
    if search_term:
        filtered = [
            item for item in filtered if search_term.lower() in item["name"].lower()
        ]

    # Apply type filter
    if type_filter != "All":
        filtered = [item for item in filtered if item["type"] == type_filter]

    # Apply sorting
    if sort_option == "Name":
        filtered.sort(key=lambda x: x["name"].lower())
    elif sort_option == "Price (Low-High)":
        filtered.sort(key=lambda x: x["price"])
    elif sort_option == "Price (High-Low)":
        filtered.sort(key=lambda x: x["price"], reverse=True)
    elif sort_option == "Type":
        filtered.sort(key=lambda x: x["type"])

    return filtered


def show_items_statistics(items_list: list[dict[str, Any]]) -> None:
    """Show statistics about the items."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Items", len(items_list))

    with col2:
        avg_price = (
            sum(item["price"] for item in items_list) / len(items_list)
            if items_list
            else 0
        )
        st.metric("Average Price", f"₽{avg_price:.0f}")

    with col3:
        max_price = max((item["price"] for item in items_list), default=0)
        st.metric("Most Expensive", f"₽{max_price}")

    with col4:
        unique_types = len({item["type"] for item in items_list})
        st.metric("Item Types", unique_types)


def show_item_card(item: dict[str, Any]) -> None:
    """Show individual item card with management options."""
    with st.expander(f"🎒 {item['name']} - ₽{item['price']}"):
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            st.write(f"**ID:** {item['id']}")
            st.write(f"**Type:** {item['type']}")
            st.write(f"**Price:** ₽{item['price']}")
            if item.get("description"):
                st.write(f"**Description:** {item['description']}")

        with col2:
            if st.button("✏️ Edit", key=f"edit_item_{item['id']}"):
                st.session_state[f"editing_item_{item['id']}"] = True
                st.rerun()

        with col3:
            if st.button("🗑️ Delete", key=f"delete_item_{item['id']}", type="secondary"):
                handle_item_deletion(item["id"])

        # Show edit form if editing
        if st.session_state.get(f"editing_item_{item['id']}", False):
            show_edit_item_form(item)


def handle_item_deletion(item_id: int) -> None:
    """Handle item deletion with confirmation."""
    confirm_key = f"confirm_delete_item_{item_id}"

    if st.session_state.get(confirm_key, False):
        try:
            api_client.delete_item(item_id)
            st.success("Item deleted successfully!")
            st.session_state[confirm_key] = False
            st.rerun()
        except Exception as e:  # pylint: disable=broad-exception-caught
            st.error(f"Error deleting item: {str(e)}")
    else:
        st.session_state[confirm_key] = True
        st.warning("Click delete again to confirm")


def show_create_item_form() -> None:
    """Show form to create new item."""
    with st.form("create_item_form"):
        st.subheader("Create New Item")

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Item Name*", placeholder="Enter item name")
            item_type = st.selectbox("Type*", FormValidators.get_item_types())

        with col2:
            price = st.number_input(
                "Price (₽)*", min_value=0, max_value=999999, value=0
            )

        description = st.text_area(
            "Description",
            placeholder="Enter item description (optional)",
            help="Optional description of the item's effects or uses",
        )

        submitted = st.form_submit_button("Create Item", type="primary")

        if submitted:
            handle_create_item_submission(name, item_type, price, description)


def handle_create_item_submission(
    name: str, item_type: str, price: int, description: str
) -> None:
    """Handle item creation form submission."""
    # Validate inputs
    name_valid, name_error = FormValidators.validate_item_name(name)
    price_valid, price_error = FormValidators.validate_price(price)

    if not all([name_valid, price_valid]):
        errors = [e for e in [name_error, price_error] if e]
        st.error(
            "Please fix the following errors:\n" + "\n".join(f"• {e}" for e in errors)
        )
        return

    try:
        item_data = {
            "name": name,
            "type": item_type,
            "price": price,
            "description": description.strip() if description.strip() else None,
        }

        with st.spinner("Creating item..."):
            response = api_client.create_item(item_data)

        st.success(f"Item '{name}' created successfully!")
        st.json(response)

    except Exception as e:  # pylint: disable=broad-exception-caught
        st.error(f"Error creating item: {str(e)}")


def show_edit_item_form(item: dict[str, Any]) -> None:
    """Show form to edit existing item."""
    form_key = f"edit_item_form_{item['id']}"

    with st.form(form_key):
        st.subheader(f"Edit {item['name']}")

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Item Name*", value=item["name"])
            item_type = st.selectbox(
                "Type*",
                FormValidators.get_item_types(),
                index=FormValidators.get_item_types().index(item["type"]),
            )

        with col2:
            price = st.number_input(
                "Price (₽)*", min_value=0, max_value=999999, value=item["price"]
            )

        description = st.text_area(
            "Description", value=item.get("description", "") or ""
        )

        # Buttons
        col1, col2 = st.columns(2)

        with col1:
            submitted = st.form_submit_button("Update Item", type="primary")

        with col2:
            cancelled = st.form_submit_button("Cancel")

        if cancelled:
            st.session_state[f"editing_item_{item['id']}"] = False
            st.rerun()

        if submitted:
            handle_edit_item_submission(item["id"], name, item_type, price, description)


def handle_edit_item_submission(
    item_id: int, name: str, item_type: str, price: int, description: str
) -> None:
    """Handle item edit form submission."""
    # Validate inputs
    name_valid, name_error = FormValidators.validate_item_name(name)
    price_valid, price_error = FormValidators.validate_price(price)

    if not all([name_valid, price_valid]):
        errors = [e for e in [name_error, price_error] if e]
        st.error(
            "Please fix the following errors:\n" + "\n".join(f"• {e}" for e in errors)
        )
        return

    try:
        item_data = {
            "name": name,
            "type": item_type,
            "price": price,
            "description": description.strip() if description.strip() else None,
        }

        with st.spinner("Updating item..."):
            api_client.update_item(item_id, item_data)

        st.success("Item updated successfully!")
        st.session_state[f"editing_item_{item_id}"] = False
        st.rerun()

    except Exception as e:  # pylint: disable=broad-exception-caught
        st.error(f"Error updating item: {str(e)}")
