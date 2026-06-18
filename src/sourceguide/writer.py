from __future__ import annotations

from pathlib import Path


class WriteError(RuntimeError):
    pass


def write_bundle(bundle: dict[str, str], output_dir: Path, overwrite: bool = False) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for filename, content in bundle.items():
        path = output_dir / filename
        if path.exists() and not overwrite:
            raise WriteError(f"Output file already exists: {path}. Use --overwrite to replace it.")
        path.write_text(content.rstrip() + "\n", encoding="utf-8")
        written.append(path)
    return written

