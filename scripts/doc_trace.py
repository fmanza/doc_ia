#!/usr/bin/env python3
"""Trazabilidad determinista entre la documentación y el código de un repositorio.

Subcomandos (no invoca ningún servicio IA ni accede a la red):

  drift   Compara las huellas SHA256 guardadas en el frontmatter de cada página con las
          fuentes actuales y lista las páginas desactualizadas.
  stamp   Calcula y escribe las huellas de las fuentes de una página (frontmatter).
  matrix  Cruza los criterios de aceptación (AC-xx, columna Test) de docs/functional/ con
          los tests reales de tests/ y lista tests citados inexistentes y tests sin citar.
  llms    Genera docs/llms.txt (formato llmstxt.org) a partir del nav de mkdocs.yml.

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
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Literal

ROOT = Path(__file__).resolve().parent.parent

HASH_LENGTH = 12
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)
AC_ROW_RE = re.compile(r"^\|\s*(AC-\d+)\s*\|")
TEST_ID_RE = re.compile(r"tests/[\w/]+\.py::[\w:]+")

DriftStatus = Literal["stale", "missing", "outside_repo"]


@dataclass(frozen=True)
class PageMeta:
    """Frontmatter de trazabilidad de una página."""

    page: Path
    archetype: str
    sources: dict[str, str]
    reviewed: str


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
    """Lee el frontmatter de trazabilidad; ``None`` si la página no declara ``fuentes``."""
    match = FRONTMATTER_RE.match(page.read_text(encoding="utf-8"))
    if match is None:
        return None
    data = _load_yaml(match.group(1))
    if not isinstance(data, dict) or not isinstance(data.get("fuentes"), dict):
        return None
    sources = {str(k): str(v) for k, v in data["fuentes"].items()}
    return PageMeta(
        page=page,
        archetype=str(data.get("arquetipo", "")),
        sources=sources,
        reviewed=str(data.get("revisado", "")),
    )


def _resolve_source(source: str, repo_root: Path) -> Path | None:
    """Ruta absoluta de la fuente si está dentro del repositorio; ``None`` si sale de él."""
    resolved = (repo_root / source).resolve()
    return resolved if resolved.is_relative_to(repo_root.resolve()) else None


def format_frontmatter(meta: PageMeta) -> str:
    """Serializa el frontmatter de trazabilidad con orden estable de fuentes."""
    lines = ["---", f'arquetipo: "{meta.archetype}"', "fuentes:"]
    lines += [f"  {src}: {digest}" for src, digest in sorted(meta.sources.items())]
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
    """Recalcula las huellas de las fuentes de ``page`` y reescribe su frontmatter."""
    current = read_page_meta(page)
    names = sources if sources else sorted(current.sources) if current else []
    if not names:
        raise ValueError(f"{page}: sin fuentes (usa --source)")
    digests: dict[str, str] = {}
    for name in names:
        resolved = _resolve_source(name, repo_root)
        if resolved is None:
            raise ValueError(f"{page}: la fuente {name} está fuera del repositorio")
        if not resolved.is_file():
            raise ValueError(f"{page}: la fuente {name} no existe")
        digests[name] = fingerprint(resolved)
    meta = PageMeta(
        page=page,
        archetype=archetype or (current.archetype if current else ""),
        sources=digests,
        reviewed=reviewed or date.today().isoformat(),
    )
    text = page.read_text(encoding="utf-8")
    body = FRONTMATTER_RE.sub("", text, count=1)
    page.write_text(format_frontmatter(meta) + body, encoding="utf-8", newline="\n")
    return meta


def check_drift(docs_dir: Path, repo_root: Path) -> list[DriftFinding]:
    """Lista, en orden estable, las fuentes cuya huella ya no coincide."""
    findings: list[DriftFinding] = []
    for page in sorted(docs_dir.rglob("*.md")):
        meta = read_page_meta(page)
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
# CLI
# ---------------------------------------------------------------------------


def _rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _cmd_drift(args: argparse.Namespace) -> int:
    root: Path = args.root.resolve()
    findings = check_drift(args.docs.resolve(), root)
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
    criteria = collect_criteria(args.docs.resolve() / "functional")
    test_ids = collect_test_ids(args.tests.resolve(), root)
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
    try:
        content = build_llms_txt(args.config, args.site_url)
    except (ValueError, OSError) as exc:
        print(f"[doc_trace] ERROR: {exc}", file=sys.stderr)
        return 1
    output: Path = args.output
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


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Trazabilidad determinista docs ↔ código.")
    parser.add_argument("--root", type=Path, default=ROOT, help="Raíz del repositorio.")
    sub = parser.add_subparsers(dest="command", required=True)

    drift = sub.add_parser("drift", help="Detecta páginas con fuentes cambiadas.")
    drift.add_argument("--docs", type=Path, default=ROOT / "docs", help="Carpeta de docs.")
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
    matrix.add_argument("--docs", type=Path, default=ROOT / "docs", help="Carpeta de docs.")
    matrix.add_argument("--tests", type=Path, default=ROOT / "tests", help="Carpeta de tests.")
    matrix.add_argument(
        "--output", type=Path, help="Fichero Markdown de salida (por defecto, stdout)."
    )
    matrix.set_defaults(func=_cmd_matrix)

    llms = sub.add_parser("llms", help="Genera llms.txt desde el nav de mkdocs.yml.")
    llms.add_argument("--config", type=Path, default=ROOT / "mkdocs.yml", help="mkdocs.yml.")
    llms.add_argument("--output", type=Path, default=ROOT / "docs" / "llms.txt", help="Salida.")
    llms.add_argument("--site-url", help="URL base (por defecto, site_url de mkdocs.yml).")
    llms.add_argument("--check", action="store_true", help="Solo comprueba que está al día.")
    llms.set_defaults(func=_cmd_llms)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Punto de entrada: 0 sin problemas · 1 drift / tests inexistentes / error · 2 uso."""
    args = _parser().parse_args(argv)
    result: int = args.func(args)
    return result


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    sys.exit(main())
