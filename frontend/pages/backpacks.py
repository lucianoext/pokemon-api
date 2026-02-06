"""Backpacks management page for Pokemon API frontend."""

from typing import Any

import pandas as pd
import streamlit as st
from utils.api_client import api_client
from utils.session_state import require_auth


def show_backpacks_page() -> None:
    """Show backpacks management page."""
    require_auth()

    st.title("🎒 Backpacks Management")

    tab1, tab2, tab3 = st.tabs(["📋 List", "➕ Manage", "📊 Analytics"])

    with tab1:
        show_backpacks_list()

    with tab2:
        show_backpack_management()

    with tab3:
        show_backpack_analytics()


def show_backpacks_list() -> None:
    """Show list of backpacks with management options."""
    st.subheader("📋 Backpacks List")

    search_term, item_filter = _get_backpack_filters()

    try:
        backpacks = _fetch_and_prepare_backpack_data()
        if not backpacks:
            st.info("No backpacks found.")
            return

        filtered_backpacks = _apply_backpack_filters(
            backpacks, search_term, item_filter
        )

        if filtered_backpacks:
            show_backpacks_statistics(filtered_backpacks)
            _display_backpack_cards(filtered_backpacks)
        else:
            st.warning("No backpacks found with the applied filters.")

    except Exception as e:
        st.error(f"Error loading backpacks: {str(e)}")


def _get_backpack_filters() -> tuple[str, str]:
    """Get filter inputs for backpack list."""
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        search_term = st.text_input(
            "🔍 Search trainer", placeholder="Search by trainer name..."
        )

    with col2:
        item_filter = st.selectbox(
            "🎯 Filter by items count",
            ["All", "Empty", "1-10", "11-50", "51-100", "100+"],
        )

    with col3:
        if st.button("🔄 Refresh List"):
            st.rerun()

    return search_term, item_filter


def _fetch_and_prepare_backpack_data() -> list[dict[str, Any]]:
    """Fetch and prepare backpack data including empty backpacks."""
    backpacks_response = api_client.get_all_backpacks()
    backpacks: list[dict[str, Any]] = (
        backpacks_response if isinstance(backpacks_response, list) else []
    )

    # Add empty backpacks for trainers without items
    all_trainers = api_client.get_trainers(limit=1000)
    trainer_ids_with_backpacks = {bp.get("trainer_id") for bp in backpacks}

    for trainer in all_trainers:
        if trainer["id"] not in trainer_ids_with_backpacks:
            empty_backpack = {
                "trainer_id": trainer["id"],
                "trainer_name": trainer["name"],
                "total_items": 0,
                "items": [],
            }
            backpacks.append(empty_backpack)

    return backpacks


def _apply_backpack_filters(
    backpacks: list[dict[str, Any]], search_term: str, item_filter: str
) -> list[dict[str, Any]]:
    """Apply search and item count filters to backpacks."""
    filtered = backpacks

    # Apply search filter
    if search_term:
        filtered = [
            b
            for b in filtered
            if search_term.lower() in b.get("trainer_name", "").lower()
        ]

    # Apply item count filter
    filtered = _apply_item_count_filter(filtered, item_filter)

    return filtered


def _apply_item_count_filter(
    backpacks: list[dict[str, Any]], item_filter: str
) -> list[dict[str, Any]]:
    """Apply item count filter to backpacks."""
    if item_filter == "All":
        return backpacks

    filter_functions = {
        "Empty": lambda b: b.get("total_items", 0) == 0,
        "1-10": lambda b: 1 <= b.get("total_items", 0) <= 10,
        "11-50": lambda b: 11 <= b.get("total_items", 0) <= 50,
        "51-100": lambda b: 51 <= b.get("total_items", 0) <= 100,
        "100+": lambda b: b.get("total_items", 0) > 100,
    }

    filter_func = filter_functions.get(item_filter)
    if filter_func:
        return [b for b in backpacks if filter_func(b)]

    return backpacks


def _display_backpack_cards(backpacks: list[dict[str, Any]]) -> None:
    """Display backpack cards."""
    for backpack in backpacks:
        show_backpack_card(backpack)


