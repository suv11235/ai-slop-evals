# CGF–FGF prompt specs (stub)

This file will hold the **exact** prompts used to run the multi-turn CGF–FGF game described in `docs/cgf_fgf_strategy.md`.

Design goals:
- Make runs reproducible (exact system prompts + injected background blocks).
- Keep scenario/task text separate from model/runtime parameters (handled by the harness).

## Common blocks

### CGF common system prompt (template)

- Role: CGF (Content Generation Framework)
- Objective: avoid slop across Dimensions I–IV **in function, not just form**
- Hard constraints: do not fabricate facts not in the provided case/material
- Output format: scenario-specific (memo/summary/draft/spec)

### FGF common system prompt (template)

- Role: FGF (Fine-Grained Failure)
- Objective: identify *structural* failure modes that survive patching
- Allowed moves: choose from the argument base in `docs/cgf_fgf_strategy.md#31-the-core-arguments`
- Output format: (1) failure claim, (2) argument applied, (3) how it persists under the proposed patch

## Scenario 1 — Bail recommendation

### CGF task spec (to fill)
```
TODO
```

### CGF slop supplement (to fill)
```
TODO
```

### FGF background (to fill)
```
TODO
```

## Scenario 2 — Public comment summary

### CGF task spec (to fill)
```
TODO
```

### CGF slop supplement (to fill)
```
TODO
```

### FGF background (to fill)
```
TODO
```

## Scenario 3 — Legislative drafting

### CGF task spec (to fill)
```
TODO
```

### CGF slop supplement (to fill)
```
TODO
```

### FGF background (to fill)
```
TODO
```

