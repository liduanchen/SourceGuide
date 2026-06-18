from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from .config import load_config
from .models import GenerateOptions
from .pipeline import generate

app = typer.Typer(help="Turn any GitHub repository into guided source-code learning paths.")
console = Console()


@app.command("generate")
def generate_cmd(
    target: Annotated[str, typer.Argument(help="Local project directory or public GitHub URL.")],
    route: Annotated[str, typer.Option("--route", help="Route: all, beginner, quick, contributor, interview.")] = "all",
    output: Annotated[str | None, typer.Option("--output", help="Output directory.")] = None,
    model: Annotated[str | None, typer.Option("--model", help="Model name.")] = None,
    base_url: Annotated[str | None, typer.Option("--base-url", help="OpenAI-compatible API base URL.")] = None,
    language: Annotated[str | None, typer.Option("--language", help="Output language.")] = None,
    depth: Annotated[str | None, typer.Option("--depth", help="Tutorial depth: basic, normal, deep.")] = None,
    overwrite: Annotated[bool, typer.Option("--overwrite", help="Overwrite existing generated files.")] = False,
    architecture: Annotated[bool, typer.Option("--architecture/--no-architecture", help="Generate architecture.md.")] = True,
    glossary: Annotated[bool, typer.Option("--glossary/--no-glossary", help="Generate glossary.md.")] = True,
) -> None:
    config = load_config()
    if route not in {"all", "beginner", "quick", "contributor", "interview"}:
        raise typer.BadParameter("route must be all, beginner, quick, contributor, or interview")
    chosen_depth = depth or config.depth
    if chosen_depth not in {"basic", "normal", "deep"}:
        raise typer.BadParameter("depth must be basic, normal, or deep")

    options = GenerateOptions(
        target=target,
        route=route,
        output_dir=output or config.output_dir,
        model=model or config.model,
        base_url=base_url or config.base_url,
        language=language or config.language,
        depth=chosen_depth,
        overwrite=overwrite,
        include_architecture=architecture,
        include_glossary=glossary,
        timeout=config.timeout,
        debug=config.debug,
    )
    console.print(f"[bold]SourceGuide[/bold] scanning {target}")
    written = generate(options, api_key=config.api_key)
    console.print("[green]Generated SourceGuide documents:[/green]")
    for path in written:
        console.print(f"- {Path(path)}")


def main() -> None:
    app()
