# Harness

## CGF–FGF (OpenRouter)

Runs the multi-turn CGF–FGF loop against models served by OpenRouter and writes one JSONL record per round to `datasets/runs/` (gitignored).

### Setup

Create an isolated environment and install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Set `OPENROUTER_API_KEY` in `.env` or the shell.

To export traces to Arize AX, also set `ARIZE_API_KEY` and `ARIZE_SPACE_ID`.
`ARIZE_PROJECT_NAME` is optional and defaults to `ai-slop-evals`;
`ARIZE_COLLECTOR_ENDPOINT` can override the default US collector. If the Arize
variables are absent, the harness warns and runs without tracing.

### Run (Scenario 1: bail recommendation)

```bash
python harness/openrouter_cgf_fgf.py --scenario s1_bail --cgf-model gpt-4o-mini --fgf-model gpt-4o-mini --rounds 2
```

The script prints the output JSONL path it wrote (under `datasets/runs/...`).

## Golden evaluation workflow

Generate the committed 40-example set (32 development, 8 holdout):

```bash
python harness/build_golden_dataset.py
```

Create `cgf-fgf-golden-v0` in Arize from
`probes/cgf_fgf/golden_examples.v0.jsonl`, then export it so the runner can use
Arize's server-assigned example IDs.

Run a small real-model baseline before scaling to all development examples:

```bash
python harness/run_golden_baseline.py \
  --dataset-export .arize-tmp-evals/DATASET_EXPORT/examples.json \
  --out datasets/runs/cgf_fgf/baseline.json \
  --split development \
  --limit 5 \
  --rounds 2
```

Apply the deterministic checks:

```bash
python harness/score_golden_runs.py \
  --dataset-export .arize-tmp-evals/DATASET_EXPORT/examples.json \
  --runs datasets/runs/cgf_fgf/baseline.json \
  --out datasets/runs/cgf_fgf/baseline.scores.json
```

After creating and exporting the Arize experiment, convert those scores into
run annotations with `build_experiment_annotations.py`. The reusable
LLM-as-judge contracts live in
`evaluators/cgf_fgf/template_evaluators.v0.json`; validate them against human
labels before enabling continuous evaluation.

