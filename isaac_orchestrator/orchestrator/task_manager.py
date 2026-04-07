"""Task management utilities for Orchestrator V1."""

from __future__ import annotations

from datetime import datetime

from .enums import TaskStatus
from .models import Task


def classify_and_update(task: Task) -> Task:
    """Set task metadata for assignment readiness without overwriting explicit type."""
    task.status = TaskStatus.CLASSIFIED
    task.updated_at = datetime.utcnow()
    return task