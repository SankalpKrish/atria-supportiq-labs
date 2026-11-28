import sqlite3
from contextlib import closing

TICKETS_A = [
    {"id": 1, "text": "refund please",      "category": "billing",   "order_id": "A1",  "priority": 3},
    {"id": 2, "text": "where is my order",  "category": "shipping",  "order_id": "A2",  "priority": 2},
    {"id": 3, "text": "double charge",      "category": "billing",   "order_id": None,  "priority": 5},
    {"id": 4, "text": "late delivery",      "category": "shipping",  "order_id": "A4",  "priority": 1},
    {"id": 5, "text": "app keeps crashing", "category": "technical", "order_id": None,  "priority": 4},
]

TICKETS_B = [
    {"id": 10, "text": "wrong item",     "category": "shipping", "order_id": "B1", "priority": 2},
    {"id": 11, "text": "card declined",  "category": "billing",  "order_id": "",   "priority": 4},
    {"id": 12, "text": "invoice wrong",  "category": "billing",  "order_id": "B3", "priority": 4},
    {"id": 13, "text": "package stuck",  "category": "shipping", "order_id": "B4", "priority": 5},
]


def _load_tickets(conn, tickets):
    """Create the tickets table and insert the ticket dicts."""
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
    """Return sorted list of (category, ticket_count, round(avg_priority,2),
    high_priority_count) using a SQL GROUP BY over an in-memory sqlite table."""
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
    """Data test: return the number of 'billing' tickets whose order_id is
    NULL or an empty string."""
    with closing(sqlite3.connect(":memory:")) as conn:
        _load_tickets(conn, tickets)

        count, = conn.execute("""
            SELECT COUNT(*)
            FROM tickets
            WHERE category = 'billing'
              AND (order_id IS NULL OR order_id = '')
        """).fetchone()

        return count
