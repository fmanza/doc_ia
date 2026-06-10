# REQUEST

## Session metadata
- id: 2026-06-10b
- fecha: 2026-06-10
- rama: main
- skill: config_review (auditoría post-bootstrap)
- fase solicitada: completa (ANÁLISIS → AUDIT → REMEDIACIÓN → VERSION)

## Solicitud original saneada
Ejecutar la auditoría post-bootstrap prevista por `bootstrap_ai_config.prompt.md` §"auditoría
de configuración", usando el agente Config Reviewer (`config_review.prompt.md`), sobre la
configuración IA recién instalada en doc_ia (commit a8ebf2c).

## Objetivo operativo de esta sesión
- Verificar integridad de los ficheros copiados/adaptados en el bootstrap.
- Verificar integridad referencial (referencias internas a ficheros existentes).
- Remediar hallazgos críticos.

## Restricciones explícitas
- Origen util_bbdd de solo lectura.
- DRY: no duplicar contenido ya cubierto por DOCUMENTATION_STANDARD.md.
- Sin APIs de IA externas.
