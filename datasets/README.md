# Datasets

This folder is for **generated artifacts** (e.g., CGF–FGF multi-turn trajectories) and any curated evaluation sets that are *not* just “probe definitions”.

Recommended convention:
- `datasets/cgf_fgf/trajectories/`: JSONL (one record per round) conforming to `probes/cgf_fgf/trajectory_schema.v0.json`
- `datasets/cgf_fgf/README.md`: dataset cards (generation procedure, models, date, known issues)

By default, large run outputs should go under `datasets/runs/` and remain gitignored.

