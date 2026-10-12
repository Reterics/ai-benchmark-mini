# AI Benchmark Mini

A lightweight but production-minded benchmarking harness for evaluating AI model outputs using a consistent prompt set and scoring rubric.

## Features
- Benchmark multiple providers in one run (OpenAI, Anthropic, Ollama)
- Run against a curated prompt library or custom JSON prompt file
- Score responses with structured rubric-based evaluation
- Save full results to JSON and a leaderboard summary
- CLI-first design for automation and CI
- Environment-driven configuration for API keys and model settings

## Project structure

```text
ai-benchmark-mini/
├── README.md
├── pyproject.toml
├── requirements.txt
├── .env.example
├── data/
│   └── prompts.json
├── app/
│   ├── __init__.py
│   ├── cli.py
│   ├── evaluator.py
│   ├── models.py
│   ├── prompts.py
│   ├── providers.py
│   └── runner.py
└── results/
    └── .gitkeep
```

## Quick start

1. Create and activate a virtual environment.
2. Install dependencies.
3. Copy `.env.example` to `.env` and set your keys.
4. Run the CLI.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.cli --provider openai --model gpt-4o-mini
```

## Examples

Run a benchmark against multiple providers:

```bash
python -m app.cli \
  --provider openai --model gpt-4o-mini \
  --provider anthropic --model claude-3-haiku-20240307 \
  --provider ollama --model llama3.1
```

Run with a custom prompt file:

```bash
python -m app.cli --prompt-file ./data/prompts.json --output ./results/run.json
```

List available built-in prompts:

```bash
python -m app.cli --list-prompts
```

## Environment variables

```bash
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
OLLAMA_BASE_URL=http://localhost:11434
```

## Output format

A benchmark run writes results in JSON. Results include:
- prompt id
- provider and model
- score
- pass/fail status
- latency in milliseconds
- rubric breakdown
- raw model output

## Recommended next steps
- Add more prompt types for reasoning, coding, writing, and safety
- Integrate CI checks to validate benchmark stability over time
- Compare models with a leaderboard and trend charts
- Store benchmark results in SQLite or Postgres for long-term comparison

## License

MIT
