# REQUEST

## Session metadata
- id: 2026-11-10c
- fecha: 2026-11-10
- rama: develop
- skill: hotfix
- fase solicitada: PLAN → AUDIT_PLAN → IMPLEMENT → AUDIT_CODE → VERSION

## Solicitud original saneada
«Hazlo /hotfix»: `db_trace.py select --name` acepta «.», «..» y nombres con «/»; escribe
`catalog.json` y `manifest.json` fuera de `_fuentes/`. Es el pendiente anotado tras el hotfix
2026-11-10b.

## Objetivo operativo de esta sesión
- Que `select` no escriba ni borre nada fuera de `_fuentes/<nombre>/` y `docs/<subdir>/`.

## Restricciones explícitas
- Fix mínimo en `import_pages`; `changes` y `tracemap` (de solo lectura) no se tocan.

## Resultado esperado
Fix + tests de reproducción + documentación; versión PATCH 0.11.2.
