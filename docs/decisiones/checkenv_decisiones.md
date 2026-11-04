---
arquetipo: "13"
ambito: CHECKENV
---
# Registro de Decisiones de Cobertura — Verificación de Entorno

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
| ⚠️ | 3 | 0 | 3 |
| ❌ | 0 | 0 | 0 |
| 🔍 | 0 | 0 | 0 |

## 3. Decisiones

### COB-CHECKENV-001 — AC-01 — Mensaje final con todo instalado { #cob-checkenv-001 }

| Campo | Valor |
|---|---|
| Página | [functional/check_env.md](../functional/check_env.md) |
| Estado detectado | ⚠️ |
| Evidencia | `scripts/check_env.py::main`; el test cubre la detección de herramientas, no el mensaje final |
| **Decisión** | Remediar |
| **Contexto aportado** | Test `tests/test_check_env.py::test_main_reports_complete_when_everything_installed`; reveló que con docling instalado el mensaje era «completo (Python).» y se corrigió `scripts/check_env.py::main` (docling pasa a nota informativa ℹ) (propuesta del agente aceptada en el chat) |
| **Responsable** | Paco Manzano |
| **Fecha** | 2026-11-04 |
| **Estado resultante** | ✅ |

### COB-CHECKENV-002 — AC-02 — Código de salida 1 si falta una herramienta { #cob-checkenv-002 }

| Campo | Valor |
|---|---|
| Página | [functional/check_env.md](../functional/check_env.md) |
| Estado detectado | ⚠️ |
| Evidencia | `scripts/check_env.py::main`, `::missing_tools`; el test no comprueba el código 1 |
| **Decisión** | Remediar |
| **Contexto aportado** | Test `tests/test_check_env.py::test_main_exits_1_listing_missing_required` (propuesta del agente aceptada en el chat) |
| **Responsable** | Paco Manzano |
| **Fecha** | 2026-11-04 |
| **Estado resultante** | ✅ |

### COB-CHECKENV-003 — AC-03 — Orden de las herramientas que faltan { #cob-checkenv-003 }

| Campo | Valor |
|---|---|
| Página | [functional/check_env.md](../functional/check_env.md) |
| Estado detectado | ⚠️ |
| Evidencia | `scripts/check_env.py::missing_tools`; el test usa una sola herramienta y no comprueba el orden |
| **Decisión** | Remediar |
| **Contexto aportado** | Test `tests/test_check_env.py::test_missing_tools_preserves_input_order` (propuesta del agente aceptada en el chat) |
| **Responsable** | Paco Manzano |
| **Fecha** | 2026-11-04 |
| **Estado resultante** | ✅ |

### COB-CHECKENV-004 — AC-04 — Aviso de herramientas de sistema { #cob-checkenv-004 }

| Campo | Valor |
|---|---|
| Página | [functional/check_env.md](../functional/check_env.md) |
| Estado detectado | ⚠️ |
| Evidencia | `scripts/check_env.py::main`, `::missing_system_tools`; el test cubre la detección, no el aviso |
| **Decisión** | Remediar |
| **Contexto aportado** | Test `tests/test_check_env.py::test_main_warns_about_pandoc_but_succeeds` (propuesta del agente aceptada en el chat) |
| **Responsable** | Paco Manzano |
| **Fecha** | 2026-11-04 |
| **Estado resultante** | ✅ |

## 4. Historial de revisiones

| Fecha | Revisión | Decisiones aplicadas | Por |
|---|---|---|---|
| 2026-11-04 | Generación inicial | — | Agente |
| 2026-11-04 | Aplicación de decisiones | COB-CHECKENV-001, COB-CHECKENV-002, COB-CHECKENV-003, COB-CHECKENV-004 | Agente |
