# PLAN + AUDIT_PLAN — Paridad Zensical rota, F7 (Zensical 0.1.1) y Zensical como estándar único

## Situación (2026-11-12)
- Zensical en PyPI: 0.1.0 (2026-11-05) y 0.1.1 (2026-11-10). El repo sigue en `zensical==0.0.73`.
- CI: todos los runs `success`, pero la anotación «Paridad Zensical» dice `FALLO (3.12/3.14)` en
  cada run desde `0ca9613` (v0.7.0, 2026-11-04 16:08). Último OK: `2871cca` (2026-11-04 12:11).
- Error: `build_docs_zip.py` (comprobación de sitio sin servidor) →
  `404.html: link to a folder /doc_ia/` (×2).

## Decisión del usuario (2026-11-12) — D4
**Zensical es el generador estándar de doc_ia, para doc_ia y para los proyectos destino, y MkDocs
queda fuera.** Se abandona el escalonado del ADR-003:
- No hay periodo de paridad antes de decidir: la decisión ya está tomada y C2 y C5 desaparecen.
- No hay fallback MkDocs hasta 2027-05-05: F13 se adelanta y se une a F8.
- F12 cambia: en lugar de «respetar el generador del destino», los destinos MkDocs se migran.

## Spike (scratchpad; repo sin cambios)
1. **Reproducido en local** con 0.0.73 (exit 1, mismo mensaje).
2. **Causa raíz**: `adb2825` añadió `navigation.indexes` y movió `index.md` dentro de la sección
   «Inicio». Desde entonces el tema calcula el enlace del **logo** (cabecera `md-header__button` y
   menú lateral `md-nav__button`) como URL de carpeta. En `2871cca` era `index.html`.
3. **El fallo no es solo de Zensical ni solo del 404.** Enlaces a carpeta en `site/`
   (66 páginas):

   | Generador | Portada | Subpáginas (58) | 404 | Detectado por la comprobación |
   |---|---|---|---|---|
   | MkDocs | `.` | `..` | `/doc_ia/.` | No |
   | Zensical 0.0.73 / 0.1.1 | `""` | `./..` | `/doc_ia/` | Solo el 404 |

   Con `file://`, `.`, `..` y `./..` abren un listado de carpeta: **el logo está roto en el ZIP
   publicado desde v0.7.0** (también en el de MkDocs). La comprobación solo detecta URLs que
   terminan en `/`. `""` es el propio documento y sí funciona.
4. **Arreglo verificado**: `extra.homepage: index.html` → el logo apunta a `index.html`,
   `../index.html` o `/doc_ia/index.html` con los dos generadores. Quedan 0 enlaces a carpeta y
   `build_docs_zip.py --builder zensical` sale con exit 0 (0.1.1).
5. **Zensical 0.1.1**:
   - Build `--strict` OK, mismas 66 rutas HTML que MkDocs (`diff` vacío) y ZIP `latest` creado.
   - Dependencias: `zensical-ui==0.0.42` (nuevo; el tema y el bundle JS se mueven ahí),
     `pymdown-extensions`, `pyyaml`, `jinja2`, `markdown`.
   - `test_theme_bundle_uses_global_mermaid[zensical]` falla porque busca el bundle en
     `zensical/`. El cargador sigue igual en `zensical_ui`.
   - El resto de la suite pasa con 0.1.1.
   - La clave `hooks:` **sigue ignorándose** en silencio.
6. **Superficie MkDocs** (`git grep`, sin sesiones ni changelog):
   - 67 ficheros con comandos o paquetes MkDocs, 119 con alguna mención.
   - Tooling: `build_docs_zip.py` (`--builder`), `check_env.py` (`REQUIRED_TOOLS` con `mkdocs`) y
     `start-server.py` (docstring).
   - Requisitos: `mkdocs`, `mkdocs-material`, `mkdocs-material-extensions` y `mkdocs-get-deps`.
   - CI: `ci.yml` (`mkdocs build --strict` + paso de paridad), `docs-release.yml`
     (`--builder mkdocs`) y `docs-zip-release.yml` (`mkdocs build`). Además, `.vscode/tasks.json`.
   - Producto: `document_project.prompt.md` (input «Generador: `mkdocs-material` por defecto |
     `zensical`», señal 2 = `hooks: [mkdocs_hooks.py]`), `TEMPLATE_mkdocs.yml`, plantillas del
     kit, `bootstrap_ai_config`, agentes y `DOCUMENTATION_STANDARD.md`.
   - Docs: unas 30 páginas, ADR-001 y ADR-003.

