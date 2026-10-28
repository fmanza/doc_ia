"""Tests para scripts/convert_to_md.py — conversión de documentos a Markdown."""

from __future__ import annotations

import zipfile
from pathlib import Path
from unittest.mock import patch

import pytest
from scripts.convert_to_md import (
    DOCLING_EXTENSIONS,
    ENGINE_EXTENSIONS,
    MARKITDOWN_EXTENSIONS,
    PANDOC_EXTENSIONS,
    ConvertOptions,
    _cuda_available,
    _detect_device,
    _parse_args,
    _prefilter_files,
    _validate_only_report,
    collect_files,
    convert_file,
    main,
    output_path,
    validate_file,
)

# --- validate_file ---


def test_validate_empty_file(tmp_path: Path) -> None:
    f = tmp_path / "empty.pdf"
    f.write_bytes(b"")
    ok, reason = validate_file(f)
    assert not ok
    assert "vacío" in reason


def test_validate_valid_pdf(tmp_path: Path) -> None:
    f = tmp_path / "valid.pdf"
    f.write_bytes(b"%PDF-1.4 some content here")
    ok, _ = validate_file(f)
    assert ok


def test_validate_invalid_pdf_header(tmp_path: Path) -> None:
    f = tmp_path / "bad.pdf"
    f.write_bytes(b"NOT_A_PDF content")
    ok, reason = validate_file(f)
    assert not ok
    assert "PDF" in reason


def test_validate_valid_docx(tmp_path: Path) -> None:
    f = tmp_path / "valid.docx"
    with zipfile.ZipFile(f, "w") as zf:
        zf.writestr("content.xml", "<doc/>")
    ok, _ = validate_file(f)
    assert ok


def test_validate_invalid_docx(tmp_path: Path) -> None:
    f = tmp_path / "corrupt.docx"
    f.write_bytes(b"not a zip file at all")
    ok, reason = validate_file(f)
    assert not ok
    assert "ZIP inválido" in reason


def test_validate_valid_xlsx(tmp_path: Path) -> None:
    f = tmp_path / "valid.xlsx"
    with zipfile.ZipFile(f, "w") as zf:
        zf.writestr("sheet.xml", "<sheet/>")
    ok, _ = validate_file(f)
    assert ok


def test_validate_nonexistent_file(tmp_path: Path) -> None:
    f = tmp_path / "ghost.pdf"
    ok, reason = validate_file(f)
    assert not ok
    assert "no se puede leer" in reason


def test_validate_plain_text_file(tmp_path: Path) -> None:
    f = tmp_path / "readme.doc"
    f.write_bytes(b"some text content")
    ok, _ = validate_file(f)
    assert ok


def test_validate_valid_png(tmp_path: Path) -> None:
    f = tmp_path / "image.png"
    f.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
    ok, _ = validate_file(f)
    assert ok


def test_validate_invalid_png_header(tmp_path: Path) -> None:
    f = tmp_path / "bad.png"
    f.write_bytes(b"NOT_PNG_DATA")
    ok, reason = validate_file(f)
    assert not ok
    assert "imagen" in reason


def test_validate_valid_jpeg(tmp_path: Path) -> None:
    f = tmp_path / "photo.jpg"
    f.write_bytes(b"\xff\xd8\xff\xe0" + b"\x00" * 100)
    ok, _ = validate_file(f)
    assert ok


def test_validate_invalid_jpeg_header(tmp_path: Path) -> None:
    f = tmp_path / "bad.jpeg"
    f.write_bytes(b"NOT_JPEG_DATA")
    ok, reason = validate_file(f)
    assert not ok
    assert "imagen" in reason


def test_validate_audio_too_small(tmp_path: Path) -> None:
    f = tmp_path / "tiny.wav"
    f.write_bytes(b"RIFF" + b"\x00" * 50)
    ok, reason = validate_file(f)
    assert not ok
    assert "audio" in reason


def test_validate_audio_valid_size(tmp_path: Path) -> None:
    f = tmp_path / "sound.wav"
    f.write_bytes(b"RIFF" + b"\x00" * 2000)
    ok, _ = validate_file(f)
    assert ok


# --- collect_files ---


def test_collect_files_single_file(tmp_path: Path) -> None:
    f = tmp_path / "doc.pdf"
    f.write_bytes(b"%PDF-1.4")
    result = collect_files(f, "docling")
    assert result == [f]


