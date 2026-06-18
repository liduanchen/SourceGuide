from __future__ import annotations

from pathlib import Path

from .ai import AIClient, OpenAICompatibleClient
from .core_files import identify_core_files
from .models import AnalysisContext, GenerateOptions
from .repository import prepare_repository
from .scanner import scan_project
from .stack import identify_stack
from .runtime import infer_runtime
from .validators import validate_bundle
from .writer import write_bundle


def selected_routes(route: str) -> list[str]:
    if route == "all":
        return ["beginner", "quick", "contributor", "interview"]
    return [route]


def generate(options: GenerateOptions, api_key: str | None, ai_client: AIClient | None = None) -> list[Path]:
    repository = prepare_repository(options.target)
    scan = scan_project(repository.root, repository.name)
    tech_stack = identify_stack(scan)
    runtime = infer_runtime(scan, tech_stack)
    core_files = identify_core_files(scan)
    context = AnalysisContext(
        repository=repository,
        scan=scan,
        tech_stack=tech_stack,
        runtime=runtime,
        core_files=core_files,
        options=options,
    )
    routes = selected_routes(options.route)
    client = ai_client or OpenAICompatibleClient(
        api_key=api_key or "",
        base_url=options.base_url,
        model=options.model,
        timeout=options.timeout,
    )
    bundle = client.generate_markdown_bundle(context, routes)
    validate_bundle(bundle, scan)
    output_dir = Path(options.output_dir)
    if not output_dir.is_absolute():
        output_dir = repository.root / output_dir
    return write_bundle(bundle, output_dir, overwrite=options.overwrite)

