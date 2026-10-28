# REQUEST

## Session metadata
- id: 2026-10-28e
- fecha: 2026-10-28
- rama: develop
- skill: new_feature
- fase solicitada: IMPLEMENT completo (M0–M5 + cierre) tras PLAN + AUDIT_PLAN aprobados ("GO entero")

## Solicitud original saneada
1. "Analizar si los gráficos mermaid son los adecuados para la documentación que se genera.
   Puedes comprobar información en internet y en https://mermaid.js.org/. Puedes recomendar
   cambios. Solo información, no se implementa nada."
2. "PLAN y AUDIT_PLAN de lo propuesto, pregunta lo que necesites."
3. "GO entero."

## Decisiones del usuario (AskUserQuestion)
- Alcance: todo, por fases (un commit por fase).
- Fijar/vendorizar Mermaid: dentro de F10 existente (sesión 2026-10-28d), no en esta sesión.
- Validación: test estático + job de CI con mermaid-cli.
- Regla de 12 nodos: mantener y hacerla cumplir con test.

## Objetivo operativo de esta sesión
- Corregir el fallo visible de las entidades HTML (`&#40;` → `&(`) y la regla que lo provoca.
- Fuente única de reglas de diagramas en `DOCUMENTATION_STANDARD.md` §3.17.
- Los diagramas de `docs/` cumplen accesibilidad, ≤12 nodos y una vista por arquetipo, con tests.
- Validación del parser real de Mermaid en CI.

## Restricciones explícitas
- Sin dependencias Python nuevas; tests sin red.
- No inventar flujos: cada diagrama nuevo se deriva de su fuente.
- Fijar la versión de Mermaid queda planificado en F10, no implementado.
- Sin push ni tag (memoria: release-steps-separate).

## Resultado esperado
- Commits M0…M5 + cierre en `develop`, cada uno con DoD verde.
- `TRACEABILITY.md` de la sesión y entrada en `INDEX.md`.
