---
arquetipo: "13"
ambito: ARCHETYPES
---
# Registro de Decisiones de Cobertura — Arquetipos Formales

*Sistema analizado: doc_ia 0.4.1 · Última generación: 2026-11-04*

## 1. Cómo usar este registro

Este documento lo **genera el agente** y lo **completan las personas**. Cada ficha corresponde a
un apartado de la documentación identificado por `COB-<ÁMBITO>-<NNN>`. Rellena los campos en
**negrita** de cada ficha; no edites los demás (los mantiene el agente). En la siguiente revisión,
el agente aplica a la documentación las decisiones que no estén en `Pendiente` y enlaza cada
apartado con su ficha.

**Leyenda de cobertura**:

| Símbolo | Significado |
|---|---|
| ✅ | Cubierto: módulo identificado y comportamiento verificado en el código |
| ⚠️ | Parcial: módulo identificado, pero con un hueco funcional o un defecto conocido |
| ❌ | Gap: no hay módulo que lo implemente |
| 🔍 | A verificar: la evidencia no basta (configuración en base de datos, sistemas externos o documentación organizativa no aportada) |

**Decisiones admitidas** (escribe exactamente una; `Pendiente` mientras no se decida):

| Estado detectado | Decisión | Contexto que debes aportar |
|---|---|---|
| ✅ | Confirmar · Reabrir | Al reabrir: el defecto o hueco observado |
| ⚠️ | Remediar · Aceptar riesgo · Reclasificar | Plan y plazo; o justificación y alcance del riesgo |
| ❌ | Implementar · Medida compensatoria · Aceptar riesgo · No aplica | Dónde se implementará; qué control externo lo cubre; o por qué no aplica |
| 🔍 | Aportar evidencia · Reclasificar · No aplica | La evidencia que faltaba (configuración en BD, sistema externo, documentación organizativa) |

Con una decisión distinta de `Pendiente`, rellena también **Responsable**, **Fecha**
(`AAAA-MM-DD`) y **Estado resultante** (✅ ⚠️ ❌ 🔍 o `No aplica`). «No aplica» va siempre en la
decisión y en el resultado. No escribas datos personales, secretos ni URLs internas: cita dónde
está el acta o la evidencia, no su contenido.

## 2. Resumen

| Estado detectado | Fichas | Pendientes | Decididas |
|---|---|---|---|
| ✅ | 0 | 0 | 0 |
| ⚠️ | 0 | 0 | 0 |
| ❌ | 0 | 0 | 0 |
| 🔍 | 2 | 2 | 0 |

## 3. Decisiones

### COB-ARCHETYPES-001 — AC-01 — Flujo completo de arquetipos sobre un proyecto sin documentación { #cob-archetypes-001 }

| Campo | Valor |
|---|---|
| Página | [functional/archetypes.md](../functional/archetypes.md) |
| Estado detectado | 🔍 |
| Evidencia | `.github/DOCUMENTATION_STANDARD.md::7. Cómo Proceder` (Criterio de Completitud) enumera condiciones de completitud del estándar sobre doc_ia; no describe el resultado de aplicar el flujo a un proyecto nuevo. El test de §7 comprueba la conformidad de doc_ia, no la ejecución del flujo, que ocurre en el chat |
| **Decisión** | Pendiente |
| **Contexto aportado** | — |
| **Responsable** | — |
| **Fecha** | — |
| **Estado resultante** | — |

### COB-ARCHETYPES-002 — Arquetipo 4 sin `.py` en flujos de chat { #cob-archetypes-002 }

| Campo | Valor |
|---|---|
| Página | [api/archetypes.md](../api/archetypes.md) |
| Estado detectado | 🔍 |
| Evidencia | `.github/prompts/example_doc.prompt.md` solo dice «Nunca código inline si el .py existe»; la excepción para flujos de chat (bloques inline sin `.py`) se deduce, no está escrita |
| **Decisión** | Pendiente |
| **Contexto aportado** | — |
| **Responsable** | — |
| **Fecha** | — |
| **Estado resultante** | — |

## 4. Historial de revisiones

| Fecha | Revisión | Decisiones aplicadas | Por |
|---|---|---|---|
| 2026-11-04 | Generación inicial | — | Agente |
