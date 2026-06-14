"""Conversión determinista de documentos a Markdown.

Detecta ficheros en formatos no legibles directamente y los convierte a Markdown,
depositando el resultado en una subcarpeta `md/` dentro del directorio raíz del
origen (estructura de subdirectorios reflejada para evitar colisiones de nombres).

Herramientas utilizadas según extensión:
  PDF                       → markitdown  (pip install markitdown)
  DOCX, DOC, PPTX, ODT,
  EPUB, RST, HTML, HTM      → pandoc      (winget/brew/apt install pandoc)

Pandoc NO puede leer PDF; markitdown cubre esa brecha.
"""

from __future__ import annotations

import argparse
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

PANDOC_EXTENSIONS: frozenset[str] = frozenset(
    {".docx", ".doc", ".pptx", ".odt", ".epub", ".rst", ".html", ".htm"}
)
MARKITDOWN_EXTENSIONS: frozenset[str] = frozenset({".pdf"})
CONVERTIBLE_EXTENSIONS: frozenset[str] = PANDOC_EXTENSIONS | MARKITDOWN_EXTENSIONS

_PANDOC_INSTALL = (
    "  Windows: winget install JohnMacFarlane.Pandoc\n"
    "  macOS:   brew install pandoc\n"
    "  Linux:   sudo apt install pandoc | sudo dnf install pandoc"
)
_MARKITDOWN_INSTALL = "  pip install markitdown"


def pandoc_available() -> bool:
    """Devuelve True si pandoc está disponible en el PATH."""
    return shutil.which("pandoc") is not None


def markitdown_available() -> bool:
    """Devuelve True si el paquete markitdown está instalado."""
    return importlib.util.find_spec("markitdown") is not None


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


def _convert_with_markitdown(
    source_file: Path,
    out: Path,
    md_root: Path,
    rel: str,
    *,
    dry_run: bool,
) -> bool:
    """Convierte un PDF a Markdown usando markitdown."""
    if dry_run:
        print(f"  DRY-RUN {rel} → md/{out.relative_to(md_root)}")
        return True
    if not markitdown_available():
        print(f"  ERROR   {rel}: markitdown no instalado ({_MARKITDOWN_INSTALL.strip()})")
        return False
    from markitdown import MarkItDown  # type: ignore[import-not-found]  # noqa: PLC0415

    try:
        result = MarkItDown().convert(str(source_file))
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(result.text_content, encoding="utf-8")
        print(f"  OK      {rel} → md/{out.relative_to(md_root)}")
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"  ERROR   {rel}: {exc}")
        out.unlink(missing_ok=True)
        return False


def _convert_with_pandoc(
    source_file: Path,
    out: Path,
    md_root: Path,
    rel: str,
    *,
    dry_run: bool,
) -> bool:
    """Convierte un documento a Markdown usando pandoc."""
    if dry_run:
        print(f"  DRY-RUN {rel} → md/{out.relative_to(md_root)}")
        return True
    if not pandoc_available():
        print(f"  ERROR   {rel}: pandoc no encontrado en el PATH")
        return False
    out.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["pandoc", str(source_file), "-o", str(out), "--wrap=none"],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print(f"  OK      {rel} → md/{out.relative_to(md_root)}")
        return True
    print(f"  ERROR   {rel}: {result.stderr.strip()}")
    out.unlink(missing_ok=True)
    return False


def convert_file(
    source_file: Path,
    source_root: Path,
    md_root: Path,
    *,
    dry_run: bool = False,
) -> bool:
    """Convierte source_file a Markdown en md_root. Devuelve True si tuvo éxito u omitió."""
    out = output_path(source_file, source_root, md_root)
    rel = str(source_file.relative_to(source_root))

    if out.exists():
        print(f"  OMITIR  {rel} → md/{out.relative_to(md_root)} (ya existe)")
        return True

    if source_file.suffix.lower() in MARKITDOWN_EXTENSIONS:
        return _convert_with_markitdown(source_file, out, md_root, rel, dry_run=dry_run)
    return _convert_with_pandoc(source_file, out, md_root, rel, dry_run=dry_run)


def main() -> int:
    """Convierte documentos no-Markdown a Markdown (markitdown para PDF, pandoc para el resto)."""
    parser = argparse.ArgumentParser(
        description="Convierte documentos a Markdown (markitdown para PDF, pandoc para el resto).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Herramientas requeridas:\n"
            "  PDF               → markitdown: pip install markitdown\n"
            "  DOCX/PPTX/…       → pandoc:\n" + _PANDOC_INSTALL + "\n\n"
            "Los ficheros convertidos se depositan en <origen>/md/ (estructura reflejada)."
        ),
    )
    parser.add_argument("source", type=Path, help="Fichero o directorio a convertir.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Muestra qué se convertiría sin ejecutar conversión.",
    )
    args = parser.parse_args()

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

    # Advertir de herramientas faltantes antes de procesar
    needs_pandoc = any(f.suffix.lower() in PANDOC_EXTENSIONS for f in files)
    needs_markitdown = any(f.suffix.lower() in MARKITDOWN_EXTENSIONS for f in files)
    if needs_pandoc and not pandoc_available() and not args.dry_run:
        print(f"⚠  pandoc no encontrado — los ficheros DOCX/PPTX/… fallarán.\n{_PANDOC_INSTALL}")
    if needs_markitdown and not markitdown_available() and not args.dry_run:
        print(f"⚠  markitdown no instalado — los PDF fallarán.\n{_MARKITDOWN_INSTALL}")

    print(f"Convirtiendo {len(files)} fichero(s) → {md_root}")
    failures = sum(
        1
        for f in files
        if not convert_file(f, source_root, md_root, dry_run=args.dry_run)
    )

    if failures:
        print(f"\n{failures} error(s). Revisa la salida anterior.")
        return 1
    print(f"\nCompletado: {len(files)} convertido(s) en md/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
