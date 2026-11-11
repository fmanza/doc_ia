# TRACEABILITY

## Session metadata
- id: 2026-11-11
- fecha: 2026-11-11
- rama: develop
- skill: hotfix
- fase: PLAN + AUDIT_PLAN + IMPLEMENT + AUDIT_CODE + VERSION

## Prompt issued
`/hotfix doc_ia he encontrado un fallo: doc_trace.py stamp borra el campo ambito cuando sella un
registro de decisiones`.

## Context supplied
- Ver `00_CONTEXT_SNAPSHOT.md`.

## AI output summary
- PLAN: causa raíz verificada. `stamp_page` reescribe el frontmatter entero con `arquetipo`,
  `fuentes`, `decisiones` y `revisado`: (1) pierde cualquier otra clave; (2) sin `fuentes` ni
  `decisiones` previos, `read_page_meta` devuelve `None` y el arquetipo sale vacío.
- AUDIT_PLAN: GO (parámetro opcional; páginas sin otras claves quedan igual).
- IMPLEMENT: `STAMP_KEYS`, `_unmanaged_frontmatter` (líneas literales de las demás claves y
  arquetipo previo) y `format_frontmatter(meta, extra)`. Test que fallaba antes
  (`arquetipo` vacío) y pasa después; 63/63 en `test_doc_trace.py`.
- AUDIT_CODE: inventario de claves en doc_ia y UFV: solo `ambito`, MADR y JSON de `docs/bd/`
  (no se sella); orden conservado; idempotente (no duplica). Sin regresiones.
- Documentación: AC-34 (34/34), API, mapa funcional (160/185), EDGE_CASES, CHANGELOG `Fixed`.
- VERSION: `fix:` + `release: v0.11.3`.

## Artefactos generados
| Artefacto | Ruta | Estado |
|---|---|---|
| Fix | `scripts/doc_trace.py` | completado |
| Test | `tests/test_doc_trace.py::test_stamp_keeps_unmanaged_keys_and_archetype` | completado |

## Directrices para Futuras IAs
- **[doc_trace stamp]**: el frontmatter de trazabilidad convive con claves propias de la página; cualquier reescritura debe conservar lo que no gestiona.

## Veredicto final
Veredicto: CLOSED
Pendientes al cierre:
- Ninguno.
