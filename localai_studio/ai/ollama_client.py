"""HTTP client for the local Ollama API."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class OllamaModel:
    """Metadata for an installed Ollama model."""

    name: str
    size: int | None = None
    modified_at: str | None = None


class OllamaClient:
    """Connects to a local Ollama instance and manages model selection."""

    DEFAULT_BASE_URL = "http://localhost:11434"

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        *,
        timeout: float = 5.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._connected = False
        self._models: list[OllamaModel] = []
        self._current_model: str | None = None

    @property
    def base_url(self) -> str:
        return self._base_url

    def is_connected(self) -> bool:
        """Return whether the last probe reached a running Ollama server."""
        return self._connected

    def list_models(self) -> list[str]:
        """Return installed model names from the cached Ollama catalog."""
        return [model.name for model in self._models]

    def current_model(self) -> str | None:
        """Return the user-selected model, if any."""
        return self._current_model

    def set_current_model(self, model_name: str | None) -> None:
        """Persist the active model selection."""
        if model_name is not None and model_name not in self.list_models():
            raise ValueError(f"Model not available: {model_name}")
        self._current_model = model_name

    def refresh(self) -> None:
        """Probe Ollama and reload the installed model list."""
        connected, models = self._probe_and_fetch_models()
        self._connected = connected
        self._models = models if connected else []
        self._ensure_valid_selection()

    def probe_and_fetch_models(self) -> tuple[bool, list[OllamaModel]]:
        """Run a live connection check and return model metadata."""
        connected, models = self._probe_and_fetch_models()
        self._connected = connected
        self._models = models if connected else []
        self._ensure_valid_selection()
        return connected, list(self._models)

    def _ensure_valid_selection(self) -> None:
        available = self.list_models()
        if self._current_model is not None and self._current_model not in available:
            self._current_model = None
        if self._current_model is None and available:
            self._current_model = available[0]

    def _probe_and_fetch_models(self) -> tuple[bool, list[OllamaModel]]:
        try:
            payload = self._get_json("/api/tags")
        except (OllamaConnectionError, OllamaAPIError):
            return False, []

        raw_models = payload.get("models", [])
        if not isinstance(raw_models, list):
            return True, []

        models: list[OllamaModel] = []
        for entry in raw_models:
            if not isinstance(entry, dict):
                continue
            name = entry.get("name")
            if not isinstance(name, str) or not name:
                continue
            size = entry.get("size")
            models.append(
                OllamaModel(
                    name=name,
                    size=size if isinstance(size, int) else None,
                    modified_at=entry.get("modified_at")
                    if isinstance(entry.get("modified_at"), str)
                    else None,
                )
            )

        models.sort(key=lambda model: model.name.lower())
        return True, models

    def _get_json(self, path: str) -> dict[str, Any]:
        url = f"{self._base_url}{path}"
        request = urllib.request.Request(
            url,
            headers={"Accept": "application/json"},
            method="GET",
        )
        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as response:
                body = response.read().decode("utf-8")
        except urllib.error.URLError as exc:
            raise OllamaConnectionError(str(exc)) from exc

        try:
            data = json.loads(body)
        except json.JSONDecodeError as exc:
            raise OllamaAPIError("Ollama returned invalid JSON.") from exc

        if not isinstance(data, dict):
            raise OllamaAPIError("Ollama returned an unexpected payload.")
        return data


class OllamaAPIError(Exception):
    """Raised when Ollama responds with an unexpected payload."""


class OllamaConnectionError(OllamaAPIError):
    """Raised when Ollama cannot be reached."""
