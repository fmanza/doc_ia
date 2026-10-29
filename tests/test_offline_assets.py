"""ZIP navegable sin servidor: plugin `offline` + shim iframe-worker local (sin red).

Con `offline`, MkDocs Material y Zensical escriben el índice de búsqueda como JS y lo cargan por
`file://`; la búsqueda necesita además el shim iframe-worker, que ambos descargan de unpkg salvo
que `extra.polyfills` ya contenga una ruta con «iframe-worker».
Sesión `2026-10-29d_zip_sin_servidor`.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

import mkdocs_hooks
import pytest

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "docs" / "assets" / "vendor" / "iframe-worker"
# Huella de `shim/index.js` del tarball de npm (ver SOURCE.txt); cambia al actualizar.
VENDORED_SHA256 = "e8e412dbcfea9b7e31b5ffa288d7b6035915e714c542f4176a0cdbe262fc9609"
CONFIGS = [ROOT / "mkdocs.yml", ROOT / ".github" / "templates" / "TEMPLATE_mkdocs.yml"]


def _vendored() -> Path:
    files = sorted(VENDOR.glob("iframe-worker-shim-*.min.js"))
    assert len(files) == 1, files
    return files[0]


def _version() -> str:
    match = re.fullmatch(r"iframe-worker-shim-(\d+\.\d+\.\d+)\.min\.js", _vendored().name)
    assert match, _vendored().name
    return match.group(1)


def _block(config: Path, key: str, indent: str = "") -> list[str]:
    """Entradas de una lista YAML (lectura textual: la plantilla no es YAML válido)."""
    block = re.search(
        rf"^{indent}{key}:\n((?:{indent}[ \t]+.*\n|[ \t]*#.*\n)*)", config.read_text("utf-8"), re.M
    )
    assert block, f"{config.name}: falta {key}"
    return re.findall(r"^\s*-\s*([^\s#:]+)", block.group(1), re.M)


def test_vendored_shim_is_pinned() -> None:
    """Un único fichero, con la huella fijada, licencia y procedencia."""
    assert hashlib.sha256(_vendored().read_bytes()).hexdigest() == VENDORED_SHA256
    assert (VENDOR / "LICENSE").is_file()
    source = (VENDOR / "SOURCE.txt").read_text(encoding="utf-8")
    assert _version() in source and VENDORED_SHA256 in source


@pytest.mark.parametrize("config", CONFIGS, ids=lambda p: p.name)
def test_config_builds_a_site_that_opens_without_server(config: Path) -> None:
    """URLs `*.html`, plugin `offline` y shim local: sin unpkg ni otro script remoto."""
    text = config.read_text(encoding="utf-8")
    assert re.search(r"^use_directory_urls:\s*false\s*$", text, re.M)
    assert "offline" in _block(config, "plugins")
    polyfills = _block(config, "polyfills", indent="  ")
    assert polyfills == [f"assets/vendor/iframe-worker/{_vendored().name}"], polyfills


def test_zip_hook_runs_after_offline_plugin() -> None:
    """El índice JS lo escribe `offline` en su on_post_build: el ZIP latest va detrás."""
    from material.plugins.offline.plugin import OfflinePlugin

    offline = getattr(OfflinePlugin.on_post_build, "mkdocs_priority", 0)
    assert getattr(mkdocs_hooks.on_post_build, "mkdocs_priority", 0) < offline
