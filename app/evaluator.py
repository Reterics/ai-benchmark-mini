from __future__ import annotations

import re
from typing import Any


def normalize_text(value: str) -> str:
    return " ".join(re.sub(r"\s+", " ", value.lower()).split())


def extract_keywords(text: str) -> set[str]:
    return {word for word in re.findall(r"[a-zA-Z0-9]+", normalize_text(text)) if len(word) > 2}


def score_response(prompt: str, response: str, expected: str | None = None) -> dict[str, Any]:
    prompt_keywords = extract_keywords(prompt)
    response_keywords = extract_keywords(response)
    expected_keywords = extract_keywords(expected or "")

    relevance = 0.0
    if prompt_keywords and response_keywords:
        overlap = len(prompt_keywords & response_keywords)
        relevance = min(1.0, overlap / max(len(prompt_keywords), 1))

    correctness = 0.0
    if expected:
        expected_tokens = normalize_text(expected)
        response_tokens = normalize_text(response)
        if expected_tokens and response_tokens:
            correctness = 1.0 if expected_tokens in response_tokens or response_tokens in expected_tokens else 0.5
    else:
        correctness = 0.8 if response.strip() else 0.0

    clarity = 0.0
    if response.strip():
        sentence_count = max(1, len(re.findall(r"[.!?]", response)))
        clarity = min(1.0, 0.5 + (len(response.strip().split()) / 80) * 0.5)
        clarity = min(clarity, 1.0 / sentence_count * 0.8 + 0.2)

    completeness = 0.0
    if response.strip():
        completeness = 0.7 if len(response.strip().split()) > 5 else 0.4

    if expected and expected_keywords:
        expected_overlap = len(expected_keywords & response_keywords)
        correctness = max(correctness, min(1.0, expected_overlap / max(len(expected_keywords), 1)))

    rubric = {
        "relevance": round(relevance, 3),
        "correctness": round(correctness, 3),
        "clarity": round(clarity, 3),
        "completeness": round(completeness, 3),
    }

    overall = (
        rubric["relevance"] * 0.3
        + rubric["correctness"] * 0.4
        + rubric["clarity"] * 0.15
        + rubric["completeness"] * 0.15
    )

    return {
        "score": round(overall, 3),
        "passed": overall >= 0.7,
        "rubric": rubric,
    }