def show_backpacks_statistics(backpacks: list[dict[str, Any]]) -> None:
    """Show statistics about backpacks."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Backpacks", len(backpacks))

    with col2:
        total_items = sum(bp.get("total_items", 0) for bp in backpacks)
        st.metric("Total Items", total_items)

    with col3:
        avg_items = total_items / len(backpacks) if backpacks else 0
        st.metric("Avg Items/Backpack", f"{avg_items:.1f}")

    with col4:
        non_empty_backpacks = sum(1 for bp in backpacks if bp.get("total_items", 0) > 0)
        st.metric("Non-Empty Backpacks", non_empty_backpacks)


def show_backpack_card(backpack: dict[str, Any]) -> None:
    """Show individual backpack card with management options."""
    trainer_name = backpack.get("trainer_name", "Unknown")
    total_items = backpack.get("total_items", 0)
    items = backpack.get("items", [])
    trainer_id = backpack.get("trainer_id")

    # Calculate total value
    total_value = sum(
        item.get("item_price", 0) * item.get("quantity", 0) for item in items
    )

    with st.expander(
        f"🎒 {trainer_name}'s Backpack ({total_items} items)", expanded=False
    ):
        if not items:
            st.info("This backpack is empty.")
            col1, _ = st.columns(2)
            with col1:
                if trainer_id and st.button(
                    "➕ Add Items",
                    key=f"manage_empty_{trainer_id}",
                    use_container_width=True,
                ):
                    st.session_state["selected_trainer_for_backpack"] = trainer_id
                    st.session_state["selected_trainer_name"] = trainer_name
                    st.rerun()
            return

        col1, col2 = st.columns([3, 1])

        with col1:
            _show_backpack_contents(items)

        with col2:
            _show_backpack_actions(
                trainer_id, trainer_name, total_items, total_value, items
            )


def _show_backpack_contents(items: list[dict[str, Any]]) -> None:
    """Show backpack contents in a table."""
    st.write("**Backpack Contents:**")

    # Create a nice table display
    backpack_data = []
    for item in sorted(items, key=lambda x: x.get("item_name", "")):
        description = item.get("item_description", "")
        truncated_description = (
            description[:50] + "..." if len(description) > 50 else description
        )
        backpack_data.append(
            {
                "Item": item.get("item_name", "Unknown"),
                "Type": item.get("item_type", "unknown"),
                "Quantity": item.get("quantity", 0),
                "Unit Price": f"${item.get('item_price', 0):,}",
                "Total Value": f"${item.get('item_price', 0) * item.get('quantity', 0):,}",
                "Description": truncated_description,
            }
        )

    if backpack_data:
        df = pd.DataFrame(backpack_data)
        st.dataframe(
            df,
            use_container_width=True,
            column_config={
                "Item": "Name",
                "Type": "Type",
                "Quantity": st.column_config.NumberColumn("Qty", format="%d"),
                "Unit Price": "Price",
                "Total Value": "Value",
                "Description": "Description",
            },
            hide_index=True,
        )


def _show_backpack_actions(
    trainer_id: int | None,
    trainer_name: str,
    total_items: int,
    total_value: float,
    items: list[dict[str, Any]],
) -> None:
    """Show backpack action buttons and metrics."""
    st.write("**Actions:**")

    if trainer_id:
        if st.button(
            "✏️ Manage Items",
            key=f"manage_backpack_{trainer_id}",
            use_container_width=True,
        ):
            st.session_state["selected_trainer_for_backpack"] = trainer_id
            st.session_state["selected_trainer_name"] = trainer_name
            st.rerun()

        if st.button(
            "🗑️ Clear All",
            key=f"clear_backpack_{trainer_id}",
            use_container_width=True,
            type="secondary",
        ):
            if st.session_state.get(f"confirm_clear_{trainer_id}", False):
                try:
                    with st.spinner("Clearing backpack..."):
                        api_client.clear_trainer_backpack(trainer_id)
                    st.success("Backpack cleared!")
                    st.session_state[f"confirm_clear_{trainer_id}"] = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Error clearing backpack: {str(e)}")
            else:
                st.session_state[f"confirm_clear_{trainer_id}"] = True
                st.warning("Click again to confirm")

    # Backpack metrics
    st.metric("Items Count", total_items)
    st.metric("Total Value", f"${total_value:,}")

    # Most valuable item
    if items:
        most_valuable = max(
            items, key=lambda x: x.get("item_price", 0) * x.get("quantity", 0)
        )
        st.write("**Most Valuable:**")
        st.write(f"💎 {most_valuable.get('item_name', 'Unknown')}")


def show_backpack_management() -> None:
    """Show backpack management interface."""
    st.subheader("➕ Backpack Management")

    # Trainer selection
    try:
        trainers = api_client.get_trainers(limit=1000)

        if not trainers:
            st.info("No trainers available.")
            return

        # Check if we have a pre-selected trainer
        selected_trainer_id = st.session_state.get("selected_trainer_for_backpack")
        selected_trainer_name = st.session_state.get("selected_trainer_name")

        if selected_trainer_id and selected_trainer_name:
            st.info(f"Managing backpack for: **{selected_trainer_name}**")

            if st.button("🔙 Back to Trainer Selection"):
                st.session_state.pop("selected_trainer_for_backpack", None)
                st.session_state.pop("selected_trainer_name", None)
                st.rerun()

            show_trainer_backpack_management(selected_trainer_id)
        else:
            trainer = st.selectbox(
                "Select trainer to manage:",
                options=trainers,
                format_func=lambda x: f"{x['name']} (ID: {x['id']}) - {x['region']}",
            )

            if trainer and st.button("Manage This Trainer's Backpack", type="primary"):
                st.session_state["selected_trainer_for_backpack"] = trainer["id"]
                st.session_state["selected_trainer_name"] = trainer["name"]
                st.rerun()

    except Exception as e:
        st.error(f"Error loading trainers: {str(e)}")


def show_trainer_backpack_management(trainer_id: int) -> None:
    """Show management interface for a specific trainer's backpack."""
    try:
        # Get current backpack
        backpack = api_client.get_trainer_backpack(trainer_id)
        current_items = backpack.get("items", [])

        col1, col2 = st.columns(2)

        with col1:
            _show_add_items_form(trainer_id)

        with col2:
            _show_current_backpack_management(trainer_id, current_items)

    except Exception as e:
        st.error(f"Error loading backpack: {str(e)}")


