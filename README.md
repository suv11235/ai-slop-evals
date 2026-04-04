# ai-slop-evals

Benchmark + evaluation harness for **communicative slop**: output that is (I) non-receptive to context, (II) pragmatically unaccountable, and/or (III) inferentially unmoored—often with (IV) *surface masking* that makes failures hard to detect.

## What this repo should produce

- A **probe suite** (prompts + variants) targeting each failure mode.
- A **scoring rubric** (human + automated) that separates Dimensions I–IV.
- A **harness** that runs models, collects outputs, and aggregates scores.
- A **versioned dataset** with clear splits and regeneration cadence.

## Action items (roadmap)

### 0) Project hygiene
- [ ] Pick a license + contribution expectations.
- [ ] Decide target audience (research vs product evals) and intended use (public benchmark vs internal regression suite).
- [ ] Define supported model interfaces (OpenAI API, local, etc.) and required artifacts (raw outputs, tool logs, citations).

### 1) Operationalize the dimensions (spec + rubric)
- [ ] Write a 1–2 page **spec** for each dimension with: definition, boundaries, common confusions, and “near-miss” examples.
- [ ] Define **scoring scales** per dimension (e.g., 0–4) with anchor examples.
- [ ] Define how to score **surface masking** as a *divergence* between proxy quality signals and dimensional scores.
- [ ] Decide which dimensions are judged on *single-turn* vs *multi-turn* conversations.

### 2) Probe design (generate a minimum viable suite)

#### Dimension I : Contextual receptivity
- [ ] Contrastive substitution templates (same intent, different constraints/stakes/interlocutors) with a structural-diff scoring plan.
- [ ] Constraint honoring set (explicit unusual constraints + compliance checks).
- [ ] Register tracking set (mid-thread register shift) with a register-drift metric.

#### Dimension II : Pragmatic accountability
- [ ] Hedge decomposition follow-ups (“what would make this wrong?”, “update on counter-evidence?”) with coherence checks.
- [ ] Stakes variance pairs (low vs high stakes) that require *substantive* reorganization, not boilerplate.
- [ ] Refusal calibration matrix (surface harm-signals × actual harm) with scoring for false-positive/false-negative refusals.
- [ ] Consequential self-consistency sequences (recommendation → reveal stakes → see if revision is substantive).

#### Dimension III : Inferential grounding
- [ ] Counterfactual sensitivity prompts (alter a fact, re-probe) with invariance detection.
- [ ] Inference-vs-observation disambiguation prompts with epistemic-status labeling checks.
- [ ] Elicited confabulation audits (details that “should be unknown”) + challenge/verification follow-ups.
- [ ] Correction penetration tests (does a correction propagate to dependent downstream claims?).

#### Dimension IV : Surface masking
- [ ] Self-critique consistency protocol: output → critique on I–III → revise → score “revision penetration”.
- [ ] Patch persistence protocol: strip a surface marker iteratively; test whether failure persists structurally.
- [ ] Proxy–dimension divergence study: collect proxy scores (fluency/coherence/helpfulness/factuality) vs dimensional scores.

### 3) Data model (make everything machine-runnable)
- [ ] Specify a canonical **JSONL schema** for probes:
  - prompt, conversation history, variants, metadata (dimension, probe type, stakes, register, constraints)
  - expected behavioral signatures (what *should* change vs what must not)
  - evaluation instructions for raters and/or automatic checkers
- [ ] Define run outputs schema (model id, params, raw text, tool calls, timestamps).
- [ ] Define scoring outputs schema (per-dimension scores + rationale + flags like “template swap”, “boilerplate hedge”, “false specificity”).

### 4) Scoring + measurement
- [ ] Human rater guide (calibration set + adjudication policy).
- [ ] Inter-rater reliability plan (Krippendorff’s alpha / Cohen’s kappa) and what counts as “good enough”.
- [ ] Automated checks where possible (constraint violations, structural similarity, refusal matrices, citation/claim audits).
- [ ] Define aggregation: per-probe → per-dimension → overall slop score; decide whether IV gates confidence in I–III.

### 5) Harness (repeatable runs)
- [ ] CLI to run a probe subset against one or more models.
- [ ] Deterministic run config capture (seeds, sampling params, system prompts).
- [ ] Result viewer: summary tables + drill-down to conversations and score rationales.
- [ ] CI job to run a small smoke suite on PRs.

### 6) Baselines + release discipline
- [ ] Choose baseline models and a “canary” set for regression detection.
- [ ] Version probes + rubric together; document breaking changes.
- [ ] Establish an eval regeneration cadence (and how to prevent overfitting to public probes).

## Proposed repo layout (minimal)

- `docs/` specs, rubric, rater guide
- `probes/` JSONL probe definitions + templates
- `harness/` runner + adapters + reporting
- `results/` (gitignored) local run outputs
- `datasets/` generated datasets (large local runs gitignored)
- `notebooks/` toy / exploratory experiments

## References

Recent literature notes live in `docs/references.md`.

## CGF–FGF adversarial game

Current strategy lives in `docs/cgf_fgf_strategy.md`. Prompt stubs live in `docs/cgf_fgf_prompt_specs.md`. A draft trajectory schema lives in `probes/cgf_fgf/trajectory_schema.v0.json`.

### Reading the trajectory JSONL

When generated by the harness, trajectories are written as **JSONL** with **one line per round**.

- Group records by `run_id` (a single run/trajectory); order by `round` (0, 1, 2, ...).
- For each record:
  - CGF side: `cgf_system_prompt`, `cgf_slop_supplement`, `cgf_input` (task + any injected critique/patch), `cgf_output`.
  - FGF side: `fgf_background`, `fgf_critique`, and labels: `fgf_argument_applied`, `patch_attempt_type`, `slop_dimensions_implicated`, `failure_depth`.
  - Change tracking: `new_failure_introduced` and `new_failure_description`.

## Next concrete step (MVP)

Create **10 probes per dimension** (40 total), each with at least:
1) a primary prompt, 2) one contrast variant, and 3) a scoring checklist that detects the dimension’s slop signature.
