# REQUEST

## Session metadata
- id: 2026-06-11d_zip_offline_detection
- fecha: 2026-06-11
- rama: develop
- skill: new_feature
- fase solicitada: PLAN + AUDIT_PLAN + IMPLEMENT

## Solicitud original saneada

El fichero de versión y el Checksum en el proyecto `util_bbdd` se autogeneran en local.
Las instrucciones IA de `doc_ia` no tienen en cuenta este patrón y se quiere que lo hagan.
Solicitud: PLAN + AUDIT_PLAN primero; IMPLEMENT tras confirmación.

## Objetivo operativo de esta sesión

- Detectar el gap: `document_project.prompt.md` no reconoce el patrón `build_docs_zip.py` / `downloads.md` en proyectos origen externos.
- Diseñar y auditar el plan de cambios antes de implementar.
- Implementar los cambios aprobados en los tres ficheros afectados.
- Mantener DRY: la regla canónica en `SHARED_INSTRUCTIONS.md`; los entry points solo referencian.

## Restricciones explícitas

- No modificar ningún archivo de `util_bbdd` (gap solo en `doc_ia`).
- No modificar `bootstrap_ai_config.prompt.md` (ya cubre el patrón en Capa B correctamente).
- No añadir tests (comportamiento es de tooling en el proyecto origen, no en `doc_ia`).

## Resultado esperado

- `document_project.prompt.md`: Fase 1 con detección de señales ZIP + nueva Fase 7b condicional + paso 8b en "Devuelve".
- `SHARED_INSTRUCTIONS.md`: sección "Artefactos generados" ampliada con el patrón generalizable.
- `CLAUDE.md`: sección "Actualizar tabla Descarga Actual" convertida a referencia DRY.
- Artefacto de sesión creado en `.ai/sessions/2026-06-11d_zip_offline_detection/`.
