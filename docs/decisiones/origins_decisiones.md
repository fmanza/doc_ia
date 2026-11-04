---
arquetipo: "13"
ambito: ORIGINS
---
# Registro de Decisiones de Cobertura — Catálogo de Tipos de Origen

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
| 🔍 | 4 | 1 | 3 |

## 3. Decisiones

### COB-ORIGINS-001 — Mapeo MATERIAL → arquetipos (numeración v2 del Arquetipo 1) { #cob-origins-001 }

| Campo | Valor |
|---|---|
| Página | [functional/origin_types.md](../functional/origin_types.md) |
| Estado detectado | ⚠️ |
| Evidencia | `.github/DOCUMENTATION_STANDARD.md::3.10`. A 2026-11-04, la fila `ESPECIFICACIÓN` de §3.10 ya usa la numeración v2 (§3, §5, §6, §7); la marca puede estar desfasada |
| **Decisión** | Reclasificar |
| **Contexto aportado** | Comprobado: la tabla de la página y la de §3.10 coinciden fila a fila con la numeración v2 del Arquetipo 1 (propuesta del agente aceptada en el chat) |
| **Responsable** | Paco Manzano |
| **Fecha** | 2026-11-04 |
| **Estado resultante** | ✅ |

### COB-ORIGINS-002 — Regla «`INFRAESTRUCTURA` sin inventario de código» { #cob-origins-002 }

| Campo | Valor |
|---|---|
| Página | [functional/origin_types.md](../functional/origin_types.md) |
| Estado detectado | 🔍 |
| Evidencia | `.github/DOCUMENTATION_STANDARD.md::3.10` (fila `INFRAESTRUCTURA`) indica qué secciones enriquece (Arq. 2 §4, Arq. 6C §3 › Despliegue); no dice explícitamente que no se inventaríe como código |
| **Decisión** | Aportar evidencia |
| **Contexto aportado** | Consecuencia de la regla «MATERIAL no genera páginas propias» (✅, §3.10): la infraestructura solo enriquece Arq. 2 §4 y Arq. 6C §3 › Despliegue (propuesta del agente aceptada en el chat) |
| **Responsable** | Paco Manzano |
| **Fecha** | 2026-11-04 |
| **Estado resultante** | ✅ |

### COB-ORIGINS-003 — AC-04 — `.py` + `openapi.yaml` del mismo proyecto { #cob-origins-003 }

| Campo | Valor |
|---|---|
| Página | [functional/origin_types.md](../functional/origin_types.md) |
| Estado detectado | 🔍 |
| Evidencia | `.github/prompts/document_project.prompt.md::Fase 0a`; la clasificación ocurre en el chat y no tiene test |
| **Decisión** | Aportar evidencia |
| **Contexto aportado** | Regla explícita en `.github/prompts/document_project.prompt.md::Fase 0a`: `.yaml` con clave `openapi:` del propio proyecto → `CONTRATO`; `.py` → `CÓDIGO`. Sin test posible: la clasificación ocurre en el chat (propuesta del agente aceptada en el chat) |
| **Responsable** | Paco Manzano |
| **Fecha** | 2026-11-04 |
| **Estado resultante** | ✅ |

### COB-ORIGINS-004 — AC-09 — PRD sin implementar como `ESPECIFICACIÓN` { #cob-origins-004 }

| Campo | Valor |
|---|---|
| Página | [functional/origin_types.md](../functional/origin_types.md) |
| Estado detectado | 🔍 |
| Evidencia | `.github/DOCUMENTATION_STANDARD.md::3.10` define `ESPECIFICACIÓN` como requisitos; la distinción frente a `MANUAL` por ser pre-implementación se deduce. Sin test |
| **Decisión** | Reclasificar |
| **Contexto aportado** | Hueco conocido: la Fase 0a clasifica por nombre o carpeta y no recoge el criterio «intención pre-implementación → `ESPECIFICACIÓN`»; un PRD llamado `manual_*.pdf` acabaría como `MANUAL`. Remediar en una sesión aparte (propuesta del agente aceptada en el chat) |
| **Responsable** | Paco Manzano |
| **Fecha** | 2026-11-04 |
| **Estado resultante** | ⚠️ |

### COB-ORIGINS-005 — Flujo «Corrección del usuario» { #cob-origins-005 }

| Campo | Valor |
|---|---|
| Página | [functional/origin_types.md](../functional/origin_types.md) |
| Estado detectado | 🔍 |
| Evidencia | `.github/DOCUMENTATION_STANDARD.md::3.10` (Regla) y `.github/prompts/document_project.prompt.md` (parámetro «Tipo de cada origen») exigen que el usuario confirme el tipo antes del INVENTARIO; que, si lo corrige, se use el tipo que indique se deduce de «confirma», no está escrito |
| **Decisión** | Pendiente |
| **Contexto aportado** | — |
| **Responsable** | — |
| **Fecha** | — |
| **Estado resultante** | — |

## 4. Historial de revisiones

| Fecha | Revisión | Decisiones aplicadas | Por |
|---|---|---|---|
| 2026-11-04 | Generación inicial | — | Agente |
| 2026-11-04 | Aplicación de decisiones | COB-ORIGINS-001 ⚠️ → ✅, COB-ORIGINS-002 🔍 → ✅, COB-ORIGINS-003 🔍 → ✅, COB-ORIGINS-004 🔍 → ⚠️ en `functional/origin_types.md` | Agente |
| 2026-11-04 | Ficha nueva y remediación | COB-ORIGINS-005 creada (🔍 del cuerpo sin fila); criterio «requisitos frente a manual» añadido a §3.10 y a la Fase 0a para COB-ORIGINS-004 (la ficha conserva su estado hasta que la persona responsable lo actualice) | Agente |
