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
# Regla única de fuentes convertidas en el destino (Fase 0c, Paso 5 del producto).
SOURCES_PATH = "_fuentes/<nombre_origen>/<ruta relativa al origen>"
SOURCES_RULE_FILES = [
    ".github/prompts/document_project.prompt.md",
    ".claude/commands/document-project.md",
    ".github/agents/documentation-generator.agent.md",
    ".github/SHARED_INSTRUCTIONS.md",
]
NON_CANONICAL_SOURCES_RE = re.compile(r"(?<!\w)\.?fuentes/")
FORBIDDING_RE = re.compile(r"Prohibido|Ningún otro nombre|[Mm]igra|no canónico")
# Instrucciones de visualización en la raíz del destino (Fase 7c del producto).
VIEW_TEMPLATE = ".github/templates/VER_DOCUMENTACION.template.md"
VIEW_SECTIONS = list(range(8))
PLACEHOLDER_RE = re.compile(r"\{[a-z_]+\}")


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


MERMAID_RE = re.compile(r"^```mermaid\n(.*?)^```", re.M | re.S)
# Mermaid no decodifica entidades HTML: `&#40;` se pinta como `&(`. Su sintaxis es `#40;`.
HTML_ENTITY_RE = re.compile(r"&#?[A-Za-z0-9]+;")
# Label sin comillas de `[...]` o `{...}` (no formas compuestas como `[(`, `[[`, `{{`, `[/`).
UNQUOTED_LABEL_RE = re.compile(r"(?<=\w)[\[{](?![\"(\[{/\\])([^\]}\n\"]*?)[\]}]")


def _mermaid_blocks() -> list[tuple[str, str]]:
    return [
        (page.relative_to(DOCS).as_posix(), block)
        for page in sorted(DOCS.rglob("*.md"))
        for block in MERMAID_RE.findall(page.read_text(encoding="utf-8"))
    ]


def test_mermaid_no_html_entities() -> None:
    """Sin entidades HTML en diagramas: Mermaid pinta un `&` sobrante (AC-11)."""
    offenders = [
        f"{page}: {line.strip()}"
        for page, block in _mermaid_blocks()
        for line in block.splitlines()
        if HTML_ENTITY_RE.search(line)
    ]
    assert not offenders, offenders


def test_mermaid_has_accessibility() -> None:
    """Todo diagrama declara `accTitle` y `accDescr` para lectores de pantalla (AC-13)."""
    offenders = [
        f"{page}: {block.splitlines()[0]}"
        for page, block in _mermaid_blocks()
        if not re.search(r"^\s*accTitle:\s*\S", block, re.M)
        or not re.search(r"^\s*accDescr(:\s*\S|\s*\{)", block, re.M)
    ]
    assert not offenders, offenders


def test_mermaid_special_chars_quoted() -> None:
    """`@ ( ) { }` en label de flowchart sin comillas → parse error en Mermaid 11 y 12 (AC-11)."""
    offenders = [
        f"{page}: {label}"
        for page, block in _mermaid_blocks()
        if block.split(maxsplit=1)[0] in {"flowchart", "graph"}
        for label in UNQUOTED_LABEL_RE.findall(block)
        if re.search(r"[@(){}]", label)
    ]
    assert not offenders, offenders


@pytest.mark.parametrize(
    ("line", "bad"),
    [
        ("A{¿x (y)?} --> B", True),
        ("A[x{y}] --> B", True),
        ("A[Cl@ve] --> B", True),
        ('A["Cl@ve (firma)"] --> B', False),
        ('C@{ shape: doc, label: "Doc" } --> A', False),
        ("A([Inicio]) --> B[(Base de datos)]", False),
        ("A[a#b] --> B[c: d]", False),
    ],
)
def test_unquoted_label_detector(line: str, bad: bool) -> None:
    """Fixtures calibradas renderizando con mermaid@11 y @12 (sesión 2026-10-28e)."""
    found = any(re.search(r"[@(){}]", lb) for lb in UNQUOTED_LABEL_RE.findall(line))
    assert found is bad


# Páginas del Arquetipo 6 (navegación principal): resumen de 8 nodos como máximo (§3.17).
LANDING_PAGES = {"index.md", "installation.md", "architecture.md", "quickstart.md"}
FLOW_SKIP = ("subgraph", "end", "direction", "classDef", "class ", "style", "linkStyle", "click")
SHAPE_RE = re.compile(r"\[[^\[\]]*\]|\([^()]*\)|\{[^{}]*\}")
EDGE_TEXT_RE = re.compile(r"(--|==)\s+[^-=>]+?\s+(-->|==>|---|===)|-\.\s*[^.]+?\s*\.->")


def _diagram_lines(block: str) -> list[str]:
    """Líneas del diagrama sin la cabecera, comentarios ni `accTitle`/`accDescr`."""
    body = re.sub(r"^\s*accDescr\s*\{.*?\}", "", block, flags=re.M | re.S)
    return [
        line.strip()
        for line in body.splitlines()[1:]
        if line.strip() and not re.match(r"\s*(%%|accTitle|accDescr)", line)
    ]


def _flowchart_nodes(lines: list[str]) -> set[str]:
    groups = {m.group(1) for line in lines if (m := re.match(r"subgraph\s+(\w+)", line))}
    nodes: set[str] = set()
    for line in lines:
        if line.startswith(FLOW_SKIP):
            continue
        text = re.sub(r"\|[^|]*\|", " ", re.sub(r'"[^"]*"', "", line))
        while SHAPE_RE.search(text):
            text = SHAPE_RE.sub(" ", text)
        text = EDGE_TEXT_RE.sub(" --> ", text)
        nodes |= set(re.findall(r"[A-Za-z_]\w*", text)) - groups
    return nodes