def _show_add_items_form(trainer_id: int) -> None:
    """Show form to add items to backpack."""
    st.write("### Add Items to Backpack")

    # Get available items
    all_items = api_client.get_items(limit=1000)

    if all_items:
        with st.form(f"add_item_form_{trainer_id}"):
            selected_item = st.selectbox(
                "Select Item:",
                options=all_items,
                format_func=lambda x: f"{x['name']} - ${x.get('price', 0):,} ({x.get('type', 'unknown')})",
            )

            quantity = st.number_input("Quantity:", min_value=1, max_value=999, value=1)

            # Show item details
            if selected_item:
                st.write("**Item Details:**")
                st.write(f"**Name:** {selected_item['name']}")
                st.write(f"**Type:** {selected_item.get('type', 'unknown')}")
                st.write(f"**Price:** ${selected_item.get('price', 0):,}")
                if selected_item.get("description"):
                    st.write(f"**Description:** {selected_item['description']}")

                total_cost = selected_item.get("price", 0) * quantity
                st.write(f"**Total Cost:** ${total_cost:,}")

            if st.form_submit_button("Add to Backpack", type="primary"):
                try:
                    backpack_data = {
                        "trainer_id": trainer_id,
                        "item_id": selected_item["id"],
                        "quantity": quantity,
                    }

                    with st.spinner("Adding item to backpack..."):
                        api_client.add_item_to_backpack(backpack_data)

                    st.success(
                        f"Added {quantity} {selected_item['name']}(s) to backpack!"
                    )
                    st.rerun()

                except Exception as e:
                    st.error(f"Error adding item: {str(e)}")
    else:
        st.info("No items available to add to backpack.")


def _show_current_backpack_management(
    trainer_id: int, current_items: list[dict[str, Any]]
) -> None:
    """Show current backpack items with management options."""
    st.write("### Current Backpack")

    if current_items:
        total_value = 0

        for item in sorted(current_items, key=lambda x: x.get("item_name", "")):
            item_value = item.get("item_price", 0) * item.get("quantity", 0)
            total_value += item_value

            st.write(
                f"**{item.get('item_name')}** "
                f"(x{item.get('quantity')}) - "
                f"${item.get('item_price', 0):,} each = "
                f"${item_value:,}"
            )

            _show_item_management_controls(trainer_id, item)
            st.divider()

        # Show total
        st.write(f"**Total Backpack Value:** ${total_value:,}")
        st.write(
            f"**Total Items:** {sum(item.get('quantity', 0) for item in current_items)}"
        )
    else:
        st.info("Backpack is empty.")


