#!/usr/bin/env python3
"""Trazabilidad determinista entre la documentación y el código de un repositorio.

Subcomandos (no invoca ningún servicio IA ni accede a la red):

  drift   Compara las huellas SHA256 guardadas en el frontmatter de cada página con las
          fuentes actuales y lista las páginas desactualizadas.
  stamp   Calcula y escribe las huellas de las fuentes de una página (frontmatter).
  matrix  Cruza los criterios de aceptación (AC-xx, columna Test) de docs/functional/ con
          los tests reales de tests/ y lista tests citados inexistentes y tests sin citar.
  llms    Genera docs/llms.txt (formato llmstxt.org) a partir del nav de mkdocs.yml.
  decisions  Cruza los registros docs/decisiones/<ámbito>_decisiones.md (Arquetipo 13) con las
          páginas que citan sus IDs COB-<ÁMBITO>-<NNN>: fichas duplicadas, huérfanas, inválidas
          o incompletas y decisiones tomadas que la documentación aún no refleja.
  baseline  Guarda en <destino>/.ai/doc_state.json el commit actual de un origen (CIERRE de
          /document-project).
  changes Lista los ficheros del origen cambiados desde su baseline (git local) y las páginas
          del destino que los citan: el INVENTARIO del modo incremental.

Frontmatter de trazabilidad (DOCUMENTATION_STANDARD.md §3.16):

    ---
    arquetipo: "2"
    fuentes:
      scripts/check_env.py: 3f2a9c1b0d4e
    revisado: 2026-10-28
    ---

Uso:
    python scripts/doc_trace.py drift
    python scripts/doc_trace.py stamp docs/api/check_env.md --source scripts/check_env.py
    python scripts/doc_trace.py matrix --output dist/traceability.md
    python scripts/doc_trace.py llms --check
    python scripts/doc_trace.py decisions --output dist/decisions.md
    python scripts/doc_trace.py --root <destino> baseline --origin <origen>
    python scripts/doc_trace.py --root <destino> changes --origin <origen>
    python scripts/doc_trace.py --root <destino> baseline --origin <repo> --path <a> --path <b>

``--path`` (repetible, pathspec de git relativo al origen) limita ``baseline``/``changes`` a un
alcance transversal dentro de un repositorio mayor (p. ej. un módulo funcional repartido entre
varios módulos Maven). El baseline guarda esas rutas (``rutas``) y ``changes`` las reutiliza.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import posixpath
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass, field, replace
from datetime import date
from pathlib import Path
from typing import Any, Literal

ROOT = Path(__file__).resolve().parent.parent

HASH_LENGTH = 12
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)
STAMP_KEYS = frozenset({"arquetipo", "fuentes", "decisiones", "revisado"})  # las reescribe stamp
AC_ROW_RE = re.compile(r"^\|\s*(AC-\d+)\s*\|")
TEST_ID_RE = re.compile(r"tests/[\w/]+\.py::[\w:]+")

DriftStatus = Literal["stale", "missing", "outside_repo", "unsealed"]


@dataclass(frozen=True)
class PageMeta:
    """Frontmatter de trazabilidad de una página."""

    page: Path
    archetype: str
    sources: dict[str, str]
    reviewed: str
    # Registros de decisiones enlazados (Arquetipo 13): ruta relativa a la página → huella.
    registers: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class DriftFinding:
    """Fuente de una página cuya huella no coincide con el estado actual."""

    page: Path
    source: str
    status: DriftStatus


@dataclass(frozen=True)
class CriterionRow:
    """Criterio de aceptación de una página funcional y los tests que cita."""

    page: Path
    criterion: str
    tests: tuple[str, ...]


# ---------------------------------------------------------------------------
# YAML (PyYAML llega con mkdocs; sin stubs tipados)
# ---------------------------------------------------------------------------


def _load_yaml(text: str) -> Any:
    """Carga YAML ignorando tags de Python (`!!python/name:`) y `!ENV` de mkdocs.yml."""
    import yaml  # type: ignore[import-untyped]  # noqa: PLC0415

    class _Loader(yaml.SafeLoader):  # type: ignore[misc]
        pass

    def _ignore(loader: Any, suffix: str, node: Any) -> None:
        return None

    _Loader.add_multi_constructor("tag:yaml.org,2002:python/", _ignore)
    _Loader.add_multi_constructor("!", _ignore)
    return yaml.load(text, Loader=_Loader)  # noqa: S506 — loader seguro derivado de SafeLoader


# ---------------------------------------------------------------------------
# Huellas y frontmatter
# ---------------------------------------------------------------------------


def fingerprint(path: Path) -> str:
    """Huella SHA256 (12 hex) del fichero con saltos de línea normalizados a LF.

    En fuentes Markdown se excluye el frontmatter: sellar una página que es fuente de otra
    no debe marcar a esta última como desactualizada.
    """
    data = path.read_bytes().replace(b"\r\n", b"\n")
    if path.suffix == ".md":
        text = data.decode("utf-8")
        data = FRONTMATTER_RE.sub("", text, count=1).encode("utf-8")
    return hashlib.sha256(data).hexdigest()[:HASH_LENGTH]


def read_page_meta(page: Path) -> PageMeta | None:
    """Lee el frontmatter de trazabilidad; ``None`` si no declara ``fuentes`` ni ``decisiones``."""
    match = FRONTMATTER_RE.match(page.read_text(encoding="utf-8"))
    if match is None:
        return None
    data = _load_yaml(match.group(1))
    if not isinstance(data, dict):
        return None
    raw_sources, raw_registers = data.get("fuentes"), data.get("decisiones")
    if not isinstance(raw_sources, dict) and not isinstance(raw_registers, dict):
        return None
    sources = {str(k): str(v) for k, v in (raw_sources or {}).items()}
    registers = {str(k): str(v) for k, v in (raw_registers or {}).items()}
    return PageMeta(
        page=page,
        archetype=str(data.get("arquetipo", "")),
        sources=sources,
        reviewed=str(data.get("revisado", "")),
        registers=registers,
    )


def linked_registers(page: Path) -> list[str]:
    """Registros de decisiones que la página enlaza desde un ID ``COB-…`` (fuera de código).

    Cada ruta se devuelve tal como la escribe el enlace, normalizada y relativa a la página:
    sirve igual si la documentación vive en otro repositorio que el código.
    """
    found: set[str] = set()
    for _, text in _code_free_lines(page):
        for href in REGISTER_LINK_RE.findall(text):
            found.add(posixpath.normpath(href))
    return sorted(found)


def _resolve_source(source: str, repo_root: Path) -> Path | None:
    """Ruta absoluta de la fuente si está dentro del repositorio; ``None`` si sale de él."""
    resolved = (repo_root / source).resolve()
    return resolved if resolved.is_relative_to(repo_root.resolve()) else None


def _unmanaged_frontmatter(text: str) -> tuple[str, list[str]]:
    """(arquetipo, líneas literales de las claves que ``stamp`` no gestiona) del frontmatter.

    Las claves propias de la página (``ambito`` de un registro, etiquetas…) se conservan tal cual.
    """
    match = FRONTMATTER_RE.match(text)
    if match is None:
        return "", []
    data = _load_yaml(match.group(1))
    archetype = str(data.get("arquetipo", "")) if isinstance(data, dict) else ""
    kept: list[str] = []
    keep = False
    for line in match.group(1).splitlines():
        if line and not line[0].isspace():
            keep = line.split(":", 1)[0].strip() not in STAMP_KEYS
        if keep:
            kept.append(line)
    return archetype, kept


def format_frontmatter(meta: PageMeta, extra: list[str] | None = None) -> str:
    """Serializa el frontmatter de trazabilidad con orden estable de fuentes y registros.

    ``extra``: líneas de otras claves de la página, que se escriben tras ``arquetipo``.
    """
    lines = ["---", f'arquetipo: "{meta.archetype}"', *(extra or [])]
    if meta.sources:
        lines.append("fuentes:")
        lines += [f"  {src}: {digest}" for src, digest in sorted(meta.sources.items())]
    if meta.registers:
        lines.append("decisiones:")
        lines += [f"  {reg}: {digest}" for reg, digest in sorted(meta.registers.items())]
    lines += [f"revisado: {meta.reviewed}", "---", ""]
    return "\n".join(lines)


def stamp_page(
    page: Path,
    repo_root: Path,
    *,
    sources: list[str] | None = None,
    archetype: str | None = None,
    reviewed: str | None = None,
) -> PageMeta:
    """Recalcula las huellas de las fuentes y de los registros enlazados de ``page``.

    Los registros de decisiones (Arquetipo 13) se detectan a partir de los enlaces de sus IDs
    ``COB-…``; una página que solo enlaza registros puede sellarse sin ``--source``.
    """
    current = read_page_meta(page)
    names = sources if sources else sorted(current.sources) if current else []
    registers: dict[str, str] = {}
    for href in linked_registers(page):
        target = (page.parent / href).resolve()
        if not target.is_file():
            raise ValueError(f"{page}: el registro enlazado {href} no existe")
        registers[href] = fingerprint(target)
    if not names and not registers:
        raise ValueError(f"{page}: sin fuentes (usa --source)")
    digests: dict[str, str] = {}
    for name in names:
        resolved = _resolve_source(name, repo_root)
        if resolved is None:
            raise ValueError(f"{page}: la fuente {name} está fuera del repositorio")
        if not resolved.is_file():
            raise ValueError(f"{page}: la fuente {name} no existe")
        digests[name] = fingerprint(resolved)
    text = page.read_text(encoding="utf-8")
    old_archetype, extra = _unmanaged_frontmatter(text)
    meta = PageMeta(
        page=page,
        archetype=archetype or (current.archetype if current else "") or old_archetype,
        sources=digests,
        reviewed=reviewed or date.today().isoformat(),
        registers=registers,
    )
    body = FRONTMATTER_RE.sub("", text, count=1)
    page.write_text(format_frontmatter(meta, extra) + body, encoding="utf-8", newline="\n")
    return meta


def check_drift(docs_dir: Path, repo_root: Path) -> list[DriftFinding]:
    """Lista, en orden estable, las fuentes cuya huella ya no coincide."""
    findings: list[DriftFinding] = []
    for page in sorted(docs_dir.rglob("*.md")):
        meta = read_page_meta(page)
        sealed = meta.registers if meta else {}
        for href in linked_registers(page):
            if href not in sealed:
                findings.append(DriftFinding(page, href, "unsealed"))
        for href, stored in sorted(sealed.items()):
            target = (page.parent / href).resolve()
            if not target.is_file():
                findings.append(DriftFinding(page, href, "missing"))
            elif fingerprint(target) != stored:
                findings.append(DriftFinding(page, href, "stale"))
        if meta is None:
            continue
        for source, stored in sorted(meta.sources.items()):
            resolved = _resolve_source(source, repo_root)
            if resolved is None:
                findings.append(DriftFinding(page, source, "outside_repo"))
            elif not resolved.is_file():
                findings.append(DriftFinding(page, source, "missing"))
            elif fingerprint(resolved) != stored:
                findings.append(DriftFinding(page, source, "stale"))
    return findings


# ---------------------------------------------------------------------------
# Matriz criterios ↔ tests
# ---------------------------------------------------------------------------


def collect_test_ids(tests_dir: Path, repo_root: Path) -> set[str]:
    """Ids ``tests/x.py::test_y`` (y ``::Clase::test_y``) definidos en ``tests_dir``."""
    ids: set[str] = set()
    for path in sorted(tests_dir.rglob("test_*.py")):
        rel = path.relative_to(repo_root).as_posix()
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                ids.add(f"{rel}::{node.name}")
            elif isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name.startswith("test_"):
                        ids.add(f"{rel}::{node.name}::{item.name}")
    return ids


def collect_criteria(functional_dir: Path) -> list[CriterionRow]:
    """Filas ``| AC-xx | … |`` de las páginas funcionales con los tests de su última columna."""
    rows: list[CriterionRow] = []
    for page in sorted(functional_dir.glob("*.md")):
        for line in page.read_text(encoding="utf-8").splitlines():
            match = AC_ROW_RE.match(line)
            if match is None:
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            tests = tuple(TEST_ID_RE.findall(cells[-1])) if len(cells) >= 5 else ()
            rows.append(CriterionRow(page, match.group(1), tests))
    return rows


def build_matrix(
    criteria: list[CriterionRow], test_ids: set[str], repo_root: Path
) -> tuple[str, list[str]]:
    """Devuelve (Markdown de la matriz, tests citados inexistentes)."""
    cited = {t for row in criteria for t in row.tests}
    unknown = sorted(cited - test_ids)
    lines = [
        "# Matriz de Trazabilidad — Criterios ↔ Tests",
        "",
        "| Página | Criterios | Con test | Tests citados |",
        "|---|---|---|---|",
    ]
    pages = sorted({row.page for row in criteria})
    for page in pages:
        page_rows = [r for r in criteria if r.page == page]
        with_test = sum(1 for r in page_rows if r.tests)
        n_tests = len({t for r in page_rows for t in r.tests})
        rel = page.relative_to(repo_root).as_posix()
        lines.append(f"| `{rel}` | {len(page_rows)} | {with_test} | {n_tests} |")
    total = len(criteria)
    total_with = sum(1 for r in criteria if r.tests)
    lines += ["", f"**Total**: {total_with}/{total} criterios con test."]
    lines += ["", "## Tests citados inexistentes", ""]
    lines += [f"- `{t}`" for t in unknown] or ["*Ninguno.*"]
    uncited = sorted(test_ids - cited)
    lines += ["", f"## Tests sin criterio de aceptación ({len(uncited)})", ""]
    lines += [f"- `{t}`" for t in uncited] or ["*Ninguno.*"]
    return "\n".join(lines) + "\n", unknown


# ---------------------------------------------------------------------------
# llms.txt
# ---------------------------------------------------------------------------


def _page_url(md_path: str, site_url: str | None, directory_urls: bool) -> str:
    """URL publicada de una página del nav (relativa al sitio si no hay ``site_url``)."""
    stem = md_path.removesuffix(".md")
    if not directory_urls:
        rel = stem + ".html"
    elif stem == "index" or stem.endswith("/index"):
        rel = stem.removesuffix("index")
    else:
        rel = stem + "/"
    return (site_url.rstrip("/") + "/" + rel) if site_url else (rel or "./")


def _nav_entries(items: list[Any], prefix: str = "") -> list[tuple[str, str]]:
    """Aplana el nav en (título, ruta .md); los grupos anidados se encadenan con « › »."""
    entries: list[tuple[str, str]] = []
    for item in items:
        if isinstance(item, str):
            entries.append((prefix + item, item))
            continue
        if not isinstance(item, dict):
            continue
        for title, value in item.items():
            label = f"{prefix}{title}"
            if isinstance(value, str):
                entries.append((label, value))
            elif isinstance(value, list):
                entries += _nav_entries(value, f"{label} › ")
    return entries


def build_llms_txt(mkdocs_yml: Path, site_url: str | None = None) -> str:
    """Genera el contenido de ``llms.txt`` a partir de ``site_name`` y ``nav``."""
    config = _load_yaml(mkdocs_yml.read_text(encoding="utf-8"))
    if not isinstance(config, dict) or not isinstance(config.get("nav"), list):
        raise ValueError(f"{mkdocs_yml}: sin sección nav")
    url = site_url if site_url is not None else config.get("site_url")
    directory_urls = bool(config.get("use_directory_urls", True))
    lines = [f"# {config.get('site_name', 'Documentación')}", ""]
    if config.get("site_description"):
        lines += [f"> {config['site_description']}", ""]
    loose: list[tuple[str, str]] = []
    sections: list[tuple[str, list[tuple[str, str]]]] = []
    for item in config["nav"]:
        if isinstance(item, dict):
            for title, value in item.items():
                if isinstance(value, list):
                    sections.append((str(title), _nav_entries(value)))
                elif isinstance(value, str):
                    loose.append((str(title), value))
        elif isinstance(item, str):
            loose.append((item, item))
    if loose:
        sections.insert(0, ("Páginas principales", loose))
    for title, entries in sections:
        lines += [f"## {title}", ""]
        lines += [
            f"- [{label}]({_page_url(path, url, directory_urls)})"
            for label, path in entries
            if path.endswith(".md")
        ]
        lines.append("")
    return "\n".join(lines).rstrip("\n") + "\n"


# ---------------------------------------------------------------------------
# Modo incremental: baseline del origen y cambios desde él (git local)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OriginChange:
    """Fichero del origen cambiado desde el baseline (``R`` conserva la ruta anterior)."""

    kind: str
    path: str
    old_path: str | None = None


@dataclass(frozen=True)
class OriginBaseline:
    """Estado del origen al cerrar una sesión de documentación."""

    commit: str | None
    branch: str | None
    dirty: bool
    date: str
    paths: tuple[str, ...] = (".",)


@dataclass(frozen=True)
class ChangeReport:
    """Resultado de ``changes``: cambios y páginas que citan cada fichero cambiado.

    ``status`` distinto de ``ok`` indica que no hay baseline utilizable y el flujo debe
    ejecutarse en modo completo; ``reason`` lo explica.
    """

    status: Literal["ok", "fallback"]
    reason: str
    base: str | None
    changes: tuple[OriginChange, ...] = ()
    pages: dict[str, tuple[Path, ...]] | None = None
    mentions: dict[str, tuple[Path, ...]] | None = None
    examples: tuple[Path, ...] = ()


# Artefactos que genera la propia documentación: si el destino está dentro del origen, sus
# cambios no son cambios del código documentado.
DOC_ARTIFACTS = (".ai", "_fuentes", "mkdocs.yml", "VER_DOCUMENTACION.md", "VIEW_DOCS.md")
GIT_TIMEOUT = 60
DEFAULT_PATHS: tuple[str, ...] = (".",)
EXAMPLE_LINK_RE = re.compile(r"\]\(([^)#\s]*examples/[^)#\s]+\.md)")
EVIDENCE_MARKER = '??? note "Evidencia"'


def _git(origin: Path, *args: str) -> bytes | None:
    """Salida de ``git -C origin …``; ``None`` si git no está o el comando falla."""
    try:
        result = subprocess.run(
            ["git", "-C", str(origin), *args],
            capture_output=True,
            timeout=GIT_TIMEOUT,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout if result.returncode == 0 else None


def _doc_ia_version() -> str:
    with (ROOT / "pyproject.toml").open("rb") as fh:
        version: str = tomllib.load(fh)["project"]["version"]
    return version


def _minor(version: str) -> str:
    return ".".join(version.split(".")[:2])


def documentation_paths(origin: Path, docs_dir: Path) -> tuple[str, ...]:
    """Rutas (POSIX, relativas al origen) de los artefactos de documentación dentro del origen."""
    origin = origin.resolve()
    dest_root = docs_dir.resolve().parent
    candidates = [docs_dir.resolve(), *(dest_root / name for name in DOC_ARTIFACTS)]
    excluded: list[str] = []
    for path in candidates:
        if path.is_relative_to(origin) and path != origin:
            excluded.append(path.relative_to(origin).as_posix())
    return tuple(sorted(excluded))


def _is_excluded(path: str, excluded: tuple[str, ...]) -> bool:
    return any(path == e or path.startswith(e + "/") for e in excluded)


def changed_files(
    origin: Path,
    base: str,
    excluded: tuple[str, ...] = (),
    paths: tuple[str, ...] = DEFAULT_PATHS,
) -> list[OriginChange] | None:
    """Cambios del árbol de trabajo frente a ``base`` (confirmados, pendientes y sin seguimiento).

    Rutas relativas al origen aunque sea una subcarpeta del repositorio. ``paths`` son pathspecs
    de git relativos al origen (alcance transversal). ``None`` si git falla.
    """
    spec = paths or DEFAULT_PATHS
    diff = _git(origin, "diff", "--name-status", "-z", "-M", "--relative", base, "--", *spec)
    untracked = _git(origin, "ls-files", "--others", "--exclude-standard", "-z", "--", *spec)
    if diff is None or untracked is None:
        return None
    fields = diff.decode("utf-8").split("\0")
    changes: list[OriginChange] = []
    i = 0
    while i < len(fields) - 1:
        kind = fields[i][:1]
        if kind == "R":
            changes.append(OriginChange("R", fields[i + 2], fields[i + 1]))
            i += 3
        elif kind == "C":  # copia: el fichero nuevo es un alta
            changes.append(OriginChange("A", fields[i + 2]))
            i += 3
        else:
            changes.append(OriginChange(kind, fields[i + 1]))
            i += 2
    changes += [OriginChange("A", p) for p in untracked.decode("utf-8").split("\0") if p]
    kept = [
        c
        for c in changes
        if not _is_excluded(c.path, excluded)
        or (c.old_path is not None and not _is_excluded(c.old_path, excluded))
    ]
    return sorted(kept, key=lambda c: (c.path, c.kind))


def _detached_ref(origin: Path) -> str | None:
    """Rama local o remota que apunta al HEAD desacoplado, si es única (sin ``*/HEAD``)."""
    out = _git(
        origin,
        "for-each-ref",
        "--points-at",
        "HEAD",
        "--format=%(refname:short)",
        "refs/heads",
        "refs/remotes",
    )
    if out is None:
        return None
    refs = [r for r in out.decode().split() if r and not r.endswith("/HEAD")]
    return refs[0] if len(refs) == 1 else None


def take_baseline(
    origin: Path,
    excluded: tuple[str, ...] = (),
    today: str | None = None,
    paths: tuple[str, ...] = DEFAULT_PATHS,
) -> OriginBaseline:
    """Commit, rama y si hay cambios sin confirmar (fuera de ``excluded``) en el alcance."""
    day = today or date.today().isoformat()
    spec = tuple(sorted(paths)) if paths else DEFAULT_PATHS
    head = _git(origin, "rev-parse", "HEAD")
    if head is None:
        return OriginBaseline(commit=None, branch=None, dirty=False, date=day, paths=spec)
    commit = head.decode().strip()
    branch_out = _git(origin, "rev-parse", "--abbrev-ref", "HEAD")
    branch = branch_out.decode().strip() if branch_out else None
    if (
        branch == "HEAD"
    ):  # desacoplado (p. ej. worktree en origin/<ref>): la única ref que apunta aquí
        branch = _detached_ref(origin) or branch
    pending = changed_files(origin, "HEAD", excluded, spec)
    return OriginBaseline(commit, branch, bool(pending), day, spec)


def read_state(state_path: Path) -> dict[str, Any]:
    """Estado del destino (``.ai/doc_state.json``); vacío si no existe."""
    if not state_path.is_file():
        return {}
    data = json.loads(state_path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def write_baseline(state_path: Path, name: str, baseline: OriginBaseline) -> None:
    """Guarda el baseline de un origen conservando los de los demás orígenes."""
    stored = read_state(state_path).get("origenes")
    origins: dict[str, Any] = stored if isinstance(stored, dict) else {}
    entry: dict[str, Any] = {
        "commit": baseline.commit,
        "rama": baseline.branch,
        "sucio": baseline.dirty,
        "fecha": baseline.date,
    }
    if baseline.paths != DEFAULT_PATHS:  # solo con alcance transversal: compatible hacia atrás
        entry["rutas"] = list(baseline.paths)
    origins[name] = entry
    state = {"doc_ia": _doc_ia_version(), "origenes": dict(sorted(origins.items()))}
    state_path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(state, indent=2, ensure_ascii=False) + "\n"
    state_path.write_text(text, encoding="utf-8", newline="\n")


def _citation_re(path: str, name: str) -> re.Pattern[str]:
    """Cita de ``path`` (o ``name/path``) como ruta completa, no como sufijo de otra ruta."""
    options = "|".join(re.escape(p) for p in (f"{name}/{path}", path))
    return re.compile(rf"(?<![\w./-])(?:{options})(?![\w.-])")


def _split_citations(text: str) -> tuple[str, str]:
    """(zona de citas, resto): frontmatter ``fuentes`` + bloque "Evidencia" frente al cuerpo."""
    match = FRONTMATTER_RE.match(text)
    frontmatter = match.group(0) if match else ""
    body = text[len(frontmatter) :]
    head, marker, evidence = body.partition(EVIDENCE_MARKER)
    return frontmatter + marker + evidence, head


def pages_citing(
    docs_dir: Path, paths: list[str], name: str
) -> tuple[dict[str, tuple[Path, ...]], dict[str, tuple[Path, ...]]]:
    """Para cada ruta: (páginas que la citan como evidencia, páginas que solo la mencionan).

    Una cita (``fuentes:`` o bloque "Evidencia") obliga a revisar la página; una mención en el
    cuerpo (ADR, changelog, guías) solo se avisa: el cambio de un fichero no la invalida.
    """
    zones = {
        page: _split_citations(page.read_text(encoding="utf-8"))
        for page in sorted(docs_dir.rglob("*.md"))
    }
    cited: dict[str, tuple[Path, ...]] = {}
    mentioned: dict[str, tuple[Path, ...]] = {}
    for path in paths:
        pattern = _citation_re(path, name)
        cited[path] = tuple(p for p, (cites, _) in zones.items() if pattern.search(cites))
        mentioned[path] = tuple(
            p
            for p, (cites, rest) in zones.items()
            if pattern.search(rest) and not pattern.search(cites)
        )
    return cited, mentioned


def linked_examples(pages: list[Path], docs_dir: Path) -> tuple[Path, ...]:
    """Ejemplos enlazados desde páginas técnicas (§5, enlace bidireccional Arquetipo 2 ↔ 4)."""
    api_dir = (docs_dir / "api").resolve()
    found: set[Path] = set()
    for page in pages:
        if not page.resolve().is_relative_to(api_dir):
            continue
        for link in EXAMPLE_LINK_RE.findall(page.read_text(encoding="utf-8")):
            target = (page.parent / link).resolve()
            if target.is_file():
                found.add(target)
    return tuple(sorted(found - {p.resolve() for p in pages}))


def check_changes(
    origin: Path,
    docs_dir: Path,
    state_path: Path,
    name: str,
    scope: tuple[str, ...] | None = None,
) -> ChangeReport:
    """Cambios del origen desde su baseline y páginas del destino afectadas.

    ``scope`` (``--path``) debe coincidir con las rutas del baseline; si se omite, se usan las
    guardadas. Un alcance distinto obliga al modo completo: el baseline no lo cubre.
    """
    state = read_state(state_path)
    origins = state.get("origenes")
    entry = origins.get(name) if isinstance(origins, dict) else None
    if not isinstance(entry, dict):
        return ChangeReport("fallback", f"sin baseline para «{name}» en {state_path}", None)
    base = entry.get("commit")
    if not base:
        return ChangeReport("fallback", "el origen no estaba bajo git al tomar el baseline", None)
    stored_version = str(state.get("doc_ia", ""))
    if _minor(stored_version) != _minor(_doc_ia_version()):
        reason = f"doc_ia {stored_version} → {_doc_ia_version()}: reglas de arquetipos cambiadas"
        return ChangeReport("fallback", reason, base)
    if _git(origin, "cat-file", "-e", f"{base}^{{commit}}") is None:
        return ChangeReport("fallback", f"el commit {base[:12]} no está en el historial", base)
    stored = entry.get("rutas")
    stored_paths = tuple(sorted(str(p) for p in stored)) if isinstance(stored, list) else None
    baseline_paths = stored_paths or DEFAULT_PATHS
    if scope and tuple(sorted(scope)) != baseline_paths:
        reason = f"alcance --path distinto del baseline ({', '.join(baseline_paths)})"
        return ChangeReport("fallback", reason, base)
    excluded = documentation_paths(origin, docs_dir)
    changes = changed_files(origin, base, excluded, baseline_paths)
    if changes is None:
        return ChangeReport("fallback", "git no pudo calcular el diff del origen", base)
    paths = sorted({p for c in changes for p in (c.path, c.old_path) if p})
    pages, mentions = pages_citing(docs_dir, paths, name)
    affected = sorted({p for found in pages.values() for p in found})
    examples = linked_examples(affected, docs_dir)
    return ChangeReport("ok", "", base, tuple(changes), pages, mentions, examples)


def format_changes(report: ChangeReport, name: str, root: Path) -> str:
    """Informe Markdown de ``changes`` para el INVENTARIO."""
    base = (report.base or "—")[:12]
    lines = [f"# Cambios en el origen «{name}» desde {base}", ""]
    if report.status != "ok":
        return "\n".join(lines + [f"Modo completo: {report.reason}.", ""])
    if not report.changes:
        lines += ["*Sin cambios: todas las páginas siguen vigentes (estado C).*", ""]
        return "\n".join(lines)
    pages, mentions = report.pages or {}, report.mentions or {}

    def _for(found: dict[str, tuple[Path, ...]], change: OriginChange) -> list[Path]:
        return sorted({*found.get(change.path, ()), *found.get(change.old_path or "", ())})

    def _cell(found: list[Path]) -> str:
        return ", ".join(f"`{_rel(p, root)}`" for p in found)

    lines += ["| Cambio | Fichero | Lo citan (Evidencia) | Lo mencionan |", "|---|---|---|---|"]
    orphans: list[str] = []
    for change in report.changes:
        cited, mentioned = _for(pages, change), _for(mentions, change)
        shown = f"{change.old_path} → {change.path}" if change.old_path else change.path
        if not cited and not mentioned:
            orphans.append(shown)
        lines.append(
            f"| {change.kind} | `{shown}` | {_cell(cited) or '*Sin página*'} "
            f"| {_cell(mentioned) or '—'} |"
        )
    affected = sorted({p for found in pages.values() for p in found})
    mentioned_only = sorted(
        {p for found in mentions.values() for p in found} - set(affected) - set(report.examples)
    )
    lines += ["", f"## Páginas a revisar ({len(affected)})", ""]
    lines += [f"- `{_rel(p, root)}`" for p in affected] or ["*Ninguna.*"]
    lines += [
        "",
        f"## Páginas que solo lo mencionan ({len(mentioned_only)}) — revisar si cambia lo descrito",
        "",
    ]
    lines += [f"- `{_rel(p, root)}`" for p in mentioned_only] or ["*Ninguna.*"]
    lines += ["", f"## Ejemplos enlazados desde páginas técnicas ({len(report.examples)})", ""]
    lines += [f"- `{_rel(p, root)}`" for p in report.examples] or ["*Ninguno.*"]
    lines += ["", f"## Ficheros sin página ({len(orphans)}) — clasificar en el INVENTARIO", ""]
    lines += [f"- `{p}`" for p in orphans] or ["*Ninguno.*"]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Registro de decisiones de cobertura (Arquetipo 13)
# ---------------------------------------------------------------------------

COVERAGE_ID_RE = re.compile(r"\bCOB-[A-Z0-9]+-\d{3}\b")
REGISTER_LINK_RE = re.compile(r"\]\(([^)\s#]*_decisiones\.md)#cob-[a-z0-9]+-\d{3}\)")
REGISTER_HEADING_RE = re.compile(r"^#{2,4}\s+(COB-[A-Z0-9]+-\d{3})\b")
HEADING_RE = re.compile(r"^#{1,6}\s")
FENCE_RE = re.compile(r"^(```|~~~)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->")
REGISTER_SUFFIX = "_decisiones.md"
PENDING = "Pendiente"
NOT_APPLICABLE = "No aplica"
# ⚠ se guarda sin el selector de variación U+FE0F: se normaliza al leer.
COVERAGE_SYMBOLS = ("✅", "⚠", "🔍", "❌")
SYMBOL_LABELS = {"✅": "✅", "⚠": "⚠️", "🔍": "🔍", "❌": "❌"}
DECISIONS_BY_STATE: dict[str, frozenset[str]] = {
    "✅": frozenset({"Confirmar", "Reabrir"}),
    "⚠": frozenset({"Remediar", "Aceptar riesgo", "Reclasificar"}),
    "❌": frozenset({"Implementar", "Medida compensatoria", "Aceptar riesgo", NOT_APPLICABLE}),
    "🔍": frozenset({"Aportar evidencia", "Reclasificar", NOT_APPLICABLE}),
}
KNOWN_DECISIONS = frozenset(d for group in DECISIONS_BY_STATE.values() for d in group)
FIELD_DETECTED = "estado detectado"
FIELD_DECISION = "decisión"
FIELD_RESULT = "estado resultante"
FIELD_DATE = "fecha"
REQUIRED_WHEN_DECIDED = ("responsable", FIELD_DATE, FIELD_RESULT)

DecisionIssue = Literal[
    "duplicate", "orphan_ref", "orphan_entry", "invalid", "incomplete", "unreflected", "mismatch"
]


@dataclass(frozen=True)
class DecisionEntry:
    """Ficha ``COB-<ÁMBITO>-<NNN>`` de un registro ``docs/decisiones/<ámbito>_decisiones.md``."""

    register: Path
    cid: str
    line: int
    fields: dict[str, str]

    @property
    def decision(self) -> str:
        """Decisión normalizada; una ficha sin decisión cuenta como ``Pendiente``."""
        return _clean_value(self.fields.get(FIELD_DECISION, "")) or PENDING

    @property
    def pending(self) -> bool:
        return self.decision == PENDING

    @property
    def detected(self) -> str | None:
        return _last_symbol(self.fields.get(FIELD_DETECTED, ""))

    @property
    def result(self) -> str | None:
        """Símbolo de «Estado resultante», ``NOT_APPLICABLE`` o ``None`` si está vacío o no vale."""
        value = _clean_value(self.fields.get(FIELD_RESULT, ""))
        if value.casefold().startswith(NOT_APPLICABLE.casefold()):
            return NOT_APPLICABLE
        return _last_symbol(value)


@dataclass(frozen=True)
class CoverageRow:
    """Línea de una página documentada que cita un ID de cobertura (fuera de código)."""

    page: Path
    cid: str
    line: int
    text: str
    symbol: str | None

    @property
    def is_coverage(self) -> bool:
        """Fila de tabla que declara un estado (símbolo o «No aplica»), no una simple mención."""
        return self.text.startswith("|") and (
            self.symbol is not None or NOT_APPLICABLE.casefold() in self.text.casefold()
        )


@dataclass(frozen=True)
class DecisionFinding:
    """Incoherencia entre un registro de decisiones y la documentación."""

    kind: DecisionIssue
    cid: str
    path: Path
    line: int
    detail: str


@dataclass(frozen=True)
class DecisionReport:
    """Resultado de ``decisions``: fichas únicas (orden estable) y hallazgos."""

    entries: tuple[DecisionEntry, ...]
    findings: tuple[DecisionFinding, ...]


def _clean_value(value: str) -> str:
    """Quita comentarios HTML y negritas; ``—`` / ``-`` cuentan como vacío."""
    text = HTML_COMMENT_RE.sub("", value).replace("*", "").strip()
    return "" if text in {"—", "-", "–"} else text


def _field_key(name: str) -> str:
    return name.replace("*", "").strip().casefold()


def _last_symbol(text: str) -> str | None:
    """Último símbolo de la leyenda que aparece en ``text`` (``⚠`` normalizado)."""
    clean = text.replace("️", "")
    best, position = None, -1
    for symbol in COVERAGE_SYMBOLS:
        index = clean.rfind(symbol)
        if index > position:
            best, position = symbol, index
    return best


def _cells(row: str) -> list[str]:
    return [cell.strip() for cell in row.strip().strip("|").split("|")]


def _code_free_lines(path: Path) -> list[tuple[int, str]]:
    """(nº de línea, texto sin sangría ni código en línea) fuera de bloques de código."""
    result: list[tuple[int, str]] = []
    in_fence = False
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = raw.strip()
        if FENCE_RE.match(stripped):
            in_fence = not in_fence
            continue
        if not in_fence:
            result.append((number, INLINE_CODE_RE.sub("", stripped)))
    return result


def parse_registers(decisions_dir: Path) -> list[DecisionEntry]:
    """Fichas de todos los ``*_decisiones.md`` de ``decisions_dir``, en orden estable."""
    entries: list[DecisionEntry] = []
    if not decisions_dir.is_dir():
        return entries
    for register in sorted(decisions_dir.glob(f"*{REGISTER_SUFFIX}")):
        current: tuple[str, int] | None = None
        fields: dict[str, str] = {}
        for number, text in _code_free_lines(register):
            heading = REGISTER_HEADING_RE.match(text)
            if heading or HEADING_RE.match(text):
                if current is not None:
                    entries.append(DecisionEntry(register, current[0], current[1], fields))
                current = (heading.group(1), number) if heading else None
                fields = {}
            elif current is not None and text.startswith("|"):
                cells = _cells(text)
                key = _field_key(cells[0])
                if len(cells) >= 2 and key not in {"", "campo"} and set(key) - set("-: "):
                    fields[key] = cells[1]
        if current is not None:
            entries.append(DecisionEntry(register, current[0], current[1], fields))
    return entries


def collect_coverage_rows(docs_dir: Path, decisions_dir: Path) -> list[CoverageRow]:
    """Líneas de ``docs_dir`` (sin el propio registro) que citan IDs ``COB-…`` fuera de código."""
    rows: list[CoverageRow] = []
    for page in sorted(docs_dir.rglob("*.md")):
        if page.is_relative_to(decisions_dir):
            continue
        for number, text in _code_free_lines(page):
            for cid in sorted(set(COVERAGE_ID_RE.findall(text))):
                rows.append(CoverageRow(page, cid, number, text, _last_symbol(text)))
    return rows


def _validate_entry(entry: DecisionEntry) -> list[DecisionFinding]:
    """Hallazgos ``invalid`` / ``incomplete`` de una ficha aislada."""

    def _found(kind: DecisionIssue, detail: str) -> DecisionFinding:
        return DecisionFinding(kind, entry.cid, entry.register, entry.line, detail)

    findings: list[DecisionFinding] = []
    scope = entry.cid.split("-")[1]
    expected = entry.register.name.removesuffix(REGISTER_SUFFIX)
    if scope.casefold() != expected.casefold():
        findings.append(_found("invalid", f"el ámbito {scope} no corresponde al registro"))
    detected, decision = entry.detected, entry.decision
    if detected is None:
        findings.append(_found("invalid", "«Estado detectado» sin símbolo de la leyenda"))
    if entry.pending:
        return findings
    if decision not in KNOWN_DECISIONS:
        findings.append(_found("invalid", f"decisión desconocida «{decision}»"))
    elif detected is not None and decision not in DECISIONS_BY_STATE[detected]:
        label = SYMBOL_LABELS[detected]
        findings.append(_found("invalid", f"«{decision}» no se admite para el estado {label}"))
    missing = [k for k in REQUIRED_WHEN_DECIDED if not _clean_value(entry.fields.get(k, ""))]
    if missing:
        findings.append(_found("incomplete", "faltan: " + ", ".join(missing)))
    date_value = _clean_value(entry.fields.get(FIELD_DATE, ""))
    if date_value:
        try:
            date.fromisoformat(date_value)
        except ValueError:
            findings.append(_found("invalid", f"fecha «{date_value}» no es AAAA-MM-DD"))
    result_value = _clean_value(entry.fields.get(FIELD_RESULT, ""))
    if result_value and entry.result is None:
        findings.append(_found("invalid", f"«Estado resultante» no válido: «{result_value}»"))
    if (decision == NOT_APPLICABLE) != (entry.result == NOT_APPLICABLE) and entry.result:
        findings.append(_found("invalid", "«No aplica» debe figurar en decisión y resultado"))
    return findings


def _reflection_problem(entry: DecisionEntry, row: CoverageRow) -> str | None:
    """Motivo por el que ``row`` no refleja la decisión de ``entry`` (``None`` si la refleja)."""
    anchor = f"{entry.register.name}#{entry.cid}".casefold()
    if anchor not in row.text.casefold():
        return f"la fila no enlaza la ficha ({anchor})"
    if entry.result == NOT_APPLICABLE:
        if NOT_APPLICABLE.casefold() not in row.text.casefold():
            return "la fila no indica «No aplica»"
        return None
    if row.symbol != entry.result:
        shown = SYMBOL_LABELS.get(row.symbol or "", "sin símbolo")
        return f"la fila muestra {shown}; la decisión fija {SYMBOL_LABELS[entry.result or '✅']}"
    return None


def check_decisions(docs_dir: Path, decisions_dir: Path) -> DecisionReport:
    """Cruza los registros de decisiones con las páginas que citan sus IDs."""
    rows = collect_coverage_rows(docs_dir, decisions_dir)
    findings: list[DecisionFinding] = []
    unique: dict[str, DecisionEntry] = {}
    for entry in parse_registers(decisions_dir):
        first = unique.get(entry.cid)
        if first is not None:
            where = f"{first.register.name}:{first.line}"
            findings.append(
                DecisionFinding("duplicate", entry.cid, entry.register, entry.line, where)
            )
            continue
        unique[entry.cid] = entry
        own = _validate_entry(entry)
        findings += own
        cited = [r for r in rows if r.cid == entry.cid]
        if not cited:
            findings.append(
                DecisionFinding(
                    "orphan_entry", entry.cid, entry.register, entry.line, "ninguna página lo cita"
                )
            )
            continue
        coverage = [r for r in cited if r.is_coverage]
        if own:
            continue
        if entry.pending:
            for row in coverage:
                if row.symbol is not None and entry.detected and row.symbol != entry.detected:
                    detail = (
                        f"la página muestra {SYMBOL_LABELS[row.symbol]}; "
                        f"la ficha {SYMBOL_LABELS[entry.detected]}"
                    )
                    findings.append(
                        DecisionFinding("mismatch", entry.cid, row.page, row.line, detail)
                    )
            continue
        if not coverage:
            findings.append(
                DecisionFinding(
                    "unreflected", entry.cid, cited[0].page, cited[0].line, "sin fila de cobertura"
                )
            )
        for row in coverage:
            problem = _reflection_problem(entry, row)
            if problem is not None:
                findings.append(
                    DecisionFinding("unreflected", entry.cid, row.page, row.line, problem)
                )
    reported: set[tuple[str, Path]] = set()
    for row in rows:
        if row.cid not in unique and (row.cid, row.page) not in reported:
            reported.add((row.cid, row.page))
            findings.append(
                DecisionFinding(
                    "orphan_ref", row.cid, row.page, row.line, "sin ficha en el registro"
                )
            )
    findings.sort(key=lambda f: (f.path.as_posix(), f.line, f.kind, f.cid))
    return DecisionReport(tuple(unique.values()), tuple(findings))


def format_decisions(report: DecisionReport, root: Path) -> str:
    """Informe Markdown de ``decisions``: resumen por registro, pendientes y hallazgos."""
    lines = [
        "# Registro de Decisiones de Cobertura — estado",
        "",
        "| Registro | Fichas | Pendientes | Decididas |",
        "|---|---|---|---|",
    ]
    for register in sorted({e.register for e in report.entries}):
        own = [e for e in report.entries if e.register == register]
        pending = sum(1 for e in own if e.pending)
        lines.append(
            f"| `{_rel(register, root)}` | {len(own)} | {pending} | {len(own) - pending} |"
        )
    if not report.entries:
        lines.append("| *Sin registros* | 0 | 0 | 0 |")
    pending_entries = [e for e in report.entries if e.pending]
    lines += ["", f"## Pendientes de decisión ({len(pending_entries)})", ""]
    lines += [
        f"- `{e.cid}` ({SYMBOL_LABELS.get(e.detected or '', '?')}) — "
        f"`{_rel(e.register, root)}:{e.line}`"
        for e in pending_entries
    ] or ["*Ninguna.*"]
    lines += ["", f"## Hallazgos ({len(report.findings)})", ""]
    if report.findings:
        lines += ["| Tipo | ID | Ubicación | Detalle |", "|---|---|---|---|"]
        lines += [
            f"| {f.kind} | `{f.cid}` | `{_rel(f.path, root)}:{f.line}` | {f.detail} |"
            for f in report.findings
        ]
    else:
        lines.append("*Ninguno.*")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _cmd_drift(args: argparse.Namespace) -> int:
    root: Path = args.root.resolve()
    # Por defecto, relativo a --root (destino externo), no a la raíz de doc_ia.
    docs: Path = (args.docs or root / "docs").resolve()
    findings = check_drift(docs, root)
    for f in findings:
        print(f"[doc_trace] {f.status:<12} {_rel(f.page, root)} ← {f.source}")
    if findings:
        print(f"[doc_trace] {len(findings)} fuente(s) desactualizada(s). Revisa y ejecuta `stamp`.")
        return 1
    print("[doc_trace] Sin drift: todas las huellas coinciden.")
    return 0


def _cmd_stamp(args: argparse.Namespace) -> int:
    root: Path = args.root.resolve()
    for page in args.pages:
        try:
            meta = stamp_page(
                page.resolve(),
                root,
                sources=args.source,
                archetype=args.archetype,
                reviewed=args.date,
            )
        except (ValueError, OSError) as exc:
            print(f"[doc_trace] ERROR: {exc}", file=sys.stderr)
            return 1
        print(f"[doc_trace] {_rel(meta.page, root)}: {len(meta.sources)} fuente(s) sellada(s)")
    return 0


def _cmd_matrix(args: argparse.Namespace) -> int:
    root: Path = args.root.resolve()
    docs: Path = (args.docs or root / "docs").resolve()
    tests: Path = (args.tests or root / "tests").resolve()
    criteria = collect_criteria(docs / "functional")
    test_ids = collect_test_ids(tests, root)
    report, unknown = build_matrix(criteria, test_ids, root)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8", newline="\n")
        print(f"[doc_trace] Matriz escrita en {args.output}")
    else:
        print(report, end="")
    if unknown:
        print(f"[doc_trace] {len(unknown)} test(s) citado(s) inexistente(s).", file=sys.stderr)
        return 1
    return 0


def _cmd_llms(args: argparse.Namespace) -> int:
    # Por defecto, relativos a --root (destino externo), no a la raíz de doc_ia.
    config: Path = args.config or args.root.resolve() / "mkdocs.yml"
    try:
        content = build_llms_txt(config, args.site_url)
        output: Path = args.output or _default_llms_output(config)
    except (ValueError, OSError) as exc:
        print(f"[doc_trace] ERROR: {exc}", file=sys.stderr)
        return 1
    if args.check:
        current = output.read_text(encoding="utf-8") if output.exists() else ""
        if current != content:
            print(f"[doc_trace] {output} desactualizado. Ejecuta `llms` sin --check.")
            return 1
        print(f"[doc_trace] {output} al día.")
        return 0
    output.write_text(content, encoding="utf-8", newline="\n")
    print(f"[doc_trace] {output} generado ({content.count('- [')} páginas).")
    return 0


def _cmd_decisions(args: argparse.Namespace) -> int:
    root: Path = args.root.resolve()
    docs: Path = (args.docs or root / "docs").resolve()
    report = check_decisions(docs, docs / "decisiones")
    text = format_decisions(report, root)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8", newline="\n")
        print(f"[doc_trace] Informe escrito en {args.output}")
    else:
        print(text, end="")
    if report.findings:
        print(
            f"[doc_trace] {len(report.findings)} hallazgo(s) en las decisiones de cobertura.",
            file=sys.stderr,
        )
        return 1
    return 0


def _default_llms_output(mkdocs_yml: Path) -> Path:
    """``<docs_dir>/llms.txt`` junto a ``mkdocs.yml`` (``docs_dir`` por defecto: ``docs``)."""
    config = _load_yaml(mkdocs_yml.read_text(encoding="utf-8"))
    docs_dir = config.get("docs_dir", "docs") if isinstance(config, dict) else "docs"
    return mkdocs_yml.parent / str(docs_dir) / "llms.txt"


def _paths_arg(args: argparse.Namespace) -> tuple[str, ...]:
    """Pathspecs de ``--path`` (vacío si no se indicó)."""
    given: list[str] | None = args.path
    # Normalizado: "gui/vg/", "./gui/vg" y "gui\vg" son el mismo alcance que "gui/vg".
    normalized = (p.replace("\\", "/").removeprefix("./").rstrip("/") or "." for p in given or ())
    return tuple(normalized)


def _origin_args(args: argparse.Namespace) -> tuple[Path, Path, Path, str]:
    """(origen, docs, fichero de estado, nombre) con los valores por defecto relativos a --root."""
    root: Path = args.root.resolve()
    origin: Path = args.origin.resolve()
    docs: Path = (args.docs or root / "docs").resolve()
    state: Path = (args.state or root / ".ai" / "doc_state.json").resolve()
    return origin, docs, state, args.name or origin.name


def _cmd_baseline(args: argparse.Namespace) -> int:
    origin, docs, state, name = _origin_args(args)
    paths = _paths_arg(args) or DEFAULT_PATHS
    baseline = take_baseline(origin, documentation_paths(origin, docs), paths=paths)
    if args.ref and baseline.commit is not None:  # ref documentada explícita (worktree desacoplado)
        baseline = replace(baseline, branch=args.ref)
    write_baseline(state, name, baseline)
    if baseline.commit is None:
        print(f"[doc_trace] {name}: el origen no está bajo git; la próxima sesión será completa.")
        return 0
    print(f"[doc_trace] {name}: baseline {baseline.commit[:12]} ({baseline.branch}) → {state}")
    if baseline.paths != DEFAULT_PATHS:
        print(f"[doc_trace] {name}: alcance {', '.join(baseline.paths)}")
    if baseline.dirty:
        print(
            f"[doc_trace] AVISO: {name} tiene cambios sin confirmar; se volverán a revisar "
            "en la próxima sesión incremental."
        )
    return 0


def _cmd_changes(args: argparse.Namespace) -> int:
    origin, docs, state, name = _origin_args(args)
    report = check_changes(origin, docs, state, name, _paths_arg(args) or None)
    text = format_changes(report, name, args.root.resolve())
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8", newline="\n")
        print(f"[doc_trace] Informe escrito en {args.output}")
    else:
        print(text, end="")
    if report.status != "ok":
        print(f"[doc_trace] Modo completo: {report.reason}.", file=sys.stderr)
        return 3
    return 1 if report.changes else 0


def _add_origin_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--origin", type=Path, required=True, help="Raíz del origen (git).")
    parser.add_argument("--name", help="Nombre del origen (por defecto, su carpeta).")
    parser.add_argument("--docs", type=Path, help="Carpeta de docs del destino (<root>/docs).")
    parser.add_argument(
        "--state", type=Path, help="Estado del destino (<root>/.ai/doc_state.json)."
    )
    parser.add_argument(
        "--path",
        action="append",
        help="Pathspec de git relativo al origen (repetible): alcance transversal.",
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Trazabilidad determinista docs ↔ código.")
    parser.add_argument("--root", type=Path, default=ROOT, help="Raíz del repositorio.")
    sub = parser.add_subparsers(dest="command", required=True)

    drift = sub.add_parser("drift", help="Detecta páginas con fuentes cambiadas.")
    drift.add_argument("--docs", type=Path, help="Carpeta de docs (<root>/docs).")
    drift.set_defaults(func=_cmd_drift)

    stamp = sub.add_parser("stamp", help="Sella las huellas de las fuentes de una página.")
    stamp.add_argument("pages", type=Path, nargs="+", help="Páginas a sellar.")
    stamp.add_argument(
        "--source", action="append", help="Fuente (repetible); por defecto las actuales."
    )
    stamp.add_argument("--archetype", help='Arquetipo de la página (p. ej. "1", "2", "12").')
    stamp.add_argument("--date", help="Fecha de revisión YYYY-MM-DD (por defecto, hoy).")
    stamp.set_defaults(func=_cmd_stamp)

    matrix = sub.add_parser("matrix", help="Cruza criterios de aceptación con tests.")
    matrix.add_argument("--docs", type=Path, help="Carpeta de docs (<root>/docs).")
    matrix.add_argument("--tests", type=Path, help="Carpeta de tests (<root>/tests).")
    matrix.add_argument(
        "--output", type=Path, help="Fichero Markdown de salida (por defecto, stdout)."
    )
    matrix.set_defaults(func=_cmd_matrix)

    llms = sub.add_parser("llms", help="Genera llms.txt desde el nav de mkdocs.yml.")
    llms.add_argument("--config", type=Path, help="mkdocs.yml (<root>/mkdocs.yml).")
    llms.add_argument("--output", type=Path, help="Salida (<docs_dir de --config>/llms.txt).")
    llms.add_argument("--site-url", help="URL base (por defecto, site_url de mkdocs.yml).")
    llms.add_argument("--check", action="store_true", help="Solo comprueba que está al día.")
    llms.set_defaults(func=_cmd_llms)

    decisions = sub.add_parser(
        "decisions", help="Cruza los registros de decisiones de cobertura con la documentación."
    )
    decisions.add_argument("--docs", type=Path, help="Carpeta de docs (<root>/docs).")
    decisions.add_argument("--output", type=Path, help="Fichero Markdown (por defecto, stdout).")
    decisions.set_defaults(func=_cmd_decisions)

    baseline = sub.add_parser("baseline", help="Guarda el commit actual del origen (CIERRE).")
    _add_origin_args(baseline)
    baseline.add_argument(
        "--ref", help="Rama/ref documentada (por defecto, la actual o la única que apunta al HEAD)."
    )
    baseline.set_defaults(func=_cmd_baseline)

    changes = sub.add_parser("changes", help="Cambios del origen desde su baseline (Fase 1).")
    _add_origin_args(changes)
    changes.add_argument("--output", type=Path, help="Fichero Markdown (por defecto, stdout).")
    changes.set_defaults(func=_cmd_changes)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Punto de entrada: 0 sin problemas · 1 drift / cambios / tests inexistentes /
    hallazgos de decisiones / error ·
    2 uso · 3 ``changes`` sin baseline utilizable (modo completo)."""
    args = _parser().parse_args(argv)
    result: int = args.func(args)
    return result


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    sys.exit(main())
