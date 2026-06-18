[🇨🇳 中文](CHANGELOG.md) | [🇬🇧 English](CHANGELOG_EN.md)

---

# 📦 更新日志

SourceGuide 的所有重要变更都会记录在此文件中。

本项目遵循[语义化版本](https://semver.org/)：`MAJOR.MINOR.PATCH`

---

## 🔖 0.1.0 — Unreleased

SourceGuide 的第一个 MVP 版本，目标是提供一个可发布到 GitHub 的 Python CLI 工具。

### ✨ Added

**CLI 与核心流程**
- 新增 `sourceguide generate <repo-or-path>` 命令
- 支持扫描**本地项目目录**
- 支持输入**公开 GitHub 仓库 URL**
- 支持通过**环境变量**配置 OpenAI 兼容 API
- 支持 **CLI 参数**覆盖环境变量配置
- 新增规则生成器 `--offline`，可在没有 API Key 时生成演示文档

**4 条学习路线**
- 🟢 **我是小白路线** — 从零跑起来
- 🔵 **快速了解路线** — 10 分钟判断价值
- 🟣 **贡献者路线** — 参与开发入口
- 🟠 **项目面试路线** — 简历/面试/分享

**扫描与识别**
- 新增**文件扫描模块**，默认忽略 `.git`、`node_modules`、`.venv`、`dist`、`build`、`__pycache__` 等
- 新增**技术栈识别模块**，覆盖 Python、Node.js、Go、Rust、Java、Docker 及常见前后端框架
- 新增**运行方式推断模块**，识别安装/启动/测试/lint/Docker 命令
- 新增**核心文件识别模块**，生成 Top 10 核心文件和推荐阅读线索

**输出与质量**
- 新增 OpenAI 兼容 **AI Provider**
- 新增 **Markdown 写入器**和**输出校验器**
- 新增 **GitHub Actions CI**
- 新增 **GitHub Codespaces** 在线体验配置

### 📖 Documentation

| 文档 | 说明 |
| --- | --- |
| `README.md` / `README_EN.md` | 中英文项目介绍 |
| `CONTRIBUTING.md` / `CONTRIBUTING_EN.md` | 中英文贡献指南 |
| `CHANGELOG.md` / `CHANGELOG_EN.md` | 中英文更新日志 |
| `.env.example` | 环境变量配置说明 |
| Issue / PR 模板 | 双语模板 |
| `examples/README.md` | 示例说明 |

### 🧪 Tests

| 测试模块 | 覆盖内容 |
| --- | --- |
| `test_config.py` | 环境变量读取 |
| `test_repository.py` | GitHub URL 和本地路径识别 |
| `test_scanner_stack_runtime.py` | 文件扫描、技术栈识别、运行方式推断 |
| `test_core_files_validator.py` | 核心文件排序、Markdown 校验 |
| `test_pipeline_integration.py` | Mock AI 集成测试 |
| `test_cli.py` | CLI `--offline` 命令测试 |

### 📝 Notes

- 当前版本仍是 **MVP**
- 暂不支持：私有仓库授权、Web UI、VS Code 插件、PDF 导出、文档站部署
- 后续计划：`sourceguide.toml`、自定义扫描规则、自定义模板、增量更新、GitHub Action

---

## 🔮 未来版本

| 版本 | 计划内容 |
| :--- | :--- |
| 🔜 **v0.2** | `sourceguide.toml` 配置 + 自定义扫描规则 + 自定义模板 |
| 🔜 **v0.3** | 增量更新，只重写变化部分，保留用户手写补充 |
| 🔜 **v0.4** | GitHub Action，仓库更新后自动生成文档 |
| 🔜 **v0.5** | 多语言输出 + 私有仓库授权 + HTML 文档站 |
| 🔮 **v1.0** | 稳定 CLI/API + 插件化分析器 + 完善示例和发布文档 |
