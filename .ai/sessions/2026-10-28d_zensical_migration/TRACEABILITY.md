# TRACEABILITY

## Session metadata
- id: 2026-10-28d
- fecha: 2026-10-28
- rama: develop
- skill: new_feature (E1) + refactor (E2) — solo planificación
- fase: PLAN + AUDIT_PLAN

## Prompt issued
"Actualmente se está usando mkdocs y se quiere migrar a zensical, se requiere valorar el impacto y
que el funcionamiento sea el mismo y proponer mejoras si es necesario. Dime también si es
recomendable la migración. Puede consultarse información en internet. PLAN y AUDIT_PLAN".

## Context supplied
- Código real: `mkdocs.yml`, `hooks/sync_root_docs.py`, `mkdocs_hooks.py`, `scripts/build_docs_zip.py`,
  `scripts/check_env.py`, `scripts/doc_trace.py`, `docs/assets/`, workflows, `requirements-*.txt`,
  ADR-001, `.claude/EDGE_CASES.md`.
- Web: PyPI (`zensical`, `mkdocs-material`), zensical.org (compatibility/configuration, plugins,
  offline, validation), blog de Material (maintenance, MkDocs 2.0).
- Spike: venv aislado en scratchpad con zensical 0.0.73 sobre una copia del repo (sin tocar el repo).

## AI output summary
- `01_PLAN_AUDIT.md`: contexto externo, spike MkDocs vs Zensical, PLAN en 3 etapas, 6 mejoras,
  AUDIT_PLAN con riesgos F/T/S, condiciones C1-C5 y recomendación.
- Hallazgo clave: Zensical **ignora `hooks:` en silencio** → sin sync de `CHANGELOG/CONTRIBUTING`
  (strict falla) y sin ZIP latest (enlaces de `downloads.md` rotos sin aviso).
- Hallazgos colaterales: doble carga de Mermaid (nativa + CDN); el ZIP "offline" depende de CDN.

## Iteración 2 — plan por fases
- Prompt: "Queremos un PLAN y AUDIT_PLAN. Empezamos ya y preparamos el siguiente paso para
  actualizar a Zensical 0.1. Quiero todos por fases independientes y con su commit".
- Decisiones: D1 = empezar ya; M2, M3 y Etapa 3 incluidas ("todos").
- Spike adicional: `offline` + `privacy` con MkDocs/Material 9.8.0 en Windows → strict abortado
  (78 avisos de symlink); con Zensical, OK ⇒ M2 se mueve detrás del cambio de default.
- `02_PLAN_FASES.md`: F0-F12 con dependencias, ficheros, commit, AUDIT y veredicto por fase.

## Fases y commits
| Fase | Commit | SHA | Estado |
|---|---|---|---|
| F0 | `docs(session): plan por fases de la migración a Zensical` | `64ab29e` | HECHO |
| F1 | `feat(build): pipeline sin hooks para construir con Zensical` | `28fd055` | HECHO |
| F2 | `ci(docs): build de paridad con Zensical (no bloqueante)` | `dd9266d` | HECHO |
| F3 | `feat(env): check_env informa de Zensical como generador opcional` | `767e97b` | HECHO |
| F4 | `test(docs): guardas de compatibilidad con Zensical` | `d7b89f6` | HECHO |
| F5 | `docs(adr): ADR-003 Zensical como generador por defecto (propuesto)` | `5cc8bfc` | HECHO |
| F11 | `feat(prompts): soporte completo de Zensical en document_project` | `d059533` | HECHO |
| F6a | `fix(docs): diagrama Runtime de architecture con nodo paralelogramo inválido` | `a96de4b` | HECHO |
| F6 | `refactor(docs): Mermaid con la integración nativa del tema` | `f370cbf` | HECHO |
| — | push de `develop` (`6ee016a..f370cbf`) → CI run 40743109579: 3.12 y 3.14 en verde | — | HECHO |
| F2b | `ci(docs): resultado de la paridad Zensical visible como anotación` | `b20b015` | HECHO |
| — | CI run 40743567252 (`b20b015`): verde; anotación `Paridad Zensical - OK` en 3.12 y 3.14 → arranca C2 | — | HECHO |
| — | `chore(ci): actions de GitHub a sus versiones mayores actuales (Node 24)` | `4b9b45e` | HECHO |
| — | CI run 40757387496 (`4b9b45e`): verde, sin avisos de Node 20; paridad OK en 3.12 y 3.14 | — | HECHO |
| — | `docs(trace): aclarar que stamp --source sustituye la lista de fuentes` | `bf7763e` | HECHO |
| — | CI run 40757783481 (`bf7763e`): verde; paridad OK en 3.12 y 3.14 | — | HECHO |
| VERSION | `release: v0.2.0 - …` (`03_VERSION_CLOSURE.md`); CI run 40758754780 verde | `d619d59` | HECHO |
| VERSION | merge `--no-ff` a `main`; CI run 40759057725 verde; release `docs-v0.2.0` (run 40759057543) | `2e8da9d` | HECHO |
| VERSION | tag `v0.2.0` sobre `2e8da9d` → release `v0.2.0` con `doc_ia-docs-0.2.0.zip` (run 40760807978) | `2e8da9d` | HECHO |
| F7-F10, F12 | ver `02_PLAN_FASES.md` | — | PENDIENTE (gates) |