def _show_item_management_controls(trainer_id: int, item: dict[str, Any]) -> None:
    """Show controls for managing individual items."""
    col_qty, col_remove = st.columns(2)

    with col_qty:
        # Quick quantity update
        new_qty = st.number_input(
            "New Qty:",
            min_value=0,
            max_value=999,
            value=item.get("quantity", 1),
            key=f"qty_{trainer_id}_{item.get('item_id')}",
        )

        if new_qty != item.get("quantity") and st.button(
            "Update",
            key=f"update_qty_{trainer_id}_{item.get('item_id')}",
        ):
            try:
                if new_qty == 0:
                    # Remove item completely
                    with st.spinner("Removing item..."):
                        api_client.remove_item_from_backpack(
                            trainer_id,
                            item.get("item_id"),
                            item.get("quantity"),
                        )
                else:
                    # Update quantity
                    with st.spinner("Updating quantity..."):
                        api_client.update_item_quantity(
                            trainer_id, item.get("item_id"), new_qty
                        )

                st.success("Updated successfully!")
                st.rerun()

            except Exception as e:
                st.error(f"Error updating item: {str(e)}")

    with col_remove:
        # Quick remove buttons
        remove_qty = min(10, item.get("quantity", 1))
        if st.button(
            f"Remove {remove_qty}",
            key=f"remove_{trainer_id}_{item.get('item_id')}",
            use_container_width=True,
        ):
            try:
                with st.spinner("Removing items..."):
                    api_client.remove_item_from_backpack(
                        trainer_id, item.get("item_id"), remove_qty
                    )

                st.success(f"Removed {remove_qty} {item.get('item_name')}(s)!")
                st.rerun()

            except Exception as e:
                st.error(f"Error removing items: {str(e)}")


def show_backpack_analytics() -> None:
    """Show backpack analytics and insights."""
    st.subheader("📊 Backpack Analytics")

    try:
        # Get all backpacks and items for analysis
        backpacks = api_client.get_all_backpacks()

        if not backpacks:
            st.info("No backpack data available for analysis.")
            return

        _show_overall_statistics(backpacks)
        _show_popular_items_analysis(backpacks)
        _show_wealthiest_trainers(backpacks)
        _show_item_type_distribution(backpacks)
        _show_backpack_status_distribution(backpacks)

    except Exception as e:
        st.error(f"Error loading analytics: {str(e)}")


def _show_overall_statistics(backpacks: list[dict[str, Any]]) -> None:
    """Show overall backpack statistics."""
    col1, col2, col3, col4 = st.columns(4)

    total_backpacks = len(backpacks)
    total_items_count = sum(bp.get("total_items", 0) for bp in backpacks)

    with col1:
        st.metric("Total Backpacks", total_backpacks)

    with col2:
        st.metric("Total Items", total_items_count)

    with col3:
        total_value = 0
        for backpack in backpacks:
            for item in backpack.get("items", []):
                total_value += item.get("item_price", 0) * item.get("quantity", 0)
        st.metric("Total Value", f"${total_value:,}")

    with col4:
        avg_value = total_value / total_backpacks if total_backpacks > 0 else 0
        st.metric("Avg Backpack Value", f"${avg_value:,.0f}")


def _show_popular_items_analysis(backpacks: list[dict[str, Any]]) -> None:
    """Show most popular items analysis."""
    st.write("### 📈 Most Popular Items")
    item_popularity: dict[str, int] = {}
    item_quantities: dict[str, int] = {}

    for backpack in backpacks:
        for item in backpack.get("items", []):
            item_name = item.get("item_name", "Unknown")
            item_popularity[item_name] = item_popularity.get(item_name, 0) + 1
            item_quantities[item_name] = item_quantities.get(item_name, 0) + item.get(
                "quantity", 0
            )

    if item_popularity:
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Most Owned Items (by trainers):**")
            popular_items = sorted(
                item_popularity.items(), key=lambda x: x[1], reverse=True
            )[:10]
            for i, (item_name, count) in enumerate(popular_items, 1):
                st.write(f"{i}. **{item_name}** - {count} trainers")

        with col2:
            st.write("**Highest Total Quantities:**")
            quantity_items = sorted(
                item_quantities.items(), key=lambda x: x[1], reverse=True
            )[:10]
            for i, (item_name, total_qty) in enumerate(quantity_items, 1):
                st.write(f"{i}. **{item_name}** - {total_qty} total")


