"""Placeholder Codex adapter for future integration (V1 non-goal)."""

from __future__ import annotations

from orchestrator.adapters.base import BaseAgentAdapter
from orchestrator.models import AgentResult, Task


class CodexAgentAdapter(BaseAgentAdapter):
    """Stub adapter for future Codex-based execution."""

    def prepare_instruction(self, task: Task) -> str:
        raise NotImplementedError("Codex adapter is not implemented in V1.")

    def parse_result(self, raw_text: str) -> AgentResult:
        raise NotImplementedError("Codex adapter is not implemented in V1.")
