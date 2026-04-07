# Orchestrator V1

A minimal Python orchestration hub for local-first task handling. V1 supports task creation, classification, manual agent instruction generation, result ingestion, policy review, and escalation when needed.

## Purpose

Orchestrator V1 provides a small, production-structured base for future extension to Linux/Docker workflows while remaining runnable in Termux-compatible Python.

## Architecture

- `orchestrator/models.py`: Pydantic models for tasks, results, reviews, and escalations.
- `orchestrator/enums.py`: Enum constants for types, statuses, and decisions.
- `orchestrator/task_classifier.py`: Keyword-based conservative classifier.
- `orchestrator/policies.py`: V1 policy checks.
- `orchestrator/review_engine.py`: Approve/reject/escalate decision logic.
- `orchestrator/escalation_engine.py`: Human-readable escalation notice generation.
- `orchestrator/queue_store.py`: JSON persistence helper.
- `orchestrator/adapters/manual_agent.py`: Manual instruction + JSON result parser.
- `orchestrator/adapters/github_agent.py`, `orchestrator/adapters/codex_agent.py`: Stubs for future integrations.
- `main.py`: End-to-end local demo flow.

## How to run

```bash
cd isaac_orchestrator
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Simulate manual agent result

1. Run `python main.py` once to generate a sample task and print instruction.
2. Create `data/agent_result.json` using `examples/sample_agent_result.json` as a template.
3. Run `python main.py` again to parse, review, and persist decision.

Example:

```bash
cp examples/sample_agent_result.json data/agent_result.json
python main.py
```

## V1 limitations

- No web UI.
- No network integrations.
- No GitHub API integration.
- No Codex API integration.
- No background workers/daemon mode.
- JSON persistence only (no SQLite).
