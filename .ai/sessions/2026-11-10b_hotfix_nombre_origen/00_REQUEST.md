# REQUEST

## Session metadata
- id: 2026-11-10b
- fecha: 2026-11-10
- rama: develop
- skill: hotfix
- fase solicitada: PLAN → AUDIT_PLAN → IMPLEMENT → AUDIT_CODE → VERSION

## Solicitud original saneada
`/hotfix`: `snapshot_sources.py` acepta «.» y «..» como nombre de origen (`NAME_RE = ^[\w.-]+$`).
Es el mismo fallo que el C1 del AUDIT_CODE de `web_captures.py` (sesión 2026-11-10). Hacerlo
antes de subir el tag `v0.11.0`.

## Objetivo operativo de esta sesión
- Impedir que un nombre de origen saque `_staging/<nombre>/` de la zona de trabajo.
- Test que reproduzca el borrado de la raíz del destino.

## Restricciones explícitas
- Fix mínimo: sin refactor ni cambios en otros scripts.

## Resultado esperado
Fix + tests + documentación de la regla; versión PATCH 0.11.1.
