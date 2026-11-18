# TRACEABILITY

## Session metadata
- id: 2026-11-18
- fecha: 2026-11-18
- rama: develop
- skill: hotfix
- fase: IMPLEMENT + AUDIT_CODE (fix en `develop`; release pendiente de confirmación)

## Prompt issued
«sí, redacta también la dirección de PRE del DTUFV y abre /hotfix para los dos fallos», tras la
sesión UFV `2026-11-18` (origen MANUAL `06_Manuales`).

## Context supplied
- UFV `_fuentes/manuales/Manual de resolución de incidencias KUNIV v1.1.md` §2.5: «… y password
  p2=<GUID>» no detectado por `redact_secrets.py`.
- UFV `.ai/doc_state.json`: `doc_trace.py baseline` sin `--path` dejó kuniv sin `rutas` (39 → 0);
  restaurado desde git en el destino.

## AI output summary

### PLAN / causa raíz
1. `redact_secrets.py`: las reglas por palabra clave exigen el separador justo después de la
   palabra (`password\s*[=:(]`); con un nombre de parámetro en medio («password p2=…») ninguna
   coincide.
2. `doc_trace.py::_cmd_baseline`: `paths = _paths_arg(args) or DEFAULT_PATHS` ignoraba las `rutas`
   guardadas, y `write_baseline` las omite cuando el alcance es `.`. `changes` sí las reutilizaba.

### IMPLEMENT
- `redact_secrets.py`: regla `password_param` (palabra + hasta 40 caracteres de la misma línea sin
  `=`, `:` ni `(` + parámetro `\w{1,20}` + separador + valor), en `_NEEDS_NON_LETTER`; docstring.
- `doc_trace.py`: `stored_paths(entry)` (lectura normalizada, ya usada por `check_changes`) y
  `_cmd_baseline` la usa cuando no hay `--path`; `--path .` quita el alcance; ayuda de `--path`.
- Tests que fallaban antes del arreglo: 2 casos `password_param` en
  `test_detects_and_redacts_value_only`, `test_baseline_without_paths_reuses_stored_paths`; además
  4 casos de prosa que no deben detectarse y `test_baseline_path_dot_resets_to_whole_repo`.
- Documentación: `docs/api/{doc_trace,redact_secrets}.md`, `docs/functional/{doc_trace,
  redact_secrets,index}.md` (AC-36, 36/36), `docs/reference/index.md`; re-sellado; CHANGELOG
  `[Unreleased]`.

### AUDIT_CODE
- Regresión: quien omitía `--path` para volver al repositorio completo debe pasar `--path .`
  (documentado; test).
- Edge cases: «en p1 y p2 introducir el usuario y password anterior» (sin valor), «contraseña del
  usuario admin: obligatorio» (solo letras), «password (ver la sección 3)», valor ya redactado: no
  se detectan (tests).
- Compatibilidad: formato de `doc_state.json` sin cambios; baselines sin `rutas` siguen igual.
- Verificación: suite completa, ruff, ruff format, mypy, `drift`, `llms --check`, `decisions`.

## VERSION
- Commit: `fix: redact_secrets detecta password p2=<valor> y baseline conserva las rutas`.
- Changelog: `[Unreleased]` → `Fixed` (2 entradas).
- Rollback: `git revert <commit>`; en un destino afectado, repetir `baseline` con las `--path`
  originales.
- Release (0.13.2): pendiente de confirmación del usuario (merge, tag y push por separado).

## Veredicto
GO_CONDICIONAL — fix verificado en `develop`; falta la release.
