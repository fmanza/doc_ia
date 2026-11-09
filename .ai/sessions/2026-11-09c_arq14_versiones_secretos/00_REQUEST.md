# REQUEST

## Session metadata

| Campo | Valor |
|---|---|
| Fecha | 2026-11-09 |
| Skill | `/new-feature` |
| Rama | `develop` |

## Solicitud original saneada

Incorporar al estándar doc_ia tres mejoras surgidas al documentar un destino (sesiones del
2026-11-09): (1) Arquetipo 14 «Integraciones»; (2) regla de versión vigente de documentos
reestructurados con soporte `snapshot_sources.py replace`; (3) detección y redacción de
credenciales en documentos fuente. Opciones elegidas por el usuario: Arquetipo 14 nuevo,
«Regla + replace», «Detectar + redactar».

## Objetivo operativo de esta sesión

PLAN → AUDIT_PLAN → IMPLEMENT → AUDIT_CODE → VERSION, sin datos del destino como plantilla.

## Restricciones explícitas

Tooling determinista sin red ni IA; mypy strict + ruff; tests sin red; Conventional Commits.

## Resultado esperado

Norma, prompt, orquestador, herramientas, tests y documentación de doc_ia actualizados.
