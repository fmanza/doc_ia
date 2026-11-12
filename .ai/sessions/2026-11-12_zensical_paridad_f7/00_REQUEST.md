# REQUEST

## Session metadata
- id: 2026-11-12
- fecha: 2026-11-12
- rama: develop
- skill: new_feature (fix + build(deps))
- fase solicitada: PLAN + AUDIT_PLAN (sin IMPLEMENT)

## Solicitud original saneada
1. Revisar la situación de lo pendiente de la migración a Zensical (F7: subir a 0.1; F8: generador
   por defecto tras ≥ 2 semanas de paridad en verde y revisión visual; F9, F10 y F12 tras F8) y
   decir si falta algo más.
2. «PLAN y AUDIT_PLAN».

## Objetivo operativo de esta sesión
- Diagnosticar por qué la paridad Zensical falla en CI desde el 2026-11-04 (oculto: el paso no es
  bloqueante y los runs salen `success`).
- Planificar el arreglo y F7 (Zensical 0.1.1) con un spike que no toque el repo.
- Auditar el plan y fijar desde cuándo cuenta C2 para F8.

## Restricciones explícitas
- Solo PLAN y AUDIT_PLAN: no se modifica código, configuración, prompts ni tests.
- Spike en el scratchpad (venv aparte y `git worktree` temporales, ya eliminados).

## Resultado esperado
- `01_PLAN_AUDIT.md` con causa raíz, fases, hallazgos de auditoría y veredicto.
- `TRACEABILITY.md` y fila en `INDEX.md`.
