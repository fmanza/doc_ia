# VERSION CLOSURE — v0.2.0

- Fecha: 2026-10-28
- Rama: `develop` → `main` (merge `--no-ff`) + tag `v0.2.0`
- Alcance: todo `[Unreleased]` desde `0.1.0` (2026-06-10). Sesiones incluidas: 2026-06-11 a
  2026-06-24 (descargas, markitdown, backport `convert_to_md`), 2026-10-28 (arquetipos v2),
  2026-10-28b (hotfix CUDA), 2026-10-28c (calidad) y 2026-10-28d (bloque A de Zensical).

## Commit message

```
release: v0.2.0 - Arquetipo 12, trazabilidad doc_trace, CI y preparación Zensical
```

## Release notes (resumen)

- **Producto (arquetipos)**: Arquetipo 12 Referencia del Sistema (+§6 Datos), regla de evidencia
  §3.16, Variante 1-I Mapa Funcional, columna `Test` en Arq. 1 §7, Arq. 2 §6, 6C despliegue y
  escenarios de calidad. ADR-002 (ACEPTADO) y ADR-003 (PROPUESTO).
- **Tooling**: `scripts/doc_trace.py` (`stamp`/`drift`/`matrix`/`llms`) y `docs/llms.txt`;
  `build_docs_zip.py --builder zensical` con pipeline sin hooks; `check_env.py` avisa de Zensical.
- **`/document-project`**: soporte de Generador = `zensical`; Fase 0b con 3 assets y Mermaid nativo.
- **CI**: `ci.yml` (3.12 y 3.14) con drift bloqueante y paridad Zensical anotada; actions en Node 24.
- **Fixes**: `convert_to_md --device auto`, `.md` con docling, `engine_version`, `check_env` en
  cp1252, diagrama Runtime de `architecture.md`.

Detalle completo: `CHANGELOG.md` § `[0.2.0] — 2026-10-28`.

## Impacto en API pública

- Sin cambios rompedores en los scripts (`convert_to_md.py`, `check_env.py`, `build_docs_zip.py`).
- Nuevo CLI `scripts/doc_trace.py`. `build_docs_zip.py --builder zensical` cambia de comportamiento:
  invoca `python -m zensical` y ejecuta los hooks fuera del build.
- Sin deprecaciones.

## Migraciones (para proyectos destino de doc_ia)

- Fase 0b: 3 assets (`nav.css`, `mermaid.css`, `sidebar-toggle.js`); si el destino tiene el CDN de
  Mermaid o `mermaid.js` propio, se retiran. `custom_fences: mermaid` es obligatorio.
- Páginas de Arq. 1, 2 y 12 con frontmatter `fuentes` deben sellarse con `doc_trace.py stamp` si el
  destino incorpora el tooling (opcional).

## Compatibilidad

- Python 3.12–3.14 (CI en 3.12 y 3.14).
- Generadores: MkDocs + Material 9.x (por defecto); Zensical 0.0.73 en paridad no bloqueante.
- Motores de conversión: docling, markitdown y pandoc sin cambios de contrato.

## Rollback

1. Borrar las releases `v0.2.0` y `docs-v0.2.0` en GitHub y el tag: `git push origin :v0.2.0`.
2. `git revert -m 1 <merge en main>` y push a `main` (vuelve a publicar `docs-v0.1.0` si hay cambios
   en `docs/`).
3. Riesgo: bajo. No hay datos ni esquemas persistentes; los proyectos destino que ya apliquen la
   Fase 0b de 3 assets siguen funcionando con MkDocs.

## Checklist final

- [x] `ruff check scripts tests hooks` y `ruff format --check` sin errores
- [x] `mypy scripts` (strict) sin errores
- [x] `pytest` verde
- [x] `python -m build` (sdist + wheel) exitoso en venv aislado
- [x] `pyproject.toml` → `0.2.0`
- [x] `CHANGELOG.md` → `[0.2.0] — 2026-10-28` (+ `docs/changelog.md` sincronizado)
- [x] `doc_trace drift` sin drift y `llms --check` al día
- [x] `mkdocs build --strict` + ZIP `dist/doc_ia-docs-0.2.0.zip`; tabla de `docs/downloads.md`
- [x] CI de `develop` y de `main`, merge a `main` (`2e8da9d`) y tag `v0.2.0` → release `v0.2.0` correcta
- [ ] Release `docs-v0.2.0`: recrear con `workflow_dispatch` (ver incidente en `TRACEABILITY.md`)

## Handoff

- C2 de ADR-003 cuenta desde el 2026-10-28: F8 no antes del 2026-11-11.
- F7 al publicarse Zensical 0.1 en PyPI (anunciada para el 2026-11-05): runbook en
  `02_PLAN_FASES.md`.
- `ubuntu-latest` migra a Ubuntu 26: si rompe algo, fijar `ubuntu-24.04`.
- Mejora menor anotada en F1: el ZIP versionado incluye el ZIP `latest` de `site/` (2,25 MB frente
  a 1,13 MB).
