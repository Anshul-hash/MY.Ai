"""Status aggregation for the application status bar."""

from __future__ import annotations

from dataclasses import dataclass

from localai_studio.ai.ollama_client import OllamaClient


@dataclass(frozen=True)
class SystemStatus:
    """Snapshot of runtime connection and hardware state."""

    ollama_connected: bool
    ollama_connection: str
    selected_model: str
    using_gpu: bool
    compute_backend: str


class StatusService:
    """Builds status snapshots from live Ollama client state."""

    def get_status(self, ollama: OllamaClient) -> SystemStatus:
        connected = ollama.is_connected()
        current = ollama.current_model()

        return SystemStatus(
            ollama_connected=connected,
            ollama_connection="Connected" if connected else "Disconnected",
            selected_model=current or "No model selected",
            using_gpu=False,
            compute_backend="CPU",
        )
