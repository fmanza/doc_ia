# PLAN + AUDIT_PLAN por fases — Migración MkDocs → Zensical

## Solicitud
"Queremos un PLAN y AUDIT_PLAN. Empezamos ya y preparamos el siguiente paso para actualizar a
Zensical 0.1. Quiero todos por fases independientes y con su commit".

## Decisiones del usuario (2026-10-28)
- **D1** — Empezar ya (Zensical 0.0.73 fijado) sin esperar a 0.1; dejar preparado el salto a 0.1.
- **D2/D3/D4** — "Todos": M2 (ZIP offline real), M3 (Mermaid nativo) y la Etapa 3 (producto) entran
  en el plan como fases propias.
- **Una fase = un commit** (Conventional Commits), revertible con `git revert <sha>` sin romper la CI.

## Evidencia añadida respecto a `01_PLAN_AUDIT.md`
- **M2 con MkDocs en Windows: no viable.** `offline` + `privacy` con Material 9.8.0 →
  `Aborted with 78 warnings in strict mode` (`Couldn't create symbolic link` × 39 por
  `iframe-worker/shim` y por Google Fonts). Con Zensical 0.0.73 el mismo `mkdocs.yml` construye sin
  avisos. ⇒ M2 solo después de que Zensical sea el generador por defecto (F10).
- Con `offline`, ambos generadores pasan a URLs `*.html`: el enlace
  `../doc_ia-docs-latest.zip` de `docs/downloads.md` sale fuera de `site/` y deja de funcionar.
- `privacy` crea `.cache/` en la raíz (no está en `.gitignore`).

---

## Reglas comunes a todas las fases

### Definición de hecho (DoD), en local, antes de cada commit
```bash
python -m ruff check scripts tests hooks
python -m ruff format --check scripts tests hooks
python -m mypy scripts
python -m pytest
python scripts/doc_trace.py drift          # 0 páginas desactualizadas (bloqueante en CI)
python scripts/doc_trace.py matrix
python scripts/doc_trace.py llms --check
python -m mkdocs build --strict
python scripts/build_docs_zip.py --builder zensical --output-dir <tmp>   # a partir de F2
```
- Toda página cuyo frontmatter `fuentes:` cite un fichero tocado se **re-sella** en el mismo commit
  (`doc_trace.py stamp`). Al tocar una página funcional, re-sellar también `docs/functional/index.md`.
- Si cambia `mkdocs.yml`: re-sellar `api/archetypes.md`, `api/document_project.md`,
  `functional/build_docs_zip.md` y `reference/index.md`, y regenerar `docs/llms.txt` si cambia el nav.
- Entrada en `CHANGELOG.md` › `[Unreleased]` (nunca en `docs/changelog.md`).
- Fila de la fase en `TRACEABILITY.md` de esta sesión con el SHA del commit.
- Todos los commits llevan el trailer `Co-Authored-By` acordado. Sin `push` salvo que se pida.

### Grafo de dependencias
```text
F0 ─┐
F1 ──► F2 ──► F7 [gate: Zensical 0.1 en PyPI] ──► F8 [gate: C2-C5] ──► F9
                                                             ├──► F10 (M2)
F1 ──► F11 ───────────────────────────────────────────────────┴──► F12
F3, F4, F5, F6 (M3): independientes entre sí y de F1
```
"Independiente" significa: el commit compila y pasa la DoD por sí solo, y revertirlo no rompe
fases posteriores **salvo** las que dependen de él según el grafo.

---

## BLOQUE A — Etapa 1: "Zensical-ready" (ahora; MkDocs sigue por defecto)

### F0 · Plan de la sesión
- **Ficheros**: `.ai/sessions/2026-10-28d_zensical_migration/{01_PLAN_AUDIT,02_PLAN_FASES,TRACEABILITY}.md`, `.ai/sessions/INDEX.md`.
- **Commit**: `docs(session): plan por fases de la migración a Zensical`
- **AUDIT**: sin riesgo (solo artefactos de sesión). **GO**.

