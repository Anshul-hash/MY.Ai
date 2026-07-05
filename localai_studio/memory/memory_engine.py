"""ZENA Memory Engine"""

from __future__ import annotations

from localai_studio.memory.memory_manager import MemoryManager


class MemoryEngine:

    def __init__(self):
        self.memory = MemoryManager()

    def process(self, message: str):

        text = message.lower()

        if "my name is" in text:
            name = message.split("is", 1)[1].strip()

            self.memory.save(
                "profile",
                f"User's name is {name}",
                10,
            )

            return f"I'll remember that your name is {name}."

        if "i like" in text:
            item = message.split("like", 1)[1].strip()

            self.memory.save(
                "preference",
                f"Likes {item}",
                7,
            )

            return f"I'll remember that you like {item}."

        if "i am working on" in text:
            project = message.split("on", 1)[1].strip()

            self.memory.save(
                "project",
                project,
                9,
            )

            return f"I'll remember your project: {project}"

        return None
