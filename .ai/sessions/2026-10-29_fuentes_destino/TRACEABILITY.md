# TRACEABILITY — 2026-10-29 fuentes convertidas en el destino

## Resumen
Los documentos convertidos llegaban al destino como `.fuentes/` o `_fuentes/` porque ninguna
instrucción fijaba su ubicación. Regla única: `<raíz del destino>/_fuentes/<nombre_origen>/<ruta
relativa al origen>`, siempre, versionada y fuera de `docs/`; `.fuentes/` y `fuentes/` se migran
con confirmación.

## Artefactos
| Artefacto | Ruta | Estado |
|---|---|---|
| Prompt del producto (Fase 0b, 0c Pasos 0/5/6/7, Fase 1, INVENTARIO, CIERRE) | `.github/prompts/document_project.prompt.md` | Modificado |
| Comando | `.claude/commands/document-project.md` | Modificado |
| Agente | `.github/agents/documentation-generator.agent.md` | Modificado |
| Instrucciones compartidas | `.github/SHARED_INSTRUCTIONS.md` | Modificado |
| Estándar §3.16 regla 4 | `.github/DOCUMENTATION_STANDARD.md` | Modificado |
| Plantilla de sesión | `.ai/sessions/TEMPLATE/00_CONTEXT_SNAPSHOT.md` | Modificado |
| Test de coherencia | `tests/test_docs_conformance.py::test_sources_folder_is_canonical` | Nuevo (4 casos) |
| Caso límite | `.claude/EDGE_CASES.md` | Añadido |
| Docs (+AC-09, AC-10, mapa funcional 0/10) | `docs/functional/{document_project,origin_types,convert_to_md,index}.md`, `docs/api/document_project.md` | Modificado; 6 páginas re-selladas |
| Contexto | `.ai/{glossary,standards}.md`, `CHANGELOG.md` | Modificado |

## Verificación
ruff ✅ · mypy ✅ · pytest ✅ · `doc_trace drift` sin hallazgos · `doc_trace matrix` ✅ ·
`mkdocs build --strict` ✅

## Directrices para IAs futuras
- El nombre de la carpeta en el destino es literal: `_fuentes/`. No proponer alternativas.
- `md/` en la raíz del destino NO es un nombre a migrar: puede ser la salida de `convert_to_md.py`.
- Pendiente A7 resuelto en la misma fecha: la Fase 0c usa docling como motor por defecto
  (markitdown solo para XLS, pandoc para DOC/ODT/RST).

## Versión
| Paso | Resultado | Commit | Estado |
|---|---|---|---|
| Commits de la sesión | `add850b` (`_fuentes/`), `3f1f024` (docling en Fase 0c) | — | HECHO |
| VERSION | `release: v0.3.0 - …` (`02_VERSION_CLOSURE.md`); CI run 40861856978 verde | `d95fff3` | HECHO |
| VERSION | merge `--no-ff` a `main`; CI run 40862075090 verde; release `docs-v0.3.0` (run 40862075101) | `6ceb437` | HECHO |
| VERSION | tag `v0.3.0` sobre `6ceb437` → release `v0.3.0` con `doc_ia-docs-0.3.0.zip` (run 40862339206) | `6ceb437` | HECHO |

## Veredicto
CLOSED — release v0.3.0 publicada y verificada.
