from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.models import PromptCase


def generate_default_prompts() -> list[PromptCase]:
    return [
        PromptCase(
            id="summarize-001",
            category="summary",
            prompt="Summarize the benefits of exercise in 2 sentences.",
            expected_behavior="Concise, accurate, and clear summary of the benefits of exercise.",
            metadata={"difficulty": "easy", "tags": ["health", "summary"]},
        ),
        PromptCase(
            id="reason-001",
            category="reasoning",
            prompt="A store has 12 apples. 5 are sold, then 3 more are added. How many apples are there now?",
            expected_behavior="Correct arithmetic showing the total is 10 apples.",
            metadata={"difficulty": "easy", "tags": ["math", "reasoning"]},
        ),
        PromptCase(
            id="rewrite-001",
            category="writing",
            prompt="Rewrite this sentence to be more professional: 'We need to fix this fast because the report is bad.'",
            expected_behavior="Professional, concise, polished language.",
            metadata={"difficulty": "medium", "tags": ["writing", "editing"]},
        ),
        PromptCase(
            id="code-001",
            category="coding",
            prompt="Write a Python function that returns the factorial of a non-negative integer using recursion.",
            expected_behavior="Correct recursive Python function with a base case and validation.",
            metadata={"difficulty": "medium", "tags": ["python", "coding"]},
        ),
    ]


def load_prompt_cases(path: str | Path | None = None) -> list[PromptCase]:
    if path is None:
        return generate_default_prompts()

    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {file_path}")

    raw = json.loads(file_path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("Prompt file must contain a JSON list of prompt objects.")

    prompts: list[PromptCase] = []
    for item in raw:
        prompts.append(
            PromptCase(
                id=str(item["id"]),
                category=str(item.get("category", "general")),
                prompt=str(item["prompt"]),
                expected_behavior=item.get("expected_behavior"),
                metadata=item.get("metadata", {}),
            )
        )
    return prompts


def save_prompt_cases(path: str | Path, prompts: list[PromptCase]) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
        json.dumps([p.to_dict() for p in prompts], indent=2),
        encoding="utf-8",
    )
