"""HTTP client for the local Ollama API."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class OllamaModel:
    name: str
    size: int | None = None
    modified_at: str | None = None


class OllamaClient:
    DEFAULT_BASE_URL = "http://localhost:11434"

    def __init__(self, base_url: str = DEFAULT_BASE_URL, *, timeout: float = 10.0):
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._connected = False
        self._models: list[OllamaModel] = []
        self._current_model: str | None = None

    def is_connected(self) -> bool:
        return self._connected

    def list_models(self) -> list[str]:
        return [m.name for m in self._models]

    def current_model(self) -> str | None:
        return self._current_model

    def set_current_model(self, model_name: str | None):
        self._current_model = model_name

    def refresh(self):
        connected, models = self._probe_and_fetch_models()
        self._connected = connected
        self._models = models

        if self._current_model not in self.list_models():
            if self._models:
                self._current_model = self._models[0].name
            else:
                self._current_model = None

    def probe_and_fetch_models(self):
        self.refresh()
        return self._connected, self._models

    def chat(self, prompt: str) -> str:
        if self._current_model is None:
            raise RuntimeError("No model selected.")

        payload = {
            "model": self._current_model,
            "prompt": prompt,
            "stream": False,
        }

        request = urllib.request.Request(
            self._base_url + "/api/generate",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(request, timeout=300) as response:
            data = json.loads(response.read().decode())

        return data["response"]

    def _probe_and_fetch_models(self):
        try:
            payload = self._get_json("/api/tags")
        except Exception:
            return False, []

        models = []

        for model in payload.get("models", []):
            models.append(
                OllamaModel(
                    name=model["name"],
                    size=model.get("size"),
                    modified_at=model.get("modified_at"),
                )
            )

        return True, models

    def _get_json(self, path: str) -> dict[str, Any]:
        request = urllib.request.Request(
            self._base_url + path,
            headers={"Accept": "application/json"},
        )

        with urllib.request.urlopen(request, timeout=self._timeout) as response:
            return json.loads(response.read().decode())
