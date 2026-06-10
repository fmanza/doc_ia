# REQUEST

## Session metadata
- id: 2026-06-10m_archetypes_revision
- fecha: 2026-06-10
- rama: develop
- skill: refactor documental
- fase solicitada: PLAN → AUDIT_PLAN → IMPLEMENT

## Solicitud original saneada

Revisar los arquetipos actuales y buscar mejoras estándar y proponer nuevos,
para ello puede mirar en internet. PLAN - AUDIT PLAN.

## Objetivo operativo de esta sesión

- Auditar los 8 arquetipos actuales contra estándares externos (Diátaxis, MADR 4.0, The Good Docs Project)
- Identificar gaps: arquetipos mezclados, desactualizados o ausentes
- Implementar mejoras en la fuente canónica (DOCUMENTATION_STANDARD.md) y prompts
- Sincronizar CLAUDE.md, SHARED_INSTRUCTIONS.md y bootstrap_ai_config.prompt.md

## Restricciones explícitas

- Solo documentación — sin cambios en scripts/ ni tests/
- No romper build `mkdocs build --strict`
- Retrocompatible: arquetipos existentes numerados no se renumeran; los nuevos se añaden

## Resultado esperado

- DOCUMENTATION_STANDARD.md actualizado con: §3.3→3a, §3.5→MADR 4.0, §3.6+variante D, §3.11-3.14 nuevos
- 5 nuevos prompts: howto_doc, tutorial_doc, changelog, ai_config_doc, contributing_doc
- architecture_doc.prompt.md actualizado a MADR 4.0
- CLAUDE.md con tabla 11 arquetipos activos
- Build mkdocs --strict sin errores
- Sesión registrada en .ai/sessions/ con trazabilidad completa
