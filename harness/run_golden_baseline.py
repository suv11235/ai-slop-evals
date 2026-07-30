#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

from openinference.semconv.trace import OpenInferenceSpanKindValues, SpanAttributes
from opentelemetry.trace import Status, StatusCode

from instrumentation import setup_tracing, shutdown_tracing, tracer
from openrouter_cgf_fgf import (
    build_cgf_messages,
    build_fgf_messages,
    load_dotenv,
    normalize_model,
    openrouter_chat_completion,
    parse_fgf_json,
)


def parse_json_field(value):
    return json.loads(value) if isinstance(value, str) else value


def scenario_from_example(properties: dict) -> dict:
    return {
        "scenario_id": properties["scenario_id"],
        "task": properties["task"],
        "cgf_slop_supplement": properties["cgf_slop_supplement"],
        "fgf_background": properties["fgf_background"],
        "patch_menu": parse_json_field(properties["patch_menu"]),
    }


def run_example(
    *,
    example: dict,
    api_key: str,
    cgf_model: str,
    fgf_model: str,
    rounds: int,
    temperature: float,
    batch_id: str,
) -> dict:
    properties = example["additional_properties"]
    scenario = scenario_from_example(properties)
    prior_fgf = None
    trajectory = []

    with tracer.start_as_current_span("golden_example.run") as span:
        span.set_attribute(
            SpanAttributes.OPENINFERENCE_SPAN_KIND,
            OpenInferenceSpanKindValues.CHAIN.value,
        )
        span.set_attribute(SpanAttributes.SESSION_ID, batch_id)
        span.set_attribute(SpanAttributes.INPUT_VALUE, properties["task"])
        span.set_attribute("metadata.example_id", properties["local_example_id"])
        span.set_attribute("metadata.probe_type", properties["probe_type"])

        for round_n in range(rounds):
            cgf_messages = build_cgf_messages(
                round_n=round_n,
                prior_fgf=prior_fgf,
                scenario=scenario,
            )
            cgf_output = openrouter_chat_completion(
                api_key=api_key,
                model=cgf_model,
                messages=cgf_messages,
                temperature=temperature,
                operation_name="cgf",
                session_id=batch_id,
            )
            fgf_messages = build_fgf_messages(cgf_output=cgf_output, scenario=scenario)
            fgf_raw = openrouter_chat_completion(
                api_key=api_key,
                model=fgf_model,
                messages=fgf_messages,
                temperature=0.0,
                operation_name="fgf",
                session_id=batch_id,
            )
            fgf = parse_fgf_json(fgf_raw, patch_menu=scenario["patch_menu"])
            trajectory.append(
                {
                    "round": round_n,
                    "cgf_output": cgf_output,
                    "fgf_critique": fgf["fgf_critique"].strip(),
                    "fgf_argument_applied": fgf["fgf_argument_applied"],
                    "patch_attempt_type": fgf["patch_attempt_type"],
                    "slop_dimensions_implicated": fgf["slop_dimensions_implicated"],
                    "new_failure_introduced": fgf["new_failure_introduced"],
                    "new_failure_description": fgf.get("new_failure_description", ""),
                    "failure_depth": fgf["failure_depth"],
                }
            )
            prior_fgf = {
                "fgf_critique": trajectory[-1]["fgf_critique"],
                "patch_attempt_type": trajectory[-1]["patch_attempt_type"],
            }

        final_output = trajectory[-1]["cgf_output"]
        span.set_attribute(SpanAttributes.OUTPUT_VALUE, final_output)
        span.set_status(Status(StatusCode.OK))

    return {
        "example_id": example["id"],
        "output": final_output,
        "local_example_id": properties["local_example_id"],
        "probe_type": properties["probe_type"],
        "split": properties["split"],
        "cgf_model": cgf_model,
        "fgf_model": fgf_model,
        "rounds": rounds,
        "trajectory": trajectory,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-export", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--split", default="development")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--rounds", type=int, default=2)
    parser.add_argument("--cgf-model", default="gpt-4o-mini")
    parser.add_argument("--fgf-model", default="gpt-4o-mini")
    parser.add_argument("--temperature", type=float, default=0.2)
    args = parser.parse_args()

    load_dotenv(".env")
    api_key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENROUTER_KEY")
    if not api_key:
        raise SystemExit("Missing OPENROUTER_API_KEY in environment or .env")

    examples = json.loads(args.dataset_export.read_text(encoding="utf-8"))
    examples = sorted(
        (
            example
            for example in examples
            if example["additional_properties"]["split"] == args.split
        ),
        key=lambda example: example["additional_properties"]["local_example_id"],
    )[: args.limit]
    if not examples:
        raise SystemExit(f"No examples found for split={args.split!r}")

    batch_id = dt.datetime.now(dt.timezone.utc).strftime("golden-%Y%m%dT%H%M%SZ")
    tracer_provider = setup_tracing()
    try:
        runs = []
        for index, example in enumerate(examples, start=1):
            local_id = example["additional_properties"]["local_example_id"]
            print(f"[{index}/{len(examples)}] {local_id}", file=sys.stderr)
            runs.append(
                run_example(
                    example=example,
                    api_key=api_key,
                    cgf_model=normalize_model(args.cgf_model),
                    fgf_model=normalize_model(args.fgf_model),
                    rounds=args.rounds,
                    temperature=args.temperature,
                    batch_id=batch_id,
                )
            )
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(runs, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote {len(runs)} real-model runs to {args.out}")
    finally:
        shutdown_tracing(tracer_provider)


if __name__ == "__main__":
    main()
