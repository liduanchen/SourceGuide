[🇨🇳 中文](CHANGELOG.md) | [🇬🇧 English](CHANGELOG_EN.md)

---

# 更新日志

SourceGuide 的所有重要变更都会记录在这个文件中。

本项目遵循语义化版本：

```text
MAJOR.MINOR.PATCH
```

- `MAJOR`：包含破坏性变更。
- `MINOR`：新增向后兼容的功能。
- `PATCH`：修复问题、优化文档或做小幅改进。

## 0.1.0 - Unreleased

SourceGuide 的第一个 MVP 版本，目标是提供一个可发布到 GitHub 的 Python CLI 工具。

### Added

- 新增 `sourceguide generate <repo-or-path>` CLI 命令。
- 支持扫描本地项目目录。
- 支持输入公开 GitHub 仓库 URL。
- 支持通过环境变量配置 OpenAI 兼容 API。
- 支持 CLI 参数覆盖环境变量配置。
- 支持生成全部路线或单条路线：
  - 我是小白路线
  - 快速了解路线
  - 贡献者路线
  - 项目面试路线
- 新增文件扫描模块，默认忽略 `.git`、`node_modules`、`.venv`、`dist`、`build`、`coverage`、`__pycache__`、大二进制文件和 minified 文件。
- 新增技术栈识别模块，覆盖 Python、Node.js、Go、Rust、Java、Docker 及常见前后端框架线索。
- 新增运行方式推断模块，用于识别安装、启动、测试、lint 和 Docker 相关命令。
- 新增核心文件识别模块，生成核心文件 Top 10 和推荐阅读线索。
- 新增 OpenAI 兼容 AI Provider。
- 新增规则生成器 `--offline`，可在没有 API Key 时生成演示文档。
- 新增 Markdown 写入器和输出校验器。
- 新增 GitHub Codespaces 在线体验配置。
- 新增 GitHub Actions CI。
- 新增 Issue 模板、PR 模板、贡献指南和示例说明。

### Documentation

- 新增中文 README。
- 新增英文 README。
- 新增中文贡献指南。
- 新增英文贡献指南。
- 新增中英文更新日志。
- 新增 `.env.example`，说明环境变量配置方式。

### Tests

- 新增配置读取测试。
- 新增 GitHub URL 和本地路径识别测试。
- 新增文件扫描忽略规则测试。
- 新增技术栈识别测试。
- 新增运行方式推断测试。
- 新增核心文件排序测试。
- 新增 Markdown 校验器测试。
- 新增 mock AI client 集成测试。
- 新增 CLI `--offline` 测试。

### Notes

- 当前版本仍是 MVP。
- 暂不支持私有仓库授权、Web UI、VS Code 插件、PDF 导出和文档站部署。
- 后续版本计划加入 `sourceguide.toml`、自定义扫描规则、自定义模板、增量更新和 GitHub Action 自动生成。

