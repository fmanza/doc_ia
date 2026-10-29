#!/usr/bin/env python3
"""Build the documentation site and package it as a ZIP for offline distribution.

Usage:
    python scripts/build_docs_zip.py
    python scripts/build_docs_zip.py --builder zensical
    python scripts/build_docs_zip.py --no-build          # only zip an existing site/
    python scripts/build_docs_zip.py --output-dir /tmp

Zensical ignores the ``hooks:`` key of mkdocs.yml, so for that builder this script runs the
hooks itself: ``hooks/sync_root_docs.py`` before the build and ``mkdocs_hooks.py`` (latest
ZIP in site/) after a successful build.

Before packaging, site/ must be browsable from file:// (double click on index.html, no server):
search index inlined as JS by the ``offline`` plugin, no remote scripts and no links to folders.
Otherwise the script exits with code 1.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import re
import subprocess
import sys
import tomllib
import zipfile
from datetime import datetime
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "site"
PYPROJECT = ROOT / "pyproject.toml"
ZIP_PREFIX = "doc_ia-docs"
# Files outside site/ shipped at the ZIP root: local server and viewing instructions.
EXTRA_FILES = ("scripts/start-server.py", "VER_DOCUMENTACION.md")

# Builders that do not execute the `hooks:` declared in mkdocs.yml.
HOOKLESS_BUILDERS: frozenset[str] = frozenset({"zensical"})

# Search index inlined as JS by the `offline` plugin: MkDocs Material, Zensical.
OFFLINE_SEARCH_INDEXES = ("search/search_index.js", "search.js")
MAX_REPORTED_PROBLEMS = 20
_SCRIPT_SRC_RE = re.compile(r'<script\b[^>]*\bsrc="([^"]+)"')
_URL_ATTR_RE = re.compile(r'\b(?:href|src)="([^"]*)"')
_SCHEME_RE = re.compile(r"[A-Za-z][A-Za-z0-9+.-]*:")


def _version() -> str:
    with PYPROJECT.open("rb") as fh:
        version: str = tomllib.load(fh)["project"]["version"]
    return version


def _load_hook(relative_path: str) -> ModuleType:
    """Load a hook module by path (the repo root is not on sys.path when run as a script)."""
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load hook module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _pre_build() -> None:
    print("[build_docs_zip] Pre-build: hooks/sync_root_docs.py")
    _load_hook("hooks/sync_root_docs.py").main()


def _post_build() -> None:
    print("[build_docs_zip] Post-build: mkdocs_hooks.py")
    _load_hook("mkdocs_hooks.py").on_post_build({"site_dir": str(SITE_DIR)})


def _build(builder: str, strict: bool) -> None:
    hookless = builder in HOOKLESS_BUILDERS
    cmd = [sys.executable, "-m", builder, "build"]
    if strict:
        cmd.append("--strict")
    if hookless:
        _pre_build()
    print(f"[build_docs_zip] Building with: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        sys.exit(result.returncode)
    if hookless:
        _post_build()


def _is_remote(url: str) -> bool:
    return url.startswith("//") or _SCHEME_RE.match(url) is not None


def _offline_problems(site_dir: Path) -> list[str]:
    """Reasons why site_dir cannot be browsed from file:// (empty list: ready)."""
    problems: list[str] = []
    if not (site_dir / "index.html").is_file():
        problems.append("index.html missing")
    if not any((site_dir / index).is_file() for index in OFFLINE_SEARCH_INDEXES):
        indexes = " or ".join(OFFLINE_SEARCH_INDEXES)
        problems.append(f"no search index as JS ({indexes}): enable the `offline` plugin")
    for page in sorted(site_dir.rglob("*.html")):
        html = page.read_text(encoding="utf-8", errors="replace")
        name = page.relative_to(site_dir).as_posix()
        for src in _SCRIPT_SRC_RE.findall(html):
            if _is_remote(src):
                problems.append(f"{name}: remote script {src}")
        for url in _URL_ATTR_RE.findall(html):
            path = url.split("#", 1)[0].split("?", 1)[0]
            if path.endswith("/") and not _is_remote(url):
                problems.append(f"{name}: link to a folder {url}")
    return problems


