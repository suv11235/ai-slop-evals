# CGF–FGF “patch vs counter” thread (scope + repo fit)

This doc translates the **CGF → FGF** thread into concrete benchmark artifacts.

## Working terms (as used in this repo)

- **CGF (Patch Generator):** the model (or prompting + scaffolding) producing an output and then attempting iterative “patches” to address a critique.
- **FGF (Failure Generator):** an adversarial critic whose job is to show how the patch **fails along Dimensions I–IV** (often via downstream/institutional dynamics rather than surface form).

The core idea: many “fixes” are **surface masking**—they improve proxy signals (hedging, uncertainty language, disclaimers, removal of numbers) without changing the *pragmatic force* or the *grounding* of what will actually be used.

## Why this belongs in this repo

This thread is a generator for:
- **Dimension II probes (Pragmatic Accountability):** “institutional position determines force”, “disclaimer ≠ constraint”, “stake-revealed follow-up”.
- **Dimension IV probes (Surface Masking):** “patch persistence”, “revision penetration”, “knows → does not act”.
- **Dimension I probes (Receptivity):** whether patches structurally reorganize under changed institutional constraints vs template swaps.
- **Dimension III probes (Grounding):** “explicit incompleteness flagging” that is itself distributional; “quasi-confidence intervals”.

## Benchmark primitive: one-round CGF–FGF game

We represent each scenario as a **fixed 1-round loop**:
1) **CGF₀:** produce the initial deliverable (recommendation/summary/draft).
2) **FGF₀:** critique it using a targeted failure claim (e.g., “institutional force overrides hedges”).
3) **CGF₁:** apply one named patch direction (A/B/C/D).
4) **FGF₁:** counter: explain how slop persists (migration, codependency, shallow alignment).

This loop becomes a probe because we can score:
- whether **CGF₁** changes *structure* vs style,
- whether it introduces **new false precision** (e.g., pseudo-CIs),
- whether it **refuses/escalates** appropriately given stakes,
- whether it anticipates **downstream extraction** (“judge skips to actionable element”),
- whether the “patch” is **dependent on human referential behavior** (codependency).

## Scenario families (from the thread)

### Scenario 1: Bail recommendation (high-stakes institutional decision support)
Patch directions: structural de-escalation, explicit incompleteness, refusal to score, meta-commentary.
Key counter-moves: institutional processing bypasses ordering; missing-factor flags are distributional; “don’t use” caveat still functions as recommendation.

### Scenario 2: Public comment summary (compression + downstream simplification)
Patch directions: two-output structure, uncertainty quantification, process transparency appendix, refusal to synthesize (data-only).
Key counter-moves: slop migrates to executive summary; pseudo-quantification; “transparency” is self-referential; human-as-API outsourcing.

### Scenario 3: Legislative drafting (precision without interpretive grounding)
Patch directions: flag contested terms, multiple alternatives, scope restriction with placeholders, process specification not draft.
Key counter-moves: flags are distributional; alternatives multiply choice without grounding; “placeholder draft” still shapes outcomes; specification pre-shapes the human alignment signal.

## Repo mapping

- `docs/cgf-fgf.md` (this file): defines the protocol and what to score.
- `probes/cgf_fgf/`: JSONL probes implementing the 1-round loop per scenario + patch direction.
- `harness/` (later): runner support for multi-turn probes and per-step scoring hooks.
- `notebooks/`: exploratory analyses (e.g., structural similarity metrics, migration heuristics).

## Concrete next step

Start with **3 probes** (one per scenario) and **2 patch directions each**:
- one “reasonable patch” (likely to look good on proxies),
- one “extreme patch” (refusal / remove number / transparency appendix),
then score whether the FGF counter is “winning” via migration/codependency.

