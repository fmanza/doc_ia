#!/usr/bin/env python3
"""Publicación y control de las capturas del origen WEB (manual de funcionamiento, Arquetipo 15).

El origen WEB es la aplicación **desplegada** en un entorno (p. ej. PRE). Sus capturas las
aporta el usuario o, en modo navegador, se toman en el chat, nunca desde un script: este script
**no accede a la red** y no abre ningún navegador. Las capturas llegan a
``<raíz del destino>/_staging/<origen>/`` (``snapshot_sources.py add`` + ``sync``), que no se
versiona. Para entrar en la documentación hacen falta dos pasos:

* ``publish``: copia a ``docs/assets/manual/<origen>/`` **solo** las capturas que se le pasan
  (las que una persona ha revisado: sin datos personales reales) y las registra en
  ``.ai/captures.json`` con su huella SHA256, el entorno, la versión desplegada y el rol.
* ``check``: comprueba que lo publicado y lo registrado coinciden y que las páginas citan bien
  las capturas:

  ``sin_registrar``  imagen en ``docs/assets/manual/`` que no pasó por ``publish``
  ``modificada``     imagen cuya huella ya no es la registrada (cambió tras la revisión)
  ``falta``          captura registrada cuyo fichero ya no existe
  ``rota``           página que cita una captura de ``assets/manual/`` inexistente
  ``sin_alt``        cita sin texto alternativo
  ``huerfana``       captura publicada que ninguna página cita
  ``url``            el manifiesto contiene una URL (la URL del entorno nunca se versiona)

Uso:
    python scripts/web_captures.py --root <destino> publish <origen> <captura> [<captura> …]
        --env PRE --version 1.8.8 [--role Coordinador] [--date YYYY-MM-DD]
    python scripts/web_captures.py --root <destino> check

``<captura>`` es la ruta relativa a ``_staging/<origen>/``. Exit de ``publish``: 0 · 2 error.
Exit de ``check``: 0 sin hallazgos · 1 con hallazgos · 2 error.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import shutil
import sys
import tomllib
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent

STAGING_DIR = "_staging"
DOCS_DIR = "docs"
CAPTURES_DIR = "assets/manual"
MANIFEST = Path(".ai") / "captures.json"
FORMAT = "doc_ia.web_captures"
FORMAT_VERSION = 1
IMAGE_SUFFIXES = frozenset({".png", ".jpg", ".jpeg", ".webp", ".gif"})
NAME_RE = re.compile(r"^(?!\.+$)[\w.-]+$")  # «.» o «..» saldrían de _staging/
CHUNK = 1 << 20

# Imagen Markdown ``![alt](ruta "título"){ attr }`` e ``<img … src="…" … alt="…">``.
MD_IMAGE_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<src>[^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_IMAGE_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
HTML_ATTR_RE = re.compile(r"(\w+)\s*=\s*(?:\"([^\"]*)\"|'([^']*)')")
# Bloques delimitados (también indentados dentro de admoniciones) y código inline.
FENCE_RE = re.compile(r"^[ \t]*(`{3,}|~{3,}).*?^[ \t]*\1", re.MULTILINE | re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
URL_RE = re.compile(r"[a-z][a-z0-9+.-]*://", re.IGNORECASE)


class CaptureError(Exception):
    """Publicación imposible: origen o captura inválidos, o manifiesto ilegible."""


@dataclass(frozen=True)
class Finding:
    """Hallazgo de ``check``: tipo, ruta (relativa a la raíz del destino) y detalle."""

    kind: str
    path: str
    detail: str = ""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(CHUNK), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _doc_ia_version() -> str:
    with (ROOT / "pyproject.toml").open("rb") as fh:
        version: str = tomllib.load(fh)["project"]["version"]
    return version


def read_manifest(path: Path) -> dict[str, Any]:
    """Manifiesto ``.ai/captures.json``; vacío si no existe."""
    if not path.is_file():
        return {"format": FORMAT, "format_version": FORMAT_VERSION, "origenes": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CaptureError(f"manifiesto con JSON inválido: {path} ({exc})") from exc
    if (
        not isinstance(data, dict)
        or data.get("format") != FORMAT
        or not isinstance(data.get("origenes"), dict)
    ):
        raise CaptureError(f"manifiesto inválido: {path}")
    for name, entry in data["origenes"].items():
        if not isinstance(entry, dict) or not isinstance(entry.get("capturas", {}), dict):
            raise CaptureError(f"manifiesto inválido: {path} (origen «{name}»)")
    return data


def write_manifest(path: Path, data: dict[str, Any]) -> None:
    """Escribe el manifiesto con orden estable (diffs legibles en git)."""
    origins: dict[str, Any] = {}
    for name, entry in sorted(data.get("origenes", {}).items()):
        captures = dict(sorted(entry.get("capturas", {}).items()))
        origins[name] = {
            **{k: v for k, v in entry.items() if k != "capturas"},
            "capturas": captures,
        }
    ordered = {
        "format": FORMAT,
        "format_version": FORMAT_VERSION,
        "doc_ia": _doc_ia_version(),
        "origenes": origins,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(ordered, indent=2, ensure_ascii=False) + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")


def _require_text(label: str, value: str) -> str:
    value = value.strip()
    if not value:
        raise CaptureError(f"{label} vacío")
    if URL_RE.search(value):
        raise CaptureError(f"{label} no puede ser una URL (la URL del entorno no se versiona)")
    return value


def _capture_rel(rel: str) -> str:
    """Ruta relativa normalizada (``/``) de una captura; rechaza rutas que salgan del origen."""
    norm = posixpath.normpath(rel.replace("\\", "/"))
    if norm.startswith(("../", "/")) or norm in {".", ".."} or re.match(r"^[A-Za-z]:", norm):
        raise CaptureError(f"ruta de captura fuera del origen: {rel}")
    if Path(norm).suffix.lower() not in IMAGE_SUFFIXES:
        raise CaptureError(f"no es una imagen ({', '.join(sorted(IMAGE_SUFFIXES))}): {rel}")
    return norm


def publish(
    root: Path,
    origin: str,
    captures: list[str],
    *,
    env: str,
    version: str,
    role: str | None = None,
    today: str | None = None,
) -> list[str]:
    """Copia las capturas revisadas de ``_staging/<origen>/`` a ``docs/assets/manual/<origen>/``.

    Valida todo antes de copiar nada. Devuelve las rutas publicadas (relativas a la raíz).
    """
    if not NAME_RE.fullmatch(origin):
        raise CaptureError(f"nombre de origen inválido «{origin}» (letras, dígitos, . _ -)")
    env = _require_text("--env", env)
    version = _require_text("--version", version)
    if role is not None:
        role = _require_text("--role", role)
    if not captures:
        raise CaptureError("sin capturas que publicar")
    staging = root / STAGING_DIR / origin
    rels = [_capture_rel(rel) for rel in captures]
    for rel in rels:
        if not (staging / rel).is_file():
            raise CaptureError(f"no existe en {STAGING_DIR}/{origin}/: {rel}")
    manifest_path = root / MANIFEST
    data = read_manifest(manifest_path)
    entry = data["origenes"].setdefault(origin, {"capturas": {}})
    entry["entorno"] = env
    entry["version"] = version
    published: list[str] = []
    for rel in rels:
        target = root / DOCS_DIR / CAPTURES_DIR / origin / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(staging / rel, target)
        record: dict[str, Any] = {
            "sha256": sha256(target),
            "version": version,
            "publicada": today or date.today().isoformat(),
        }
        if role is not None:
            record["rol"] = role
        entry["capturas"][rel] = record
        published.append(target.relative_to(root).as_posix())
    write_manifest(manifest_path, data)
    return published


def _references(page: Path, docs: Path) -> list[tuple[str, str]]:
    """``(alt, ruta relativa a docs/)`` de las imágenes de ``assets/manual/`` que cita la página."""
    text = INLINE_CODE_RE.sub("", FENCE_RE.sub("", page.read_text(encoding="utf-8")))
    found: list[tuple[str, str]] = [(m["alt"], m["src"]) for m in MD_IMAGE_RE.finditer(text)]
    for tag in HTML_IMAGE_RE.findall(text):
        attrs = {k.lower(): dq or sq for k, dq, sq in HTML_ATTR_RE.findall(tag)}
        if "src" in attrs:
            found.append((attrs.get("alt", ""), attrs["src"]))
    refs: list[tuple[str, str]] = []
    page_dir = page.parent.relative_to(docs).as_posix()
    for alt, src in found:
        src = src.split("#", 1)[0].split("?", 1)[0]
        if URL_RE.match(src) or CAPTURES_DIR not in src:
            continue
        refs.append((alt, posixpath.normpath(posixpath.join(page_dir, src))))
    return refs


def check(root: Path) -> list[Finding]:
    """Coherencia entre ``docs/assets/manual/``, ``.ai/captures.json`` y las páginas."""
    findings: list[Finding] = []
    manifest_path = root / MANIFEST
    if manifest_path.is_file() and URL_RE.search(manifest_path.read_text(encoding="utf-8")):
        findings.append(Finding("url", MANIFEST.as_posix(), "contiene una URL"))
    data = read_manifest(manifest_path)
    docs = root / DOCS_DIR
    registered: dict[str, str] = {}
    for origin, entry in data["origenes"].items():
        for rel, record in entry.get("capturas", {}).items():
            path = f"{CAPTURES_DIR}/{origin}/{rel}"
            registered[path] = str(record.get("sha256", "")) if isinstance(record, dict) else ""
    on_disk: set[str] = set()
    folder = docs / CAPTURES_DIR
    if folder.is_dir():
        on_disk = {
            p.relative_to(docs).as_posix()
            for p in folder.rglob("*")
            if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES
        }
    for path in sorted(on_disk - set(registered)):
        findings.append(Finding("sin_registrar", f"{DOCS_DIR}/{path}", "no pasó por publish"))
    for path, digest in sorted(registered.items()):
        if path not in on_disk:
            findings.append(Finding("falta", f"{DOCS_DIR}/{path}", "registrada y sin fichero"))
        elif sha256(docs / path) != digest:
            findings.append(Finding("modificada", f"{DOCS_DIR}/{path}", "cambió tras publish"))
    cited: set[str] = set()
    if docs.is_dir():
        for page in sorted(docs.rglob("*.md")):
            page_rel = page.relative_to(root).as_posix()
            for alt, target in _references(page, docs):
                cited.add(target)
                if not alt.strip():
                    findings.append(Finding("sin_alt", page_rel, target))
                if not (docs / target).is_file():
                    findings.append(Finding("rota", page_rel, target))
    for path in sorted((set(registered) & on_disk) - cited):
        findings.append(Finding("huerfana", f"{DOCS_DIR}/{path}", "ninguna página la cita"))
    return findings


def _cmd_publish(args: argparse.Namespace) -> int:
    published = publish(
        args.root,
        args.origin,
        args.captures,
        env=args.env,
        version=args.version,
        role=args.role,
        today=args.date,
    )
    for path in published:
        print(f"[captures] publicada {path}")
    print(f"[captures] {len(published)} captura(s) publicada(s) · {MANIFEST.as_posix()}")
    return 0


def _cmd_check(args: argparse.Namespace) -> int:
    findings = check(args.root)
    for finding in findings:
        detail = f" · {finding.detail}" if finding.detail else ""
        print(f"[captures] {finding.kind}: {finding.path}{detail}")
    print(f"[captures] {len(findings)} hallazgo(s).")
    return 1 if findings else 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Capturas del origen WEB (Arquetipo 15).")
    parser.add_argument(
        "--root", type=Path, required=True, help="Raíz del destino (carpeta con mkdocs.yml)."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    pub = sub.add_parser("publish", help="Publica capturas revisadas en docs/assets/manual/.")
    pub.add_argument("origin", help="Nombre del origen (carpeta en _staging/).")
    pub.add_argument("captures", nargs="+", help="Capturas revisadas, relativas al origen.")
    pub.add_argument("--env", required=True, help="Entorno (p. ej. PRE). Nunca la URL.")
    pub.add_argument("--version", required=True, help="Versión desplegada que se ve.")
    pub.add_argument("--role", help="Rol con el que se tomaron las capturas.")
    pub.add_argument("--date", help="Fecha de publicación YYYY-MM-DD (por defecto, hoy).")
    pub.set_defaults(func=_cmd_publish)

    chk = sub.add_parser("check", help="Comprueba capturas, manifiesto y citas.")
    chk.set_defaults(func=_cmd_check)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        code: int = args.func(args)
    except (CaptureError, OSError, UnicodeDecodeError) as exc:
        print(f"[captures] ERROR: {exc}", file=sys.stderr)
        return 2
    return code


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    sys.exit(main())