### F1 · Pipeline de build sin hooks para Zensical (M1)
- **Objetivo**: `build_docs_zip.py --builder zensical` reproduce lo que hacen los hooks de MkDocs.
- **Ficheros**:
  - `scripts/build_docs_zip.py`:
    - `HOOKLESS_BUILDERS = frozenset({"zensical"})`.
    - Pre-build: `sync_root_docs.main()`.
    - Build: `[sys.executable, "-m", "zensical", "build"]` + `--strict` según el flag (no `zensical` por PATH).
    - Post-build, **solo si el build devuelve 0**: `mkdocs_hooks.on_post_build({"site_dir": ...})`.
    - Los módulos de la raíz (`mkdocs_hooks.py`, `hooks/sync_root_docs.py`) se cargan por ruta con
      `importlib.util.spec_from_file_location`, porque al ejecutar `python scripts/...` la raíz no está
      en `sys.path`. Rama `mkdocs` sin cambios.
  - `tests/test_build_docs_zip.py`:
    - Orden pre → build → post.
    - Sin post (ni ZIP latest) si el build falla.
    - El comando usa `sys.executable -m zensical`.
    - La rama `mkdocs` no ejecuta pre/post.
    - Todo con `subprocess` mockeado, sin Zensical instalado.
  - `docs/api/build_docs_zip.md`, `docs/functional/build_docs_zip.md` (+ criterio AC nuevo con
    test), `docs/reference/index.md`, `docs/examples/build_docs_zip_offline.md` → re-sellado.
  - `.claude/EDGE_CASES.md`: "[Zensical] `hooks:` se ignora en silencio".
- **Commit**: `feat(build): pipeline sin hooks para construir con Zensical`
- **AUDIT**:
  - Riesgo T: carga por ruta de módulos fuera de `scripts/` → mypy strict necesita tipar el
    `ModuleType`; cubrir con test que use el `ROOT` parcheado.
  - Riesgo F: sync en pre-build modifica `docs/changelog.md` (ya versionado, idempotente).
  - LSP: CLI intacta.
  - **GO**.

### F2 · Paridad Zensical en CI (depende de F1)
- **Ficheros**:
  - `requirements-dev.txt`: `zensical==0.0.73`.
  - `requirements.txt`: `zensical==0.0.73`, `deepmerge==4.0.0`.
  - `.github/workflows/ci.yml`: paso "Build Zensical (paridad, no bloqueante)" →
    `python scripts/build_docs_zip.py --builder zensical --output-dir "$RUNNER_TEMP/zdist"` con
    `continue-on-error: true` + verificación de que existe `site/doc_ia-docs-latest.zip`.
  - `docs/reference/index.md` re-sellado si cambia algo citado.
- **Commit**: `ci(docs): build de paridad con Zensical (no bloqueante)`
- **Preparación de F7**: la versión de Zensical vive en un solo sitio por fichero de requisitos;
  el salto a 0.1 es un cambio de una línea.
- **AUDIT**:
  - T1 (alfa): versión exacta; `continue-on-error` evita que una regresión de Zensical bloquee
    `develop`.
  - S2: nueva dependencia de supply chain, solo en dev/CI.
  - **GO**.

### F3 · `check_env` informa de Zensical (opcional)
- **Ficheros**: `scripts/check_env.py` (aviso informativo si falta, como `docling`),
  `tests/test_check_env.py`, `docs/api/check_env.md`, `docs/functional/check_env.md` (+ re-sellar
  `functional/index.md`), `docs/reference/index.md`.
- **Commit**: `feat(env): check_env informa de Zensical como generador opcional`
- **AUDIT**:
  - No cambia `REQUIRED_TOOLS` ni el código de salida (contrato intacto).
  - Respeta el fix `82ec5f0` (UTF-8 en consola Windows).
  - **GO**.

### F4 · Guardas de conformidad para Zensical (M5)
- **Ficheros**: `tests/test_docs_conformance.py` con dos tests nuevos:
  - Todo plugin de `mkdocs.yml` ∈ `ZENSICAL_SUPPORTED_PLUGINS` (lista mínima documentada con la URL
    de zensical.org/compatibility/plugins).
  - Los enlaces al ZIP de `docs/downloads.md` coinciden con el nombre que produce `mkdocs_hooks.py`.
  - Re-sellar `api/archetypes.md` y `functional/archetypes.md` (+ `functional/index.md`).
- **Commit**: `test(docs): guardas de compatibilidad con Zensical`
- **AUDIT**:
  - La lista de plugins hay que mantenerla a mano (se revisa en F7).
  - Sin red.
  - **GO**.

