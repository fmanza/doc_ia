"""Verificación determinista del entorno de tooling documental.

Comprueba que las herramientas Python requeridas (mkdocs, ruff, mypy, pytest) y las
herramientas de conversión están disponibles. No invoca ningún servicio IA.

Herramientas de conversión:
  markitdown (Python, principal) — cubre PDF, DOCX, PPTX, XLSX, XLS, HTML, CSV, EPUB, IPYNB.
  pandoc     (binario, complemento) — cubre DOC, ODT, RST y fallback para DOCX/PPTX/EPUB.

Plugins opcionales de markitdown (amplían formatos soportados):
  pdfminer   → PDF        python-docx → DOCX       python-pptx → PPTX
  openpyxl   → XLSX       xlrd        → XLS
"""

from __future__ import annotations

import importlib.util
import shutil
import sys

REQUIRED_TOOLS: tuple[str, ...] = ("mkdocs", "ruff", "mypy", "pytest")

OPTIONAL_PYTHON_TOOLS: tuple[str, ...] = ("markitdown",)

MARKITDOWN_PLUGINS: dict[str, str] = {
    "pdfminer": ".pdf",
    "docx": ".docx (python-docx)",
    "pptx": ".pptx (python-pptx)",
    "openpyxl": ".xlsx",
    "xlrd": ".xls",
}

SYSTEM_TOOLS: tuple[str, ...] = ("pandoc",)

_PANDOC_INSTALL = (
    "    Windows: winget install JohnMacFarlane.Pandoc\n"
    "    macOS:   brew install pandoc\n"
    "    Linux:   sudo apt install pandoc | sudo dnf install pandoc"
)
_MARKITDOWN_INSTALL = "    pip install markitdown"
_MARKITDOWN_PLUGINS_INSTALL = "    pip install python-docx python-pptx openpyxl xlrd"


def missing_tools(tools: tuple[str, ...] = REQUIRED_TOOLS) -> list[str]:
    """Devuelve la lista de herramientas Python no importables en el entorno actual."""
    return [tool for tool in tools if importlib.util.find_spec(tool) is None]


def missing_system_tools(tools: tuple[str, ...] = SYSTEM_TOOLS) -> list[str]:
    """Devuelve la lista de herramientas de sistema no encontradas en el PATH."""
    return [tool for tool in tools if shutil.which(tool) is None]


def check_markitdown_plugins() -> tuple[list[str], list[str]]:
    """Comprueba plugins de markitdown. Devuelve (instalados, faltantes)."""
    installed: list[str] = []
    missing: list[str] = []
    for plugin, ext_desc in MARKITDOWN_PLUGINS.items():
        if importlib.util.find_spec(plugin) is not None:
            installed.append(f"{plugin} ({ext_desc})")
        else:
            missing.append(f"{plugin} ({ext_desc})")
    return installed, missing


def main() -> int:
    """Imprime el estado del entorno; devuelve 0 si está completo, 1 si falta algo."""
    absent = missing_tools()
    if absent:
        print(f"Faltan herramientas: {', '.join(absent)}")
        return 1

    warnings: list[str] = []

    has_markitdown = importlib.util.find_spec("markitdown") is not None
    if not has_markitdown:
        warnings.append(
            "markitdown no instalado: conversión de documentos a Markdown "
            "(PDF, DOCX, PPTX, XLSX, HTML, CSV, EPUB…).\n"
            f"   Instalar con:\n{_MARKITDOWN_INSTALL}"
        )
    else:
        _, missing_plugins = check_markitdown_plugins()
        if missing_plugins:
            warnings.append(
                "markitdown instalado pero faltan plugins opcionales:\n"
                + "".join(f"      ✗ {p}\n" for p in missing_plugins)
                + f"   Instalar con:\n{_MARKITDOWN_PLUGINS_INSTALL}"
            )

    absent_system = missing_system_tools()
    if absent_system:
        warnings.append(
            "pandoc no encontrado: complemento para DOC, ODT, RST y fallback de DOCX/PPTX/EPUB.\n"
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
