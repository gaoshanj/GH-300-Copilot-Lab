from dataclasses import dataclass


@dataclass(frozen=True)
class Order:
    order_id: str
    customer: str
    items: list[tuple[str, int, float]]


ORDERS = {
    "demo-100": Order(
        order_id="demo-100",
        customer="Ada",
        items=[("notebook", 2, 12.50), ("pen", 1, 3.00)],
    ),
    "demo-200": Order(
        order_id="demo-200",
        customer="Grace",
        items=[("keyboard", 1, 80.00)],
    ),
}


def calculate_checksum(text: str) -> int:
    """Return a stable checksum suitable for the teaching API."""
    return sum(text.encode("utf-8")) % 10_000


def find_order(order_id: str) -> Order | None:
    return ORDERS.get(order_id.strip().lower())


def summarize_order(order: Order) -> dict:
    # Intentional lab defect: the quantity is omitted from the total.
    total = sum(price for _, _, price in order.items)
    return {
        "order_id": order.order_id,
        "customer": order.customer,
        "item_count": sum(quantity for _, quantity, _ in order.items),
        "total": round(total, 2),
    }

