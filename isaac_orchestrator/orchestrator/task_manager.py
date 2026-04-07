"""Task management utilities for Orchestrator V1."""

from __future__ import annotations

from datetime import datetime

from .enums import TaskStatus
from .models import Task


def classify_and_update(task: Task) -> Task:
    """Apply classifier and set task metadata for assignment readiness."""
    task.status = TaskStatus.CLASSIFIED
    task.updated_at = datetime.utcnow()
    return task
