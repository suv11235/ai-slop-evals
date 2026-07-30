import os
import warnings

from arize.otel import register
from openinference.instrumentation import TracerProvider
from opentelemetry.trace import get_tracer


DEFAULT_PROJECT_NAME = "ai-slop-evals"

tracer = get_tracer(DEFAULT_PROJECT_NAME)


def setup_tracing() -> TracerProvider | None:
    missing = [
        name
        for name in ("ARIZE_API_KEY", "ARIZE_SPACE_ID")
        if not os.environ.get(name)
    ]
    if missing:
        warnings.warn(
            "Arize tracing is disabled; set " + " and ".join(missing) + " to enable it.",
            stacklevel=2,
        )
        return None

    options = {
        "api_key": os.environ["ARIZE_API_KEY"],
        "space_id": os.environ["ARIZE_SPACE_ID"],
        "project_name": os.environ.get("ARIZE_PROJECT_NAME", DEFAULT_PROJECT_NAME),
        "verbose": False,
    }
    endpoint = os.environ.get("ARIZE_COLLECTOR_ENDPOINT")
    if endpoint:
        options["endpoint"] = endpoint

    try:
        return register(**options)
    except Exception as exc:
        warnings.warn(f"Arize tracing initialization failed; continuing without tracing: {exc}", stacklevel=2)
        return None


def shutdown_tracing(tracer_provider: TracerProvider | None) -> None:
    if tracer_provider is None:
        return

    try:
        if not tracer_provider.force_flush():
            warnings.warn("Arize tracing flush timed out.", stacklevel=2)
    finally:
        tracer_provider.shutdown()
