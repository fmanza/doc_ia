"""Sincroniza CHANGELOG.md y CONTRIBUTING.md de la raíz del repo a docs/.

Uso como MkDocs hook (automático via mkdocs.yml):
    hooks:
      - hooks/sync_root_docs.py

Uso como CLI independiente:
    python hooks/sync_root_docs.py
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent

PAIRS: tuple[tuple[str, str], ...] = (
    ("CHANGELOG.md", "changelog.md"),
    ("CONTRIBUTING.md", "contributing.md"),
)

# Sustituciones aplicadas en la copia de docs/ (no en los originales de raíz).
# Necesario porque los originales enlazan con nombres de raíz (CHANGELOG.md)
# mientras que en docs/ los ficheros usan nombre en minúsculas (changelog.md).
_LINK_FIXES: dict[str, dict[str, str]] = {
    "contributing.md": {"(CHANGELOG.md)": "(changelog.md)"},
}


def _sync(src: Path, dst: Path) -> None:
    if not src.exists():
        print(f"[sync_root_docs] AVISO: {src.name} no existe, se omite.")
        return
    shutil.copy2(src, dst)
    fixes = _LINK_FIXES.get(dst.name, {})
    if fixes:
        text = dst.read_text(encoding="utf-8")
        for old, new in fixes.items():
            text = text.replace(old, new)
        dst.write_text(text, encoding="utf-8")
    print(f"[sync_root_docs] {src.name} -> {dst}")


def on_pre_build(config: Any) -> None:
    docs_dir = Path(config["docs_dir"])
    for root_name, docs_name in PAIRS:
        _sync(ROOT / root_name, docs_dir / docs_name)


def main() -> int:
    docs_dir = ROOT / "docs"
    for root_name, docs_name in PAIRS:
        _sync(ROOT / root_name, docs_dir / docs_name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
