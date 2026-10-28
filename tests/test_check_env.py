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


def test_main_warns_when_zensical_missing(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(check_env, "missing_tools", _only_missing("zensical"))
    assert check_env.main() == 0
    assert "zensical no instalado (opcional)" in capsys.readouterr().out


def test_main_no_zensical_warning_when_installed(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(check_env, "missing_tools", _only_missing())
    assert check_env.main() == 0
    assert "zensical" not in capsys.readouterr().out


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
