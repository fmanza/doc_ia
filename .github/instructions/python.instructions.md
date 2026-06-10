---
applyTo: "scripts/**/*.py,tests/**/*.py"
---
# Reglas para ficheros Python — doc_ia

> **TL;DR** — Tooling determinista: tipado strict, sin servicios IA, sin red en tests,
> scripts standalone con exit code.

---

## Naturaleza del código

Todo el Python de este repositorio es **tooling determinista de documentación**.
No existe librería de negocio ni paquete instalable: `scripts/` contiene CLIs standalone
y `tests/` sus tests unitarios.

## Reglas obligatorias

### Estructura
- Cada script en `scripts/` es ejecutable standalone: `python scripts/<nombre>.py`.
- Docstring de módulo obligatorio (qué hace y qué NO hace — p.ej. "No invoca ningún servicio IA").
- Lógica testeable en funciones puras; `main() -> int` + `if __name__ == "__main__": sys.exit(main())`.
- Exit code: `0` éxito, `≠0` fallo (los hooks y el CI dependen de ello).

### Tipado y estilo
- Type hints completos en todas las funciones; debe pasar `python -m mypy scripts` (modo strict).
- `ruff check` y `ruff format` limpios (config en `pyproject.toml`: line-length 100, reglas E/F/W/I/UP/B).
- F-strings para interpolación; nunca `.format()`, `%` ni concatenación.
- `from __future__ import annotations` en scripts con tipos no triviales.

### Prohibiciones (principios del producto)
- ❌ Llamadas a APIs de servicios IA (OpenAI, Anthropic, Google…) — la generación ocurre en chat.
- ❌ Credenciales, tokens o API keys (ni hardcoded ni leídas de `.env`).
- ❌ Dependencias de red en tests.
- ❌ Estado global mutable.
- ✅ `print()` permitido: los scripts son CLIs, no librería.

### Dependencias
- Solo las de `requirements.txt` (mkdocs-material, ruff, mypy, pytest) y stdlib.
- Añadir una dependencia nueva exige actualizar `requirements.txt` + README + justificación en PR.

## Tests

- Ubicación: `tests/test_<nombre_script>.py`.
- Import del script vía `sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))`
  (patrón de `tests/test_check_env.py`; no hay paquete instalable).
- Deterministas: mismo input → mismo output; sin red, sin filesystem fuera de `tmp_path`.

## Validación antes de commit

```bash
python -m ruff check scripts tests
python -m ruff format scripts tests
python -m mypy scripts
python -m pytest
```

---

*Regenerado en bootstrap: 2026-06-10*
