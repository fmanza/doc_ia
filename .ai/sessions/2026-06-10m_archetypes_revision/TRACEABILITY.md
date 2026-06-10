---
session: 2026-06-10m_archetypes_revision
skill: refactor documental
branch: develop
status: CLOSED
---

# TRACEABILITY — 2026-06-10m: Revisión y mejora de arquetipos de documentación

## Solicitud

Revisar los arquetipos actuales y buscar mejoras estándar y proponer nuevos
mirando en internet. Flujo: PLAN → AUDIT_PLAN → IMPLEMENT.

## Fases ejecutadas

PLAN → AUDIT_PLAN → IMPLEMENT

## Investigación externa realizada

| Estándar | Versión | Hallazgo relevante |
|---|---|---|
| **Diátaxis** (Daniele Procida) | 2024-2025 | Distingue explícitamente Tutorial (aprendizaje) de How-to (tarea). El Arquetipo 3 actual mezclaba ambos en una sola estructura. |
| **MADR** (Markdown Any Decision Records) | 4.0 — septiembre 2024 | Añade frontmatter YAML (status/date/deciders/consulted/informed), título `Use X for Y`, formatos Full y Minimal. |
| **The Good Docs Project** | 2025 | Templates específicos para Quickstart, Changelog, CONTRIBUTING, README. El Quickstart es distinto de la Instalación. |
| **Keep a Changelog** | 1.1.0 | Estándar de-facto para CHANGELOG.md: categorías fijas, [Unreleased] permanente, enlaces de comparación. |
| **Google Season of Docs Archetypes** | FOSDEM 2025 | 13 project archetypes; el primero ("The Migration") demostrado en FOSDEM 2025. |

## Gaps identificados (pre-implementación)

| Gap | Arquetipos afectados | Prioridad |
|---|---|---|
| Tutorial ≠ How-to mezclados | Arquetipo 3 | Alta |
| ADR sin frontmatter YAML ni "Use X for Y" | Arquetipo 5 | Alta |
| Changelog sin arquetipo formal (CHANGELOG.md existe pero sin contrato) | — | Alta |
| Configuración de agente IA sin arquetipo (CLAUDE.md no documentado como tipo) | — | Media |
| Quick Start ausente (distinto de Instalación) | Arquetipo 6 | Media |
| Guía de Contribución sin arquetipo (diferente de Onboarding) | — | Media |

## Archivos creados / modificados

| Archivo | Tipo | Cambios |
|---|---|---|
| `.github/DOCUMENTATION_STANDARD.md` | ACTUALIZADO | §3.3 → Arquetipo 3a How-to; §3.5 → MADR 4.0 con Full/Minimal; §3.6 + Variante D Quick Start; §3.9 conjunto mínimo +CONTRIBUTING +CHANGELOG; §3.11 Arquetipo 3b Tutorial; §3.12 Arquetipo 9 Changelog; §3.13 Arquetipo 10 Config IA; §3.14 Arquetipo 11 Contribución; §4.3 tabla secciones opcionales; §7 criterios completitud |
| `CLAUDE.md` | ACTUALIZADO | Tabla arquetipos: 7 → 11 activos; referencias a Diátaxis y MADR 4.0 |
| `.github/SHARED_INSTRUCTIONS.md` | ACTUALIZADO | 3 referencias "7 arquetipos" → conteo abierto + lista actualizada |
| `.github/prompts/architecture_doc.prompt.md` | ACTUALIZADO | Reescrito para MADR 4.0: frontmatter YAML, "Use X for Y", formatos Full/Minimal, tabla Full vs Minimal |
| `.github/prompts/guide_doc.prompt.md` | ACTUALIZADO | Nota de deprecación → redirige a howto_doc y tutorial_doc |
| `.github/prompts/bootstrap_ai_config.prompt.md` | ACTUALIZADO | Lista y tabla de arquetipos actualizadas (3a/3b, 9, 11) |
| `.github/prompts/howto_doc.prompt.md` | CREADO | Arquetipo 3a How-to (Diátaxis cuadrante How-to) |
| `.github/prompts/tutorial_doc.prompt.md` | CREADO | Arquetipo 3b Tutorial (Diátaxis cuadrante Tutorial) |
| `.github/prompts/changelog.prompt.md` | CREADO | Arquetipo 9 Changelog (Keep a Changelog 1.1.0) |
| `.github/prompts/ai_config_doc.prompt.md` | CREADO | Arquetipo 10 Configuración Agente IA (propio de doc_ia) |
| `.github/prompts/contributing_doc.prompt.md` | CREADO | Arquetipo 11 Guía de Contribución |

## Build verificado

`python -m mkdocs build --strict` → `Documentation built in 0.51 seconds` sin errores.
`python -m ruff check scripts tests` → `All checks passed!`
`python -m mypy scripts` → `Success: no issues found in 2 source files`

## Directrices para Futuras IAs

- **[arquetipos]**: El Arquetipo 3 está ahora dividido en 3a (How-to) y 3b (Tutorial). Para guías nuevas usar `howto_doc.prompt.md` o `tutorial_doc.prompt.md` según si el objetivo es resolver una tarea o aprender.
- **[ADR]**: El Arquetipo 5 sigue MADR 4.0. Los ADR nuevos deben tener frontmatter YAML y título en forma `Use X for Y`. Los ADR existentes sin frontmatter son válidos; actualizarlos al modificarlos.
- **[guide_doc.prompt.md]**: Fichero deprecado. Solo para compatibilidad con guías generadas antes de la división 3a/3b. No usar para nuevas guías.
- **[arquetipos 9-11]**: Changelog, Config IA y Contribución son opcionales según el tipo de proyecto. Activarlos cuando aplique (ver §4.3 del DOCUMENTATION_STANDARD).
- **[bootstrap]**: `bootstrap_ai_config.prompt.md` ya incluye los nuevos arquetipos (3a, 3b, 9, 11) en su lista de ficheros a replicar.

## Veredicto final

Veredicto: GO
Pendientes al cierre:
- Ninguno. Build limpio, coherencia verificada, todos los prompts creados y referenciados.
