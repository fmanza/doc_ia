# TRACEABILITY

## Session metadata
- id: 2026-11-10c
- fecha: 2026-11-10
- rama: develop
- skill: hotfix
- fase: PLAN + AUDIT_PLAN + IMPLEMENT + AUDIT_CODE + VERSION

## Prompt issued
«Hazlo /hotfix»: corregir `db_trace.py select --name` sin validar.

## Context supplied
- Ver `00_CONTEXT_SNAPSHOT.md`.

## AI output summary
- PLAN: causa raíz verificada en `import_pages`, que construye rutas con tres valores sin
  validar: `--name` (`_fuentes/<name>/`), `--subdir` (`docs/<subdir>/`) y el `path` de cada objeto
  del catálogo. Hallazgo más grave que el informado: con `--subdir ..` o `.`, la retirada de
  páginas obsoletas borra los `.md` de la raíz del destino o de `docs/`.
- AUDIT_PLAN: GO (solo cambia lo que se rechaza; sin cambio de firma).
- IMPLEMENT: `NAME_RE` (igual que en `snapshot_sources`), `_inside` (ruta relativa sin `..`, ni
  absoluta, ni `.`), comprobación de las páginas del catálogo junto a las que ya había, todo antes
  de escribir. 7 tests que fallaban antes del fix, más uno de no regresión para `bd/<base>`;
  24/24 tests del módulo.
- AUDIT_CODE: `--subdir bd/kunivufv` (uso de UFV) sigue siendo válido; las rutas del catálogo
  real (`tables/*.md`) pasan; `tables/../x.md` se normaliza dentro de la sección; `changes` y
  `tracemap` solo leen. Sin regresiones.
- Documentación: regla y AC-17 – AC-19 (19/19), API, referencia, mapa funcional (159/184),
  EDGE_CASES (pendiente resuelto) y CHANGELOG `Fixed`.
- VERSION: `fix:` + `release: v0.11.2`.

## Artefactos generados
| Artefacto | Ruta | Estado |
|---|---|---|
| Fix | `scripts/db_trace.py` | completado |
| Tests | `tests/test_db_trace.py` (8 casos) | completado |

## Directrices para Futuras IAs
- **[rutas]**: en cualquier script que retire ficheros «obsoletos» de una carpeta construida con un parámetro, valida antes que la carpeta no sea `.` ni salga con `..`: el borrado actúa sobre todo lo que encuentra.

## Veredicto final
Veredicto: CLOSED
Pendientes al cierre:
- Subir los tags `v0.11.1` y `v0.11.2` (los sube el usuario o lo autoriza explícitamente).
