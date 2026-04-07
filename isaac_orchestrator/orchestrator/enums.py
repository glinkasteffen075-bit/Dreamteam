"""Enum definitions for Orchestrator V1."""

from enum import Enum


class TaskType(str, Enum):
    OPERATIONAL_FIX = "operational_fix"
    VERIFICATION = "verification"
    REFACTOR_SAFE = "refactor_safe"
    ARCHITECTURAL_CHANGE = "architectural_change"


class TaskStatus(str, Enum):
    CREATED = "created"
    CLASSIFIED = "classified"
    ASSIGNED = "assigned"
    RUNNING = "running"
    REVIEW_PENDING = "review_pending"
    RETRY_REQUESTED = "retry_requested"
    ESCALATED = "escalated"
    APPROVED = "approved"
    REJECTED = "rejected"
    DONE = "done"
    FAILED = "failed"


class ReviewDecisionType(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    ESCALATE = "escalate"


class EscalationReason(str, Enum):
    ARCHITECTURE = "architecture"
    BEHAVIOR = "behavior"
    SCOPE = "scope"
    UNCLEAR = "unclear"


class AgentType(str, Enum):
    MANUAL = "manual"
    GITHUB = "github"
    CODEX = "codex"
