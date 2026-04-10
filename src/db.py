# src/db.py

import sqlite3
from src.models import Event, Alert


DB_PATH = "logs.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                source TEXT,
                user TEXT,
                message TEXT,
                metadata JSON
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS alerts (
                id TEXT PRIMARY KEY,
                event_id TEXT,
                rule_name TEXT,
                level TEXT,
                category TEXT,
                title TEXT,
                ip TEXT,
                user TEXT,
                timestamp TEXT,
                hint TEXT
            )
            """
        )
        conn.commit()


def save_event(ev: Event):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO events (id, timestamp, source, user, message, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                ev.id,
                ev.timestamp,
                ev.source,
                ev.user,
                ev.message,
                str(ev.metadata),
            )
        )
        conn.commit()


def save_alert(alert: Alert):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO alerts (id, event_id, rule_name, level, category, title, ip, user, timestamp, hint)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                alert.id,
                alert.event_id,
                alert.rule_name,
                alert.level,
                alert.category,
                alert.title,
                alert.ip,
                alert.user,
                alert.timestamp,
                alert.hint,
            )
        )
        conn.commit()



