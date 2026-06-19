"""Conversión determinista de documentos a Markdown con validación previa.

Detecta ficheros en formatos no legibles directamente y los convierte a Markdown,
depositando el resultado en una subcarpeta `md/` dentro del directorio raíz del
origen (estructura de subdirectorios reflejada para evitar colisiones de nombres).

Flujo: VALIDACIÓN → CONVERSIÓN → INFORME
  1. Validación previa: extensiones soportadas, plugins disponibles, integridad de ficheros.
  2. Conversión: markitdown (principal) o pandoc (complemento) según disponibilidad.
  3. Informe: resumen de resultados por fichero.

Herramientas utilizadas según extensión:

  markitdown (principal):
    PDF (.pdf)               → pdfminer
    DOCX (.docx)             → python-docx
    PPTX (.pptx)             → python-pptx
    XLSX (.xlsx)              → openpyxl
    XLS (.xls)               → xlrd
    HTML/HTM (.html, .htm)   → beautifulsoup4 (core)
    CSV (.csv)               → built-in
    EPUB (.epub)              → built-in
    IPYNB (.ipynb)            → built-in

  pandoc (complemento — formatos sin soporte en markitdown):
    DOC (.doc), ODT (.odt), RST (.rst)

  pandoc (fallback — cuando el plugin de markitdown no está instalado):
    DOCX, PPTX, EPUB

Uso:
  python scripts/convert_to_md.py <ruta>                 # Validar + convertir
  python scripts/convert_to_md.py <ruta> --validate-only # Solo validar, sin convertir
  python scripts/convert_to_md.py <ruta> --dry-run       # Mostrar qué se convertiría
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Mapeo de extensiones y plugins
# ---------------------------------------------------------------------------

MARKITDOWN_PLUGINS: dict[str, str | None] = {
    ".pdf": "pdfminer",
    ".docx": "docx",
    ".pptx": "pptx",
    ".xlsx": "openpyxl",
    ".xls": "xlrd",
    ".html": None,
    ".htm": None,
    ".csv": None,
    ".epub": None,
    ".ipynb": None,
}

MARKITDOWN_EXTENSIONS: frozenset[str] = frozenset(MARKITDOWN_PLUGINS.keys())

PANDOC_ONLY_EXTENSIONS: frozenset[str] = frozenset({".doc", ".odt", ".rst"})

PANDOC_FALLBACK_EXTENSIONS: frozenset[str] = frozenset({".docx", ".pptx", ".epub"})

CONVERTIBLE_EXTENSIONS: frozenset[str] = MARKITDOWN_EXTENSIONS | PANDOC_ONLY_EXTENSIONS

_PANDOC_INSTALL = (
    "  Windows: winget install JohnMacFarlane.Pandoc\n"
    "  macOS:   brew install pandoc\n"
    "  Linux:   sudo apt install pandoc | sudo dnf install pandoc"
)
_MARKITDOWN_INSTALL = "  pip install markitdown"


# ---------------------------------------------------------------------------
# Disponibilidad de herramientas
# ---------------------------------------------------------------------------


def pandoc_available() -> bool:
    """Devuelve True si pandoc está disponible en el PATH."""
    return shutil.which("pandoc") is not None


def markitdown_available() -> bool:
    """Devuelve True si el paquete markitdown está instalado."""
    return importlib.util.find_spec("markitdown") is not None


def _plugin_available(ext: str) -> bool:
    """Devuelve True si el plugin de markitdown para la extensión está disponible."""
    plugin = MARKITDOWN_PLUGINS.get(ext)
    if plugin is None:
        return True
    return importlib.util.find_spec(plugin) is not None


# ---------------------------------------------------------------------------
# Validación previa
# ---------------------------------------------------------------------------


def validate_file(path: Path) -> list[str]:
    """Valida integridad de un fichero antes de convertir. Devuelve lista de errores."""
    errors: list[str] = []
    if not path.exists():
        errors.append("no existe")
        return errors
    if not path.is_file():
        errors.append("no es un fichero regular")
        return errors
    if path.stat().st_size == 0:
        errors.append("fichero vacío (0 bytes)")
    if not os.access(path, os.R_OK):
        errors.append("sin permisos de lectura")
    return errors


def select_converter(ext: str) -> str:
    """Selecciona conversor óptimo: 'markitdown', 'pandoc' o 'none'."""
    if ext in MARKITDOWN_EXTENSIONS:
        if markitdown_available() and _plugin_available(ext):
            return "markitdown"
        if ext in PANDOC_FALLBACK_EXTENSIONS and pandoc_available():
            return "pandoc"
        return "none"
    if ext in PANDOC_ONLY_EXTENSIONS:
        return "pandoc" if pandoc_available() else "none"
    return "none"


def _report_tools(report: list[str]) -> None:
    """Añade al informe el estado de las herramientas de conversión."""
    has_markitdown = markitdown_available()
    mk_label = f"OK (v{_markitdown_version()})" if has_markitdown else "NO INSTALADO"
    report.append(f"  markitdown: {mk_label}")
    if has_markitdown:
        _report_plugins(report)
    pandoc_label = "OK" if pandoc_available() else "NO ENCONTRADO"
    report.append(f"  pandoc:     {pandoc_label}")
    report.append("")


def _report_plugins(report: list[str]) -> None:
    """Añade al informe el detalle de plugins de markitdown."""
    installed: list[str] = []
    missing: list[str] = []
    for ext, plugin in sorted(MARKITDOWN_PLUGINS.items()):
        if plugin is None:
            installed.append(f"{ext} (core)")
        elif importlib.util.find_spec(plugin) is not None:
            installed.append(f"{ext} ({plugin})")
        else:
            missing.append(f"{ext} ({plugin})")
    if installed:
        report.append(f"    Plugins OK: {', '.join(installed)}")
    if missing:
        report.append(f"    Plugins FALTAN: {', '.join(missing)}")


def _diagnose_no_converter(ext: str) -> str:
    """Diagnostica por qué no hay conversor disponible para una extensión."""
    if ext in MARKITDOWN_EXTENSIONS and not markitdown_available():
        return f"SIN CONVERSOR: requiere markitdown ({_MARKITDOWN_INSTALL.strip()})"
    if ext in MARKITDOWN_EXTENSIONS and not _plugin_available(ext):
        plugin = MARKITDOWN_PLUGINS.get(ext, "?")
        has_fallback = ext in PANDOC_FALLBACK_EXTENSIONS
        fallback = "" if has_fallback else " (pandoc no disponible como fallback)"
        return f"SIN PLUGIN: requiere pip install {plugin}{fallback}"
    return "SIN CONVERSOR: requiere pandoc"


def _validate_single_file(f: Path) -> tuple[str, str | None]:
    """Valida un fichero y devuelve (status, error_o_None)."""
    file_errors = validate_file(f)
    if file_errors:
        status = f"ERROR: {'; '.join(file_errors)}"
        return status, f"{f.name}: {status}"

    converter = select_converter(f.suffix.lower())
    if converter == "none":
        status = _diagnose_no_converter(f.suffix.lower())
        return status, f"{f.name}: {status}"

    return f"OK → {converter}", None


def validate_conversion_readiness(files: list[Path]) -> tuple[list[str], list[str], bool]:
    """Valida pre-condiciones de conversión.

    Devuelve (informe, errores_bloqueantes, todo_ok).
    """
    report: list[str] = ["=== Validación previa de conversión ===\n"]
    errors: list[str] = []

    _report_tools(report)

    for f in files:
        status, error = _validate_single_file(f)
        if error:
            errors.append(error)
        report.append(f"  {f.name:40s} {status}")

    report.append("")
    if not errors:
        report.append(f"Validación completada: {len(files)} fichero(s) listos para conversión.")
    else:
        report.append(f"Validación completada: {len(errors)} error(es) de {len(files)} fichero(s).")
        report.append("Ficheros con problemas:")
        for e in errors:
            report.append(f"  ✗ {e}")

    return report, errors, len(errors) == 0


def _markitdown_version() -> str:
    """Devuelve la versión de markitdown instalada, o '?' si no se puede determinar."""
    try:
        from importlib.metadata import version  # noqa: PLC0415

        return version("markitdown")
    except Exception:  # noqa: BLE001
        return "?"


# ---------------------------------------------------------------------------
# Recolección de ficheros
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Conversión
# ---------------------------------------------------------------------------


def _convert_with_markitdown(
    source_file: Path,
    out: Path,
    md_root: Path,
    rel: str,
    *,
    dry_run: bool,
) -> bool:
    """Convierte un documento a Markdown usando markitdown."""
    if dry_run:
        print(f"  DRY-RUN {rel} → md/{out.relative_to(md_root)}")
        return True
    if not markitdown_available():
        print(f"  ERROR   {rel}: markitdown no instalado ({_MARKITDOWN_INSTALL.strip()})")
        return False
    from markitdown import MarkItDown  # noqa: PLC0415

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

    ext = source_file.suffix.lower()
    converter = select_converter(ext)

    if converter == "markitdown":
        return _convert_with_markitdown(source_file, out, md_root, rel, dry_run=dry_run)
    if converter == "pandoc":
        return _convert_with_pandoc(source_file, out, md_root, rel, dry_run=dry_run)

    plugin = MARKITDOWN_PLUGINS.get(ext)
    if plugin:
        print(f"  ERROR   {rel}: plugin '{plugin}' no instalado (pip install {plugin})")
    else:
        print(f"  ERROR   {rel}: sin conversor disponible para {ext}")
    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    """Convierte documentos a Markdown con validación previa."""
    parser = argparse.ArgumentParser(
        description=(
            "Convierte documentos a Markdown con validación previa.\n"
            "markitdown (principal) para PDF/DOCX/PPTX/XLSX/HTML/CSV/EPUB/IPYNB;\n"
            "pandoc (complemento) para DOC/ODT/RST y fallback de DOCX/PPTX/EPUB."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Herramientas requeridas:\n"
            "  markitdown (principal): pip install 'markitdown[all]'\n"
            "    Plugins opcionales: pip install python-docx python-pptx openpyxl xlrd\n"
            "  pandoc (complemento):\n" + _PANDOC_INSTALL + "\n\n"
            "Los ficheros convertidos se depositan en <origen>/md/ (estructura reflejada).\n\n"
            "Flujo: VALIDACIÓN → CONVERSIÓN → INFORME\n"
            "  --validate-only ejecuta solo la fase de validación sin convertir."
        ),
    )
    parser.add_argument("source", type=Path, help="Fichero o directorio a convertir.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Muestra qué se convertiría sin ejecutar conversión.",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Solo ejecuta validación previa (extensiones, plugins, integridad). No convierte.",
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

    # --- Fase 1: Validación previa (siempre) ---
    report, validation_errors, all_ok = validate_conversion_readiness(files)
    for line in report:
        print(line)

    if args.validate_only:
        return 0 if all_ok else 1

    if validation_errors and not args.dry_run:
        print(f"\n⚠  {len(validation_errors)} fichero(s) no se podrán convertir (ver arriba).")
        print("Los ficheros válidos se procesarán igualmente.\n")

    # --- Fase 2: Conversión ---
    print(f"Convirtiendo {len(files)} fichero(s) → {md_root}")
    failures = sum(
        1
        for f in files
        if not convert_file(f, source_root, md_root, dry_run=args.dry_run)
    )

    if failures:
        print(f"\n{failures} error(es). Revisa la salida anterior.")
        return 1
    print(f"\nCompletado: {len(files)} convertido(s) en md/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
