"""Entry point for running Orchestrator V1 locally."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from orchestrator.adapters.manual_agent import ManualAgentAdapter
from orchestrator.enums import AgentType, ReviewDecisionType, TaskStatus, TaskType
from orchestrator.escalation_engine import build_escalation_notice
from orchestrator.models import Task, TaskScope, TaskSpec
from orchestrator.queue_store import JsonQueueStore
from orchestrator.review_engine import review_task_result
from orchestrator.task_manager import classify_and_update
from orchestrator.utils import load_yaml


def main() -> None:
    root = Path(__file__).resolve().parent
    config = load_yaml(root / "config.yaml")

    tasks_store = JsonQueueStore(root / config["storage"]["tasks_file"])
    reviews_store = JsonQueueStore(root / config["storage"]["reviews_file"])
    escalations_store = JsonQueueStore(root / config["storage"]["escalations_file"])

    task = Task(
        type=TaskType.VERIFICATION,
        status=TaskStatus.CREATED,
        assigned_agent=AgentType.MANUAL,
        spec=TaskSpec(
            title="Verify policy-based review flow",
            description="Verify a local manual-agent result can be reviewed safely.",
            acceptance_criteria=[
                "Instruction is generated",
                "Agent result can be reviewed",
                "Decision is persisted",
            ],
        ),
        scope=TaskScope(
            allowed_files=["orchestrator", "README.md"],
            forbidden_files=["secrets", ".env"],
            allow_behavior_change=False,
            allow_contract_change=False,
        ),
    )

    task = classify_and_update(task)
    task.status = TaskStatus.ASSIGNED
    task.updated_at = datetime.utcnow()
    tasks_store.append(task.model_dump(mode="json"))

    adapter = ManualAgentAdapter()
    instruction = adapter.prepare_instruction(task)
    print("=== Manual Agent Instruction ===")
    print(instruction)

    agent_result_path = root / "data" / "agent_result.json"
    if not agent_result_path.exists():
        print("\nNo data/agent_result.json found. Create it to run review phase.")
        return

    raw_result = agent_result_path.read_text(encoding="utf-8")
    result = adapter.parse_result(raw_result)
    decision = review_task_result(task, result)
    reviews_store.append(decision.model_dump(mode="json"))

    print("\n=== Review Decision ===")
    print(f"Task ID: {decision.task_id}")
    print(f"Decision: {decision.decision.value}")
    print(f"Reasons: {decision.reasons}")

    if decision.decision == ReviewDecisionType.ESCALATE:
        notice = build_escalation_notice(task, decision)
        escalations_store.append(notice.model_dump(mode="json"))
        print("Escalation created:")
        print(f"- Reason: {notice.reason.value}")
        print(f"- Summary: {notice.summary}")


if __name__ == "__main__":
    main()
