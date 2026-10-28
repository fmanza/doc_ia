# Changelog

Todos los cambios notables de este proyecto se documentan aquí.
Formato: [Keep a Changelog](https://keepachangelog.com/) · Versioning: [SemVer](https://semver.org/)

## [Unreleased]

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

### Changed

- `build_docs_zip.py` invoca Zensical como `python -m zensical` (antes `zensical` desde el PATH).
- CI: build de paridad con Zensical (`build_docs_zip.py --builder zensical`, no bloqueante) que
  verifica además el ZIP `latest`. `zensical==0.0.73` fijado en `requirements-dev.txt` y
  `requirements.txt` (con `deepmerge` y `tomli`).

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

### Fixed

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

[Unreleased]: https://github.com/fmanza/doc_ia/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/fmanza/doc_ia/releases/tag/v0.1.0
