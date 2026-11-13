# REQUEST

## Session metadata
- id: 2026-11-13
- fecha: 2026-11-13
- rama: develop
- skill: new_feature + refactor (cierre de pendientes de la migración a Zensical)
- fase solicitada: PLAN + AUDIT_PLAN (sin IMPLEMENT)

## Solicitud original saneada
«Probada la búsqueda y todo bien. En doc_ia, sin urgencia: PLAN y AUDIT_PLAN» de los pendientes
de la sesión `2026-11-12_zensical_paridad_f7`:

1. Commits de `develop` posteriores a v0.12.0 (solo documentación) → siguiente release.
2. Retirar la opción obsoleta `--builder` de `build_docs_zip.py` en la siguiente versión menor.
3. Procedimiento para actualizar Zensical (beta) de forma deliberada.
4. Las releases `v0.12.0` y `docs-v0.12.0` publican ZIP de builds distintas con el mismo nombre
   y huellas distintas; solo `docs-v*` adjunta `.sha256`.

Fuera de alcance (lo decide el usuario): orden nombre → tipo de los diagramas ER (se hará en
util_bbdd en otro momento).

## Objetivo operativo de esta sesión
- PLAN por fases con ficheros, commit y verificación.
- AUDIT_PLAN contra el repositorio y los workflows reales.

## Restricciones explícitas
- Solo PLAN y AUDIT_PLAN; sin cambios de código, configuración ni tests.
- Releases: merge, tag y push por separado y con confirmación (memoria del proyecto).

## Resultado esperado
- `01_PLAN_AUDIT.md`, `TRACEABILITY.md` y fila en `INDEX.md`.