## Decisiones
- **D1** — Arreglar el logo con `extra.homepage`, no quitando `navigation.indexes`: es una línea,
  no cambia ninguna URL y mantiene la pestaña «Inicio» de v0.7.0.
- **D2** — La comprobación sin servidor considera enlace a carpeta cualquier URL local cuyo último
  segmento sea `.` o `..` o que termine en `/`. `""` y las que solo llevan `#` siguen siendo
  válidas. El 404 no se excluye.
- **D3** — P1 y P2 en commits separados y una release de parche (v0.11.4) antes de la migración.
- **D4** — Zensical estándar único; MkDocs fuera (decisión del usuario, arriba).
- **D5** *(propuesta; confirmar)* — Se mantienen los nombres heredados `mkdocs.yml` y
  `mkdocs_hooks.py`:
  - Zensical lee `mkdocs.yml` de forma nativa, y `doc_trace llms`, `kit.py`, los tests de
    conformidad, la Fase 0b y todos los destinos dependen de ese nombre.
  - Pasar a `zensical.toml` o renombrar el módulo post-build se deja para una sesión posterior,
    cuando Zensical lo pida (p. ej., si deja de leer `mkdocs.yml`).
  - «MkDocs fuera» significa: sin paquetes, sin comandos y sin build MkDocs.
- **D6** *(propuesta; confirmar)* — Destinos existentes en MkDocs:
  - `/document-project` los migra en su Fase 0b al ejecutarse (protocolo ACTUALIZAR).
  - La migración quita `hooks:`, cambia el build al pipeline, valida los plugins contra
    `ZENSICAL_SUPPORTED_PLUGINS` y lo deja reflejado en el RESUMEN.
  - Si algún plugin no está soportado, la migración **se detiene y lo informa**: nunca pierde
    funcionalidad en silencio.
  - No hay migración masiva fuera de `/document-project`.

## Fases

### Bloque 1 — Arreglo y F7 (sin cambios de alcance)

#### P1 · `fix(docs): el logo enlaza a index.html y el ZIP sin servidor lo comprueba`
- `mkdocs.yml`: `extra.homepage: index.html`, con un comentario que explique el motivo.
- `scripts/build_docs_zip.py::_offline_problems`: regla D2.
- `tests/test_build_docs_zip.py`:
  - Nuevos casos `href=".."`, `href="./.."`, `href="."` y `href="/doc_ia/."` → enlace a carpeta.
  - `href=""` → sin problema.
- Producto: `extra.homepage` en `TEMPLATE_mkdocs.yml` y en la plantilla del estándar §4; checklist
  de la Fase 0b (`document-project.md` 118/139 y `document_project.prompt.md` 549).
- `tests/test_docs_conformance.py`: `extra.homepage == "index.html"` en `mkdocs.yml` y en la
  plantilla.
- `.claude/EDGE_CASES.md` (`[mkdocs.yml] navigation.indexes + offline`), `CHANGELOG.md` (Fixed),
  re-sellados y `llms --check`.

#### P2 · `build(deps): Zensical 0.1.1` (F7)
- Leer las notas de versión de 0.1.0 y 0.1.1.
- `zensical==0.1.1` + `zensical-ui==0.0.42` en `requirements-dev.txt` y `requirements.txt`.
- `test_mermaid_assets.py`: buscar el bundle en `zensical_ui`, o en `zensical` si es anterior.
- Revisar `ZENSICAL_SUPPORTED_PLUGINS`.
- `hooks:` sigue ignorado → `EDGE_CASES` y ADR-003.
- `CHANGELOG.md` (Changed).

**VERSION v0.11.4** (merge, tag y push por separado, con confirmación).

### Bloque 2 — Zensical estándar único (D4); sustituye a F8, F9, F12 y F13

