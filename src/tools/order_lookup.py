import json
from pathlib import Path


ORDERS_FILE = Path("data/orders.json")


def load_orders() -> list[dict]:
    """Load the mock order dataset."""

    with ORDERS_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    return data["orders"]


def lookup_order(order_id: str) -> dict | None:
    """
    Look up an order and return only information
    that is safe for the assistant to expose.
    """

    order_id = order_id.strip().upper()

    orders = load_orders()

    order = next(
        (
            order
            for order in orders
            if order.get("order_id") == order_id
        ),
        None,
    )

    if order is None:
        return None

    status = order.get("status")

    result = {
        "order_id": order.get("order_id"),
        "membership_tier": order.get("membership_tier"),
        "status": status,
        "placed_at": order.get("placed_at"),
        "status_updated_at": order.get("status_updated_at"),
        "shipped_at": order.get("shipped_at"),
        "delivered_at": order.get("delivered_at"),
        "items": [
            {
                "sku": item.get("sku"),
                "name": item.get("name"),
                "quantity": item.get("quantity"),
                "final_sale": item.get("final_sale"),
            }
            for item in order.get("items", [])
        ],
    }

    # Carrier and ETA are only meaningful for orders
    # that are currently in the shipping process.
    if status in {"shipped", "out_for_delivery"}:
        result["carrier"] = order.get("carrier")

        # Different datasets sometimes use different names
        # for estimated delivery.
        result["estimated_delivery"] = (
            order.get("estimated_delivery")
            or order.get("eta")
            or order.get("estimated_delivery_date")
        )

    return result