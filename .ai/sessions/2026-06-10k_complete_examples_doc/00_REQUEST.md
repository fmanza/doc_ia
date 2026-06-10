# REQUEST

## Session metadata
- id: 2026-06-10k_complete_examples_doc
- fecha: 2026-06-10
- rama: develop
- skill: document_project (ejecución sobre doc_ia)
- fase solicitada: PLAN + AUDIT_PLAN

## Solicitud original saneada

Actualizar documentación para que no se queden ejemplos sin documentar.

## Objetivo operativo de esta sesión

- Inventariar qué páginas de Arquetipo 4 (Ejemplos) faltan para los Flujos IA
- Inventariar qué páginas de Arquetipo 2 (Técnica/API) faltan para los Flujos IA
- Emitir un PLAN_DOC con acciones CREAR y las páginas exactas a generar
- Emitir un AUDIT_PLAN que valide riesgos, dependencias y cobertura final
- No implementar en esta sesión (solo PLAN + AUDIT_PLAN)

## Restricciones explícitas

- No modificar páginas clasificadas como C (vigentes)
- No inventar comportamiento: basar Arquetipo 2 en los archivos de prompts y agentes reales
- Los Flujos IA no tienen Python → Arquetipo 4 §2 usa inline (patrón `document_project_usage.md`)
- No añadir entradas en mkdocs.yml antes de crear los archivos correspondientes

## Resultado esperado

- `.ai/sessions/2026-06-10k_complete_examples_doc/PLAN.md`
- `.ai/sessions/2026-06-10k_complete_examples_doc/AUDIT_PLAN.md`
