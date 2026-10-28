# PLAN + AUDIT_PLAN — Migración MkDocs → Zensical

## Solicitud
"Actualmente se está usando mkdocs y se quiere migrar a zensical, se requiere valorar el impacto y
que el funcionamiento sea el mismo y proponer mejoras si es necesario. Dime también si es
recomendable la migración. Puede consultarse información en internet. PLAN y AUDIT_PLAN".

Alcance de esta sesión: **solo PLAN + AUDIT_PLAN** (sin IMPLEMENT). El repo no se ha modificado salvo
este artefacto de sesión.

---

## 1. Contexto externo (consultado el 2026-10-28)

| Hecho | Fuente |
|---|---|
| Material for MkDocs en mantenimiento desde 2025-11-05; **fin de vida 2027-05-05** (solo fixes críticos y de seguridad hasta entonces). Última versión 9.8.0 (2026-10-24). | PyPI `mkdocs-material`; blog de Material (2025-11-05) |
| MkDocs 2.0 (anunciado feb-2026) rompe temas, plugins y formato de config (TOML). Material limita `mkdocs<2`. MkDocs 1.6.1 (la fijada aquí) no evoluciona. | Blog de Material "mkdocs 2.0" (2026-02-18) |
| Zensical: MIT, mismo equipo que Material, **alfa** (`Development Status :: 3 - Alpha`), versión 0.0.73 (2026-10-26), releases cada 3-4 días. Python ≥ 3.11. | PyPI `zensical` |
| Anunciado: Zensical 0.1 el **2026-11-05** como inicio de una línea de releases "fiable". | Comunicación del proyecto (no verificado en PyPI todavía) |
| Lee `mkdocs.yml` de forma nativa. **`hooks:` no soportado.** No ejecuta plugins MkDocs arbitrarios; los no listados se **ignoran en silencio**. Module API sin fecha. | zensical.org/compatibility/configuration, /plugins |
| `zensical build --strict` existe (desde 0.0.38) y valida además anclas y referencias. | Release notes v0.0.38; zensical.org/docs/setup/validation |
| Plugins `offline` (búsqueda desde `file://`) y `privacy` (descarga assets externos) soportados. | zensical.org/docs/setup/offline |

## 2. Spike empírico (venv aislado en scratchpad, copia del repo, zensical 0.0.73, Python 3.14, Windows)

| Prueba | MkDocs 1.6.1 + Material 9.8.0 | Zensical 0.0.73 |
|---|---|---|
| `build --strict` tal cual | ✅ OK | ❌ **Falla**: `index.md:74 changelog.md page does not exist` — `hooks/sync_root_docs.py` no se ejecuta |
| `build --strict` tras sync manual | ✅ OK | ✅ OK, "No issues found" |
| Páginas HTML | 39 | 39 (mismas rutas, `diff` vacío) |
| ZIP `site/doc_ia-docs-latest.zip` (+ `.sha256`) | ✅ (vía `mkdocs_hooks.py`) | ❌ **No se genera** — y Zensical no avisa |
| Enlaces de `downloads.md` al ZIP latest (HTML crudo) | resuelven | **rotos en silencio** (ningún strict valida `<a href>` crudo) |
| Tiempo de build | ~9,9 s | ~2,4 s (≈4×) |
| DOM: `md-nav__item--nested` / `md-grid` / `md-tabs__item` / `lang="es"` | 15 / 5 / 14 / es | 15 / 5 / 14 / es → `nav.css` y `sidebar-toggle.js` siguen aplicando |
| Mermaid / pestañas / permalinks | 3 / 1 / 6 | 3 / 1 / 6 |
| `extra_css` / `extra_javascript` | inyectados | inyectados (mismo orden) |
| Emoji `!!python/name:material.extensions.emoji.twemoji` | OK | OK sin `mkdocs-material` instalado |
| Búsqueda | `search/search_index.json` (lunr) | `search.json`, `lang: es` |
| `+ offline + privacy` | — | ✅ strict OK; Mermaid, fuentes e `iframe-worker` vendorizados en `assets/external/`; **URLs pasan a `*.html`** |

