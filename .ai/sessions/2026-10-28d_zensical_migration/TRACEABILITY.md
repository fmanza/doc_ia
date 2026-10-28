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
| F6a | `fix(docs): diagrama Runtime de architecture con nodo paralelogramo inválido` | (este commit) | HECHO |
| F6-F10, F12 | ver `02_PLAN_FASES.md` | — | PENDIENTE |

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

## Veredicto final
Veredicto: F0-F5, F11 GO · F6 GO_CONDICIONAL (C6, C7) · F7 gate 0.1 · F8 gate C2-C5 ·
F9/F10/F12 tras F8
Pendientes al cierre:
- GO del usuario para ejecutar F1.
