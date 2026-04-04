# Harness

## CGF–FGF (OpenRouter)

Runs the multi-turn CGF–FGF loop against models served by OpenRouter and writes one JSONL record per round to `datasets/runs/` (gitignored).

### Setup

- Put your key in `.env` as `OPENROUTER_API_KEY=...`

### Run (Scenario 1: bail recommendation)

```bash
python harness/openrouter_cgf_fgf.py --scenario s1_bail --cgf-model gpt-4o-mini --fgf-model gpt-4o-mini --rounds 2
```

The script prints the output JSONL path it wrote (under `datasets/runs/...`).

