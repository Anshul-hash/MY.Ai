"""User preferences for ZENA."""

from __future__ import annotations

from localai_studio.memory.memory_manager import MemoryManager


class Preferences:
    """Stores long-term user preferences."""

    def __init__(self, memory: MemoryManager):
        self.memory = memory

    def set_language(self, language: str) -> None:
        self.memory.save(
            category="preference",
            content=f"Language: {language}",
            importance=8,
        )

    def set_voice(self, voice: str) -> None:
        self.memory.save(
            category="preference",
            content=f"Voice: {voice}",
            importance=8,
        )

    def set_theme(self, theme: str) -> None:
        self.memory.save(
            category="preference",
            content=f"Theme: {theme}",
            importance=7,
        )

    def set_compute(self, compute: str) -> None:
        self.memory.save(
            category="preference",
            content=f"Compute: {compute}",
            importance=7,
        )

    def search(self, keyword: str):
        return [
            row
            for row in self.memory.search(keyword)
            if row["category"] == "preference"
        ]

    def recent(self, limit: int = 10):
        return [
            row
            for row in self.memory.recent(limit)
            if row["category"] == "preference"
        ]