#### Z1 · `feat(build)!: Zensical como único generador de doc_ia` (F8 + F13)
- Tooling:
  - `build_docs_zip.py` construye solo con Zensical: se retiran `--builder` y `HOOKLESS_BUILDERS`,
    y siempre se ejecutan el pre y el post-build.
  - `check_env.py`: `REQUIRED_TOOLS` con `zensical` en lugar de `mkdocs`; docstrings.
  - Docstring de `start-server.py`.
  - Tests de los tres.
- Dependencias:
  - `requirements-docs.txt`: `zensical`, `zensical-ui`, `pymdown-extensions` y `PyYAML`
    explícito.
  - Fuera `mkdocs`, `mkdocs-material`, `mkdocs-material-extensions` y `mkdocs-get-deps`, de
    todos los ficheros de requisitos.
- `mkdocs.yml`: se quita la clave `hooks:` (Zensical la ignora). El sync de los ficheros raíz
  sigue en el pipeline y en el hook PostToolUse de Claude Code.
- CI y workflows:
  - `ci.yml`: build Zensical **bloqueante** vía `build_docs_zip.py`; fuera el paso
    `mkdocs build` y la paridad.
  - `docs-release.yml` y `docs-zip-release.yml` solo usan `build_docs_zip.py`.
  - `.vscode/tasks.json`.
- Tests:
  - `test_mermaid_assets.py` sin el caso `material`.
  - `test_offline_assets.py` y `test_zensical_compat.py` revisados.
  - **Nuevo test de guarda**: no quedan comandos `mkdocs build|serve` ni el paquete
    `mkdocs-material` en código, instrucciones, plantillas y docs vivas. Excepciones: ADR-001,
    CHANGELOG, `.ai/sessions/` y la sección histórica de `EDGE_CASES`.
- ADRs: ADR-003 pasa a ACEPTADO y se reescribe sin escalonado ni fallback (C2 y C5 retiradas,
  C3 y C10 cumplidas); ADR-001 pasa a `REEMPLAZADO POR ADR-003`.
- `EDGE_CASES`: las entradas solo de MkDocs pasan a una sección «Histórico (MkDocs)».
- Commit con pie `BREAKING CHANGE: build_docs_zip.py ya no acepta --builder; MkDocs no se soporta`.

#### Z2 · `docs: Zensical como generador de doc_ia en instrucciones y documentación` (F9)
- Instrucciones:
  - `SHARED_INSTRUCTIONS.md`, `CLAUDE.md`, `GEMINI.md`, `copilot-instructions.md`,
    `.cursorrules`, `AGENTS.md` e `INTEGRATION_MAP.md`.
  - `.github/instructions/{docs,sync,python}`.
  - `.ai/{runtime,architecture,standards,product,glossary}.md`.
- Docs (unas 30 páginas): `index`, `installation`, `quickstart`, `architecture` y `downloads`;
  `api/`, `functional/` y `examples/` de `build_docs_zip`, `check_env`, `document_project`,
  `archetypes` y `bootstrap`; las guías; `ai-config/claude.md`; `README.md`, `CONTRIBUTING.md` y
  `VER_DOCUMENTACION.md`.
- Comandos de sustitución:
  - Construir: `python scripts/build_docs_zip.py` (o `python -m zensical build --strict` tras el
    sync).
  - Servir: `python -m zensical serve`.
  - Se avisa de que `serve` no sincroniza los ficheros raíz.
- Checklist de sincronización de `CLAUDE.md`, re-sellados y `llms --check`.

#### Z3 · `feat(prompts)!: Zensical como único generador para proyectos destino` (F12 + D6)
- Input `Generador` de `/document-project`:
  - Se elimina la pregunta: el generador es siempre Zensical.
  - Si el usuario pide MkDocs, se le responde que doc_ia ya no lo soporta y se ofrece migrar.
