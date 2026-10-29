# TRACEABILITY — 2026-10-29d ZIP navegable sin servidor

## Session metadata
- id: 2026-10-29d
- fecha: 2026-10-29
- rama: develop
- skill: new_feature
- fase: PLAN + AUDIT_PLAN + IMPLEMENT (L1-L3) + AUDIT_CODE + prueba de humo C2

## Resumen
El ZIP se abre con doble clic en `index.html` tras extraerlo, con navegación, búsqueda y
diagramas, sin Python, servidor ni red, con MkDocs Material y Zensical: `use_directory_urls:
false` + plugin `offline` + shim iframe-worker 1.0.4 local en `extra.polyfills` (los dos temas lo
pedían a unpkg). `build_docs_zip.py` rechaza un `site/` que no se abra así. Se corrigió que el ZIP
`latest` saliera sin índice de búsqueda (orden de `on_post_build`).

## Artefactos
| Artefacto | Ruta | Estado |
|---|---|---|
| Shim vendorizado | `docs/assets/vendor/iframe-worker/` | Nuevo |
| Configuración | `mkdocs.yml`, `.github/templates/TEMPLATE_mkdocs.yml` | Modificado |
| Tooling | `scripts/build_docs_zip.py`, `mkdocs_hooks.py`, `.github/workflows/{ci,docs-zip-release}.yml` | Modificado |
| Tests | `tests/test_offline_assets.py` (nuevo), `tests/test_build_docs_zip.py`, `tests/test_docs_conformance.py` | Nuevo / modificado |
| Producto | prompt, comando, agente, SHARED, CLAUDE.md, DOCUMENTATION_STANDARD, docs.instructions, plantilla `VER_DOCUMENTACION` | Modificado |
| Docs | `downloads.md`, `{functional,api}/build_docs_zip.md`, ejemplo, referencia, troubleshooting, `{functional,api}/document_project.md`, mapa funcional, `llms.txt`; 9 páginas re-selladas | Modificado |
| Contexto | `VER_DOCUMENTACION.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `.claude/EDGE_CASES.md`, `.ai/{product,glossary}.md` | Modificado |
| Prueba de humo | `.ai/sessions/2026-10-29d_zip_sin_servidor/smoke/` (scripts CDP y BiDi + resultados) | Nuevo |

## Directrices para Futuras IAs
- **[offline]**: sin una entrada con `iframe-worker` en `extra.polyfills`, Material y Zensical
  añaden `https://unpkg.com/iframe-worker/shim`; sin red, la búsqueda por `file://` no arranca.
- **[mkdocs_hooks.py]**: el hook del ZIP debe ir después de `offline` (`mkdocs_priority = -200`);
  si no, el ZIP `latest` sale sin `search/search_index.js`.
- **[búsqueda por file://]**: Material solo envía el índice al worker al abrir la búsqueda; para
  probarla, usar clic y teclado reales, no eventos sintéticos. Zensical la monta en shadow DOM.
- **[Firefox sin ventana]**: `document.hasFocus()` es false; el foco no abre la búsqueda.
- **[Procesos]**: matar el proceso padre de un navegador sin ventana deja hijos un tiempo; filtrar
  siempre por el nombre del perfil temporal, nunca por el nombre del ejecutable.

## Veredicto final
GO — sin commit (pendiente de indicación).