def _check_offline(site_dir: Path) -> None:
    problems = _offline_problems(site_dir)
    if not problems:
        return
    print(
        f"[build_docs_zip] ERROR: {site_dir} cannot be opened without a server "
        "(use_directory_urls: false, `offline` plugin, local iframe-worker in extra.polyfills):",
        file=sys.stderr,
    )
    for problem in problems[:MAX_REPORTED_PROBLEMS]:
        print(f"  - {problem}", file=sys.stderr)
    if len(problems) > MAX_REPORTED_PROBLEMS:
        print(f"  ... and {len(problems) - MAX_REPORTED_PROBLEMS} more", file=sys.stderr)
    sys.exit(1)


def _zip(output_dir: Path, version: str) -> Path:
    """Same layout as the latest ZIP of mkdocs_hooks.py: site/ without nested archives + extras."""
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"{ZIP_PREFIX}-{version}.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in sorted(p for p in SITE_DIR.rglob("*") if p.is_file()):
            if file_path.suffix in (".zip", ".sha256"):
                continue
            zf.write(file_path, arcname=file_path.relative_to(SITE_DIR).as_posix())
        for extra in EXTRA_FILES:
            extra_path = ROOT / extra
            if extra_path.is_file():
                zf.write(extra_path, arcname=extra_path.name)
    print(f"[build_docs_zip] Created: {archive}")
    return archive


def _sha256_file(file_path: Path) -> str:
    """Calculate SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def _create_checksum_files(archive: Path) -> str:
    """Create .sha256 and CHECKSUMS.txt files for integrity validation."""
    sha256_hash = _sha256_file(archive)

    sha256_file = archive.with_suffix(".zip.sha256")
    with open(sha256_file, "w") as f:
        f.write(f"{sha256_hash}  {archive.name}\n")

    checksums_file = archive.parent / "CHECKSUMS.txt"
    timestamp = datetime.now().isoformat()
    with open(checksums_file, "a") as f:
        f.write(f"{sha256_hash}  {archive.name}  ({timestamp})\n")

    file_size_mb = archive.stat().st_size / (1024 * 1024)
    print(f"\n[build_docs_zip] ZIP created: {archive.name} ({file_size_mb:.2f} MB)")
    print(f"[build_docs_zip] SHA256: {sha256_hash}")
    print(f"[build_docs_zip] Checksum saved to: {sha256_file.name}")
    print(f"[build_docs_zip] All checksums in: {checksums_file.name}")

    return sha256_hash


def main() -> None:
    parser = argparse.ArgumentParser(description="Build docs and package as offline ZIP.")
    parser.add_argument(
        "--builder",
        choices=["mkdocs", "zensical"],
        default="mkdocs",
        help="Doc builder to use (default: mkdocs)",
    )
    parser.add_argument(
        "--no-strict",
        dest="strict",
        action="store_false",
        default=True,
        help="Skip --strict flag when building",
    )
    parser.add_argument(
        "--no-build",
        action="store_true",
        default=False,
        help="Skip the build step; zip whatever is already in site/",
    )
    parser.add_argument(
        "--output-dir",
        default="dist",
        metavar="DIR",
        help="Directory for the output ZIP (default: dist/)",
    )
    args = parser.parse_args()

    if not args.no_build:
        _build(args.builder, args.strict)
    elif not SITE_DIR.exists():
        print(
            f"[build_docs_zip] ERROR: {SITE_DIR} does not exist. Run without --no-build first.",
            file=sys.stderr,
        )
        sys.exit(1)
    _check_offline(SITE_DIR)

    output_dir = (
        Path(args.output_dir) if Path(args.output_dir).is_absolute() else ROOT / args.output_dir
    )
    archive = _zip(output_dir, _version())
    _create_checksum_files(archive)


if __name__ == "__main__":
    main()
