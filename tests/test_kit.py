"""Tests de scripts/kit.py: sobre un doc_ia y un destino temporales, sin red."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from scripts.kit import KIT_DIR, KitError, check, main, parse_manifest, sha256, sync

ROOT = Path(__file__).resolve().parents[1]


def test_digest_ignores_line_endings_but_not_binary(tmp_path: Path) -> None:
    lf, crlf = tmp_path / "lf.md", tmp_path / "crlf.md"
    lf.write_bytes(b"a\nb\n")
    crlf.write_bytes(b"a\r\nb\r\n")
    assert sha256(lf) == sha256(crlf)
    bin_lf, bin_crlf = tmp_path / "a.bin", tmp_path / "b.bin"
    bin_lf.write_bytes(b"\x00a\nb")
    bin_crlf.write_bytes(b"\x00a\r\nb")
    assert sha256(bin_lf) != sha256(bin_crlf)


def test_checkout_with_other_line_endings_is_not_an_edit(tmp_path: Path) -> None:
    """git puede devolver el kit con LF o CRLF en otro equipo: no es una edición local."""
    src, dest = _doc_ia(tmp_path), _dest(tmp_path)
    (src / "scripts/doc_trace.py").write_bytes(b"print('v1')\r\nx = 1\r\n")
    sync(src, dest)
    (dest / ".doc_ia/scripts/doc_trace.py").write_bytes(b"print('v1')\nx = 1\n")
    assert check(dest).conflicts[:1] != [(".doc_ia/scripts/doc_trace.py", "editado en el destino")]
    assert sync(src, dest).conflicts == []


MANIFEST = """# prueba
[metodologia]
pyproject.toml
.github/prompts/document_project.prompt.md
scripts/doc_trace.py

[lanzadores]
.github/templates/kit/documentar.command.md -> .claude/commands/documentar.md

