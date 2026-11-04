---
arquetipo: "13"
ambito: BOOTSTRAP
---
# Registro de Decisiones de Cobertura — Bootstrap de Configuración IA

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
| 🔍 | 4 | 4 | 0 |

## 3. Decisiones

### COB-BOOTSTRAP-001 — Flujo «Plataformas IA parciales» { #cob-bootstrap-001 }

| Campo | Valor |
|---|---|
| Página | [functional/bootstrap.md](../functional/bootstrap.md) |
| Estado detectado | 🔍 |
| Evidencia | `.github/prompts/bootstrap_ai_config.prompt.md::Contexto a completar` pide «Plataformas IA activas — marca las que apliquen»; no describe qué se hace con los entry points de las plataformas no marcadas |
| **Decisión** | Pendiente |
| **Contexto aportado** | — |
| **Responsable** | — |
| **Fecha** | — |
| **Estado resultante** | — |

### COB-BOOTSTRAP-002 — Flujo «Fase parcial (solo PLAN + AUDIT_PLAN)» { #cob-bootstrap-002 }

| Campo | Valor |
|---|---|
| Página | [functional/bootstrap.md](../functional/bootstrap.md) |
| Estado detectado | 🔍 |
| Evidencia | `.github/prompts/bootstrap_ai_config.prompt.md::Devuelve en este orden` enumera las fases; la parada tras AUDIT_PLAN solo aparece en el ejemplo de invocación (parámetro `Fase`), no como regla |
| **Decisión** | Pendiente |
| **Contexto aportado** | — |
| **Responsable** | — |
| **Fecha** | — |
| **Estado resultante** | — |

### COB-BOOTSTRAP-003 — AC-02 — Destino con un generador distinto de MkDocs { #cob-bootstrap-003 }

| Campo | Valor |
|---|---|
| Página | [functional/bootstrap.md](../functional/bootstrap.md) |
| Estado detectado | 🔍 |
| Evidencia | `.github/prompts/bootstrap_ai_config.prompt.md::Contexto a completar` pide el generador del destino y la Capa B adapta el builder; no dice explícitamente que la configuración de MkDocs no se copie cuando el generador es otro. Sin test: el bootstrap se ejecuta en el chat |
| **Decisión** | Pendiente |
| **Contexto aportado** | — |
| **Responsable** | — |
| **Fecha** | — |
| **Estado resultante** | — |

### COB-BOOTSTRAP-004 — Capa D excluida aunque el usuario lo pida { #cob-bootstrap-004 }

| Campo | Valor |
|---|---|
| Página | [api/bootstrap.md](../api/bootstrap.md) |
| Estado detectado | 🔍 |
| Evidencia | `.github/prompts/bootstrap_ai_config.prompt.md::Capa D` dice «Excluir explícitamente», sin mencionar qué ocurre si el usuario pide copiar un fichero de esa capa |
| **Decisión** | Pendiente |
| **Contexto aportado** | — |
| **Responsable** | — |
| **Fecha** | — |
| **Estado resultante** | — |

## 4. Historial de revisiones

| Fecha | Revisión | Decisiones aplicadas | Por |
|---|---|---|---|
| 2026-11-04 | Generación inicial | — | Agente |
