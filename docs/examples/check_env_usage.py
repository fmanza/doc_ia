"""Ejemplo: verificación del entorno de tooling con check_env.missing_tools."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from check_env import REQUIRED_TOOLS, missing_tools  # noqa: E402

faltan = missing_tools(REQUIRED_TOOLS)
if faltan:
    print(f"Faltan herramientas: {', '.join(faltan)}")
else:
    print("Entorno de tooling documental completo.")
