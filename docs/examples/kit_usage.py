"""Ejemplo: instalar, actualizar y comprobar el kit de documentación (sin red, determinista)."""

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from kit import Report, check, sync  # noqa: E402

MANIFEST = """[metodologia]
pyproject.toml
.github/prompts/document_project.prompt.md
scripts/doc_trace.py

[lanzadores]
.github/templates/kit/documentar.command.md -> .claude/commands/documentar.md

[instancia]
.github/templates/kit/DOCUMENTAR.template.md -> DOCUMENTAR.md
"""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def show(title: str, report: Report) -> None:
    print(title)
    for kind, rel in report.changes:
        print(f"  {kind:<16} {rel}")
    for rel, reason in report.conflicts:
        print(f"  {'conflicto':<16} {rel} — {reason}")


with tempfile.TemporaryDirectory() as tmp:
    doc_ia = Path(tmp) / "doc_ia"  # simula un doc_ia mínimo con su lista blanca
    write(doc_ia / ".github/kit/MANIFEST.txt", MANIFEST)
    write(doc_ia / "pyproject.toml", '[project]\nname = "doc_ia"\nversion = "1.0.0"\n')
    write(doc_ia / ".github/prompts/document_project.prompt.md", "# prompt\n")
    write(doc_ia / "scripts/doc_trace.py", "print('v1')\n")
    write(doc_ia / ".github/templates/kit/documentar.command.md", "# /documentar\n")
    write(
        doc_ia / ".github/templates/kit/DOCUMENTAR.template.md",
        "<!--\nPLANTILLA\n-->\n# Cómo documentar {proyecto}\n",
    )
    dest = Path(tmp) / "mi_modulo_docs"  # raíz del destino
    write(dest / "mkdocs.yml", "site_name: Mi Módulo\n")

    show("1. Instalación:", sync(doc_ia, dest, today="2026-11-07"))
    print("   DOCUMENTAR.md:", (dest / "DOCUMENTAR.md").read_text(encoding="utf-8").strip())
    show("2. Comprobación:", check(dest))

    write(dest / ".ai/prompts/documentar.prompt.md", "# instancia\n")  # lo escribe el CIERRE
    write(doc_ia / "scripts/doc_trace.py", "print('v2')\n")  # doc_ia publica un cambio
    show("3. Comprobación contra doc_ia:", check(dest, doc_ia))
    show("4. Actualización:", sync(doc_ia, dest, today="2026-11-08"))

    write(dest / ".doc_ia/scripts/doc_trace.py", "print('parche local')\n")
    write(doc_ia / "scripts/doc_trace.py", "print('v3')\n")
    show("5. Actualización con un fichero editado en el destino:", sync(doc_ia, dest))
    kept = (dest / ".doc_ia/scripts/doc_trace.py").read_text(encoding="utf-8")
    print("   Contenido conservado:", kept.strip())
