"""Tests del tooling de verificación de entorno."""

import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import check_env  # noqa: E402
from check_env import missing_system_tools, missing_tools  # noqa: E402


def _only_missing(*absent: str) -> object:
    """Sustituto de ``missing_tools`` que da por ausentes solo las herramientas indicadas."""

    def fake(tools: tuple[str, ...] = check_env.REQUIRED_TOOLS) -> list[str]:
        return [tool for tool in tools if tool in absent]

    return fake


def test_zensical_is_required_and_mkdocs_is_not() -> None:
    """Zensical es el único generador (ADR-003): sin él, el entorno está incompleto."""
    assert "zensical" in check_env.REQUIRED_TOOLS
    assert "mkdocs" not in check_env.REQUIRED_TOOLS


def test_main_fails_when_zensical_missing(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(check_env, "missing_tools", _only_missing("zensical"))
    assert check_env.main() == 1
    assert "Faltan herramientas: zensical" in capsys.readouterr().out


def test_missing_tools_empty_when_tools_exist() -> None:
    assert missing_tools(("sys",)) == []


def test_missing_tools_detects_absent_tool() -> None:
    assert missing_tools(("paquete_inexistente_xyz",)) == ["paquete_inexistente_xyz"]


def test_missing_system_tools_detects_absent_tool() -> None:
    assert missing_system_tools(("herramienta_inexistente_xyz123",)) == [
        "herramienta_inexistente_xyz123"
    ]


def test_missing_system_tools_empty_when_tool_exists() -> None:
    for candidate in ("python", "python3", "git"):
        if shutil.which(candidate) is not None:
            assert missing_system_tools((candidate,)) == []
            return


def test_main_script_survives_non_utf8_console() -> None:
    """En una consola cp1252 (Windows) los avisos con «⚠» no deben romper el script."""
    import os
    import subprocess

    script = Path(__file__).resolve().parents[1] / "scripts" / "check_env.py"
    env = {**os.environ, "PYTHONIOENCODING": "cp1252"}
    result = subprocess.run(
        [sys.executable, str(script)], capture_output=True, env=env, timeout=60, check=False
    )
    assert b"UnicodeEncodeError" not in result.stderr
    assert result.returncode in (0, 1)


def _all_installed(monkeypatch: pytest.MonkeyPatch, *system_absent: str) -> None:
    """Entorno simulado con todas las herramientas; ``system_absent`` falta en el PATH."""
    real_find_spec = check_env.importlib.util.find_spec

    def fake_find_spec(name: str, *args: object) -> object:
        return object() if name in check_env.OPTIONAL_PYTHON_TOOLS else real_find_spec(name)

    monkeypatch.setattr(check_env, "missing_tools", _only_missing())
    monkeypatch.setattr(check_env, "missing_system_tools", lambda tools=(): list(system_absent))
    monkeypatch.setattr(check_env, "check_markitdown_plugins", lambda: ([], []))
    monkeypatch.setattr(check_env.importlib.util, "find_spec", fake_find_spec)


def test_main_reports_complete_when_everything_installed(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """AC-01: todo instalado → «completo.» sin avisos; docling solo como nota informativa."""
    _all_installed(monkeypatch)
    assert check_env.main() == 0
    out = capsys.readouterr().out
    assert out.splitlines()[0] == "Entorno de tooling documental completo."
    assert "⚠" not in out


def test_main_exits_1_listing_missing_required(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """AC-02: falta alguna requerida → lista exacta y código 1."""
    monkeypatch.setattr(check_env, "missing_tools", _only_missing("ruff", "pytest"))
    assert check_env.main() == 1
    assert capsys.readouterr().out.strip() == "Faltan herramientas: ruff, pytest"


def test_missing_tools_preserves_input_order() -> None:
    """AC-03: solo las ausentes, en el orden de la lista."""
    tools = ("zz_inexistente_xyz", "sys", "aa_inexistente_xyz")
    assert missing_tools(tools) == ["zz_inexistente_xyz", "aa_inexistente_xyz"]


def test_main_warns_about_pandoc_but_succeeds(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """AC-04: requeridas completas sin pandoc → completo con aviso y código 0."""
    _all_installed(monkeypatch, "pandoc")
    assert check_env.main() == 0
    out = capsys.readouterr().out
    assert out.splitlines()[0] == "Entorno de tooling documental completo (Python)."
    assert "⚠  pandoc no encontrado" in out
