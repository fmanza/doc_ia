#!/usr/bin/env python3
"""Instantánea local y versionada de los orígenes documentales (Fase 0-pre de /document-project).

Copia los orígenes MATERIAL (manuales, especificaciones, normativa) a una zona de trabajo local,
``<raíz del destino>/_staging/<nombre>/``, y registra en ``<raíz del destino>/.ai/sources.json``
qué se copió: huella SHA256, versión detectada en el nombre e historial de cambios. Las fases
siguientes (conversión con ``convert_to_md.py``, ``_fuentes/``, evidencia) trabajan solo sobre
esa copia: el origen nunca se escribe.

Formas de origen admitidas (siempre rutas del sistema de ficheros; no accede a la red):

* **Fichero**: ``\\\\servidor\\recurso\\manual.docx``.
* **Carpeta**: se copian sus ficheros (``--include`` filtra por patrón glob).
* **Fichero con versión en el nombre**: el token ``{ver}`` marca la versión, p. ej.
  ``…\\Manual_ViolenciaGenero_v{ver}.docx``. Se elige la versión más alta (comparación
  numérica: ``1.2.50`` > ``1.2.9``) y se copia con un **nombre estable** sin versión
  (``Manual_ViolenciaGenero.docx``): la evidencia y ``_fuentes/`` no cambian de ruta al
  publicarse una versión nueva, y el historial registra la evolución.

SharePoint y OneDrive se leen a través de la biblioteca sincronizada en local (cliente de
OneDrive); los repositorios remotos se obtienen con git/glab antes de usar este script.

Subcomandos:

  add      Declara (o actualiza) un origen en el manifiesto, sin copiar nada.
  replace  Sustituye un origen por un documento **reestructurado** (otro nombre o ubicación) que
           indica el usuario: manda aunque su versión sea menor. Conserva el historial
           («sustituido») y retira ``_staging/<nombre>/``. Exit 0 · 2 error.
  sync     Copia los orígenes declarados que hayan cambiado y actualiza el manifiesto.
           ``--dry-run`` solo informa. Exit 0 sin cambios · 1 con cambios · 2 error.
  list     Muestra los orígenes declarados, su versión y sus ficheros.

Una versión nueva del **mismo** documento (mismo patrón ``{ver}``) no necesita ``replace``: la
recoge ``sync``. Las versiones solo se comparan dentro de un mismo patrón.

Uso:
    python scripts/snapshot_sources.py --root <destino> add manual "<carpeta>\\Manual_v{ver}.docx"
    python scripts/snapshot_sources.py --root <destino> replace manual "<otra>\\Guia_v{ver}.docx"
    python scripts/snapshot_sources.py --root <destino> add normativa "<carpeta>" --include "*.pdf"
    python scripts/snapshot_sources.py --root <destino> sync [nombre …] [--dry-run]
    python scripts/snapshot_sources.py --root <destino> list
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import shutil
import sys
import tomllib
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent

VERSION_TOKEN = "{ver}"
VERSION_GROUP = r"(?P<ver>\d+(?:\.\d+)*)"
# Separador y prefijo «v» que acompañan a la versión y desaparecen del nombre estable.
STABLE_NAME_RE = re.compile(r"[ _.-]?[vV]?\{ver\}")
NAME_RE = re.compile(r"^(?!\.+$)[\w.-]+$")  # «.» o «..» saldrían de _staging/
STAGING_DIR = "_staging"
MANIFEST = Path(".ai") / "sources.json"
# Carpetas y ficheros que nunca forman parte de un origen: salida de conversión, control de
# versiones, bloqueos de Office y metadatos del sistema.
SKIP_DIRS = frozenset({"md", ".git", STAGING_DIR, "__pycache__"})
SKIP_FILES = ("~$*", "Thumbs.db", "desktop.ini", ".DS_Store", "*.tmp")
CHUNK = 1 << 20


class SnapshotError(Exception):
    """Origen no resoluble: ruta inexistente, sin versiones o declaración inválida."""


@dataclass(frozen=True)
class Resolved:
    """Fichero del origen y su ruta (POSIX) dentro de ``_staging/<nombre>/``."""

    source: Path
    rel: str
    version: str | None = None


@dataclass(frozen=True)
class Change:
    """Cambio aplicado (o previsto, con ``--dry-run``) en un fichero del origen."""

    kind: str  # alta | modificado | baja
    rel: str
    version: str | None = None
    previous_version: str | None = None


# --- resolución de orígenes ---


def version_key(version: str) -> tuple[int, ...]:
    """Clave de orden numérico: ``1.2.50`` > ``1.2.9``."""
    return tuple(int(part) for part in version.split("."))


def stable_name(template: str) -> str:
    """Nombre sin versión: ``Manual_v{ver}.docx`` → ``Manual.docx``."""
    name = STABLE_NAME_RE.sub("", template)
    if not name.partition(".")[0].strip(" _-"):  # ".docx" o "_.pdf": sin nombre útil
        raise SnapshotError(f"el patrón «{template}» no deja nombre estable sin la versión")
    return name


def resolve_versioned(spec: Path) -> Resolved:
    """Fichero de versión más alta que encaja con un patrón ``…{ver}…``."""
    template = spec.name
    if VERSION_TOKEN in str(spec.parent):
        raise SnapshotError(f"{{ver}} solo puede ir en el nombre del fichero: {spec}")
    if not spec.parent.is_dir():
        raise SnapshotError(f"la carpeta del patrón no existe o no es legible: {spec.parent}")
    pattern = re.escape(template).replace(re.escape(VERSION_TOKEN), VERSION_GROUP)
    matcher = re.compile(pattern, re.IGNORECASE)
    found: list[tuple[tuple[int, ...], str, Path, str]] = []
    for candidate in spec.parent.iterdir():
        match = matcher.fullmatch(candidate.name)
        if match and candidate.is_file():
            version = match.group("ver")
            found.append((version_key(version), candidate.name, candidate, version))
    if not found:
        raise SnapshotError(f"ningún fichero de {spec.parent} encaja con «{template}»")
    _, _, source, version = max(found)
    return Resolved(source, stable_name(template), version)


def _skipped(rel: Path) -> bool:
    if any(part in SKIP_DIRS or part.startswith(".") for part in rel.parts[:-1]):
        return True
    return any(fnmatch.fnmatch(rel.name, pattern) for pattern in SKIP_FILES)


def resolve_directory(folder: Path, include: tuple[str, ...]) -> list[Resolved]:
    """Ficheros de una carpeta (recursivo), filtrados por ``include`` si se indica."""
    resolved: list[Resolved] = []
    for path in sorted(folder.rglob("*")):
        rel = path.relative_to(folder)
        if not path.is_file() or _skipped(rel):
            continue
        posix = rel.as_posix()
        if include and not any(
            fnmatch.fnmatch(rel.name, g) or fnmatch.fnmatch(posix, g) for g in include
        ):
            continue
        resolved.append(Resolved(path, posix))
    return resolved


def resolve(spec: str, include: tuple[str, ...] = ()) -> list[Resolved]:
    """Ficheros que aporta un origen declarado."""
    path = Path(spec)
    if VERSION_TOKEN in spec:
        return [resolve_versioned(path)]
    if path.is_file():
        return [Resolved(path, path.name)]
    if path.is_dir():
        return resolve_directory(path, include)
    raise SnapshotError(f"el origen no existe o no es legible: {spec}")


# --- manifiesto ---


def sha256(path: Path) -> str:
    """Huella SHA256 completa del fichero (lectura por bloques)."""
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        while chunk := fh.read(CHUNK):
            digest.update(chunk)
    return digest.hexdigest()


def _doc_ia_version() -> str:
    with (ROOT / "pyproject.toml").open("rb") as fh:
        version: str = tomllib.load(fh)["project"]["version"]
    return version


def read_manifest(path: Path) -> dict[str, Any]:
    """Manifiesto ``.ai/sources.json``; vacío si no existe."""
    if not path.is_file():
        return {"fuentes": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SnapshotError(f"manifiesto con JSON inválido: {path} ({exc})") from exc
    if not isinstance(data, dict) or not isinstance(data.get("fuentes"), dict):
        raise SnapshotError(f"manifiesto inválido: {path}")
    for name in data["fuentes"]:
        if not NAME_RE.fullmatch(name):
            raise SnapshotError(f"manifiesto inválido: {path} (nombre de origen «{name}»)")
    return data


def write_manifest(path: Path, data: dict[str, Any]) -> None:
    """Escribe el manifiesto con orden estable (diffs legibles en git)."""
    sources = data.get("fuentes", {})
    ordered = {"doc_ia": _doc_ia_version(), "fuentes": dict(sorted(sources.items()))}
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(ordered, indent=2, ensure_ascii=False) + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")


def declare(data: dict[str, Any], name: str, spec: str, include: tuple[str, ...]) -> None:
    """Añade o actualiza la declaración de un origen conservando su estado."""
    if not NAME_RE.fullmatch(name):
        raise SnapshotError(f"nombre de origen inválido «{name}» (letras, dígitos, . _ -)")
    if VERSION_TOKEN in spec and include:
        raise SnapshotError("--include no aplica a un fichero con {ver}")
    entry = data["fuentes"].setdefault(name, {"ficheros": {}, "historial": []})
    entry["origen"] = spec
    if include:
        entry["incluir"] = list(include)
    else:
        entry.pop("incluir", None)


def replace_source(
    data: dict[str, Any], name: str, spec: str, include: tuple[str, ...], today: str
) -> str:
    """Sustituye el origen declarado por un documento **reestructurado** (otro nombre o ubicación).

    La versión vigente la indica el usuario: el documento nuevo sustituye al anterior aunque su
    número de versión sea menor (no se comparan versiones entre documentos distintos). Conserva
    el historial con un evento ``sustituido`` y vacía ``ficheros`` para que el siguiente ``sync``
    copie el documento nuevo como alta. Devuelve el origen anterior.
    """
    sources: dict[str, Any] = data["fuentes"]
    if name not in sources:
        raise SnapshotError(f"origen no declarado: {name} (usa `add`)")
    entry: dict[str, Any] = sources[name]
    previous = str(entry.get("origen", ""))
    if previous == spec:
        raise SnapshotError(f"«{name}» ya apunta a ese origen: usa `sync` para una versión nueva")
    if VERSION_TOKEN in spec and include:
        raise SnapshotError("--include no aplica a un fichero con {ver}")
    resolve(spec, include)  # el documento nuevo debe existir antes de retirar el anterior
    history: list[dict[str, Any]] = entry.setdefault("historial", [])
    history.append(
        {"fecha": today, "cambio": "sustituido", "origen_anterior": previous, "origen": spec}
    )
    entry["origen"] = spec
    if include:
        entry["incluir"] = list(include)
    else:
        entry.pop("incluir", None)
    entry["ficheros"] = {}
    entry.pop("sincronizado", None)
    return previous


# --- sincronización ---


def md_twin(staging: Path, rel: str) -> Path:
    """Conversión Markdown de un fichero de ``_staging/<nombre>/`` (convención de convert_to_md)."""
    return staging / "md" / Path(rel).with_suffix(".md")


def _invalidate(staging: Path, rel: str) -> None:
    """Borra el binario y su ``.md``: convert_to_md omite los ficheros ya convertidos."""
    for path in (staging / rel, md_twin(staging, rel)):
        path.unlink(missing_ok=True)


def sync_source(
    root: Path, name: str, entry: dict[str, Any], today: str, dry_run: bool = False
) -> list[Change]:
    """Copia a ``_staging/<nombre>/`` los ficheros nuevos o cambiados y retira los eliminados."""
    spec = str(entry.get("origen", ""))
    include = tuple(str(g) for g in entry.get("incluir", []))
    resolved = resolve(spec, include)
    staging = root / STAGING_DIR / name
    known: dict[str, Any] = entry.setdefault("ficheros", {})
    history: list[dict[str, Any]] = entry.setdefault("historial", [])
    changes: list[Change] = []
    current: dict[str, Any] = {}
    for item in resolved:
        digest = sha256(item.source)
        previous = known.get(item.rel)
        record = {
            "sha256": digest,
            "bytes": item.source.stat().st_size,
            "origen": str(item.source),
            "version": item.version,
        }
        current[item.rel] = record
        unchanged = (
            isinstance(previous, dict)
            and previous.get("sha256") == digest
            and previous.get("version") == item.version
            and (staging / item.rel).is_file()
        )
        if unchanged:
            continue
        old_version = previous.get("version") if isinstance(previous, dict) else None
        kind = "modificado" if isinstance(previous, dict) else "alta"
        changes.append(Change(kind, item.rel, item.version, old_version))
        if not dry_run:
            _invalidate(staging, item.rel)
            target = staging / item.rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(item.source, target)
    for rel in sorted(set(known) - set(current)):
        old = known[rel]
        old_version = old.get("version") if isinstance(old, dict) else None
        changes.append(Change("baja", rel, None, old_version))
        if not dry_run:
            _invalidate(staging, rel)
    if dry_run or not changes:
        return changes
    for change in changes:
        event: dict[str, Any] = {"fecha": today, "fichero": change.rel, "cambio": change.kind}
        if change.kind != "baja":
            event["sha256"] = current[change.rel]["sha256"]
        if change.version is not None:
            event["version"] = change.version
        if change.previous_version is not None and change.previous_version != change.version:
            event["version_anterior"] = change.previous_version
        history.append(event)
    entry["ficheros"] = dict(sorted(current.items()))
    entry["sincronizado"] = today
    return changes


def format_change(name: str, change: Change) -> str:
    version = ""
    if change.previous_version and change.previous_version != change.version:
        version = f" (v{change.previous_version} → v{change.version})"
    elif change.version:
        version = f" (v{change.version})"
    return f"  {change.kind.upper():<10} {name}/{change.rel}{version}"


# --- CLI ---


def _manifest_path(args: argparse.Namespace) -> Path:
    root: Path = args.root.resolve()
    return root / MANIFEST


def _cmd_add(args: argparse.Namespace) -> int:
    path = _manifest_path(args)
    data = read_manifest(path)
    declare(data, args.name, args.source, tuple(args.include or ()))
    write_manifest(path, data)
    print(f"[snapshot] Origen «{args.name}» declarado en {path}. Ejecuta `sync` para copiarlo.")
    return 0


def _cmd_replace(args: argparse.Namespace) -> int:
    root: Path = args.root.resolve()
    path = _manifest_path(args)
    data = read_manifest(path)
    today = args.date or date.today().isoformat()
    previous = replace_source(data, args.name, args.source, tuple(args.include or ()), today)
    staging = root / STAGING_DIR / args.name
    if staging.is_dir():  # el binario anterior y su md/ ya no corresponden al origen
        shutil.rmtree(staging)
    write_manifest(path, data)
    print(f"[snapshot] «{args.name}»: {previous} → {args.source} (sustituido, {today}).")
    print(
        f"[snapshot] Ejecuta `sync` para copiar el documento nuevo; los ficheros antiguos de "
        f"_fuentes/{args.name}/ quedan huérfanos (Fase 0c: listar y borrar con confirmación)."
    )
    return 0


def _cmd_sync(args: argparse.Namespace) -> int:
    root: Path = args.root.resolve()
    path = _manifest_path(args)
    data = read_manifest(path)
    sources: dict[str, Any] = data["fuentes"]
    names: list[str] = args.names or sorted(sources)
    unknown = [n for n in names if n not in sources]
    if unknown:
        raise SnapshotError(f"orígenes no declarados: {', '.join(unknown)} (usa `add`)")
    if not names:
        print("[snapshot] No hay orígenes declarados (usa `add`).")
        return 0
    today = args.date or date.today().isoformat()
    total = 0
    failed: list[str] = []
    for name in names:
        try:
            changes = sync_source(root, name, sources[name], today, args.dry_run)
        except (SnapshotError, OSError) as exc:  # un origen caído no frena a los demás
            failed.append(name)
            print(f"[snapshot] ERROR en {name}: {exc}", file=sys.stderr)
            continue
        total += len(changes)
        state = "sin cambios" if not changes else f"{len(changes)} cambio(s)"
        print(f"[snapshot] {name}: {state}")
        for change in changes:
            print(format_change(name, change))
        if changes and not args.dry_run:  # tras cada origen: _staging/ y manifiesto a la par
            write_manifest(path, data)
    if args.dry_run:
        print("[snapshot] --dry-run: no se ha copiado nada.")
    elif total:
        print(f"[snapshot] Manifiesto actualizado: {path}")
    if failed:
        return 2
    return 1 if total else 0


def _cmd_list(args: argparse.Namespace) -> int:
    data = read_manifest(_manifest_path(args))
    for name, entry in sorted(data["fuentes"].items()):
        files: dict[str, Any] = entry.get("ficheros", {})
        print(f"{name}: {entry.get('origen')} · {len(files)} fichero(s)")
        for rel, record in files.items():
            version = f" v{record['version']}" if record.get("version") else ""
            print(f"  {rel}{version} · {str(record.get('sha256', ''))[:12]}")
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Instantánea local de orígenes documentales.")
    parser.add_argument(
        "--root", type=Path, required=True, help="Raíz del destino (carpeta con mkdocs.yml)."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Declara un origen en el manifiesto.")
    add.add_argument("name", help="Nombre del origen (carpeta en _staging/ y _fuentes/).")
    add.add_argument("source", help="Fichero, carpeta o patrón con {ver}.")
    add.add_argument("--include", action="append", help="Patrón glob (repetible, carpetas).")
    add.set_defaults(func=_cmd_add)

    rep = sub.add_parser(
        "replace",
        help="Sustituye un origen por un documento reestructurado (lo indica el usuario).",
    )
    rep.add_argument("name", help="Nombre del origen ya declarado.")
    rep.add_argument("source", help="Fichero, carpeta o patrón con {ver} del documento nuevo.")
    rep.add_argument("--include", action="append", help="Patrón glob (repetible, carpetas).")
    rep.add_argument("--date", help="Fecha del historial YYYY-MM-DD (por defecto, hoy).")
    rep.set_defaults(func=_cmd_replace)

    sync = sub.add_parser("sync", help="Copia los orígenes cambiados a _staging/.")
    sync.add_argument("names", nargs="*", help="Orígenes a sincronizar (por defecto, todos).")
    sync.add_argument("--dry-run", action="store_true", help="Solo informa; no copia.")
    sync.add_argument("--date", help="Fecha del historial YYYY-MM-DD (por defecto, hoy).")
    sync.set_defaults(func=_cmd_sync)

    lst = sub.add_parser("list", help="Muestra los orígenes declarados.")
    lst.set_defaults(func=_cmd_list)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        code: int = args.func(args)
    except (SnapshotError, OSError) as exc:
        print(f"[snapshot] ERROR: {exc}", file=sys.stderr)
        return 2
    return code


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    sys.exit(main())
