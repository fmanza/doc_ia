# TRACEABILITY

## Session metadata

| Campo | Valor |
|---|---|
| Fecha | 2026-11-09 |
| Skill | `/new-feature` |
| Rama | `develop` |
| Veredicto | GO |

## Prompt issued

`/new-feature` con los tres objetivos de `00_REQUEST.md`; AUDIT_PLAN GO_CONDICIONAL (informe sin
valores, test de presencia del Arq. 14 en todos los puntos, `replace` solo para documentos
reestructurados que indica el usuario). Las tres condiciones se cumplen.

## Context supplied

Ver `00_CONTEXT_SNAPSHOT.md`.

## AI output summary

1. `scripts/snapshot_sources.py`: `replace_source()` y subcomando `replace` (historial
   «sustituido», retira `_staging/<nombre>/`, valida el documento nuevo antes de tocar nada).
2. `scripts/redact_secrets.py` (nuevo): 6 reglas, filtros de marcadores, URL y prosa, tramos sobre
   el texto original, E/S en bytes, `--check`, exit 0/1/2, informe sin valores. Prueba de humo:
   detecta los secretos reales de un destino y ningún falso positivo tras ajustar las reglas.
3. Norma §3.19 (Arquetipo 14) + delimitación en §3.2, §2.3 y §4.3; prompt
   `integration_doc.prompt.md`; `document_project`: versión vigente y `replace` (Fase 0-pre),
   mapeo MATERIAL, Paso 4b, detección de integraciones (Fase 1), Fase 3b, CIERRE `--check`;
   comando, agente, `docs.instructions`, `CLAUDE.md`, `SHARED_INSTRUCTIONS`, MANIFEST,
   `EDGE_CASES` (2 casos).
4. Tests: 6 de `replace`, 12 funciones de `redact_secrets` (25 casos), 4 de conformidad.
5. Dogfooding: páginas funcional, técnica y ejemplo de `redact_secrets`; `snapshot_sources`
   (AC-14..17), arquetipos (AC-16), `document_project`, tipos de origen, referencia, mapa funcional
   (142/167), nav; `stamp`, `drift`, `decisions`, `matrix`, `llms` en 0; build `--strict`.

## Artefactos generados

| Artefacto | Ruta | Estado |
|---|---|---|
| Subcomando replace | `scripts/snapshot_sources.py` | completado |
| Redacción de credenciales | `scripts/redact_secrets.py` | completado |
| Arquetipo 14 | `.github/DOCUMENTATION_STANDARD.md` §3.19, `.github/prompts/integration_doc.prompt.md` | completado |
| Orquestación | `.github/prompts/document_project.prompt.md`, `.claude/commands/document-project.md` | completado |
| Tests | `tests/test_redact_secrets.py`, `tests/test_snapshot_sources.py`, `tests/test_docs_conformance.py` | completado |
| Docs | `docs/{functional,api,examples}/redact_secrets*`, páginas actualizadas | completado |

## Directrices para Futuras IAs

- `replace` solo para documentos reestructurados que indica el usuario; una versión nueva del
  mismo documento la recoge `sync`.
- `redact_secrets.py` es una red de seguridad: no detecta pares «usuario / clave» sin separador ni
  contraseñas solo de letras.
- Los destinos reciben las novedades con `kit.py sync`; migrar sus páginas de integraciones a
  `docs/integraciones/` en una sesión `/documentar` propia.

## Veredicto final

**GO** — pendiente de commit en `develop` (propuesto en VERSION).
