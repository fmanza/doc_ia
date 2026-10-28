# REQUEST

## Session metadata
- id: 2026-10-28
- fecha: 2026-10-28
- rama: develop
- skill: new_feature
- fase solicitada: PLAN + AUDIT_PLAN (las tres entregas) + IMPLEMENT de la entrega P1

## Solicitud original saneada
Analizar si se pueden o se recomienda actualizar los arquetipos actuales con el objetivo de
obtener la máxima información funcional y técnica sobre el repositorio de código, revisando
buenas prácticas externas. Tras el análisis: emitir PLAN y AUDIT_PLAN con lo propuesto,
guardarlos en una sesión y continuar con IMPLEMENT de la entrega P1.

## Objetivo operativo de esta sesión
- Persistir PLAN (`01_PLAN.md`) y AUDIT_PLAN (`02_AUDIT_PLAN.md`) de las entregas P1/P2/P3.
- Implementar P1: alinear la norma con los prompts reales (Arq. 1 y 2), añadir la regla
  transversal de evidencia y confianza, crear el Arquetipo 12 (Referencia del sistema) y la
  vista de despliegue + escenarios de calidad en la Variante 6C.
- Hacer dogfooding de P1 sobre doc_ia (`docs/reference/`, `docs/architecture.md`) y registrar
  la decisión en un ADR MADR 4.0.

## Restricciones explícitas
- Sin APIs de IA; tooling determinista.
- mypy strict + ruff sin errores en el código que se toque (P1 no toca código Python).
- Numeración de arquetipos y secciones existente preservada (sin renumerar).
- P2 y P3 solo planificados; no se implementan en esta sesión.

## Resultado esperado
- `.ai/sessions/2026-10-28_archetypes_v2/` con REQUEST, CONTEXT_SNAPSHOT, PLAN, AUDIT_PLAN,
  IMPLEMENT y TRACEABILITY.
- Norma, prompts, agentes, entry points y docs de doc_ia actualizados para P1.
- `python -m mkdocs build --strict` en verde.
