# REQUEST

## Session metadata
- id: 2026-06-10l_ia_docs_update
- fecha: 2026-06-10
- rama: develop
- skill: document_project (ejecución sobre doc_ia — actualización IA)
- fase solicitada: PLAN + AUDIT_PLAN

## Solicitud original saneada

Actualizar documentación IA para que no se queden ejemplos sin documentar.

## Objetivo operativo de esta sesión

- Detectar páginas IA en estado B por la feature multi-origen (sesión j)
- Detectar páginas IA en estado A aún no creadas
- Emitir PLAN_DOC con acciones ACTUALIZAR (B) y CREAR (A) exactas
- Emitir AUDIT_PLAN que valide riesgos y orden de ejecución
- No implementar en esta sesión (solo PLAN + AUDIT_PLAN)

## Restricciones explícitas

- No modificar páginas C (vigentes)
- Basar los cambios en el código y documentación real; no inventar comportamiento
- Solo actualizar secciones afectadas en páginas B; conservar verbatim las vigentes

## Resultado esperado

- `.ai/sessions/2026-06-10l_ia_docs_update/PLAN.md`
- `.ai/sessions/2026-06-10l_ia_docs_update/AUDIT_PLAN.md`
