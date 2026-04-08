"""Review engine for evaluating agent results against task policy."""

from __future__ import annotations

from .enums import ReviewDecisionType
from .models import AgentResult, ReviewDecision, Task
from .policies import (
    detect_forbidden_files,
    escalation_reason_for,
    reject_unexpected_behavior_changes,
    reject_unexpected_contract_changes,
    validate_allowed_files,
)


def review_task_result(task: Task, result: AgentResult) -> ReviewDecision:
    """Review result and return approve/reject/escalate decision."""
    violations: list[str] = []
    violations.extend(validate_allowed_files(task, result))
    violations.extend(detect_forbidden_files(task, result))
    violations.extend(reject_unexpected_behavior_changes(task, result))
    violations.extend(reject_unexpected_contract_changes(task, result))

    if violations:
        return ReviewDecision(
            task_id=task.id,
            decision=ReviewDecisionType.REJECT,
            reasons=violations,
        )

    escalation_reason = escalation_reason_for(task, result)
    if escalation_reason is not None:
        return ReviewDecision(
            task_id=task.id,
            decision=ReviewDecisionType.ESCALATE,
            reasons=["Result requires human decision."],
            escalation_reason=escalation_reason,
        )

    return ReviewDecision(
        task_id=task.id,
        decision=ReviewDecisionType.APPROVE,
        reasons=["Result satisfies task scope and policy."],
    )
