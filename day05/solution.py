from collections.abc import Sized


def _has_value(value):
    """Treat null and empty values as missing, while allowing zero and False."""
    return value is not None and (not isinstance(value, Sized) or len(value) > 0)


def is_valid(ticket, contract):
    """Check the ticket ID, required fields, category, and priority."""
    return (
        _has_value(ticket.get("id"))
        and all(_has_value(ticket.get(field)) for field in contract["required"])
        and "category" in ticket
        and ticket["category"] in contract["category"]
        and "priority" in ticket
        and ticket["priority"] in contract["priority"]
    )


def validate_tickets(tickets, contract):
    """Return sorted lists of accepted and quarantined ticket IDs."""
    valid_ids = []
    quarantined_ids = []
    for ticket in tickets:
        ticket_id = ticket.get("id")
        if is_valid(ticket, contract):
            valid_ids.append(ticket_id)
        else:
            quarantined_ids.append(ticket_id if _has_value(ticket_id) else "<no-id>")

    return sorted(valid_ids), sorted(quarantined_ids)