Hallazgo colateral: el tema ya integra Mermaid de forma nativa (con `privacy` se descarga
`unpkg.com/mermaid@12`) **además** del `mermaid@11` por CDN + `assets/js/mermaid.js` del proyecto →
doble carga de Mermaid (también ocurre hoy con Material). Y el ZIP "offline" actual depende de CDN
para Mermaid aunque la release de GitHub anuncia "Mermaid diagrams (rendered)" offline.

No verificado: paridad **visual** (capturas en claro/oscuro, toggle de sidebar), `zensical serve`
con recarga, y el build en Linux/CI con Python 3.12.

---

## PLAN

### Objetivo
Migrar el builder del sitio de doc_ia de MkDocs + Material a Zensical **sin pérdida funcional**
(sync de ficheros raíz, ZIP latest + SHA256, ZIP versionado, build estricto, `llms.txt`, assets
visuales), por etapas y con MkDocs como red de seguridad hasta su fin de vida.

### Alcance in / out
- **In (E1-E2)**: sitio propio de doc_ia, tooling (`build_docs_zip.py`, `check_env.py`), CI y
  workflows, documentación e instrucciones que describen el builder de doc_ia, ADR.
- **Out (E3, sesión aparte)**: cambiar el generador **recomendado a proyectos destino** en
  `document_project` / Documentation Generator / bootstrap (patrón offline de 3 señales, Fase 0b).
  Es producto, no infraestructura, y toca ~30 ficheros de instrucciones.
- **Out**: migrar a `zensical.toml` (se mantiene `mkdocs.yml` como fuente única; `doc_trace.py` lo
  parsea y Zensical lo lee nativamente).

### Etapa 1 — "Zensical-ready" (MkDocs sigue por defecto) · `/new-feature`
Saca la lógica de los hooks a un paso agnóstico del builder.

| Fichero | Cambio |
|---|---|
| `scripts/build_docs_zip.py` | Con `--builder zensical`: (1) pre-build `hooks/sync_root_docs.main()`; (2) build con `sys.executable -m zensical build [--strict]` (no `zensical` por PATH: mismo fallo que `EDGE_CASES § plugin MkDocs`); (3) post-build `mkdocs_hooks.on_post_build({"site_dir": ...})` **solo si el build devuelve 0** (resuelve de paso el edge case "ZIP latest con build fallido" para este builder). |
| `mkdocs_hooks.py`, `hooks/sync_root_docs.py` | Sin cambios de comportamiento (siguen siendo plantilla copiable para destinos y hooks de MkDocs; Zensical los ignora). |
| `scripts/check_env.py` | Informar `zensical` como herramienta opcional (no requerida en E1). |
| `requirements-dev.txt` | `zensical==<versión exacta>` (no en `requirements-docs.txt` todavía). |
| `.github/workflows/ci.yml` | Paso "Build Zensical (paridad)" vía `build_docs_zip.py --builder zensical --output-dir <tmp>` con `continue-on-error: true`. |
| `tests/test_build_docs_zip.py` | Rama zensical: orden pre → build → post, sin post si build ≠ 0, comando con `sys.executable -m`. Subprocess mockeado (sin red). |
| `tests/test_docs_conformance.py` | Guarda: todo plugin de `mkdocs.yml` ∈ lista de plugins soportados por Zensical (evita el "ignorado en silencio"). |
| `docs/adr/ADR-003-zensical-por-defecto.md` | MADR 4.0, estado PROPUESTO, "Use Zensical as the default documentation generator". |
| `docs/reference/index.md`, `docs/api/build_docs_zip.md`, `docs/functional/build_docs_zip.md`, `docs/guides/troubleshooting.md`, `.claude/EDGE_CASES.md` | Documentar pre/post del pipeline Zensical y el caso "hooks ignorados en silencio". `doc_trace.py stamp` tras editar. |

### Etapa 2 — Cambio de builder por defecto · `/refactor` + `/version-closure`
Solo cuando se cumplan las condiciones de AUDIT_PLAN (C1-C5).

