from pathlib import Path

from sourceguide.runtime import infer_runtime
from sourceguide.scanner import scan_project
from sourceguide.stack import identify_stack


def test_scanner_ignores_unwanted_files(tmp_path: Path):
    (tmp_path / "README.md").write_text("# Demo", encoding="utf-8")
    (tmp_path / "package.json").write_text('{"scripts":{"dev":"vite"}}', encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.ts").write_text("console.log('hi')", encoding="utf-8")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "ignored.js").write_text("ignored", encoding="utf-8")
    (tmp_path / "dist").mkdir()
    (tmp_path / "dist" / "bundle.min.js").write_text("ignored", encoding="utf-8")

    scan = scan_project(tmp_path, "demo")

    assert "README.md" in scan.readmes
    assert "package.json" in scan.dependency_files
    assert "src/main.ts" in scan.entry_candidates
    assert "node_modules/ignored.js" not in scan.file_paths
    assert "dist/bundle.min.js" not in scan.file_paths


def test_stack_identifies_node_vite_react(tmp_path: Path):
    (tmp_path / "package.json").write_text(
        '{"dependencies":{"vite":"latest","react":"latest"},"scripts":{"dev":"vite"}}',
        encoding="utf-8",
    )

    scan = scan_project(tmp_path, "demo")
    stack = identify_stack(scan)

    assert "Node.js" in stack.languages
    assert "Vite" in stack.frameworks
    assert "React" in stack.frameworks
    assert "npm scripts" in stack.tools


def test_runtime_infers_node_commands(tmp_path: Path):
    (tmp_path / "package.json").write_text(
        '{"scripts":{"dev":"vite","test":"vitest","lint":"eslint ."}}',
        encoding="utf-8",
    )

    scan = scan_project(tmp_path, "demo")
    stack = identify_stack(scan)
    runtime = infer_runtime(scan, stack)

    assert runtime.install[0].command == "npm install"
    assert runtime.recommended[0].command == "npm run dev"
    assert runtime.tests[0].command == "npm run test"
    assert runtime.lint[0].command == "npm run lint"


def test_runtime_infers_python_commands(tmp_path: Path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
    (tmp_path / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "cli.py").write_text("print('hi')", encoding="utf-8")

    scan = scan_project(tmp_path, "demo")
    stack = identify_stack(scan)
    runtime = infer_runtime(scan, stack)

    assert any(command.command == "pip install -e ." for command in runtime.install)
    assert any(command.command == "pytest" for command in runtime.tests)

