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
| F2 | `ci(docs): build de paridad con Zensical (no bloqueante)` | (este commit) | HECHO |
| F3-F12 | ver `02_PLAN_FASES.md` | — | PENDIENTE |

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

## Veredicto final
Veredicto: F0-F5, F11 GO · F6 GO_CONDICIONAL (C6, C7) · F7 gate 0.1 · F8 gate C2-C5 ·
F9/F10/F12 tras F8
Pendientes al cierre:
- GO del usuario para ejecutar F1.
