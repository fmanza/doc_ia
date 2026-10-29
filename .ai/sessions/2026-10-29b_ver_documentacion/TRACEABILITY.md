# TRACEABILITY — 2026-10-29b instrucciones de visualización en el destino

## Resumen
Quien recibe la documentación (incluso sin Python) no tenía instrucciones válidas: la «Opción B»
(abrir `index.html`) no navega con `use_directory_urls: true`. Nueva Fase 7c: `VER_DOCUMENTACION.md`
siempre en la raíz del destino desde plantilla; viaja en los dos ZIP con `start-server.py`, ahora
solo en loopback, concurrente y con detección real de puerto ocupado.

## Artefactos
| Artefacto | Ruta | Estado |
|---|---|---|
| Plantilla | `.github/templates/VER_DOCUMENTACION.template.md` | Nuevo |
| Instancia doc_ia | `VER_DOCUMENTACION.md` | Nuevo |
| Producto | `.github/prompts/document_project.prompt.md`, `.claude/commands/document-project.md`, `.github/agents/documentation-generator.agent.md`, `.github/SHARED_INSTRUCTIONS.md` | Modificado |
| Tooling | `scripts/start-server.py`, `scripts/build_docs_zip.py`, `mkdocs_hooks.py`, `.github/workflows/docs-zip-release.yml` | Modificado |
| Tests | `tests/test_start_server.py` (nuevo, 6), `tests/test_build_docs_zip.py` (+1), `tests/test_docs_conformance.py` (+4 funciones, 7 casos) | Nuevo / modificado |
| Docs | `docs/downloads.md`, `docs/reference/index.md`, `docs/{api,functional}/{build_docs_zip,document_project}.md`, `docs/functional/index.md`; re-sellado de 9 páginas | Modificado |
| Contexto | `.ai/{product,glossary}.md`, `.claude/EDGE_CASES.md` (+3), `CHANGELOG.md` | Modificado |

## Directrices para IAs futuras
- Nunca ofrecer «abrir `index.html` directamente» para el ZIP: solo servidor local.
- `VER_DOCUMENTACION.md` está fuera de `docs/`: no enlazarlo desde el sitio.
- `start-server.py` debe seguir en `127.0.0.1`, con hilos y sin `SO_REUSEADDR` en Windows.
- Los dos ZIP deben tener el mismo contenido (`EXTRA_FILES` en hook y script).

## Veredicto
GO — IMPLEMENT + AUDIT_CODE completos; sin commit (pendiente de indicación). D5 pendiente como feature aparte.
