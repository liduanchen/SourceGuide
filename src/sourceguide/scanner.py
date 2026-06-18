from __future__ import annotations

from collections import Counter
from pathlib import Path

from .models import FileInfo, ProjectScan

IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}

BINARY_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".mp4",
    ".mov",
    ".avi",
    ".zip",
    ".tar",
    ".gz",
    ".7z",
    ".pdf",
    ".exe",
    ".dll",
    ".so",
    ".dylib",
}

DEPENDENCY_FILES = {
    "pyproject.toml",
    "requirements.txt",
    "setup.py",
    "package.json",
    "go.mod",
    "Cargo.toml",
    "pom.xml",
    "build.gradle",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
}

CONFIG_NAMES = {
    ".env.example",
    "tsconfig.json",
    "vite.config.js",
    "vite.config.ts",
    "next.config.js",
    "pytest.ini",
    "tox.ini",
    "ruff.toml",
    ".ruff.toml",
}

ENTRY_NAMES = {
    "main.py",
    "app.py",
    "cli.py",
    "__main__.py",
    "index.js",
    "index.ts",
    "main.js",
    "main.ts",
    "server.js",
    "server.ts",
    "main.go",
    "main.rs",
}

LANGUAGE_BY_SUFFIX = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
    ".kt": "Kotlin",
    ".rb": "Ruby",
    ".php": "PHP",
    ".cs": "C#",
    ".vue": "Vue",
    ".svelte": "Svelte",
}


def scan_project(root: Path, repo_name: str) -> ProjectScan:
    files: list[FileInfo] = []
    readmes: list[str] = []
    dependency_files: list[str] = []
    config_files: list[str] = []
    entry_candidates: list[str] = []
    test_dirs: set[str] = set()
    example_dirs: set[str] = set()
    language_counts: Counter[str] = Counter()

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel_path = path.relative_to(root).as_posix()
        parts = set(path.relative_to(root).parts[:-1])
        if parts & IGNORE_DIRS:
            continue
        if _should_skip_file(path):
            continue

        size = path.stat().st_size
        role = _classify_file(path)
        files.append(FileInfo(path=rel_path, size=size, suffix=path.suffix, role=role))

        name = path.name
        lower_name = name.lower()
        if lower_name.startswith("readme"):
            readmes.append(rel_path)
        if name in DEPENDENCY_FILES:
            dependency_files.append(rel_path)
        if name in CONFIG_NAMES or name.endswith((".config.js", ".config.ts", ".config.mjs")):
            config_files.append(rel_path)
        if name in ENTRY_NAMES:
            entry_candidates.append(rel_path)
        if any(part.lower() in {"test", "tests", "__tests__"} for part in path.relative_to(root).parts):
            test_dirs.add(_top_level_dir(path, root))
        if any(part.lower() in {"example", "examples", "demo", "demos"} for part in path.relative_to(root).parts):
            example_dirs.add(_top_level_dir(path, root))
        if path.suffix in LANGUAGE_BY_SUFFIX:
            language_counts[LANGUAGE_BY_SUFFIX[path.suffix]] += 1

    files.sort(key=lambda item: item.path)
    return ProjectScan(
        root=root,
        repo_name=repo_name,
        files=files,
        readmes=sorted(readmes),
        dependency_files=sorted(dependency_files),
        config_files=sorted(config_files),
        entry_candidates=sorted(entry_candidates),
        test_dirs=sorted(test_dirs),
        example_dirs=sorted(example_dirs),
        language_counts=dict(language_counts),
    )


def _should_skip_file(path: Path) -> bool:
    name = path.name
    if path.suffix.lower() in BINARY_SUFFIXES:
        return True
    if ".min." in name:
        return True
    try:
        return path.stat().st_size > 300_000
    except OSError:
        return True


def _classify_file(path: Path) -> str:
    name = path.name.lower()
    if name.startswith("readme"):
        return "readme"
    if path.name in DEPENDENCY_FILES:
        return "dependency"
    if path.name in CONFIG_NAMES or name.endswith((".config.js", ".config.ts", ".config.mjs")):
        return "config"
    if path.name in ENTRY_NAMES:
        return "entry"
    if path.suffix.lower() in {".md", ".rst", ".txt"}:
        return "docs"
    return "source"


def _top_level_dir(path: Path, root: Path) -> str:
    relative = path.relative_to(root)
    return relative.parts[0] if len(relative.parts) > 1 else "."

