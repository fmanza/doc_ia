"""Verificación determinista del entorno de tooling documental.

Comprueba que las herramientas requeridas (mkdocs, ruff, mypy, pytest) están
instaladas en el entorno activo. No invoca ningún servicio IA.
"""

from __future__ import annotations

import importlib.util
import sys

REQUIRED_TOOLS: tuple[str, ...] = ("mkdocs", "ruff", "mypy", "pytest")


def missing_tools(tools: tuple[str, ...] = REQUIRED_TOOLS) -> list[str]:
    """Devuelve la lista de herramientas no importables en el entorno actual."""
    return [tool for tool in tools if importlib.util.find_spec(tool) is None]


def main() -> int:
    """Imprime el estado del entorno; devuelve 0 si está completo, 1 si falta algo."""
    absent = missing_tools()
    if absent:
        print(f"Faltan herramientas: {', '.join(absent)}")
        return 1
    print("Entorno de tooling documental completo.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