- Fase 0b: migración de destinos MkDocs según D6, con guarda de plugins.
- Fase 1, señal 2: solo la variante pipeline.
- Fase 7: `python -m zensical build --strict`.
- Fase 7b: Gap A2 solo en la variante Zensical.
- Ficheros:
  - `document_project.prompt.md`, `.claude/commands/document-project.md`, agentes
    `documentation-generator`, `documentation-reviewer` y `config-reviewer`.
  - `bootstrap_ai_config.prompt.md` (Capa B), `DOCUMENTATION_STANDARD.md` §4,
    `TEMPLATE_mkdocs.yml` y `VER_DOCUMENTACION.template.md`.
  - Kit (`DOCUMENTAR.template.md`, `documentar.prompt.template.md`) y `kit.py` si cambia la
    instancia.
  - Docs de producto `{functional,api,examples}` de `document_project`, `bootstrap` y
    `archetypes`.
- Tests de conformidad del producto (validación de inputs, plantilla, kit).

#### Z4 · F10 reducido · `feat(docs): ZIP sin conexión completo`
- Ya hecho en `a43ebcc`: `use_directory_urls: false`, `offline` y el shim local de iframe-worker.
- Pendiente:
  - Decidir sobre `privacy`. El riesgo de symlinks en Windows desaparece con MkDocs fuera, pero
    hay que confirmar que Zensical soporta `privacy`.
  - C8: ZIP con `file://` — búsqueda, Mermaid, navegación y logo.
  - Texto de la release en `docs-zip-release.yml`.

#### Z5 · Plan de la migración y sesión al día
- `2026-10-28d_zensical_migration/{02_PLAN_FASES,TRACEABILITY}.md`:
  - F7 hecha.
  - F8, F9, F12 y F13 sustituidas por Z1-Z3 (referencia a esta sesión).
  - C2 y C5 retiradas por D4.
- `INDEX.md` y `TRACEABILITY.md`.

**VERSION v1.0.0? / v0.12.0** *(a decidir en `/version-closure`)*:
- Z1 y Z3 son BREAKING. Con versión 0.x, SemVer permite un salto menor (v0.12.0).
- Merge, tag y push por separado, con confirmación.

### Orden
P1 → P2 → (CI en verde con 0.1.1) → C3 → Z1 → Z2 → Z3 → Z4 → Z5.

## AUDIT_PLAN

### Bloque 1
| # | Hallazgo | Severidad | Tratamiento |
|---|---|---|---|
| A1 | Logo roto con `file://` en el ZIP **publicado** desde v0.7.0, MkDocs incluido, sin detectar durante 8 días: hueco en la comprobación (`.`, `..`) y paridad no bloqueante. | Alta | P1 + regla D2 con tests. |
| A2 | La conclusión del run (`success`) ocultó el fallo de paridad. | Media | Con D4 se resuelve de raíz: Z1 hace bloqueante el build de Zensical. Hasta Z1, revisar las anotaciones. |
| A3 | Los destinos documentados con la plantilla de v0.7.0 en adelante tienen el logo roto. | Media | P1 corrige la plantilla y la Fase 0b. Los destinos se corrigen en su próxima ejecución (junto con la migración D6). |
| A4 | `zensical-ui` es un paquete nuevo (cadena de suministro) y el bundle cambia de sitio. | Media | Versión exacta de los dos; el test sigue al paquete nuevo. |
| A5 | C9 (Mermaid sin conexión) se verificó con 0.0.73. | Media | **C-b** antes del commit de P2: repetir C9 con 0.1.1 y unpkg bloqueado. |
| A6 | Las notas de versión de 0.1.x no se leyeron en el spike. | Baja | **C-a** antes de P2. |
| A7 | `mkdocs.yml` es fuente sellada: `drift` marcará páginas. | Baja | Re-sellado tras revisar cada página. |
| A8 | El 404 usa URLs absolutas. | Informativo | Solo lo sirve un servidor. Fuera de alcance. |

