from __future__ import annotations

import os

from .models import AppConfig


def _bool_from_env(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _float_from_env(value: str | None, default: float) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def load_config(environ: dict[str, str] | None = None) -> AppConfig:
    env = environ if environ is not None else os.environ
    return AppConfig(
        api_key=env.get("OPENAI_API_KEY"),
        base_url=env.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        model=env.get("SOURCEGUIDE_MODEL", "gpt-4.1-mini"),
        language=env.get("SOURCEGUIDE_LANGUAGE", "zh-CN"),
        output_dir=env.get("SOURCEGUIDE_OUTPUT_DIR", "docs/sourceguide"),
        depth=env.get("SOURCEGUIDE_DEPTH", "normal"),
        timeout=_float_from_env(env.get("SOURCEGUIDE_TIMEOUT"), 60.0),
        debug=_bool_from_env(env.get("SOURCEGUIDE_DEBUG"), False),
    )

