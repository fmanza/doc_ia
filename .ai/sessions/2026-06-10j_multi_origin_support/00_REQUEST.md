# REQUEST

## Session metadata
- id: 2026-06-10j_multi_origin_support
- fecha: 2026-06-10
- rama: develop
- skill: new_feature (extensión de /document-project)
- fase solicitada: PLAN + AUDIT_PLAN + IMPLEMENT

## Solicitud original saneada

Revisar `.claude/commands/document-project.md` y proponer mejoras para:
- Detectar si múltiples orígenes son proyectos de código o documentación de entrada (normativa, pantallas, especificaciones, etc.)
- Determinar la mejor estrategia de documentación para cada tipo de origen
- Actualizar la documentación IA para reflejar los nuevos requisitos

## Objetivo operativo de esta sesión

- Diseñar el concepto de tipos de origen (CÓDIGO / NORMATIVA / ESPECIFICACIÓN / UI/PANTALLAS / REFERENCIA)
- Añadir Fase 0a (Clasificación de orígenes) al flujo de `/document-project`
- Definir estrategias para múltiples orígenes CÓDIGO (federado / hub+satélite / monorepo)
- Sincronizar los cambios en los 4 ficheros afectados: comando, prompt, agente y estándar

## Restricciones explícitas

- No modificar los arquetipos existentes (1-8): solo añadir la capa de clasificación
- No alterar el comportamiento para origen único de tipo CÓDIGO (caso más frecuente)
- La clasificación siempre propone y el usuario confirma: nunca autodetectar sin confirmación
- La estrategia multi-CÓDIGO nunca se autodetecta: siempre preguntar al usuario

## Resultado esperado

- `.claude/commands/document-project.md` con campo `Tipo de cada origen`, campo `Estrategia` y sección CLASIFICACIÓN DE ORÍGENES en el flujo Devuelve
- `.github/prompts/document_project.prompt.md` sincronizado con Fase 0a
- `.github/agents/documentation-generator.agent.md` con Paso 0a completo (señales, mapeo, protocolo)
- `.github/DOCUMENTATION_STANDARD.md` con §3.10 "Documentación con Múltiples Orígenes"
