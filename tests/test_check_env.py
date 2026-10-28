"""Tests del tooling de verificación de entorno."""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from check_env import missing_system_tools, missing_tools  # noqa: E402


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
