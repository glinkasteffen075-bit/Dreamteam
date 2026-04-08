from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    base = Path("isaac_orchestrator")
    source_path = base / "data" / "codex_output.json"
    target_path = base / "data" / "agent_result.json"

    if not source_path.exists():
        raise FileNotFoundError(f"Missing {source_path}")

    raw = source_path.read_text(encoding="utf-8").strip()
    parsed = json.loads(raw)

    target_path.write_text(
        json.dumps(parsed, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Saved validated agent result to {target_path}")


if __name__ == "__main__":
    main()
