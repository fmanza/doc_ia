# REQUEST

## Session metadata
- id: 2026-06-10p
- fecha: 2026-06-10
- rama: develop
- skill: hotfix
- fase: PLAN + AUDIT_PLAN → IMPLEMENT

## Solicitud original saneada

El menú lateral de `util` (destino de `/document-project`) no tiene sub-apartados
colapsables/desplegables a diferencia de `doc_ia` (origen). Revisar instrucciones IA,
identificar causa raíz y proponer PLAN + AUDIT_PLAN.

## Objetivo operativo de esta sesión

- Identificar por qué el menú lateral de `util` no colapsa sus secciones
- Ejecutar corrección mínima en los 3 archivos afectados
- Validar build sin warnings

## Restricciones explícitas

- Cambio mínimo: no refactorizar ni añadir funcionalidad
- Validar con `mkdocs build --strict` en util
- No tocar código fuente de util

## Resultado esperado

- [x] `util/mkdocs.yml`: `navigation.sections` eliminado
- [x] `TEMPLATE_mkdocs.yml`: línea comentada con aviso de incompatibilidad
- [x] `document-project.md`: tabla de compatibilidad de `theme.features` añadida
- [x] Build util: 0 warnings
- [x] Sesión trazable en `.ai/sessions/2026-06-10p_*/`
