#!/usr/bin/env python3
"""Detecta y redacta credenciales en los documentos convertidos (Fase 0c de /document-project).

Los documentos fuente (especificaciones, diseños técnicos, wikis) a veces llevan credenciales en
claro: un ``client_secret`` de OAuth en una URL de ejemplo, una contraseña o un token. Su texto
convertido se versiona en ``_fuentes/``, así que el valor debe sustituirse por ``<REDACTADO>``
**antes** de copiarlo. Este script lo hace de forma determinista sobre ficheros ``.md``:

* Solo sustituye el **valor**, nunca la clave: el documento sigue diciendo que había un
  ``client_secret`` y dónde.
* No toca marcadores evidentes (``xxxxxx``, ``--``, ``***``, ``<…>``, ``${VAR}``), URL ni valores
  ya redactados: es idempotente. En las reglas por palabra clave (``client_secret``,
  ``password``, ``token``) el valor debe tener algún carácter que no sea letra (descarta
  «Password: obligatorio» o «client_secret: proporcionado»); una contraseña solo de letras no se
  detecta.
* El informe da fichero, línea y regla, **nunca el valor** encontrado.
* Es una red de seguridad, no una garantía: la revisión del INVENTARIO sigue siendo obligatoria.

Uso:
    python scripts/redact_secrets.py <ruta> [<ruta> …]           # redacta en el sitio
    python scripts/redact_secrets.py <ruta> [<ruta> …] --check   # solo informa (p. ej. _fuentes/)

Exit 0 sin hallazgos · 1 con hallazgos (redactados o, con ``--check``, pendientes) · 2 error.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REDACTED = "<REDACTADO>"

# Separador entre clave y valor: «=», «:» o «(» con negritas, comillas o espacios de Markdown.
_SEP = r"\s*[=:(]\s*[*`\"']*\s*"
# Guion bajo que docling escapa en Markdown (``client\_secret``).
_US = r"\\?_"
# Valor: sin espacios ni delimitadores de URL, tabla o Markdown.
_VALUE = r"([^\s&*`\"'<>|),;\[\]]{%d,})"
# Reglas por palabra clave en las que una palabra corriente («obligatorio», «Bearer») no es secreto.
_NEEDS_NON_LETTER = frozenset({"client_secret", "password", "token"})


@dataclass(frozen=True)
class SecretRule:
    """Patrón de credencial; el grupo ``value`` (o el patrón entero) es lo que se redacta."""

    name: str
    pattern: re.Pattern[str]


@dataclass(frozen=True)
class Finding:
    """Hallazgo sin el valor: fichero, línea (1-based, del texto original) y regla."""

    path: str
    line: int
    rule: str


RULES: tuple[SecretRule, ...] = (
    SecretRule(
        "private_key",
        re.compile(
            r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.DOTALL
        ),
    ),
    SecretRule(
        "client_secret",
        re.compile(rf"(?i)client{_US}secret{_SEP}(?P<value>{_VALUE % 8})"),
    ),
    SecretRule(
        "password",
        re.compile(rf"(?i)\b(?:password|passwd|pwd|pass|contraseña){_SEP}(?P<value>{_VALUE % 6})"),
    ),
    SecretRule(
        "token",
        re.compile(
            rf"(?i)\b(?:(?:access|refresh|id){_US})?(?:token|api{_US}?key|apikey|secret)"
            rf"{_SEP}(?P<value>{_VALUE % 16})"
        ),
    ),
    SecretRule("url_basic_auth", re.compile(r"://[^/\s:@]+:(?P<value>[^@\s/]{3,})@")),
    SecretRule("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}")),
)

# Marcadores que no son un secreto: x/*/./- repetidos, <…>, {…}, ${VAR}, $VAR o ya redactado.
_PLACEHOLDER = re.compile(r"^(?:[xX*.\-_]+|<[^>]*>|\{[^}]*\}|\$\{?[\w.]+\}?)$")


def _is_placeholder(value: str) -> bool:
    """Marcador, valor ya redactado o URL (``Token url: https://…`` describe un endpoint)."""
    return (
        bool(_PLACEHOLDER.match(value))
        or REDACTED in value
        or "://" in value
        or value.lower().startswith("http")
    )


def _spans(text: str) -> list[tuple[int, int, str]]:
    """Tramos ``(inicio, fin, regla)`` a redactar, sin solapes, en orden de aparición."""
    found: list[tuple[int, int, str]] = []
    for rule in RULES:
        for match in rule.pattern.finditer(text):
            if "value" in rule.pattern.groupindex:
                value = match.group("value")
                if _is_placeholder(value):
                    continue
                if rule.name in _NEEDS_NON_LETTER and value.isalpha():
                    continue
                start, end = match.span("value")
            else:
                if REDACTED in match.group(0):
                    continue
                start, end = match.span()
            found.append((start, end, rule.name))
    found.sort()
    spans: list[tuple[int, int, str]] = []
    for start, end, name in found:
        if spans and start < spans[-1][1]:  # solapa con un tramo anterior (p. ej. JWT en token)
            continue
        spans.append((start, end, name))
    return spans


def find_secrets(text: str) -> list[tuple[int, str]]:
    """Líneas (1-based) y reglas con credenciales en ``text``, sin devolver los valores."""
    return [(text.count("\n", 0, start) + 1, name) for start, _, name in _spans(text)]


def redact(text: str) -> tuple[str, list[tuple[int, str]]]:
    """Texto con cada valor sustituido por ``<REDACTADO>`` y la lista de ``(línea, regla)``."""
    spans = _spans(text)
    hits = [(text.count("\n", 0, start) + 1, name) for start, _, name in spans]
    for start, end, _ in reversed(spans):
        text = text[:start] + REDACTED + text[end:]
    return text, hits


def _markdown_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    if not root.is_dir():
        raise FileNotFoundError(f"no existe: {root}")
    return sorted(p for p in root.rglob("*.md") if p.is_file())


def redact_tree(root: Path, check: bool = False) -> list[Finding]:
    """Redacta (o con ``check``, solo detecta) los ``.md`` de ``root``.

    Conserva los saltos de línea del fichero (lee y escribe bytes).
    """
    findings: list[Finding] = []
    for path in _markdown_files(root):
        raw = path.read_bytes().decode("utf-8")
        new, hits = redact(raw)
        findings.extend(Finding(str(path), line, rule) for line, rule in hits)
        if hits and not check:
            path.write_bytes(new.encode("utf-8"))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Detecta y redacta credenciales en Markdown.")
    parser.add_argument("paths", nargs="+", type=Path, help="Ficheros .md o carpetas.")
    parser.add_argument("--check", action="store_true", help="Solo informa; no modifica.")
    args = parser.parse_args(argv)
    findings: list[Finding] = []
    try:
        for root in args.paths:
            findings.extend(redact_tree(root, args.check))
    except (OSError, UnicodeDecodeError) as exc:
        print(f"[redact] ERROR: {exc}", file=sys.stderr)
        return 2
    action = "pendiente(s) de redactar" if args.check else "redactado(s)"
    for finding in findings:
        print(f"[redact] {finding.path}:{finding.line} · {finding.rule}")
    print(f"[redact] {len(findings)} valor(es) {action}.")
    return 1 if findings else 0


if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    sys.exit(main())