def test_collect_files_non_convertible(tmp_path: Path) -> None:
    f = tmp_path / "readme.txt"
    f.write_text("hello", encoding="utf-8")
    result = collect_files(f, "docling")
    assert result == []


def test_collect_files_directory(tmp_path: Path) -> None:
    (tmp_path / "a.pdf").write_bytes(b"%PDF-1.4")
    (tmp_path / "b.docx").write_bytes(b"docx")
    (tmp_path / "c.txt").write_text("skip", encoding="utf-8")
    result = collect_files(tmp_path, "docling")
    extensions = {p.suffix for p in result}
    assert ".pdf" in extensions
    assert ".docx" in extensions
    assert ".txt" not in extensions


def test_collect_files_excludes_md_subfolder(tmp_path: Path) -> None:
    md_dir = tmp_path / "md"
    md_dir.mkdir()
    (md_dir / "converted.pdf").write_bytes(b"%PDF-1.4")
    (tmp_path / "source.pdf").write_bytes(b"%PDF-1.4")
    result = collect_files(tmp_path, "docling")
    names = [p.name for p in result]
    assert "source.pdf" in names
    assert "converted.pdf" not in names


def test_collect_files_nested_directory(tmp_path: Path) -> None:
    sub = tmp_path / "subdir"
    sub.mkdir()
    (sub / "deep.docx").write_bytes(b"docx")
    result = collect_files(tmp_path, "docling")
    assert len(result) == 1
    assert result[0].name == "deep.docx"


def test_collect_files_engine_filter(tmp_path: Path) -> None:
    (tmp_path / "doc.pdf").write_bytes(b"%PDF-1.4")
    (tmp_path / "img.png").write_bytes(b"\x89PNG")
    (tmp_path / "old.doc").write_bytes(b"doc content")

    docling_result = collect_files(tmp_path, "docling")
    assert any(p.suffix == ".png" for p in docling_result)
    assert not any(p.suffix == ".doc" for p in docling_result)

    pandoc_result = collect_files(tmp_path, "pandoc")
    assert any(p.suffix == ".doc" for p in pandoc_result)
    assert not any(p.suffix == ".png" for p in pandoc_result)


# --- output_path ---


def test_output_path_flat(tmp_path: Path) -> None:
    source_file = tmp_path / "doc.pdf"
    md_root = tmp_path / "md"
    result = output_path(source_file, tmp_path, md_root)
    assert result == md_root / "doc.md"


def test_output_path_nested(tmp_path: Path) -> None:
    sub = tmp_path / "a" / "b"
    source_file = sub / "deep.docx"
    md_root = tmp_path / "md"
    result = output_path(source_file, tmp_path, md_root)
    assert result == md_root / "a" / "b" / "deep.md"


# --- convert_file ---


def test_convert_file_skips_existing(tmp_path: Path) -> None:
    source_file = tmp_path / "doc.pdf"
    source_file.write_bytes(b"%PDF-1.4 content")
    md_root = tmp_path / "md"
    md_root.mkdir()
    out = md_root / "doc.md"
    out.write_text("already converted", encoding="utf-8")
    result = convert_file(source_file, tmp_path, md_root)
    assert result is True
    assert out.read_text(encoding="utf-8") == "already converted"


def test_convert_file_invalid_file(tmp_path: Path) -> None:
    source_file = tmp_path / "bad.pdf"
    source_file.write_bytes(b"")
    md_root = tmp_path / "md"
    result = convert_file(source_file, tmp_path, md_root)
    assert result is False


def test_convert_file_dry_run_docling(tmp_path: Path) -> None:
    source_file = tmp_path / "doc.pdf"
    source_file.write_bytes(b"%PDF-1.4 content")
    md_root = tmp_path / "md"
    opts = ConvertOptions(engine="docling", dry_run=True)
    result = convert_file(source_file, tmp_path, md_root, options=opts)
    assert result is True
    assert not (md_root / "doc.md").exists()


def test_convert_file_dry_run_markitdown(tmp_path: Path) -> None:
    source_file = tmp_path / "doc.pdf"
    source_file.write_bytes(b"%PDF-1.4 content")
    md_root = tmp_path / "md"
    opts = ConvertOptions(engine="markitdown", dry_run=True)
    result = convert_file(source_file, tmp_path, md_root, options=opts)
    assert result is True
    assert not (md_root / "doc.md").exists()


