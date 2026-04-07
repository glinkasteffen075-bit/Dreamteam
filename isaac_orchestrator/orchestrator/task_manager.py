"""Task management utilities for Orchestrator V1."""

from __future__ import annotations

from datetime import datetime

from .enums import TaskStatus
from .models import Task
from .task_classifier import classify_task


def classify_and_update(task: Task) -> Task:
    """Apply classifier and set task metadata for assignment readiness."""
    task.type = classify_task(task.spec.title + " " + task.spec.description)
    task.status = TaskStatus.CLASSIFIED
    task.updated_at = datetime.utcnow()
    return task
