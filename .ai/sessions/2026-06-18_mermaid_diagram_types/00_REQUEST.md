# REQUEST

## Session metadata
- id: 2026-06-18_mermaid_diagram_types
- fecha: 2026-06-18
- rama: develop
- skill: refactor
- fase solicitada: PLAN + AUDIT_PLAN + IMPLEMENT

## Solicitud original saneada
Revisar las instrucciones IA y proponer mejoras para la documentacion, para incluir diagramas
Mermaid donde se necesiten. Buscar en https://mermaid.js.org/ los posibles diagramas para
documentacion de desarrollo, y proponer mejoras para la documentacion.
Proponer PLAN - AUDIT PLAN.

## Objetivo operativo de esta sesion
- Evaluar los 28 tipos de diagrama de Mermaid v11 contra las necesidades de documentacion de desarrollo
- Seleccionar los tipos con valor demostrable, clasificados por nivel de prescripcion
- Incorporar los nuevos tipos en los ficheros de instrucciones (prompts, agents, standards)
- Mantener consistencia entre todos los ficheros que referencian tipos de diagrama

## Restricciones explicitas
- Solo modificar ficheros de instrucciones (.github/), no docs/ ni codigo Python
- No incorporar tipos beta de Mermaid (riesgo de rotura entre versiones)
- No forzar diagramas donde no aportan valor (how-tos, changelog, examples)
- Mantener retrocompatibilidad con los 18 diagramas existentes en docs/

## Resultado esperado
- 9 ficheros de instrucciones actualizados con 6 nuevos tipos de diagrama
- Build `mkdocs build --strict` sin errores
- Carpeta .ai/sessions/2026-06-18_mermaid_diagram_types/ con artefactos de trazabilidad
