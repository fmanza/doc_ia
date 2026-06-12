"""Verificación determinista del entorno de tooling documental.

Comprueba que las herramientas Python requeridas (mkdocs, ruff, mypy, pytest) y las
herramientas de sistema recomendadas (pandoc) están disponibles. No invoca ningún servicio IA.
"""

from __future__ import annotations

import importlib.util
import shutil
import sys

REQUIRED_TOOLS: tuple[str, ...] = ("mkdocs", "ruff", "mypy", "pytest")
SYSTEM_TOOLS: tuple[str, ...] = ("pandoc",)

_PANDOC_INSTALL = (
    "    Windows: winget install JohnMacFarlane.Pandoc\n"
    "    macOS:   brew install pandoc\n"
    "    Linux:   sudo apt install pandoc | sudo dnf install pandoc"
)


def missing_tools(tools: tuple[str, ...] = REQUIRED_TOOLS) -> list[str]:
    """Devuelve la lista de herramientas Python no importables en el entorno actual."""
    return [tool for tool in tools if importlib.util.find_spec(tool) is None]


def missing_system_tools(tools: tuple[str, ...] = SYSTEM_TOOLS) -> list[str]:
    """Devuelve la lista de herramientas de sistema no encontradas en el PATH."""
    return [tool for tool in tools if shutil.which(tool) is None]


def main() -> int:
    """Imprime el estado del entorno; devuelve 0 si está completo, 1 si falta algo."""
    absent = missing_tools()
    if absent:
        print(f"Faltan herramientas: {', '.join(absent)}")
        return 1

    absent_system = missing_system_tools()
    if absent_system:
        print("Entorno de tooling documental completo (Python).")
        print(f"⚠  Herramientas opcionales no encontradas: {', '.join(absent_system)}")
        print("   pandoc: conversión PDF/DOCX/… a Markdown (scripts/convert_to_md.py).")
        print(f"   Instalar con:\n{_PANDOC_INSTALL}")
        return 0

    print("Entorno de tooling documental completo.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
