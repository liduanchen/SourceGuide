from __future__ import annotations

from pathlib import Path

from .models import CoreFile, CoreFileReport, ProjectScan


IMPORTANT_NAME_PARTS = (
    "route",
    "router",
    "controller",
    "service",
    "model",
    "schema",
    "config",
    "settings",
    "store",
    "api",
    "command",
    "cli",
)


def identify_core_files(scan: ProjectScan, limit: int = 10) -> CoreFileReport:
    scores: dict[str, tuple[int, list[str]]] = {}

    for file in scan.files:
        score = 0
        reasons: list[str] = []
        path = file.path
        lower = path.lower()
        name = Path(path).name

        if path in scan.entry_candidates:
            score += 40
            reasons.append("入口候选文件")
        if file.role == "dependency":
            score += 25
            reasons.append("依赖或构建配置")
        if file.role == "config":
            score += 18
            reasons.append("配置中心")
        if file.role == "readme":
            score += 16
            reasons.append("项目说明入口")
        if any(part in lower for part in IMPORTANT_NAME_PARTS):
            score += 14
            reasons.append("文件名显示核心职责")
        if "/tests/" in f"/{lower}" or lower.startswith("tests/"):
            score += 6
            reasons.append("测试覆盖线索")
        if name in {"main.py", "app.py", "server.js", "index.js", "main.go", "main.rs"}:
            score += 20
            reasons.append("常见启动文件")
        if file.suffix in {".py", ".js", ".ts", ".tsx", ".go", ".rs", ".java"}:
            score += 5
        if file.size > 0:
            score += min(file.size // 4000, 8)

        if score > 0:
            scores[path] = (score, reasons)

    ranked = sorted(scores.items(), key=lambda item: (-item[1][0], item[0]))[:limit]
    return CoreFileReport(
        files=[
            CoreFile(path=path, score=score, reason="、".join(_dedupe(reasons)))
            for path, (score, reasons) in ranked
        ]
    )


def _dedupe(values: list[str]) -> list[str]:
    result = []
    for value in values:
        if value not in result:
            result.append(value)
    return result

