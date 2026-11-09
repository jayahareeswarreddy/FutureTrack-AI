"""
LLM access layer: structured output, JSON-schema validation, retries.

Provider-agnostic. Groq and OpenAI both speak the OpenAI chat-completions
protocol, so one client covers both and the provider is a config value rather
than a code path:

    AI_PROVIDER=groq    GROQ_API_KEY=...      (default; free tier, Llama 3.3)
    AI_PROVIDER=openai  OPENAI_API_KEY=...    (GPT-4o-mini)

Three things this module guarantees to its callers:

1. The event loop is never blocked. The SDK call is synchronous, so it runs in
   a worker thread via `asyncio.to_thread`.
2. Every response is parsed as JSON and validated against a JSON Schema. A
   response that does not conform raises `SchemaValidationError`.
3. Transient failures and schema violations are retried with exponential
   backoff and jitter, up to `MAX_RETRIES`. A schema violation feeds the
   validation error back to the model on the next attempt so it can
   self-correct.

If no key is configured, or every attempt fails, callers fall back to the
deterministic rule-based path in `server.py` and the API still answers.
"""

import asyncio
import json
import os
import random
import time
from typing import Any, Callable, Optional

from jsonschema import Draft202012Validator
from jsonschema import ValidationError as JSONSchemaValidationError

# --------------------------------------------------------------- providers

PROVIDERS = {
    "groq": {
        "label": "Groq",
        "env_key": "GROQ_API_KEY",
        "base_url": "https://api.groq.com/openai/v1",
        "default_model": "llama-3.3-70b-versatile",
    },
    "openai": {
        "label": "OpenAI",
        "env_key": "OPENAI_API_KEY",
        "base_url": None,  # SDK default
        "default_model": "gpt-4o-mini",
    },
}

MAX_RETRIES = int(os.getenv("AI_MAX_RETRIES", "3"))
BASE_BACKOFF = float(os.getenv("AI_BASE_BACKOFF", "0.5"))
REQUEST_TIMEOUT = float(os.getenv("AI_TIMEOUT", "30"))


def provider_name() -> str:
    """
    Which provider to use.

    Defaults to groq, but if only OPENAI_API_KEY is present we honour that
    rather than reporting "not configured" at someone holding a usable key.
    """
    explicit = os.getenv("AI_PROVIDER", "").strip().lower()
    if explicit in PROVIDERS:
        return explicit
    if not os.getenv("GROQ_API_KEY", "").strip() and os.getenv("OPENAI_API_KEY", "").strip():
        return "openai"
    return "groq"


def provider_config() -> dict:
    return PROVIDERS[provider_name()]


def api_key() -> str:
    return os.getenv(provider_config()["env_key"], "").strip()


def is_configured() -> bool:
    return bool(api_key())


def model_name() -> str:
    return os.getenv("AI_MODEL", "").strip() or provider_config()["default_model"]


def describe_provider() -> dict:
    """Human-readable provider state, surfaced by GET /health."""
    cfg = provider_config()
    return {
        "provider": cfg["label"],
        "model": model_name(),
        "env_var": cfg["env_key"],
        "configured": is_configured(),
    }


class AIUnavailable(RuntimeError):
    """No API key configured, or every retry was exhausted."""


class SchemaValidationError(ValueError):
    """The model returned JSON that does not match the expected schema."""


def _validate(payload: Any, schema: dict) -> dict:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: list(e.path))
    if errors:
        detail = "; ".join(
            f"{'/'.join(str(p) for p in e.path) or '<root>'}: {e.message}"
            for e in errors[:4]
        )
        raise SchemaValidationError(detail)
    return payload


def _call_llm_sync(system: str, user: str, schema_name: str) -> str:
    """Blocking chat-completions call. Always run through asyncio.to_thread."""
    from openai import OpenAI

    cfg = provider_config()
    kwargs = {"api_key": api_key(), "timeout": REQUEST_TIMEOUT}
    if cfg["base_url"]:
        kwargs["base_url"] = cfg["base_url"]

    client = OpenAI(**kwargs)
    response = client.chat.completions.create(
        model=model_name(),
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        # Forces syntactically valid JSON; the schema check enforces shape.
        # Supported by both Groq and OpenAI.
        response_format={"type": "json_object"},
        max_tokens=900,
        temperature=0.7,
    )
    content = response.choices[0].message.content
    if not content:
        raise SchemaValidationError(f"{schema_name}: model returned empty content")
    return content


async def generate_validated(
    *,
    system: str,
    user: str,
    schema: dict,
    on_attempt: Optional[Callable[[int, str], None]] = None,
) -> dict:
    """
    Ask the model for JSON and return it only once it validates against `schema`.

    Raises AIUnavailable if there is no key or all retries are exhausted.
    """
    if not is_configured():
        raise AIUnavailable(f"{provider_config()['env_key']} is not set")

    schema_name = schema.get("title", "response")
    schema_hint = json.dumps(schema, separators=(",", ":"))
    last_error = "unknown error"
    prompt = user

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            raw = await asyncio.to_thread(
                _call_llm_sync,
                f"{system}\n\nReply with JSON only, matching this JSON Schema:\n{schema_hint}",
                prompt,
                schema_name,
            )
            parsed = json.loads(raw)
            return _validate(parsed, schema)

        except (
            json.JSONDecodeError,
            SchemaValidationError,
            JSONSchemaValidationError,
        ) as exc:
            # The model is reachable but wrong. Show it the error and try again.
            last_error = f"{type(exc).__name__}: {exc}"
            prompt = (
                f"{user}\n\nYour previous reply was rejected by schema "
                f"validation: {exc}\nReturn corrected JSON matching the "
                f"schema exactly."
            )

        except Exception as exc:  # network, rate limit, auth, timeout
            last_error = f"{type(exc).__name__}: {exc}"

        if on_attempt:
            on_attempt(attempt, last_error)

        if attempt < MAX_RETRIES:
            # Exponential backoff with jitter, so retries do not synchronise.
            delay = BASE_BACKOFF * (2 ** (attempt - 1)) + random.uniform(0, 0.25)
            await asyncio.sleep(delay)

    raise AIUnavailable(
        f"{schema_name} failed after {MAX_RETRIES} attempts: {last_error}"
    )


class RetryStats:
    """Counters surfaced by GET /health so retry behaviour is observable."""

    def __init__(self) -> None:
        self.calls = 0
        self.retries = 0
        self.schema_rejections = 0
        self.failures = 0
        self.last_error = None
        self.started = time.time()

    def record_attempt(self, error: str) -> None:
        self.retries += 1
        # Keep the most recent failure so a deployed instance can be
        # diagnosed from /health without shell access to the logs.
        self.last_error = error[:300]
        if "SchemaValidationError" in error or "JSONDecodeError" in error:
            self.schema_rejections += 1

    def as_dict(self) -> dict:
        return {
            "ai_calls": self.calls,
            "retries": self.retries,
            "schema_rejections": self.schema_rejections,
            "fallbacks_to_rule_based": self.failures,
            "last_error": self.last_error,
            "uptime_seconds": round(time.time() - self.started, 1),
        }


stats = RetryStats()
