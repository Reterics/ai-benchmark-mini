from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class PromptCase:
    id: str
    category: str
    prompt: str
    expected_behavior: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ProviderConfig:
    provider: str
    model: str
    system_prompt: str | None = None
    temperature: float = 0.2

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class EvaluationBreakdown:
    relevance: float
    correctness: float
    clarity: float
    completeness: float
    overall: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class EvalResult:
    prompt_id: str
    model: str
    provider: str
    score: float
    passed: bool
    latency_ms: int
    rubric: dict[str, float]
    response: str
    details: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
