#!/usr/bin/env python3
"""Kit de documentación de doc_ia: instala, sincroniza y comprueba su copia en un destino.

Un destino documentado con doc_ia lleva dentro todo lo necesario para relanzar la documentación
sin abrir doc_ia: la metodología y los scripts en ``<destino>/.doc_ia/`` (copia fijada), los
lanzadores por plataforma (``/documentar``) en su raíz y ``DOCUMENTAR.md`` con instrucciones.
Qué se copia lo decide la lista blanca ``.github/kit/MANIFEST.txt``. No accede a la red.

Subcomandos:

  install / sync  Copia o actualiza el kit desde doc_ia (``--from``; por defecto, el doc_ia que
                  contiene este script). Nunca pisa un fichero editado en el destino ni un
                  fichero ajeno con el mismo nombre (``--force`` para hacerlo). Retira lo que
                  doc_ia ya no distribuye. Crea ``DOCUMENTAR.md`` solo si falta.
                  Exit 0 sin cambios · 1 con cambios · 2 conflictos o error.
  check           Comprueba la copia del destino contra ``.doc_ia/kit.lock.json`` (ficheros
                  editados o ausentes) y, con ``--from``, contra doc_ia (desfasados). Avisa si
                  faltan ``DOCUMENTAR.md`` o ``.ai/prompts/documentar.prompt.md``.
                  Exit 0 al día · 1 hallazgos · 2 error.

Uso:
    python <doc_ia>/scripts/kit.py sync --root <destino>
    python <destino>/.doc_ia/scripts/kit.py check --root <destino>
    python <destino>/.doc_ia/scripts/kit.py --from <doc_ia> sync --root <destino>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tomllib
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
KIT_DIR = ".doc_ia"
LOCK_NAME = "kit.lock.json"
MANIFEST = Path(".github") / "kit" / "MANIFEST.txt"
INSTANCE_PROMPT = Path(".ai") / "prompts" / "documentar.prompt.md"
SECTIONS = ("metodologia", "lanzadores", "instancia")
LEADING_COMMENT_RE = re.compile(r"\A<!--.*?-->\s*", re.S)
SITE_NAME_RE = re.compile(r"^site_name:\s*['\"]?(.+?)['\"]?\s*$", re.M)


class KitError(Exception):
    """doc_ia de origen inválido, manifiesto mal formado o destino inutilizable."""


@dataclass(frozen=True)
class Manifest:
    """Lista blanca: metodología (a ``.doc_ia/``), lanzadores e instancia (origen -> destino)."""

    methodology: tuple[str, ...]
    launchers: tuple[tuple[str, str], ...]
    instance: tuple[tuple[str, str], ...]


@dataclass
class Report:
    """Resultado de ``sync``/``check``: cambios aplicados (o previstos) y conflictos."""

    changes: list[tuple[str, str]] = field(default_factory=list)
    conflicts: list[tuple[str, str]] = field(default_factory=list)


# --- manifiesto y huellas ---


def parse_manifest(path: Path) -> Manifest:
    """Lee la lista blanca por secciones ``[metodologia]``, ``[lanzadores]``, ``[instancia]``."""
    if not path.is_file():
        raise KitError(f"no es un doc_ia válido: falta {path}")
    found: dict[str, list[str]] = {name: [] for name in SECTIONS}
    section: str | None = None
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1]
            if section not in found:
                raise KitError(f"{path}:{number}: sección desconocida [{section}]")
            continue
        if section is None:
            raise KitError(f"{path}:{number}: entrada fuera de sección")
        found[section].append(line)

    def pairs(name: str) -> tuple[tuple[str, str], ...]:
        result: list[tuple[str, str]] = []
        for entry in found[name]:
            source, arrow, target = entry.partition("->")
            if not arrow or not source.strip() or not target.strip():
                raise KitError(f"{path}: [{name}] espera «origen -> destino»: {entry}")
            result.append((source.strip(), target.strip()))
        return tuple(result)

    return Manifest(tuple(found["metodologia"]), pairs("lanzadores"), pairs("instancia"))


def sha256(path: Path) -> str:
    """Huella del contenido; en texto, independiente del fin de línea (CRLF = LF).

    git convierte los finales de línea al hacer checkout (``autocrlf``, ``eol=lf``): sin
    normalizar, el mismo fichero tendría otra huella en otro equipo y ``check`` lo daría por
    editado.
    """
    data = path.read_bytes()
    if b"\0" not in data[:8192]:  # texto
        data = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def doc_ia_version(source: Path) -> str:
    with (source / "pyproject.toml").open("rb") as fh:
        version: str = tomllib.load(fh)["project"]["version"]
    return version


def read_lock(dest: Path) -> dict[str, Any]:
    path = dest / KIT_DIR / LOCK_NAME
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise KitError(f"lock con JSON inválido: {path} ({exc})") from exc
    return data if isinstance(data, dict) else {}


def write_lock(dest: Path, version: str, files: dict[str, str], today: str) -> None:
    path = dest / KIT_DIR / LOCK_NAME
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {"doc_ia": version, "fecha": today, "ficheros": dict(sorted(files.items()))}
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def managed_files(source: Path, manifest: Manifest) -> dict[str, Path]:
    """Ruta en el destino (POSIX) → fichero de doc_ia, para todo lo que gestiona el kit."""
    files = {f"{KIT_DIR}/{rel}": source / rel for rel in manifest.methodology}
    files.update({target: source / origin for origin, target in manifest.launchers})
    return files


def render_instance(template: Path, dest: Path) -> str:
    """Plantilla del proyecto sin su comentario inicial y con ``{proyecto}`` resuelto."""
    text = LEADING_COMMENT_RE.sub("", template.read_text(encoding="utf-8"), count=1)
    config = dest / "mkdocs.yml"
    match = SITE_NAME_RE.search(config.read_text(encoding="utf-8")) if config.is_file() else None
    return text.replace("{proyecto}", match.group(1) if match else dest.name)


# --- operaciones ---


def resolve_source(source: Path | None) -> Path:
    """doc_ia de origen: ``--from`` o el repositorio que contiene este script (no una copia)."""
    candidate = (source or ROOT).resolve()
    if candidate.name == KIT_DIR:
        raise KitError("este kit.py es la copia de un destino: indica el doc_ia con --from")
    return candidate


def sync(
    source: Path, dest: Path, *, force: bool = False, dry_run: bool = False, today: str = ""
) -> Report:
    """Instala o actualiza el kit de ``source`` en ``dest``."""
    source, dest = source.resolve(), dest.resolve()
    if dest == source or (dest / KIT_DIR).resolve() == source:
        raise KitError("el destino no puede ser el propio doc_ia")
    if not dest.is_dir():
        raise KitError(f"el destino no existe: {dest}")
    manifest = parse_manifest(source / MANIFEST)
    lock = read_lock(dest)
    locked: dict[str, str] = (
        lock.get("ficheros", {}) if isinstance(lock.get("ficheros"), dict) else {}
    )
    report = Report()
    files: dict[str, str] = {}
    for target_rel, origin in managed_files(source, manifest).items():
        if not origin.is_file():
            raise KitError(f"el manifiesto cita un fichero que no existe en doc_ia: {origin}")
        wanted = sha256(origin)
        target = dest / target_rel
        previous = locked.get(target_rel)
        if target.is_file():
            current = sha256(target)
            if current == wanted:
                files[target_rel] = wanted
                continue
            if not force and previous is None:
                report.conflicts.append((target_rel, "fichero ajeno: no lo instaló el kit"))
                continue
            if not force and current != previous:
                report.conflicts.append((target_rel, "editado en el destino"))
                files[target_rel] = previous or current
                continue
            report.changes.append(("actualizado", target_rel))
        else:
            report.changes.append(("creado", target_rel))
        files[target_rel] = wanted
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(origin, target)
    for target_rel, previous in sorted(locked.items()):
        if target_rel in files or any(target_rel == c for c, _ in report.conflicts):
            continue
        target = dest / target_rel
        if target.is_file() and sha256(target) != previous and not force:
            report.conflicts.append((target_rel, "doc_ia ya no lo distribuye y está editado"))
            files[target_rel] = previous
            continue
        if target.is_file():
            report.changes.append(("retirado", target_rel))
            if not dry_run:
                target.unlink()
    for origin_rel, target_rel in manifest.instance:
        target = dest / target_rel
        if not target.is_file():
            report.changes.append(("creado", target_rel))
            if not dry_run:
                target.write_text(render_instance(source / origin_rel, dest), encoding="utf-8")
    version = doc_ia_version(source)
    unchanged = lock.get("doc_ia") == version and locked == files
    if not dry_run and not unchanged:  # sin cambios no se reescribe: ningún diff en el destino
        write_lock(dest, version, files, today or date.today().isoformat())
    return report


def check(dest: Path, source: Path | None = None) -> Report:
    """Integridad del kit del destino y, con ``source``, ficheros desfasados respecto a doc_ia."""
    dest = dest.resolve()
    report = Report()
    lock = read_lock(dest)
    locked = lock.get("ficheros")
    if not isinstance(locked, dict) or not locked:
        report.conflicts.append((f"{KIT_DIR}/{LOCK_NAME}", "kit no instalado"))
        return report
    for target_rel, previous in sorted(locked.items()):
        target = dest / target_rel
        if not target.is_file():
            report.conflicts.append((target_rel, "falta"))
        elif sha256(target) != previous:
            report.conflicts.append((target_rel, "editado en el destino"))
    for rel in ("DOCUMENTAR.md", INSTANCE_PROMPT.as_posix()):
        if not (dest / rel).is_file():
            report.conflicts.append((rel, "falta (lo crea /documentar o el CIERRE)"))
    if source is not None:
        source = resolve_source(source)  # nunca la copia del propio destino
        shipped = managed_files(source, parse_manifest(source / MANIFEST))
        for target_rel, origin in shipped.items():
            if target_rel not in locked:
                report.changes.append(("nuevo en doc_ia", target_rel))
            elif origin.is_file() and sha256(origin) != locked[target_rel]:
                report.changes.append(("desfasado", target_rel))
        for target_rel in sorted(set(locked) - set(shipped)):
            report.changes.append(("retirado en doc_ia", target_rel))
    return report


# --- CLI ---


def _print(report: Report) -> None:
    for kind, rel in report.changes:
        print(f"  {kind.upper():<16} {rel}")
    for rel, reason in report.conflicts:
        print(f"  {'CONFLICTO':<16} {rel} — {reason}")


def _cmd_sync(args: argparse.Namespace) -> int:
    source = resolve_source(args.source)
    report = sync(source, args.root, force=args.force, dry_run=args.dry_run, today=args.date or "")
    version = doc_ia_version(source)
    state = "sin cambios" if not report.changes else f"{len(report.changes)} cambio(s)"
    print(f"[kit] doc_ia {version} → {args.root.resolve()}: {state}")
    _print(report)
    if args.dry_run:
        print("[kit] --dry-run: no se ha escrito nada.")
    if report.conflicts:
        print(f"[kit] {len(report.conflicts)} conflicto(s): revisa o usa --force.", file=sys.stderr)
        return 2
    return 1 if report.changes else 0


def _cmd_check(args: argparse.Namespace) -> int:
    source = args.source.resolve() if args.source else None
    report = check(args.root, source)
    lock = read_lock(args.root.resolve())
    print(f"[kit] kit doc_ia {lock.get('doc_ia', '—')} en {args.root.resolve()}")
    _print(report)
    if not report.changes and not report.conflicts:
        print("[kit] Kit al día.")
        return 0
    return 1


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Kit de documentación de doc_ia en un destino.")
    parser.add_argument(
        "--from",
        dest="source",
        type=Path,
        help="doc_ia de origen (por defecto, el de este script).",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("install", "sync"):
        cmd = sub.add_parser(name, help="Instala o actualiza el kit en el destino.")
        cmd.add_argument("--root", type=Path, required=True, help="Raíz del destino (mkdocs.yml).")
        cmd.add_argument("--force", action="store_true", help="Sobrescribe editados y ajenos.")
        cmd.add_argument("--dry-run", action="store_true", help="Solo informa; no escribe.")
        cmd.add_argument("--date", help="Fecha del lock YYYY-MM-DD (por defecto, hoy).")
        cmd.set_defaults(func=_cmd_sync)
    chk = sub.add_parser("check", help="Comprueba el kit del destino.")
    chk.add_argument("--root", type=Path, required=True, help="Raíz del destino (mkdocs.yml).")
    chk.set_defaults(func=_cmd_check)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        code: int = args.func(args)
    except (KitError, OSError) as exc:
        print(f"[kit] ERROR: {exc}", file=sys.stderr)
        return 2
    return code


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    sys.exit(main())
