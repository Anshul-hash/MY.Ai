"""Central Brain for ZENA."""

from __future__ import annotations

from localai_studio.memory.memory_manager import MemoryManager
from localai_studio.brain.profile import Profile
from localai_studio.brain.projects import Projects
from localai_studio.brain.preferences import Preferences
from localai_studio.brain.conversation import Conversation


class Brain:
    """Central coordinator for all ZENA subsystems."""

    def __init__(self) -> None:
        # Shared long-term memory manager
        self.memory = MemoryManager()

        # Domain modules (all share the same MemoryManager)
        self.profile = Profile(self.memory)
        self.projects = Projects(self.memory)
        self.preferences = Preferences(self.memory)

        # Conversation history
        self.conversation = Conversation()

    def summary(self) -> dict:
        """Return a readable summary of the Brain."""

        return {
            "recent_memories": [
                dict(row)
             for row in self.memory.recent(limit=10)
        ],

            "recent_projects": [
                dict(row)
                for row in self.projects.recent(limit=5)
        ],

        "recent_preferences": [
            dict(row)
            for row in self.preferences.recent(limit=5)
        ],

        "recent_conversation": [
            dict(row)
            for row in self.conversation.last_messages(limit=10)
        ],
    }
  
