[🇨🇳 中文](README.md) | [🇬🇧 English](README_EN.md)

---

# Examples

This directory documents example SourceGuide runs for small public repositories.

The MVP test suite uses local fixtures so CI never depends on a real API key or network access. Before publishing a release, maintainers should generate at least two real examples with commands like:

```bash
sourceguide generate https://github.com/pallets/click --route all --output examples/click-sourceguide --overwrite
sourceguide generate https://github.com/vitejs/vite --route quick --output examples/vite-sourceguide --overwrite
```

Do not commit API keys or local `.env` files.
