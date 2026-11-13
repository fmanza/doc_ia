# TRACEABILITY

## Session metadata
- id: 2026-11-13b
- fecha: 2026-11-13
- rama: develop
- skill: hotfix
- fase: IMPLEMENT (CLOSED)

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

## Pendiente
- Publicar en una versión de parche (0.13.1) cuando se decida.
