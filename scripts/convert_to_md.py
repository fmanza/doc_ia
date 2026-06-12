"""Conversión determinista de documentos a Markdown mediante pandoc.

Detecta ficheros en formatos no legibles directamente (.pdf, .docx, .doc, .pptx, .odt,
.epub, .rst, .html, .htm) y los convierte a Markdown usando pandoc, depositando el
resultado en una subcarpeta `md/` dentro del directorio raíz del origen, reflejando
la estructura de subdirectorios para evitar colisiones de nombres.

Requiere pandoc instalado en el PATH del sistema:
  Windows:  winget install JohnMacFarlane.Pandoc
  macOS:    brew install pandoc
  Linux:    sudo apt install pandoc | sudo dnf install pandoc
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

CONVERTIBLE_EXTENSIONS: frozenset[str] = frozenset(
    {".pdf", ".docx", ".doc", ".pptx", ".odt", ".epub", ".rst", ".html", ".htm"}
)

_PANDOC_INSTALL = (
    "  Windows: winget install JohnMacFarlane.Pandoc\n"
    "  macOS:   brew install pandoc\n"
    "  Linux:   sudo apt install pandoc | sudo dnf install pandoc"
)


def pandoc_available() -> bool:
    """Devuelve True si pandoc está disponible en el PATH."""
    return shutil.which("pandoc") is not None


def collect_files(source: Path) -> list[Path]:
    """Devuelve ficheros convertibles bajo source, excluyendo la carpeta md/ de salida."""
    if source.is_file():
        return [source] if source.suffix.lower() in CONVERTIBLE_EXTENSIONS else []
    return sorted(
        p
        for p in source.rglob("*")
        if p.is_file()
        and p.suffix.lower() in CONVERTIBLE_EXTENSIONS
        and "md" not in p.relative_to(source).parts[:-1]
    )


def output_path(source_file: Path, source_root: Path, md_root: Path) -> Path:
    """Calcula la ruta de salida en md_root reflejando la estructura relativa."""
    relative = source_file.relative_to(source_root)
    return md_root / relative.with_suffix(".md")


def convert_file(
    source_file: Path,
    source_root: Path,
    md_root: Path,
    *,
    dry_run: bool = False,
) -> bool:
    """Convierte source_file a Markdown en md_root. Devuelve True si tuvo éxito."""
    out = output_path(source_file, source_root, md_root)

    if out.exists():
        rel_out = out.relative_to(md_root)
        print(f"  OMITIR  {source_file.relative_to(source_root)} → md/{rel_out} (ya existe)")
        return True

    if dry_run:
        print(f"  DRY-RUN {source_file.relative_to(source_root)} → md/{out.relative_to(md_root)}")
        return True

    out.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["pandoc", str(source_file), "-o", str(out), "--wrap=none"],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print(f"  OK      {source_file.relative_to(source_root)} → md/{out.relative_to(md_root)}")
        return True
    print(f"  ERROR   {source_file.relative_to(source_root)}: {result.stderr.strip()}")
    out.unlink(missing_ok=True)
    return False


def main() -> int:
    """Convierte documentos no-Markdown a Markdown usando pandoc."""
    parser = argparse.ArgumentParser(
        description="Convierte documentos a Markdown usando pandoc.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Formatos soportados: PDF, DOCX, DOC, PPTX, ODT, EPUB, RST, HTML, HTM\n"
            "Los ficheros convertidos se depositan en <origen>/md/ (estructura reflejada).\n\n"
            "Instalar pandoc si no está disponible:\n" + _PANDOC_INSTALL
        ),
    )
    parser.add_argument("source", type=Path, help="Fichero o directorio a convertir.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Muestra qué se convertiría sin ejecutar pandoc.",
    )
    args = parser.parse_args()

    if not pandoc_available():
        print(f"ERROR: pandoc no encontrado en el PATH.\n{_PANDOC_INSTALL}")
        return 1

    source: Path = args.source.resolve()
    if not source.exists():
        print(f"ERROR: El origen '{source}' no existe.")
        return 1

    source_root = source if source.is_dir() else source.parent
    md_root = source_root / "md"
    files = collect_files(source)

    if not files:
        print(f"No se encontraron ficheros convertibles en: {source}")
        return 0

    print(f"Convirtiendo {len(files)} fichero(s) → {md_root}")
    failures = sum(
        1
        for f in files
        if not convert_file(f, source_root, md_root, dry_run=args.dry_run)
    )

    if failures:
        print(f"\n{failures} error(s). Revisa la salida de pandoc.")
        return 1
    print(f"\nCompletado: {len(files)} convertido(s) en md/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
