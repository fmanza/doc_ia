# TRACEABILITY

## Session metadata
- id: 2026-11-13b
- fecha: 2026-11-13
- rama: develop
- skill: hotfix
- fase: IMPLEMENT + VERSION (CLOSED, v0.13.1)

## Prompt issued
1. Pendientes de UFV: quitar `--builder` en su Fase 0b y revisar PRE frente a `origin/evaluados`.
2. «si» → commit en UFV y hotfix en doc_ia.

## Context supplied
- UFV `.ai/doc_state.json`: 30 de las 39 rutas de kuniv con `\r` final (baseline del 2026-11-13).
- `scripts/doc_trace.py` (`_paths_arg`, `check_changes`).

## AI output summary
- Causa: `_paths_arg` no quitaba espacios ni saltos de línea de `--path`; una lista de rutas leída
  de un fichero CRLF guardaba `ruta\r`, y `changes` la pasaba tal cual a git como pathspec, que no
  coincidía con nada → cambios en esas rutas invisibles (estado C falso).
- Arreglo: `_normalize_path` (`strip()` + normalización previa) en `--path`; los valores en blanco
  se ignoran; `check_changes` normaliza también las rutas guardadas (baselines antiguas válidas sin
  repetirlas).
- Tests: `test_paths_with_carriage_return_are_stripped`,
  `test_stored_paths_with_carriage_return_still_detect_changes` (fallan sin el arreglo).
- Verificación: suite completa OK, ruff, ruff format y mypy limpios.
- UFV: Fase 0b a 0.13.0 y baseline con rutas limpias (commit `b4bb813` en UFV).

## Corrección posterior
- CI rojo tras `ae0fb49`: `drift` (no se ejecutó en local). `docs/api/doc_trace.md` y
  `docs/functional/doc_trace.md` decían que las rutas se comparaban «sin normalizar» (ya era
  falso antes del hotfix); se describe `_normalize_path`, se añade AC-35 (35/35) y se re-sella
  (`e1f7f46`).
- CHANGELOG e INDEX con un carácter CR real en lugar del texto `\r`: corregido en la release.

## VERSION
- `release: v0.13.1` (parche): `pyproject.toml`, `.ai/product.md`, `VER_DOCUMENTACION.md`,
  descargas, referencia, ejemplos del kit, CHANGELOG (`[0.13.1]`) y `docs/changelog.md`.
- Pasos por separado: commit en `develop` → CI verde → merge `--no-ff` a `main` → push → CI y
  `docs-v0.13.1` → tag `v0.13.1` sobre el merge verificado → push del tag.
