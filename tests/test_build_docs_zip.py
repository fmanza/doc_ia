"""Tests para scripts/build_docs_zip.py y mkdocs_hooks.py — ZIP offline con SHA256."""

from __future__ import annotations

import hashlib
import subprocess
import sys
import zipfile
from pathlib import Path
from unittest.mock import patch

import mkdocs_hooks
import pytest
from scripts import build_docs_zip


def _project(tmp_path: Path, version: str = "0.1.0") -> Path:
    (tmp_path / "pyproject.toml").write_text(
        f'[project]\nname = "demo"\nversion = "{version}"\n', encoding="utf-8"
    )
    site = tmp_path / "site"
    site.mkdir()
    (site / "index.html").write_text("<h1>Demo</h1>", encoding="utf-8")
    return tmp_path


def _run_main(root: Path, *argv: str) -> None:
    with (
        patch.object(build_docs_zip, "ROOT", root),
        patch.object(build_docs_zip, "SITE_DIR", root / "site"),
        patch.object(build_docs_zip, "PYPROJECT", root / "pyproject.toml"),
        patch.object(sys, "argv", ["build_docs_zip.py", *argv]),
    ):
        build_docs_zip.main()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_main_builds_strict_and_packages_versioned_zip(tmp_path: Path) -> None:
    root = _project(tmp_path)
    ok = subprocess.CompletedProcess(args=[], returncode=0)
    with patch.object(build_docs_zip.subprocess, "run", return_value=ok) as run:
        _run_main(root)
    cmd = run.call_args.args[0]
    assert cmd[-2:] == ["build", "--strict"]
    archive = root / "dist" / "doc_ia-docs-0.1.0.zip"
    assert archive.is_file()
    assert (root / "dist" / "doc_ia-docs-0.1.0.zip.sha256").is_file()
    assert "doc_ia-docs-0.1.0.zip" in (root / "dist" / "CHECKSUMS.txt").read_text()
    with zipfile.ZipFile(archive) as zf:
        assert "index.html" in zf.namelist()


def test_main_no_strict_omits_flag(tmp_path: Path) -> None:
    root = _project(tmp_path)
    ok = subprocess.CompletedProcess(args=[], returncode=0)
    with patch.object(build_docs_zip.subprocess, "run", return_value=ok) as run:
        _run_main(root, "--no-strict")
    assert "--strict" not in run.call_args.args[0]


def test_main_no_build_without_site_exits_1(tmp_path: Path) -> None:
    root = _project(tmp_path)
    (root / "site" / "index.html").unlink()
    (root / "site").rmdir()
    with pytest.raises(SystemExit) as exc:
        _run_main(root, "--no-build")
    assert exc.value.code == 1
    assert not (root / "dist").exists()


def test_main_build_failure_propagates_exit_code(tmp_path: Path) -> None:
    root = _project(tmp_path)
    failed = subprocess.CompletedProcess(args=[], returncode=3)
    with (
        patch.object(build_docs_zip.subprocess, "run", return_value=failed),
        pytest.raises(SystemExit) as exc,
    ):
        _run_main(root)
    assert exc.value.code == 3
    assert not (root / "dist").exists()


def test_main_no_build_relative_output_dir(tmp_path: Path) -> None:
    root = _project(tmp_path, version="2.0.0")
    _run_main(root, "--no-build", "--output-dir", "out")
    assert (root / "out" / "doc_ia-docs-2.0.0.zip").is_file()


def test_sha256_file_matches_archive(tmp_path: Path) -> None:
    root = _project(tmp_path)
    _run_main(root, "--no-build")
    archive = root / "dist" / "doc_ia-docs-0.1.0.zip"
    line = (root / "dist" / "doc_ia-docs-0.1.0.zip.sha256").read_text(encoding="utf-8")
    assert line == f"{_sha256(archive)}  {archive.name}\n"


def test_checksums_txt_is_append_only(tmp_path: Path) -> None:
    root = _project(tmp_path)
    _run_main(root, "--no-build")
    _run_main(root, "--no-build")
    lines = (root / "dist" / "CHECKSUMS.txt").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert all(line.split("  ")[1] == "doc_ia-docs-0.1.0.zip" for line in lines)


def test_post_build_hook_creates_latest_zip(tmp_path: Path) -> None:
    site = tmp_path / "site"
    site.mkdir()
    (site / "index.html").write_text("<h1>Demo</h1>", encoding="utf-8")
    mkdocs_hooks.on_post_build({"site_dir": str(site)})
    latest = site / "doc_ia-docs-latest.zip"
    assert latest.is_file()
    line = (site / "doc_ia-docs-latest.zip.sha256").read_text(encoding="utf-8")
    assert line == f"{_sha256(latest)}  {latest.name}\n"
    with zipfile.ZipFile(latest) as zf:
        names = zf.namelist()
    assert "index.html" in names
    assert "start-server.py" in names
    assert not any(n.endswith((".zip", ".sha256")) for n in names)
