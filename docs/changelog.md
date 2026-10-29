# Changelog

Todos los cambios notables de este proyecto se documentan aquí.
Formato: [Keep a Changelog](https://keepachangelog.com/) · Versioning: [SemVer](https://semver.org/)

## [Unreleased]

### Added

- **Producto — instrucciones de visualización** (Fase 7c de `/document-project`, siempre): el
  destino recibe `VER_DOCUMENTACION.md` (`VIEW_DOCS.md` en inglés) en su raíz, generado desde
  `.github/templates/VER_DOCUMENTACION.template.md`: qué ruta seguir (web, ZIP, código fuente),
  instalación de Python desde cero en Windows, macOS y Linux, servidor local y problemas
  frecuentes, con valores verificados en el destino. Gap V1 (sin `requirements-docs.txt` → se
  crea) y Gap V2 (`EXTRA_FILES` en hook/script). Instancia propia de doc_ia en la raíz.
- Tests: `test_start_server.py`, `test_versioned_zip_matches_latest_layout` (AC-11 del ZIP
  offline) y guardas de coherencia de la Fase 7c (AC-11 de Documentar un Proyecto).

### Changed

- `start-server.py` escucha solo en `127.0.0.1` (antes, todas las interfaces), atiende cada
  conexión en su hilo (antes, una conexión ociosa del navegador bloqueaba el servidor), sirve su
  carpeta sin cambiar el directorio de trabajo y, con el puerto ocupado, termina con código 1 y
  sugiere `--port` (en Windows, sin `SO_REUSEADDR`, que permitía compartir el puerto en silencio).
- Los dos ZIP llevan `start-server.py` y `VER_DOCUMENTACION.md` en su raíz (`EXTRA_FILES` en
  `mkdocs_hooks.py` y `build_docs_zip.py`).

### Fixed

- El ZIP versionado (`dist/`, el que publican las Releases) no incluía `start-server.py` y
  contenía anidado `doc_ia-docs-latest.zip` con su `.sha256`: ahora tiene el mismo contenido
  que el ZIP "latest".
- `docs/downloads.md`, el Paso B3 del producto y las notas de release ofrecían abrir `index.html`
  directamente: con `use_directory_urls: true` los enlaces apuntan a carpetas y no navega.

## [0.3.0] — 2026-10-29

### Added

- **Regla transversal de diagramas** (`DOCUMENTATION_STANDARD.md` §3.17): fuente única de las
  reglas Mermaid (tipo por arquetipo con columna de colores del tema, una vista por arquetipo,
  máximo 12 nodos y 8 en el Arquetipo 6, etiquetas, accesibilidad, estilo y validación).
- **Tests de conformidad de diagramas**: sin entidades HTML, labels especiales entre comillas,
  `accTitle`/`accDescr` obligatorios y tamaño máximo (criterios AC-11 a AC-13).
- **Job `mermaid` en CI**: valida cada página de `docs/` con el parser real
  (`@mermaid-js/mermaid-cli`) y la misma versión que sirve el sitio.
- **Mermaid servido en local** (`docs/assets/vendor/mermaid/mermaid-12.2.0.min.js` +
  `assets/js/mermaid-theme.js`): los diagramas del sitio y del ZIP offline se dibujan sin conexión,
  con la misma versión en MkDocs Material y Zensical. `tests/test_mermaid_assets.py` vigila versión,
  huella, orden de carga, coherencia con CI y el cargador del tema (AC-10 del ZIP offline).
- **Producto**: la Fase 0b de `/document-project` sincroniza cinco recursos en vez de tres y lleva
  Mermaid local a los proyectos documentados.
- **Producto**: el destino de `/document-project` recibe siempre los documentos convertidos en
  `_fuentes/<nombre_origen>/<ruta relativa al origen>` (Fase 0c, Paso 5), versionados y fuera de
  `docs/`, para que la evidencia y `doc_trace` citen rutas del propio repositorio.
  `test_sources_folder_is_canonical` comprueba la regla en prompt, comando, agente y
  `SHARED_INSTRUCTIONS.md`.

### Changed

- Rediseño de 9 diagramas que superaban 12 nodos o repetían el mismo flujo en varios
  arquetipos (document_project, convert_to_md, archetypes, origin_types, doc_trace); los 24
  diagramas declaran título y descripción accesibles.
- `gitgraph` y `architecture-beta` pasan a OPCIONAL; la "Arquitectura física" usa `flowchart LR`
  con `subgraph`; el Arquetipo 1 §3 admite `flowchart TD` de decisiones.

### Fixed

- La regla `@` → `&#64;` pintaba un `&` sobrante (Mermaid no decodifica entidades HTML): las
  labels con `@ ( ) { }` van entre comillas. Corregido `on_post_build(config)` en
  `docs/api/build_docs_zip.md`.
- **Producto**: los documentos convertidos llegaban al destino con nombres improvisados
  (`.fuentes/` en unas sesiones, `_fuentes/` en otras) porque ninguna instrucción fijaba la
  ubicación. Ahora `_fuentes/` es el único nombre; los otros se migran con confirmación.
- **Producto**: la Fase 0c de `/document-project` describía markitdown como motor principal,
  con enrutado por extensión, plugins y fallback a pandoc que `convert_to_md.py` ya no tiene.
  Ahora usa docling (motor por defecto) y recurre a `--engine markitdown` solo para XLS y a
  `--engine pandoc` para DOC/ODT/RST. Alineados `SHARED_INSTRUCTIONS.md`, `.ai/` y los textos
  de `check_env.py`.

## [0.2.0] — 2026-10-28

### Added

- **Arquetipo 12 — Referencia del Sistema** (`docs/reference/`, condicional): configuración,
  CLI, errores y códigos de salida, eventos e interfaces publicadas; prompt
  `reference_doc.prompt.md`. Primera aplicación: `docs/reference/index.md` de doc_ia.
- **Regla transversal de evidencia y confianza** (`DOCUMENTATION_STANDARD.md` §3.16): bloque
  plegable "Evidencia" en los Arquetipos 1, 2 y 12, citas `ruta::símbolo` en código inline y
  leyenda ✅ ⚠️ 🔍 ❌.
- **Variante 6C**: subapartado §3 › Despliegue (arc42 §7, condicional) y escenarios de calidad
  en §4 (arc42 §10). Aplicado en `docs/architecture.md`.
- **ADR-002** — Use evidence-backed archetypes for repository documentation.
- **Trazabilidad funcional y de pruebas** (P2): columna `Test` en los criterios de aceptación del
  Arquetipo 1 §7, nueva §6 "Verificación y Tests" del Arquetipo 2 y subsección condicional
  "Actores y permisos" en el Arquetipo 1 §2.
- **Mapa Funcional** (Variante 1-I del Arquetipo 1, `docs/functional/index.md`): capacidades,
  recorridos transversales, actores y glosario global del sistema.
- **Arquetipo 12 §6 "Datos"** (condicional): `erDiagram` global y diccionario con sensibilidad
  por campo; aplicado a los ficheros con formato propio de doc_ia.
- **`scripts/doc_trace.py`** (P3): trazabilidad determinista docs ↔ código con subcomandos
  `stamp` (huellas SHA256 en el frontmatter), `drift` (páginas desactualizadas), `matrix`
  (criterios de aceptación ↔ tests) y `llms` (`docs/llms.txt` desde el nav). 20 tests.
- **Frontmatter de trazabilidad** (`arquetipo`, `fuentes`, `revisado`) en las 15 páginas de
  doc_ia con bloque "Evidencia"; `docs/llms.txt` publicado en la raíz del sitio.
- **CI de calidad** (`.github/workflows/ci.yml`, Python 3.12 y 3.14): ruff, formato, mypy strict,
  pytest, `doc_trace` (drift bloqueante, matrix, `llms --check`) y build `--strict` en cada push/PR
  a `develop` y `main`.
- `requirements-docs.txt` (stack MkDocs) y `requirements-dev.txt` (+ ruff, mypy, pytest): la CI y
  los workflows de documentación ya no instalan docling ni torch.
- `tests/test_build_docs_zip.py` (8 tests: script y hook del ZIP) y `tests/test_docs_conformance.py`
  (conformidad de `docs/` con los arquetipos). Cobertura de criterios: 45/67.
- `build_docs_zip.py --builder zensical` ejecuta él mismo los hooks que Zensical ignora:
  `hooks/sync_root_docs.py` antes del build y `mkdocs_hooks.py` (ZIP `latest`) solo si el build
  termina con 0. 4 tests nuevos; criterios AC-07 y AC-08 en `functional/build_docs_zip.md`.
- `check_env.py` avisa si falta `zensical` (generador opcional, `OPTIONAL_DOC_BUILDERS`) y remite a
  `requirements-dev.txt`; no cambia el código de salida. 2 tests nuevos; AC-06 en
  `functional/check_env.md`.
- `tests/test_zensical_compat.py`: guardas para lo que ningún `--strict` detecta. Falla si
  `mkdocs.yml` declara un plugin que Zensical ignoraría en silencio o si los enlaces al ZIP de
  `docs/downloads.md` no resuelven al ZIP `latest`. AC-09 en `functional/build_docs_zip.md`.
- **ADR-003** (PROPUESTO) — Use Zensical as the default documentation generator: cambio
  escalonado con condiciones C1-C5 (Zensical ≥ 0.1, paridad en CI ≥ 2 semanas, revisión visual,
  ZIP `latest` cubierto, antes del fin de vida de Material el 2027-05-05).
- `/document-project` con **Generador = `zensical`**: nueva sección *Reglas por generador: Zensical*
  en `document_project.prompt.md`. Añade la señal `TIENE_PIPELINE_SIN_HOOKS` y el Gap A4 (script de
  build sin pasos pre/post), la comprobación de plugins soportados, el build vía
  `build_docs_zip.py --builder zensical` y la regla de no crear `zensical.toml`. Slash command,
  agentes Generator/Reviewer, `docs.instructions.md` y la norma remiten a ella. AC-08 en
  `functional/document_project.md`. MkDocs Material sigue siendo el generador por defecto para
  destinos.

### Changed

- `build_docs_zip.py` invoca Zensical como `python -m zensical` (antes `zensical` desde el PATH).
- **Mermaid con la integración nativa del tema**: se retiran el CDN `mermaid@11` y
  `docs/assets/js/mermaid.js` de `extra_javascript`. Duplicaban el render: el tema ya pinta cada
  diagrama y el `mermaid.run()` propio dejaba un SVG de error oculto en cada bloque. La pieza
  imprescindible es `custom_fences: mermaid`. Fase 0b y Fase 5 de `/document-project` pasan de 4 a
  3 assets (si un destino tiene el CDN o `mermaid.js`, se retiran). Norma §4.1,
  `docs.instructions.md`, plantilla `TEMPLATE_mkdocs.yml`, agentes, `CLAUDE.md`, `CONTRIBUTING.md`
  y `EDGE_CASES` § Mermaid actualizados. Verificado en navegador (Edge headless + CDP): 23/23
  diagramas visibles con MkDocs y con Zensical, en claro y en oscuro.
- CI: build de paridad con Zensical (`build_docs_zip.py --builder zensical`, no bloqueante) que
  verifica además el ZIP `latest`. `zensical==0.0.73` fijado en `requirements-dev.txt` y
  `requirements.txt` (con `deepmerge` y `tomli`). El resultado real se publica como anotación
  `Paridad Zensical` (OK/FALLO), porque `continue-on-error` marca el paso como `success` aunque falle.
- Workflows: `actions/checkout` y `actions/setup-python` v4 → v7, `actions/upload-artifact` v4 → v7 y
  `softprops/action-gh-release` v2 → v3 (Node 24 nativo; GitHub ya no admite Node 20 en los runners).
- Norma del Arquetipo 1 alineada con su prompt (8 secciones); las páginas con la estructura v1
  siguen siendo válidas en transición.
- Prompt del Arquetipo 2 alineado con la norma (§2 "Modelo de Datos / Contratos"); la directiva
  autodoc solo se usa si el generador tiene mkdocstrings.
- Material `CONTRATO` alimenta también el Arquetipo 12 §5; `INFRAESTRUCTURA` va a 6C §3 › Despliegue.
- `/document-project`: la **Fase 0b** es siempre la sincronización visual (ahora también en el prompt
  multiplataforma); la conversión de documentos a Markdown pasa a llamarse **Fase 0c**.
- Bootstrap: ruta de la guía de Codex corregida (`docs/guides/codex_guide.md`); la Capa B incluye los
  Arquetipos 7, 8, 10 y 12 y ofrece `scripts/doc_trace.py` como tooling opcional.
- `.claude/settings.json.example`: añadido el hook `sync_root_docs.py` como primer PostToolUse.
- `DOCUMENTATION_STANDARD.md` §4.2: la copia del `nav` se sustituye por una referencia a `mkdocs.yml`.
- El sitio no se publica en GitHub Pages: `site_url` solo fija la URL canónica (sitemap y `llms.txt`).
- mypy limpio sin los extras opcionales (overrides para `docling` y `markitdown`).
- `CONTRIBUTING.md`: la sincronización visual pasa a §5.1 y «Release» vuelve a ser §6 (Arquetipo 11).
- `docs/installation.md`: corregido que `requirements.txt` no incluye ruff ni mypy.
- `requirements.txt` regenerado desde el entorno local completo (docling 2.107.0, markitdown con
  plugins PDF/XLS); `pywin32` solo en Windows (`sys_platform == "win32"`), lo que permite instalarlo
  en Linux/macOS. `requirements-docs.txt` y `requirements-dev.txt` alineados con sus versiones.
- `check_env.py`: la ayuda de plugins de markitdown incluye `pdfminer.six`.
- `doc_trace.py stamp --source`: `CLAUDE.md`, la norma §3.16 y las páginas `api`/`reference` aclaran que
  `--source` sustituye la lista entera de fuentes; para re-sellar se usa `stamp <página>` sin él.

### Fixed

- `docs/architecture.md`: el diagrama de Runtime mostraba «Syntax error in text». El nodo
  `B[/document-project…]` abre un paralelogramo en Mermaid 11; pasa a `B[Comando document-project…]`.
  Nuevo test `test_mermaid_nodes_do_not_start_with_slash` (`--strict` no detecta este error).
- `convert_to_md.py --device auto` detecta la GPU: el `CUDA_VISIBLE_DEVICES=""` que el módulo
  fija al importarse ya no se confunde con una elección del usuario.
- `convert_to_md.py` con docling ya no recoge los `.md` del origen: el Markdown ya es legible y
  se reconvertía a `md/` sin necesidad.
- `check_env.py` ya no se interrumpe con `UnicodeEncodeError` al mostrar avisos en una consola
  Windows (cp1252): la salida se reconfigura a UTF-8.
- `convert_to_md.py --metadata` con docling escribe la versión real del motor en `engine_version`
  (antes siempre `unknown`: docling no expone `__version__`).

## [0.1.0] — 2026-06-10

### Added

- **Tooling determinista**: `scripts/check_env.py` (verificación de herramientas del entorno) y
  `scripts/build_docs_zip.py` (ZIP offline con SHA256 y checksums).
- **Bootstrap multiplataforma** (`.github/agents/`, `.github/prompts/`, `.claude/commands/`):
  replica el sistema de instrucciones IA en proyectos destino mediante modelo PULL.
- **Flujo `/document-project`** como comando de entrada único para documentar proyectos:
  validación obligatoria de inputs, inventario por fases, orquestación de arquetipos.
- **Soporte de orígenes heterogéneos** en `/document-project`: Fase 0a de clasificación
  (`CÓDIGO`, `NORMATIVA`, `ESPECIFICACIÓN`, `UI/PANTALLAS`, `REFERENCIA`); estrategias
  `federado`, `hub+satélite` y `monorepo` para múltiples orígenes de código.
- **11 arquetipos formales** de documentación con estructura fija y audiencia definida:
  - 1 — Funcional, 2 — Técnica/API, 3a — How-to (Diátaxis), 3b — Tutorial (Diátaxis),
    4 — Ejemplos de Código, 5 — ADR/MADR 4.0, 6 — Navegación Principal (Variantes A–D),
    7 — Onboarding Dev, 8 — Trazabilidad Normativa (condicional),
    9 — Changelog, 10 — Config Agente IA, 11 — Guía de Contribución.
- **Documentación completa de doc_ia** (dogfooding): 24 páginas en `docs/` cubriendo
  funcional, técnica, ejemplos, guías, arquitectura y ADRs para todos los módulos.
- **Descarga de documentación offline**: `dist/doc_ia-docs-{version}.zip` + SHA256; workflow
  GitHub Actions `docs-zip-release.yml` publica automáticamente en cada release.
- **UX del sitio**: márgenes, sidebar toggle, soporte Mermaid 11, tabs sticky.
- **Estados A/B/C** en el inventario de `/document-project` para distinguir páginas
  a crear, actualizar u omitir.

### Fixed

- Restauración de 10 ficheros de la Capa A corruptos durante el bootstrap inicial.
- Restauración de `config-reviewer.agent.md` y creación de `docs.instructions.md`
  tras corrupción del bootstrap.

[Unreleased]: https://github.com/fmanza/doc_ia/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/fmanza/doc_ia/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/fmanza/doc_ia/compare/docs-v0.1.0...v0.2.0
[0.1.0]: https://github.com/fmanza/doc_ia/releases/tag/docs-v0.1.0
