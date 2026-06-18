from pathlib import Path

import pytest

from sourceguide.core_files import identify_core_files
from sourceguide.scanner import scan_project
from sourceguide.validators import ValidationError, validate_bundle


def test_core_files_prioritizes_entries_and_dependencies(tmp_path: Path):
    (tmp_path / "package.json").write_text("{}", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.ts").write_text("console.log('hi')", encoding="utf-8")

    scan = scan_project(tmp_path, "demo")
    report = identify_core_files(scan)
    paths = [item.path for item in report.files]

    assert "src/main.ts" in paths
    assert "package.json" in paths


def test_validator_rejects_missing_runtime_section(tmp_path: Path):
    (tmp_path / "README.md").write_text("# Demo", encoding="utf-8")
    scan = scan_project(tmp_path, "demo")

    with pytest.raises(ValidationError):
        validate_bundle({"02-快速了解路线.md": "# 快速了解\n"}, scan)


def test_validator_rejects_unknown_file_references(tmp_path: Path):
    (tmp_path / "README.md").write_text("# Demo", encoding="utf-8")
    scan = scan_project(tmp_path, "demo")

    with pytest.raises(ValidationError):
        validate_bundle({"README.md": "See `missing.py`."}, scan)

