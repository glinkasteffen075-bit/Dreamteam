"""Manual adapter: emits structured instructions and parses JSON results."""

from __future__ import annotations

import json

from orchestrator.adapters.base import BaseAgentAdapter
from orchestrator.models import AgentResult, Task


class ManualAgentAdapter(BaseAgentAdapter):
    """Adapter for human/manual execution and JSON result submission."""

    def prepare_instruction(self, task: Task) -> str:
        criteria = "\n".join(f"- {item}" for item in task.spec.acceptance_criteria) or "- (none)"
        allowed = ", ".join(task.scope.allowed_files) or "(not restricted)"
        forbidden = ", ".join(task.scope.forbidden_files) or "(none)"
        return (
            f"Task ID: {task.id}\n"
            f"Type: {task.type.value}\n"
            f"Title: {task.spec.title}\n"
            f"Description: {task.spec.description}\n"
            f"Acceptance Criteria:\n{criteria}\n"
            f"Scope Allowed Files: {allowed}\n"
            f"Scope Forbidden Files: {forbidden}\n"
            f"Behavior Change Allowed: {task.scope.allow_behavior_change}\n"
            f"Contract Change Allowed: {task.scope.allow_contract_change}\n\n"
            "Return result as JSON matching AgentResult fields."
        )

    def parse_result(self, raw_text: str) -> AgentResult:
        payload = json.loads(raw_text)
        return AgentResult.model_validate(payload)
