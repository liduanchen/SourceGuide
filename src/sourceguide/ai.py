from __future__ import annotations

import json
from dataclasses import asdict
from typing import Protocol

import httpx

from .models import AnalysisContext


class AIError(RuntimeError):
    pass


class AIClient(Protocol):
    def generate_markdown_bundle(self, context: AnalysisContext, routes: list[str]) -> dict[str, str]:
        ...


class OpenAICompatibleClient:
    def __init__(self, api_key: str, base_url: str, model: str, timeout: float = 60.0) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def generate_markdown_bundle(self, context: AnalysisContext, routes: list[str]) -> dict[str, str]:
        if not self.api_key:
            raise AIError("OPENAI_API_KEY is required for real AI generation.")
        prompt = build_generation_prompt(context, routes)
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "你是 SourceGuide 的源码学习路线生成器。"
                        "必须用自然中文写作，只能引用扫描结果中真实存在的文件。"
                        "无法确定的内容必须标注“不确定”。"
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
        }
        try:
            response = httpx.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise AIError(f"AI request failed: {exc}") from exc

        data = response.json()
        content = data["choices"][0]["message"]["content"]
        return parse_markdown_bundle(content)


class RuleBasedAIClient:
    """Deterministic fallback used for tests and offline demos."""

    def generate_markdown_bundle(self, context: AnalysisContext, routes: list[str]) -> dict[str, str]:
        from .renderer import render_rule_based_bundle

        return render_rule_based_bundle(context, routes)


def build_generation_prompt(context: AnalysisContext, routes: list[str]) -> str:
    summary = {
        "repo": context.repository.name,
        "routes": routes,
        "language": context.options.language,
        "depth": context.options.depth,
        "scan": {
            "readmes": context.scan.readmes,
            "dependency_files": context.scan.dependency_files,
            "config_files": context.scan.config_files,
            "entry_candidates": context.scan.entry_candidates,
            "test_dirs": context.scan.test_dirs,
            "example_dirs": context.scan.example_dirs,
            "language_counts": context.scan.language_counts,
            "all_files": [file.path for file in context.scan.files[:300]],
        },
        "tech_stack": asdict(context.tech_stack),
        "runtime": asdict(context.runtime),
        "core_files": asdict(context.core_files),
    }
    return (
        "请基于以下真实扫描结果生成 SourceGuide Markdown 文档包。\n"
        "输出必须是 JSON 对象，key 为文件名，value 为完整 Markdown 内容。\n"
        "需要的文件名包括 README.md、run-guide.md、source-map.md、exercises.md，"
        "以及所选路线文件。若 routes 包含 beginner/quick/contributor/interview，分别生成："
        "01-我是小白路线.md、02-快速了解路线.md、03-贡献者路线.md、04-项目面试路线.md。"
        "如果启用架构和术语表，也生成 architecture.md 和 glossary.md。\n"
        "每条路线必须有“如何运行这个项目”章节。不要输出 JSON 之外的文字。\n\n"
        + json.dumps(summary, ensure_ascii=False, indent=2)
    )


def parse_markdown_bundle(content: str) -> dict[str, str]:
    text = content.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:].strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise AIError("AI response was not valid JSON.") from exc
    if not isinstance(data, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in data.items()):
        raise AIError("AI response JSON must be an object of filename to markdown content.")
    return data

