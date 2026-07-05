"""Conversation history for ZENA."""

from __future__ import annotations

import sqlite3


class Conversation:
    """Stores and retrieves conversation history."""

    def __init__(self, db_path: str = "localai_studio/data/zena.db"):
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def add_user_message(self, message: str) -> None:
        self._save("user", message)

    def add_assistant_message(self, message: str) -> None:
        self._save("assistant", message)

    def _save(self, role: str, message: str) -> None:
        conn = self._connect()

        conn.execute(
            """
            INSERT INTO conversations(role, message)
            VALUES(?, ?)
            """,
            (role, message),
        )

        conn.commit()
        conn.close()

    def last_messages(self, limit: int = 20):
        conn = self._connect()

        rows = conn.execute(
            """
            SELECT *
            FROM conversations
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

        conn.close()

        return list(reversed(rows))

    def clear(self):
        conn = self._connect()

        conn.execute("DELETE FROM conversations")

        conn.commit()
        conn.close()
