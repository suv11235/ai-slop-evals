# CGF–FGF probes

These probes implement the **one-round CGF→FGF→CGF→FGF** loop described in `docs/cgf-fgf.md`.

## Files

- `probes/cgf_fgf/scenarios_round1.v0.jsonl`: initial probe set (toy versions).

## Conventions (v0)

Each JSONL line is a standalone probe with:
- `id`: stable identifier
- `targets`: which slop dimensions are primarily tested
- `scenario`: short label
- `messages`: a chat transcript to run
- `rubric`: checklist for scoring, including “what counts as migration/codependency”

