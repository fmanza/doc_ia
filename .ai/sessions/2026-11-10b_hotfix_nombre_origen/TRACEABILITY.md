# TRACEABILITY

## Session metadata
- id: 2026-11-10b
- fecha: 2026-11-10
- rama: develop
- skill: hotfix
- fase: PLAN + AUDIT_PLAN + IMPLEMENT + AUDIT_CODE + VERSION

## Prompt issued
«Tienes mi permiso, antes /hotfix»: corregir `NAME_RE` de `snapshot_sources.py` antes de subir el
tag `v0.11.0`.

## Context supplied
- Ver `00_CONTEXT_SNAPSHOT.md`.

## AI output summary
- PLAN: causa raíz verificada. `NAME_RE` admite `.`/`..`; `replace ..` ejecuta
  `shutil.rmtree(<destino>/_staging/..)` (la raíz del destino), y `sync` copia y borra ficheros
  en ella. Fix: `NAME_RE = ^(?!\.+$)[\w.-]+$` y validar los nombres en `read_manifest`.
- AUDIT_PLAN: GO (solo cambia lo que se rechaza; sin cambio de firma).
- IMPLEMENT: 3 tests que fallaban antes del fix (`add .`/`add ..`, `..` escrito a mano en el
  registro con `replace` y `sync`, la raíz intacta); fix en 2 puntos; 32/32 tests del módulo.
- AUDIT_CODE: sin regresiones (nombres como `.oculto`, `v1.2` o `a..b` siguen siendo válidos; los
  orígenes de UFV también); compatibilidad con los registros existentes. Hallazgo fuera de
  alcance: `db_trace.py select --name ..` escribiría `catalog.json` y `manifest.json` en la raíz
  del destino (sin borrar) → propuesto como hotfix aparte.
- Documentación: regla y AC-18/AC-19 en la página funcional (19/19), página técnica,
  referencia, mapa funcional (156/181), `EDGE_CASES`, CHANGELOG `Fixed`.
- VERSION: `fix:` + `release: v0.11.1`.

## Artefactos generados
| Artefacto | Ruta | Estado |
|---|---|---|
| Fix | `scripts/snapshot_sources.py` | completado |
| Tests | `tests/test_snapshot_sources.py` (3 casos) | completado |

## Directrices para Futuras IAs
- **[nombres de origen]**: todo nombre que forme una ruta (`_staging/<nombre>/`, `_fuentes/<nombre>/`, `docs/assets/manual/<origen>/`) excluye los nombres formados solo por puntos; valídalo también al leer registros editables a mano.

## Veredicto final
Veredicto: CLOSED
Pendientes al cierre:
- Hotfix propuesto: `db_trace.py select --name` sin validar.
