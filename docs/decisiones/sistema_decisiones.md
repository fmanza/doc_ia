---
arquetipo: "13"
ambito: SISTEMA
---
# Registro de Decisiones de Cobertura — Sistema (arquitectura y mapa funcional)

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
| 🔍 | 1 | 0 | 1 |

## 3. Decisiones

### COB-SISTEMA-001 — Escenario de calidad «Trazabilidad de sesiones» { #cob-sistema-001 }

| Campo | Valor |
|---|---|
| Página | [architecture.md](../architecture.md) |
| Estado detectado | ⚠️ |
| Evidencia | Instrucciones de cierre de sesión (`.ai/sessions/TEMPLATE/`, `INDEX.md`); ninguna verificación automática comprueba que exista `TRACEABILITY.md` ni la fila del índice |
| **Decisión** | Remediar |
| **Contexto aportado** | Test `tests/test_docs_conformance.py::test_every_session_has_traceability_and_index_row` (propuesta del agente aceptada en el chat) |
| **Responsable** | Paco Manzano |
| **Fecha** | 2026-11-04 |
| **Estado resultante** | ✅ |

### COB-SISTEMA-002 — Recorrido «bootstrap → documentar» { #cob-sistema-002 }

| Campo | Valor |
|---|---|
| Página | [functional/index.md](../functional/index.md) |
| Estado detectado | 🔍 |
| Evidencia | Se deduce de encadenar `docs/functional/bootstrap.md::§4` (postcondiciones) con `docs/functional/document_project.md::§2` (precondiciones); ninguna instrucción lo describe como recorrido |
| **Decisión** | Aportar evidencia |
| **Contexto aportado** | `.github/prompts/bootstrap_ai_config.prompt.md::Capa A` copia `.github/prompts/*.prompt.md` y `.claude/commands/`, incluido `document_project`: el destino puede documentarse después (propuesta del agente aceptada en el chat) |
| **Responsable** | Paco Manzano |
| **Fecha** | 2026-11-04 |
| **Estado resultante** | ✅ |

## 4. Historial de revisiones

| Fecha | Revisión | Decisiones aplicadas | Por |
|---|---|---|---|
| 2026-11-04 | Generación inicial | — | Agente |
| 2026-11-04 | Aplicación de decisiones | COB-SISTEMA-001, COB-SISTEMA-002 | Agente |
