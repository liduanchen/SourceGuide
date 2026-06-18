from __future__ import annotations

import json
import re
from pathlib import Path

from .models import ProjectScan, RuntimeCommand, RuntimeReport, TechStackReport


def infer_runtime(scan: ProjectScan, tech_stack: TechStackReport) -> RuntimeReport:
    install: list[RuntimeCommand] = []
    recommended: list[RuntimeCommand] = []
    alternatives: list[RuntimeCommand] = []
    tests: list[RuntimeCommand] = []
    lint: list[RuntimeCommand] = []
    environment: list[str] = []
    unknowns: list[str] = []

    package_json = scan.root / "package.json"
    if package_json.exists():
        _from_package_json(package_json, install, recommended, tests, lint, environment)

    if (scan.root / "pyproject.toml").exists() or (scan.root / "requirements.txt").exists():
        environment.append("Python 3.10+")
        if (scan.root / "pyproject.toml").exists():
            install.append(RuntimeCommand("安装 Python 包", "pip install -e .", "medium", ["pyproject.toml"]))
        if (scan.root / "requirements.txt").exists():
            install.append(RuntimeCommand("安装 Python 依赖", "pip install -r requirements.txt", "high", ["requirements.txt"]))
        if any(path.endswith("cli.py") for path in scan.entry_candidates):
            recommended.append(RuntimeCommand("运行 CLI 入口", "python -m <package>", "low", scan.entry_candidates))
        if _contains_file(scan, "pytest.ini") or "pytest" in tech_stack.tools:
            tests.append(RuntimeCommand("运行 Python 测试", "pytest", "medium", ["pytest.ini"] if _contains_file(scan, "pytest.ini") else []))

    if (scan.root / "go.mod").exists():
        environment.append("Go")
        install.append(RuntimeCommand("下载 Go 依赖", "go mod download", "high", ["go.mod"]))
        recommended.append(RuntimeCommand("运行 Go 项目", "go run .", "medium", ["go.mod"]))
        tests.append(RuntimeCommand("运行 Go 测试", "go test ./...", "medium", ["go.mod"]))

    if (scan.root / "Cargo.toml").exists():
        environment.append("Rust toolchain")
        recommended.append(RuntimeCommand("运行 Rust 项目", "cargo run", "high", ["Cargo.toml"]))
        tests.append(RuntimeCommand("运行 Rust 测试", "cargo test", "high", ["Cargo.toml"]))

    if (scan.root / "Dockerfile").exists():
        alternatives.append(RuntimeCommand("构建 Docker 镜像", "docker build -t <image-name> .", "medium", ["Dockerfile"]))
        alternatives.append(RuntimeCommand("运行 Docker 容器", "docker run --rm -p <host-port>:<container-port> <image-name>", "low", ["Dockerfile"]))
        environment.append("Docker")

    compose = [path for path in scan.file_paths if path.startswith("docker-compose.")]
    if compose:
        alternatives.append(RuntimeCommand("使用 Docker Compose 启动", "docker compose up --build", "medium", compose))
        environment.append("Docker Compose")

    readme_commands = _extract_readme_commands(scan.root, scan.readmes)
    for command in readme_commands[:5]:
        alternatives.append(RuntimeCommand("README 中发现的命令", command, "medium", scan.readmes[:1]))

    if not recommended:
        unknowns.extend(
            [
                "未能确定唯一推荐启动命令",
                "需要用户确认项目入口、端口、环境变量和外部服务依赖",
            ]
        )

    return RuntimeReport(
        recommended=_dedupe_commands(recommended),
        alternatives=_dedupe_commands(alternatives),
        install=_dedupe_commands(install),
        tests=_dedupe_commands(tests),
        lint=_dedupe_commands(lint),
        environment=sorted(set(environment)),
        unknowns=unknowns,
    )


def _from_package_json(
    package_json: Path,
    install: list[RuntimeCommand],
    recommended: list[RuntimeCommand],
    tests: list[RuntimeCommand],
    lint: list[RuntimeCommand],
    environment: list[str],
) -> None:
    try:
        data = json.loads(package_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    scripts = data.get("scripts", {})
    environment.append("Node.js")
    install.append(RuntimeCommand("安装 Node 依赖", _node_install_command(package_json.parent), "high", ["package.json"]))
    for script in ("dev", "start", "serve"):
        if script in scripts:
            recommended.append(RuntimeCommand(f"运行 npm {script}", f"npm run {script}", "high", ["package.json"]))
            break
    for script in ("test", "unit"):
        if script in scripts:
            tests.append(RuntimeCommand(f"运行 npm {script}", f"npm run {script}", "high", ["package.json"]))
            break
    for script in ("lint", "format:check"):
        if script in scripts:
            lint.append(RuntimeCommand(f"运行 npm {script}", f"npm run {script}", "high", ["package.json"]))
            break


def _node_install_command(root: Path) -> str:
    if (root / "pnpm-lock.yaml").exists():
        return "pnpm install"
    if (root / "yarn.lock").exists():
        return "yarn install"
    if (root / "package-lock.json").exists():
        return "npm ci"
    return "npm install"


def _contains_file(scan: ProjectScan, filename: str) -> bool:
    return filename in scan.file_paths


def _extract_readme_commands(root: Path, readmes: list[str]) -> list[str]:
    commands: list[str] = []
    for readme in readmes:
        path = root / readme
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for match in re.finditer(r"```(?:bash|sh|shell|powershell|ps1)?\n(.*?)```", text, re.DOTALL | re.IGNORECASE):
            block = match.group(1)
            for line in block.splitlines():
                line = line.strip()
                if line and not line.startswith("#") and _looks_like_command(line):
                    commands.append(line)
    return commands


def _looks_like_command(line: str) -> bool:
    prefixes = ("npm ", "pnpm ", "yarn ", "python ", "pip ", "go ", "cargo ", "docker ", "pytest", "uvicorn ")
    return line.startswith(prefixes)


def _dedupe_commands(commands: list[RuntimeCommand]) -> list[RuntimeCommand]:
    seen: set[str] = set()
    result: list[RuntimeCommand] = []
    for command in commands:
        if command.command in seen:
            continue
        seen.add(command.command)
        result.append(command)
    return result

