from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from app.evaluator import evaluate_prompt
from app.models import EvalResult, PromptCase, ProviderConfig
from app.prompts import load_prompt_cases


class BenchmarkRunner:
    def __init__(self, provider_configs: list[ProviderConfig], prompt_file: str | Path | None = None):
        self.provider_configs = provider_configs
        self.prompts = load_prompt_cases(prompt_file)

    def run(self) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for config in self.provider_configs:
            for prompt in self.prompts:
                evaluation = evaluate_prompt(
                    provider_config=config,
                    prompt_text=prompt.prompt,
                    expected_behavior=prompt.expected_behavior,
                    system_prompt=config.system_prompt,
                )
                evaluation.prompt_id = prompt.id
                results.append(
                    {
                        "prompt_id": prompt.id,
                        "category": prompt.category,
                        "provider": config.provider,
                        "model": config.model,
                        "score": evaluation.score,
                        "passed": evaluation.passed,
                        "latency_ms": evaluation.latency_ms,
                        "rubric": evaluation.rubric,
                        "response": evaluation.response,
                        "metadata": prompt.metadata,
                    }
                )
        return results

    def leaderboard(self, results: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return sorted(results, key=lambda item: (-item["score"], item["provider"], item["model"]))

    def write_json(self, results: list[dict[str, Any]], output_path: str | Path) -> None:
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(results, indent=2), encoding="utf-8")

    def write_csv(self, results: list[dict[str, Any]], output_path: str | Path) -> None:
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "prompt_id",
                    "category",
                    "provider",
                    "model",
                    "score",
                    "passed",
                    "latency_ms",
                    "response",
                ],
            )
            writer.writeheader()
            for row in results:
                writer.writerow({
                    "prompt_id": row["prompt_id"],
                    "category": row["category"],
                    "provider": row["provider"],
                    "model": row["model"],
                    "score": row["score"],
                    "passed": row["passed"],
                    "latency_ms": row["latency_ms"],
                    "response": row["response"],
                })


def build_default_runner(provider_names: list[str], model_names: list[str], prompt_file: str | Path | None = None) -> BenchmarkRunner:
    configs = []
    for index, provider in enumerate(provider_names):
        model = model_names[index]
        configs.append(ProviderConfig(provider=provider, model=model))
    return BenchmarkRunner(configs, prompt_file)
