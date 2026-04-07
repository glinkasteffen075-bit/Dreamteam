"""Simple JSON-backed persistence for Orchestrator V1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, List

from .utils import ensure_parent_dir


class JsonQueueStore:
    """A minimal JSON list store with load/save/append operations."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        ensure_parent_dir(file_path)
        if not self.file_path.exists():
            self.save_all([])

    def load_all(self) -> List[dict[str, Any]]:
        """Load all objects from JSON file. Returns empty list on malformed data."""
        try:
            with self.file_path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            if isinstance(data, list):
                return data
            return []
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_all(self, items: List[dict[str, Any]]) -> None:
        """Persist full list atomically enough for V1 local usage."""
        with self.file_path.open("w", encoding="utf-8") as handle:
            json.dump(items, handle, indent=2)

    def append(self, item: dict[str, Any]) -> None:
        """Append one item by loading and saving the full list."""
        items = self.load_all()
        items.append(item)
        self.save_all(items)