def test_convert_file_dry_run_pandoc(tmp_path: Path) -> None:
    source_file = tmp_path / "doc.odt"
    source_file.write_bytes(b"odt content")
    md_root = tmp_path / "md"
    opts = ConvertOptions(engine="pandoc", dry_run=True)
    result = convert_file(source_file, tmp_path, md_root, options=opts)
    assert result is True
    assert not (md_root / "doc.md").exists()


def test_convert_file_docling_not_installed(tmp_path: Path) -> None:
    source_file = tmp_path / "doc.pdf"
    source_file.write_bytes(b"%PDF-1.4 content")
    md_root = tmp_path / "md"
    opts = ConvertOptions(engine="docling")
    with patch("scripts.convert_to_md.docling_available", return_value=False):
        result = convert_file(source_file, tmp_path, md_root, options=opts)
    assert result is False


def test_convert_file_markitdown_not_installed(tmp_path: Path) -> None:
    source_file = tmp_path / "doc.pdf"
    source_file.write_bytes(b"%PDF-1.4 content")
    md_root = tmp_path / "md"
    opts = ConvertOptions(engine="markitdown")
    with patch("scripts.convert_to_md.markitdown_available", return_value=False):
        result = convert_file(source_file, tmp_path, md_root, options=opts)
    assert result is False


def test_convert_file_pandoc_not_installed(tmp_path: Path) -> None:
    source_file = tmp_path / "doc.odt"
    source_file.write_bytes(b"odt content")
    md_root = tmp_path / "md"
    opts = ConvertOptions(engine="pandoc")
    with patch("scripts.convert_to_md.pandoc_available", return_value=False):
        result = convert_file(source_file, tmp_path, md_root, options=opts)
    assert result is False


def test_convert_file_unsupported_format(tmp_path: Path) -> None:
    source_file = tmp_path / "doc.doc"
    source_file.write_bytes(b"doc content")
    md_root = tmp_path / "md"
    opts = ConvertOptions(engine="docling")
    result = convert_file(source_file, tmp_path, md_root, options=opts)
    assert result is False


def test_convert_file_force_reconvert(tmp_path: Path) -> None:
    source_file = tmp_path / "doc.odt"
    source_file.write_bytes(b"odt content")
    md_root = tmp_path / "md"
    md_root.mkdir()
    out = md_root / "doc.md"
    out.write_text("old", encoding="utf-8")
    opts = ConvertOptions(engine="pandoc", force=True, dry_run=True)
    result = convert_file(source_file, tmp_path, md_root, options=opts)
    assert result is True


# --- engine selection CLI ---


def test_parse_args_default_engine() -> None:
    opts = _parse_args(["some/path"])
    assert opts.engine == "docling"


def test_parse_args_explicit_engine() -> None:
    opts = _parse_args(["some/path", "--engine", "markitdown"])
    assert opts.engine == "markitdown"


def test_parse_args_chunk_requires_docling() -> None:
    with pytest.raises(SystemExit):
        _parse_args(["some/path", "--engine", "markitdown", "--chunk"])


def test_parse_args_chunk_with_docling() -> None:
    opts = _parse_args(["some/path", "--engine", "docling", "--chunk"])
    assert opts.chunk is True


def test_parse_args_metadata_flag() -> None:
    opts = _parse_args(["some/path", "--metadata"])
    assert opts.metadata is True


def test_parse_args_ocr_lang_split() -> None:
    opts = _parse_args(["some/path", "--ocr-lang", "fr,de,en"])
    assert opts.ocr_lang == ["fr", "de", "en"]


def test_parse_args_no_ocr() -> None:
    opts = _parse_args(["some/path", "--no-ocr"])
    assert opts.ocr is False


# --- extension sets ---


def test_engine_extensions_keys() -> None:
    assert set(ENGINE_EXTENSIONS.keys()) == {"docling", "markitdown", "pandoc"}


def test_docling_covers_markitdown_formats() -> None:
    covered = MARKITDOWN_EXTENSIONS - {".xls"}
    assert covered.issubset(DOCLING_EXTENSIONS)


