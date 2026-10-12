from __future__ import annotations

import os
import time
from typing import Any

from app.models import EvalResult, ProviderConfig
from app.prompts import score_response


class ProviderAdapter:
    provider: str

    def __init__(self, config: ProviderConfig):
        self.config = config

    def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        raise NotImplementedError


class OpenAIProvider(ProviderAdapter):
    provider = "openai"

    def __init__(self, config: ProviderConfig):
        super().__init__(config)
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not set.")

        from openai import OpenAI

        self.client = OpenAI(api_key=self.api_key, timeout=60.0)

    def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature,
        )
        return response.choices[0].message.content or ""


class AnthropicProvider(ProviderAdapter):
    provider = "anthropic"

    def __init__(self, config: ProviderConfig):
        super().__init__(config)
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is not set.")

        import anthropic

        self.client = anthropic.Anthropic(api_key=self.api_key, timeout=60.0)

    def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        response = self.client.messages.create(
            model=self.config.model,
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.config.temperature,
        )
        return response.content[0].text


class OllamaProvider(ProviderAdapter):
    provider = "ollama"

    def __init__(self, config: ProviderConfig):
        super().__init__(config)
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        try:
            from ollama import Client
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("The 'ollama' package is required for Ollama providers.") from exc
        self.client = Client(host=self.base_url)

    def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        response = self.client.generate(
            model=self.config.model,
            prompt=prompt,
            system=system_prompt,
            options={"temperature": self.config.temperature},
        )
        return response["response"]


def build_provider(config: ProviderConfig) -> ProviderAdapter:
    if config.provider == "openai":
        return OpenAIProvider(config)
    if config.provider == "anthropic":
        return AnthropicProvider(config)
    if config.provider == "ollama":
        return OllamaProvider(config)
    raise ValueError(f"Unsupported provider: {config.provider}")


def evaluate_prompt(provider_config: ProviderConfig, prompt_text: str, expected_behavior: str | None, system_prompt: str | None = None) -> EvalResult:
    adapter = build_provider(provider_config)
    start = time.perf_counter()
    response_text = adapter.generate(prompt_text, system_prompt or provider_config.system_prompt)
    elapsed_ms = int((time.perf_counter() - start) * 1000)

    evaluation = score_response(prompt_text, response_text, expected_behavior)
    return EvalResult(
        prompt_id="",
        model=provider_config.model,
        provider=provider_config.provider,
        score=evaluation["score"],
        passed=evaluation["passed"],
        latency_ms=elapsed_ms,
        rubric=evaluation["rubric"],
        response=response_text,
        details={
            "expected_behavior": expected_behavior,
            "prompt": prompt_text,
        },
    )
