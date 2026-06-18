from pathlib import Path

from sourceguide.repository import is_github_url, prepare_repository


def test_is_github_url_accepts_public_repo_url():
    assert is_github_url("https://github.com/pallets/flask")


def test_is_github_url_rejects_other_urls():
    assert not is_github_url("https://gitlab.com/org/repo")
    assert not is_github_url("not-a-url")


def test_prepare_repository_accepts_local_directory(tmp_path: Path):
    info = prepare_repository(str(tmp_path))

    assert info.root == tmp_path.resolve()
    assert info.name == tmp_path.name
    assert info.is_temporary is False

