[🇨🇳 中文](CONTRIBUTING.md) | [🇬🇧 English](CONTRIBUTING_EN.md)

---

# 贡献指南

感谢你愿意帮助 SourceGuide 变得更好。SourceGuide 的目标是把任意 GitHub 仓库或本地项目转换成清晰、可信、适合中文开发者阅读的源码学习路线。

欢迎提交 Issue、Pull Request、真实仓库生成示例、文档改进和新的技术栈识别规则。

## 开发环境

推荐使用 Python 3.10 或更高版本。

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest
```

macOS / Linux:

```bash
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## 常用命令

运行测试：

```bash
pytest
```

查看 CLI 帮助：

```bash
sourceguide --help
sourceguide generate --help
```

不配置 API Key，离线生成演示文档：

```bash
sourceguide generate . --route quick --offline --output demo/sourceguide --overwrite
```

## 适合贡献的方向

- 新增技术栈识别规则，例如 PHP、C#、Ruby、移动端项目、Monorepo。
- 改进运行方式推断，例如更准确识别安装、启动、测试、lint 和 Docker 命令。
- 改进中文文档生成质量，让输出更自然、更少模板味。
- 增加真实仓库生成示例，帮助用户理解 SourceGuide 的效果。
- 增加测试 fixture，覆盖更多项目结构和边界情况。
- 改进 README、示例、错误提示和贡献流程。

## Pull Request Checklist

提交 PR 前请确认：

- 已为行为变化新增或更新测试。
- 已运行 `pytest` 并通过。
- 没有提交 API Key、`.env`、临时 clone 目录、缓存文件或生成产物。
- CLI 参数、环境变量名、输出文件名尽量保持兼容。
- 如果修改了对外行为，已更新 `CHANGELOG.md`。
- 如果生成文档引用了文件，引用的文件必须来自真实扫描结果。
- 不确定的信息应标注“不确定”，不要让文档假装知道。

## Issue 类型

- **Bug**：扫描错误、生成错误、CLI 行为异常、校验器误判。
- **Feature**：新的技术栈识别、输出格式、AI Provider、工作流。
- **Docs**：README、示例、生成文档清晰度、贡献说明。
- **Question**：使用方式、配置、路线图或设计讨论。

## 设计原则

- SourceGuide 不是 README 总结器，而是源码学习路线生成器。
- 所有路线都必须包含“如何运行这个项目”。
- 所有引用文件必须来自真实扫描结果。
- 不确定的内容必须明确标注“不确定”。
- Markdown 输出应该能直接放进 GitHub 仓库。
- 对外接口要谨慎变更，包括 CLI 参数、环境变量和输出文件名。

## 发布与维护

SourceGuide 使用语义化版本：

```text
MAJOR.MINOR.PATCH
```

公开行为发生变化时，请更新 `CHANGELOG.md`。如果是破坏性变更，需要在 PR 中说明原因、影响范围和迁移方式。

