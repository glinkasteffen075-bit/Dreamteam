"""Pydantic data models for Orchestrator V1."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from .enums import (
    AgentType,
    EscalationReason,
    ReviewDecisionType,
    TaskStatus,
    TaskType,
)


class TaskScope(BaseModel):
    """Describes boundaries and expected constraints for a task."""

    allowed_files: List[str] = Field(default_factory=list)
    forbidden_files: List[str] = Field(default_factory=list)
    allow_behavior_change: bool = False
    allow_contract_change: bool = False


class TaskSpec(BaseModel):
    """Represents a task's business intent and execution details."""

    title: str
    description: str
    acceptance_criteria: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)


class Task(BaseModel):
    """Main task entity tracked by the orchestrator."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    type: TaskType
    status: TaskStatus = TaskStatus.CREATED
    spec: TaskSpec
    scope: TaskScope
    assigned_agent: AgentType = AgentType.MANUAL


class AgentResult(BaseModel):
    """Structured result produced by an agent."""

    task_id: str
    summary: str
    changed_files: List[str] = Field(default_factory=list)
    behavior_changed: bool = False
    contract_changed: bool = False
    tests_run: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)


class ReviewDecision(BaseModel):
    """Review output from policy and review engines."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    task_id: str
    decision: ReviewDecisionType
    reasons: List[str] = Field(default_factory=list)
    escalation_reason: Optional[EscalationReason] = None


class EscalationNotice(BaseModel):
    """Human-readable escalation object for unresolved or risky outcomes."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    task_id: str
    reason: EscalationReason
    summary: str
    details: List[str] = Field(default_factory=list)
