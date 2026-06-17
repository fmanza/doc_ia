# TRACEABILITY

## Session metadata
- id: 2026-06-18_mermaid_diagram_types
- fecha: 2026-06-18
- rama: develop
- skill: refactor
- fase: PLAN + AUDIT_PLAN + IMPLEMENT

## Prompt issued
Revisar las instrucciones IA y proponer mejoras para la documentacion, para incluir diagramas
Mermaid donde se necesiten. Buscar en https://mermaid.js.org/ los posibles diagramas para
documentacion de desarrollo, y proponer mejoras para la documentacion.
Proponer PLAN - AUDIT PLAN.

## Context supplied
- Catalogo completo de 28 tipos de diagrama Mermaid v11 (mermaid.js.org)
- Sintaxis detallada de architecture, kanban, timeline, stateDiagram, gitgraph
- 14 ficheros de instrucciones del proyecto (CLAUDE.md, SHARED_INSTRUCTIONS, DOCUMENTATION_STANDARD, docs.instructions, 6 prompts, 1 agent, 1 review)
- Inventario de 18 diagramas existentes en docs/ (14 archivos)

## AI output summary
- Investigacion: fetch de 5 paginas de mermaid.js.org para catalogo y sintaxis detallada
- Exploracion: agente Explore mapeo los 14 archivos con diagramas y los 18 sin ellos
- PLAN: evaluacion de 28 tipos, seleccion de 6 (3 RECOMENDADO + 3 OPCIONAL), descarte de 18 (beta/bajo valor)
- AUDIT_PLAN: 5 riesgos identificados con mitigacion, 5 verificaciones post-implementacion
- IMPLEMENT: 9 ficheros modificados con adiciones (93 lineas anadidas, 13 eliminadas)
- Verificacion: `mkdocs build --strict` pasa sin errores, consistencia verificada con grep

## Artefactos generados

| Artefacto | Ruta | Estado |
|---|---|---|
| PLAN + AUDIT_PLAN | C:\Users\manza\.claude\plans\dapper-meandering-pond.md | emitido + aprobado |
| docs.instructions.md | .github/instructions/docs.instructions.md | completado |
| DOCUMENTATION_STANDARD.md | .github/DOCUMENTATION_STANDARD.md | completado |
| technical_doc.prompt.md | .github/prompts/technical_doc.prompt.md | completado |
| functional_doc.prompt.md | .github/prompts/functional_doc.prompt.md | completado |
| onboarding_dev.prompt.md | .github/prompts/onboarding_dev.prompt.md | completado |
| contributing_doc.prompt.md | .github/prompts/contributing_doc.prompt.md | completado |
| landing_doc.prompt.md | .github/prompts/landing_doc.prompt.md | completado |
| documentation-generator.agent.md | .github/agents/documentation-generator.agent.md | completado |
| documentation_review.prompt.md | .github/prompts/documentation_review.prompt.md | completado |

## Directrices para Futuras IAs
- **[Mermaid tipos estables]**: En Mermaid v11 los tipos estables son: flowchart, sequence, class, state, ER, user journey, gantt, pie, quadrant, requirement, gitgraph, C4, mindmap, timeline, zenUML. Los demas (kanban, sankey, radar, venn, ishikawa, wardley, treemap, treeview, packet, block, event modeling, architecture) estan en beta y pueden romper entre versiones.
- **[stateDiagram vs flowchart]**: La distincion clave es: `stateDiagram-v2` modela en que estado esta la entidad (ciclo de vida); `flowchart TD` modela que pasos ejecuta el proceso (pipeline/decision). No son intercambiables.
- **[gitgraph render]**: `gitgraph` renderiza en MkDocs Material y GitHub, pero NO en VS Code preview. Igual que `architecture-beta`.
- **[Diagramas en arquetipos]**: Solo Arquetipos 1 (Funcional) y 2 (Tecnica) tienen diagramas OBLIGATORIOS. Arquetipos 7 y 11 tienen RECOMENDADO (gitgraph). El resto de arquetipos no requieren diagramas por diseno.
- **[docs.instructions.md es canonico]**: Las reglas detalladas de cada tipo de diagrama Mermaid viven solo en `docs.instructions.md`. Los prompts y agents referencian esa seccion (DRY).

## Veredicto final
Veredicto: GO
Pendientes al cierre:
- Actualizar la documentacion generada en docs/ para usar los nuevos tipos donde aplique (tarea separada)
