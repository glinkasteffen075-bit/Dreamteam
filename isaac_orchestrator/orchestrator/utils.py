"""Utility helpers for Orchestrator V1."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML file into a dictionary."""
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected dict config in {path}, got {type(data).__name__}")
    return data


def ensure_parent_dir(path: Path) -> None:
    """Ensure parent directory exists for a file path."""
    path.parent.mkdir(parents=True, exist_ok=True)
