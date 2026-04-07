"""Escalation creation helpers for Orchestrator V1."""

from __future__ import annotations

from .enums import ReviewDecisionType
from .models import EscalationNotice, ReviewDecision, Task


def build_escalation_notice(task: Task, decision: ReviewDecision) -> EscalationNotice:
    """Convert an escalation review decision to a human-readable notice."""
    if decision.decision != ReviewDecisionType.ESCALATE or decision.escalation_reason is None:
        raise ValueError("Escalation notice can only be built from escalation decisions.")

    summary = f"Task '{task.spec.title}' requires human review ({decision.escalation_reason.value})."
    return EscalationNotice(
        task_id=task.id,
        reason=decision.escalation_reason,
        summary=summary,
        details=decision.reasons,
    )
