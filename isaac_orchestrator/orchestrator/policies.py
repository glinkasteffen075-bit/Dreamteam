"""Policy checks for task result review in Orchestrator V1."""

from __future__ import annotations

from .enums import EscalationReason
from .models import AgentResult, Task


def _matches_scope(file_path: str, allowed_paths: list[str]) -> bool:
    return any(file_path == allowed or file_path.startswith(f"{allowed}/") for allowed in allowed_paths)


def validate_allowed_files(task: Task, result: AgentResult) -> list[str]:
    """Return violations when changed files are outside allowed scope."""
    allowed = task.scope.allowed_files
    if not allowed:
        return []

    violations: list[str] = []
    for changed in result.changed_files:
        if not _matches_scope(changed, allowed):
            violations.append(f"File outside allowed scope: {changed}")
    return violations


def detect_forbidden_files(task: Task, result: AgentResult) -> list[str]:
    """Return violations when changed files hit forbidden paths."""
    forbidden = task.scope.forbidden_files
    violations: list[str] = []
    for changed in result.changed_files:
        if _matches_scope(changed, forbidden):
            violations.append(f"Forbidden file touched: {changed}")
    return violations


def reject_unexpected_behavior_changes(task: Task, result: AgentResult) -> list[str]:
    """Reject behavior change when task scope forbids it."""
    if result.behavior_changed and not task.scope.allow_behavior_change:
        return ["Unexpected behavior change detected."]
    return []


def reject_unexpected_contract_changes(task: Task, result: AgentResult) -> list[str]:
    """Reject API/contract change when task scope forbids it."""
    if result.contract_changed and not task.scope.allow_contract_change:
        return ["Unexpected contract change detected."]
    return []


def escalation_reason_for(task: Task, result: AgentResult, violations: list[str]) -> EscalationReason | None:
    """Suggest escalation reason for ambiguous or high-risk outcomes."""
    if task.type.value == "architectural_change":
        return EscalationReason.ARCHITECTURE
    if any("behavior" in v.lower() for v in violations):
        return EscalationReason.BEHAVIOR
    if any("scope" in v.lower() or "forbidden" in v.lower() for v in violations):
        return EscalationReason.SCOPE
    if not result.summary.strip():
        return EscalationReason.UNCLEAR
    return None
