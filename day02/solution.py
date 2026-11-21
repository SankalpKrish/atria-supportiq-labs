class OrderNotFoundError(Exception):
    """Raised when a valid order id does not match any order."""


def lookup_order(orders, order_id):
    """Return the order with ``order_id`` or raise a typed error."""
    if not isinstance(order_id, str) or not order_id:
        raise ValueError("order_id must be a non-empty string")

    for order in orders:
        if order["order_id"] == order_id:
            return order

    raise OrderNotFoundError(order_id)


def describe_order(orders, order_id):
    """Describe a known order, or report that it is missing."""
    try:
        order = lookup_order(orders, order_id)
    except OrderNotFoundError:
        return f"Order {order_id} not found"

    return f"{order['status']} order {order_id} totaling {order['total']}"


def raises_not_found(orders, order_id):
    """Return True when the lookup raises OrderNotFoundError."""
    try:
        lookup_order(orders, order_id)
    except OrderNotFoundError:
        return True

    return False
