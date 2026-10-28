"""Mermaid servido en local: coherencia entre el fichero, `mkdocs.yml` y la CI (sin red).

Material y Zensical solo descargan Mermaid de unpkg si `window.mermaid` no existe; con la
librería en `docs/assets/vendor/mermaid/` el sitio y el ZIP offline dibujan los diagramas sin
conexión (`docs/functional/build_docs_zip.md`, AC-10). Sesión `2026-10-28f_mermaid_local`.
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "docs" / "assets" / "vendor" / "mermaid"
THEME_JS = "assets/js/mermaid-theme.js"
# Huella de `dist/mermaid.min.js` del tarball de npm (ver SOURCE.txt); cambia al actualizar.
VENDORED_SHA256 = "a8a6a6f805b074a8261a2825c86f99c8054acb3b35f50bb7e24a4f9f2c3c3b9f"


def _vendored() -> Path:
    files = sorted(VENDOR.glob("mermaid-*.min.js"))
    assert len(files) == 1, files
    return files[0]


def _version() -> str:
    match = re.fullmatch(r"mermaid-(\d+\.\d+\.\d+)\.min\.js", _vendored().name)
    assert match, _vendored().name
    return match.group(1)


def _extra_javascript(config: Path) -> list[str]:
    """Entradas de `extra_javascript` (lectura textual: `mkdocs.yml` usa tags `!!python`)."""
    block = re.search(
        r"^extra_javascript:\n((?:[ \t]+.*\n|#.*\n|\n)*)", config.read_text("utf-8"), re.M
    )
    assert block, config
    return re.findall(r"^\s*-\s*([^\s#]+)", block.group(1), re.M)


def test_vendored_mermaid_is_pinned() -> None:
    """Un único fichero, cuya versión interna coincide con el nombre y con la huella fijada."""
    vendored = _vendored()
    data = vendored.read_bytes()
    assert f'version:"{_version()}"'.encode() in data
    assert hashlib.sha256(data).hexdigest() == VENDORED_SHA256
    assert (VENDOR / "LICENSE").is_file()
    source = (VENDOR / "SOURCE.txt").read_text(encoding="utf-8")
    assert _version() in source and VENDORED_SHA256 in source


@pytest.mark.parametrize("config", [ROOT / "mkdocs.yml"], ids=lambda p: p.name)
def test_extra_javascript_loads_local_mermaid_then_theme(config: Path) -> None:
    """Librería local antes de `mermaid-theme.js`; sin CDN ni `mermaid.run()` propio (AC-10)."""
    scripts = _extra_javascript(config)
    vendored = f"assets/vendor/mermaid/{_vendored().name}"
    assert vendored in scripts and THEME_JS in scripts, scripts
    assert scripts.index(vendored) < scripts.index(THEME_JS)
    assert not [s for s in scripts if re.search(r"unpkg|jsdelivr|assets/js/mermaid\.js$", s)]


def test_ci_validates_the_vendored_version() -> None:
    """El job `mermaid` de CI parsea los diagramas con la misma versión que se sirve."""
    ci = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert f'mermaid: "{_version()}"' in ci


def test_theme_script_fixes_startup_and_theme() -> None:
    """`mermaid-theme.js` evita el render propio de Mermaid y completa el tema para Material."""
    script = (ROOT / "docs" / THEME_JS).read_text(encoding="utf-8")
    assert "startOnLoad: false" in script
    assert 'theme: "default"' in script


@pytest.mark.parametrize("package", ["material", "zensical"])
def test_theme_bundle_uses_global_mermaid(package: str) -> None:
    """El tema instalado solo descarga Mermaid si `window.mermaid` no existe y llama a `initialize`.

    Si una actualización del tema cambia su cargador, el fichero local dejaría de usarse.
    """
    spec = importlib.util.find_spec(package)
    if spec is None or spec.origin is None:
        pytest.skip(f"{package} no instalado")
    bundles = list(Path(spec.origin).parent.glob("templates/assets/javascripts/bundle.*.min.js"))
    assert bundles, package
    text = bundles[0].read_text(encoding="utf-8")
    assert 'typeof mermaid=="undefined"' in text
    assert "mermaid.initialize(" in text
