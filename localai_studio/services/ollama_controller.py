"""Qt-facing coordinator for background Ollama polling."""

from __future__ import annotations

from PySide6.QtCore import QObject, QThread, QTimer, Signal

from localai_studio.ai.ollama_client import OllamaClient


class _OllamaRefreshWorker(QThread):
    """Fetch Ollama state off the UI thread."""

    finished_with_state = Signal(bool, list)

    def __init__(self, client: OllamaClient, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._client = client

    def run(self) -> None:
        connected, models = self._client.probe_and_fetch_models()
        self.finished_with_state.emit(connected, [model.name for model in models])


class OllamaController(QObject):
    """Polls Ollama periodically and broadcasts state changes."""

    connection_changed = Signal(bool)
    models_changed = Signal(list)
    current_model_changed = Signal(str)

    def __init__(
        self,
        client: OllamaClient | None = None,
        *,
        poll_interval_ms: int = 5000,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._client = client or OllamaClient()
        self._poll_interval_ms = poll_interval_ms
        self._worker: _OllamaRefreshWorker | None = None
        self._last_connected = False
        self._last_models: list[str] = []
        self._last_current_model: str | None = None

        self._timer = QTimer(self)
        self._timer.setInterval(self._poll_interval_ms)
        self._timer.timeout.connect(self.refresh)

    @property
    def client(self) -> OllamaClient:
        return self._client

    def start(self) -> None:
        self.refresh()
        self._timer.start()

    def stop(self) -> None:
        self._timer.stop()
        if self._worker is not None and self._worker.isRunning():
            self._worker.wait()

    def refresh(self) -> None:
        if self._worker is not None and self._worker.isRunning():
            return

        self._worker = _OllamaRefreshWorker(self._client, self)
        self._worker.finished_with_state.connect(self._on_refresh_finished)
        self._worker.finished.connect(self._on_worker_finished)
        self._worker.start()

    def select_model(self, model_name: str) -> None:
        if not model_name:
            return
        if model_name not in self._client.list_models():
            return
        if self._client.current_model() == model_name:
            return
        self._client.set_current_model(model_name)
        self._emit_current_model_if_changed()

    def _on_refresh_finished(self, connected: bool, models: list) -> None:
        if connected != self._last_connected:
            self._last_connected = connected
            self.connection_changed.emit(connected)

        if models != self._last_models:
            self._last_models = list(models)
            self.models_changed.emit(self._last_models)

        self._emit_current_model_if_changed()

    def _emit_current_model_if_changed(self) -> None:
        current = self._client.current_model()
        if current != self._last_current_model:
            self._last_current_model = current
            if current is not None:
                self.current_model_changed.emit(current)

    def _on_worker_finished(self) -> None:
        self._worker = None