def test_pandoc_has_unique_formats() -> None:
    unique = PANDOC_EXTENSIONS - DOCLING_EXTENSIONS
    assert ".doc" in unique
    assert ".odt" in unique
    assert ".rst" in unique


# --- device detection ---


def test_detect_device_cpu_sets_env() -> None:
    with patch.dict("os.environ", {}, clear=False):
        result = _detect_device("cpu")
    assert result == "cpu"


def test_cuda_available_no_nvidia_smi() -> None:
    with patch("scripts.convert_to_md.shutil.which", return_value=None):
        assert _cuda_available() is False


def test_cuda_available_nvidia_smi_ok() -> None:
    import subprocess as sp

    fake_result = sp.CompletedProcess(args=[], returncode=0, stdout=b"NVIDIA RTX 4090\n")
    with (
        patch("scripts.convert_to_md.shutil.which", return_value="/usr/bin/nvidia-smi"),
        patch("scripts.convert_to_md.subprocess.run", return_value=fake_result),
    ):
        assert _cuda_available() is True


def test_cuda_available_nvidia_smi_timeout() -> None:
    import subprocess as sp

    with (
        patch("scripts.convert_to_md.shutil.which", return_value="/usr/bin/nvidia-smi"),
        patch("scripts.convert_to_md.subprocess.run", side_effect=sp.TimeoutExpired("x", 5)),
    ):
        assert _cuda_available() is False


def test_detect_device_auto_no_cuda() -> None:
    with (
        patch.dict("os.environ", {}, clear=False),
        patch("scripts.convert_to_md._cuda_available", return_value=False),
    ):
        result = _detect_device("auto")
    assert result == "cpu"


def test_detect_device_auto_with_cuda() -> None:
    with (
        patch.dict("os.environ", {}, clear=True),
        patch("scripts.convert_to_md._cuda_available", return_value=True),
    ):
        result = _detect_device("auto")
    assert result == "cuda"


def test_detect_device_cuda_not_available() -> None:
    with (
        patch("scripts.convert_to_md._cuda_available", return_value=False),
        pytest.raises(SystemExit),
    ):
        _detect_device("cuda")


def test_detect_device_respects_existing_env_empty() -> None:
    with (
        patch.dict("os.environ", {"CUDA_VISIBLE_DEVICES": ""}, clear=False),
        patch("scripts.convert_to_md._CUDA_ENV_INJECTED", False),
    ):
        result = _detect_device("auto")
    assert result == "cpu"


def test_detect_device_auto_ignores_import_default() -> None:
    """El "" que inyecta el módulo al importarse no debe impedir detectar la GPU."""
    with (
        patch.dict("os.environ", {"CUDA_VISIBLE_DEVICES": ""}, clear=False),
        patch("scripts.convert_to_md._CUDA_ENV_INJECTED", True),
        patch("scripts.convert_to_md._cuda_available", return_value=True),
    ):
        result = _detect_device("auto")
    assert result == "cuda"


def test_detect_device_respects_existing_env_set() -> None:
    with patch.dict("os.environ", {"CUDA_VISIBLE_DEVICES": "0"}, clear=False):
        result = _detect_device("auto")
    assert result == "cuda"


# --- CLI args nuevos ---


def test_parse_args_device_default() -> None:
    opts = _parse_args(["some/path"])
    assert opts.device == "cpu"


def test_parse_args_device_cuda() -> None:
    opts = _parse_args(["some/path", "--device", "cuda"])
    assert opts.device == "cuda"


def test_parse_args_device_auto() -> None:
    opts = _parse_args(["some/path", "--device", "auto"])
    assert opts.device == "auto"


def test_parse_args_batch_size() -> None:
    opts = _parse_args(["some/path", "--batch-size", "4"])
    assert opts.batch_size == 4


def test_parse_args_workers() -> None:
    opts = _parse_args(["some/path", "--workers", "2"])
    assert opts.workers == 2


def test_parse_args_num_threads() -> None:
    opts = _parse_args(["some/path", "--num-threads", "8"])
    assert opts.num_threads == 8


def test_parse_args_flash_attention() -> None:
    opts = _parse_args(["some/path", "--flash-attention", "--device", "cuda"])
    assert opts.flash_attention is True


