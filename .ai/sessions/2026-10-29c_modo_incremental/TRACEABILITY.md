# TRACEABILITY — 2026-10-29c modo incremental de `/document-project`

## Resumen
Relanzar `/document-project` sobre un destino ya documentado releía el origen entero. Ahora el
CIERRE guarda el commit de cada origen (`doc_trace.py baseline` → `.ai/doc_state.json`) y la
Fase 1 siguiente parte de `doc_trace.py changes`: ficheros cambiados y páginas que los citan.

## Artefactos
| Artefacto | Ruta | Estado |
|---|---|---|
| Herramienta | `scripts/doc_trace.py` (`baseline`, `changes`) | Modificado |
| Tests | `tests/test_doc_trace.py` (+12 casos, git real en `tmp_path`), `tests/test_docs_conformance.py` (+4) | Modificado |
| Producto | `.github/prompts/document_project.prompt.md`, `.claude/commands/document-project.md`, `.github/agents/documentation-generator.agent.md`, `.github/SHARED_INSTRUCTIONS.md`, `.ai/sessions/TEMPLATE/00_CONTEXT_SNAPSHOT.md` | Modificado |
| Docs | `docs/{functional,api,examples}/doc_trace.md`, `docs/reference/index.md`, `docs/{functional,api}/document_project.md`, `docs/functional/index.md`; 9 páginas re-selladas | Modificado |
| Contexto | `.ai/{product,glossary}.md`, `.claude/EDGE_CASES.md` (+2), `CHANGELOG.md` | Modificado |

## Directrices para IAs futuras
- `.ai/doc_state.json` lo escribe solo `doc_trace.py baseline`; nunca a mano.
- En incremental, leer el **diff** de cada fichero cambiado, no el fichero ni el origen entero.
- «Lo mencionan» ≠ «Lo citan»: una mención solo pasa a B si el diff cambia lo descrito.
- Código 3 de `changes` = modo completo para ese origen; anotar el motivo en INVENTARIO.

## Veredicto
GO — IMPLEMENT + AUDIT_CODE completos; sin commit (pendiente de indicación).
