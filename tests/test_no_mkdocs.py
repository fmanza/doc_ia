"""Guarda de ADR-003: Zensical es el único generador y MkDocs queda fuera.

Falla si reaparece un comando o paquete de MkDocs en código, instrucciones, plantillas o
documentación viva. Quedan fuera el histórico (ADR-001, CHANGELOG, sesiones `.ai/`), la sección
«Histórico (MkDocs)» de EDGE_CASES y este propio fichero.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MKDOCS_RE = re.compile(
    # `mkdocs-material` sin el nombre de fichero del ADR-001 (histórico, enlazado a propósito).
    r"mkdocs (build|serve|gh-deploy)|mkdocs-material(?!-por-defecto)|^mkdocs==",
    re.IGNORECASE | re.MULTILINE,
)

# Histórico o generado: puede nombrar MkDocs a propósito.
EXCLUDED = (
    ".ai/sessions/",
    "CHANGELOG.md",
    "docs/changelog.md",
    "docs/adr/ADR-001-mkdocs-material-por-defecto.md",
    "tests/test_no_mkdocs.py",
)
HISTORY_HEADING = "## Histórico (MkDocs)"


def _tracked_text_files() -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files", "*.md", "*.py", "*.yml", "*.yaml", "*.txt", "*.json", "*.toml"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return [ROOT / line for line in out.splitlines() if not line.startswith(EXCLUDED)]


def _live_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.name == "EDGE_CASES.md" and HISTORY_HEADING in text:
        text = text.split(HISTORY_HEADING, 1)[0]
    return text


def test_no_mkdocs_commands_or_packages_remain() -> None:
    hits = [
        f"{path.relative_to(ROOT).as_posix()}: {match.group(0)}"
        for path in _tracked_text_files()
        if path.is_file()
        for match in MKDOCS_RE.finditer(_live_text(path))
    ]
    assert not hits, "MkDocs fuera (ADR-003); restos:\n" + "\n".join(hits)
