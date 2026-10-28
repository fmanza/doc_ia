"""Conformidad de la documentación de doc_ia con los arquetipos (DOCUMENTATION_STANDARD.md §3).

Dogfooding: doc_ia se documenta con sus propios arquetipos, así que estos tests verifican sobre
su `docs/` los criterios estructurales de `docs/functional/archetypes.md` (§7).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
EVIDENCE = '??? note "Evidencia"'
SECTION_RE = re.compile(r"^## (\d+)\. ", re.M)

# Scripts sin páginas propias: se distribuye dentro del ZIP y se documenta en la Referencia.
UNDOCUMENTED_SCRIPTS = {"__init__", "start-server"}
# Ejemplos cuyo nombre no coincide con el del módulo.
EXAMPLE_FOR = {"build_docs_zip": "build_docs_zip_offline"}


def _sections(page: Path) -> list[int]:
    return [int(n) for n in SECTION_RE.findall(page.read_text(encoding="utf-8"))]


def _pages(folder: str) -> list[Path]:
    return sorted(p for p in (DOCS / folder).glob("*.md") if p.name != "index.md")


def _ids(pages: list[Path]) -> list[str]:
    return [p.stem for p in pages]


@pytest.mark.parametrize("page", _pages("functional"), ids=_ids(_pages("functional")))
def test_functional_pages_follow_archetype_1(page: Path) -> None:
    """Arq. 1: 8 secciones en orden, columna Test en §7 y bloque Evidencia (AC-10)."""
    text = page.read_text(encoding="utf-8")
    assert _sections(page) == list(range(1, 9))
    assert "| ID | Dado | Cuando | Entonces | Test |" in text
    assert EVIDENCE in text


@pytest.mark.parametrize("page", _pages("api"), ids=_ids(_pages("api")))
def test_api_pages_follow_archetype_2(page: Path) -> None:
    """Arq. 2: 6 secciones en orden y bloque Evidencia (AC-10)."""
    assert _sections(page) == list(range(1, 7))
    assert EVIDENCE in page.read_text(encoding="utf-8")


def test_reference_follows_archetype_12() -> None:
    """Arq. 12: 6 secciones, Evidencia y entrada en el nav (AC-09)."""
    page = DOCS / "reference" / "index.md"
    assert _sections(page) == list(range(1, 7))
    assert EVIDENCE in page.read_text(encoding="utf-8")
    assert "Referencia del Sistema: reference/index.md" in (ROOT / "mkdocs.yml").read_text(
        encoding="utf-8"
    )


def test_functional_map_follows_variant_1i() -> None:
    """Variante 1-I: 4 secciones, Evidencia y una fila por página funcional."""
    page = DOCS / "functional" / "index.md"
    text = page.read_text(encoding="utf-8")
    assert _sections(page) == [1, 2, 3, 4]
    assert EVIDENCE in text
    for functional in _pages("functional"):
        assert f"]({functional.name})" in text, functional.name


def test_every_script_has_functional_technical_and_example_pages() -> None:
    """Cada módulo de scripts/ tiene Arquetipos 1, 2 y 4 (AC-01)."""
    for script in sorted((ROOT / "scripts").glob("*.py")):
        if script.stem in UNDOCUMENTED_SCRIPTS:
            continue
        example = EXAMPLE_FOR.get(script.stem, f"{script.stem}_usage")
        assert (DOCS / "functional" / f"{script.stem}.md").is_file(), script.stem
        assert (DOCS / "api" / f"{script.stem}.md").is_file(), script.stem
        assert (DOCS / "examples" / f"{example}.md").is_file(), script.stem


@pytest.mark.parametrize("page", _pages("api"), ids=_ids(_pages("api")))
def test_api_and_example_link_both_ways(page: Path) -> None:
    """Enlace bidireccional Arq. 2 §5 ↔ Arq. 4 §5 (AC-02)."""
    section5 = page.read_text(encoding="utf-8").split("## 5.", 1)[1].split("## 6.", 1)[0]
    examples = set(re.findall(r"\.\./examples/([\w]+\.md)", section5))
    assert examples or "Pendiente" in section5
    for example in examples:
        back = (DOCS / "examples" / example).read_text(encoding="utf-8")
        assert f"../api/{page.name}" in back, f"{example} no enlaza a api/{page.name}"


@pytest.mark.parametrize(
    "page",
    [p for p in DOCS.rglob("*.md") if SECTION_RE.search(p.read_text(encoding="utf-8"))],
    ids=lambda p: p.relative_to(DOCS).as_posix(),
)
def test_numbered_sections_are_never_empty(page: Path) -> None:
    """Ninguna sección numerada queda vacía: se escribe «No aplica» (AC-04)."""
    # Los bloques de código cuentan como contenido, pero sus líneas no deben leerse como títulos.
    text = re.sub(r"```.*?```", "[código]", page.read_text(encoding="utf-8"), flags=re.S)
    parts = re.split(r"^## \d+\. .*$", text, flags=re.M)[1:]
    for i, body in enumerate(parts, 1):
        content = re.split(r"^## ", body, flags=re.M)[0].strip()
        assert content, f"§{i} vacía"


def test_no_normative_archetype_without_normative() -> None:
    """Sin normativa de referencia, no hay docs/normativa/ ni entrada en el nav (AC-03)."""
    assert not (DOCS / "normativa").exists()
    assert "normativa/" not in (ROOT / "mkdocs.yml").read_text(encoding="utf-8")


def test_changelog_follows_keep_a_changelog() -> None:
    """Arq. 9: Keep a Changelog con sección [Unreleased] (AC-05)."""
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "keepachangelog.com" in text
    assert "## [Unreleased]" in text


def test_ai_config_has_seven_sections() -> None:
    """Arq. 10: cada página de docs/ai-config/ tiene las 7 secciones (AC-06)."""
    pages = sorted((DOCS / "ai-config").glob("*.md"))
    assert pages
    for page in pages:
        assert _sections(page) == list(range(1, 8)), page.name


def test_contributing_has_six_sections() -> None:
    """Arq. 11: CONTRIBUTING.md tiene las 6 secciones (AC-07)."""
    assert _sections(ROOT / "CONTRIBUTING.md") == list(range(1, 7))


def test_mermaid_nodes_do_not_start_with_slash() -> None:
    """`[/texto` abre un nodo paralelogramo en Mermaid 11 → «Syntax error in text» al renderizar.

    Regla de `document_project.prompt.md` (Mermaid — sintaxis de nodos); `--strict` no la detecta.
    """
    offenders = []
    for page in sorted(DOCS.rglob("*.md")):
        text = page.read_text(encoding="utf-8")
        for block in re.findall(r"^```mermaid\n(.*?)^```", text, flags=re.M | re.S):
            offenders += [
                f"{page.relative_to(DOCS).as_posix()}: {line.strip()}"
                for line in block.splitlines()
                if re.search(r"\[/", line)
            ]
    assert not offenders, offenders


def test_guides_naming_convention() -> None:
    """Guías en minúsculas con guion bajo y sin subcarpetas; how-to ≠ tutorial (AC-08)."""
    guides = DOCS / "guides"
    assert not [p for p in guides.iterdir() if p.is_dir()]
    for guide in guides.glob("*.md"):
        assert re.fullmatch(r"[a-z0-9_]+\.md", guide.name), guide.name
        assert not ("_howto" in guide.stem and "_tutorial" in guide.stem), guide.name
