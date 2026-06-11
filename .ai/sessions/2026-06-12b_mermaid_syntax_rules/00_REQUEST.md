# REQUEST

## Session metadata
- id: 2026-06-12b_mermaid_syntax_rules
- fecha: 2026-06-12
- rama: develop
- skill: hotfix
- fase solicitada: RCA + FIX — parse errors Mermaid en documentación socyalpro

## Solicitud original saneada

Dos errores consecutivos al renderizar diagramas Mermaid en socyalpro:
1. `mermaid.min.js:894 Uncaught (in promise) Error: Parse error on line 14`
2. `mermaid.min.js:894 Uncaught (in promise) Error: Parse error on line 24`

## Objetivo operativo de esta sesión

1. Identificar qué construcción Mermaid causa el error en línea 14 y en línea 24.
2. Corregir los diagramas afectados en socyalpro.
3. Actualizar los agentes para que no generen estas construcciones inválidas.

## Restricciones explícitas

- No crear artefactos de sesión en socyalpro.
- Correcciones mínimas: solo los labels y subgraph afectados.

## Resultado esperado

- 3 ficheros corregidos en socyalpro: `docs/index.md`, `docs/architecture.md`, `docs/api/integrations.md`
- Reglas Mermaid actualizadas en `documentation-generator.agent.md` y `document_project.prompt.md`
