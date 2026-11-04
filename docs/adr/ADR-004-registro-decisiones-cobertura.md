---
status: "ACEPTADO"
date: 2026-11-04
deciders: [Paco Manzano]
consulted: [Documentation Generator, Documentation Reviewer]
informed: [usuarios de /document-project]
---

# Use a human-edited decision register for coverage gaps

## Contexto y Problema

La leyenda de cobertura del Arquetipo 8, generalizada en la regla de evidencia (ADR-002), marca
cada apartado como cubierto ✅, parcial ⚠️, sin módulo ❌ o por verificar 🔍. El agente puede
detectar esos estados en el código, pero no puede resolverlos: un 🔍 suele depender de
configuración en base de datos, de sistemas externos o de documentación organizativa que no
está en el repositorio, y un ⚠️ o un ❌ exigen una decisión de producto o de cumplimiento
(remediar, aceptar el riesgo, compensar fuera del sistema).

Hasta ahora esos apartados acababan en una lista de "pendiente de revisión humana" del RESUMEN,
sin un lugar donde las personas respondieran ni un mecanismo para que la siguiente revisión
aplicara lo decidido. Además, la leyenda tenía dos redacciones distintas: la del §3.8 y la del
§3.16, que daban un significado diferente a ❌.

## Decisión

- **Arquetipo 13 — Registro de Decisiones de Cobertura** (`docs/decisiones/<ámbito>_decisiones.md`,
  `DOCUMENTATION_STANDARD.md` §3.18): condicional y transversal. Es obligatorio con el
  Arquetipo 8 y se adopta con los Arquetipos 1, 2 y 12 si el destino ya lo tiene o el usuario lo
  pide.
- Cada apartado tiene un identificador estable `COB-<ÁMBITO>-<NNN>` y una ficha. El agente
  rellena el estado detectado y la evidencia; las personas rellenan la decisión, el contexto
  aportado, el responsable, la fecha y el estado resultante. El vocabulario de decisiones es
  cerrado y depende del estado.
- En cada revisión, el agente **aplica** primero las decisiones tomadas: enlaza la ficha desde
  cada fila que cita el identificador y deja como último símbolo el estado resultante. Nunca
  escribe en los campos de persona.
- `doc_trace.py decisions` comprueba de forma determinista que registro y documentación
  coinciden. Las fichas pendientes no se tratan como fallo.
- Hay una única **leyenda canónica** en §3.8; §3.16 remite a ella.
- El registro **se publica** con el sitio y el ZIP offline (decisión de la persona usuaria);
  no contiene datos personales, secretos ni URLs internas.

## Consecuencias

| Tipo | Descripción |
|---|---|
| Ventaja | Cada ⚠️ ❌ 🔍 tiene un responsable, una fecha y un contexto auditables |
| Ventaja | La documentación cita la decisión que justifica cada estado, y la CI detecta si la contradice |
| Ventaja | Editar el registro marca como `stale` la página que lo declara en `fuentes:`, de modo que `drift` avisa de que hay decisiones nuevas |
| Compromiso | Las filas de cobertura ganan una columna o un prefijo de identificador y un enlace |
| Compromiso | Un registro publicado expone decisiones de la organización; las confidenciales se citan por la ubicación del acta |
| Deuda técnica | La documentación de doc_ia no adopta el registro: sus ⚠️ y 🔍 actuales siguen sin ficha |
| Riesgo aceptado | Una decisión que mantiene el estado ("Aceptar riesgo" sobre ⚠️) cuenta como reflejada en cuanto la fila enlaza la ficha |

## Alternativas Consideradas

| Alternativa | Pros | Contras | Motivo rechazo |
|---|---|---|---|
| Columnas de decisión dentro de la página del Arquetipo 8 | Un único fichero | Mezcla contenido generado y humano; al regenerar se pisan las decisiones | Riesgo de perder decisiones |
| Registro solo para el Arquetipo 8 | Menor alcance | Los ⚠️ y 🔍 de los Arquetipos 1, 2 y 12 quedan sin cauce de decisión | La persona usuaria eligió el alcance transversal |
| Un ADR por decisión | Formato existente | Decenas de ADR de grano fino; los ADR son para decisiones arquitectónicas | Se mantiene el ADR solo para decisiones arquitectónicas, enlazado desde la ficha |
| Registro fuera de `docs/` | No se publica | No se puede consultar en el sitio ni enlazar desde las páginas | La persona usuaria eligió publicarlo |

## Estado y Revisión

ACEPTADO — 2026-11-04. Sesión: `.ai/sessions/2026-11-04_registro_decisiones/`.
Revisar cuando un proyecto destino real complete un ciclo de generación → decisión → aplicación,
o si la documentación de doc_ia adopta el registro.
Relacionado: [ADR-002](ADR-002-arquetipos-con-evidencia.md) (regla de evidencia y leyenda).
