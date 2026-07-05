"""Project manager for ZENA."""

from __future__ import annotations

from localai_studio.memory.memory_manager import MemoryManager


class Projects:
    """Stores and manages user projects."""

    def __init__(self, memory: MemoryManager):
        self.memory = memory

    def add(self, name: str) -> None:
        self.memory.save(
            category="project",
            content=name,
            importance=9,
        )

    def search(self, keyword: str):
        return self.memory.search(keyword)

    def all(self):
        rows = self.memory.search("")

        return [
            row
            for row in rows
            if row["category"] == "project"
        ]

    def recent(self, limit: int = 10):
        rows = self.memory.recent(limit)

        return [
            row
            for row in rows
            if row["category"] == "project"
        ]
