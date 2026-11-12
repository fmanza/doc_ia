---
arquetipo: "13"
ambito: BUILDZIP
---
# Registro de Decisiones de Cobertura — ZIP de Documentación Offline

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

### COB-BUILDZIP-001 — Hook ejecutado antes del aborto por `--strict` { #cob-buildzip-001 }

| Campo | Valor |
|---|---|
| Página | [api/build_docs_zip.md](../api/build_docs_zip.md) |
| Estado detectado | ⚠️ |
| Evidencia | Comportamiento de una dependencia externa: `mkdocs.commands.build::build` de MkDocs 1.6.1. Verificado en esa versión; sin test en doc_ia. Desde 2026-11-12 (ADR-003) MkDocs ya no se usa: el post-build lo ejecuta `scripts/build_docs_zip.py::_build` solo tras un build OK (`tests/test_build_docs_zip.py::test_zensical_build_failure_skips_post_build`), así que el caso ya no se da. Pendiente de que las personas decidan si se reclasifica |
| **Decisión** | Aceptar riesgo |
| **Contexto aportado** | Comportamiento de MkDocs 1.6.1, versión fijada en `requirements-docs.txt`; revisar al actualizar MkDocs (propuesta del agente aceptada en el chat) |
| **Responsable** | Paco Manzano |
| **Fecha** | 2026-11-04 |
| **Estado resultante** | ⚠️ |

### COB-BUILDZIP-002 — Zensical no ejecuta `hooks:` de `mkdocs.yml` y no avisa { #cob-buildzip-002 }

| Campo | Valor |
|---|---|
| Página | [functional/build_docs_zip.md](../functional/build_docs_zip.md), [api/build_docs_zip.md](../api/build_docs_zip.md) |
| Estado detectado | ⚠️ |
| Evidencia | Fuente externa: zensical.org/compatibility/configuration (Zensical 0.0.73, en alfa); re-verificado el 2026-11-12 con Zensical 0.1.1 (beta): `hooks:` sigue sin soporte (zensical.org/docs/compatibility/mkdocs/migration/ y build mínimo). Sin test en doc_ia; puede cambiar en versiones posteriores |
| **Decisión** | Aceptar riesgo |
| **Contexto aportado** | Zensical está en alfa (0.0.73); revisar al actualizar Zensical (propuesta del agente aceptada en el chat) |
| **Responsable** | Paco Manzano |
| **Fecha** | 2026-11-04 |
| **Estado resultante** | ⚠️ |

### COB-BUILDZIP-003 — Índice de búsqueda JS de Zensical en `search.js` { #cob-buildzip-003 }

| Campo | Valor |
|---|---|
| Página | [api/build_docs_zip.md](../api/build_docs_zip.md) |
| Estado detectado | ⚠️ |
| Evidencia | Verificado con un build real de Zensical 0.0.73 (sesión 2026-10-29d) y de nuevo con 0.1.1 (sesión 2026-11-12: `search.js` en la raíz); depende de detalles internos de Zensical y no tiene test |
| **Decisión** | Aceptar riesgo |
| **Contexto aportado** | Detalle interno de Zensical 0.0.73 (alfa); revisar al actualizar Zensical (propuesta del agente aceptada en el chat) |
| **Responsable** | Paco Manzano |
| **Fecha** | 2026-11-04 |
| **Estado resultante** | ⚠️ |

### COB-BUILDZIP-004 — Búsqueda por `file://` en Firefox { #cob-buildzip-004 }

| Campo | Valor |
|---|---|
| Página | [functional/build_docs_zip.md](../functional/build_docs_zip.md) |
| Estado detectado | ⚠️ |
| Evidencia | Prueba de humo de la sesión 2026-10-29d: sin ventana, Firefox no abre la búsqueda al enfocar el campo y la prueba la abre con el icono; no se ha comprobado con ventana |
| **Decisión** | Aceptar riesgo |
| **Contexto aportado** | Prueba de humo solo sin ventana; con ventana no se ha probado y no bloquea el uso (propuesta del agente aceptada en el chat) |
| **Responsable** | Paco Manzano |
| **Fecha** | 2026-11-04 |
| **Estado resultante** | ⚠️ |

## 4. Historial de revisiones

| Fecha | Revisión | Decisiones aplicadas | Por |
|---|---|---|---|
| 2026-11-04 | Generación inicial | — | Agente |
| 2026-11-04 | Aplicación de decisiones | COB-BUILDZIP-001, COB-BUILDZIP-002, COB-BUILDZIP-003, COB-BUILDZIP-004 | Agente |
