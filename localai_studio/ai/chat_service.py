"""High-level chat service for ZENA."""

from __future__ import annotations

from localai_studio.ai.ollama_client import OllamaClient
from localai_studio.memory.memory_engine import MemoryEngine
from localai_studio.brain.conversation import Conversation


SYSTEM_PROMPT = """
You are ZENA.

You are Anshul's personal AI companion.

Rules:
- Be friendly.
- Be intelligent.
- Be honest.
- Speak naturally.
- Prefer Hindi for normal conversations.
- Use English for programming and code.
- Be concise unless more detail is requested.
- Never invent facts.

Memory:
- Use remembered facts naturally.
- Do not claim to remember something unless it exists.
- If the user shares a long-term preference or project, acknowledge it naturally.
"""


class ChatService:
    """Handles conversations with Ollama and ZENA's memory."""

    def __init__(self) -> None:
        self.client = OllamaClient()
        self.client.refresh()

        # Long-term memory
        self.memory = MemoryEngine()

        # Conversation history
        self.conversation = Conversation()

    def ask(self, message: str) -> str:
        """Process memory, send prompt to Ollama and return the reply."""

        if not self.client.is_connected():
            return "⚠ Ollama is not running."

        if self.client.current_model() is None:
            return "⚠ No model selected."

        # Save user message
        self.conversation.add_user_message(message)

        # Give the memory engine a chance to store useful facts.
        memory_reply = self.memory.process(message)

        # Retrieve recent memories for context.
        recent = self.memory.memory.recent(limit=10)

        memory_context = ""
        if recent:
            memory_context = "\n".join(
                f"- {row['category']}: {row['content']}"
                for row in recent
            )

        prompt = f"""
{SYSTEM_PROMPT}

Known facts about Anshul:
{memory_context}

User:
{message}

ZENA:
"""

        try:
            response = self.client.chat(prompt).strip()

            # Save assistant response
            self.conversation.add_assistant_message(response)

            if memory_reply:
                return f"{memory_reply}\n\n{response}"

            return response

        except Exception as exc:
            return f"Error: {exc}"
