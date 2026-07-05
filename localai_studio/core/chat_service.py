"""Chat service for ZENA."""

from localai_studio.ai.ollama_client import OllamaClient


class ChatService:
    def __init__(self):
        self.client = OllamaClient()
        self.client.refresh()

    def ask(self, prompt: str) -> str:
        if not self.client.is_connected():
            return "⚠ Ollama is not running."

        if self.client.current_model() is None:
            return "⚠ No model selected."

        try:
            return self.client.chat(prompt)
        except Exception as e:
            return f"Error: {e}"