### F1 — verificación
- DoD local (`.venv`, Python 3.14): ruff, format, mypy, pytest **177**, drift 0, matrix
  **48/70**, `llms --check`, `mkdocs build --strict` → OK.
- Build real con Zensical 0.0.73 (venv del scratchpad):
  `build_docs_zip.py --builder zensical` → sync, "No issues found", `site/doc_ia-docs-latest.zip`
  + `.sha256` y ZIP versionado.
- Observación (sin cambio, comportamiento previo también con MkDocs): el ZIP versionado incluye el
  ZIP `latest` porque empaqueta `site/` entero (≈1,25 MB frente a ≈0,63 MB). Candidato a mejora
  menor fuera de este plan.

### F2 — verificación
- `.venv`: `pip install zensical==0.0.73` solo añade `deepmerge 4.0.0`, `tomli 2.5.0` y `zensical`
  (sin cambiar versiones existentes); `requirements.txt` recibe esas 3 líneas.
- venv limpio con `requirements-dev.txt` (Python 3.14.3): `pip check` OK y secuencia completa de
  `ci.yml` en verde, incluido el paso nuevo (Zensical "No issues found" + ZIP `latest` presente).
- **Preparación de F7**: el salto a 0.1 = cambiar `zensical==0.0.73` en `requirements-dev.txt` y
  `requirements.txt` (+ dependencias nuevas que traiga) y seguir el runbook de `02_PLAN_FASES.md`.

### F3 — verificación
- `check_env.py` con `.venv` (Zensical instalado): sin aviso de Zensical, código 0.
- venv sin Zensical y `PYTHONIOENCODING=cp1252`: aviso de Zensical como primer `⚠`, código 0.
- Corrección arrastrada de F1: la fila de Evidencia «ZIP offline» del Mapa Funcional decía 5/6
  (la tabla ya decía 7/8); se corrige en este commit.

### F4 — verificación
- **Desviación del plan**: las guardas van en `tests/test_zensical_compat.py` (nuevo) y no en
  `tests/test_docs_conformance.py`, que verifica arquetipos y es fuente sellada de
  `api/archetypes.md` y `functional/archetypes.md`: evita re-sellar páginas no relacionadas.
- Mutaciones (revertidas tras comprobarlas): plugin `git-revision-date` añadido →
  falla la guarda de plugins; `use_directory_urls: false` → falla la de enlaces (`../` sale de
  `site/`, el caso previsto para F10); nombre de ZIP cambiado en `downloads.md` → falla.

### F5 — verificación
- ADR-003 MADR 4.0 FULL (5 secciones) con C1-C5; ADR-001 conserva ACEPTADO y enlaza la propuesta.
- Ajuste del plan: en F8 ADR-001 pasa a `REEMPLAZADO POR ADR-003` (vocabulario de
  `architecture_doc.prompt.md`), no "SUSTITUIDO".
