"""Verificación determinista del entorno de tooling documental.

Comprueba que las herramientas Python requeridas (mkdocs, ruff, mypy, pytest) y las
herramientas de conversión están disponibles. No invoca ningún servicio IA.

Herramientas de conversión:
  markitdown (Python, principal) — cubre PDF, DOCX, PPTX, HTML, EPUB y más.
  pandoc     (binario, complemento) — mejor calidad para ODT, RST y DOCX complejos.
"""

from __future__ import annotations

import importlib.util
import shutil
import sys

REQUIRED_TOOLS: tuple[str, ...] = ("mkdocs", "ruff", "mypy", "pytest")
# Paquetes Python opcionales (importables); markitdown es la dependencia principal de conversión
OPTIONAL_PYTHON_TOOLS: tuple[str, ...] = ("markitdown",)
# Herramientas de sistema opcionales (binarios en PATH); pandoc complementa para ODT/RST
SYSTEM_TOOLS: tuple[str, ...] = ("pandoc",)

_PANDOC_INSTALL = (
    "    Windows: winget install JohnMacFarlane.Pandoc\n"
    "    macOS:   brew install pandoc\n"
    "    Linux:   sudo apt install pandoc | sudo dnf install pandoc"
)
_MARKITDOWN_INSTALL = "    pip install markitdown"


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

    warnings: list[str] = []

    absent_optional_py = [t for t in OPTIONAL_PYTHON_TOOLS if importlib.util.find_spec(t) is None]
    if absent_optional_py:
        warnings.append(
            "markitdown no instalado: conversión de documentos a Markdown (PDF, DOCX, PPTX…).\n"
            f"   Instalar con:\n{_MARKITDOWN_INSTALL}"
        )

    absent_system = missing_system_tools()
    if absent_system:
        warnings.append(
            "pandoc no encontrado: complemento para ODT, RST y DOCX complejos.\n"
            f"   Instalar con:\n{_PANDOC_INSTALL}"
        )

    if warnings:
        print("Entorno de tooling documental completo (Python).")
        for w in warnings:
            print(f"⚠  {w}")
        return 0

    print("Entorno de tooling documental completo.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
