from __future__ import annotations

from .models import AnalysisContext, RuntimeCommand

ROUTE_FILES = {
    "beginner": "01-我是小白路线.md",
    "quick": "02-快速了解路线.md",
    "contributor": "03-贡献者路线.md",
    "interview": "04-项目面试路线.md",
}


def render_rule_based_bundle(context: AnalysisContext, routes: list[str]) -> dict[str, str]:
    bundle = {
        "README.md": _render_index(context, routes),
        "run-guide.md": _render_run_guide(context),
        "source-map.md": _render_source_map(context),
        "exercises.md": _render_exercises(context),
    }
    if context.options.include_architecture:
        bundle["architecture.md"] = _render_architecture(context)
    if context.options.include_glossary:
        bundle["glossary.md"] = _render_glossary(context)
    for route in routes:
        bundle[ROUTE_FILES[route]] = _render_route(context, route)
    return bundle


def _render_index(context: AnalysisContext, routes: list[str]) -> str:
    stack = _join_or_unknown(context.tech_stack.languages + context.tech_stack.frameworks)
    return f"""# {context.repository.name} SourceGuide

这组文档由 SourceGuide 根据真实文件扫描结果生成，用来帮助不同目的的读者学习 `{context.repository.name}`。

## 项目是什么

不确定：需要结合项目 README 和核心源码进一步确认业务目标。已识别技术线索：{stack}。

## 推荐阅读

- 先读 `run-guide.md`，确认项目如何运行。
- 再读 `source-map.md`，了解核心文件和入口候选。
- 根据目标选择路线：{", ".join(ROUTE_FILES[route] for route in routes)}。

## 已生成路线

{_bullet_lines(ROUTE_FILES[route] for route in routes)}
"""


def _render_run_guide(context: AnalysisContext) -> str:
    return f"""# 运行说明

## 环境要求

{_bullet_lines(context.runtime.environment or ["不确定：未从依赖文件中识别出明确运行环境。"])}

## 安装依赖

{_command_lines(context.runtime.install)}

## 如何运行这个项目

{_command_lines(context.runtime.recommended)}

## 备用运行方式

{_command_lines(context.runtime.alternatives)}

## 如何运行测试

{_command_lines(context.runtime.tests)}

## 如何检查代码风格

{_command_lines(context.runtime.lint)}

## 不确定项和排查建议

{_bullet_lines(context.runtime.unknowns or ["当前扫描结果没有发现明显不确定项，但仍建议核对 README、环境变量和外部服务依赖。"])}
"""


def _render_source_map(context: AnalysisContext) -> str:
    core = "\n".join(f"- `{item.path}`：{item.reason}，评分 {item.score}" for item in context.core_files.files)
    return f"""# 核心文件地图

## README

{_bullet_lines(context.scan.readmes or ["未发现 README。"])}

## 依赖和配置文件

{_bullet_lines(context.scan.dependency_files + context.scan.config_files or ["未发现明确依赖或配置文件。"])}

## 入口候选

{_bullet_lines(context.scan.entry_candidates or ["不确定：未发现常见入口文件名。"])}

## 核心文件 Top 10

{core or "- 不确定：扫描结果不足以排序核心文件。"}
"""


def _render_architecture(context: AnalysisContext) -> str:
    return f"""# 架构说明

## 技术栈概览

- 语言：{_join_or_unknown(context.tech_stack.languages)}
- 框架：{_join_or_unknown(context.tech_stack.frameworks)}
- 工具：{_join_or_unknown(context.tech_stack.tools)}
- 包管理：{_join_or_unknown(context.tech_stack.package_managers)}

## 模块关系

不确定：MVP 只基于文件名、配置和 README 线索生成架构初稿。建议从 `source-map.md` 中的入口候选和核心文件开始验证真实调用关系。
"""