def _show_wealthiest_trainers(backpacks: list[dict[str, Any]]) -> None:
    """Show wealthiest trainers analysis."""
    st.write("### 💰 Wealthiest Trainers")

    trainer_values = _calculate_trainer_values(backpacks)
    _display_wealth_rankings(trainer_values)


def _calculate_trainer_values(backpacks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Calculate trainer wealth values."""
    trainer_values = []

    for backpack in backpacks:
        backpack_value = 0
        for item in backpack.get("items", []):
            backpack_value += item.get("item_price", 0) * item.get("quantity", 0)

        trainer_values.append(
            {
                "trainer": backpack.get("trainer_name", "Unknown"),
                "value": backpack_value,
                "items": backpack.get("total_items", 0),
            }
        )

    return trainer_values


def _display_wealth_rankings(trainer_values: list[dict[str, Any]]) -> None:
    """Display wealth rankings table."""
    if not trainer_values:
        return

    richest_trainers = sorted(trainer_values, key=lambda x: x["value"], reverse=True)[
        :10
    ]

    wealth_data = []
    for i, trainer_data in enumerate(richest_trainers, 1):
        wealth_data.append(
            {
                "Rank": i,
                "Trainer": trainer_data["trainer"],
                "Total Value": f"${trainer_data['value']:,}",
                "Items Count": trainer_data["items"],
            }
        )

    df = pd.DataFrame(wealth_data)
    st.dataframe(
        df,
        use_container_width=True,
        column_config={
            "Rank": st.column_config.NumberColumn("#", format="%d"),
            "Trainer": "Trainer Name",
            "Total Value": "Backpack Value",
            "Items Count": st.column_config.NumberColumn("Items", format="%d"),
        },
        hide_index=True,
    )


def _show_item_type_distribution(backpacks: list[dict[str, Any]]) -> None:
    """Show item type distribution analysis."""
    st.write("### 🏷️ Item Type Distribution")
    type_counts: dict[str, int] = {}
    type_values: dict[str, int] = {}

    for backpack in backpacks:
        for item in backpack.get("items", []):
            item_type = item.get("item_type", "unknown")
            quantity = item.get("quantity", 0)
            price = item.get("item_price", 0)

            type_counts[item_type] = type_counts.get(item_type, 0) + quantity
            type_values[item_type] = type_values.get(item_type, 0) + (quantity * price)

    if type_counts:
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Most Common Types (by quantity):**")
            common_types = sorted(
                type_counts.items(), key=lambda x: x[1], reverse=True
            )[:10]
            for i, (type_name, count) in enumerate(common_types, 1):
                st.write(f"{i}. **{type_name.title()}** - {count} items")

        with col2:
            st.write("**Most Valuable Types:**")
            valuable_types = sorted(
                type_values.items(), key=lambda x: x[1], reverse=True
            )[:10]
            for i, (type_name, value) in enumerate(valuable_types, 1):
                st.write(f"{i}. **{type_name.title()}** - ${value:,}")


def _show_backpack_status_distribution(backpacks: list[dict[str, Any]]) -> None:
    """Show backpack status distribution."""
    st.write("### 📦 Backpack Status Distribution")
    empty_count = sum(1 for bp in backpacks if bp.get("total_items", 0) == 0)
    light_count = sum(1 for bp in backpacks if 1 <= bp.get("total_items", 0) <= 10)
    medium_count = sum(1 for bp in backpacks if 11 <= bp.get("total_items", 0) <= 50)
    heavy_count = sum(1 for bp in backpacks if bp.get("total_items", 0) > 50)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Empty", empty_count)
    with col2:
        st.metric("Light (1-10)", light_count)
    with col3:
        st.metric("Medium (11-50)", medium_count)
    with col4:
        st.metric("Heavy (50+)", heavy_count)
