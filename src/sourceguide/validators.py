from __future__ import annotations

import re

from .models import ProjectScan

ROUTE_FILENAMES = {
    "01-我是小白路线.md",
    "02-快速了解路线.md",
    "03-贡献者路线.md",
    "04-项目面试路线.md",
}


class ValidationError(RuntimeError):
    pass


def validate_bundle(bundle: dict[str, str], scan: ProjectScan) -> None:
    errors: list[str] = []
    for filename, content in bundle.items():
        if filename in ROUTE_FILENAMES and "如何运行" not in content:
            errors.append(f"{filename} is missing runtime guidance.")
        errors.extend(_validate_file_references(filename, content, scan.file_paths))
    if errors:
        raise ValidationError("\n".join(errors))


def _validate_file_references(filename: str, content: str, valid_paths: set[str]) -> list[str]:
    errors: list[str] = []
    allowed_docs = {
        "README.md",
        "run-guide.md",
        "source-map.md",
        "architecture.md",
        "glossary.md",
        "exercises.md",
        "01-我是小白路线.md",
        "02-快速了解路线.md",
        "03-贡献者路线.md",
        "04-项目面试路线.md",
    }
    for ref in re.findall(r"`([^`\n]+\.[A-Za-z0-9]+)`", content):
        if ref in allowed_docs:
            continue
        if ref.startswith("<") or " " in ref:
            continue
        if ref not in valid_paths:
            errors.append(f"{filename} references unknown file `{ref}`.")
    return errors

