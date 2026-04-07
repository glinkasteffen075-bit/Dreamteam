"""Base adapter contract for orchestrator agents."""

from __future__ import annotations

from abc import ABC, abstractmethod

from orchestrator.models import AgentResult, Task


class BaseAgentAdapter(ABC):
    """Abstract adapter interface used by task manager and orchestrator flows."""

    @abstractmethod
    def prepare_instruction(self, task: Task) -> str:
        """Build task instruction payload for agent consumption."""

    @abstractmethod
    def parse_result(self, raw_text: str) -> AgentResult:
        """Parse raw agent output into a validated AgentResult model."""
