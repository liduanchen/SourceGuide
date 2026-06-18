from pathlib import Path

from sourceguide.ai import RuleBasedAIClient
from sourceguide.models import GenerateOptions
from sourceguide.pipeline import generate


def test_pipeline_generates_docs_with_mock_ai(tmp_path: Path):
    project = tmp_path / "demo"
    project.mkdir()
    (project / "README.md").write_text("# Demo\n\n```bash\nnpm run dev\n```", encoding="utf-8")
    (project / "package.json").write_text(
        '{"dependencies":{"vite":"latest"},"scripts":{"dev":"vite","test":"vitest"}}',
        encoding="utf-8",
    )
    (project / "src").mkdir()
    (project / "src" / "main.ts").write_text("console.log('hi')", encoding="utf-8")

    options = GenerateOptions(
        target=str(project),
        route="quick",
        output_dir="docs/sourceguide",
        overwrite=True,
    )

    written = generate(options, api_key=None, ai_client=RuleBasedAIClient())
    names = {path.name for path in written}

    assert "README.md" in names
    assert "run-guide.md" in names
    assert "source-map.md" in names
    assert "02-快速了解路线.md" in names
    assert "01-我是小白路线.md" not in names
    assert "如何运行" in (project / "docs" / "sourceguide" / "02-快速了解路线.md").read_text(encoding="utf-8")

