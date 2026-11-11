# REQUEST

## Session metadata
- id: 2026-11-11
- fecha: 2026-11-11
- rama: develop
- skill: hotfix
- fase solicitada: PLAN → AUDIT_PLAN → IMPLEMENT → AUDIT_CODE → VERSION

## Solicitud original saneada
`/hotfix`: `doc_trace.py stamp` borra el campo `ambito` cuando sella un registro de decisiones
(detectado en la sesión UFV 2026-11-11 con `docs/decisiones/web_decisiones.md`).

## Objetivo operativo de esta sesión
- Que `stamp` conserve las claves del frontmatter que no gestiona y el arquetipo.

## Restricciones explícitas
- Fix mínimo en `stamp_page` / `format_frontmatter`; sin refactor.

## Resultado esperado
Fix + test de reproducción + documentación; versión PATCH 0.11.3.
