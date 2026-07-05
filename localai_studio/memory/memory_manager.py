"""ZENA Memory Manager"""

from __future__ import annotations

from localai_studio.database.database import Database


class MemoryManager:

    def __init__(self):
        self.db = Database()

    def save(self, category: str, content: str, importance: int = 1):

        self.db.execute(
            """
            INSERT INTO memories(category, content, importance)
            VALUES (?, ?, ?)
            """,
            (category, content, importance),
        )

    def search(self, keyword: str):

        return self.db.query(
            """
            SELECT *
            FROM memories
            WHERE content LIKE ?
            ORDER BY importance DESC
            """,
            (f"%{keyword}%",),
        )

    def recent(self, limit: int = 10):

        return self.db.query(
            """
            SELECT *
            FROM memories
            ORDER BY created DESC
            LIMIT ?
            """,
            (limit,),
        )

    def delete(self, memory_id: int):

        self.db.execute(
            """
            DELETE FROM memories
            WHERE id=?
            """,
            (memory_id,),
        )
