[🇨🇳 中文](CHANGELOG.md) | [🇬🇧 English](CHANGELOG_EN.md)

---

# 📦 Changelog

All notable changes to SourceGuide will be documented in this file.

This project follows [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`

---

## 🔖 0.1.0 — Unreleased

The first MVP release of SourceGuide — a Python CLI tool ready for GitHub.

### ✨ Added

**CLI & Core Pipeline**
- `sourceguide generate <repo-or-path>` command
- Scan **local project directories**
- Analyze **public GitHub repository URLs**
- Environment-variable based **OpenAI-compatible API** configuration
- **CLI flags** override environment variables
- `--offline` rule-based generator for demo without API keys

**4 Learning Paths**
- 🟢 **Beginner Path** — Run from scratch
- 🔵 **Quick Overview Path** — 10-minute assessment
- 🟣 **Contributor Path** — Dev onboarding
- 🟠 **Interview Path** — Resume & sharing

**Scanning & Detection**
- **File scanner** — ignores `.git`, `node_modules`, `.venv`, `dist`, `build`, `__pycache__`, etc.
- **Tech-stack detection** — Python, Node.js, Go, Rust, Java, Docker, and common frontend/backend frameworks
- **Run-method inference** — detect install/start/test/lint/Docker commands
- **Core file identification** — Top 10 core files with reading suggestions

**Output & Quality**
- OpenAI-compatible **AI Provider**
- **Markdown writer** + **output validator**
- **GitHub Actions CI**
- **GitHub Codespaces** support for online trial

### 📖 Documentation

| Document | Description |
| --- | --- |
| `README.md` / `README_EN.md` | Bilingual project introduction |
| `CONTRIBUTING.md` / `CONTRIBUTING_EN.md` | Bilingual contribution guide |
| `CHANGELOG.md` / `CHANGELOG_EN.md` | Bilingual changelog |
| `.env.example` | Environment config reference |
| Issue / PR templates | Bilingual templates |
| `examples/README.md` | Example usage guide |

### 🧪 Tests

| Module | Coverage |
| --- | --- |
| `test_config.py` | Environment variable parsing |
| `test_repository.py` | GitHub URL and local path recognition |
| `test_scanner_stack_runtime.py` | File scanning, tech-stack detection, run-method inference |
| `test_core_files_validator.py` | Core file ranking, Markdown validation |
| `test_pipeline_integration.py` | Mock AI integration test |
| `test_cli.py` | CLI `--offline` command test |

### 📝 Notes

- This is an **MVP** release
- Not yet supported: private repos, Web UI, VS Code extension, PDF export, doc-site deployment
- Planned: `sourceguide.toml`, custom scan rules, custom templates, incremental updates, GitHub Action

---

## 🔮 Upcoming

| Version | Content |
| :--- | :--- |
| 🔜 **v0.2** | `sourceguide.toml` config + custom scan rules + custom templates |
| 🔜 **v0.3** | Incremental updates — preserve manual edits |
| 🔜 **v0.4** | GitHub Action — auto-generate on push |
| 🔜 **v0.5** | Multi-language + private repo support + HTML doc site |
| 🔮 **v1.0** | Stable CLI/API + plugin analyzers + polished examples |