### F5 · ADR-003 (PROPUESTO)
- **Ficheros**: `docs/adr/ADR-003-zensical-por-defecto.md` (MADR 4.0, "Use Zensical as the default
  documentation generator", estado PROPUESTO, con condiciones C1-C5); `mkdocs.yml` (nav);
  `docs/llms.txt`; re-sellados por cambio de `mkdocs.yml`; enlace desde ADR-001 ("ver ADR-003").
- **Commit**: `docs(adr): ADR-003 Zensical como generador por defecto (propuesto)`
- **AUDIT**: el cambio de `mkdocs.yml` provoca drift en 4 páginas (`EDGE_CASES § doc_trace`), que se
  re-sellan en el mismo commit. **GO**.

### F6 · Mermaid solo nativo (M3)
- **Objetivo**: quitar la doble carga de Mermaid (CDN `mermaid@11` + `assets/js/mermaid.js` además
  de la integración nativa del tema). Funciona igual con ambos generadores.
- **Ficheros**:
  - doc_ia:
    - `mkdocs.yml`: retirar CDN y `assets/js/mermaid.js` de `extra_javascript`.
    - Borrar `docs/assets/js/mermaid.js`.
    - `mermaid.css` se conserva.
  - Producto (regla de Fase 0b, 4 → 3 assets):
    - `.claude/commands/document-project.md`
    - `.github/prompts/document_project.prompt.md` (Fase 0b y Fase 5)
    - `.github/agents/documentation-generator.agent.md`
    - `.github/DOCUMENTATION_STANDARD.md` §4.1
    - `.github/instructions/docs.instructions.md`
    - `CLAUDE.md` (Fase 0b)
    - `.claude/EDGE_CASES.md`
    - Si un destino ya tiene `mermaid.js` + CDN, se tolera (no es un error); en destinos nuevos no se
      añade.
  - Re-sellados: `api/document_project.md`, `functional/document_project.md`, `api/archetypes.md`,
    `functional/archetypes.md`, `functional/origin_types.md`, `functional/index.md`,
    `reference/index.md`.
- **Commit**: `refactor(docs): Mermaid con la integración nativa del tema`
- **AUDIT**:
  - **Riesgo F alto**: revierte la decisión del hotfix `2026-06-12a` (Mermaid no se renderizaba en
    socyalpro). La RCA de entonces atribuyó el fallo a la falta de CDN, pero con
    `custom_fences: mermaid` el tema carga Mermaid por sí mismo.
  - El modo oscuro debería mejorar (el `mermaid.js` propio fija `theme: 'default'`).
  - **GO_CONDICIONAL**:
    - **C6**: verificación en navegador de los 3 diagramas de `architecture` y de un diagrama por
      tipo (flowchart, sequence, ER), en claro y oscuro, con MkDocs y con Zensical, sirviendo
      `site/` por HTTP.
    - **C7**: reproducir el caso de socyalpro (mkdocs.yml sin CDN pero con `custom_fences`) y
      confirmar que renderiza.

---

## BLOQUE B — Etapa 2: Zensical 0.1 y cambio de generador por defecto

### F7 · Actualizar a Zensical 0.1.x (gate: 0.1 publicada en PyPI; anunciada para el 2026-11-05)
- **Runbook** (mecánico, preparado por F2):
  1. Leer las notas de versión 0.1 (breaking changes, plugins, `hooks`, `--strict`, Module API).
  2. `zensical==0.1.x` en `requirements-dev.txt` y `requirements.txt` (+ dependencias nuevas
     según `pip install`).
  3. Revisar `ZENSICAL_SUPPORTED_PLUGINS` (F4) y `EDGE_CASES` (¿siguen sin soportarse los hooks?).
  4. DoD completa + comparación con el spike: 39 páginas, `diff` de rutas vacío, ZIP latest presente.
  5. Si 0.1 ya soporta `hooks:` → anotarlo en ADR-003; F1 se mantiene (es agnóstico).
- **Commit**: `build(deps): Zensical 0.1.x`
- **AUDIT**: riesgo de breaking changes en la propia 0.1 → mitigado porque la paridad no bloquea la
  CI. **GO_CONDICIONAL** a que 0.1 esté publicada.

### F8 · Zensical como generador por defecto (gate C2-C5; depende de F1, F2, F7)
- **Ficheros**:
  - Tooling:
    - `scripts/build_docs_zip.py`: `--builder` por defecto `zensical`.
    - `scripts/check_env.py`: `REQUIRED_TOOLS` pasa de `mkdocs` a `zensical`.
    - Tests de ambos.
  - Dependencias:
    - `requirements-docs.txt`: `zensical` + `PyYAML` explícito (lo importa `doc_trace.py`).
      `mkdocs`/`mkdocs-material` pasan a `requirements-dev.txt` para el fallback.
    - Comentario de PyYAML en `scripts/doc_trace.py`.
  - CI y workflows:
    - `ci.yml`: Zensical bloqueante; MkDocs pasa a paridad no bloqueante hasta 2027-05-05.
    - `docs-release.yml` y `docs-zip-release.yml`: `build_docs_zip.py --builder zensical`; el
      segundo deja de llamar a `mkdocs build` directamente.
  - Entorno local: `.vscode/tasks.json`.
  - ADRs: ADR-003 pasa a ACEPTADO; ADR-001 pasa a `REEMPLAZADO POR ADR-003` (vocabulario MADR de `architecture_doc.prompt.md`).
  - Re-sellados.
- **Commit**: `feat(build)!: Zensical como generador por defecto`
  - Pie del commit: `BREAKING CHANGE: build_docs_zip.py usa zensical por defecto`.
- **AUDIT**:
  - Cambio del default de la CLI (impacto LSP en el contrato de `--builder` → BREAKING declarado).
  - Rollback = revertir el commit.
  - **GO_CONDICIONAL** a:
    - **C2**: paridad en verde ≥ 2 semanas.
    - **C3**: revisión visual.
    - **C4**: ZIP latest cubierto por test (F1).
    - **C5**: antes de 2027-05-05.

### F9 · Instrucciones y docs de doc_ia alineadas (depende de F8)
- **Ficheros**:
  - Instrucciones:
    - `.github/SHARED_INSTRUCTIONS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`,
      `.cursorrules`.
    - `.github/instructions/{docs,sync,python}.instructions.md`.
    - `.ai/{runtime,architecture,product,standards,glossary}.md`.
  - Docs: `docs/{index,installation,quickstart,architecture,downloads}.md`,
    `docs/guides/{onboarding_dev,troubleshooting,claude_code_guide,codex_guide}.md`,
    `docs/ai-config/claude.md`.
  - Re-sellados y `llms --check`.
  - Checklist de sincronización de `CLAUDE.md`.
- **Commit**: `docs: comandos y arquitectura con Zensical como generador por defecto`
- **AUDIT**:
  - Solo texto. Los comandos `python -m mkdocs ...` se sustituyen por
    `python scripts/build_docs_zip.py` / `python -m zensical serve`.
  - Se aclara que `zensical serve` no sincroniza los ficheros raíz (riesgo F2 del plan inicial).
  - **GO** tras F8.

### F10 · ZIP realmente offline (M2) (depende de F8)
- **Ficheros**:
  - `mkdocs.yml`:
    - Añadir `- offline` y `- privacy`.
    - `use_directory_urls: false` explícito, para que `doc_trace llms` genere las mismas URLs que
      `offline`.
  - `docs/llms.txt` regenerado.
  - `docs/downloads.md`: enlaces relativos al ZIP sin `../`; texto de búsqueda sin servidor.
  - `.gitignore`: `.cache/`.
  - `.github/workflows/docs-zip-release.yml`: el cuerpo de la release describe el offline real.
  - `extra.polyfills` con `iframe-worker` local solo si se quiere evitar la descarga en el build.
  - **Mermaid ya no forma parte de F10**: lo resolvió la sesión `2026-10-28f_mermaid_local`
    (copia local 12.2.0 en `docs/assets/vendor/mermaid/` + `mermaid-theme.js`, sin depender de
    `privacy`). F10 solo debe comprobar que `offline`/`privacy` no alteran esa configuración.
  - Re-sellados por `mkdocs.yml`.
- **Commit**: `feat(docs): ZIP de documentación navegable sin conexión`
- **AUDIT**:
  - **F**: las URLs pasan a `*.html`. El sitio no se publica (D1 de `2026-10-28c`), así que no hay
    enlaces externos que romper.
  - **S1**: `privacy` descarga recursos de terceros en el build (red en CI, no en tests).
  - **T**: el fallback MkDocs deja de construir en strict en Windows (symlinks) → documentarlo en
    `EDGE_CASES`; la paridad MkDocs en CI (Linux) no se ve afectada.
  - **GO_CONDICIONAL**:
    - **C8**: abrir el ZIP extraído con `file://` y verificar búsqueda, Mermaid y navegación sin
      red.
    - **C9**: CUMPLIDA en la sesión `2026-10-28f_mermaid_local` (24/24 diagramas sin conexión,
      0 SVG de error, MkDocs y Zensical, claro y oscuro). Repetir solo si F10 toca `extra_javascript`.

---

## BLOQUE C — Etapa 3: producto (proyectos destino)

### F11 · Zensical como generador completo en `/document-project` (depende de F1)
- **Objetivo**: hoy `generador = zensical` se acepta como input, pero el patrón offline (señal 2 =
  `mkdocs_hooks.py`) y la Fase 7 asumen MkDocs.
- **Ficheros**: `.github/prompts/document_project.prompt.md`, `.claude/commands/document-project.md`,
  `.github/agents/documentation-generator.agent.md`, `.github/agents/documentation-reviewer.agent.md`,
  `.github/DOCUMENTATION_STANDARD.md`, `.github/instructions/docs.instructions.md`.
  Reglas por generador:
  - **Fase 1**: con `zensical`, la señal 2 pasa a ser "el pipeline de build ejecuta pre/post" (patrón
    F1). `hooks:` se reporta como no efectivo.
  - **Fase 5**: guarda de plugins soportados; `hooks:` como aviso.
  - **Fase 7**: `python -m zensical build --strict`.
  - **Fase 7b**: Gap A2 en variante Zensical (pipeline en lugar de hook).
  - Docs: `api/functional/examples` de `document_project` + re-sellados.
- **Commit**: `feat(prompts): soporte completo de Zensical en document_project`
- **AUDIT**:
  - Superficie amplia de instrucciones → revisar con el agente Documentation Reviewer.
  - No cambia el default para destinos (MkDocs sigue siéndolo).
  - **GO**.

### F12 · Zensical por defecto para proyectos destino (depende de F8 y F11)
- **Ficheros**:
  - Validación de inputs: `document_project.prompt.md` (líneas 17/39) y
    `.claude/commands/document-project.md` (ejemplos).
  - `bootstrap_ai_config.prompt.md` (Capa B).
  - `.github/agents/config-reviewer.agent.md`.
  - `.github/DOCUMENTATION_STANDARD.md` §4.
  - `docs/{functional,api,examples}/bootstrap*`.
  - `docs/functional/archetypes.md`.
  - Re-sellados.
- **Commit**: `feat(prompts)!: Zensical como generador por defecto para proyectos destino`
- **AUDIT**:
  - Afecta a destinos ya documentados (socyalpro, dpss…): la regla debe respetar el generador
    existente del destino y no migrarlo de forma implícita.
  - **GO_CONDICIONAL** a F8 en verde.

### Fuera de este plan
- **F13** (≥ 2027-05-05): retirar el fallback MkDocs (`hooks:` de `mkdocs.yml`, paridad MkDocs en CI,
  `mkdocs*` de requisitos). `mkdocs_hooks.py` se mantiene como plantilla para destinos MkDocs.
- `/version-closure` al terminar el Bloque A y al terminar el Bloque B.

---

## AUDIT_PLAN global

| Riesgo | Nivel | Mitigación | Fase |
|---|---|---|---|
| Pérdida silenciosa (hooks ignorados, plugins ignorados, ZIP ausente) | Alto | Pipeline pre/post + tests + guardas | F1, F4 |
| Zensical alfa con releases cada 3-4 días | Alto | Versión exacta, paridad no bloqueante, salto deliberado a 0.1 | F2, F7 |
| Mermaid deja de renderizar al quitar CDN | Alto | C6/C7 en navegador antes del commit; F6 revertible | F6 |
| Paridad visual no verificada | Medio | C3 antes de F8 | F8 |
| Drift de `doc_trace` bloquea la CI en cada commit | Medio | Re-sellado en el mismo commit (DoD) | Todas |
| `privacy` en Windows con MkDocs (symlinks) | Medio | M2 solo después de F8 | F10 |
| Destinos existentes migrados sin querer | Medio | Respetar el generador del destino | F12 |
| Supply chain (nueva dependencia) | Bajo | Versión exacta, solo dev hasta F8 | F2, F8 |

**Simplificaciones aplicadas**:
- Reutilizar `mkdocs_hooks.on_post_build` y `sync_root_docs.main` (sin duplicar).
- Mantener `mkdocs.yml` (sin `zensical.toml`).
- Separar el cambio de default (F8) de la documentación (F9) para que cada commit sea revisable.

### Veredicto
| Fase | Veredicto | Cuándo |
|---|---|---|
| F0-F5, F11 | **GO** | Ahora |
| F6 | **GO_CONDICIONAL** (C6, C7) | Ahora, con verificación en navegador |
| F7 | **GO_CONDICIONAL** (0.1 en PyPI) | Desde el 2026-11-05 |
| F8 | **GO_CONDICIONAL** (C2-C5) | ≥ 2 semanas de paridad tras F7 |
| F9, F10, F12 | **GO_CONDICIONAL** (F8; F10 además C8) | Tras F8 |

Orden de ejecución propuesto ahora: **F0 → F1 → F2 → F3 → F4 → F5 → F11 → F6**.