### Bloque 2 (D4)
| # | Hallazgo | Severidad | Tratamiento |
|---|---|---|---|
| B1 | **Sin fallback.** Zensical 0.1 es joven (releases cada pocos días) y un fallo del generador bloquea la documentación y las releases de docs. | Alta | Versión exacta de `zensical` y `zensical-ui`; actualizar solo de forma deliberada, con `test_zensical_compat`, el spike de rutas y C9. Rollback = revertir Z1 (los requisitos MkDocs vuelven con el revert). Los ZIP ya publicados no se tocan. |
| B2 | Se retira la paridad, que era la única prueba objetiva de equivalencia antes de quitar MkDocs. | Media | **C3 pasa a ser obligatoria antes de Z1**: revisión visual completa del sitio Zensical 0.1.1 (portada, pestañas, barra lateral con `nav.css`/`sidebar-toggle.js`, tablas, admonitions, pestañas de contenido, código, búsqueda, claro/oscuro y móvil). Mermaid ya está cubierto por C9. Diff de rutas vacío (ya verificado). |
| B3 | Superficie amplia (67 + 119 ficheros): alto riesgo de dejar comandos MkDocs sueltos y de deriva entre instrucciones. | Media | Un commit por capa (Z1 tooling, Z2 docs, Z3 producto). El test de guarda de Z1 bloquea las regresiones. Revisión de Z3 con el agente Documentation Reviewer. |
| B4 | **Cambio de contrato para los destinos.** El plan anterior decía «respetar el generador existente; no migrar de forma implícita», y D4 lo invierte. Destinos afectados conocidos: socyalpro, dpss y UFV. | Alta | D6: la migración es explícita (Fase 0b la anuncia y la registra en el RESUMEN), con guarda de plugins que **detiene** en lugar de degradar. Las sesiones `.ai/` del destino registran el cambio. |
| B5 | Sin `hooks:`, `python -m zensical build` a secas no sincroniza `CHANGELOG`/`CONTRIBUTING` → `--strict` falla con «page does not exist». | Media | Comando canónico = `build_docs_zip.py`; documentarlo en Z2. El hook PostToolUse ya sincroniza en local, y `EDGE_CASES` mantiene la entrada. |
| B6 | Z1 cambia la CLI de `build_docs_zip.py` (`--builder` desaparece). Rompe a quien lo invoque con `--builder` (workflows propios y destinos con copia del script). | Media | BREAKING declarado. Alternativa más suave: aceptar `--builder zensical` como no-op durante una versión y rechazar `mkdocs` con un mensaje claro. **Recomendado.** |
| B7 | ADR-003 se escribió como escalonado (C1-C5, fallback hasta 2027-05-05). | Baja | Reescritura en Z1: decisión de 2026-11-12 sin escalonado. Las alternativas rechazadas se actualizan («Migrar ya, sin escalonar» pasa a ser la elegida, con B1 como consecuencia asumida). |
| B8 | `mermaid-theme.js` fuerza `theme: "default"` por un problema de Material + Mermaid v12. Sin Material, ya no hace falta. | Baja | Mantenerlo (es inocuo y Zensical ya pasa `default`). Simplificarlo, en otra sesión. |
| B9 | Los nombres `mkdocs.yml` y `mkdocs_hooks.py` se quedan con D4 en vigor (D5): pueden confundir. | Baja | Explicarlo en `architecture.md` y el glosario: «nombre heredado; lo lee Zensical». |
| B10 | `privacy` en Zensical sin verificar. | Baja | Z4 lo comprueba antes de decidir. |

**DoD común**:
- ruff, mypy strict y pytest en verde.
- `build_docs_zip.py` con exit 0.
- `doc_trace.py drift|decisions|llms --check` sin hallazgos.
- CI en verde.
- Desde Z1: build Zensical bloqueante y test de guarda sin MkDocs.

## Veredicto
- **P1: GO.**
- **P2: GO_CONDICIONAL** a C-a (notas de versión) y C-b (C9 con 0.1.1).
- **Z1: GO_CONDICIONAL** a:
  - P2 publicado y CI en verde con 0.1.1;
  - **C3** completa (B2);
  - confirmación de D5 y D6;
  - decisión sobre B6 (no-op temporal o corte directo).
- **Z2: GO tras Z1.**
- **Z3: GO_CONDICIONAL** a D6 confirmada y revisión del Documentation Reviewer.
- **Z4: GO_CONDICIONAL** a C8 (y a B10 si se añade `privacy`).
- **Z5: GO.**
- **Retiradas por D4:** C2 (2 semanas de paridad) y C5 (fecha límite 2027-05-05).
