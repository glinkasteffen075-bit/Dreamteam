"""Keyword-based task classifier for Orchestrator V1."""

from __future__ import annotations

from .enums import TaskType


KEYWORDS: dict[TaskType, tuple[str, ...]] = {
    TaskType.VERIFICATION: ("verify", "validation", "check", "test"),
    TaskType.OPERATIONAL_FIX: ("fix", "bug", "incident", "hotfix"),
    TaskType.REFACTOR_SAFE: ("refactor", "cleanup", "rename", "format"),
    TaskType.ARCHITECTURAL_CHANGE: ("architecture", "redesign", "restructure", "platform"),
}


def classify_task(description: str) -> TaskType:
    """Classify task by keywords with conservative default to verification."""
    text = description.lower()
    for task_type, words in KEYWORDS.items():
        if any(word in text for word in words):
            return task_type
    return TaskType.VERIFICATION
