# Estándares — doc_ia

> Contexto persistente para agentes IA. Regenerado en el bootstrap (2026-06-10).
> El detalle normativo vive en `.github/SHARED_INSTRUCTIONS.md` (canónico); esta página
> es el resumen operativo que los agentes cargan antes de planificar.

## Código (scripts/ y tests/)

- Python >= 3.12; `mypy --strict` sin errores; `ruff check` + `ruff format` limpios.
- F-strings para interpolación; sin `.format()` ni `%`.
- Scripts standalone con exit code (`0` éxito, `≠0` fallo); `print()` permitido (son CLIs).
- Prohibido: llamadas a APIs de IA, credenciales, estado global mutable, red en tests.
- Docstring de módulo obligatorio en cada script y cada test.

## Tests

- Deterministas, unitarios, sin servicios externos.
- Patrón de import: `sys.path.insert` hacia `scripts/` (ver `tests/test_check_env.py`).
- Nuevo script ⇒ nuevo `tests/test_<nombre>.py`.

## Documentación

- Arquetipos formales de `.github/DOCUMENTATION_STANDARD.md`; secciones fijas, nunca omitidas.
- Nombres en `docs/`: minúsculas con guiones bajos; guías siempre en `docs/guides/`.
- `mkdocs.yml` es la fuente única de navegación; actualizar al crear/mover/borrar páginas.
- Validación: `python -m mkdocs build --strict` sin errores ni warnings.
- No inventar capacidades/módulos/APIs; marcar como pendiente lo no verificable.
- Ejemplos de código en `.py` reales bajo `docs/examples/` referenciados con `--8<--` (SSOT).

## Instrucciones IA

- Regla de oro: editar `.github/SHARED_INSTRUCTIONS.md` primero; entry points solo especializan.
- Rutas relativas y portables; cero referencias a otros proyectos (p.ej. util_bbdd).
- Cambios de agentes ⇒ actualizar `.github/AGENTS.md` e `INTEGRATION_MAP.md`.

## Versionado y cierre

- Conventional Commits; SemVer (`pyproject.toml` es la versión canónica).
- Fase VERSION: checklist de `.github/instructions/sync.instructions.md` +
  poblar `## Directrices para Futuras IAs` en el TRACEABILITY.md de la sesión.

## Seguridad

- `.gitignore` bloquea `.env*`, `*.key`, `*.pem`, `secrets*`, `.claude/settings.local.json`.
- Workflows CI solo con `GITHUB_TOKEN` nativo; nunca secrets de servicios IA.