- Nav + `llms.txt` (+1 entrada); re-sellado por `mkdocs.yml` de `api/archetypes`,
  `api/document_project`, `functional/build_docs_zip` y `reference/index` (contenido no afectado).
- DoD completa en verde; el ADR se genera con MkDocs y con Zensical.

### F11 — verificación
- DRY: una única sección canónica (`document_project.prompt.md` § *Reglas por generador:
  Zensical*). Fases 1, 5, 7 y salida 8b, slash command, agentes Generator/Reviewer,
  `docs.instructions.md` y `DOCUMENTATION_STANDARD.md` §2.1 remiten a ella.
- Contenido: `TIENE_PIPELINE_SIN_HOOKS`, Gap A4, `mkdocs_hooks.py` como plantilla invocada por
  el script, `default="zensical"` en el Paso B1, plugins soportados, comandos de build/serve,
  enlaces de `downloads.md` según `use_directory_urls`/`offline`, versión exacta.
- Páginas: `functional/document_project.md` (regla, flujo alternativo, AC-08 sin test) y
  `api/document_project.md` actualizadas. `functional/archetypes`, `functional/origin_types` y
  `api/archetypes` revisadas: no describen el generador → solo re-sellado.
- No se ha ejecutado `/document-project` con Zensical sobre un destino real: la regla se
  validará en la primera sesión de ese tipo (AC-08 sin test, como el resto del flujo IA).

### Verificación visual de Mermaid (C6) — método
- Edge headless no devuelve `--dump-dom` por stdout en esta máquina. Se usa CDP desde Python
  (`websockets`): `Emulation.setEmulatedMedia` (claro u oscuro), `DOM.getDocument(pierce=True)`
  para leer los shadow roots **cerrados** de Material, y una captura recortada por diagrama.
  Scripts en el scratchpad de la sesión (`mermaid/cdp_check.py`), no versionados.
- Hallazgo: con la config actual (CDN + `assets/js/mermaid.js`), la integración nativa de Material
  pinta el diagrama visible en un shadow root cerrado. El `mermaid.run()` propio llega tarde y
  deja un SVG de error **oculto** en el DOM normal de cada bloque (23/23). Al usuario solo le
  llega el render nativo.

### F6a — hotfix encontrado durante C6
- Línea base (MkDocs, claro): 22/23 diagramas visibles bien; el que falla es `architecture.md`
  #2 (Runtime): `B[/document-project…]` → paralelogramo de Mermaid 11 → «Syntax error in text».
  Ocurría también en el render nativo: error real, independiente de F6.
- Arreglo: `B[Comando document-project…]` → 23/23 y captura revisada.
- Regresión: `test_mermaid_nodes_do_not_start_with_slash` (falla sin el arreglo, pasa con él).

### F6 — verificación (C6 y C7 cumplidas)
- **C6**: sin CDN ni `assets/js/mermaid.js`, 23 diagramas (flowchart, sequence, ER) × MkDocs y
  Zensical × claro y oscuro = **92/92 visibles**, 0 errores y sin scripts de Mermaid en la página
  (los carga el tema). Capturas revisadas: flowchart y sequence en oscuro, ER en claro, diagrama
  de F1 y Runtime corregido en oscuro (Zensical). En oscuro, el tema aplica sus colores.
- **C7**: la configuración de doc_ia tras F6 es la de socyalpro (sin CDN, con `custom_fences`):
  renderiza. Contraprueba sin `custom_fences` → ningún `.mermaid`, el diagrama sale como código.
  La causa real de 2026-06-12a era la ausencia de `custom_fences`, no la del CDN.
- Producto: Fase 0b/5 de 4 → 3 assets y retirada activa del CDN/`mermaid.js` en destinos
  (el plan decía "se tolera"; la evidencia de errores ocultos justifica retirarlos).
- Limitación conocida (sin cambio): el tema carga Mermaid desde CDN → el ZIP offline necesita
  red para los diagramas hasta F10 (`privacy`).

