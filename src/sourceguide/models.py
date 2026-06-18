from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


ROUTES = ("beginner", "quick", "contributor", "interview")


@dataclass(frozen=True)
class AppConfig:
    api_key: str | None
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4.1-mini"
    language: str = "zh-CN"
    output_dir: str = "docs/sourceguide"
    depth: str = "normal"
    timeout: float = 60.0
    debug: bool = False


@dataclass(frozen=True)
class GenerateOptions:
    target: str
    route: str = "all"
    output_dir: str = "docs/sourceguide"
    model: str = "gpt-4.1-mini"
    base_url: str = "https://api.openai.com/v1"
    language: str = "zh-CN"
    depth: str = "normal"
    overwrite: bool = False
    include_architecture: bool = True
    include_glossary: bool = True
    timeout: float = 60.0
    debug: bool = False


@dataclass(frozen=True)
class RepositoryInfo:
    source: str
    root: Path
    name: str
    is_temporary: bool = False
    default_branch: str | None = None


@dataclass(frozen=True)
class FileInfo:
    path: str
    size: int
    suffix: str
    role: str = "source"


@dataclass(frozen=True)
class ProjectScan:
    root: Path
    repo_name: str
    files: list[FileInfo]
    readmes: list[str] = field(default_factory=list)
    dependency_files: list[str] = field(default_factory=list)
    config_files: list[str] = field(default_factory=list)
    entry_candidates: list[str] = field(default_factory=list)
    test_dirs: list[str] = field(default_factory=list)
    example_dirs: list[str] = field(default_factory=list)
    language_counts: dict[str, int] = field(default_factory=dict)

    @property
    def file_paths(self) -> set[str]:
        return {file.path for file in self.files}


@dataclass(frozen=True)
class TechStackReport:
    languages: list[str]
    package_managers: list[str]
    frameworks: list[str]
    tools: list[str]
    evidence: dict[str, list[str]]


@dataclass(frozen=True)
class RuntimeCommand:
    title: str
    command: str
    confidence: str
    evidence: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class RuntimeReport:
    recommended: list[RuntimeCommand]
    alternatives: list[RuntimeCommand]
    install: list[RuntimeCommand]
    tests: list[RuntimeCommand]
    lint: list[RuntimeCommand]
    environment: list[str]
    unknowns: list[str]


@dataclass(frozen=True)
class CoreFile:
    path: str
    reason: str
    score: int


@dataclass(frozen=True)
class CoreFileReport:
    files: list[CoreFile]


@dataclass(frozen=True)
class AnalysisContext:
    repository: RepositoryInfo
    scan: ProjectScan
    tech_stack: TechStackReport
    runtime: RuntimeReport
    core_files: CoreFileReport
    options: GenerateOptions