def _render_glossary(context: AnalysisContext) -> str:
    terms = sorted(set(context.tech_stack.languages + context.tech_stack.frameworks + context.tech_stack.tools))
    if not terms:
        terms = ["运行方式", "入口文件", "依赖文件"]
    return "# 术语表\n\n" + "\n".join(f"- **{term}**：与当前项目扫描结果相关的技术或概念，需要结合源码上下文理解。" for term in terms) + "\n"


def _render_exercises(context: AnalysisContext) -> str:
    first_file = context.core_files.files[0].path if context.core_files.files else "README.md"
    return f"""# 练习任务

- 跑通项目：按 `run-guide.md` 执行安装和启动步骤，记录遇到的错误。
- 读入口文件：从 `{first_file}` 开始，画出启动后的主要流程。
- 做一个小改动：选择一个文案、配置或测试相关的小任务，完成修改并运行测试。
"""


def _render_route(context: AnalysisContext, route: str) -> str:
    title = {
        "beginner": "我是小白路线",
        "quick": "快速了解路线",
        "contributor": "贡献者路线",
        "interview": "项目面试路线",
    }[route]
    extra = {
        "beginner": _beginner_extra(context),
        "quick": _quick_extra(context),
        "contributor": _contributor_extra(context),
        "interview": _interview_extra(context),
    }[route]
    return f"""# {title}

## 目标

这条路线帮助你用 `{context.repository.name}` 的真实文件线索学习项目。

## 这个项目是什么

不确定：需要结合 README 和核心源码进一步确认。当前扫描到的技术栈是 {_join_or_unknown(context.tech_stack.languages + context.tech_stack.frameworks)}。

## 如何运行这个项目

请先阅读 `run-guide.md`。下面是当前最重要的运行线索：

{_command_lines(context.runtime.recommended or context.runtime.alternatives)}

## 入口在哪里

{_bullet_lines(context.scan.entry_candidates or ["不确定：未发现常见入口文件名，请从 README 和依赖配置继续确认。"])}

## 我应该先看哪些文件

{_bullet_lines(f"`{item.path}`：{item.reason}" for item in context.core_files.files[:5])}

## 遇到问题怎么排查

{_bullet_lines(context.runtime.unknowns or ["先确认依赖是否安装、环境变量是否齐全、启动命令是否来自项目 README。"])}

{extra}
"""


def _beginner_extra(context: AnalysisContext) -> str:
    return """## 小白练习

- 逐条解释 `run-guide.md` 中的命令，确认每一步做了什么。
- 找到一个入口候选文件，给每个主要函数写一句中文说明。
- 记录 3 个不懂的术语，到 `glossary.md` 中补充自己的理解。
"""


def _quick_extra(context: AnalysisContext) -> str:
    return """## 10 分钟判断

- 值得继续读：如果运行方式明确、入口文件清楚、核心文件和测试目录能对应上。
- 潜在风险：如果启动命令不确定、核心模块缺少测试、README 没有维护说明。
"""


def _contributor_extra(context: AnalysisContext) -> str:
    return """## 第一次贡献建议

- 先跑通测试，再做小改动。
- 优先选择文档、示例、测试或错误提示类任务。
- 提交 PR 前确认没有引用不存在的文件，且运行命令仍然有效。
"""


def _interview_extra(context: AnalysisContext) -> str:
    return """## 面试表达

- 一句话讲法：我用 SourceGuide 把项目从运行方式、入口文件、核心模块和可贡献点四个角度拆解。
- 可优化方向：补充更明确的运行文档、增加测试覆盖、梳理入口到核心模块的调用链。
"""


def _command_lines(commands: list[RuntimeCommand]) -> str:
    if not commands:
        return "- 不确定：未发现明确命令，请检查 README、依赖文件和环境变量要求。"
    return "\n".join(f"- {command.title}：`{command.command}`（置信度：{command.confidence}，证据：{_join_or_unknown(command.evidence)}）" for command in commands)


def _bullet_lines(items) -> str:
    values = list(items)
    if not values:
        return "- 不确定"
    return "\n".join(f"- {item}" for item in values)


def _join_or_unknown(items: list[str]) -> str:
    return "、".join(items) if items else "不确定"

