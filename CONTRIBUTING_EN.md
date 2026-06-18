[🇨🇳 中文](CONTRIBUTING.md) | [🇬🇧 English](CONTRIBUTING_EN.md)

---

# 🤝 Contributing to SourceGuide

Thanks for helping SourceGuide become a better open-source learning tool!

> **Mission:** Turn any GitHub repository or local project into clear, reliable, Chinese-friendly source-code learning paths.

We welcome Issues, Pull Requests, real-world examples, documentation improvements, and new tech-stack detection rules.

---

## 📋 Table of Contents

- [🐣 Where to Contribute](#-where-to-contribute)
- [🛠️ Development Setup](#️-development-setup)
- [📝 Pull Request Checklist](#-pull-request-checklist)
- [🎯 Issue Types](#-issue-types)
- [🧭 Design Principles](#-design-principles)
- [📦 Release & Maintenance](#-release--maintenance)

---

## 🐣 Where to Contribute

| Area | Description |
| --- | --- |
| 🧩 **New tech-stack detection** | PHP, C#, Ruby, mobile frameworks, Monorepo |
| 🎯 **Better run-method inference** | More accurate install/start/test/lint/Docker detection |
| 📝 **Better document generation** | More natural Chinese output, less templated |
| 📸 **Real-world examples** | Show what SourceGuide can do with real repos |
| 🧪 **Test fixtures** | Cover more project structures and edge cases |
| 📖 **Documentation** | README, examples, error messages, contribution flow |

---

## 🛠️ Development Setup

Requires Python 3.10+.

```bash
# Clone & enter
git clone https://github.com/liduanchen/SourceGuide.git
cd SourceGuide

# Create virtual environment
python -m venv .venv
```

**Windows PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

**macOS / Linux:**
```bash
source .venv/bin/activate
pip install -e ".[dev]"
```

**Common commands:**

```bash
# Run tests
pytest

# Generate demo docs offline (no API key needed)
sourceguide generate . --route quick --offline --output demo/sourceguide --overwrite

# View CLI help
sourceguide --help
sourceguide generate --help
```

---

## 📝 Pull Request Checklist

Before submitting, verify each item:

```markdown
- [ ] Added or **updated tests** for behavior changes
- [ ] `pytest` **passes** with no errors
- [ ] No API keys, `.env`, temp clones, caches, or build artifacts committed
- [ ] CLI args, env vars, output file names remain **backward compatible**
- [ ] Public-facing changes → `CHANGELOG.md` updated
- [ ] Documented files come from **real scan results**
- [ ] Uncertain information marked as **"uncertain"**
```

---

## 🎯 Issue Types

| Type | Label | Description |
| --- | --- | --- |
| 🐛 **Bug** | `bug` | Incorrect scan, generation, CLI behavior, or validation |
| ✨ **Feature** | `enhancement` | New framework detection, output format, provider, workflow |
| 📖 **Docs** | `documentation` | README, examples, generated doc clarity, contribution guides |
| ❓ **Question** | `question` | Usage, configuration, roadmap, or design discussion |

---

## 🧭 Design Principles

1. **Not a README summarizer** — it's a source-code learning path generator
2. **Every path must include "how to run this project"**
3. **All referenced files come from real scan results**
4. **Uncertain content must be labeled "uncertain"**
5. **Markdown output should be ready for a GitHub repo**
6. **External interfaces change carefully** — CLI args, env vars, output file names

---

## 📦 Release & Maintenance

This project follows [Semantic Versioning](https://semver.org/):

```
MAJOR.MINOR.PATCH
```

- `MAJOR`: breaking changes
- `MINOR`: new backward-compatible features
- `PATCH`: bug fixes, documentation, minor improvements

Update `CHANGELOG.md` when public-facing behavior changes. Breaking changes must include rationale, impact scope, and migration guide in the PR.

---

<div align="center">

**Thanks again for contributing!** 🎉

</div>
