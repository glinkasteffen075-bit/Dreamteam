from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    source_path = Path("data/codex_output.json")
    target_path = Path("data/agent_result.json")

    if not source_path.exists():
        raise FileNotFoundError("Missing data/codex_output.json")

    raw = source_path.read_text(encoding="utf-8").strip()
    parsed = json.loads(raw)

    target_path.write_text(
        json.dumps(parsed, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Saved validated agent result to {target_path}")


if __name__ == "__main__":
    main()
