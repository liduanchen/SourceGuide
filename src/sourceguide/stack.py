from __future__ import annotations

import json
from pathlib import Path

from .models import ProjectScan, TechStackReport


def identify_stack(scan: ProjectScan) -> TechStackReport:
    evidence: dict[str, list[str]] = {}
    languages = sorted(scan.language_counts, key=scan.language_counts.get, reverse=True)
    package_managers: set[str] = set()
    frameworks: set[str] = set()
    tools: set[str] = set()

    file_paths = scan.file_paths
    _add_by_file(file_paths, "pyproject.toml", "Python", languages, evidence)
    _add_by_file(file_paths, "requirements.txt", "pip", package_managers, evidence)
    _add_by_file(file_paths, "setup.py", "setuptools", package_managers, evidence)
    _add_by_file(file_paths, "package.json", "Node.js", languages, evidence)
    _add_by_file(file_paths, "go.mod", "Go", languages, evidence)
    _add_by_file(file_paths, "Cargo.toml", "Rust", languages, evidence)
    _add_by_file(file_paths, "pom.xml", "Maven", package_managers, evidence)
    _add_by_file(file_paths, "build.gradle", "Gradle", package_managers, evidence)
    _add_by_file(file_paths, "Dockerfile", "Docker", tools, evidence)

    if any(path.startswith("docker-compose.") for path in file_paths):
        tools.add("Docker Compose")
        evidence.setdefault("Docker Compose", []).extend(
            path for path in file_paths if path.startswith("docker-compose.")
        )

    package_json = scan.root / "package.json"
    if package_json.exists():
        _inspect_package_json(package_json, frameworks, package_managers, tools, evidence)

    pyproject = scan.root / "pyproject.toml"
    requirements = scan.root / "requirements.txt"
    text = ""
    if pyproject.exists():
        text += _safe_read(pyproject)
    if requirements.exists():
        text += "\n" + _safe_read(requirements)
    for keyword, framework in {
        "fastapi": "FastAPI",
        "flask": "Flask",
        "django": "Django",
        "pytest": "pytest",
        "typer": "Typer",
    }.items():
        if keyword in text.lower():
            bucket = frameworks if framework not in {"pytest"} else tools
            bucket.add(framework)
            evidence.setdefault(framework, []).extend(
                path for path in ("pyproject.toml", "requirements.txt") if path in file_paths
            )

    return TechStackReport(
        languages=_dedupe(languages),
        package_managers=sorted(package_managers),
        frameworks=sorted(frameworks),
        tools=sorted(tools),
        evidence={key: sorted(set(value)) for key, value in evidence.items()},
    )


def _add_by_file(file_paths: set[str], filename: str, label: str, target, evidence: dict[str, list[str]]) -> None:
    if filename in file_paths:
        if isinstance(target, set):
            target.add(label)
        elif label not in target:
            target.append(label)
        evidence.setdefault(label, []).append(filename)


def _inspect_package_json(
    package_json: Path,
    frameworks: set[str],
    package_managers: set[str],
    tools: set[str],
    evidence: dict[str, list[str]],
) -> None:
    try:
        data = json.loads(package_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    deps = {}
    deps.update(data.get("dependencies", {}))
    deps.update(data.get("devDependencies", {}))
    names = set(deps)
    for package, framework in {
        "next": "Next.js",
        "vite": "Vite",
        "react": "React",
        "vue": "Vue",
        "svelte": "Svelte",
        "express": "Express",
        "@nestjs/core": "NestJS",
    }.items():
        if package in names:
            frameworks.add(framework)
            evidence.setdefault(framework, []).append("package.json")
    for manager_file, manager in {
        "package-lock.json": "npm",
        "pnpm-lock.yaml": "pnpm",
        "yarn.lock": "Yarn",
    }.items():
        if (package_json.parent / manager_file).exists():
            package_managers.add(manager)
            evidence.setdefault(manager, []).append(manager_file)
    if data.get("scripts"):
        tools.add("npm scripts")
        evidence.setdefault("npm scripts", []).append("package.json")


def _safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def _dedupe(values: list[str]) -> list[str]:
    result = []
    for value in values:
        if value not in result:
            result.append(value)
    return result

