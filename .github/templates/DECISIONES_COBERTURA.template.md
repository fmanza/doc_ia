---
arquetipo: "13"
ambito: <ÁMBITO>
---
# Registro de Decisiones de Cobertura — <Ámbito>

*Sistema analizado: <nombre> <versión> · Última generación: <AAAA-MM-DD>*

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
| 🔍 | 0 | 0 | 0 |

## 3. Decisiones

### COB-<ÁMBITO>-001 — <apartado> { #cob-<ámbito>-001 }

| Campo | Valor |
|---|---|
| Página | [<página>](../<carpeta>/<página>.md) |
| Estado detectado | 🔍 |
| Evidencia | `<ruta>::<símbolo>` — <qué falta para verificar> |
| **Decisión** | Pendiente |
| **Contexto aportado** | — |
| **Responsable** | — |
| **Fecha** | — |
| **Estado resultante** | — |

## 4. Historial de revisiones

| Fecha | Revisión | Decisiones aplicadas | Por |
|---|---|---|---|
| <AAAA-MM-DD> | Generación inicial | — | Agente |