| Fichero | Cambio |
|---|---|
| `requirements-docs.txt` / `requirements.txt` | `zensical==X.Y.Z` fijado; retirar `mkdocs`, `mkdocs-material`, `mkdocs-material-extensions`; fijar `PyYAML` explícito (lo importa `doc_trace.py`). |
| `scripts/build_docs_zip.py` | `--builder` por defecto `zensical`; `mkdocs` se conserva como fallback hasta 2027-05-05. |
| `scripts/check_env.py` | `REQUIRED_TOOLS`: `mkdocs` → `zensical`. |
| `.github/workflows/{ci,docs-release,docs-zip-release}.yml` | Build con `build_docs_zip.py --builder zensical` (el de `docs-zip-release` hoy llama a `mkdocs build` directo + `--no-build`). |
| `mkdocs.yml` | Mantener; `hooks:` se retira cuando se retire el fallback MkDocs. |
| `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.cursorrules`, `.github/SHARED_INSTRUCTIONS.md`, `.github/instructions/{docs,sync}.instructions.md`, `.ai/{runtime,architecture}.md`, `.vscode/tasks.json` (tareas `docs: build` / `docs: serve`) | Comandos `python -m mkdocs build/serve` → `python scripts/build_docs_zip.py` / `python -m zensical serve`. |
| `docs/` (installation, quickstart, architecture, onboarding_dev, downloads, api/functional/examples de build_docs_zip, ADR-001 → SUSTITUIDO) | Actualizar + `doc_trace.py stamp` + `llms --check`. |
| `CHANGELOG.md` | Entrada `feat(docs)!:` o `build(docs):` según impacto. |

### Etapa 3 — Producto (sesión independiente, fuera de este plan)
Generador por defecto para proyectos destino, variante Zensical del patrón offline (sin
`mkdocs_hooks.py`), Fase 0b y bootstrap.

### Mejoras propuestas (independientes del cambio de default; cada una opt-in)
| # | Mejora | Beneficio | Coste / riesgo |
|---|---|---|---|
| M1 | Pipeline pre/post fuera de hooks (E1) | Builder-agnóstico; ZIP latest solo si el build pasa | Bajo — **necesaria** para la paridad |
| M2 | ZIP realmente offline con `offline` + `privacy` (solo Zensical) | Búsqueda sin servidor desde `file://`; Mermaid y fuentes sin CDN; corrige la promesa falsa de la release | URLs pasan a `*.html` → hay que alinear `use_directory_urls` con `doc_trace llms` y con los enlaces de `downloads.md`; `offline` no admite toggle por entorno |
| M3 | Mermaid solo nativo (retirar CDN `mermaid@11` + `assets/js/mermaid.js`) | Elimina doble carga y una dependencia CDN | Cambia la regla obligatoria de Fase 0b (4 assets) → toca producto; verificar render y tema oscuro |
| M4 | Paso CI de paridad Zensical (E1) | Detecta regresiones de la alfa antes del cambio | Bajo |
| M5 | Guarda de plugins soportados (E1) | Evita pérdidas silenciosas | Bajo; la lista hay que mantenerla |
| M6 | Validación estricta de anclas/referencias de Zensical | Más enlaces rotos detectados que con MkDocs | Puede aflorar avisos nuevos (hoy: 0) |

---

## AUDIT_PLAN

### Riesgos funcionales
- **F1 (alto)** — Pérdida silenciosa de funcionalidad: Zensical ignora `hooks:` sin avisar →
  `docs/changelog.md`/`contributing.md` desfasados y ZIP latest ausente con enlaces de
  `downloads.md` rotos que ningún `--strict` detecta. Mitigación: M1 + test de que el pipeline
  produce `site/doc_ia-docs-latest.zip(.sha256)`.
- **F2 (medio)** — `zensical serve` no ejecuta el sync. Mitigado en parte: el PostToolUse de Claude
  ya sincroniza tras cada Edit/Write y los ficheros generados están versionados. Documentarlo.
- **F3 (medio)** — Paridad visual no verificada (solo DOM). Condición C3.
- **F4 (bajo)** — M2 cambia URLs (`*.html`): impacta `llms.txt`, `sitemap.xml` y `downloads.md`.
  El sitio no se publica (decisión D1 de `2026-10-28c`), lo que reduce el impacto.

