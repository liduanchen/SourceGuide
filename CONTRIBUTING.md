# Contributing to SourceGuide

Thanks for helping SourceGuide become a better open-source learning tool.

## Development Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

On macOS or Linux, activate the environment with:

```bash
source .venv/bin/activate
```

## Pull Request Checklist

- Add or update tests for behavior changes.
- Keep CLI arguments, environment variable names, and output file names backward compatible when possible.
- Update `CHANGELOG.md` for public-facing changes.
- Do not commit API keys, `.env`, generated caches, or temporary cloned repositories.
- If generated docs reference files, ensure those files come from real scan results.

## Issue Types

- Bug: incorrect scan, generation, CLI behavior, or validation.
- Feature: new framework detection, output format, provider, or workflow.
- Docs: README, examples, generated document clarity.
- Question: usage, configuration, or roadmap discussion.