def test_parse_args_flash_requires_gpu() -> None:
    with pytest.raises(SystemExit):
        _parse_args(["some/path", "--flash-attention"])


def test_parse_args_batch_requires_docling() -> None:
    with pytest.raises(SystemExit):
        _parse_args(["some/path", "--batch-size", "2", "--engine", "markitdown"])


def test_parse_args_workers_requires_docling() -> None:
    with pytest.raises(SystemExit):
        _parse_args(["some/path", "--workers", "2", "--engine", "pandoc"])


# --- ConvertOptions nuevos campos ---


def test_convert_options_new_fields_defaults() -> None:
    opts = ConvertOptions()
    assert opts.device == "cpu"
    assert opts.num_threads == 4
    assert opts.flash_attention is False
    assert opts.batch_size == 1
    assert opts.workers == 1


# --- prefilter ---


def test_prefilter_omits_existing(tmp_path: Path) -> None:
    src = tmp_path / "doc.pdf"
    src.write_bytes(b"%PDF-1.4 content")
    md_root = tmp_path / "md"
    md_root.mkdir()
    out = md_root / "doc.md"
    out.write_text("existing", encoding="utf-8")

    opts = ConvertOptions(source=tmp_path, engine="docling")
    to_convert, failures = _prefilter_files([src], tmp_path, md_root, options=opts)
    assert to_convert == []
    assert failures == 0


def test_prefilter_rejects_invalid(tmp_path: Path) -> None:
    src = tmp_path / "empty.pdf"
    src.write_bytes(b"")
    md_root = tmp_path / "md"

    opts = ConvertOptions(source=tmp_path, engine="docling")
    to_convert, failures = _prefilter_files([src], tmp_path, md_root, options=opts)
    assert to_convert == []
    assert failures == 1


def test_prefilter_dry_run(tmp_path: Path) -> None:
    src = tmp_path / "doc.pdf"
    src.write_bytes(b"%PDF-1.4 content")
    md_root = tmp_path / "md"

    opts = ConvertOptions(source=tmp_path, engine="docling", dry_run=True)
    to_convert, failures = _prefilter_files([src], tmp_path, md_root, options=opts)
    assert to_convert == []
    assert failures == 0


# --- validate-only ---


def test_parse_args_validate_only() -> None:
    opts = _parse_args(["some/path", "--validate-only"])
    assert opts.validate_only is True


def test_parse_args_validate_only_default_false() -> None:
    opts = _parse_args(["some/path"])
    assert opts.validate_only is False


def test_validate_only_report_all_valid(tmp_path: Path) -> None:
    f = tmp_path / "doc.pdf"
    f.write_bytes(b"%PDF-1.4 content")
    opts = ConvertOptions(engine="docling")
    with patch("scripts.convert_to_md.engine_available", return_value=True):
        result = _validate_only_report([f], tmp_path, opts)
    assert result == 0


def test_validate_only_report_invalid_file(tmp_path: Path) -> None:
    f = tmp_path / "bad.pdf"
    f.write_bytes(b"")
    opts = ConvertOptions(engine="docling")
    with patch("scripts.convert_to_md.engine_available", return_value=True):
        result = _validate_only_report([f], tmp_path, opts)
    assert result == 1


def test_validate_only_report_engine_not_installed(tmp_path: Path) -> None:
    f = tmp_path / "doc.pdf"
    f.write_bytes(b"%PDF-1.4 content")
    opts = ConvertOptions(engine="docling")
    with patch("scripts.convert_to_md.engine_available", return_value=False):
        result = _validate_only_report([f], tmp_path, opts)
    assert result == 0


def test_validate_only_does_not_create_output(tmp_path: Path) -> None:
    f = tmp_path / "doc.pdf"
    f.write_bytes(b"%PDF-1.4 content")
    with (
        patch("scripts.convert_to_md.engine_available", return_value=True),
        patch("scripts.convert_to_md._detect_device", return_value="cpu"),
    ):
        result = main(["--validate-only", "--engine", "markitdown", str(tmp_path)])
    assert result == 0
    assert not (tmp_path / "md").exists()


def test_main_validate_only_no_files(tmp_path: Path) -> None:
    empty = tmp_path / "empty_dir"
    empty.mkdir()
    result = main(["--validate-only", "--engine", "markitdown", str(empty)])
    assert result == 0
