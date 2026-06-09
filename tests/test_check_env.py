"""Tests del tooling de verificación de entorno."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from check_env import missing_tools  # noqa: E402


def test_missing_tools_empty_when_tools_exist() -> None:
    assert missing_tools(("sys",)) == []


def test_missing_tools_detects_absent_tool() -> None:
    assert missing_tools(("paquete_inexistente_xyz",)) == ["paquete_inexistente_xyz"]
