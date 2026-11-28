import sqlite3
from contextlib import closing

import pandas as pd

tickets = [
    {
        "id": "T1",
        "text": "Question about an invoice",
        "category": "billing",
        "order_id": "ORD-101",
        "priority": 3,
    },
    {
        "id": "T2",
        "text": "Refund request",
        "category": "billing",
        "order_id": None,
        "priority": 5,
    },
    {
        "id": "T3",
        "text": "Unable to sign in",
        "category": "technical",
        "order_id": "",
        "priority": 4,
    },
]

print(pd.DataFrame(tickets))
print()


def _load_tickets(conn, tickets):
    conn.execute("""
        CREATE TABLE tickets (
            id TEXT,
            text TEXT,
            category TEXT,
            order_id TEXT,
            priority INTEGER
        )
    """)

    conn.executemany("""
        INSERT INTO tickets (id, text, category, order_id, priority)
        VALUES (:id, :text, :category, :order_id, :priority)
    """, tickets)


def category_features(tickets):
    """Return one summary tuple per category, sorted by category."""
    with closing(sqlite3.connect(":memory:")) as conn:
        _load_tickets(conn, tickets)

        return conn.execute("""
            SELECT
                category,
                COUNT(*) AS ticket_count,
                ROUND(AVG(priority), 2) AS avg_priority,
                SUM(CASE WHEN priority >= 4 THEN 1 ELSE 0 END)
                    AS high_priority_count
            FROM tickets
            GROUP BY category
            ORDER BY category ASC
        """).fetchall()


def failing_billing_rows(tickets):
    """Count billing tickets with a NULL or empty order ID."""
    with closing(sqlite3.connect(":memory:")) as conn:
        _load_tickets(conn, tickets)

        count, = conn.execute("""
            SELECT COUNT(*)
            FROM tickets
            WHERE category = 'billing'
              AND (order_id IS NULL OR order_id = '')
        """).fetchone()

        return count


if __name__ == "__main__":
    print(category_features(tickets))
    print(failing_billing_rows(tickets))