### Primer push y CI en GitHub (repo ya público)
- Los 3 runs anteriores en `develop` (`7718e2d`, `b6f80ab`, `6ee016a`) **no llegaron a arrancar**:
  "recent account payments have failed or your spending limit needs to be increased". Era
  facturación de Actions con el repo privado, no el código. Con el repo público, el run
  40743109579 (`f370cbf`) arranca y termina en verde en 3.12 y 3.14 (todos los pasos).
- **C4 de 2026-10-28c cerrada**: CI validada en GitHub, incluida la matriz 3.12.
- Los logs de jobs piden permisos de admin incluso en repo público, y `continue-on-error` marca el
  paso de paridad como `success` aunque falle → **F2b**: paso final que publica
  `steps.zensical.outcome` como anotación `Paridad Zensical` (legible con
  `GET /repos/fmanza/doc_ia/check-runs/<job>/annotations`). Así se mide C2 (≥ 2 semanas en verde).
- Avisos de GitHub (sin impacto hoy): `actions/checkout@v4` y `actions/setup-python@v4` apuntan a
  Node 20 y se ejecutan forzados en Node 24; `ubuntu-latest` migra a Ubuntu 26 desde el
  2026-10-19. Candidato a `chore(ci)`: subir a las versiones mayores actuales de esas actions.

### F2b — verificación
- Run 40743567252 (`b20b015`) en verde; anotaciones del paso nuevo: `Paridad Zensical - OK (Python 3.12)`
  y `OK (Python 3.14)`. **C2 empieza a contar el 2026-10-28** (F8 no antes del 2026-11-11).

### chore(ci) — actions a Node 24 (fuera del plan, a petición del usuario)
- Versiones consultadas en la API de GitHub (2026-10-28): `checkout` v7.0.1, `setup-python` v7.1.0,
  `upload-artifact` v7.0.2, `action-gh-release` v3.0.3; `ncipollo/release-action@v1` ya usa `node24`.
- Cambios rompedores revisados, sin impacto: setup-python v7 elimina `pip-install` (no se usa);
  checkout v7 bloquea PR de forks en `pull_request_target`/`workflow_run` (no se usan) y v6 guarda
  las credenciales en un fichero aparte; upload-artifact v7 añade `archive` (por defecto `true`, igual).

### Hallazgo — `stamp --source`
- Al re-sellar `docs/reference/index.md` con `--source <ruta>` la página se quedó con una sola
  fuente: `--source` sustituye la lista (diseño correcto para el primer sellado). Detectado en el
  diff antes del commit; `CLAUDE.md` lo mostraba como forma de re-sellar → aclarado en `bf7763e`.

### Incidente en la release v0.2.0
- `git merge … -F -` falló (`-F` no lee de stdin) y el `git tag` encadenado en el mismo comando se
  creó sobre el `main` antiguo (`6ee016a`) y se subió. El workflow `docs-release.yml` publicó una
  release `v0.2.0` con `doc_ia-docs-0.1.0.zip`.
- El borrado del tag remoto fue denegado por permisos (operación git destructiva): lo hizo el
  usuario (borrar release, borrar tag y recrearlo sobre `2e8da9d`). Release `v0.2.0` correcta.
- Tras la limpieza, la API pública no listaba la release `docs-v0.2.0` (el tag seguía). Se ejecutó
  a mano «📦 Build & Publish Docs ZIP» sobre `main` (run 40762456792, `workflow_dispatch`): release
  `docs-v0.2.0` con ZIP, `.sha256` y `CHECKSUMS.txt`. Conserva su `created_at` original (19:58),
  así que probablemente no llegó a borrarse y la consulta anterior fue un dato desactualizado.
- Lección: no encadenar merge, tag y push en un único comando; verificar el merge antes de etiquetar.

## Veredicto final
Veredicto: bloque A (F0-F6, F2b, F11) GO y publicado en **v0.2.0** (2026-10-28) · F6 C6/C7 cumplidas ·
F7 gate Zensical 0.1 · F8 gate C2-C5 (C2 desde 2026-10-28) · F9/F10/F12 tras F8
Pendientes al cierre:
- F7: al publicarse Zensical 0.1 en PyPI (anunciada 2026-11-05).
- F8: no antes del 2026-11-11, con C2-C5 cumplidas y GO del usuario.
