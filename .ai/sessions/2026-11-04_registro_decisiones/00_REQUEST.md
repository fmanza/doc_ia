# REQUEST

## Session metadata
- id: 2026-11-04
- fecha: 2026-11-04
- rama: develop
- skill: new_feature
- fase solicitada: PLAN + AUDIT_PLAN → IMPLEMENT (opciones elegidas: C + D)

## Solicitud original saneada
Leyenda de cobertura:
- ✅ Cubierto: módulo identificado y comportamiento verificado en el código
- ⚠️ Parcial: módulo identificado, pero con un hueco funcional o un defecto conocido
- ❌ Gap: no hay módulo que lo implemente
- 🔍 A verificar: la evidencia no basta (configuración en base de datos, sistemas externos o
  documentación organizativa no aportada)

Actualizar las instrucciones para que:
- se genere un documento Markdown para tomar decisiones sobre esta información;
- el documento lo revisen personas y lo actualicen a mano con la decisión de cada apartado,
  aportando contexto nuevo según el estado de la leyenda;
- en las revisiones se lea el documento, se identifiquen las decisiones tomadas y se actualice
  la documentación citando el propio documento.

Decisiones del usuario: alcance **C + D** (Arquetipo 13 transversal + `doc_trace decisions`),
registro **dentro de `docs/`**, IDs **`COB-<ÁMBITO>-<NNN>`**, commit directo en `develop`.

## Objetivo operativo de esta sesión
- Arquetipo 13 «Registro de Decisiones de Cobertura» en el estándar, con la leyenda canónica.
- Instrucciones (prompt, agentes, flujo `/document-project`, entry points) que generan el
  registro y lo consumen en las revisiones sin tocar los campos humanos.
- Subcomando determinista `doc_trace.py decisions` con tests.
- Documentación propia (dogfooding de doc_trace y arquetipos), ADR-004 y CHANGELOG.

## Restricciones explícitas
- Sin API keys ni servicios IA; tooling determinista, sin red en tests.
- mypy strict + ruff sin errores; sin dependencias nuevas.
- Prohibido refactorizar código existente.
- Commit directo en `develop`; sin merge ni tag.

## Resultado esperado
- `.ai/sessions/2026-11-04_registro_decisiones/{00_REQUEST,01_PLAN_AUDIT,TRACEABILITY}.md`
- Cambios en estándar, prompts, agentes, plantilla, script, tests, docs y CHANGELOG.
