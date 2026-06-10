# Guía de Testing con PostToolUse — doc_ia

> Plantilla inicial creada en el bootstrap (2026-06-10).

## Hooks configurados (`.claude/settings.json`)

Tras cada `Edit`/`Write`, Claude Code ejecuta automáticamente:

1. `python -m ruff check scripts tests --quiet` — linting
2. `python -m mypy scripts --no-error-summary` — type-checking strict
3. `python -m pytest --collect-only -q tests` — validación de sintaxis de tests (no ejecución)

## Ejecución manual completa

```bash
python -m pytest            # Suite completa (rápida: tests unitarios deterministas)
python -m pytest -k <expr>  # Subconjunto por nombre
```

## Reglas de testing del proyecto

- Tests deterministas: sin red, sin credenciales, sin servicios externos.
- Los scripts de `scripts/` se testean importando sus funciones
  (patrón en `tests/test_check_env.py`: `sys.path.insert` hacia `scripts/`).
- Nuevo script → nuevo fichero `tests/test_<nombre>.py`.

## Personalización local

```bash
# Copia la plantilla y ajusta en local (git-ignored)
cp .claude/settings.json.example .claude/settings.local.json
```
