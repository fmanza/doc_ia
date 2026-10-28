"""Conversión de documentos a Markdown con selección explícita de motor.

Detecta ficheros en formatos no legibles directamente y los convierte a Markdown,
depositando el resultado en una subcarpeta ``md/`` dentro del directorio raíz del
origen (estructura de subdirectorios reflejada para evitar colisiones de nombres).

Motores disponibles (--engine):
  docling     (default)  -> PDF, DOCX, PPTX, XLSX, CSV, HTML, EPUB, imágenes,
                            email (EML/MSG), LaTeX, audio (WAV/MP3)
  markitdown             -> PDF, DOCX, PPTX, XLSX, XLS, CSV, EPUB, HTML, HTM, MSG
  pandoc                 -> DOC, ODT, RST, TEX/LATEX

Antes de cada conversión se ejecuta una validación previa del fichero para detectar
archivos vacíos, corruptos o con formatos incompatibles.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import zipfile
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# Por defecto, deshabilitar CUDA para evitar bloqueos en import torch.
# _detect_device() sobreescribe esto si el usuario pide --device cuda|auto.
# _CUDA_ENV_INJECTED distingue este valor por defecto de un "" exportado por el usuario.
_CUDA_ENV_INJECTED = "CUDA_VISIBLE_DEVICES" not in os.environ
if _CUDA_ENV_INJECTED:
    os.environ["CUDA_VISIBLE_DEVICES"] = ""

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]

# ---------------------------------------------------------------------------
# Conjuntos de extensiones por motor
# ---------------------------------------------------------------------------

DOCLING_EXTENSIONS: frozenset[str] = frozenset(
    {
        ".pdf",
        ".docx",
        ".pptx",
        ".xlsx",
        ".csv",
        ".html",
        ".htm",
        ".epub",
        ".png",
        ".jpg",
        ".jpeg",
        ".tiff",
        ".bmp",
        ".webp",
        ".eml",
        ".msg",
        ".tex",
        ".latex",
        ".wav",
        ".mp3",
    }
)

MARKITDOWN_EXTENSIONS: frozenset[str] = frozenset(
    {".pdf", ".docx", ".pptx", ".xlsx", ".xls", ".csv", ".epub", ".html", ".htm", ".msg"}
)

PANDOC_EXTENSIONS: frozenset[str] = frozenset({".doc", ".odt", ".rst", ".tex", ".latex"})

ENGINE_EXTENSIONS: dict[str, frozenset[str]] = {
    "docling": DOCLING_EXTENSIONS,
    "markitdown": MARKITDOWN_EXTENSIONS,
    "pandoc": PANDOC_EXTENSIONS,
}

CONVERTIBLE_EXTENSIONS: frozenset[str] = (
    DOCLING_EXTENSIONS | MARKITDOWN_EXTENSIONS | PANDOC_EXTENSIONS
)

_ZIP_BASED_EXTENSIONS: frozenset[str] = frozenset({".docx", ".pptx", ".xlsx", ".epub"})
_AUDIO_EXTENSIONS: frozenset[str] = frozenset({".wav", ".mp3"})

_IMAGE_HEADERS: dict[str, bytes] = {
    ".png": b"\x89PNG",
    ".jpg": b"\xff\xd8\xff",
    ".jpeg": b"\xff\xd8\xff",
    ".bmp": b"BM",
    ".webp": b"RIFF",
}

INSTALL_INSTRUCTIONS: dict[str, str] = {
    "docling": "  pip install docling",
    "markitdown": "  pip install markitdown",
    "pandoc": (
        "  Windows: winget install JohnMacFarlane.Pandoc\n"
        "  macOS:   brew install pandoc\n"
        "  Linux:   sudo apt install pandoc"
    ),
}

# ---------------------------------------------------------------------------
# Opciones de conversión
# ---------------------------------------------------------------------------


@dataclass
class ConvertOptions:
    """Agrupa todas las opciones de CLI relevantes para la conversión."""

    source: Path = field(default_factory=lambda: Path("."))
    engine: str = "docling"
    dry_run: bool = False
    validate_only: bool = False
    force: bool = False
    metadata: bool = False
    chunk: bool = False
    chunk_max_tokens: int = 512
    ocr: bool = True
    ocr_engine: str = "auto"
    ocr_lang: list[str] = field(default_factory=lambda: ["es", "en"])
    table_mode: str = "accurate"
    image_export: str = "placeholder"
    pdf_backend: str = "docling-parse"
    timeout: int = 300
    device: str = "cpu"
    num_threads: int = 4
    flash_attention: bool = False
    batch_size: int = 1
    workers: int = 1


# ---------------------------------------------------------------------------
# Detección de disponibilidad
# ---------------------------------------------------------------------------


def docling_available() -> bool:
    """Devuelve True si el paquete docling está instalado."""
    return importlib.util.find_spec("docling") is not None


def markitdown_available() -> bool:
    """Devuelve True si el paquete markitdown está instalado."""
    return importlib.util.find_spec("markitdown") is not None


def pandoc_available() -> bool:
    """Devuelve True si pandoc está disponible en el PATH."""
    return shutil.which("pandoc") is not None


def engine_available(engine: str) -> bool:
    """Devuelve True si el motor solicitado está disponible."""
    checkers: dict[str, object] = {
        "docling": docling_available,
        "markitdown": markitdown_available,
        "pandoc": pandoc_available,
    }
    checker = checkers.get(engine)
    if not callable(checker):
        return False
    return bool(checker())


# ---------------------------------------------------------------------------
# Detección de dispositivo (CPU / CUDA)
# ---------------------------------------------------------------------------


def _cuda_available() -> bool:
    """Detecta CUDA sin importar torch (evita hang de 27min en Python 3.14)."""
    nvidia_smi = shutil.which("nvidia-smi")
    if nvidia_smi is None:
        return False
    try:
        result = subprocess.run(
            [nvidia_smi, "--query-gpu=name", "--format=csv,noheader"],
            capture_output=True,
            timeout=5,
        )
        return result.returncode == 0 and len(result.stdout.strip()) > 0
    except (subprocess.TimeoutExpired, OSError):
        return False


def _detect_device(requested: str) -> str:
    """Resuelve el dispositivo efectivo y configura CUDA_VISIBLE_DEVICES.

    Args:
        requested: ``"cpu"``, ``"cuda"`` o ``"auto"``

    Returns:
        ``"cpu"`` o ``"cuda"`` (resuelto).
    """
    if requested == "cpu":
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
        return "cpu"

    if requested == "auto":
        existing = os.environ.get("CUDA_VISIBLE_DEVICES")
        if existing is not None and not (_CUDA_ENV_INJECTED and existing == ""):
            if existing == "":
                return "cpu"
            return "cuda"
        if _cuda_available():
            os.environ.pop("CUDA_VISIBLE_DEVICES", None)
            print("  INFO    CUDA detectado — usando GPU.", flush=True)
            return "cuda"
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
        print("  INFO    CUDA no disponible — usando CPU.", flush=True)
        return "cpu"

    # requested == "cuda"
    if not _cuda_available():
        print("ERROR: --device cuda pero nvidia-smi no encontrado o no responde.")
        sys.exit(1)
    os.environ.pop("CUDA_VISIBLE_DEVICES", None)
    return "cuda"


# ---------------------------------------------------------------------------
# Validación previa
# ---------------------------------------------------------------------------


def _validate_header(source_file: Path, expected: bytes, label: str) -> tuple[bool, str]:
    """Valida que el fichero comience con la cabecera esperada."""
    try:
        with source_file.open("rb") as f:
            header = f.read(len(expected))
        if not header.startswith(expected):
            return False, f"cabecera {label} inválida (fichero corrupto)"
    except OSError as exc:
        return False, f"no se puede leer cabecera {label}: {exc}"
    return True, ""


def validate_file(source_file: Path) -> tuple[bool, str]:
    """Validación previa del fichero antes de intentar la conversión."""
    try:
        size = source_file.stat().st_size
    except OSError as exc:
        return False, f"no se puede leer: {exc}"

    if size == 0:
        return False, "fichero vacío (0 bytes)"

    ext = source_file.suffix.lower()

    if ext in _ZIP_BASED_EXTENSIONS and not zipfile.is_zipfile(source_file):
        return False, f"archivo ZIP inválido (formato {ext} corrupto o no reconocido)"

    if ext == ".pdf":
        return _validate_header(source_file, b"%PDF-", "PDF")

    expected = _IMAGE_HEADERS.get(ext)
    if expected:
        return _validate_header(source_file, expected, f"imagen {ext}")

    if ext in _AUDIO_EXTENSIONS and size < 1024:
        return False, f"fichero de audio demasiado pequeño ({size} bytes, mínimo 1KB)"

    return True, ""


# ---------------------------------------------------------------------------
# Recolección de ficheros
# ---------------------------------------------------------------------------


def collect_files(source: Path, engine: str = "docling") -> list[Path]:
    """Devuelve ficheros convertibles bajo source para el motor indicado."""
    extensions = ENGINE_EXTENSIONS.get(engine, CONVERTIBLE_EXTENSIONS)
    if source.is_file():
        return [source] if source.suffix.lower() in extensions else []
    return sorted(
        p
        for p in source.rglob("*")
        if p.is_file()
        and p.suffix.lower() in extensions
        and "md" not in p.relative_to(source).parts[:-1]
    )


# ---------------------------------------------------------------------------
# Rutas de salida
# ---------------------------------------------------------------------------


def output_path(source_file: Path, source_root: Path, md_root: Path) -> Path:
    """Calcula la ruta de salida en md_root reflejando la estructura relativa."""
    relative = source_file.relative_to(source_root)
    return md_root / relative.with_suffix(".md")


# ---------------------------------------------------------------------------
# Metadatos frontmatter
# ---------------------------------------------------------------------------


def _docling_version() -> str:
    """Versión instalada de docling (el paquete no expone ``__version__``)."""
    try:
        return importlib.metadata.version("docling")
    except importlib.metadata.PackageNotFoundError:
        return "unknown"


def _build_metadata_basic(source_file: Path, engine: str) -> dict[str, object]:
    """Metadatos básicos disponibles para cualquier motor."""
    return {
        "source": str(source_file.name),
        "engine": engine,
        "converted_at": datetime.now(tz=UTC).strftime("%Y-%m-%dT%H:%M:%S"),
    }


def _format_frontmatter(metadata: dict[str, object]) -> str:
    """Serializa metadatos como frontmatter YAML."""
    lines = ["---"]
    for key, value in metadata.items():
        if isinstance(value, bool):
            lines.append(f"{key}: {'true' if value else 'false'}")
        elif isinstance(value, (int, float)):
            lines.append(f"{key}: {value}")
        else:
            lines.append(f'{key}: "{value}"')
    lines.append("---\n")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Motor: Docling
# ---------------------------------------------------------------------------


def _convert_with_docling(
    source_file: Path,
    out: Path,
    md_root: Path,
    rel: str,
    *,
    options: ConvertOptions,
) -> bool:
    """Convierte un documento a Markdown usando Docling."""
    if options.dry_run:
        print(f"  DRY-RUN {rel} -> md/{out.relative_to(md_root)}")
        return True

    if not docling_available():
        inst = INSTALL_INSTRUCTIONS["docling"].strip()
        print(f"  ERROR   {rel}: docling no instalado ({inst})")
        return False

    try:
        converter = _build_docling_converter(options)
        print(f"  CONV    {rel} ...", end="", flush=True)
        result = converter.convert(str(source_file))
        doc = result.document
        md_content: str = doc.export_to_markdown()

        if options.metadata:
            metadata = _build_metadata_basic(source_file, "docling")
            metadata["engine_version"] = _docling_version()
            metadata["title"] = getattr(doc, "name", source_file.stem) or source_file.stem
            md_content = _format_frontmatter(metadata) + md_content

        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md_content, encoding="utf-8")
        print(f" OK -> md/{out.relative_to(md_root)}", flush=True)

        if options.chunk:
            _run_chunking(doc, out, md_root, rel)

        return True
    except Exception as exc:  # noqa: BLE001
        print(f" ERROR: {exc}", flush=True)
        out.unlink(missing_ok=True)
        return False


_docling_converter_cache: dict[str, Any] = {}


def _build_docling_converter(options: ConvertOptions) -> Any:
    """Construye un DocumentConverter de Docling con la configuración indicada (cacheado)."""
    cache_key = (
        f"{options.ocr}|{options.ocr_engine}|{options.table_mode}|{options.pdf_backend}"
        f"|{options.device}|{options.num_threads}|{options.flash_attention}"
    )
    if cache_key in _docling_converter_cache:
        return _docling_converter_cache[cache_key]

    print("  INFO    Cargando motor docling (puede tardar unos minutos)...", flush=True)
    from docling.document_converter import DocumentConverter  # noqa: PLC0415

    try:
        from docling.datamodel.base_models import InputFormat  # noqa: PLC0415
        from docling.datamodel.pipeline_options import (  # noqa: PLC0415
            PdfPipelineOptions,
        )
        from docling.document_converter import PdfFormatOption  # noqa: PLC0415
    except ImportError:
        converter = DocumentConverter()
        _docling_converter_cache[cache_key] = converter
        print("  INFO    Motor docling listo.", flush=True)
        return converter

    try:
        from docling.datamodel.pipeline_options import (  # noqa: PLC0415
            TableStructureOptions,
        )

        table_mode_value = _resolve_table_mode(options.table_mode)
        table_opts = TableStructureOptions(mode=table_mode_value)
    except ImportError:
        table_opts = None

    ocr_opts = _resolve_ocr_options(options)

    try:
        from docling.datamodel.accelerator_options import (  # noqa: PLC0415
            AcceleratorOptions,
        )

        accel_opts = AcceleratorOptions(
            device=options.device,
            num_threads=options.num_threads,
            cuda_use_flash_attention2=options.flash_attention,
        )
    except ImportError:
        accel_opts = None

    pipeline_kwargs: dict[str, object] = {
        "do_ocr": options.ocr,
        "do_table_structure": True,
    }
    if table_opts is not None:
        pipeline_kwargs["table_structure_options"] = table_opts
    if ocr_opts is not None:
        pipeline_kwargs["ocr_options"] = ocr_opts
    if accel_opts is not None:
        pipeline_kwargs["accelerator_options"] = accel_opts

    pipeline_options = PdfPipelineOptions(**pipeline_kwargs)  # type: ignore[arg-type]

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options),
        },
    )
    _docling_converter_cache[cache_key] = converter
    print("  INFO    Motor docling listo.", flush=True)
    return converter


def _resolve_table_mode(mode_str: str) -> Any:
    """Resuelve el string del CLI al enum TableFormerMode."""
    try:
        from docling.datamodel.pipeline_options import TableFormerMode  # noqa: PLC0415

        modes = {"accurate": TableFormerMode.ACCURATE, "fast": TableFormerMode.FAST}
        return modes.get(mode_str, TableFormerMode.ACCURATE)
    except ImportError:
        return None


def _resolve_ocr_options(options: ConvertOptions) -> Any:
    """Resuelve las opciones de OCR según el motor elegido."""
    if not options.ocr:
        return None

    engine = options.ocr_engine
    langs = options.ocr_lang

    try:
        if engine == "easyocr":
            from docling.datamodel.pipeline_options import EasyOcrOptions  # noqa: PLC0415

            return EasyOcrOptions(lang=langs, use_gpu=(options.device == "cuda"))
        elif engine == "tesseract":
            from docling.datamodel.pipeline_options import TesseractOcrOptions  # noqa: PLC0415

            return TesseractOcrOptions(lang=langs)
        elif engine == "rapidocr":
            from docling.datamodel.pipeline_options import RapidOcrOptions  # noqa: PLC0415

            return RapidOcrOptions()
    except ImportError:
        pass
    return None


def _run_chunking(
    doc: Any,
    out: Path,
    md_root: Path,
    rel: str,
) -> None:
    """Genera chunks del documento con HybridChunker."""
    try:
        from docling.chunking import HybridChunker  # type: ignore[attr-defined]  # noqa: PLC0415
    except ImportError:
        print(f"  CHUNK   {rel}: HybridChunker no disponible (pip install docling)")
        return

    try:
        chunker = HybridChunker()
        chunks = list(chunker.chunk(doc))
    except Exception as exc:  # noqa: BLE001
        print(f"  CHUNK   {rel}: error al chunking: {exc}")
        return

    chunks_dir = out.parent / "chunks" / out.stem
    chunks_dir.mkdir(parents=True, exist_ok=True)

    manifest: list[dict[str, object]] = []
    for i, chunk in enumerate(chunks, 1):
        chunk_text = getattr(chunk, "text", str(chunk))
        chunk_file = chunks_dir / f"{i:03d}.md"
        chunk_file.write_text(chunk_text, encoding="utf-8")
        manifest.append(
            {
                "id": i,
                "file": chunk_file.name,
                "preview": chunk_text[:80],
                "chars": len(chunk_text),
            }
        )

    manifest_file = chunks_dir / "_manifest.json"
    manifest_file.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    chunks_rel = chunks_dir.relative_to(md_root)
    print(f"  CHUNK   {rel} -> md/{chunks_rel}/ ({len(chunks)} chunks)")


# ---------------------------------------------------------------------------
# Motor: MarkItDown
# ---------------------------------------------------------------------------


def _convert_with_markitdown(
    source_file: Path,
    out: Path,
    md_root: Path,
    rel: str,
    *,
    options: ConvertOptions,
) -> bool:
    """Convierte un documento a Markdown usando markitdown."""
    if options.dry_run:
        print(f"  DRY-RUN {rel} -> md/{out.relative_to(md_root)}")
        return True

    if not markitdown_available():
        print(
            f"  ERROR   {rel}: markitdown no instalado"
            f" ({INSTALL_INSTRUCTIONS['markitdown'].strip()})"
        )
        return False

    from markitdown import MarkItDown  # noqa: PLC0415

    try:
        result = MarkItDown().convert(str(source_file))
        md_content: str = result.text_content

        if options.metadata:
            metadata = _build_metadata_basic(source_file, "markitdown")
            md_content = _format_frontmatter(metadata) + md_content

        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md_content, encoding="utf-8")
        print(f"  OK      {rel} -> md/{out.relative_to(md_root)}")
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"  ERROR   {rel}: {exc}")
        out.unlink(missing_ok=True)
        return False


# ---------------------------------------------------------------------------
# Motor: Pandoc
# ---------------------------------------------------------------------------


def _convert_with_pandoc(
    source_file: Path,
    out: Path,
    md_root: Path,
    rel: str,
    *,
    options: ConvertOptions,
) -> bool:
    """Convierte un documento a Markdown usando pandoc."""
    if options.dry_run:
        print(f"  DRY-RUN {rel} -> md/{out.relative_to(md_root)}")
        return True

    if not pandoc_available():
        print(f"  ERROR   {rel}: pandoc no encontrado en el PATH\n{INSTALL_INSTRUCTIONS['pandoc']}")
        return False

    out.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["pandoc", str(source_file), "-o", str(out), "--wrap=none"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  ERROR   {rel}: {result.stderr.strip()}")
        out.unlink(missing_ok=True)
        return False

    if options.metadata:
        try:
            existing = out.read_text(encoding="utf-8")
            metadata = _build_metadata_basic(source_file, "pandoc")
            out.write_text(_format_frontmatter(metadata) + existing, encoding="utf-8")
        except OSError:
            pass

    print(f"  OK      {rel} -> md/{out.relative_to(md_root)}")
    return True


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

_ENGINE_CONVERTERS = {
    "docling": _convert_with_docling,
    "markitdown": _convert_with_markitdown,
    "pandoc": _convert_with_pandoc,
}


def convert_file(
    source_file: Path,
    source_root: Path,
    md_root: Path,
    *,
    options: ConvertOptions | None = None,
) -> bool:
    """Convierte source_file a Markdown en md_root. Devuelve True si tuvo éxito u omitió."""
    if options is None:
        options = ConvertOptions()

    out = output_path(source_file, source_root, md_root)
    rel = str(source_file.relative_to(source_root))

    if out.exists() and not options.force:
        print(f"  OMITIR  {rel} -> md/{out.relative_to(md_root)} (ya existe)", flush=True)
        return True

    valid, reason = validate_file(source_file)
    if not valid:
        print(f"  INVÁLID {rel}: {reason}", flush=True)
        return False

    extensions = ENGINE_EXTENSIONS.get(options.engine, frozenset())
    if source_file.suffix.lower() not in extensions:
        print(
            f"  NOSOPOR {rel}: formato '{source_file.suffix}' no soportado por"
            f" motor '{options.engine}'"
        )
        return False

    converter = _ENGINE_CONVERTERS[options.engine]
    return converter(source_file, out, md_root, rel, options=options)


# ---------------------------------------------------------------------------
# Conversión por lotes (docling)
# ---------------------------------------------------------------------------


def _convert_batch_docling(
    files: list[Path],
    source_root: Path,
    md_root: Path,
    *,
    options: ConvertOptions,
) -> int:
    """Convierte ficheros con docling convert_all(). Retorna conteo de fallos."""
    to_convert, failures = _prefilter_files(files, source_root, md_root, options=options)

    if not to_convert or options.dry_run:
        return failures

    converter = _build_docling_converter(options)
    ctx = _batch_context(options) if options.batch_size > 1 or options.workers > 1 else None
    source_paths = [str(f) for f in to_convert]

    if ctx is not None:
        ctx.__enter__()
    try:
        results = converter.convert_all(source_paths, raises_on_error=False)
        for i, result in enumerate(results):
            ok = _process_batch_result(
                result,
                to_convert[i],
                source_root,
                md_root,
                options=options,
            )
            if not ok:
                failures += 1
    finally:
        if ctx is not None:
            ctx.__exit__(None, None, None)

    return failures


def _prefilter_files(
    files: list[Path],
    source_root: Path,
    md_root: Path,
    *,
    options: ConvertOptions,
) -> tuple[list[Path], int]:
    """Filtra ficheros antes del batch: OMITIR, DRY-RUN, INVÁLID, NOSOPOR."""
    extensions = ENGINE_EXTENSIONS.get(options.engine, frozenset())
    to_convert: list[Path] = []
    failures = 0

    for f in files:
        out = output_path(f, source_root, md_root)
        rel = str(f.relative_to(source_root))

        if out.exists() and not options.force:
            print(f"  OMITIR  {rel} -> md/{out.relative_to(md_root)} (ya existe)", flush=True)
            continue

        if options.dry_run:
            print(f"  DRY-RUN {rel} -> md/{out.relative_to(md_root)}", flush=True)
            continue

        valid, reason = validate_file(f)
        if not valid:
            print(f"  INVÁLID {rel}: {reason}", flush=True)
            failures += 1
            continue

        if f.suffix.lower() not in extensions:
            print(
                f"  NOSOPOR {rel}: formato '{f.suffix}' no soportado por motor '{options.engine}'",
                flush=True,
            )
            failures += 1
            continue

        to_convert.append(f)

    return to_convert, failures


def _process_batch_result(
    result: Any,
    src_file: Path,
    source_root: Path,
    md_root: Path,
    *,
    options: ConvertOptions,
) -> bool:
    """Procesa un resultado individual de convert_all(). Retorna True si OK."""
    out = output_path(src_file, source_root, md_root)
    rel = str(src_file.relative_to(source_root))

    if not _is_conversion_success(result):
        err = getattr(result, "errors", ["unknown error"])
        print(f"  CONV    {rel} ... ERROR: {err}", flush=True)
        return False

    doc = result.document
    md_content: str = doc.export_to_markdown()

    if options.metadata:
        metadata = _build_metadata_basic(src_file, "docling")
        metadata["engine_version"] = _docling_version()
        metadata["title"] = getattr(doc, "name", src_file.stem) or src_file.stem
        md_content = _format_frontmatter(metadata) + md_content

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md_content, encoding="utf-8")
    print(f"  CONV    {rel} ... OK -> md/{out.relative_to(md_root)}", flush=True)

    if options.chunk:
        _run_chunking(doc, out, md_root, rel)

    return True


def _is_conversion_success(result: Any) -> bool:
    """Comprueba si un resultado de convert_all() fue exitoso."""
    try:
        from docling.datamodel.base_models import ConversionStatus  # noqa: PLC0415

        return bool(getattr(result, "status", None) == ConversionStatus.SUCCESS)
    except ImportError:
        return True


def _batch_context(options: ConvertOptions) -> Any:
    """Crea context manager de BatchConcurrencySettings si disponible."""
    try:
        from docling.datamodel.settings import (  # noqa: PLC0415
            BatchConcurrencySettings,
            scoped,
        )

        settings = BatchConcurrencySettings(
            doc_batch_size=options.batch_size,
            doc_batch_concurrency=options.workers,
        )
        return scoped(perf=settings)
    except ImportError:
        return None


# ---------------------------------------------------------------------------
# Resumen de validación
# ---------------------------------------------------------------------------


def _validate_only_report(files: list[Path], source_root: Path, options: ConvertOptions) -> int:
    """Ejecuta solo validación previa sin convertir. Retorna 0 si todo OK."""
    engine_ok = engine_available(options.engine)
    errors = 0

    print(f"=== Validación previa ({len(files)} fichero(s), motor: {options.engine}) ===\n")
    print(f"  Motor {options.engine}: {'OK' if engine_ok else 'NO INSTALADO'}")
    print()

    for f in files:
        rel = str(f.relative_to(source_root))

        valid, reason = validate_file(f)
        if not valid:
            print(f"  INVÁLID {rel}: {reason}")
            errors += 1
            continue

        print(f"  OK      {rel}")

    print()
    if not engine_ok:
        print(
            f"  ⚠ Motor '{options.engine}' no instalado."
            f"\n  {INSTALL_INSTRUCTIONS.get(options.engine, '')}"
        )
        print()

    if errors:
        print(f"Validación completada: {errors} error(es) de {len(files)} fichero(s).")
        return 1
    print(f"Validación completada: {len(files)} fichero(s) listos para conversión.")
    return 0


def _print_validation_summary(files: list[Path], source_root: Path, *, dry_run: bool) -> None:
    """Muestra un resumen de ficheros que no superaron la validación previa."""
    if dry_run:
        return
    invalid = 0
    for f in files:
        ok, reason = validate_file(f)
        if not ok:
            invalid += 1
            rel = str(f.relative_to(source_root))
            print(f"  INVÁLID {rel}: {reason}")
    if invalid:
        print(f"  ({invalid} fichero(s) no superaron la validación previa)\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _parse_args(argv: list[str] | None = None) -> ConvertOptions:
    """Parsea argumentos CLI y devuelve ConvertOptions."""
    parser = argparse.ArgumentParser(
        description="Convierte documentos a Markdown (docling | markitdown | pandoc).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Motores disponibles:\n"
            "  docling    (default) -> PDF, DOCX, PPTX, XLSX, CSV, HTML, EPUB, imágenes,\n"
            "                         email, LaTeX, audio\n"
            "  markitdown           -> PDF, DOCX, PPTX, XLSX, XLS, CSV, EPUB, HTML, MSG\n"
            "  pandoc               -> DOC, ODT, RST, TEX/LATEX\n"
            "\nInstalación:\n"
            "  docling:    pip install docling\n"
            "  markitdown: pip install markitdown\n"
            "  pandoc:     winget install JohnMacFarlane.Pandoc (o brew/apt)\n"
            "\nValidación previa: tamaño > 0, integridad ZIP, cabecera PDF/imagen, audio > 1KB.\n"
            "Los ficheros convertidos se depositan en <origen>/md/ (estructura reflejada)."
        ),
    )
    parser.add_argument("source", type=Path, help="Fichero o directorio a convertir.")
    parser.add_argument(
        "--engine",
        choices=["docling", "markitdown", "pandoc"],
        default="docling",
        help="Motor de conversión (default: docling).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Muestra qué se convertiría sin ejecutar conversión.",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Solo ejecuta validación previa (extensiones, integridad). No convierte.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-convierte aunque ya exista el .md de salida.",
    )
    parser.add_argument(
        "--metadata",
        action="store_true",
        help="Incluye frontmatter YAML con metadatos extraídos.",
    )
    parser.add_argument(
        "--chunk",
        action="store_true",
        help="Genera ficheros chunkeados para RAG (solo docling).",
    )
    parser.add_argument(
        "--chunk-max-tokens",
        type=int,
        default=512,
        help="Tamaño máximo de chunk en tokens (default: 512).",
    )
    parser.add_argument(
        "--ocr",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Habilita/deshabilita OCR (default: habilitado).",
    )
    parser.add_argument(
        "--ocr-engine",
        choices=["auto", "easyocr", "tesseract", "rapidocr"],
        default="auto",
        help="Motor OCR para docling (default: auto).",
    )
    parser.add_argument(
        "--ocr-lang",
        default="es,en",
        help="Idiomas OCR separados por coma (default: es,en).",
    )
    parser.add_argument(
        "--table-mode",
        choices=["accurate", "fast"],
        default="accurate",
        help="Modo de extracción de tablas para docling (default: accurate).",
    )
    parser.add_argument(
        "--image-export",
        choices=["placeholder", "embedded", "referenced"],
        default="placeholder",
        help="Modo de exportación de imágenes (default: placeholder).",
    )
    parser.add_argument(
        "--pdf-backend",
        choices=["docling-parse", "pypdfium2"],
        default="docling-parse",
        help="Backend PDF para docling (default: docling-parse).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Timeout por documento en segundos (default: 300).",
    )
    parser.add_argument(
        "--device",
        choices=["cpu", "cuda", "auto"],
        default="cpu",
        help="Dispositivo: cpu (default), cuda (GPU NVIDIA), auto (detectar).",
    )
    parser.add_argument(
        "--num-threads",
        type=int,
        default=4,
        help="Hilos CPU para docling AcceleratorOptions (default: 4).",
    )
    parser.add_argument(
        "--flash-attention",
        action="store_true",
        help="Habilita Flash Attention 2 (requiere GPU Ampere+).",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1,
        help="Documentos por lote en docling convert_all (default: 1).",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Hilos de concurrencia por lote en docling (default: 1).",
    )

    args = parser.parse_args(argv)

    if args.chunk and args.engine != "docling":
        parser.error("--chunk solo funciona con --engine docling")
    if args.flash_attention and args.device == "cpu":
        parser.error("--flash-attention requiere --device cuda o --device auto")
    if args.batch_size > 1 and args.engine != "docling":
        parser.error("--batch-size >1 solo funciona con --engine docling")
    if args.workers > 1 and args.engine != "docling":
        parser.error("--workers >1 solo funciona con --engine docling")

    return ConvertOptions(
        source=args.source.resolve(),
        engine=args.engine,
        dry_run=args.dry_run,
        validate_only=args.validate_only,
        force=args.force,
        metadata=args.metadata,
        chunk=args.chunk,
        chunk_max_tokens=args.chunk_max_tokens,
        ocr=args.ocr,
        ocr_engine=args.ocr_engine,
        ocr_lang=[lang.strip() for lang in args.ocr_lang.split(",")],
        table_mode=args.table_mode,
        image_export=args.image_export,
        pdf_backend=args.pdf_backend,
        timeout=args.timeout,
        device=args.device,
        num_threads=args.num_threads,
        flash_attention=args.flash_attention,
        batch_size=args.batch_size,
        workers=args.workers,
    )


def main(argv: list[str] | None = None) -> int:
    """Convierte documentos no-Markdown a Markdown con el motor elegido."""
    options = _parse_args(argv)
    source = options.source

    if not source.exists():
        print(f"ERROR: El origen '{source}' no existe.")
        return 1

    source_root = source if source.is_dir() else source.parent

    if options.validate_only:
        files = collect_files(source, options.engine)
        if not files:
            print(f"No se encontraron ficheros convertibles en: {source} (motor: {options.engine})")
            return 0
        return _validate_only_report(files, source_root, options)

    md_root = source_root / "md"

    if options.engine == "docling" and not options.dry_run:
        options.device = _detect_device(options.device)

    if not engine_available(options.engine) and not options.dry_run:
        print(
            f"ERROR: Motor '{options.engine}' no disponible.\n"
            f"{INSTALL_INSTRUCTIONS.get(options.engine, '')}\n"
            f"  Alternativas: --engine "
            + " | --engine ".join(e for e in ENGINE_EXTENSIONS if e != options.engine)
        )
        return 1

    files = collect_files(source, options.engine)

    if not files:
        print(f"No se encontraron ficheros convertibles en: {source} (motor: {options.engine})")
        return 0

    print(
        f"Convirtiendo {len(files)} fichero(s) con motor '{options.engine}' -> {md_root}",
        flush=True,
    )
    _print_validation_summary(files, source_root, dry_run=options.dry_run)

    if options.engine == "docling":
        failures = _convert_batch_docling(
            files,
            source_root,
            md_root,
            options=options,
        )
    else:
        failures = sum(
            1 for f in files if not convert_file(f, source_root, md_root, options=options)
        )

    if failures:
        print(f"\n{failures} error(es). Revisa la salida anterior.")
        return 1
    print(f"\nCompletado: {len(files)} convertido(s) en md/ (motor: {options.engine})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
