"""Tests de scripts/snapshot_sources.py: sin red, sobre carpetas temporales."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from scripts.snapshot_sources import (
    SnapshotError,
    main,
    resolve,
    stable_name,
    version_key,
)

DAY = "2026-11-05"


def _write(path: Path, content: str = "x") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content.encode("utf-8"))
    return path


def _manifest(dest: Path) -> dict[str, dict[str, object]]:
    data = json.loads((dest / ".ai" / "sources.json").read_text(encoding="utf-8"))
    sources: dict[str, dict[str, object]] = data["fuentes"]
    return sources


def _run(dest: Path, *args: str) -> int:
    return main(["--root", str(dest), *args])


def _sync(dest: Path, *args: str) -> int:
    return _run(dest, "sync", "--date", DAY, *args)


# --- versión y nombre estable ---


def test_version_key_compares_numerically() -> None:
    assert version_key("1.2.50") > version_key("1.2.9")
    assert version_key("2") > version_key("1.99.99")


@pytest.mark.parametrize(
    ("template", "expected"),
    [
        ("SocyalPro_Manual_ViolenciaGenero_v{ver}.docx", "SocyalPro_Manual_ViolenciaGenero.docx"),
        ("Manual {ver}.pdf", "Manual.pdf"),
        ("Guia-V{ver}.docx", "Guia.docx"),
        ("{ver}_notas.md", "_notas.md"),
    ],
)
def test_stable_name_strips_version_and_separator(template: str, expected: str) -> None:
    assert stable_name(template) == expected


def test_stable_name_without_stem_is_an_error() -> None:
    with pytest.raises(SnapshotError, match="nombre estable"):
        stable_name("v{ver}.docx")


def test_resolve_versioned_picks_highest_version(tmp_path: Path) -> None:
    src = tmp_path / "Modulos"
    for version in ("1.2.9", "1.2.50", "1.2.10"):
        _write(src / f"Manual_VG_v{version}.docx", version)
    _write(src / "Manual_VG_v1.2.99.pdf")  # otra extensión: no encaja
    _write(src / "Otro_Manual_v9.docx")
    [found] = resolve(str(src / "Manual_VG_v{ver}.docx"))
    assert (found.source.name, found.rel, found.version) == (
        "Manual_VG_v1.2.50.docx",
        "Manual_VG.docx",
        "1.2.50",
    )


def test_resolve_versioned_without_match_is_an_error(tmp_path: Path) -> None:
    _write(tmp_path / "Manual.docx")
    with pytest.raises(SnapshotError, match="encaja"):
        resolve(str(tmp_path / "Manual_v{ver}.docx"))


def test_resolve_directory_filters_and_skips_generated(tmp_path: Path) -> None:
    src = tmp_path / "Normativa"
    _write(src / "BOE-A-2004-21760.pdf")
    _write(src / "sub" / "plan.pdf")
    _write(src / "notas.txt")
    _write(src / "md" / "BOE-A-2004-21760.md")  # salida de conversión previa
    _write(src / "~$borrador.docx")  # bloqueo de Office
    _write(src / ".git" / "config")
    assert [r.rel for r in resolve(str(src))] == [
        "BOE-A-2004-21760.pdf",
        "notas.txt",
        "sub/plan.pdf",
    ]
    assert [r.rel for r in resolve(str(src), ("*.pdf",))] == [
        "BOE-A-2004-21760.pdf",
        "sub/plan.pdf",
    ]


def test_resolve_missing_origin_is_an_error(tmp_path: Path) -> None:
    with pytest.raises(SnapshotError, match="no existe"):
        resolve(str(tmp_path / "nada"))


# --- add / sync ---


def test_sync_versioned_file_records_evolution(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    src, dest = tmp_path / "share", tmp_path / "VG"
    _write(src / "Manual_v1.2.50.docx", "v50")
    _write(src / "Manual_v1.2.50.pdf", "pdf")  # el hermano PDF no se copia
    pattern = str(src / "Manual_v{ver}.docx")
    assert _run(dest, "add", "manual", pattern) == 0
    assert _sync(dest) == 1
    staged = dest / "_staging" / "manual" / "Manual.docx"
    assert staged.read_text(encoding="utf-8") == "v50"
    assert sorted(p.name for p in staged.parent.iterdir()) == ["Manual.docx"]
    assert _sync(dest) == 0  # idempotente

    # Nueva versión: misma ruta estable, la conversión anterior se invalida.
    _write(dest / "_staging" / "manual" / "md" / "Manual.md", "conversión v50")
    _write(src / "Manual_v1.2.51.docx", "v51")
    capsys.readouterr()
    assert _sync(dest) == 1
    assert "(v1.2.50 → v1.2.51)" in capsys.readouterr().out
    assert staged.read_text(encoding="utf-8") == "v51"
    assert not (dest / "_staging" / "manual" / "md" / "Manual.md").exists()
    entry = _manifest(dest)["manual"]
    assert entry["ficheros"]["Manual.docx"]["version"] == "1.2.51"  # type: ignore[index]
    history = entry["historial"]
    assert [(e["cambio"], e.get("version"), e.get("version_anterior")) for e in history] == [  # type: ignore[union-attr]
        ("alta", "1.2.50", None),
        ("modificado", "1.2.51", "1.2.50"),
    ]


def test_sync_directory_detects_modified_and_removed(tmp_path: Path) -> None:
    src, dest = tmp_path / "Normativa", tmp_path / "VG"
    _write(src / "ley.pdf", "a")
    _write(src / "plan.pdf", "b")
    _run(dest, "add", "normativa", str(src), "--include", "*.pdf")
    assert _sync(dest) == 1
    _write(dest / "_staging" / "normativa" / "md" / "plan.md")
    _write(src / "ley.pdf", "a2")
    (src / "plan.pdf").unlink()
    assert _sync(dest) == 1
    assert not (dest / "_staging" / "normativa" / "plan.pdf").exists()
    assert not (dest / "_staging" / "normativa" / "md" / "plan.md").exists()
    entry = _manifest(dest)["normativa"]
    assert list(entry["ficheros"]) == ["ley.pdf"]  # type: ignore[call-overload]
    assert [e["cambio"] for e in entry["historial"]][-2:] == ["modificado", "baja"]  # type: ignore[union-attr]
    assert entry["incluir"] == ["*.pdf"]


def test_sync_dry_run_copies_nothing(tmp_path: Path) -> None:
    src, dest = tmp_path / "doc.docx", tmp_path / "VG"
    _write(src)
    _run(dest, "add", "doc", str(src))
    assert _sync(dest, "--dry-run") == 1
    assert not (dest / "_staging").exists()
    assert _manifest(dest)["doc"]["ficheros"] == {}


def test_sync_restores_deleted_staging_copy(tmp_path: Path) -> None:
    src, dest = tmp_path / "doc.docx", tmp_path / "VG"
    _write(src)
    _run(dest, "add", "doc", str(src))
    _sync(dest)
    (dest / "_staging" / "doc" / "doc.docx").unlink()
    assert _sync(dest) == 1
    assert (dest / "_staging" / "doc" / "doc.docx").is_file()


def test_sync_never_writes_into_the_origin(tmp_path: Path) -> None:
    src, dest = tmp_path / "share", tmp_path / "VG"
    _write(src / "a.docx")
    before = sorted(p.relative_to(src) for p in src.rglob("*"))
    _run(dest, "add", "share", str(src))
    _sync(dest)
    assert sorted(p.relative_to(src) for p in src.rglob("*")) == before


@pytest.mark.parametrize(
    ("args", "message"),
    [
        (("add", "mal nombre", "x"), "nombre de origen inválido"),
        (("add", "m", "a_v{ver}.docx", "--include", "*.pdf"), "--include no aplica"),
        (("sync", "desconocido"), "no declarados"),
    ],
)
def test_errors_exit_2(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], args: tuple[str, ...], message: str
) -> None:
    assert _run(tmp_path, *args) == 2
    assert message in capsys.readouterr().err


def test_sync_missing_origin_exit_2(tmp_path: Path) -> None:
    dest = tmp_path / "VG"
    _run(dest, "add", "doc", str(tmp_path / "no_existe.docx"))
    assert _sync(dest) == 2


def test_sync_failing_origin_does_not_lose_the_others(tmp_path: Path) -> None:
    src, dest = tmp_path / "ok.docx", tmp_path / "VG"
    _write(src)
    _run(dest, "add", "a_caido", str(tmp_path / "unidad_desconectada"))
    _run(dest, "add", "b_ok", str(src))
    assert _sync(dest) == 2
    assert list(_manifest(dest)["b_ok"]["ficheros"]) == ["ok.docx"]  # type: ignore[call-overload]
    assert _sync(dest, "b_ok") == 0


def test_list_shows_versions(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    src, dest = tmp_path / "share", tmp_path / "VG"
    _write(src / "Manual_v3.1.docx")
    _run(dest, "add", "manual", str(src / "Manual_v{ver}.docx"))
    _sync(dest)
    capsys.readouterr()
    assert _run(dest, "list") == 0
    assert "Manual.docx v3.1" in capsys.readouterr().out


def test_corrupt_manifest_exit_2(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _write(tmp_path / ".ai" / "sources.json", "{no es json")
    assert _run(tmp_path, "list") == 2
    assert "JSON inválido" in capsys.readouterr().err


# --- replace: documento reestructurado (la versión vigente la indica el usuario) ---


def _restructured(tmp_path: Path) -> tuple[Path, str, str]:
    """Origen antiguo con versión alta y documento nuevo, reestructurado, con versión menor."""
    _write(tmp_path / "general" / "Diseno_Integraciones_v1.10.docx", "antiguo")
    _write(tmp_path / "modulo" / "Diseno_Integraciones_Info_v1.2.docx", "nuevo")
    old_spec = str(tmp_path / "general" / "Diseno_Integraciones_v{ver}.docx")
    new_spec = str(tmp_path / "modulo" / "Diseno_Integraciones_Info_v{ver}.docx")
    return tmp_path / "destino", old_spec, new_spec


def test_replace_switches_source_even_with_lower_version(tmp_path: Path) -> None:
    dest, old_spec, new_spec = _restructured(tmp_path)
    assert _run(dest, "add", "dt", old_spec) == 0
    assert _sync(dest) == 1
    _write(dest / "_staging" / "dt" / "md" / "Diseno_Integraciones.md", "conversión antigua")
    assert _run(dest, "replace", "dt", new_spec, "--date", DAY) == 0
    entry = _manifest(dest)["dt"]
    assert entry["origen"] == new_spec
    assert entry["ficheros"] == {}
    assert not (dest / "_staging" / "dt").exists()  # binario anterior y su md/ retirados
    assert entry["historial"][-1] == {  # type: ignore[index]
        "fecha": DAY,
        "cambio": "sustituido",
        "origen_anterior": old_spec,
        "origen": new_spec,
    }
    assert _sync(dest) == 1  # el documento nuevo entra como alta, con su versión menor
    files = _manifest(dest)["dt"]["ficheros"]
    assert list(files) == ["Diseno_Integraciones_Info.docx"]  # type: ignore[call-overload]
    assert files["Diseno_Integraciones_Info.docx"]["version"] == "1.2"  # type: ignore[index]
    staged = dest / "_staging" / "dt" / "Diseno_Integraciones_Info.docx"
    assert staged.read_text(encoding="utf-8") == "nuevo"


def test_replace_keeps_previous_history(tmp_path: Path) -> None:
    dest, old_spec, new_spec = _restructured(tmp_path)
    _run(dest, "add", "dt", old_spec)
    _sync(dest)
    _run(dest, "replace", "dt", new_spec)
    _sync(dest)
    history = _manifest(dest)["dt"]["historial"]
    assert [e["cambio"] for e in history] == ["alta", "sustituido", "alta"]  # type: ignore[union-attr]


def test_replace_with_missing_document_keeps_old_declaration(tmp_path: Path) -> None:
    dest, old_spec, _ = _restructured(tmp_path)
    _run(dest, "add", "dt", old_spec)
    _sync(dest)
    assert _run(dest, "replace", "dt", str(tmp_path / "modulo" / "No_Existe_v{ver}.docx")) == 2
    assert _manifest(dest)["dt"]["origen"] == old_spec
    assert (dest / "_staging" / "dt" / "Diseno_Integraciones.docx").is_file()


@pytest.mark.parametrize(
    ("declared", "message"),
    [(False, "no declarado"), (True, "usa `sync`")],
)
def test_replace_errors_exit_2(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], declared: bool, message: str
) -> None:
    dest, old_spec, _ = _restructured(tmp_path)
    if declared:
        _run(dest, "add", "dt", old_spec)
    assert _run(dest, "replace", "dt", old_spec) == 2
    assert message in capsys.readouterr().err


def test_list_tolerates_replaced_history(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    dest, old_spec, new_spec = _restructured(tmp_path)
    _run(dest, "add", "dt", old_spec)
    _run(dest, "replace", "dt", new_spec)
    capsys.readouterr()
    assert _run(dest, "list") == 0
    assert "Diseno_Integraciones_Info_v{ver}.docx" in capsys.readouterr().out


def test_cli_prints_version_arrow_on_non_utf8_console(tmp_path: Path) -> None:
    """Consola cp1252 (Windows): la flecha de cambio de versión no rompe el sync."""
    import os
    import subprocess
    import sys

    src, dest = tmp_path / "share", tmp_path / "VG"
    _write(src / "Manual_v1.0.docx", "a")
    script = Path(__file__).resolve().parent.parent / "scripts" / "snapshot_sources.py"
    env = {**os.environ, "PYTHONIOENCODING": "cp1252"}

    def cli(*args: str) -> subprocess.CompletedProcess[bytes]:
        cmd = [sys.executable, str(script), "--root", str(dest), *args]
        return subprocess.run(cmd, capture_output=True, env=env, check=False)

    cli("add", "manual", str(src / "Manual_v{ver}.docx"))
    cli("sync")
    _write(src / "Manual_v1.1.docx", "b")
    result = cli("sync")
    assert result.returncode == 1, result.stderr
    assert _manifest(dest)["manual"]["ficheros"]["Manual.docx"]["version"] == "1.1"  # type: ignore[index]