### Riesgos técnicos
- **T1 (alto)** — Zensical en alfa (0.0.x, release cada 3-4 días): cambios de comportamiento entre
  parches. Mitigación: versión exacta, actualizaciones deliberadas, paso de paridad en CI.
- **T2 (medio)** — Sin API de módulos ni hooks, la extensibilidad futura queda limitada a lo que
  ofrezca Zensical o a pasos pre/post en scripts.
- **T3 (bajo)** — Material/MkDocs: sin features nuevas, pero estable y fijado (`mkdocs==1.6.1`,
  Material limita `mkdocs<2`) → no hay presión técnica inmediata; la fecha límite real es 2027-05-05.
- **T4 (bajo)** — `doc_trace.py` depende de PyYAML que hoy llega con mkdocs; con Zensical también
  llega (verificado), pero conviene fijarlo explícitamente (E2).
- **LSP/ISP** — `build_docs_zip.py` mantiene su CLI (`--builder`, `--no-strict`, `--no-build`,
  `--output-dir`); solo cambia el default en E2. Ejecución síncrona (subprocess), sin cambio de
  contratos sync/async. `mkdocs_hooks.on_post_build(config)` se reutiliza con la misma firma.

### Riesgos de seguridad
- **S1** — `privacy` descarga recursos de terceros en el build: aceptable (mismo origen que hoy el
  navegador del usuario), pero introduce red en el build → no aplicarlo en tests (`pytest` sin red).
- **S2** — Nueva dependencia de supply chain: fijar versión exacta y, si se usa
  `pip install --require-hashes` en el futuro, incluirla.
- Sin credenciales ni servicios IA: principios del proyecto intactos.

### Simplificaciones posibles
- Reutilizar `mkdocs_hooks.on_post_build` y `sync_root_docs.main` en vez de duplicar lógica.
- No migrar a `zensical.toml` (Zensical lee `mkdocs.yml`; mantiene fuente única y `doc_trace`).
- Separar producto (E3) de infraestructura (E1-E2): reduce el diff a ~15 ficheros por etapa.

### Condiciones para pasar de E1 a E2
- **C1** — Zensical ≥ 0.1 publicado y fijado (versión exacta en `requirements-*.txt`).
- **C2** — Paso de paridad Zensical en verde en CI (3.12 y 3.14) durante ≥ 2 semanas.
- **C3** — Revisión visual claro/oscuro de 5 páginas representativas (index, architecture con
  Mermaid, api con tablas, examples con pestañas, downloads) + toggle de sidebar.
- **C4** — `site/doc_ia-docs-latest.zip` y `.sha256` generados por el pipeline y test que lo cubre.
- **C5** — Ejecutar E2 antes de 2027-05-05 (EOL de Material).

### Veredicto
- **Etapa 1**: **GO** (bajo riesgo, no cambia el default, aporta M1/M4/M5 y verificación continua).
- **Etapa 2**: **GO_CONDICIONAL** a C1-C5.
- **Etapa 3**: fuera de alcance; requiere su propio PLAN.

### ¿Es recomendable migrar?
**Sí, pero por etapas y no como cambio de default inmediato.** Razones a favor: Material llega a
fin de vida el 2027-05-05, MkDocs 1.x no evoluciona y MkDocs 2.0 es incompatible con el stack
actual; Zensical lee el mismo `mkdocs.yml` y el spike muestra paridad de contenido y DOM con un build
~4× más rápido y validación más estricta. Razones para no hacerlo ya: está en alfa, no soporta hooks
(de los que dependen el sync y el ZIP latest) y las pérdidas son silenciosas. El riesgo de quedarse
en MkDocs hasta mediados de 2027 es bajo (versiones fijadas), así que no hay urgencia.

### Decisiones pendientes del usuario
- **D1** — ¿Arrancar E1 ahora o esperar a Zensical 0.1 (anunciado 2026-11-05)?
- **D2** — ¿Incluir M2 (ZIP offline real con `offline` + `privacy`) en E2?
- **D3** — ¿Incluir M3 (Mermaid solo nativo)? Implica tocar la regla de Fase 0b (producto).
- **D4** — ¿Planificar E3 (generador por defecto para proyectos destino) como sesión aparte?
