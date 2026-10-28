---
status: "ACEPTADO"
date: 2026-10-28
deciders: [Paco Manzano]
consulted: [Documentation Generator, Documentation Reviewer]
informed: [usuarios de /document-project]
---

# Use evidence-backed archetypes for repository documentation

## Contexto y Problema

El objetivo de doc_ia es extraer la **máxima información funcional y técnica** de un
repositorio de código. Los arquetipos 1–11 documentan bien cada módulo, pero un análisis
contra arc42, Diátaxis y prácticas de documentación inversa (2026-10-28) detectó tres huecos:

1. **Sin referencia consultable del sistema**: la configuración, los comandos, los códigos de
   salida y las interfaces publicadas quedaban dispersos entre páginas técnicas por módulo
   (Diátaxis *Reference* sin arquetipo propio).
2. **Sin vista de despliegue**: el material `INFRAESTRUCTURA` se volcaba en el §3 *Runtime* de
   la Variante 6C, que no describe dónde se ejecuta ni se publica cada componente (arc42 §7).
3. **Sin evidencia verificable**: solo el Arquetipo 8 distinguía lo verificado de lo inferido;
   el resto de páginas no indicaba de qué parte del código salía cada afirmación.

Además, la norma y los prompts de los Arquetipos 1 y 2 habían divergido (5 frente a 8
secciones en el 1; "Modelo de Datos / Contratos" frente a "API Reference" con autodoc en el 2).

## Decisión

Se amplía el estándar en tres entregas (P1 → P2 → P3). Esta decisión cubre la **P1**:

- **Arquetipo 12 — Referencia del Sistema** (`docs/reference/`, condicional): configuración,
  CLI, errores y códigos de salida, eventos e interfaces publicadas, una página por sistema.
- **Variante 6C §3 › Despliegue** (condicional) y **escenarios de calidad** en 6C §4.
- **Regla transversal de evidencia** (`DOCUMENTATION_STANDARD.md` §3.16): bloque plegable
  "Evidencia" sin número al final de los Arquetipos 1, 2 y 12; citas `ruta::símbolo` en código
  inline; leyenda ✅ ⚠️ 🔍 ❌ del Arquetipo 8 generalizada.
- **Alineación norma ↔ prompts**: Arquetipo 1 con las 8 secciones del prompt; Arquetipo 2 con
  el §2 "Modelo de Datos / Contratos" de la norma y autodoc solo si hay mkdocstrings.

No se renumera ningún arquetipo ni sección existente.

## Consecuencias

| Tipo | Descripción |
|---|---|
| Ventaja | Cada afirmación documental es auditable contra el código; lo inferido queda marcado |
| Ventaja | Operadores e integradores tienen un único punto de consulta (`docs/reference/`) |
| Ventaja | El material `INFRAESTRUCTURA` tiene un destino propio (6C §3 › Despliegue) |
| Compromiso | El bloque "Evidencia" añade mantenimiento: las citas deben revisarse al cambiar el código |
| Deuda técnica | Las 7 páginas funcionales de doc_ia siguen la estructura v1 (5 secciones) hasta su migración en P2 |
| Deuda técnica | Sin detección automática de citas obsoletas hasta el script de trazabilidad de P3 |
| Riesgo aceptado | Las citas por línea (`ruta:línea`) caducan; se mitiga priorizando `ruta::símbolo` |

## Alternativas Consideradas

| Alternativa | Pros | Contras | Motivo rechazo |
|---|---|---|---|
| Adoptar arc42 completo (12 secciones) en 6C | Estándar reconocido | Muchas secciones vacías en proyectos pequeños; arc42 las declara opcionales | Coste alto sin información adicional proporcional |
| Cinco arquetipos nuevos (Referencia, Modelo de datos, Mapa funcional, Runbook, Seguridad) | Cobertura explícita | Sin casos reales en doc_ia para validar Runbook y Seguridad; más numeración | Simplificado a uno (12); Modelo de datos → Arq. 12 §6 y Mapa funcional → variante del Arq. 1 (P2); Runbook y Seguridad aplazados |
| Citas como enlaces Markdown al código | Navegables | Rompen `mkdocs build --strict` fuera de `docs/`; no existen en el sitio publicado | Incompatible con el build estricto |
| Bajar el prompt del Arquetipo 1 a 5 secciones | Sin migración | Pierde precondiciones, postcondiciones y límites | Contrario al objetivo de máxima información |

## Estado y Revisión

ACEPTADO — 2026-10-28. Sesión: `.ai/sessions/2026-10-28_archetypes_v2/`.

**P2 completada (2026-10-28)**: roles condicionales y columna `Test` en el Arquetipo 1,
Variante 1-I (Mapa Funcional), Arquetipo 2 §6 Verificación y Tests y Arquetipo 12 §6 Datos.
Las 7 páginas funcionales de doc_ia están migradas a la estructura v2; se cierra la deuda
técnica de transición de P1.
Revisar al cerrar P2 (mapa funcional, criterios ligados a tests, modelo de datos) y P3
(frontmatter de trazabilidad y script de drift). Runbook y Seguridad se reabren cuando un
proyecto destino real los requiera.