def _mermaid_nodes(block: str) -> int:
    """Nodos según §3.17: IDs, participantes, estados o entidades (0 si no aplica)."""
    kind, lines = block.split(maxsplit=1)[0], _diagram_lines(block)
    if kind in {"flowchart", "graph"}:
        return len(_flowchart_nodes(lines))
    found: set[str] = set()
    for line in lines:
        if kind == "sequenceDiagram":
            m = re.match(r"(?:participant|actor)\s+(\w+)", line) or re.match(
                r"(\w+)\s*[-<>x)]+[+-]?\s*(\w+)\s*:", line
            )
        elif kind == "stateDiagram-v2":
            m = re.match(r"state\s+(?:\"[^\"]*\"\s+as\s+)?(\w+)", line) or re.match(
                r"(\[\*\]|\w+)\s*-->\s*(\[\*\]|\w+)", line
            )
        elif kind == "erDiagram":
            m = re.match(r"([\w-]+)\s+[|}o{.-]+\s+([\w-]+)\s*:", line) or re.match(
                r"([\w-]+)\s*\{", line
            )
        else:
            return 0
        if m:
            found |= {g for g in m.groups() if g and g != "[*]"}
    return len(found)


@pytest.mark.parametrize(
    ("block", "expected"),
    [
        ("flowchart TD\n A[x] -- No, y vigente --> B{y}\n B -->|z| C & D", 4),
        ("flowchart TD\n subgraph S[t]\n A --> B\n end\n X --> S", 3),
        ('flowchart TD\n accTitle: t\n A["a (b) -- c"] -. git push .-> B@{ shape: doc }', 2),
        ("sequenceDiagram\n actor U as Usuario\n participant A\n U->>A: hola\n A-->>B: x", 3),
        ('stateDiagram-v2\n state "x" as S1\n [*] --> S1\n S1 --> S2 : ok\n S2 --> [*]', 2),
        ('erDiagram\n A ||--o{ B : "x"\n B }o--|| C : y', 3),
        ("gitGraph\n commit", 0),
    ],
)
def test_mermaid_node_counter(block: str, expected: int) -> None:
    """El contador de nodos de §3.17 sobre casos límite de cada tipo de diagrama."""
    assert _mermaid_nodes(block) == expected


def test_mermaid_max_nodes() -> None:
    """≤12 nodos por diagrama y ≤8 en las páginas del Arquetipo 6 (AC-12)."""
    offenders = [
        f"{page}: {n} nodos"
        for page, block in _mermaid_blocks()
        if (n := _mermaid_nodes(block)) > (8 if page in LANDING_PAGES else 12)
    ]
    assert not offenders, offenders


def test_guides_naming_convention() -> None:
    """Guías en minúsculas con guion bajo y sin subcarpetas; how-to ≠ tutorial (AC-08)."""
    guides = DOCS / "guides"
    assert not [p for p in guides.iterdir() if p.is_dir()]
    for guide in guides.glob("*.md"):
        assert re.fullmatch(r"[a-z0-9_]+\.md", guide.name), guide.name
        assert not ("_howto" in guide.stem and "_tutorial" in guide.stem), guide.name


@pytest.mark.parametrize("path", SOURCES_RULE_FILES)
def test_sources_folder_is_canonical(path: str) -> None:
    """Las instrucciones fijan `_fuentes/`; otros nombres solo aparecen para prohibir o migrar."""
    text = (ROOT / path).read_text(encoding="utf-8")
    assert SOURCES_PATH in text
    for match in NON_CANONICAL_SOURCES_RE.finditer(text):
        window = text[max(0, match.start() - 200) : match.end() + 200]
        assert FORBIDDING_RE.search(window), f"{path}: {match.group()} sin prohibición ni migración"


@pytest.mark.parametrize("path", SOURCES_RULE_FILES)
def test_view_instructions_rule_everywhere(path: str) -> None:
    """La Fase 7c (instrucciones de visualización) está en las cuatro fuentes de instrucciones."""
    text = (ROOT / path).read_text(encoding="utf-8")
    assert "VER_DOCUMENTACION.md" in text
    assert "VER_DOCUMENTACION.template.md" in text


def test_view_template_has_fixed_sections() -> None:
    assert _sections(ROOT / VIEW_TEMPLATE) == VIEW_SECTIONS


def test_view_instructions_filled_for_doc_ia() -> None:
    """Dogfooding: la instancia de doc_ia tiene las secciones fijas y ningún marcador pendiente."""
    text = (ROOT / "VER_DOCUMENTACION.md").read_text(encoding="utf-8")
    assert _sections(ROOT / "VER_DOCUMENTACION.md") == VIEW_SECTIONS
    assert not PLACEHOLDER_RE.findall(text)
    assert "PLANTILLA" not in text


def test_downloads_never_offers_opening_index_html() -> None:
    """Con `use_directory_urls: true`, abrir `index.html` sin servidor no navega."""
    text = (DOCS / "downloads.md").read_text(encoding="utf-8")
    for match in re.finditer(r"index\.html", text):
        window = text[max(0, match.start() - 200) : match.end() + 200]
        assert re.search(r"no funciona|[Nn]unca|Prohibido", window), window


@pytest.mark.parametrize("path", SOURCES_RULE_FILES)
def test_incremental_mode_rule_everywhere(path: str) -> None:
    """Modo incremental: `changes` en la Fase 1 y `baseline` en el CIERRE, con el mismo estado."""
    text = (ROOT / path).read_text(encoding="utf-8")
    assert ".ai/doc_state.json" in text
    assert "baseline" in text
