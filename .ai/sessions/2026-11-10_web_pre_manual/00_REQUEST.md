# REQUEST

## Session metadata
- id: 2026-11-10
- fecha: 2026-11-10
- rama: develop
- skill: new_feature
- fase solicitada: PLAN + AUDIT_PLAN (solo análisis; sin IMPLEMENT)

## Solicitud original saneada
Analizar la posibilidad de incluir la versión desplegada en WEB en el entorno de PRE como origen
opcional, para realizar un documento tipo manual de su funcionamiento y de los requisitos que se
tienen que tener en cuenta. Solo análisis y PLAN; no se implementa nada. Después: AUDIT_PLAN,
preguntando lo necesario, y guardar PLAN y AUDIT_PLAN como sesión.

## Objetivo operativo de esta sesión
- Analizar el encaje de un origen «WEB desplegada en PRE» en el flujo `/document-project`.
- Emitir PLAN con requisitos (acceso, seguridad, datos personales, versión, calidad del manual).
- Auditar el PLAN contra el repositorio real (AUDIT_PLAN) y cerrar las decisiones con el usuario.
- Dejar la sesión trazable para arrancar `/new-feature` sin repetir el análisis.

## Restricciones explícitas
- Solo análisis y plan: no se modifica código, prompts, estándar ni tests.
- La URL de PRE la declara el usuario y **no se versiona**: solo se registra el entorno.
- Principios innegociables: los scripts no acceden a la red ni invocan servicios IA.

## Resultado esperado
Carpeta `.ai/sessions/2026-11-10_web_pre_manual/` con `00_REQUEST.md`,
`00_CONTEXT_SNAPSHOT.md`, `01_PLAN.md`, `02_AUDIT_PLAN.md`, `TRACEABILITY.md` y fila en
`INDEX.md`.
