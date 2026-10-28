# TRACEABILITY

## Session metadata
- id: 2026-10-28b
- fecha: 2026-10-28
- rama: develop
- skill: hotfix
- fase: PLAN + AUDIT_PLAN + IMPLEMENT + AUDIT_CODE + VERSION

## Prompt issued
"Adelante con todo" — hotfix propuesto tras P2 para `--device auto` en `convert_to_md.py`.

## Context supplied
- Hallazgo de la sesión `2026-10-28_archetypes_v2` (AUDIT_CODE P1).
- `scripts/convert_to_md.py::_detect_device`, `tests/test_convert_to_md.py` (tests de dispositivo).

## AI output summary
- **Causa raíz**: el módulo inyecta `CUDA_VISIBLE_DEVICES=""` al importarse (para evitar el
  bloqueo de `import torch`) y `_detect_device("auto")` no distinguía ese valor de un `""`
  exportado por el usuario → siempre CPU.
- **Fix mínimo**: flag de módulo `_CUDA_ENV_INJECTED` calculado antes de inyectar; `auto`
  ignora el `""` solo si lo inyectó el módulo. Los 4 imports stdlib (`dataclasses`, `datetime`,
  `pathlib`, `typing`) suben por encima del bloque para cumplir E402 (no cargan torch).
- **Tests**: nuevo `test_detect_device_auto_ignores_import_default`; 
  `test_detect_device_respects_existing_env_empty` ahora fija `_CUDA_ENV_INJECTED=False` para
  modelar explícitamente el valor del usuario (antes dependía de si la máquina tenía GPU).
- **Reproducción real** (subproceso, sin variable previa, GPU simulada): antes `auto -> cpu`,
  después `auto -> cuda`.
- Verificación: pytest 77 OK; ruff OK; mypy sin errores nuevos (10 preexistentes por docling).
- Docs: marcas ⚠️ retiradas en `docs/functional/convert_to_md.md`, `docs/api/convert_to_md.md`,
  `docs/reference/index.md`; CHANGELOG `[Unreleased] › Fixed`.

## AUDIT_CODE
- **Regresiones**: `--device cpu` y `--device cuda` no cambian; `auto` con valor del usuario
  (`""` o `"0"`) se sigue respetando.
- **Edge cases**: si el usuario exporta `""` antes de ejecutar, `_CUDA_ENV_INJECTED=False` y
  `auto` resuelve a CPU (comportamiento documentado).
- **Compatibilidad**: sin cambios de CLI ni de API pública.

## Directrices para Futuras IAs
- **[convert_to_md]**: no asignar variables antes de los imports salvo vía `os.environ`/`sys.path`
  (ruff E402 solo exime esas mutaciones); el flag va tras los imports stdlib.

## Veredicto final
Veredicto: GO
Rollback: `git revert <commit>` (un commit, dos ficheros de código + docs).
