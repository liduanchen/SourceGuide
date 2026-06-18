from pathlib import Path

from typer.testing import CliRunner

from sourceguide.cli import app


def test_cli_offline_generates_without_api_key(tmp_path: Path, monkeypatch):
    project = tmp_path / "demo"
    project.mkdir()
    (project / "README.md").write_text("# Demo", encoding="utf-8")
    (project / "package.json").write_text(
        '{"scripts":{"dev":"vite"},"dependencies":{"vite":"latest"}}',
        encoding="utf-8",
    )
    (project / "src").mkdir()
    (project / "src" / "main.ts").write_text("console.log('hi')", encoding="utf-8")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    result = CliRunner().invoke(
        app,
        [
            "generate",
            str(project),
            "--route",
            "quick",
            "--offline",
            "--output",
            "docs/sourceguide",
            "--overwrite",
        ],
    )

    assert result.exit_code == 0
    assert (project / "docs" / "sourceguide" / "02-快速了解路线.md").exists()

