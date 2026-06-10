---
session: 2026-06-10i_example_document_project
skill: new_feature (Arquetipo 4 — ejemplo de uso)
branch: develop
status: CLOSED
---

# TRACEABILITY — 2026-06-10i: Ejemplo de uso de /document-project

## Solicitud

Crear un ejemplo de uso del proyecto (feature principal: `/document-project`).

## Contexto de partida

`docs/examples/` solo tenía ejemplos del tooling determinista (`check_env_usage.md`,
`build_docs_zip_offline.md`). La capacidad IA principal del producto no tenía ningún
ejemplo en Arquetipo 4.

## Archivos creados / modificados

| Archivo | Tipo | Contenido |
|---|---|---|
| `docs/examples/document_project_usage.md` | CREADO | Arquetipo 4: 3 escenarios (sin doc, parcial, --verify-build), output esperado por fase, enlace bidireccional §5 |
| `mkdocs.yml` | ACTUALIZADO nav | Nueva subsección "Flujos IA" con entrada "Documentar un Proyecto" en sección "Ejemplos" |

## Decisiones tomadas

- **No se creó `.py`** para §2: el flujo `/document-project` ocurre en el chat (principio
  del proyecto). Se usaron bloques inline siguiendo el patrón de `build_docs_zip_offline.md`.
- **Subsección "Flujos IA"** añadida antes de "Tooling Determinista" en `nav: Ejemplos`,
  replicando la estructura ya presente en "Documentación Funcional".

## Build verificado

`python -m mkdocs build --strict` → `Documentation built in 0.45 seconds` sin warnings.

## Veredicto

PASS — el ejemplo cubre los 3 escenarios principales de uso, muestra el output real de
cada fase del flujo y queda enlazado bidireccionalmente con `functional/document_project.md`
y `functional/archetypes.md`.
