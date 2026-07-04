"""Placeholder status service for Ollama and hardware indicators."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SystemStatus:
    """Snapshot of runtime connection and hardware state."""

    ollama_connected: bool
    ollama_connection: str
    selected_model: str
    using_gpu: bool
    compute_backend: str


class StatusService:
    """Provides placeholder status data until real integrations are wired."""

    def get_status(self) -> SystemStatus:
        return SystemStatus(
            ollama_connected=False,
            ollama_connection="Disconnected",
            selected_model="No model selected",
            using_gpu=False,
            compute_backend="CPU",
        )
