# TRACEABILITY

## Session metadata
- id: 2026-06-10n_dogfooding_archetypes_sync
- fecha: 2026-06-10
- rama: develop
- skill: document_project + new_feature
- fase: INVENTARIO → PLAN_DOC → GENERACIÓN → SYNC NAV → BUILD + PLAN → AUDIT_PLAN → IMPLEMENT

## Prompt issued

```
/document-project
Origen:    C:\Desarrollo\python\libs\doc_ia
Destino:   C:\Desarrollo\python\libs\doc_ia\docs
Generador: mkdocs-material
Idioma:    es
Flags:     --verify-build
```

Seguido de:
```
La actualización que suguieres debe ser realizada por este proyecto de forma automática.
PLAN - AUDIT PLAN
```

## Context supplied

- Código fuente de la sesión anterior (`2026-06-10m`) con 11 arquetipos en DOCUMENTATION_STANDARD.md
- Estado del repo: docs/ con 24 páginas, mkdocs.yml, scripts/, tests/
- Commits recientes indicando la adición de arquetipos 3b, 9-11 (commit `93f22e2`)

## AI output summary

- Validó inputs de `/document-project` (4 parámetros ✅)
- Clasificó origen como CÓDIGO único; omitió Fase 0a
- Ejecutó inventario: 4 páginas Estado A (crear) + 5 Estado B (actualizar) + 19 Estado C (omitir)
- **CREAR (A)**:
  - `CHANGELOG.md` (Arquetipo 9, Keep a Changelog 0.1.0)
  - `CONTRIBUTING.md` (Arquetipo 11, 6 secciones)
  - `docs/quickstart.md` (Arquetipo 6 Variante D)
  - `docs/ai-config/claude.md` (Arquetipo 10, 7 secciones)
  - `docs/changelog.md` y `docs/contributing.md` (wrappers MkDocs)
- **ACTUALIZAR (B)**:
  - `docs/adr/ADR-001-…`: migrado a MADR 4.0 (frontmatter YAML + título "Use X for Y")
  - `docs/functional/archetypes.md`: §1 + §3 + §4 — arquetipos 3b, 9, 10, 11 añadidos
  - `docs/api/archetypes.md`: §1 diagrama Mermaid + §2 tabla — 11 arquetipos
  - `docs/examples/archetypes_usage.md`: §2 — invocaciones para 3b, 9, 10, 11
  - `docs/index.md`: §2 "11 arquetipos"; §4 mapa actualizado
- SYNC NAV: añadidas entradas Quick Start, Configuración IA > Claude Code, Changelog, Contribuir
- Detectó problema: `--8<-- "CHANGELOG.md"` (snippets) no funciona dentro de MkDocs con base_path `.` → resuelto escribiendo contenido directamente en wrappers
- Build `python -m mkdocs build --strict` ✅ (sin errores)
- **PLAN** (sync automático): diseñó `hooks/sync_root_docs.py` (MkDocs on_pre_build + CLI)
- **AUDIT_PLAN**: verificó ROOT resolution, exit code 0, `_LINK_FIXES`, mypy exclusion
- **IMPLEMENT**:
  - Creó `hooks/sync_root_docs.py` con `_LINK_FIXES` para reescribir enlace CHANGELOG.md→changelog.md en copia de contributing.md
  - Añadió `hooks:` en mkdocs.yml
  - Añadió `"hooks"` al src de ruff en pyproject.toml
  - Actualizó `.claude/settings.json`: nuevo comando PostToolUse + ruff ampliado
- Build final ✅ — hook ejecutado, sin warnings

## Artefactos generados

| Artefacto | Ruta | Estado |
|---|---|---|
| Changelog v0.1.0 | `CHANGELOG.md` | creado |
| Guía de contribución | `CONTRIBUTING.md` | creado |
| Quick Start | `docs/quickstart.md` | creado |
| Config Agente IA — Claude | `docs/ai-config/claude.md` | creado |
| Wrappers MkDocs | `docs/changelog.md`, `docs/contributing.md` | creados |
| ADR-001 MADR 4.0 | `docs/adr/ADR-001-…` | actualizado |
| Arquetipos Funcional | `docs/functional/archetypes.md` | actualizado |
| Arquetipos API | `docs/api/archetypes.md` | actualizado |
| Arquetipos Ejemplos | `docs/examples/archetypes_usage.md` | actualizado |
| Índice del sitio | `docs/index.md` | actualizado |
| MkDocs nav | `mkdocs.yml` | actualizado |
| Hook sync | `hooks/sync_root_docs.py` | creado |
| Config ruff | `pyproject.toml` | actualizado |
| PostToolUse hooks | `.claude/settings.json` | actualizado |
| Sesión | `.ai/sessions/2026-06-10n_…/` | creada |

## Directrices para Futuras IAs

- **[snippets MkDocs]**: `--8<-- "file"` con `base_path: [.]` no resuelve ficheros fuera de `docs_dir` dentro del proceso de build de MkDocs, aunque funcione en Python standalone. Solución: escribir contenido directamente en docs/ o usar el `on_pre_build` hook para copiar antes del build.
- **[hooks/ y mypy]**: el directorio `hooks/` contiene código con firmas MkDocs (`on_pre_build(config: Any)`). NO añadir `hooks/` a `mypy.files` — las anotaciones MkDocs son incompatibles con mypy strict sin stubs. Sí añadir a ruff src.
- **[LINK_FIXES]**: `hooks/sync_root_docs.py` aplica `_LINK_FIXES` post-copia para corregir `(CHANGELOG.md)` → `(changelog.md)` en la copia docs/contributing.md. Si se añaden nuevos ficheros a PAIRS con enlaces que difieren entre raíz y docs/, extender `_LINK_FIXES`.
- **[docs/changelog.md vs CHANGELOG.md]**: los dos ficheros son la misma fuente de verdad; `hooks/sync_root_docs.py` los mantiene sincronizados. Al actualizar `CHANGELOG.md` (raíz), no actualizar `docs/changelog.md` manualmente — el hook lo sobreescribe en el siguiente Edit/Write o build.

## Veredicto final

Veredicto: **GO**
Pendientes al cierre:
- Subir rama `develop` a GitHub (pendiente de commit + push)
