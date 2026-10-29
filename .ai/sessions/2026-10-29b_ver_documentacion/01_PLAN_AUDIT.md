# PLAN + AUDIT_PLAN + AUDIT_CODE — Instrucciones de visualización en el destino

## PLAN (aprobado con «IMPLEMENT», decisiones recomendadas)
`/document-project` genera siempre `VER_DOCUMENTACION.md` (`VIEW_DOCS.md` si idioma `en`) en la
raíz del destino, fuera de `docs/`, desde `.github/templates/VER_DOCUMENTACION.template.md`.
Secciones fijas 0-7: ¿qué tienes? · requisitos por ruta · instalar Python (Windows/macOS/Linux) ·
Ruta A web (solo con publicación verificada) · Ruta B ZIP + `start-server.py` · Ruta C código
fuente con `.venv` sin activar · problemas frecuentes · detener y limpiar.

| Fase | Ficheros | Estado |
|---|---|---|
| F1 Producto | plantilla nueva; prompt (Fase 7c, salida 8c, Paso B3 sin «Opción B», A2-1 con `EXTRA_FILES`, Gaps V1/V2); comando; agente; `SHARED_INSTRUCTIONS.md` | ✅ |
| F2 Empaquetado | `mkdocs_hooks.py` y `build_docs_zip.py` con `EXTRA_FILES`; `_zip` sin `make_archive` (sin ZIP anidado); notas de release del workflow | ✅ |
| F3 Servidor | `start-server.py`: `127.0.0.1`, `directory=` sin `os.chdir`, puerto ocupado → exit 1 + sugerencia; `DocsServer(ThreadingHTTPServer)` sin `SO_REUSEADDR` en Windows | ✅ |
| F4 Guardas | `test_start_server.py` (6), `test_versioned_zip_matches_latest_layout`, 4 tests de coherencia en `test_docs_conformance.py`; EDGE_CASES ×3 | ✅ |
| F5 Dogfooding y docs | `VER_DOCUMENTACION.md` de doc_ia; `downloads.md`; reference, api/functional `build_docs_zip` (AC-11) y `document_project` (AC-11), mapa funcional; `.ai/{product,glossary}.md`; CHANGELOG | ✅ |

## AUDIT_PLAN — GO_CONDICIONAL → condiciones cumplidas
| ID | Hallazgo | Resolución |
|---|---|---|
| A1 | «Opción B: abrir `index.html`» falsa (enlaces a carpetas) | Retirada de `downloads.md`, Paso B3, agente y notas de release; test `test_downloads_never_offers_opening_index_html` |
| A2 | Ver el ZIP requiere Python | La guía instala Python en los tres sistemas; ZIP sin servidor = D5, fuera de alcance |
| A3 | `pip install` inventado si el destino no declara dependencias | Gap V1: crear `requirements-docs.txt` |
| A4 | Enlace desde `docs/` rompe `--strict` | Se cita como código inline |
| A5 | Ruta A inventada | Solo con `site_url` + publicación; doc_ia: «No aplica» (no hay workflow de Pages) |
| A6 | ExecutionPolicy al activar el venv | Se usa `.venv\Scripts\python` sin activar |
| A7/A8 | `start-server.py` en todas las interfaces | Solo `127.0.0.1`; CLI sin cambios |
| A9 | Fuentes de instalación | Solo python.org, winget, Homebrew y gestores de paquetes de la distribución |
| A10 | Drift bloqueante | 9 páginas revisadas y re-selladas; `drift` = 0 |

## AUDIT_CODE — GO
| ID | Hallazgo | Resolución |
|---|---|---|
| C1 | El ZIP versionado (Releases) no llevaba `start-server.py` y anidaba el ZIP `latest` (155 entradas) | `_zip` replica al hook: 99 entradas, idéntico al `latest` (verificado) |
| C2 | Prueba de humo: una conexión ociosa (preconexión de Chrome) bloqueaba `TCPServer` | `ThreadingHTTPServer`; test con loopback real |
| C3 | `ThreadingHTTPServer` activa `SO_REUSEADDR`: en Windows, segundo bind aceptado (verificado) → el puerto ocupado no se detecta | `allow_reuse_address = sys.platform != "win32"`; `test_second_server_on_same_port_fails` |
| C4 | Primera lectura del Mermaid local recién extraído: 11 s en Windows, incluso sin servidor (antivirus) | Fila en «Problemas frecuentes» de la plantilla |
| C5 | ZIP de releases ≤ 0.3.0 sin `start-server.py` | Alternativa `python -m http.server --bind 127.0.0.1` en §4 |
| C6 | `EXTRA_FILES` duplicado en hook y script | Aceptado: ambos son patrones independientes que se copian a destinos; los dos tests vigilan el contenido |
| C7 | Los tests de la Fase 7c comprueban coherencia de instrucciones y la instancia de doc_ia, no el resultado en destinos externos | ⚠️ en la Evidencia de `functional/document_project.md` |
| C8 | `VIEW_DOCS.md` (inglés) sin test propio | Riesgo residual: la plantilla es en español y el agente la traduce |

DoD: ruff ✅ · mypy ✅ · pytest 225 ✅ · `mkdocs build --strict` ✅ · `doc_trace drift/matrix/llms` ✅ ·
prueba de humo del ZIP extraído (5 rutas 200 con conexión ociosa; puerto ocupado → exit 1) ✅.

## Pendiente
- D5: ZIP navegable sin servidor (plugin `offline` / `use_directory_urls: false`) → feature aparte.
- Sin commit hasta indicación del usuario.
