"""Guardas de compatibilidad con Zensical: pérdidas que ningún build `--strict` detecta.

Zensical ignora en silencio los plugins de MkDocs que no soporta y la clave `hooks:`
(ver `.claude/EDGE_CASES.md` § Zensical). Estos tests convierten esas pérdidas en fallos.
"""

from __future__ import annotations

import posixpath
import re
from pathlib import Path
from typing import Any

import mkdocs_hooks
from scripts.doc_trace import _load_yaml

ROOT = Path(__file__).resolve().parents[1]

# Plugins de mkdocs.yml que Zensical ejecuta o sustituye por un módulo nativo.
# Fuente: https://zensical.org/compatibility/plugins/ (consultada el 2026-10-28, Zensical 0.0.73).
# Revisar al actualizar Zensical.
ZENSICAL_SUPPORTED_PLUGINS = frozenset(
    {
        "api-autonav",
        "audio",
        "autoapi",
        "autorefs",
        "awesome-nav",
        "blog",
        "callouts",
        "exclude",
        "gh-admonitions",
        "glightbox",
        "include-markdown",
        "literate-nav",
        "llmstxt",
        "macros",
        "markdown-exec",
        "markdownextradata",
        "meta",
        "mike",
        "minify",
        "mkdocstrings",
        "nav-weight",
        "offline",
        "privacy",
        "redirects",
        "rss",
        "search",
        "section-index",
        "social",
        "table-reader",
        "tags",
        "video",
    }
)

ZIP_LINK_RE = re.compile(r'href="([^"]+\.zip(?:\.sha256)?)"')


def _config() -> dict[str, Any]:
    config = _load_yaml((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
    assert isinstance(config, dict)
    return config


def _plugin_names(config: dict[str, Any]) -> list[str]:
    plugins = config.get("plugins", ["search"])
    return [next(iter(p)) if isinstance(p, dict) else str(p) for p in plugins]


def test_mkdocs_plugins_are_supported_by_zensical() -> None:
    """Un plugin no soportado se ignora sin aviso: el sitio perdería su función."""
    unsupported = [p for p in _plugin_names(_config()) if p not in ZENSICAL_SUPPORTED_PLUGINS]
    assert not unsupported, f"Plugins que Zensical ignoraría en silencio: {unsupported}"


def test_downloads_links_point_to_latest_zip(tmp_path: Path) -> None:
    """Los enlaces de downloads.md resuelven al ZIP latest que genera mkdocs_hooks.py.

    `--strict` no valida `<a href>` en HTML crudo: un enlace que salga de `site/` (p. ej. al
    pasar a URLs `*.html`) o un nombre de ZIP distinto pasarían el build sin aviso.
    """
    site = tmp_path / "site"
    site.mkdir()
    (site / "index.html").write_text("<h1>Demo</h1>", encoding="utf-8")
    mkdocs_hooks.on_post_build({"site_dir": str(site)})
    produced = {p.name for p in site.iterdir() if p.name.endswith((".zip", ".zip.sha256"))}

    page_dir = "downloads" if _config().get("use_directory_urls", True) else ""
    links = ZIP_LINK_RE.findall((ROOT / "docs" / "downloads.md").read_text(encoding="utf-8"))
    assert links, "downloads.md no enlaza ningún ZIP"
    for href in links:
        target = posixpath.normpath(posixpath.join(page_dir, href))
        assert target in produced, f"{href} → {target}; generados en site/: {sorted(produced)}"
