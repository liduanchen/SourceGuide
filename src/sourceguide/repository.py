from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path

from .models import RepositoryInfo

GITHUB_RE = re.compile(r"^https://github\.com/[^/\s]+/[^/\s]+/?$")


class RepositoryError(RuntimeError):
    pass


def is_github_url(value: str) -> bool:
    return bool(GITHUB_RE.match(value.strip()))


def prepare_repository(target: str) -> RepositoryInfo:
    if is_github_url(target):
        return clone_public_repository(target)

    path = Path(target).expanduser().resolve()
    if not path.exists() or not path.is_dir():
        raise RepositoryError(f"Input is not a directory or supported GitHub URL: {target}")
    return RepositoryInfo(source=target, root=path, name=path.name, is_temporary=False)


def clone_public_repository(url: str) -> RepositoryInfo:
    repo_name = url.rstrip("/").split("/")[-1]
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]
    temp_dir = Path(tempfile.mkdtemp(prefix="sourceguide-"))
    repo_dir = temp_dir / repo_name
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", url, str(repo_dir)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError as exc:
        raise RepositoryError("git is required to clone GitHub repositories.") from exc
    except subprocess.CalledProcessError as exc:
        raise RepositoryError(f"Failed to clone repository: {exc.stderr.strip()}") from exc
    return RepositoryInfo(source=url, root=repo_dir, name=repo_name, is_temporary=True)

