---
arquetipo: "13"
ambito: DOCPROJ
---
# Registro de Decisiones de Cobertura — Documentar un Proyecto

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
| ⚠️ | 4 | 4 | 0 |
| ❌ | 0 | 0 | 0 |
| 🔍 | 1 | 1 | 0 |

## 3. Decisiones

### COB-DOCPROJ-001 — Regla «Sincronización visual obligatoria (Fase 0b)» { #cob-docproj-001 }

| Campo | Valor |
|---|---|
| Página | [functional/document_project.md](../functional/document_project.md) |
| Estado detectado | ⚠️ |
| Evidencia | La regla está en `.claude/commands/document-project.md` y en `.github/prompts/document_project.prompt.md::Fase 0b`, y su fila de Evidencia la marca ✅; el cuerpo la marca ⚠️ sin indicar qué parte no está verificada |
| **Decisión** | Pendiente |
| **Contexto aportado** | — |
| **Responsable** | — |
| **Fecha** | — |
| **Estado resultante** | — |

### COB-DOCPROJ-002 — Regla «Instrucciones de visualización siempre» y AC-11 { #cob-docproj-002 }

| Campo | Valor |
|---|---|
| Página | [functional/document_project.md](../functional/document_project.md) |
| Estado detectado | ⚠️ |
| Evidencia | `.github/prompts/document_project.prompt.md::Fase 7c` y `tests/test_docs_conformance.py::test_view_instructions_rule_everywhere`: el test comprueba la coherencia de las instrucciones; el resultado solo se comprueba sobre doc_ia |
| **Decisión** | Pendiente |
| **Contexto aportado** | — |
| **Responsable** | — |
| **Fecha** | — |
| **Estado resultante** | — |

### COB-DOCPROJ-003 — Regla «Relanzar solo sobre lo cambiado» y AC-12 { #cob-docproj-003 }

| Campo | Valor |
|---|---|
| Página | [functional/document_project.md](../functional/document_project.md) |
| Estado detectado | ⚠️ |
| Evidencia | `scripts/doc_trace.py::check_changes` tiene tests; `tests/test_docs_conformance.py::test_incremental_mode_rule_everywhere` comprueba la coherencia de las instrucciones. El flujo incremental completo no tiene test |
| **Decisión** | Pendiente |
| **Contexto aportado** | — |
| **Responsable** | — |
| **Fecha** | — |
| **Estado resultante** | — |

### COB-DOCPROJ-004 — Regla «Fuentes convertidas en `_fuentes/`», AC-09 y AC-10 { #cob-docproj-004 }

| Campo | Valor |
|---|---|
| Página | [functional/document_project.md](../functional/document_project.md) |
| Estado detectado | ⚠️ |
| Evidencia | `tests/test_docs_conformance.py::test_sources_folder_is_canonical` comprueba la coherencia de las instrucciones, no el resultado en un destino |
| **Decisión** | Pendiente |
| **Contexto aportado** | — |
| **Responsable** | — |
| **Fecha** | — |
| **Estado resultante** | — |

### COB-DOCPROJ-005 — AC-01 — Documentar un proyecto sin documentación previa { #cob-docproj-005 }

| Campo | Valor |
|---|---|
| Página | [functional/document_project.md](../functional/document_project.md) |
| Estado detectado | 🔍 |
| Evidencia | `.github/prompts/document_project.prompt.md::Devuelve en este orden` describe la salida; el resultado de punta a punta no tiene test porque el flujo se ejecuta en el chat |
| **Decisión** | Pendiente |
| **Contexto aportado** | — |
| **Responsable** | — |
| **Fecha** | — |
| **Estado resultante** | — |

## 4. Historial de revisiones

| Fecha | Revisión | Decisiones aplicadas | Por |
|---|---|---|---|
| 2026-11-04 | Generación inicial | — | Agente |
