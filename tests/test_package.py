# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Package metadata and the local-only invariant."""

from __future__ import annotations

import ast
import tomllib
from pathlib import Path

import jspassgen

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "src" / "jspassgen"

# Modules the library must never import: network access (it makes no call
# and has no telemetry) and the non-cryptographic ``random`` module.
FORBIDDEN = {"random", "socket", "ssl", "http", "urllib", "httpx", "requests", "aiohttp"}


def imported_roots(path: Path) -> set[str]:
    """The top-level module of every import in ``path``."""
    roots: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            roots.add(node.module.split(".")[0])
    return roots


def test_version_comes_from_pyproject() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    assert jspassgen.__version__ == project["version"]


def test_public_names() -> None:
    assert sorted(jspassgen.__all__) == ["RandomGeneratorPort", "SecretsRandom", "__version__"]


def test_library_imports_nothing_forbidden() -> None:
    files = sorted(SOURCE.rglob("*.py"))
    assert files
    for path in files:
        assert not imported_roots(path) & FORBIDDEN, path.name


def test_the_import_guard_sees_forbidden_imports(tmp_path: Path) -> None:
    sample = tmp_path / "sample.py"
    sample.write_text("import random\nfrom urllib.request import urlopen\nfrom . import x\n")
    assert imported_roots(sample) == {"random", "urllib"}
