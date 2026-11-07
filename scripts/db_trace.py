#!/usr/bin/env python3
"""Trazabilidad entre la documentación, el código y la base de datos (origen BASE DE DATOS).

Lee la documentación Markdown que genera ``util_bbdd`` (``manifest.json`` con
``format: util_bbdd.doc.markdown`` y ``docs/catalog.json`` con ``format: util_bbdd.doc.catalog``,
contrato versionado de su ADR-006). No se conecta a ninguna base de datos ni accede a la red: la
exportación la genera el usuario con ``util_bbdd`` y sus credenciales, fuera de doc_ia.

Subcomandos:

  info      Comprueba el contrato de la exportación y muestra entorno, motor y fecha.
  select    Importa en ``<destino>/docs/<carpeta>/`` las páginas de los objetos del alcance
            (``--include``, patrones glob sin distinguir mayúsculas), reescribe como texto los
            enlaces a objetos no importados, genera el índice de la sección y guarda en
            ``<destino>/_fuentes/<nombre>/`` el catálogo y el manifiesto del subconjunto.
            Exit 0 sin cambios · 1 con cambios.
  compare   Contrasta el modelo del código (``entities.xml``) con el catálogo: tablas, columnas,
            nulabilidad y FK que solo están en un lado. Exit 0 sin discrepancias · 1 con ellas.
  changes   Objetos añadidos, retirados o modificados (por huella) entre dos catálogos y páginas
            de la documentación que los citan. Exit 0 sin cambios · 1 con cambios.
  tracemap  Genera el ``trace_map.toml`` de ``util_bbdd`` desde la evidencia de la documentación
            (páginas funcionales y técnicas que citan cada objeto) y el código del módulo.

Uso:
    python scripts/db_trace.py info --export <carpeta util_bbdd>
    python scripts/db_trace.py select --export <carpeta> --root <destino> --name bd_calidad \\
        --env Calidad --include "MVG_*" --include "V_MVG_*"
    python scripts/db_trace.py compare --catalog <catalog.json> --entities <entities.xml> \\
        --include "MVG_*"
    python scripts/db_trace.py changes --catalog <nuevo> --previous <anterior> --docs <docs> \\
        --include "MVG_*"
    python scripts/db_trace.py tracemap --catalog <catalog.json> --docs <docs> --origin <repo> \\
        --output <destino>/.ai/trace_map.toml
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import posixpath
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

MANIFEST_FORMAT = "util_bbdd.doc.markdown"
CATALOG_FORMAT = "util_bbdd.doc.catalog"
SUPPORTED_MANIFEST = frozenset({1, 2})
SUPPORTED_CATALOG = frozenset({1})
REQUIRED_KEYS = ("id", "kind", "name", "path")
SCHEMA_KINDS = frozenset({"table", "view"})  # lo que modela el código; las rutinas no
LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)\)")  # enlaces, no imágenes
GENERATED_NOTE = (
    "<!-- Generado por doc_ia scripts/db_trace.py select desde util_bbdd: no editar a mano. -->\n"
)
FUNCTIONAL_GUIDES = ("_howto.md", "_tutorial.md")


def is_functional(page: str) -> bool:
    """Página funcional: ``functional/`` o guías de uso (how-to, tutorial); el resto, técnica."""
    return page.startswith("functional/") or (
        page.startswith("guides/") and page.endswith(FUNCTIONAL_GUIDES)
    )


def is_entity_code(path: str, entity: str) -> bool:
    """Fichero de la entidad: ``Mvg<X>``, ``IMvg<X>Service``, ``Mvg<X>Wnd``… o su carpeta.

    ``MvgAgresion`` no se queda con ``MvgAgresioninfo``: tras el nombre solo admite un sufijo
    que empiece en mayúscula.
    """
    p = Path(path)
    return bool(re.fullmatch(rf"I?{re.escape(entity)}(?:[A-Z]\w*)?", p.stem)) or entity in p.parts


class DbTraceError(Exception):
    """Exportación fuera de contrato, ficheros inexistentes o parámetros inválidos."""


# --- contrato de la exportación ---


def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise DbTraceError(f"no existe: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise DbTraceError(f"JSON inválido: {path} ({exc})") from exc
    if not isinstance(data, dict):
        raise DbTraceError(f"se esperaba un objeto JSON: {path}")
    return data


def load_manifest(export: Path) -> dict[str, Any]:
    """``manifest.json`` de la exportación, con formato y versión comprobados."""
    data = _load_json(export / "manifest.json")
    if data.get("format") != MANIFEST_FORMAT:
        raise DbTraceError(f"no es una exportación de util_bbdd: format={data.get('format')!r}")
    if data.get("format_version") not in SUPPORTED_MANIFEST:
        raise DbTraceError(f"manifest format_version no soportada: {data.get('format_version')}")
    return data


def load_catalog(path: Path) -> dict[str, Any]:
    """Catálogo (``catalog.json``) con formato y versión comprobados."""
    data = _load_json(path)
    if data.get("format") != CATALOG_FORMAT:
        raise DbTraceError(f"no es un catálogo de util_bbdd: format={data.get('format')!r}")
    if data.get("format_version") not in SUPPORTED_CATALOG:
        raise DbTraceError(f"catalog format_version no soportada: {data.get('format_version')}")
    if not isinstance(data.get("objects"), list):
        raise DbTraceError(f"catálogo sin 'objects': {path}")
    for number, obj in enumerate(data["objects"]):
        missing = [k for k in REQUIRED_KEYS if not isinstance(obj, dict) or not obj.get(k)]
        if missing:
            raise DbTraceError(f"{path}: objeto {number} sin {', '.join(missing)}")
    return data


def matches(name: str, patterns: tuple[str, ...]) -> bool:
    """Nombre dentro del alcance (patrones glob, sin distinguir mayúsculas)."""
    return any(fnmatch.fnmatch(name.upper(), p.upper()) for p in patterns)


def select_objects(catalog: dict[str, Any], patterns: tuple[str, ...]) -> list[dict[str, Any]]:
    objects: list[dict[str, Any]] = catalog["objects"]
    return (
        [o for o in objects if matches(str(o.get("name", "")), patterns)] if patterns else objects
    )


def frontier(selected: list[dict[str, Any]]) -> list[str]:
    """Ids de objetos fuera del alcance enlazados por FK con los seleccionados (profundidad 1)."""
    inside = {o["id"] for o in selected}
    outside: set[str] = set()
    for obj in selected:
        outside.update(fk["ref"] for fk in obj.get("fk_out", []) if fk.get("ref") not in inside)
        outside.update(ref for ref in obj.get("fk_in", []) if ref not in inside)
    return sorted(outside)


def _short(object_id: str) -> str:
    """``table:SCHEMA.NOMBRE`` → ``NOMBRE``."""
    return object_id.split(":", 1)[-1].split(".", 1)[-1]


# --- select: importación de páginas ---


@dataclass
class ImportReport:
    changes: list[tuple[str, str]] = field(default_factory=list)


def rewrite_links(text: str, page_rel: str, imported: set[str]) -> str:
    """Enlaces a páginas no importadas → texto en código; los demás se conservan."""
    base = posixpath.dirname(page_rel)

    def _sub(match: re.Match[str]) -> str:
        label, target = match.group(1), match.group(2)
        if re.match(r"^[a-z]+:", target) or target.startswith("#"):
            return match.group(0)
        path = posixpath.normpath(posixpath.join(base, target.split("#", 1)[0]))
        return match.group(0) if path in imported else f"`{label}`"

    return LINK_RE.sub(_sub, text)


def _index_page(
    manifest: dict[str, Any], selected: list[dict[str, Any]], edge: list[str], env: str
) -> str:
    rows = [
        f"| [{o['name']}]({o['path']}) | {o['kind']} | {(o.get('comment') or '').strip()} |"
        for o in selected
    ]
    lines = [
        GENERATED_NOTE.rstrip(),
        "# Base de datos",
        "",
        "Páginas del esquema real de la base de datos para los objetos de este proyecto,",
        "generadas con `util_bbdd` e importadas por doc_ia. Describen **lo desplegado** en el",
        "entorno indicado; el contraste con el código está en el modelo de datos y en las",
        "decisiones de cobertura.",
        "",
        "| Dato | Valor |",
        "|---|---|",
        f"| Entorno | **{env}** |",
        f"| Base de datos | `{manifest.get('database')}` (esquema `{manifest.get('schema')}`) |",
        f"| Motor | {manifest.get('engine')} |",
        f"| Generada | {manifest.get('generated_at')} |",
        f"| Generador | util_bbdd {manifest.get('util_bbdd_version')} |",
        "",
        f"## Objetos del alcance ({len(selected)})",
        "",
        "| Objeto | Tipo | Comentario |",
        "|---|---|---|",
        *rows,
        "",
        f"## Frontera (objetos relacionados por FK, no importados: {len(edge)})",
        "",
        ", ".join(f"`{_short(i)}`" for i in edge) or "*No aplica.*",
        "",
    ]
    return "\n".join(lines)


def _write_if_changed(path: Path, text: str, report: ImportReport, rel: str) -> None:
    if path.is_file() and path.read_text(encoding="utf-8") == text:
        return
    report.changes.append(("actualizado" if path.exists() else "creado", rel))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def import_pages(
    export: Path,
    root: Path,
    name: str,
    patterns: tuple[str, ...],
    subdir: str = "bd",
    env: str = "",
) -> ImportReport:
    """Importa al destino las páginas del alcance y guarda el catálogo del subconjunto."""
    if not env.strip():
        raise DbTraceError("indica el entorno que representa la exportación (--env)")
    manifest = load_manifest(export)
    catalog = load_catalog(export / "docs" / "catalog.json")
    selected = select_objects(catalog, patterns)
    if not selected:
        raise DbTraceError(f"ningún objeto encaja con {list(patterns)}")
    missing = [str(o["path"]) for o in selected if not (export / "docs" / str(o["path"])).is_file()]
    if missing:  # antes de escribir nada: el destino no queda a medias
        raise DbTraceError(f"el catálogo cita páginas inexistentes: {', '.join(missing)}")
    target = root / "docs" / subdir
    report = ImportReport()
    imported = {str(o["path"]) for o in selected}
    for obj in selected:
        rel = str(obj["path"])
        source = export / "docs" / rel
        text = rewrite_links(source.read_text(encoding="utf-8"), rel, imported)
        _write_if_changed(target / rel, text, report, f"docs/{subdir}/{rel}")
    for stale in sorted(target.rglob("*.md")) if target.is_dir() else []:
        rel = stale.relative_to(target).as_posix()
        if rel != "index.md" and rel not in imported:
            stale.unlink()
            report.changes.append(("retirado", f"docs/{subdir}/{rel}"))
    edge = frontier(selected)
    _write_if_changed(
        target / "index.md",
        _index_page(manifest, selected, edge, env),
        report,
        f"docs/{subdir}/index.md",
    )
    subset = {**catalog, "objects": selected, "doc_ia_alcance": list(patterns)}
    header: dict[str, Any] = {"doc_ia_entorno": env}
    header |= {
        k: manifest.get(k)
        for k in (
            "database",
            "engine",
            "format",
            "format_version",
            "generated_at",
            "schema",
            "util_bbdd_version",
        )
    }
    sources = root / "_fuentes" / name
    for fname, data in (("catalog.json", subset), ("manifest.json", header)):
        text = json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
        _write_if_changed(sources / fname, text, report, f"_fuentes/{name}/{fname}")
    return report


# --- compare: modelo del código ↔ catálogo ---


@dataclass(frozen=True)
class Finding:
    kind: str  # tabla | columna | nulabilidad | fk
    obj: str
    detail: str


def load_entities(path: Path) -> dict[str, dict[str, Any]]:
    """``entities.xml`` (vdyn): tabla → {entidad, columnas {nombre: (nullable, foreignType)}}."""
    if not path.is_file():
        raise DbTraceError(f"no existe: {path}")
    root = ET.parse(path).getroot()
    entities = {e.get("name", ""): e.get("table", "") for e in root.iter("entity")}
    model: dict[str, dict[str, Any]] = {}
    for entity in root.iter("entity"):
        table = (entity.get("table") or "").upper()
        columns: dict[str, tuple[str | None, str | None]] = {}
        for fld in entity.iter("field"):
            column = fld.get("column")
            if column:
                foreign = fld.get("foreignType") if fld.get("manyToOne") == "true" else None
                ref = entities.get(foreign or "", "").upper() or (foreign and f"({foreign})")
                columns[column.upper()] = (fld.get("nullable"), ref or None)
        model[table] = {"entity": entity.get("name"), "columns": columns}
    return model


def compare(
    catalog: dict[str, Any], model: dict[str, dict[str, Any]], patterns: tuple[str, ...]
) -> list[Finding]:
    """Discrepancias entre el modelo del código y la base de datos dentro del alcance."""
    findings: list[Finding] = []
    db = {
        str(o["name"]).upper(): o
        for o in select_objects(catalog, patterns)
        if o["kind"] in SCHEMA_KINDS
    }
    code = {t: m for t, m in model.items() if not patterns or matches(t, patterns)}
    for table in sorted(set(code) - set(db)):
        findings.append(
            Finding("tabla", table, f"en el código ({code[table]['entity']}) y no en la BD")
        )
    for table in sorted(set(db) - set(code)):
        findings.append(
            Finding("tabla", table, f"en la BD ({db[table]['kind']}) y no en el código")
        )
    for table in sorted(set(db) & set(code)):
        db_cols = {str(c["name"]).upper(): c for c in db[table].get("columns", [])}
        code_cols: dict[str, tuple[str | None, str | None]] = code[table]["columns"]
        for col in sorted(set(db_cols) - set(code_cols)):
            findings.append(Finding("columna", f"{table}.{col}", "en la BD y no en el código"))
        for col in sorted(set(code_cols) - set(db_cols)):
            findings.append(Finding("columna", f"{table}.{col}", "en el código y no en la BD"))
        fks = {
            c.upper(): _short(fk["ref"]).upper()
            for fk in db[table].get("fk_out", [])
            for c in fk.get("columns", [])
        }
        for col in sorted(set(db_cols) & set(code_cols)):
            nullable, ref = code_cols[col]
            db_null = bool(db_cols[col].get("nullable"))
            if nullable in ("true", "false") and (nullable == "true") != db_null:
                findings.append(
                    Finding(
                        "nulabilidad",
                        f"{table}.{col}",
                        f"código nullable={nullable}, BD {'NULL' if db_null else 'NOT NULL'}",
                    )
                )
            if ref and db[table]["kind"] == "table":
                if col not in fks:
                    findings.append(
                        Finding(
                            "fk", f"{table}.{col}", f"relación {ref} en el código sin FK en la BD"
                        )
                    )
                elif not ref.startswith("(") and fks[col] != ref:
                    findings.append(
                        Finding("fk", f"{table}.{col}", f"código → {ref}, BD → {fks[col]}")
                    )
    return findings


# --- changes: entre dos catálogos ---


def catalog_changes(
    new: dict[str, Any], old: dict[str, Any], patterns: tuple[str, ...] = ()
) -> list[tuple[str, str]]:
    """(cambio, id) por objeto del alcance: alta, baja o modificado (huella distinta).

    Con ``patterns`` se comparan solo los objetos del alcance en los dos catálogos: el catálogo
    nuevo puede ser la exportación completa y el anterior, el subconjunto de ``_fuentes/``.
    """
    a = {o["id"]: o.get("hash") for o in select_objects(new, patterns)}
    b = {o["id"]: o.get("hash") for o in select_objects(old, patterns)}
    out = [("alta", i) for i in sorted(set(a) - set(b))]
    out += [("baja", i) for i in sorted(set(b) - set(a))]
    out += [("modificado", i) for i in sorted(set(a) & set(b)) if a[i] != b[i]]
    return out


def pages_citing(
    docs: Path, names: list[str], skip: str = "bd", prefix: bool = False
) -> dict[str, list[str]]:
    """Páginas (fuera de la sección importada) que citan cada nombre de objeto.

    Con ``prefix``, un nombre de clase (con minúsculas, p. ej. ``MvgExpediente``) también cita
    con un sufijo en mayúscula (``MvgExpedienteWnd``); los nombres de tabla, todo mayúsculas,
    siempre exactos (``MVG_AGRESION`` no cita ``MVG_AGRESIONINFO``).
    """
    pages = {
        p: p.read_text(encoding="utf-8")
        for p in sorted(docs.rglob("*.md"))
        if p.relative_to(docs).parts[0] != skip
    }
    found: dict[str, list[str]] = {}
    for name in names:
        suffix = r"(?:[A-Z]\w*)?" if prefix and name != name.upper() else ""
        pattern = re.compile(rf"(?<![\w]){re.escape(name)}{suffix}(?![\w])")
        found[name] = [
            p.relative_to(docs).as_posix() for p, t in pages.items() if pattern.search(t)
        ]
    return found


# --- tracemap ---


def _toml_list(values: list[str]) -> str:
    return "[" + ", ".join(json.dumps(v, ensure_ascii=False) for v in values) + "]"


def build_tracemap(
    catalog: dict[str, Any],
    docs: Path,
    origin: Path | None,
    entities: dict[str, dict[str, Any]] | None,
    patterns: tuple[str, ...],
    subdir: str = "bd",
) -> str:
    """``trace_map.toml`` de util_bbdd: por objeto, páginas funcionales/técnicas y código."""
    selected = select_objects(catalog, patterns)
    entity_of = {
        str(o["name"]): (entities or {}).get(str(o["name"]).upper(), {}).get("entity")
        for o in selected
    }
    # Las páginas funcionales hablan en lenguaje de negocio y citan la entidad o sus clases
    # (``MvgExpedienteWnd``), no la tabla: se busca por los dos nombres.
    names = sorted({n for o in selected for n in (str(o["name"]), entity_of[str(o["name"])]) if n})
    cited = pages_citing(docs, names, skip=subdir, prefix=True)
    files: list[str] = []
    if origin is not None:
        out = subprocess.run(
            ["git", "-C", str(origin), "-c", "core.quotepath=off", "ls-files", "-z"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        files = [f for f in out.stdout.split("\0") if f] if out.returncode == 0 else []
    lines = [
        "# trace_map de util_bbdd (markdown.trace_map) — generado por doc_ia scripts/db_trace.py",
        "# tracemap desde la evidencia de la documentación. No editar a mano: se regenera.",
        "",
    ]
    section = {"table": "tables", "view": "views"}
    for obj in selected:
        kind = str(obj["kind"])
        if kind not in section:
            continue
        name = str(obj["name"])
        entity = entity_of[name]
        pages = sorted({*cited.get(name, []), *(cited.get(entity, []) if entity else [])})
        functional = [f"docs/{p}" for p in pages if is_functional(p)]
        technical = [f"docs/{p}" for p in pages if not is_functional(p)]
        code = sorted(f for f in files if entity and is_entity_code(f, entity))
        if not (functional or technical or code):
            continue
        lines.append(f'[{section[kind]}."{name}"]')
        for key, values in (("code", code), ("functional", functional), ("technical", technical)):
            if values:
                lines.append(f"{key} = {_toml_list(values)}")
        lines.append("")
    return "\n".join(lines)


# --- CLI ---


def _patterns(args: argparse.Namespace) -> tuple[str, ...]:
    given: list[str] | None = getattr(args, "include", None)
    return tuple(given or ())


def _cmd_info(args: argparse.Namespace) -> int:
    manifest = load_manifest(args.export)
    catalog = load_catalog(args.export / "docs" / "catalog.json")
    kinds: dict[str, int] = {}
    for obj in catalog["objects"]:
        kinds[str(obj["kind"])] = kinds.get(str(obj["kind"]), 0) + 1
    print(
        f"[db_trace] {manifest.get('database')} · {manifest.get('engine')} · "
        f"util_bbdd {manifest.get('util_bbdd_version')} · {manifest.get('generated_at')}"
    )
    print("[db_trace] objetos: " + ", ".join(f"{k} {v}" for k, v in sorted(kinds.items())))
    return 0


def _cmd_select(args: argparse.Namespace) -> int:
    report = import_pages(args.export, args.root, args.name, _patterns(args), args.subdir, args.env)
    print(f"[db_trace] {len(report.changes)} cambio(s) en {args.root}")
    for kind, rel in report.changes:
        print(f"  {kind.upper():<12} {rel}")
    return 1 if report.changes else 0


def _cmd_compare(args: argparse.Namespace) -> int:
    findings = compare(load_catalog(args.catalog), load_entities(args.entities), _patterns(args))
    lines = ["# Contraste código ↔ base de datos", "", f"Discrepancias: {len(findings)}", ""]
    if findings:
        lines += ["| Tipo | Objeto | Detalle |", "|---|---|---|"]
        lines += [f"| {f.kind} | `{f.obj}` | {f.detail} |" for f in findings]
    text = "\n".join(lines) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8", newline="\n")
    print(text, end="")
    return 1 if findings else 0


def _cmd_changes(args: argparse.Namespace) -> int:
    changes = catalog_changes(
        load_catalog(args.catalog), load_catalog(args.previous), _patterns(args)
    )
    names = [_short(i) for _, i in changes]
    cited = pages_citing(args.docs, names, skip=args.subdir) if args.docs else {}
    print(f"# Cambios de esquema ({len(changes)})\n")
    for kind, oid in changes:
        pages = ", ".join(f"`{p}`" for p in cited.get(_short(oid), [])) or "—"
        print(f"- {kind}: `{_short(oid)}` → {pages}")
    return 1 if changes else 0


def _cmd_tracemap(args: argparse.Namespace) -> int:
    entities = load_entities(args.entities) if args.entities else None
    text = build_tracemap(
        load_catalog(args.catalog), args.docs, args.origin, entities, _patterns(args), args.subdir
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8", newline="\n")
    print(f"[db_trace] trace_map escrito en {args.output}")
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Trazabilidad docs ↔ código ↔ base de datos.")
    sub = parser.add_subparsers(dest="command", required=True)
    info = sub.add_parser("info", help="Comprueba la exportación de util_bbdd.")
    info.add_argument("--export", type=Path, required=True, help="Carpeta con manifest.json.")
    info.set_defaults(func=_cmd_info)
    sel = sub.add_parser("select", help="Importa al destino las páginas del alcance.")
    sel.add_argument("--export", type=Path, required=True)
    sel.add_argument("--root", type=Path, required=True, help="Raíz del destino.")
    sel.add_argument("--name", required=True, help="Nombre del origen en _fuentes/.")
    sel.add_argument(
        "--env", required=True, help="Entorno que representa la exportación (p. ej. Calidad)."
    )
    sel.set_defaults(func=_cmd_select)
    cmp_ = sub.add_parser("compare", help="Contrasta entities.xml con el catálogo.")
    cmp_.add_argument("--catalog", type=Path, required=True)
    cmp_.add_argument("--entities", type=Path, required=True)
    cmp_.add_argument("--output", type=Path, help="Informe Markdown (además de stdout).")
    cmp_.set_defaults(func=_cmd_compare)
    chg = sub.add_parser("changes", help="Cambios entre dos catálogos.")
    chg.add_argument("--catalog", type=Path, required=True)
    chg.add_argument("--previous", type=Path, required=True)
    chg.add_argument("--docs", type=Path, help="docs/ del destino: páginas que citan cada objeto.")
    chg.set_defaults(func=_cmd_changes)
    trm = sub.add_parser("tracemap", help="Genera el trace_map.toml de util_bbdd.")
    trm.add_argument("--catalog", type=Path, required=True)
    trm.add_argument("--docs", type=Path, required=True)
    trm.add_argument("--origin", type=Path, help="Repositorio del código (git ls-files).")
    trm.add_argument("--entities", type=Path, help="entities.xml para localizar el código.")
    trm.add_argument("--output", type=Path, required=True)
    trm.set_defaults(func=_cmd_tracemap)
    for cmd in (sel, cmp_, chg, trm):
        cmd.add_argument("--include", action="append", help="Patrón glob de nombres (repetible).")
    for cmd in (sel, chg, trm):
        cmd.add_argument(
            "--subdir", default="bd", help="Sección importada dentro de docs/ (por defecto, bd)."
        )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        code: int = args.func(args)
    except (DbTraceError, OSError, ET.ParseError) as exc:
        print(f"[db_trace] ERROR: {exc}", file=sys.stderr)
        return 2
    return code


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    sys.exit(main())
