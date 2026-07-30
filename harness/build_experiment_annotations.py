#!/usr/bin/env python3

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scores", type=Path, required=True)
    parser.add_argument("--experiment-export", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    scores = json.loads(args.scores.read_text(encoding="utf-8"))
    scores_by_example = {row["example_id"]: row for row in scores}
    experiment_runs = json.loads(args.experiment_export.read_text(encoding="utf-8"))

    annotations = []
    for run in experiment_runs:
        score_row = scores_by_example[run["example_id"]]
        values = []
        for name, evaluation in score_row["evaluations"].items():
            values.append(
                {
                    "name": name,
                    "label": evaluation["label"],
                    "text": evaluation["explanation"],
                }
            )
        annotations.append({"record_id": run["id"], "values": values})

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(annotations, indent=2), encoding="utf-8")
    print(f"Wrote annotations for {len(annotations)} experiment runs to {args.out}")


if __name__ == "__main__":
    main()