[instancia]
.github/templates/kit/DOCUMENTAR.template.md -> DOCUMENTAR.md
"""


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _doc_ia(tmp_path: Path, version: str = "9.9.0") -> Path:
    src = tmp_path / "doc_ia"
    _write(src / ".github/kit/MANIFEST.txt", MANIFEST)
    _write(src / "pyproject.toml", f'[project]\nname = "doc_ia"\nversion = "{version}"\n')
    _write(src / ".github/prompts/document_project.prompt.md", "# prompt v1\n")
    _write(src / "scripts/doc_trace.py", "print('v1')\n")
    _write(src / ".github/templates/kit/documentar.command.md", "# /documentar\n")
    _write(
        src / ".github/templates/kit/DOCUMENTAR.template.md",
        "<!--\nPLANTILLA\n-->\n# Cómo documentar {proyecto}\n",
    )
    return src


def _dest(tmp_path: Path) -> Path:
    dest = tmp_path / "VG"
    _write(dest / "mkdocs.yml", "site_name: MVG — Prueba\n")
    return dest


def _lock(dest: Path) -> dict[str, object]:
    data: dict[str, object] = json.loads(
        (dest / KIT_DIR / "kit.lock.json").read_text(encoding="utf-8")
    )
    return data


def test_install_copies_methodology_launchers_and_instance(tmp_path: Path) -> None:
    src, dest = _doc_ia(tmp_path), _dest(tmp_path)
    report = sync(src, dest, today="2026-11-07")
    assert {k for k, _ in report.changes} == {"creado"}
    assert (dest / ".doc_ia/.github/prompts/document_project.prompt.md").is_file()
    assert (dest / ".doc_ia/scripts/doc_trace.py").is_file()
    assert (dest / ".claude/commands/documentar.md").read_text(
        encoding="utf-8"
    ) == "# /documentar\n"
    assert (dest / "DOCUMENTAR.md").read_text(
        encoding="utf-8"
    ) == "# Cómo documentar MVG — Prueba\n"
    lock = _lock(dest)
    assert lock["doc_ia"] == "9.9.0" and lock["fecha"] == "2026-11-07"
    assert ".claude/commands/documentar.md" in lock["ficheros"]  # type: ignore[operator]
    assert "DOCUMENTAR.md" not in lock["ficheros"]  # type: ignore[operator]  # es del proyecto


def test_sync_is_idempotent_and_keeps_project_owned_files(tmp_path: Path) -> None:
    src, dest = _doc_ia(tmp_path), _dest(tmp_path)
    sync(src, dest)
    _write(dest / "DOCUMENTAR.md", "# Editado por el proyecto\n")
    assert sync(src, dest).changes == []
    assert (dest / "DOCUMENTAR.md").read_text(encoding="utf-8") == "# Editado por el proyecto\n"


def test_sync_updates_changed_and_removes_retired(tmp_path: Path) -> None:
    src, dest = _doc_ia(tmp_path), _dest(tmp_path)
    sync(src, dest)
    _write(src / "scripts/doc_trace.py", "print('v2')\n")
    _write(
        src / ".github/kit/MANIFEST.txt",
        MANIFEST.replace("pyproject.toml\n", "pyproject.toml\n", 1).replace(
            ".github/prompts/document_project.prompt.md\n", ""
        ),
    )
    report = sync(src, dest)
    assert ("actualizado", ".doc_ia/scripts/doc_trace.py") in report.changes
    assert ("retirado", ".doc_ia/.github/prompts/document_project.prompt.md") in report.changes
    assert not (dest / ".doc_ia/.github/prompts/document_project.prompt.md").exists()
    assert (dest / ".doc_ia/scripts/doc_trace.py").read_text(encoding="utf-8") == "print('v2')\n"


def test_sync_never_overwrites_local_edits_without_force(tmp_path: Path) -> None:
    src, dest = _doc_ia(tmp_path), _dest(tmp_path)
    sync(src, dest)
    _write(dest / ".doc_ia/scripts/doc_trace.py", "print('parche local')\n")
    _write(src / "scripts/doc_trace.py", "print('v2')\n")
    report = sync(src, dest)
    assert (".doc_ia/scripts/doc_trace.py", "editado en el destino") in report.conflicts
    assert "parche local" in (dest / ".doc_ia/scripts/doc_trace.py").read_text(encoding="utf-8")
    assert sync(src, dest, force=True).conflicts == []
    assert (dest / ".doc_ia/scripts/doc_trace.py").read_text(encoding="utf-8") == "print('v2')\n"


def test_sync_does_not_overwrite_foreign_launcher(tmp_path: Path) -> None:
    """Un repositorio de código con su propio /documentar no se pisa."""
    src, dest = _doc_ia(tmp_path), _dest(tmp_path)
    _write(dest / ".claude/commands/documentar.md", "# comando propio del proyecto\n")
    report = sync(src, dest)
    assert (
        ".claude/commands/documentar.md",
        "fichero ajeno: no lo instaló el kit",
    ) in report.conflicts
    assert "propio" in (dest / ".claude/commands/documentar.md").read_text(encoding="utf-8")


def test_check_detects_edits_missing_instance_and_outdated(tmp_path: Path) -> None:
    src, dest = _doc_ia(tmp_path), _dest(tmp_path)
    assert check(dest).conflicts == [(".doc_ia/kit.lock.json", "kit no instalado")]
    sync(src, dest)
    found = check(dest)
    assert (
        ".ai/prompts/documentar.prompt.md",
        "falta (lo crea /documentar o el CIERRE)",
    ) in found.conflicts
    _write(dest / ".ai/prompts/documentar.prompt.md", "# instancia\n")
    assert check(dest).conflicts == [] and check(dest).changes == []
    _write(src / "scripts/doc_trace.py", "print('v2')\n")
    assert ("desfasado", ".doc_ia/scripts/doc_trace.py") in check(dest, src).changes
    (dest / ".doc_ia/.github/prompts/document_project.prompt.md").unlink()
    assert (".doc_ia/.github/prompts/document_project.prompt.md", "falta") in check(dest).conflicts


def test_sync_without_changes_does_not_rewrite_the_lock(tmp_path: Path) -> None:
    """La Fase 0b sincroniza en cada sesión: sin cambios no debe quedar diff en el destino."""
    src, dest = _doc_ia(tmp_path), _dest(tmp_path)
    sync(src, dest, today="2026-11-07")
    lock = dest / KIT_DIR / "kit.lock.json"
    before = lock.read_bytes()
    assert sync(src, dest, today="2026-12-01").changes == []
    assert lock.read_bytes() == before
    _write(src / "scripts/doc_trace.py", "print('v2')\n")
    sync(src, dest, today="2026-12-01")
    assert _lock(dest)["fecha"] == "2026-12-01"


def test_dry_run_writes_nothing(tmp_path: Path) -> None:
    src, dest = _doc_ia(tmp_path), _dest(tmp_path)
    report = sync(src, dest, dry_run=True)
    assert (
        report.changes and not (dest / KIT_DIR).exists() and not (dest / "DOCUMENTAR.md").exists()
    )


def test_retired_file_edited_in_destination_is_a_conflict(tmp_path: Path) -> None:
    src, dest = _doc_ia(tmp_path), _dest(tmp_path)
    sync(src, dest)
    _write(dest / ".doc_ia/.github/prompts/document_project.prompt.md", "# editado\n")
    retired = MANIFEST.replace(".github/prompts/document_project.prompt.md\n", "")
    _write(src / ".github/kit/MANIFEST.txt", retired)
    report = sync(src, dest)
    assert (
        ".doc_ia/.github/prompts/document_project.prompt.md",
        "doc_ia ya no lo distribuye y está editado",
    ) in report.conflicts
    assert (dest / ".doc_ia/.github/prompts/document_project.prompt.md").is_file()


def test_check_from_reports_new_and_retired_and_rejects_vendored(tmp_path: Path) -> None:
    src, dest = _doc_ia(tmp_path), _dest(tmp_path)
    sync(src, dest)
    _write(src / "scripts/nuevo.py", "x = 1\n")
    manifest = MANIFEST.replace("scripts/doc_trace.py\n", "scripts/nuevo.py\n")
    _write(src / ".github/kit/MANIFEST.txt", manifest)
    changes = check(dest, src).changes
    assert ("nuevo en doc_ia", ".doc_ia/scripts/nuevo.py") in changes
    assert ("retirado en doc_ia", ".doc_ia/scripts/doc_trace.py") in changes
    with pytest.raises(KitError, match="copia de un destino"):
        check(dest, dest / KIT_DIR)


def test_invalid_lock_is_an_error(tmp_path: Path) -> None:
    src, dest = _doc_ia(tmp_path), _dest(tmp_path)
    _write(dest / KIT_DIR / "kit.lock.json", "{no es json")
    assert main(["--from", str(src), "sync", "--root", str(dest)]) == 2
    assert main(["check", "--root", str(dest)]) == 2


def test_sync_rejects_vendored_copy_and_self(tmp_path: Path) -> None:
    src, dest = _doc_ia(tmp_path), _dest(tmp_path)
    with pytest.raises(KitError, match="propio doc_ia"):
        sync(src, src)
    sync(src, dest)
    with pytest.raises(KitError, match="propio doc_ia"):
        sync(dest / KIT_DIR, dest)


def test_cli_exit_codes(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    src, dest = _doc_ia(tmp_path), _dest(tmp_path)
    assert main(["--from", str(src), "sync", "--root", str(dest)]) == 1
    assert main(["--from", str(src), "sync", "--root", str(dest)]) == 0
    assert main(["check", "--root", str(dest)]) == 1  # falta el prompt de instancia
    _write(dest / ".ai/prompts/documentar.prompt.md", "# instancia\n")
    assert main(["check", "--root", str(dest)]) == 0
    _write(dest / ".doc_ia/scripts/doc_trace.py", "editado\n")
    assert main(["--from", str(src), "sync", "--root", str(dest)]) == 2
    assert main(["--from", str(dest / KIT_DIR), "sync", "--root", str(dest)]) == 2
    assert "ERROR" in capsys.readouterr().err


def test_manifest_rejects_unknown_section_and_bad_pair(tmp_path: Path) -> None:
    with pytest.raises(KitError, match="sección desconocida"):
        parse_manifest(_write(tmp_path / "a.txt", "[otra]\nx\n"))
    with pytest.raises(KitError, match="origen -> destino"):
        parse_manifest(_write(tmp_path / "b.txt", "[lanzadores]\nsolo_origen\n"))


# --- manifiesto real de doc_ia ---


def test_real_manifest_files_exist_and_exclude_doc_ia_development() -> None:
    manifest = parse_manifest(ROOT / ".github/kit/MANIFEST.txt")
    for rel in manifest.methodology:
        assert (ROOT / rel).is_file(), rel
    for origin, _ in (*manifest.launchers, *manifest.instance):
        assert (ROOT / origin).is_file(), origin
    excluded = (
        "SHARED_INSTRUCTIONS",
        "bootstrap_ai_config",
        "config_review",
        "version_closure",
        "tests/",
    )
    assert not [r for r in manifest.methodology if any(e in r for e in excluded)]


def test_real_kit_installs_into_empty_destination(tmp_path: Path) -> None:
    dest = _dest(tmp_path)
    report = sync(ROOT, dest)
    assert report.conflicts == []
    assert (dest / ".doc_ia/scripts/kit.py").is_file()
    assert (dest / "AGENTS.md").is_file() and (dest / "GEMINI.md").is_file()
    assert "{proyecto}" not in (dest / "DOCUMENTAR.md").read_text(encoding="utf-8")
    assert not (dest / "DOCUMENTAR.md").read_text(encoding="utf-8").startswith("<!--")
