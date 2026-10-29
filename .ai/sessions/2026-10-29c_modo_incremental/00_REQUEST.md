# REQUEST

## Session metadata
- id: 2026-10-29c
- fecha: 2026-10-29
- rama: develop
- skill: new_feature (tooling `doc_trace` + instrucciones IA del producto)
- fase solicitada: PLAN + AUDIT_PLAN («si»); IMPLEMENT («IMPLEMENT») + AUDIT_CODE

## Solicitud original saneada
"¿Cómo se puede relanzar contra destino y que solo mire los cambios?" → propuesta de modo
incremental → "si" (PLAN y AUDIT_PLAN) → "IMPLEMENT".

## Hallazgos de partida
- El inventario ya omite páginas vigentes (estado C), pero relee el origen entero.
- `doc_trace drift` no ve orígenes externos (`outside_repo`) y depende de páginas selladas.
- La sesión no guarda el commit del origen documentado.
- Las evidencias citan `ruta::símbolo` relativo al origen (§3.16 regla 4): base para cruzar
  ficheros cambiados con páginas sin IA.

## Objetivo operativo de esta sesión
- `doc_trace.py baseline` y `changes` (deterministas, git local, sin red).
- Parámetro `Modo` y Fase 1 incremental en prompt, comando, agente y SHARED; `baseline` en CIERRE.
- Tests con repositorios git temporales; docs, AC y trazabilidad al día.

## Restricciones explícitas
- Tooling determinista; sin dependencias nuevas; sin red en tests.
- Sin commit hasta indicación del usuario.

## Decisiones del usuario
- «IMPLEMENT» (2026-10-29): recomendadas. D1 `.ai/doc_state.json` JSON versionado; D2 incremental
  por defecto con baseline; D3 ficheros sin cita siempre listados; D4 cambio de versión
  mayor/menor de doc_ia fuerza modo completo.
