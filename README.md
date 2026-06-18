# SourceGuide

把任意 GitHub 仓库变成源码学习路线。

SourceGuide 是一个面向中文开发者的开源 CLI 工具。你给它一个公开 GitHub 仓库地址或本地项目目录，它会自动扫描项目结构、识别技术栈、推断运行方式、找出核心文件，并生成一组适合阅读和发布的 Markdown 文档。

它不是普通的 README 总结器。SourceGuide 的重点是：同一个仓库，不同目的的人应该有不同读法。

## What It Generates

SourceGuide 会生成 4 条源码学习路线：

- **我是小白路线**：从零跑起来，解释命令、依赖、入口文件和常见报错。
- **快速了解路线**：用 10 分钟判断项目是否值得继续深入。
- **贡献者路线**：帮助你进入开发模式、跑测试、找 first PR 切入点。
- **项目面试路线**：把项目讲清楚，用于简历、面试或技术分享。

默认输出到目标项目的 `docs/sourceguide/`：

```text
docs/sourceguide/
├── README.md
├── 01-我是小白路线.md
├── 02-快速了解路线.md
├── 03-贡献者路线.md
├── 04-项目面试路线.md
├── run-guide.md
├── source-map.md
├── architecture.md
├── glossary.md
└── exercises.md
```

每条路线都必须包含“如何运行这个项目”。如果运行方式无法确定，SourceGuide 会明确写出已发现线索、可能的启动方式、需要确认的配置和排查建议。

## Features

- 支持公开 GitHub 仓库 URL
- 支持本地项目目录
- 默认中文输出
- 可生成全部路线，也可只生成单条路线
- 自动识别 Python、Node.js、Go、Rust、Java、Docker 等常见技术栈
- 自动推断安装、启动、测试和 lint 命令
- 自动生成核心文件 Top 10 和推荐阅读顺序
- 支持 OpenAI 兼容 API
- 使用环境变量配置，适合本地和 CI
- Markdown-first，方便放进 GitHub、掘金、知乎或文档站

## Project Status

当前版本是 `v0.1.0` MVP。

已包含 CLI、扫描流水线、技术栈识别、运行方式推断、AI Provider、Markdown 写入器、校验器、测试和 GitHub CI。

暂不支持：

- Web UI
- VS Code 插件
- 私有仓库授权
- PDF 导出
- 文档站部署
- GitHub Action 自动生成

这些能力已放入后续路线图。

## Installation

从源码安装：

```bash
git clone https://github.com/YOUR_NAME/sourceguide.git
cd sourceguide
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -e .
```

macOS / Linux:

```bash
source .venv/bin/activate
pip install -e .
```

验证 CLI：

```bash
sourceguide --help
```

## Configuration

SourceGuide 使用环境变量配置模型和 API。

必填：

```bash
OPENAI_API_KEY=sk-your-api-key
```

可选：

| Variable | Default | Description |
| --- | --- | --- |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | OpenAI 兼容 API 地址 |
| `SOURCEGUIDE_MODEL` | `gpt-4.1-mini` | 默认模型 |
| `SOURCEGUIDE_LANGUAGE` | `zh-CN` | 输出语言 |
| `SOURCEGUIDE_OUTPUT_DIR` | `docs/sourceguide` | 默认输出目录 |
| `SOURCEGUIDE_DEPTH` | `normal` | 教程深度：`basic`、`normal`、`deep` |
| `SOURCEGUIDE_TIMEOUT` | `60` | API 超时时间，单位秒 |
| `SOURCEGUIDE_DEBUG` | `false` | 是否输出调试信息 |

Windows PowerShell 示例：

```powershell
$env:OPENAI_API_KEY = "sk-your-api-key"
$env:SOURCEGUIDE_MODEL = "gpt-4.1-mini"
```

macOS / Linux 示例：

```bash
export OPENAI_API_KEY="sk-your-api-key"
export SOURCEGUIDE_MODEL="gpt-4.1-mini"
```

你也可以参考 `.env.example`。请不要把真实 API Key 提交到 GitHub。

## Usage

为当前项目生成全部路线：

```bash
sourceguide generate .
```

只生成快速了解路线：

```bash
sourceguide generate . --route quick --overwrite
```

分析公开 GitHub 仓库：

```bash
sourceguide generate https://github.com/pallets/flask --route all
```

指定输出目录：

```bash
sourceguide generate . --output docs/sourceguide --overwrite
```

临时覆盖模型和 API 地址：

```bash
sourceguide generate . --model gpt-4.1 --base-url https://api.example.com/v1
```

## CLI Options

```text
sourceguide generate <repo-or-path>

Options:
  --route all|beginner|quick|contributor|interview
  --output docs/sourceguide
  --model gpt-4.1-mini
  --base-url https://api.openai.com/v1
  --language zh-CN
  --depth basic|normal|deep
  --overwrite
  --architecture / --no-architecture
  --glossary / --no-glossary
```

CLI 参数优先级高于环境变量。

## How It Works

SourceGuide 的主流程：

1. 接收本地路径或公开 GitHub URL
2. 准备源码目录
3. 扫描文件树并过滤无关文件
4. 识别 README、依赖文件、配置文件、入口文件、测试目录
5. 识别技术栈
6. 推断安装、启动、测试和 lint 命令
7. 识别核心文件 Top 10
8. 分阶段调用 OpenAI 兼容 API 生成文档
9. 校验文档是否包含运行说明、是否引用真实文件
10. 写入 Markdown 输出目录

## Development

安装开发依赖：

```bash
pip install -e ".[dev]"
```

运行测试：

```bash
pytest
```

当前测试覆盖：

- 环境变量读取
- GitHub URL 和本地路径识别
- 文件扫描忽略规则
- 技术栈识别
- 运行方式推断
- 核心文件排序
- Markdown 校验器
- 使用 mock AI client 的集成生成流程

## Repository Structure

```text
src/sourceguide/
├── cli.py          # CLI 入口
├── config.py       # 环境变量配置
├── repository.py   # 本地目录和 GitHub 仓库准备
├── scanner.py      # 文件扫描
├── stack.py        # 技术栈识别
├── runtime.py      # 运行方式推断
├── core_files.py   # 核心文件识别
├── ai.py           # OpenAI 兼容 Provider
├── renderer.py     # 规则生成器和模板化输出
├── writer.py       # Markdown 写入
├── validators.py   # 输出校验
└── pipeline.py     # 主流程编排
```

## Roadmap

- `v0.1`：MVP CLI，支持公开 GitHub 仓库、本地目录、中文 Markdown 输出
- `v0.2`：支持 `sourceguide.toml`、自定义扫描规则、自定义模板
- `v0.3`：增量更新，只重写变化相关文档，保留用户手写补充
- `v0.4`：GitHub Action，仓库更新后自动生成文档
- `v0.5`：多语言输出、私有仓库支持、HTML 文档站
- `v1.0`：稳定 CLI/API、插件化分析器、完善示例和发布文档

## Contributing

欢迎提交 Issue 和 Pull Request。建议优先贡献：

- 新技术栈识别规则
- 更准确的运行方式推断
- 更自然的中文文档模板
- 真实仓库生成示例
- 测试用 fixture 项目

提交 PR 前请运行：

```bash
pytest
```

更多说明见 `CONTRIBUTING.md`。

## License

MIT License.

