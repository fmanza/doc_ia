---
arquetipo: "13"
ambito: CONVERT
---
# Registro de Decisiones de Cobertura — Conversión de Documentos a Markdown

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
| ⚠️ | 1 | 0 | 1 |
| ❌ | 0 | 0 | 0 |
| 🔍 | 0 | 0 | 0 |

## 3. Decisiones

### COB-CONVERT-001 — AC-02 — Reconversión con `--force` { #cob-convert-001 }

| Campo | Valor |
|---|---|
| Página | [functional/convert_to_md.md](../functional/convert_to_md.md) |
| Estado detectado | ⚠️ |
| Evidencia | `scripts/convert_to_md.py::convert_file`; el test combina `--force` con simulación |
| **Decisión** | Aceptar riesgo |
| **Contexto aportado** | El test con motor simulado es el nivel adecuado; los motores reales (docling, markitdown, pandoc) son dependencias externas (propuesta del agente aceptada en el chat) |
| **Responsable** | Paco Manzano |
| **Fecha** | 2026-11-04 |
| **Estado resultante** | ⚠️ |

### COB-CONVERT-002 — AC-10 — Mensaje con alternativas de motor { #cob-convert-002 }

| Campo | Valor |
|---|---|
| Página | [functional/convert_to_md.md](../functional/convert_to_md.md) |
| Estado detectado | ⚠️ |
| Evidencia | `scripts/convert_to_md.py::convert_file`; el mensaje con alternativas que emite `main` no está cubierto por tests |
| **Decisión** | Remediar |
| **Contexto aportado** | Test `tests/test_convert_to_md.py::test_main_engine_unavailable_suggests_alternatives` (propuesta del agente aceptada en el chat) |
| **Responsable** | Paco Manzano |
| **Fecha** | 2026-11-04 |
| **Estado resultante** | ✅ |

## 4. Historial de revisiones

| Fecha | Revisión | Decisiones aplicadas | Por |
|---|---|---|---|
| 2026-11-04 | Generación inicial | — | Agente |
| 2026-11-04 | Aplicación de decisiones | COB-CONVERT-001, COB-CONVERT-002 | Agente |
