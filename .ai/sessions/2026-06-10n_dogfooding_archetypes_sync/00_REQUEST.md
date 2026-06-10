# REQUEST

## Session metadata
- id: 2026-06-10n_dogfooding_archetypes_sync
- fecha: 2026-06-10
- rama: develop
- skill: document_project + new_feature
- fase solicitada: /document-project (dogfooding) + PLAN → AUDIT_PLAN → IMPLEMENT (sync)

## Solicitud original saneada

1. `/document-project` sobre doc_ia (dogfooding) aplicando los arquetipos nuevos (9-11, 3b,
   MADR 4.0, Quick Start) resultantes de la sesión anterior (`2026-06-10m`).
2. Revisión del problema de contenido vacío en páginas Changelog y Contribuir.
3. Automatización de la sincronización CHANGELOG.md / CONTRIBUTING.md → docs/ mediante
   MkDocs hook y PostToolUse de Claude Code. PLAN - AUDIT PLAN (aprobado → IMPLEMENT).

## Objetivo operativo de esta sesión

- Ejecutar `/document-project` completo sobre doc_ia: inventario, PLAN_DOC, generación de
  4 páginas nuevas (Arq. 9, 10, 11, 6D) + actualización de 5 páginas existentes
- Migrar ADR-001 a formato MADR 4.0 (frontmatter YAML + título "Use X for Y")
- Resolver el problema de contenido vacío en docs/changelog.md y docs/contributing.md
- Implementar sincronización automática raíz → docs/ vía `hooks/sync_root_docs.py`

## Restricciones explícitas

- Solo documentación en la primera parte — sin cambios en scripts/ ni tests/
- No romper `python -m mkdocs build --strict`
- La generación ocurre en el chat, nunca via API externa
- La sincronización usa only stdlib (shutil, pathlib) — sin dependencias nuevas

## Resultado esperado

- 4 ficheros creados: CHANGELOG.md, CONTRIBUTING.md, docs/quickstart.md, docs/ai-config/claude.md
- 5 páginas actualizadas: ADR-001, functional/archetypes, api/archetypes, examples/archetypes_usage, index
- hooks/sync_root_docs.py operativo como MkDocs hook y CLI standalone
- Build mkdocs --strict limpio (sin warnings)
- Sesión registrada con trazabilidad completa
